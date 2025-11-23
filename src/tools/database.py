"""
Database utilities for storing and querying student profiles.
Supports JSON file storage (can be migrated to SQL/vector DB later).
"""
import json
import os
from typing import List, Dict, Any, Optional
from ..models import StudentProfile
from ..agents.profile_agent import normalize
from .data_loader import _get_sample_profiles


class StudentProfileDatabase:
    """Database interface for student profiles."""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize the database.
        
        Args:
            db_path: Path to JSON database file. If None, uses default from config
        """
        if db_path is None:
            from ..config import PROFILES_JSON_PATH
            db_path = PROFILES_JSON_PATH
        
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Ensure the database file and directory exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            # Initialize with sample data
            self._initialize_with_samples()
    
    def _initialize_with_samples(self):
        """Initialize database with sample profiles."""
        sample_profiles = _get_sample_profiles()
        profiles_data = [self._profile_to_dict(profile) for profile in sample_profiles]
        self._save_profiles(profiles_data)
    
    def _profile_to_dict(self, profile: StudentProfile) -> Dict[str, Any]:
        """Convert StudentProfile to dictionary for storage."""
        return {
            "name": profile.name,
            "current_grade": profile.current_grade.value,
            "interests": profile.interests,
            "academic_strengths": profile.academic_strengths,
            "courses_taken": profile.courses_taken,
            "courses_planned": profile.courses_planned,
            "extracurriculars": profile.extracurriculars,
            "achievements": profile.achievements,
            "target_colleges": profile.target_colleges,
            "target_majors": profile.target_majors,
            "gpa": profile.gpa,
            "test_scores": profile.test_scores,
            "additional_info": profile.additional_info
        }
    
    def _dict_to_profile(self, data: Dict[str, Any]) -> StudentProfile:
        """Convert dictionary to StudentProfile."""
        return normalize(data)
    
    def _load_profiles(self) -> List[Dict[str, Any]]:
        """Load all profiles from database."""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_profiles(self, profiles: List[Dict[str, Any]]):
        """Save profiles to database."""
        with open(self.db_path, 'w') as f:
            json.dump(profiles, f, indent=2)
    
    def add_profile(self, profile: StudentProfile) -> bool:
        """
        Add a new profile to the database.
        
        Args:
            profile: StudentProfile to add
            
        Returns:
            True if successful
        """
        profiles = self._load_profiles()
        profile_dict = self._profile_to_dict(profile)
        profiles.append(profile_dict)
        self._save_profiles(profiles)
        return True
    
    def get_all_profiles(self) -> List[StudentProfile]:
        """
        Get all profiles from the database.
        
        Returns:
            List of StudentProfile objects
        """
        profiles_data = self._load_profiles()
        return [self._dict_to_profile(data) for data in profiles_data]
    
    def search_by_interests(self, interests: List[str], top_k: int = 10) -> List[StudentProfile]:
        """
        Search profiles by matching interests.
        
        Args:
            interests: List of interest keywords
            top_k: Maximum number of results
            
        Returns:
            List of matching StudentProfile objects
        """
        all_profiles = self.get_all_profiles()
        matches = []
        
        interest_set = set(i.lower() for i in interests)
        
        for profile in all_profiles:
            profile_interests = set(i.lower() for i in profile.interests)
            profile_majors = set(m.lower() for m in profile.target_majors)
            
            # Calculate match score
            common_interests = interest_set & profile_interests
            common_majors = interest_set & profile_majors
            
            if common_interests or common_majors:
                score = len(common_interests) + len(common_majors) * 1.5
                matches.append((score, profile))
        
        # Sort by score and return top_k
        matches.sort(key=lambda x: x[0], reverse=True)
        return [profile for _, profile in matches[:top_k]]
    
    def search_by_major(self, major: str, top_k: int = 10) -> List[StudentProfile]:
        """
        Search profiles by target major.
        
        Args:
            major: Major to search for
            top_k: Maximum number of results
            
        Returns:
            List of matching StudentProfile objects
        """
        all_profiles = self.get_all_profiles()
        major_lower = major.lower()
        
        matches = []
        for profile in all_profiles:
            for profile_major in profile.target_majors:
                if major_lower in profile_major.lower() or profile_major.lower() in major_lower:
                    matches.append(profile)
                    break
        
        return matches[:top_k]
    
    def search_by_college(self, college: str, top_k: int = 10) -> List[StudentProfile]:
        """
        Search profiles by target college.
        
        Args:
            college: College name to search for
            top_k: Maximum number of results
            
        Returns:
            List of matching StudentProfile objects
        """
        all_profiles = self.get_all_profiles()
        college_lower = college.lower()
        
        matches = []
        for profile in all_profiles:
            for target_college in profile.target_colleges:
                if college_lower in target_college.lower() or target_college.lower() in college_lower:
                    matches.append(profile)
                    break
        
        return matches[:top_k]
    
    def get_profile_count(self) -> int:
        """Get total number of profiles in database."""
        return len(self._load_profiles())


# Global database instance
_db_instance: Optional[StudentProfileDatabase] = None


def get_database() -> StudentProfileDatabase:
    """Get or create the global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = StudentProfileDatabase()
    return _db_instance

