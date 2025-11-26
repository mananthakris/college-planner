"""
Tests for Profile Agent.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.profile_agent import normalize, parse_natural_language
from src.models import Grade


def test_normalize():
    """Test profile normalization with structured input."""
    profile_dict = {
        'name': 'Test Student',
        'current_grade': 9,
        'interests': ['Computer Science', 'Mathematics'],
        'academic_strengths': ['Math', 'Science'],
        'target_colleges': ['MIT', 'Stanford'],
        'target_majors': ['Computer Science']
    }
    
    profile = normalize(profile_dict)
    assert profile.name == 'Test Student'
    assert profile.current_grade == Grade.FRESHMAN
    assert 'Computer Science' in profile.interests
    assert 'MIT' in profile.target_colleges
    print("✓ test_normalize passed")


def test_parse_natural_language():
    """Test natural language parsing."""
    text = "I am a freshman interested in computer science and math. I want to go to MIT."
    profile = parse_natural_language(text)
    
    assert profile.current_grade == Grade.FRESHMAN
    assert len(profile.interests) > 0
    assert 'MIT' in profile.target_colleges or len(profile.target_colleges) > 0
    print("✓ test_parse_natural_language passed")


if __name__ == "__main__":
    test_normalize()
    test_parse_natural_language()
    print("\n✓ All Profile Agent tests passed!")

