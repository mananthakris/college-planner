"""
Script to enrich and validate student profiles in the database.
"""
import json
import os
from typing import List, Dict, Any


def load_profiles(file_path: str = "data/student_profiles.json") -> List[Dict[str, Any]]:
    """Load profiles from JSON file."""
    if not os.path.exists(file_path):
        return []
    
    with open(file_path, 'r') as f:
        return json.load(f)


def save_profiles(profiles: List[Dict[str, Any]], file_path: str = "data/student_profiles.json"):
    """Save profiles to JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(profiles, f, indent=2)
    print(f"✓ Saved {len(profiles)} profiles")


def enrich_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich profile with default values and inferred data."""
    # Set defaults for missing fields
    profile.setdefault("courses_planned", [])
    profile.setdefault("achievements", [])
    profile.setdefault("additional_info", {})
    profile.setdefault("test_scores", {})
    profile.setdefault("colleges_admitted", [])
    
    # Infer academic strengths from interests/courses
    if not profile.get("academic_strengths"):
        strengths = []
        interests = profile.get("interests", [])
        courses = profile.get("courses_taken", [])
        
        all_text = " ".join(interests + courses).lower()
        
        if "math" in all_text or "calculus" in all_text:
            strengths.append("Mathematics")
        if "science" in all_text or "biology" in all_text or "chemistry" in all_text:
            strengths.append("Science")
        if "computer" in all_text or "programming" in all_text:
            strengths.append("Computer Science")
        if "writing" in all_text or "english" in all_text:
            strengths.append("Writing")
        
        if strengths:
            profile["academic_strengths"] = strengths
    
    # Infer interests from majors if missing
    if not profile.get("interests") and profile.get("target_majors"):
        profile["interests"] = profile["target_majors"].copy()
    
    # Ensure name is anonymized
    if "name" in profile:
        name = profile["name"]
        # If it looks like a real name (has spaces, not "Student X"), anonymize
        if " " in name and not name.startswith("Student"):
            profile["name"] = f"Student {hash(name) % 10000}"
    
    return profile


def validate_profile(profile: Dict[str, Any]) -> tuple[bool, List[str]]:
    """Validate profile and return (is_valid, errors)."""
    errors = []
    
    # Check required fields
    required = ["name", "current_grade", "interests", "target_colleges", "target_majors"]
    for field in required:
        if field not in profile or not profile[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate grade
    if "current_grade" in profile:
        grade = profile["current_grade"]
        if not isinstance(grade, int) or grade < 9 or grade > 12:
            errors.append(f"Invalid grade: {grade}")
    
    # Validate GPA
    if "gpa" in profile and profile["gpa"] is not None:
        gpa = profile["gpa"]
        if not isinstance(gpa, (int, float)) or gpa < 0 or gpa > 5.0:
            errors.append(f"Invalid GPA: {gpa}")
    
    # Validate test scores
    if "test_scores" in profile:
        scores = profile["test_scores"]
        if isinstance(scores, dict):
            if "SAT" in scores and (scores["SAT"] < 400 or scores["SAT"] > 1600):
                errors.append(f"Invalid SAT score: {scores['SAT']}")
            if "ACT" in scores and (scores["ACT"] < 1 or scores["ACT"] > 36):
                errors.append(f"Invalid ACT score: {scores['ACT']}")
    
    return len(errors) == 0, errors


def enrich_all_profiles(file_path: str = "data/student_profiles.json"):
    """Enrich all profiles in the database."""
    profiles = load_profiles(file_path)
    
    if not profiles:
        print("No profiles found.")
        return
    
    print(f"Found {len(profiles)} profiles")
    print("Enriching and validating...\n")
    
    enriched = []
    invalid = []
    
    for i, profile in enumerate(profiles, 1):
        # Enrich
        profile = enrich_profile(profile)
        
        # Validate
        is_valid, errors = validate_profile(profile)
        
        if is_valid:
            enriched.append(profile)
            print(f"✓ Profile {i}: Valid")
        else:
            invalid.append((i, errors))
            print(f"✗ Profile {i}: Invalid - {', '.join(errors)}")
    
    # Save enriched profiles
    save_profiles(enriched, file_path)
    
    print(f"\n✓ Enriched {len(enriched)} profiles")
    if invalid:
        print(f"⚠ {len(invalid)} invalid profiles found (not saved)")
        print("\nInvalid profiles:")
        for idx, errors in invalid:
            print(f"  Profile {idx}: {', '.join(errors)}")


def main():
    """Main function."""
    print("=" * 60)
    print("Profile Enrichment Tool")
    print("=" * 60 + "\n")
    
    enrich_all_profiles()
    
    print("\n✓ Enrichment complete!")
    print("\nNext steps:")
    print("1. Review enriched profiles")
    print("2. Manually fix any invalid profiles")
    print("3. Add more profiles using collect_profiles.py")


if __name__ == "__main__":
    main()

