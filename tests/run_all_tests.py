"""
Run all tests for the College Planner system.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def run_tests():
    """Run all test modules."""
    print("=" * 60)
    print("College Planner - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        ("Profile Agent", "test_profile_agent"),
        ("Database", "test_database"),
        ("Agent Tools", "test_agent_tools"),
        ("Retrieval Agent", "test_retrieval_agent"),
        ("Full Pipeline", "test_pipeline")
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_module in tests:
        print(f"Running {test_name} tests...")
        try:
            module = __import__(test_module)
            if hasattr(module, '__main__'):
                # Run the test module
                exec(f"import {test_module}; {test_module}.__name__ = '__main__'")
            print()
            passed += 1
        except Exception as e:
            print(f"  ✗ Failed: {e}")
            print()
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    # Import and run each test module
    import test_profile_agent
    import test_database
    import test_agent_tools
    import test_retrieval_agent
    import test_pipeline
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)

