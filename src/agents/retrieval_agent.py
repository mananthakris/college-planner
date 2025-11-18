"""
Retrieval Agent: Finds similar profiles and relevant opportunities.
"""
from typing import Dict, Any
from ..models import StudentProfile, SimilarProfile, Opportunity
from ..tools.data_loader import load_student_profiles, load_opportunities, find_similar_profiles


def run_retrieval(profile: StudentProfile) -> Dict[str, Any]:
    """
    Retrieve similar profiles and relevant opportunities.
    
    Args:
        profile: The student profile to find matches for
        
    Returns:
        Dictionary containing similar_profiles and opportunities
    """
    # Load all available profiles
    all_profiles = load_student_profiles()
    
    # Find similar profiles
    similar_profiles = find_similar_profiles(profile, all_profiles, top_k=5)
    
    # Load opportunities
    all_opportunities = load_opportunities()
    
    # Filter opportunities relevant to the student's grade and interests
    relevant_opportunities = _filter_relevant_opportunities(profile, all_opportunities)
    
    return {
        "similar_profiles": similar_profiles,
        "opportunities": relevant_opportunities
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
