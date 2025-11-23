"""
Retrieval Agent: Finds similar profiles and relevant opportunities.
Uses Google ADK Agent class for proper integration.
"""
from typing import Dict, Any
from ..models import StudentProfile, SimilarProfile, Opportunity
from ..tools.data_loader import load_opportunities, find_similar_profiles
from ..tools.database import get_database
from ..config import get_gemini_model


def _create_retrieval_agent():
    """
    Create a Google ADK Agent for profile retrieval.
    
    Returns:
        ADK Agent instance configured for profile matching
    """
    try:
        from google.adk.agents import Agent
        
        agent = Agent(
            name="retrieval_agent",
            model=get_gemini_model(),
            description="Finds similar student profiles and relevant opportunities from the database",
            instruction="""You are a retrieval agent. Your task is to:
            1. Find similar student profiles based on interests, majors, and academic strengths
            2. Filter relevant opportunities (competitions, programs, internships) based on grade level and interests
            3. Rank results by relevance and similarity
            4. Return structured results with similarity scores
            
            Always prioritize profiles with the highest similarity to the input profile.""",
            tools=[]  # Can add database tools later
        )
        return agent
    except ImportError:
        print("Warning: google-adk not installed. Using fallback implementation.")
        return None


def run_retrieval(profile: StudentProfile) -> Dict[str, Any]:
    """
    Retrieve similar profiles and relevant opportunities from database.
    Uses ADK Agent if available, otherwise uses direct database queries.
    
    Args:
        profile: The student profile to find matches for
        
    Returns:
        Dictionary containing similar_profiles and opportunities
    """
    # Get database instance
    db = get_database()
    
    # Load all profiles from database
    all_profiles = db.get_all_profiles()
    
    # Try using ADK Agent for intelligent matching
    agent = _create_retrieval_agent()
    
    if agent:
        try:
            # Use ADK agent to enhance matching
            # For now, we'll use it to improve similarity scoring
            # In the future, we can pass the full retrieval task to the agent
            pass  # Placeholder for ADK agent enhancement
        except Exception as e:
            print(f"Warning: ADK Agent error ({e}). Using direct database queries.")
    
    # Find similar profiles using similarity algorithm
    similar_profiles = find_similar_profiles(profile, all_profiles, top_k=5)
    
    # Also try database search methods for additional matches
    if profile.interests:
        interest_matches = db.search_by_interests(profile.interests, top_k=3)
        # Add to similar profiles if not already included
        existing_names = {sp.profile.name for sp in similar_profiles}
        for match in interest_matches:
            if match.name not in existing_names:
                # Create SimilarProfile with estimated similarity
                similar = SimilarProfile(
                    profile=match,
                    similarity_score=0.7,  # Estimated score for interest match
                    colleges_admitted=match.target_colleges or ["Top University"],
                    final_major=match.target_majors[0] if match.target_majors else None
                )
                similar_profiles.append(similar)
    
    # If target major specified, also search by major
    if profile.target_majors:
        major_matches = db.search_by_major(profile.target_majors[0], top_k=2)
        existing_names = {sp.profile.name for sp in similar_profiles}
        for match in major_matches:
            if match.name not in existing_names:
                similar = SimilarProfile(
                    profile=match,
                    similarity_score=0.75,
                    colleges_admitted=match.target_colleges or ["Top University"],
                    final_major=match.target_majors[0] if match.target_majors else None
                )
                similar_profiles.append(similar)
    
    # Sort by similarity score and take top 5
    similar_profiles.sort(key=lambda x: x.similarity_score, reverse=True)
    similar_profiles = similar_profiles[:5]
    
    # Load opportunities
    all_opportunities = load_opportunities()
    
    # Filter opportunities relevant to the student's grade and interests
    relevant_opportunities = _filter_relevant_opportunities(profile, all_opportunities)
    
    return {
        "similar_profiles": similar_profiles,
        "opportunities": relevant_opportunities,
        "database_size": db.get_profile_count()
    }


def _filter_relevant_opportunities(
    profile: StudentProfile,
    opportunities: list[Opportunity]
) -> list[Opportunity]:
    """
    Filter opportunities based on grade level and interests.
    
    Args:
        profile: Student profile
        opportunities: List of all opportunities
        
    Returns:
        Filtered list of relevant opportunities
    """
    relevant = []
    
    for opp in opportunities:
        # Check if opportunity is appropriate for student's grade
        if profile.current_grade not in opp.grade_levels:
            continue
        
        # Check if opportunity aligns with interests (simple keyword matching)
        # In production, this could use more sophisticated matching
        interest_match = False
        for interest in profile.interests:
            if interest.lower() in opp.name.lower() or interest.lower() in opp.description.lower():
                interest_match = True
                break
        
        # Include if it matches interests or is a general opportunity
        if interest_match or opp.type in ["academic", "extracurricular"]:
            relevant.append(opp)
    
    return relevant


# ADK Agent instance (lazy initialization)
_retrieval_agent_instance = None

def get_retrieval_agent():
    """Get or create the ADK retrieval agent instance."""
    global _retrieval_agent_instance
    if _retrieval_agent_instance is None:
        _retrieval_agent_instance = _create_retrieval_agent()
    return _retrieval_agent_instance
