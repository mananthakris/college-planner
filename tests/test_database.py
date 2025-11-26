"""
Tests for Database functionality.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.database import get_database
from src.agents.profile_agent import normalize


def test_database_initialization():
    """Test database initialization."""
    db = get_database()
    assert db is not None
    count = db.get_profile_count()
    assert count >= 0
    print(f"✓ Database initialized: {count} profiles")


def test_search_by_interests():
    """Test searching profiles by interests."""
    db = get_database()
    results = db.search_by_interests(['Computer Science'], top_k=5)
    assert isinstance(results, list)
    print(f"✓ Search by interests: {len(results)} results")


def test_search_by_major():
    """Test searching profiles by major."""
    db = get_database()
    results = db.search_by_major('Computer Science', top_k=5)
    assert isinstance(results, list)
    print(f"✓ Search by major: {len(results)} results")


if __name__ == "__main__":
    test_database_initialization()
    test_search_by_interests()
    test_search_by_major()
    print("\n✓ All Database tests passed!")

