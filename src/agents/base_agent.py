"""
Base Agent class for the multi-agent system.
Provides a common interface for all agents following Google ADK patterns.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..config import get_gemini_api_key, get_gemini_model


class BaseAgent(ABC):
    """
    Base class for all agents in the college planner system.
    Follows Google ADK agent patterns for consistency.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        use_gemini: bool = False,
        **kwargs
    ):
        """
        Initialize the agent.
        
        Args:
            name: Agent name
            description: Agent description
            use_gemini: Whether to use Gemini API for this agent
            **kwargs: Additional configuration
        """
        self.name = name
        self.description = description
        self.use_gemini = use_gemini
        self.config = kwargs
        
        # Initialize Gemini if needed
        self._gemini_model = None
        if use_gemini:
            self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini model if API key is available."""
        api_key = get_gemini_api_key()
        if api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self._gemini_model = genai.GenerativeModel(get_gemini_model())
            except ImportError:
                print(f"Warning: google-generativeai not installed. {self.name} will work without Gemini.")
        else:
            print(f"Warning: GOOGLE_API_KEY not set. {self.name} will work without Gemini.")
    
    def get_gemini_model(self):
        """Get the Gemini model instance."""
        return self._gemini_model
    
    @abstractmethod
    def run(self, *args, **kwargs) -> Any:
        """
        Main execution method for the agent.
        Must be implemented by subclasses.
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

