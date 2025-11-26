"""
Tests for Agent Tools.
"""
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.tools.agent_tools import (
    search_profiles_tool,
    search_by_major_tool,
    find_similar_profiles_tool,
    get_opportunities_tool
)


def test_search_profiles_tool():
    """Test search_profiles_tool."""
    result = search_profiles_tool('Computer Science', top_k=2)
    assert isinstance(result, str)
    data = json.loads(result)
    assert isinstance(data, list)
    print(f"✓ search_profiles_tool: {len(data)} results")


def test_search_by_major_tool():
    """Test search_by_major_tool."""
    result = search_by_major_tool('Computer Science', top_k=2)
    assert isinstance(result, str)
    data = json.loads(result)
    assert isinstance(data, list)
    print(f"✓ search_by_major_tool: {len(data)} results")


def test_find_similar_profiles_tool():
    """Test find_similar_profiles_tool."""
    result = find_similar_profiles_tool('Computer Science, Math', 'Computer Science', top_k=2)
    assert isinstance(result, str)
    data = json.loads(result)
    assert isinstance(data, list)
    print(f"✓ find_similar_profiles_tool: {len(data)} results")


def test_get_opportunities_tool():
    """Test get_opportunities_tool."""
    result = get_opportunities_tool(9, 'Computer Science')
    assert isinstance(result, str)
    data = json.loads(result)
    assert isinstance(data, list)
    print(f"✓ get_opportunities_tool: {len(data)} results")


if __name__ == "__main__":
    test_search_profiles_tool()
    test_search_by_major_tool()
    test_find_similar_profiles_tool()
    test_get_opportunities_tool()
    print("\n✓ All Agent Tools tests passed!")

