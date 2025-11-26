"""
Agent modules for the college planner system.
"""
from . import profile_agent
from . import retrieval_agent
from . import planner_agent
from . import critic_agent
from . import explainer_agent

# Import functions for convenience
from .profile_agent import normalize, parse_natural_language, get_profile_agent
from .retrieval_agent import run_retrieval, get_retrieval_agent

# Import tools for agents
from ..tools.agent_tools import (
    search_profiles_tool,
    search_by_major_tool,
    search_by_college_tool,
    find_similar_profiles_tool,
    get_opportunities_tool,
    get_profile_statistics_tool
)

__all__ = [
    "profile_agent",
    "retrieval_agent",
    "planner_agent",
    "critic_agent",
    "explainer_agent",
    "normalize",
    "parse_natural_language",
    "run_retrieval",
    "get_profile_agent",
    "get_retrieval_agent"
]

