"""
Data loading utilities for student profiles and opportunities.
"""
import json
import os
from typing import List, Dict, Any
from ..models import StudentProfile, Opportunity, Grade, SimilarProfile


def load_student_profiles(file_path: str = "data/student_profiles.json") -> List[StudentProfile]:
    """
    Load student profiles from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing student profiles
        
    Returns:
        List of StudentProfile objects
    """
    if not os.path.exists(file_path):
        # Return sample profiles for development
        return _get_sample_profiles()
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        profiles = []
        for profile_data in data:
            profile = _dict_to_profile(profile_data)
            profiles.append(profile)
        
        return profiles
    except Exception as e:
        print(f"Error loading profiles: {e}")
        return _get_sample_profiles()


def load_opportunities(file_path: str = "data/opportunities.json") -> List[Opportunity]:
    """
    Load opportunities from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing opportunities
        
    Returns:
        List of Opportunity objects
    """
    if not os.path.exists(file_path):
        return _get_sample_opportunities()
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        opportunities = []
        for opp_data in data:
            opp = _dict_to_opportunity(opp_data)
            opportunities.append(opp)
        
        return opportunities
    except Exception as e:
        print(f"Error loading opportunities: {e}")
        return _get_sample_opportunities()


def find_similar_profiles(
    target_profile: StudentProfile,
    all_profiles: List[StudentProfile],
    top_k: int = 5
) -> List[SimilarProfile]:
    """
    Find similar profiles based on interests, majors, and academic strengths.
    
    Args:
        target_profile: The student profile to find matches for
        all_profiles: List of all available profiles
        top_k: Number of similar profiles to return
        
    Returns:
        List of SimilarProfile objects sorted by similarity
    """
    similarities = []
    
    for profile in all_profiles:
        score = _calculate_similarity(target_profile, profile)
        # For now, we'll create SimilarProfile with mock college data
        # In production, this would come from the profile data
        similar = SimilarProfile(
            profile=profile,
            similarity_score=score,
            colleges_admitted=profile.target_colleges or ["Top University"],
            final_major=profile.target_majors[0] if profile.target_majors else None
        )
        similarities.append(similar)
    
    # Sort by similarity score (descending)
    similarities.sort(key=lambda x: x.similarity_score, reverse=True)
    
    return similarities[:top_k]


def _calculate_similarity(profile1: StudentProfile, profile2: StudentProfile) -> float:
    """Calculate similarity score between two profiles."""
    score = 0.0
    total_weight = 0.0
    
    # Interest overlap (weight: 0.3)
    if profile1.interests and profile2.interests:
        common_interests = set(profile1.interests) & set(profile2.interests)
        interest_score = len(common_interests) / max(len(profile1.interests), len(profile2.interests), 1)
        score += interest_score * 0.3
        total_weight += 0.3
    
    # Major overlap (weight: 0.4)
    if profile1.target_majors and profile2.target_majors:
        common_majors = set(profile1.target_majors) & set(profile2.target_majors)
        major_score = len(common_majors) / max(len(profile1.target_majors), len(profile2.target_majors), 1)
        score += major_score * 0.4
        total_weight += 0.4
    
    # Academic strengths overlap (weight: 0.2)
    if profile1.academic_strengths and profile2.academic_strengths:
        common_strengths = set(profile1.academic_strengths) & set(profile2.academic_strengths)
        strength_score = len(common_strengths) / max(len(profile1.academic_strengths), len(profile2.academic_strengths), 1)
        score += strength_score * 0.2
        total_weight += 0.2
    
    # Extracurricular overlap (weight: 0.1)
    if profile1.extracurriculars and profile2.extracurriculars:
        common_ecs = set(profile1.extracurriculars) & set(profile2.extracurriculars)
        ec_score = len(common_ecs) / max(len(profile1.extracurriculars), len(profile2.extracurriculars), 1)
        score += ec_score * 0.1
        total_weight += 0.1
    
    # Normalize by total weight
    if total_weight > 0:
        return score / total_weight
    
    return 0.0


def _dict_to_profile(data: Dict[str, Any]) -> StudentProfile:
    """Convert dictionary to StudentProfile."""
    from ..agents.profile_agent import normalize
    return normalize(data)


def _dict_to_opportunity(data: Dict[str, Any]) -> Opportunity:
    """Convert dictionary to Opportunity."""
    grade_levels = [Grade(int(g)) for g in data.get("grade_levels", [])]
    return Opportunity(
        name=data["name"],
        type=data.get("type", "extracurricular"),
        grade_levels=grade_levels,
        description=data.get("description", ""),
        requirements=data.get("requirements", []),
        benefits=data.get("benefits", []),
        deadline=data.get("deadline")
    )


def _get_sample_profiles() -> List[StudentProfile]:
    """Return sample profiles for development."""
    from ..agents.profile_agent import normalize
    
    samples = [
        {
            "name": "Sample Student 1",
            "current_grade": 12,
            "interests": ["Computer Science", "Mathematics", "Robotics"],
            "academic_strengths": ["Math", "Science"],
            "courses_taken": ["AP Calculus", "AP Computer Science", "AP Physics"],
            "extracurriculars": ["Robotics Club", "Math Olympiad"],
            "target_colleges": ["MIT", "Stanford", "UC Berkeley"],
            "target_majors": ["Computer Science", "Engineering"]
        },
        {
            "name": "Sample Student 2",
            "current_grade": 12,
            "interests": ["Biology", "Medicine", "Research"],
            "academic_strengths": ["Biology", "Chemistry"],
            "courses_taken": ["AP Biology", "AP Chemistry", "AP Statistics"],
            "extracurriculars": ["Science Research", "Hospital Volunteer"],
            "target_colleges": ["Johns Hopkins", "Harvard", "Yale"],
            "target_majors": ["Biology", "Pre-Med"]
        }
    ]
    
    return [normalize(p) for p in samples]


def _get_sample_opportunities() -> List[Opportunity]:
    """Return sample opportunities for development."""
    return [
        Opportunity(
            name="USAMO (USA Mathematical Olympiad)",
            type="competition",
            grade_levels=[Grade.JUNIOR, Grade.SENIOR],
            description="Prestigious math competition",
            requirements=["Strong math background", "Qualification through AMC"],
            benefits=["National recognition", "College admissions boost"]
        ),
        Opportunity(
            name="Science Research Program",
            type="academic",
            grade_levels=[Grade.SOPHOMORE, Grade.JUNIOR, Grade.SENIOR],
            description="Independent research opportunity",
            requirements=["GPA 3.5+", "Teacher recommendation"],
            benefits=["Research experience", "Publication opportunity"]
        ),
        Opportunity(
            name="Summer Internship - Tech Company",
            type="internship",
            grade_levels=[Grade.JUNIOR, Grade.SENIOR],
            description="Real-world work experience",
            requirements=["Programming skills", "Application"],
            benefits=["Industry experience", "Networking"]
        )
    ]

