"""
Profile Agent: Normalizes and processes student input.
"""
from typing import Dict, Any
from ..models import StudentProfile, Grade


def normalize(profile_input: Dict[str, Any]) -> StudentProfile:
    """
    Normalize raw student input into a structured StudentProfile.
    
    Args:
        profile_input: Raw dictionary with student information
        
    Returns:
        Normalized StudentProfile object
    """
    # Extract and normalize grade
    current_grade = _normalize_grade(profile_input.get("current_grade", 9))
    
    # Extract lists, ensuring they're lists
    interests = _ensure_list(profile_input.get("interests", []))
    academic_strengths = _ensure_list(profile_input.get("academic_strengths", []))
    courses_taken = _ensure_list(profile_input.get("courses_taken", []))
    courses_planned = _ensure_list(profile_input.get("courses_planned", []))
    extracurriculars = _ensure_list(profile_input.get("extracurriculars", []))
    achievements = _ensure_list(profile_input.get("achievements", []))
    target_colleges = _ensure_list(profile_input.get("target_colleges", []))
    target_majors = _ensure_list(profile_input.get("target_majors", []))
    
    # Extract optional fields
    gpa = profile_input.get("gpa")
    test_scores = profile_input.get("test_scores", {})
    name = profile_input.get("name", "Student")
    additional_info = profile_input.get("additional_info", {})
    
    return StudentProfile(
        name=name,
        current_grade=current_grade,
        interests=interests,
        academic_strengths=academic_strengths,
        courses_taken=courses_taken,
        courses_planned=courses_planned,
        extracurriculars=extracurriculars,
        achievements=achievements,
        target_colleges=target_colleges,
        target_majors=target_majors,
        gpa=gpa,
        test_scores=test_scores,
        additional_info=additional_info
    )


def _normalize_grade(grade_input: Any) -> Grade:
    """Convert various grade inputs to Grade enum."""
    if isinstance(grade_input, Grade):
        return grade_input
    
    if isinstance(grade_input, int):
        return Grade(grade_input)
    
    if isinstance(grade_input, str):
        grade_lower = grade_input.lower()
        if "freshman" in grade_lower or "9" in grade_lower:
            return Grade.FRESHMAN
        elif "sophomore" in grade_lower or "10" in grade_lower:
            return Grade.SOPHOMORE
        elif "junior" in grade_lower or "11" in grade_lower:
            return Grade.JUNIOR
        elif "senior" in grade_lower or "12" in grade_lower:
            return Grade.SENIOR
    
    return Grade.FRESHMAN  # Default


def _ensure_list(value: Any) -> list:
    """Ensure value is a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # Split by comma if it's a string
        return [item.strip() for item in value.split(",") if item.strip()]
    return [value]

