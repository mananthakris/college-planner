"""
Retrieval Agent: Finds similar profiles and relevant opportunities.
Uses Google ADK Agent with database tools.
"""
from typing import Dict, Any
import warnings
from ..models import StudentProfile, SimilarProfile, Opportunity
from ..tools.data_loader import load_opportunities, find_similar_profiles
from ..tools.database import get_database
from ..config import get_gemini_model
from ..utils.adk_helper import run_agent_sync, extract_json_from_response


def _create_retrieval_agent():
    """
    Create a Google ADK Agent for profile retrieval with database tools.
    
    Returns:
        ADK Agent instance configured for profile matching
    """
    try:
        from google.adk.agents import Agent
        from google.adk.tools import FunctionTool
        from ..tools.agent_tools import (
            search_profiles_tool,
            search_by_major_tool,
            search_by_college_tool,
            find_similar_profiles_tool,
            get_opportunities_tool,
            get_profile_statistics_tool
        )
        
        agent = Agent(
            name="retrieval_agent",
            model=get_gemini_model(),
            description="Finds similar student profiles and relevant opportunities from the database",
            instruction="""You are a retrieval agent specialized in finding similar student profiles and relevant opportunities.

Your task is to:
1. Find similar student profiles based on interests, majors, and academic strengths
2. Filter relevant opportunities (competitions, programs, internships) based on grade level and interests
3. Rank results by relevance and similarity
4. Return structured results with similarity scores

When searching:
- Use find_similar_profiles_tool for the most accurate similarity matching
- Use search_profiles_tool to search by interests
- Use search_by_major_tool to find students by major
- Use search_by_college_tool to find students targeting specific colleges
- Use get_opportunities_tool to find relevant opportunities
- Use get_profile_statistics_tool to understand the database

Always prioritize profiles with the highest similarity to the input profile. When returning results, include:
- Similarity scores
- Target colleges and majors
- Key achievements or distinguishing factors
- Relevant opportunities for the student's grade level

Format your response as structured JSON with clear sections for similar_profiles and opportunities.""",
            tools=[
                FunctionTool(search_profiles_tool),
                FunctionTool(search_by_major_tool),
                FunctionTool(search_by_college_tool),
                FunctionTool(find_similar_profiles_tool),
                FunctionTool(get_opportunities_tool),
                FunctionTool(get_profile_statistics_tool)
            ]
        )
        return agent
    except ImportError as e:
        raise ImportError(
            f"google-adk is not available. Please activate your virtual environment first:\n"
            f"  source venv/bin/activate\n"
            f"Then ensure google-adk is installed: pip install google-adk\n"
            f"Original error: {e}"
        )


def run_retrieval(profile: StudentProfile) -> Dict[str, Any]:
    """
    Retrieve similar profiles and relevant opportunities using ADK Agent with tools.
    
    Args:
        profile: The student profile to find matches for
        
    Returns:
        Dictionary containing similar_profiles and opportunities
    """
    agent = _create_retrieval_agent()  # This will raise ImportError if ADK is not available
    
    # Create a natural language query for the agent
    interests_str = ", ".join(profile.interests) if profile.interests else "general interests"
    majors_str = ", ".join(profile.target_majors) if profile.target_majors else ""
    colleges_str = ", ".join(profile.target_colleges) if profile.target_colleges else ""
    
    query = f"""Find similar student profiles and relevant opportunities for this student:

Student Profile:
- Current Grade: {profile.current_grade.name} ({profile.current_grade.value})
- Interests: {interests_str}
- Target Majors: {majors_str if majors_str else 'Not specified'}
- Target Colleges: {colleges_str if colleges_str else 'Not specified'}
- Academic Strengths: {', '.join(profile.academic_strengths) if profile.academic_strengths else 'Not specified'}
- Current Extracurriculars: {', '.join(profile.extracurriculars) if profile.extracurriculars else 'None'}

Please:
1. Find the top 5 most similar student profiles using find_similar_profiles_tool
2. Find relevant opportunities for grade {profile.current_grade.value} using get_opportunities_tool
3. Return the results in a structured format

Focus on profiles that match the student's interests and target majors/colleges."""

    try:
        # Suppress warnings from ADK library about non-text parts (function calls)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*non-text parts.*")
            warnings.filterwarnings("ignore", category=UserWarning)
            
            # Run the agent
            response = run_agent_sync(agent, query)
        
        # Extract JSON from response using helper
        result_data = extract_json_from_response(response)
        if not result_data:
            # Fallback: parse the response text manually if JSON extraction fails
            result_data = _parse_agent_response(str(response), profile)
        
        # Convert to expected format
        similar_profiles = _convert_to_similar_profiles(result_data.get("similar_profiles", []))
        opportunities = _convert_to_opportunities(result_data.get("opportunities", []))
        
        # If agent didn't return enough data, supplement with direct database queries
        if len(similar_profiles) < 3:
            db = get_database()
            all_profiles = db.get_all_profiles()
            direct_similar = find_similar_profiles(profile, all_profiles, top_k=5)
            # Merge with agent results
            existing_names = {sp.profile.name for sp in similar_profiles}
            for sim in direct_similar:
                if sim.profile.name not in existing_names:
                    similar_profiles.append(sim)
        
        if not opportunities:
            opportunities = _filter_relevant_opportunities(profile, load_opportunities())
        
        return {
            "similar_profiles": similar_profiles[:5],  # Top 5
            "opportunities": opportunities,
            "database_size": get_database().get_profile_count()
        }
        
    except Exception as e:
        print(f"Error running retrieval agent: {e}")
        # Fallback to direct database queries if agent fails
        return _fallback_retrieval(profile)


def _parse_agent_response(response_text: str, profile: StudentProfile) -> Dict[str, Any]:
    """Parse agent response and extract structured data."""
    # This is a fallback parser - the agent should ideally return structured JSON
    result = {
        "similar_profiles": [],
        "opportunities": []
    }
    
    # Try to extract information from the response
    # In a real implementation, the agent should return properly structured JSON
    # This is a basic parser for when that doesn't happen
    
    return result


def _convert_to_similar_profiles(profile_data: list) -> list[SimilarProfile]:
    """Convert agent response data to SimilarProfile objects."""
    from ..agents.profile_agent import normalize
    
    similar_profiles = []
    
    for data in profile_data:
        if isinstance(data, dict):
            # Create a profile from the data
            profile_dict = {
                "name": data.get("name", "Student"),
                "current_grade": data.get("current_grade", 12),
                "interests": data.get("interests", []),
                "target_colleges": data.get("target_colleges", []),
                "target_majors": data.get("target_majors", []),
                "gpa": data.get("gpa"),
                "extracurriculars": data.get("extracurriculars", []),
                "test_scores": data.get("test_scores", {})
            }
            
            profile = normalize(profile_dict)
            similarity_score = data.get("similarity_score", 0.7)
            
            similar = SimilarProfile(
                profile=profile,
                similarity_score=similarity_score,
                colleges_admitted=data.get("colleges_admitted", profile.target_colleges),
                final_major=data.get("final_major", profile.target_majors[0] if profile.target_majors else None)
            )
            similar_profiles.append(similar)
    
    return similar_profiles


def _convert_to_opportunities(opp_data: list) -> list[Opportunity]:
    """Convert agent response data to Opportunity objects."""
    opportunities = []
    
    for data in opp_data:
        if isinstance(data, dict):
            from ..models import Grade
            grade_levels = [Grade(int(g)) for g in data.get("grade_levels", [9, 10, 11, 12])]
            
            opp = Opportunity(
                name=data.get("name", ""),
                type=data.get("type", "extracurricular"),
                grade_levels=grade_levels,
                description=data.get("description", ""),
                requirements=data.get("requirements", []),
                benefits=data.get("benefits", []),
                deadline=data.get("deadline")
            )
            opportunities.append(opp)
    
    return opportunities


def _filter_relevant_opportunities(
    profile: StudentProfile,
    opportunities: list[Opportunity]
) -> list[Opportunity]:
    """
    Filter opportunities based on grade level and interests.
    """
    relevant = []
    
    for opp in opportunities:
        # Check if opportunity is appropriate for student's grade
        if profile.current_grade not in opp.grade_levels:
            continue
        
        # Check if opportunity aligns with interests
        interest_match = False
        for interest in profile.interests:
            if interest.lower() in opp.name.lower() or interest.lower() in opp.description.lower():
                interest_match = True
                break
        
        # Include if it matches interests or is a general opportunity
        if interest_match or opp.type in ["academic", "extracurricular"]:
            relevant.append(opp)
    
    return relevant


def _fallback_retrieval(profile: StudentProfile) -> Dict[str, Any]:
    """
    Fallback retrieval using direct database queries.
    Only used if ADK agent fails.
    """
    db = get_database()
    all_profiles = db.get_all_profiles()
    
    # Find similar profiles
    similar_profiles = find_similar_profiles(profile, all_profiles, top_k=5)
    
    # Load opportunities
    all_opportunities = load_opportunities()
    relevant_opportunities = _filter_relevant_opportunities(profile, all_opportunities)
    
    return {
        "similar_profiles": similar_profiles,
        "opportunities": relevant_opportunities,
        "database_size": db.get_profile_count()
    }


# ADK Agent instance (lazy initialization)
_retrieval_agent_instance = None

def get_retrieval_agent():
    """Get or create the ADK retrieval agent instance."""
    global _retrieval_agent_instance
    if _retrieval_agent_instance is None:
        _retrieval_agent_instance = _create_retrieval_agent()
    return _retrieval_agent_instance
