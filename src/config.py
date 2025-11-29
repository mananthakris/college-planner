"""
Configuration for the College Planner system.
"""
import os
from typing import Optional


def get_gemini_api_key() -> Optional[str]:
    """
    Get Google Gemini API key from environment variable.
    
    Set it with: export GOOGLE_API_KEY="your-api-key-here"
    Or create a .env file with: GOOGLE_API_KEY=your-api-key-here
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        # Try loading from .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("GOOGLE_API_KEY")
        except ImportError:
            pass
    
    return api_key


def get_gemini_model() -> str:
    """Get the Gemini model name to use."""
    # Default to a valid model name (gemini-pro doesn't exist, use gemini-1.5-flash)
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


# Database configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/student_profiles.db")
PROFILES_JSON_PATH = os.getenv("PROFILES_JSON_PATH", "data/student_profiles.json")


# Debug configuration
def is_debug_mode() -> bool:
    """
    Check if debug mode is enabled.
    
    Set with: export DEBUG_MODE=1
    Or in .env file: DEBUG_MODE=1
    
    Returns:
        True if debug mode is enabled, False otherwise
    """
    debug = os.getenv("DEBUG_MODE", "0").lower()
    return debug in ("1", "true", "yes", "on")

