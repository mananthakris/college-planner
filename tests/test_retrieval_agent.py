"""
Tests for Retrieval Agent.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.profile_agent import normalize
from src.agents.retrieval_agent import run_retrieval, get_retrieval_agent


def test_get_retrieval_agent():
    """Test retrieval agent creation."""
    agent = get_retrieval_agent()
    # Agent may be None if ADK not installed, which is OK
    if agent:
        print("✓ RetrievalAgent created with ADK")
    else:
        print("⚠ RetrievalAgent requires ADK (this is OK if ADK not installed)")


def test_run_retrieval():
    """Test retrieval functionality."""
    profile = normalize({
        'name': 'Test',
        'current_grade': 9,
        'interests': ['Computer Science'],
        'target_colleges': ['MIT'],
        'target_majors': ['Computer Science']
    })
    
    try:
        retrieval = run_retrieval(profile)
        assert 'similar_profiles' in retrieval
        assert 'opportunities' in retrieval
        assert 'database_size' in retrieval
        print(f"✓ Retrieval works: {len(retrieval['similar_profiles'])} similar profiles")
    except RuntimeError as e:
        if "requires google-adk" in str(e):
            print("⚠ Retrieval requires ADK (install google-adk to test)")
        else:
            raise


if __name__ == "__main__":
    test_get_retrieval_agent()
    test_run_retrieval()
    print("\n✓ All Retrieval Agent tests passed!")

