"""
Helper utilities for working with Google ADK agents.
"""
import asyncio
import json
import re
import os
import warnings
from typing import Any, Optional
from ..config import is_debug_mode


def run_agent_sync(agent, prompt: str) -> str:
    """
    Run an ADK agent synchronously using Runner.run_debug (simplified pattern from Kaggle notebooks).
    
    This follows the simpler pattern shown in Kaggle's "Day 2a - Agent Tools" notebook:
    - Create Runner with agent and session service
    - Use run_debug() which takes a string directly and handles everything
    - Extract text from returned events
    
    Args:
        agent: ADK Agent instance
        prompt: Input prompt for the agent (simple string)
        
    Returns:
        Response text from the agent
    """
    try:
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        import google.generativeai as genai
        
        # Get API key (required for ADK)
        api_key = _get_api_key()
        if not api_key:
            raise RuntimeError(
                "GOOGLE_API_KEY is not set. Please set it in your environment or .env file. "
                "ADK agents require a Google API key to function."
            )
        
        # Configure genai (ADK uses this internally)
        genai.configure(api_key=api_key)
        
        # Suppress warnings about non-text parts (function calls) in responses
        # These are normal when agents use tools and don't need to be surfaced to users
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*non-text parts.*")
            warnings.filterwarnings("ignore", message=".*non-text parts in the response.*")
            warnings.filterwarnings("ignore", category=UserWarning, module="google.*")
            warnings.filterwarnings("ignore", category=UserWarning)
            
            # Create Runner - simplified pattern from Kaggle notebooks
            session_service = InMemorySessionService()
            runner = Runner(
                app_name='agents',  # Use default to match ADK's expected app name
                agent=agent,
                session_service=session_service
            )
            
            # Use run_debug - simpler interface that takes string directly
            # This is the pattern shown in Kaggle notebooks
            # run_debug handles sessions, user_id, session_id automatically
            async def _run_with_debug():
                events = await runner.run_debug(prompt, quiet=True)
                return events
            
            # Handle both sync and async contexts (FastAPI runs in async event loop)
            # Note: uvicorn uses uvloop by default, which nest_asyncio can't patch
            # So we use a thread pool executor to run the async code in a separate thread
            try:
                # Check if we're in an async context (FastAPI)
                asyncio.get_running_loop()
                # We're in an async context - use thread pool executor
                # This works with any event loop type (asyncio, uvloop, etc.)
                import concurrent.futures
                def run_in_thread():
                    # Create new event loop in thread (standard asyncio, not uvloop)
                    new_loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(new_loop)
                    try:
                        return new_loop.run_until_complete(_run_with_debug())
                    finally:
                        new_loop.close()
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_thread)
                    events = future.result()
            except RuntimeError:
                # No event loop running - safe to use asyncio.run() directly
                events = asyncio.run(_run_with_debug())
            
            # Validate events before processing
            if events is None:
                raise RuntimeError("Runner returned None events - agent may have failed")
            
            # Debug: log events type
            if is_debug_mode():
                print(f"DEBUG [run_agent_sync]: Events type: {type(events)}")
                if hasattr(events, '__len__'):
                    print(f"DEBUG [run_agent_sync]: Events length: {len(events)}")
            
            # Convert to list if it's an async generator or other iterable
            if not isinstance(events, (list, tuple)):
                try:
                    events = list(events) if events else []
                except (TypeError, StopIteration) as e:
                    if is_debug_mode():
                        print(f"DEBUG [run_agent_sync]: Failed to convert events to list: {e}")
                    raise RuntimeError(f"Failed to process events: {e}. Events type: {type(events)}")
            
            # Extract text from all events (following Kaggle notebook pattern)
            response_parts = []
            try:
                for event in events:
                    text = _extract_text_from_event(event)
                    if text:
                        response_parts.append(text)
            except TypeError as e:
                raise RuntimeError(f"Failed to iterate over events: {e}. Events type: {type(events)}")
            
            result = "".join(response_parts).strip()
            
            # Debug output
            if is_debug_mode():
                print("\n" + "="*80)
                print("DEBUG [run_agent_sync]: Agent Response")
                print("="*80)
                print(f"Response type: {type(result)}")
                print(f"Response length: {len(result)} characters")
                print(f"Number of events processed: {len(events)}")
                print(f"Response (first 1000 chars):\n{result[:1000]}")
                if len(result) > 1000:
                    print(f"... ({len(result) - 1000} more characters)")
                print("="*80 + "\n")
            
            if result:
                return result
            
            raise RuntimeError("Runner returned no text response")
        
    except ImportError as e:
        raise RuntimeError(
            f"Required ADK components not available: {e}. "
            "Make sure google-adk is properly installed."
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to run ADK agent: {e}. "
            "Make sure GOOGLE_API_KEY is set and valid."
        ) from e


def _build_agent_prompt(agent, user_prompt: str) -> str:
    """Build a full prompt including agent instructions."""
    parts = []
    
    # Add agent description if available
    if hasattr(agent, 'description') and agent.description:
        parts.append(f"Role: {agent.description}")
    
    # Add agent instructions if available
    if hasattr(agent, 'instruction') and agent.instruction:
        parts.append(f"\nInstructions:\n{agent.instruction}")
    elif hasattr(agent, 'canonical_instruction') and agent.canonical_instruction:
        parts.append(f"\nInstructions:\n{agent.canonical_instruction}")
    
    # Add the user prompt
    parts.append(f"\n\nUser Request:\n{user_prompt}")
    
    # Add tool information if available
    if hasattr(agent, 'tools') and agent.tools:
        parts.append(f"\n\nAvailable Tools: {len(agent.tools)} tools are available.")
        # Note: In a full implementation, tools would be called by the agent
        # For now, we rely on the LLM to understand the context
    
    return "\n".join(parts)


def _get_api_key() -> Optional[str]:
    """Get Google API key from environment."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
        except ImportError:
            pass
    return api_key


async def _run_agent_async(agent, prompt: str) -> str:
    """
    Try to run agent using ADK's async methods.
    This is a fallback if direct Gemini doesn't work.
    """
    response_parts = []
    
    # Try to create a minimal context
    # Note: This may not work without proper session setup
    try:
        # Try with None context (may fail, but worth trying)
        async for event in agent.run_async(None):
            # Extract text from various event structures
            text = _extract_text_from_event(event)
            if text:
                response_parts.append(text)
    except Exception:
        # If run_async fails, try run_live
        try:
            # run_live also needs context, but let's try
            async for event in agent.run_live(None):
                text = _extract_text_from_event(event)
                if text:
                    response_parts.append(text)
        except Exception:
            pass
    
    result = "".join(response_parts).strip()
    if result and result != prompt:
        return result
    
    # If we got nothing useful, raise to trigger fallback
    raise RuntimeError("ADK async methods did not return usable response")


def _extract_text_from_event(event) -> Optional[str]:
    """
    Extract text content from an ADK event.
    
    ADK events can contain multiple types of parts:
    - text: Regular text content
    - function_call: Tool/function calls (we skip these)
    - function_response: Tool/function responses (we skip these)
    
    This function extracts only the text parts and ignores function-related parts.
    """
    text_parts = []
    
    # Try various ways to extract text from events
    if hasattr(event, 'candidates') and event.candidates:
        for candidate in event.candidates:
            if hasattr(candidate, 'content') and candidate.content:
                if hasattr(candidate.content, 'parts'):
                    for part in candidate.content.parts:
                        # Only extract text parts, skip function_call and function_response
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
    
    if text_parts:
        return ''.join(text_parts)
    
    # Fallback methods
    if hasattr(event, 'text') and event.text:
        return str(event.text)
    
    if hasattr(event, 'content'):
        content = event.content
        if hasattr(content, 'parts'):
            for part in content.parts:
                if hasattr(part, 'text') and part.text:
                    text_parts.append(part.text)
            if text_parts:
                return ''.join(text_parts)
        if hasattr(content, '__str__'):
            content_str = str(content)
            # Don't return if it's just a repr string
            if not content_str.startswith('<'):
                return content_str
    
    if hasattr(event, 'response'):
        response = event.response
        if hasattr(response, 'text') and response.text:
            return response.text
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
            if text_parts:
                return ''.join(text_parts)
    
    return None if not text_parts else ''.join(text_parts)


def extract_json_from_response(response_text: str) -> Optional[dict]:
    """
    Extract JSON from agent response, handling markdown code blocks.
    
    Args:
        response_text: Raw response text from agent
        
    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    debug = is_debug_mode()
    
    if not response_text:
        if debug:
            print("DEBUG [extract_json]: response_text is empty or None")
        return None
    
    response_text = str(response_text).strip()
    
    if debug:
        print("\n" + "="*80)
        print("DEBUG [extract_json]: Attempting to extract JSON")
        print("="*80)
        print(f"Response length: {len(response_text)} characters")
        print(f"First 500 chars:\n{response_text[:500]}")
        print("="*80)
    
    # Try to find JSON in markdown code blocks (greedy matching for nested JSON)
    json_match = re.search(r'```(?:json|JSON)?\s*(\{.*\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
    if json_match:
        if debug:
            print("DEBUG [extract_json]: Found JSON in markdown code block")
        try:
            result = json.loads(json_match.group(1))
            if debug:
                print(f"DEBUG [extract_json]: ✓ Successfully parsed JSON from markdown")
                print(f"DEBUG [extract_json]: Keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            return result
        except json.JSONDecodeError as e:
            if debug:
                print(f"DEBUG [extract_json]: ✗ Failed to parse JSON from markdown: {e}")
                print(f"DEBUG [extract_json]: Extracted JSON (first 500 chars): {json_match.group(1)[:500]}")
    
    # Try to find JSON without markdown (greedy matching)
    json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
    if json_match:
        if debug:
            print("DEBUG [extract_json]: Found JSON pattern (no markdown)")
        try:
            result = json.loads(json_match.group(1))
            if debug:
                print(f"DEBUG [extract_json]: ✓ Successfully parsed JSON without markdown")
            return result
        except json.JSONDecodeError as e:
            if debug:
                print(f"DEBUG [extract_json]: ✗ Failed to parse JSON without markdown: {e}")
    
    # Try parsing the entire response as JSON
    if debug:
        print("DEBUG [extract_json]: Trying to parse entire response as JSON")
    try:
        result = json.loads(response_text)
        if debug:
            print(f"DEBUG [extract_json]: ✓ Successfully parsed entire response as JSON")
        return result
    except json.JSONDecodeError as e:
        if debug:
            print(f"DEBUG [extract_json]: ✗ Failed to parse entire response as JSON: {e}")
    
    if debug:
        print("DEBUG [extract_json]: ✗ All JSON extraction attempts failed")
        print("="*80 + "\n")
    
    return None

