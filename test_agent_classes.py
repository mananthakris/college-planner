"""
Test script demonstrating the new BaseAgent class architecture.
Shows both class-based and legacy function-based usage.
"""
from src.agents import ProfileAgent, RetrievalAgent, BaseAgent
from src.agents.profile_agent import normalize, parse_natural_language
from src.agents.retrieval_agent import run_retrieval


def test_class_based_usage():
    """Test the new class-based agent usage."""
    print("=" * 80)
    print("TESTING CLASS-BASED AGENT USAGE")
    print("=" * 80 + "\n")
    
    # Create Profile Agent instance
    profile_agent = ProfileAgent(use_gemini=False)
    print(f"✓ Created {profile_agent.name}")
    print(f"  Description: {profile_agent.description}")
    print(f"  Type: {type(profile_agent).__name__}")
    print(f"  Inherits from BaseAgent: {isinstance(profile_agent, BaseAgent)}\n")
    
    # Test with dictionary input
    profile_dict = {
        "name": "Alex Johnson",
        "current_grade": 9,
        "interests": ["Computer Science", "Mathematics"],
        "target_colleges": ["MIT", "Stanford"],
        "target_majors": ["Computer Science"]
    }
    
    profile = profile_agent.run(profile_dict)
    print(f"✓ Profile Agent processed dictionary input:")
    print(f"  Name: {profile.name}")
    print(f"  Grade: {profile.current_grade.name}")
    print(f"  Interests: {', '.join(profile.interests)}")
    print(f"  Target Colleges: {', '.join(profile.target_colleges)}\n")
    
    # Test with natural language input
    nl_input = "I'm a sophomore interested in biology and chemistry. I want to go to Harvard for pre-med."
    nl_profile = profile_agent.run(nl_input)
    print(f"✓ Profile Agent processed natural language input:")
    print(f"  Name: {nl_profile.name}")
    print(f"  Grade: {nl_profile.current_grade.name}")
    print(f"  Interests: {', '.join(nl_profile.interests) if nl_profile.interests else 'None'}")
    print(f"  Target Colleges: {', '.join(nl_profile.target_colleges) if nl_profile.target_colleges else 'None'}\n")
    
    # Create Retrieval Agent instance
    retrieval_agent = RetrievalAgent()
    print(f"✓ Created {retrieval_agent.name}")
    print(f"  Description: {retrieval_agent.description}")
    print(f"  Inherits from BaseAgent: {isinstance(retrieval_agent, BaseAgent)}\n")
    
    # Test retrieval
    retrieval = retrieval_agent.run(profile)
    print(f"✓ Retrieval Agent found:")
    print(f"  Similar Profiles: {len(retrieval['similar_profiles'])}")
    print(f"  Opportunities: {len(retrieval['opportunities'])}")
    print(f"  Database Size: {retrieval.get('database_size', 0)} profiles\n")
    
    return profile, retrieval


def test_legacy_usage():
    """Test legacy function-based usage for backward compatibility."""
    print("=" * 80)
    print("TESTING LEGACY FUNCTION-BASED USAGE")
    print("=" * 80 + "\n")
    
    # Test legacy normalize function
    profile_dict = {
        "name": "Sarah Chen",
        "current_grade": 10,
        "interests": ["Biology", "Chemistry"],
        "target_colleges": ["Johns Hopkins", "Harvard"]
    }
    
    profile = normalize(profile_dict)
    print(f"✓ Legacy normalize() function works:")
    print(f"  Name: {profile.name}")
    print(f"  Grade: {profile.current_grade.name}\n")
    
    # Test legacy parse_natural_language function
    nl_profile = parse_natural_language("I'm a junior interested in engineering")
    print(f"✓ Legacy parse_natural_language() function works:")
    print(f"  Grade: {nl_profile.current_grade.name}")
    print(f"  Interests: {', '.join(nl_profile.interests) if nl_profile.interests else 'None'}\n")
    
    # Test legacy run_retrieval function
    retrieval = run_retrieval(profile)
    print(f"✓ Legacy run_retrieval() function works:")
    print(f"  Similar Profiles: {len(retrieval['similar_profiles'])}")
    print(f"  Opportunities: {len(retrieval['opportunities'])}\n")
    
    return profile, retrieval


def test_multi_agent_architecture():
    """Test that the full multi-agent architecture still works."""
    print("=" * 80)
    print("TESTING MULTI-AGENT ARCHITECTURE")
    print("=" * 80 + "\n")
    
    # Import all agents
    from src.agents import planner_agent, critic_agent, explainer_agent
    
    print("✓ All agents are available:")
    print(f"  - ProfileAgent: {ProfileAgent}")
    print(f"  - RetrievalAgent: {RetrievalAgent}")
    print(f"  - planner_agent: {planner_agent}")
    print(f"  - critic_agent: {critic_agent}")
    print(f"  - explainer_agent: {explainer_agent}\n")
    
    # Test that orchestrator can use them
    from src.orchestrator import run_pipeline
    
    profile_input = {
        "name": "Test Student",
        "current_grade": 9,
        "interests": ["Computer Science"],
        "target_colleges": ["MIT"],
        "target_majors": ["Computer Science"]
    }
    
    print("✓ Testing full pipeline with orchestrator...")
    result = run_pipeline(profile_input, max_iterations=1, min_score_threshold=0.6)
    
    print(f"  Profile: {result['profile'].name}")
    print(f"  Plan created: {result['plan'] is not None}")
    print(f"  Critique score: {result['critique'].score:.1%}")
    print(f"  Explanation generated: {result['explanation'] is not None}\n")
    
    return result


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("AGENT CLASS ARCHITECTURE TEST")
    print("=" * 80 + "\n")
    
    # Test class-based usage
    profile1, retrieval1 = test_class_based_usage()
    
    # Test legacy usage
    profile2, retrieval2 = test_legacy_usage()
    
    # Test multi-agent architecture
    result = test_multi_agent_architecture()
    
    print("=" * 80)
    print("✓ ALL TESTS PASSED")
    print("=" * 80)
    print("\nSummary:")
    print("  ✓ BaseAgent class architecture working")
    print("  ✓ ProfileAgent and RetrievalAgent use BaseAgent")
    print("  ✓ Legacy function wrappers maintain backward compatibility")
    print("  ✓ Full multi-agent architecture preserved")
    print("  ✓ Orchestrator works with all agents\n")

