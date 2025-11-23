"""
Test script for natural language profile input with Gemini.
"""
import os
from src.agents.profile_agent import parse_natural_language
from src.agents.retrieval_agent import run_retrieval
from src.tools.database import get_database


def test_natural_language_parsing():
    """Test parsing natural language input into structured profiles."""
    
    print("=" * 80)
    print("NATURAL LANGUAGE PROFILE PARSING TEST")
    print("=" * 80)
    
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n⚠️  GOOGLE_API_KEY not found in environment.")
        print("   The system will use fallback rule-based parsing.")
        print("   Set it with: export GOOGLE_API_KEY='your-api-key'\n")
    else:
        print("\n✓ Google API key found. Using Gemini for parsing.\n")
    
    # Test cases
    test_cases = [
        {
            "name": "Engineering Student",
            "input": """I'm a freshman in high school. I'm really interested in 
            engineering and robotics. I love math and physics. I want to go to 
            MIT or Stanford to study mechanical engineering. I'm currently in 
            the robotics club at my school."""
        },
        {
            "name": "Pre-Med Student",
            "input": """Hi, I'm a 9th grader. I'm passionate about medicine and 
            biology. I volunteer at the local hospital on weekends. My dream is 
            to become a doctor, so I want to go to Johns Hopkins or Harvard for 
            pre-med. I'm really good at chemistry and biology."""
        },
        {
            "name": "Computer Science Student",
            "input": """I'm a sophomore. I love coding and computer science. 
            I've taken some programming classes and I'm in the coding club. 
            I want to major in computer science at UC Berkeley or Stanford. 
            My GPA is 3.9."""
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        print(f"\n{'='*80}")
        print(f"TEST: {test_case['name']}")
        print(f"{'='*80}\n")
        print(f"Input: {test_case['input']}\n")
        print("Parsing...\n")
        
        try:
            # Parse natural language
            profile = parse_natural_language(test_case['input'])
            
            # Display parsed profile
            print("✓ Parsed Profile:")
            print(f"  Name: {profile.name}")
            print(f"  Grade: {profile.current_grade.name} ({profile.current_grade.value})")
            print(f"  Interests: {', '.join(profile.interests) if profile.interests else 'None'}")
            print(f"  Academic Strengths: {', '.join(profile.academic_strengths) if profile.academic_strengths else 'None'}")
            print(f"  Extracurriculars: {', '.join(profile.extracurriculars) if profile.extracurriculars else 'None'}")
            print(f"  Target Colleges: {', '.join(profile.target_colleges) if profile.target_colleges else 'None'}")
            print(f"  Target Majors: {', '.join(profile.target_majors) if profile.target_majors else 'None'}")
            if profile.gpa:
                print(f"  GPA: {profile.gpa}")
            
            # Test retrieval
            print("\n" + "-"*80)
            print("Testing Retrieval Agent...\n")
            retrieval = run_retrieval(profile)
            
            print(f"✓ Found {len(retrieval['similar_profiles'])} similar profiles")
            print(f"✓ Database contains {retrieval.get('database_size', 0)} profiles")
            print(f"✓ Found {len(retrieval['opportunities'])} relevant opportunities")
            
            if retrieval['similar_profiles']:
                print("\n  Top Similar Profiles:")
                for i, similar in enumerate(retrieval['similar_profiles'][:3], 1):
                    print(f"    {i}. {similar.profile.name} (similarity: {similar.similarity_score:.2f})")
                    if similar.profile.target_colleges:
                        print(f"       Colleges: {', '.join(similar.profile.target_colleges[:2])}")
            
            results.append({
                "test_name": test_case['name'],
                "profile": profile,
                "retrieval": retrieval,
                "success": True
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "test_name": test_case['name'],
                "success": False,
                "error": str(e)
            })
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")
    
    successful = sum(1 for r in results if r.get('success', False))
    print(f"✓ Successful: {successful}/{len(results)}")
    
    if successful < len(results):
        print("\nFailed tests:")
        for r in results:
            if not r.get('success', False):
                print(f"  - {r['test_name']}: {r.get('error', 'Unknown error')}")
    
    return results


if __name__ == "__main__":
    test_natural_language_parsing()

