"""
Tests for full pipeline.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import run_pipeline


def test_pipeline_engineering():
    """Test pipeline with engineering profile."""
    profile_input = {
        'name': 'Engineering Student',
        'current_grade': 9,
        'interests': ['Engineering', 'Mathematics', 'Robotics'],
        'academic_strengths': ['Math', 'Science'],
        'target_colleges': ['MIT', 'Stanford'],
        'target_majors': ['Engineering']
    }
    
    result = run_pipeline(profile_input, max_iterations=1, min_score_threshold=0.6)
    
    assert result['profile'] is not None
    assert result['plan'] is not None
    assert result['critique'] is not None
    assert result['explanation'] is not None
    assert result['final_score'] >= 0
    assert result['iterations'] >= 1
    
    print(f"✓ Engineering pipeline: Score {result['final_score']:.1%}")


def test_pipeline_premed():
    """Test pipeline with pre-med profile."""
    profile_input = {
        'name': 'Pre-Med Student',
        'current_grade': 9,
        'interests': ['Biology', 'Medicine'],
        'academic_strengths': ['Biology', 'Chemistry'],
        'target_colleges': ['Johns Hopkins', 'Harvard'],
        'target_majors': ['Biology', 'Pre-Med']
    }
    
    result = run_pipeline(profile_input, max_iterations=1, min_score_threshold=0.6)
    
    assert result['profile'] is not None
    assert result['plan'] is not None
    assert result['final_score'] >= 0
    
    print(f"✓ Pre-Med pipeline: Score {result['final_score']:.1%}")


if __name__ == "__main__":
    test_pipeline_engineering()
    test_pipeline_premed()
    print("\n✓ All Pipeline tests passed!")

