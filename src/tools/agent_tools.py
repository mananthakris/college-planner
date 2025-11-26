"""
Tools that ADK agents can use to interact with the database.
"""
from typing import List, Dict, Any
import json
from ..tools.database import get_database
from ..models import StudentProfile
from ..tools.data_loader import find_similar_profiles, load_opportunities


def search_profiles_tool(interests: str, top_k: int = 10) -> str:
    """
    Search for student profiles by interests.
    
    Args:
        interests: Comma-separated list of interests (e.g., "Computer Science, Math")
        top_k: Maximum number of results
        
    Returns:
        JSON string with matching profiles
    """
    db = get_database()
    interest_list = [i.strip() for i in interests.split(",") if i.strip()]
    
    if not interest_list:
        return json.dumps({"error": "No interests provided"})
    
    profiles = db.search_by_interests(interest_list, top_k=top_k)
    
    # Convert to JSON-serializable format
    results = []
    for profile in profiles:
        results.append({
            "name": profile.name,
            "interests": profile.interests,
            "target_colleges": profile.target_colleges,
            "target_majors": profile.target_majors,
            "gpa": profile.gpa,
            "extracurriculars": profile.extracurriculars[:5],  # Limit for brevity
            "current_grade": profile.current_grade.value
        })
    
    return json.dumps(results, indent=2)


def search_by_major_tool(major: str, top_k: int = 10) -> str:
    """
    Search for profiles by target major.
    
    Args:
        major: Major to search for (e.g., "Computer Science")
        top_k: Maximum number of results
        
    Returns:
        JSON string with matching profiles
    """
    db = get_database()
    profiles = db.search_by_major(major, top_k=top_k)
    
    results = []
    for profile in profiles:
        results.append({
            "name": profile.name,
            "target_major": profile.target_majors[0] if profile.target_majors else None,
            "target_colleges": profile.target_colleges,
            "gpa": profile.gpa,
            "courses_taken": profile.courses_taken,
            "interests": profile.interests
        })
    
    return json.dumps(results, indent=2)


def search_by_college_tool(college: str, top_k: int = 10) -> str:
    """
    Search for profiles targeting a specific college.
    
    Args:
        college: College name (e.g., "MIT")
        top_k: Maximum number of results
        
    Returns:
        JSON string with matching profiles
    """
    db = get_database()
    profiles = db.search_by_college(college, top_k=top_k)
    
    results = []
    for profile in profiles:
        results.append({
            "name": profile.name,
            "target_college": college,
            "target_majors": profile.target_majors,
            "gpa": profile.gpa,
            "test_scores": profile.test_scores,
            "extracurriculars": profile.extracurriculars
        })
    
    return json.dumps(results, indent=2)


def find_similar_profiles_tool(
    interests: str,
    majors: str = "",
    top_k: int = 5
) -> str:
    """
    Find profiles similar to given interests and majors.
    
    Args:
        interests: Comma-separated interests
        majors: Comma-separated majors (optional)
        top_k: Maximum number of results
        
    Returns:
        JSON string with similar profiles and similarity scores
    """
    from ..agents.profile_agent import normalize
    
    # Create a temporary profile for similarity matching
    temp_profile = normalize({
        "name": "Temp",
        "current_grade": 12,
        "interests": [i.strip() for i in interests.split(",") if i.strip()],
        "target_majors": [m.strip() for m in majors.split(",") if m.strip()] if majors else [],
        "target_colleges": []
    })
    
    db = get_database()
    all_profiles = db.get_all_profiles()
    
    # Use existing similarity matching
    similar = find_similar_profiles(temp_profile, all_profiles, top_k=top_k)
    
    results = []
    for sim_profile in similar:
        results.append({
            "name": sim_profile.profile.name,
            "similarity_score": round(sim_profile.similarity_score, 3),
            "interests": sim_profile.profile.interests,
            "target_colleges": sim_profile.profile.target_colleges,
            "target_majors": sim_profile.profile.target_majors,
            "colleges_admitted": sim_profile.colleges_admitted,
            "final_major": sim_profile.final_major,
            "gpa": sim_profile.profile.gpa
        })
    
    return json.dumps(results, indent=2)


def get_opportunities_tool(grade: int, interests: str = "") -> str:
    """
    Get relevant opportunities for a grade level and interests.
    
    Args:
        grade: Grade level (9, 10, 11, or 12)
        interests: Comma-separated interests (optional)
        
    Returns:
        JSON string with relevant opportunities
    """
    from ..models import Grade
    
    try:
        grade_enum = Grade(grade)
    except ValueError:
        return json.dumps({"error": f"Invalid grade: {grade}. Must be 9, 10, 11, or 12"})
    
    all_opportunities = load_opportunities()
    
    # Filter by grade
    relevant = [opp for opp in all_opportunities if grade_enum in opp.grade_levels]
    
    # Filter by interests if provided
    if interests:
        interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]
        filtered = []
        for opp in relevant:
            opp_text = (opp.name + " " + opp.description).lower()
            if any(interest in opp_text for interest in interest_list):
                filtered.append(opp)
        relevant = filtered
    
    results = []
    for opp in relevant[:10]:  # Limit to 10
        results.append({
            "name": opp.name,
            "type": opp.type,
            "description": opp.description,
            "requirements": opp.requirements,
            "benefits": opp.benefits,
            "deadline": opp.deadline
        })
    
    return json.dumps(results, indent=2)


def get_profile_statistics_tool() -> str:
    """
    Get statistics about profiles in the database.
    
    Returns:
        JSON string with statistics
    """
    db = get_database()
    all_profiles = db.get_all_profiles()
    
    stats = {
        "total_profiles": len(all_profiles),
        "by_grade": {},
        "by_major": {},
        "by_college": {}
    }
    
    # Count by grade
    for profile in all_profiles:
        grade = profile.current_grade.value
        stats["by_grade"][grade] = stats["by_grade"].get(grade, 0) + 1
    
    # Count by major
    for profile in all_profiles:
        for major in profile.target_majors:
            stats["by_major"][major] = stats["by_major"].get(major, 0) + 1
    
    # Count by college
    for profile in all_profiles:
        for college in profile.target_colleges:
            stats["by_college"][college] = stats["by_college"].get(college, 0) + 1
    
    return json.dumps(stats, indent=2)

