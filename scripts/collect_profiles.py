"""
Script to help collect and format student profiles from various sources.
This is a template - customize based on your data source.
"""
import json
import os
from typing import List, Dict, Any


def load_existing_profiles(file_path: str = "data/student_profiles.json") -> List[Dict[str, Any]]:
    """Load existing profiles from JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return []


def save_profiles(profiles: List[Dict[str, Any]], file_path: str = "data/student_profiles.json"):
    """Save profiles to JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(profiles, f, indent=2)
    print(f"✓ Saved {len(profiles)} profiles to {file_path}")


def validate_profile(profile: Dict[str, Any]) -> bool:
    """Validate that a profile has required fields."""
    required_fields = ["name", "current_grade", "interests", "target_colleges", "target_majors"]
    return all(field in profile for field in required_fields)


def anonymize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Anonymize a profile by removing PII.
    
    IMPORTANT: This is a basic anonymization. Review carefully before using real data.
    """
    # Remove or anonymize name
    if "name" in profile:
        # If it looks like a real name, replace with generic
        if len(profile["name"].split()) > 1:  # Likely a real name
            profile["name"] = f"Student {hash(profile.get('name', '')) % 10000}"
    
    # Remove specific school names if present
    if "school" in profile:
        profile.pop("school")
    
    # Remove addresses
    for key in ["address", "city", "state", "zip", "location"]:
        if key in profile:
            profile.pop(key)
    
    # Remove email/phone
    for key in ["email", "phone", "contact"]:
        if key in profile:
            profile.pop(key)
    
    return profile


def add_profile_interactive():
    """Interactively add a new profile."""
    print("\n" + "="*60)
    print("Add New Student Profile")
    print("="*60 + "\n")
    
    profile = {}
    
    # Basic info
    profile["name"] = input("Name (will be anonymized): ").strip() or "Student"
    grade = input("Current grade (9-12): ").strip()
    try:
        profile["current_grade"] = int(grade) if grade else 12
    except ValueError:
        profile["current_grade"] = 12
    
    # Interests
    interests = input("Interests (comma-separated): ").strip()
    profile["interests"] = [i.strip() for i in interests.split(",") if i.strip()]
    
    # Academic strengths
    strengths = input("Academic strengths (comma-separated): ").strip()
    profile["academic_strengths"] = [s.strip() for s in strengths.split(",") if s.strip()]
    
    # Courses
    courses = input("Courses taken (comma-separated): ").strip()
    profile["courses_taken"] = [c.strip() for c in courses.split(",") if c.strip()]
    
    # Extracurriculars
    ecs = input("Extracurriculars (comma-separated): ").strip()
    profile["extracurriculars"] = [e.strip() for e in ecs.split(",") if e.strip()]
    
    # Target colleges
    colleges = input("Target colleges (comma-separated): ").strip()
    profile["target_colleges"] = [c.strip() for c in colleges.split(",") if c.strip()]
    
    # Target majors
    majors = input("Target majors (comma-separated): ").strip()
    profile["target_majors"] = [m.strip() for m in majors.split(",") if m.strip()]
    
    # Optional fields
    gpa = input("GPA (optional, press Enter to skip): ").strip()
    if gpa:
        try:
            profile["gpa"] = float(gpa)
        except ValueError:
            pass
    
    # Test scores
    sat = input("SAT score (optional): ").strip()
    act = input("ACT score (optional): ").strip()
    test_scores = {}
    if sat:
        try:
            test_scores["SAT"] = int(sat)
        except ValueError:
            pass
    if act:
        try:
            test_scores["ACT"] = int(act)
        except ValueError:
            pass
    if test_scores:
        profile["test_scores"] = test_scores
    
    # Colleges admitted (if known)
    admitted = input("Colleges admitted (comma-separated, optional): ").strip()
    if admitted:
        profile["colleges_admitted"] = [c.strip() for c in admitted.split(",") if c.strip()]
    
    # Final major (if known)
    final_major = input("Final major chosen (optional): ").strip()
    if final_major:
        profile["final_major"] = final_major
    
    # Anonymize
    profile = anonymize_profile(profile)
    
    # Set defaults for missing fields
    profile.setdefault("courses_planned", [])
    profile.setdefault("achievements", [])
    profile.setdefault("additional_info", {})
    
    return profile


def main():
    """Main function to collect profiles."""
    print("="*60)
    print("Student Profile Collection Tool")
    print("="*60)
    print("\nThis tool helps you collect and format student profiles.")
    print("Remember to anonymize all personal information!\n")
    
    # Load existing profiles
    existing = load_existing_profiles()
    print(f"Currently have {len(existing)} profiles in database.\n")
    
    # Collect new profiles
    new_profiles = []
    while True:
        profile = add_profile_interactive()
        
        if validate_profile(profile):
            new_profiles.append(profile)
            print(f"\n✓ Profile added! Total new profiles: {len(new_profiles)}")
        else:
            print("\n⚠ Profile missing required fields. Not added.")
        
        continue_adding = input("\nAdd another profile? (y/n): ").strip().lower()
        if continue_adding != 'y':
            break
    
    # Combine and save
    if new_profiles:
        all_profiles = existing + new_profiles
        save_profiles(all_profiles)
        print(f"\n✓ Added {len(new_profiles)} new profiles")
        print(f"✓ Total profiles: {len(all_profiles)}")
    else:
        print("\nNo new profiles added.")


if __name__ == "__main__":
    main()

