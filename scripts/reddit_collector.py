"""
Script to help collect student profiles from Reddit (r/collegeresults).
IMPORTANT: Always anonymize data and respect Reddit's terms of service.
"""
import json
import re
from typing import List, Dict, Any, Optional
import os


def parse_reddit_post(text: str) -> Optional[Dict[str, Any]]:
    """
    Parse a Reddit post from r/collegeresults into a profile.
    
    This is a basic parser - you may need to customize based on post format.
    """
    profile = {
        "name": "Student",  # Always anonymized
        "current_grade": 12,  # Assume senior if not specified
        "interests": [],
        "academic_strengths": [],
        "courses_taken": [],
        "courses_planned": [],
        "extracurriculars": [],
        "achievements": [],
        "target_colleges": [],
        "target_majors": [],
        "gpa": None,
        "test_scores": {},
        "colleges_admitted": [],
        "final_major": None,
        "additional_info": {}
    }
    
    text_lower = text.lower()
    
    # Extract GPA
    gpa_match = re.search(r'gpa[:\s]+([\d.]+)', text_lower)
    if gpa_match:
        try:
            profile["gpa"] = float(gpa_match.group(1))
        except ValueError:
            pass
    
    # Extract SAT
    sat_match = re.search(r'sat[:\s]+(\d{3,4})', text_lower)
    if sat_match:
        try:
            profile["test_scores"]["SAT"] = int(sat_match.group(1))
        except ValueError:
            pass
    
    # Extract ACT
    act_match = re.search(r'act[:\s]+(\d{1,2})', text_lower)
    if act_match:
        try:
            profile["test_scores"]["ACT"] = int(act_match.group(1))
        except ValueError:
            pass
    
    # Extract major (common patterns)
    major_patterns = [
        r'major[:\s]+([a-z\s]+)',
        r'studying\s+([a-z\s]+)',
        r'pursuing\s+([a-z\s]+)'
    ]
    for pattern in major_patterns:
        match = re.search(pattern, text_lower)
        if match:
            major = match.group(1).strip()
            if major and len(major) < 50:  # Reasonable length
                profile["target_majors"].append(major.title())
                profile["final_major"] = major.title()
            break
    
    # Extract colleges (common names)
    college_keywords = {
        "mit": "MIT",
        "stanford": "Stanford",
        "harvard": "Harvard",
        "yale": "Yale",
        "princeton": "Princeton",
        "columbia": "Columbia",
        "upenn": "University of Pennsylvania",
        "penn": "University of Pennsylvania",
        "caltech": "Caltech",
        "berkeley": "UC Berkeley",
        "ucla": "UCLA",
        "usc": "USC",
        "nyu": "NYU",
        "cornell": "Cornell",
        "duke": "Duke",
        "jhu": "Johns Hopkins",
        "johns hopkins": "Johns Hopkins"
    }
    
    for keyword, college in college_keywords.items():
        if keyword in text_lower:
            # Check if it's in accepted/rejected section
            if "accepted" in text_lower or "admitted" in text_lower:
                if college not in profile["colleges_admitted"]:
                    profile["colleges_admitted"].append(college)
            if college not in profile["target_colleges"]:
                profile["target_colleges"].append(college)
    
    # Extract courses (AP courses)
    ap_courses = re.findall(r'ap\s+([a-z\s]+)', text_lower)
    for course in ap_courses:
        course_clean = course.strip().title()
        if course_clean and len(course_clean) < 50:
            profile["courses_taken"].append(f"AP {course_clean}")
    
    # Extract extracurriculars (common patterns)
    ec_keywords = [
        "robotics", "debate", "model un", "mun", "science olympiad",
        "math team", "math olympiad", "usamo", "science fair",
        "volunteer", "internship", "research", "club", "sports"
    ]
    
    for keyword in ec_keywords:
        if keyword in text_lower:
            profile["extracurriculars"].append(keyword.title())
    
    # Extract interests from context
    interest_keywords = {
        "computer science": "Computer Science",
        "cs": "Computer Science",
        "engineering": "Engineering",
        "math": "Mathematics",
        "biology": "Biology",
        "chemistry": "Chemistry",
        "physics": "Physics",
        "medicine": "Medicine",
        "pre-med": "Pre-Med"
    }
    
    for keyword, interest in interest_keywords.items():
        if keyword in text_lower:
            profile["interests"].append(interest)
    
    # Only return if we extracted meaningful data
    if (profile["target_majors"] or profile["target_colleges"] or 
        profile["courses_taken"] or profile["extracurriculars"]):
        return profile
    
    return None


def anonymize_profile(profile: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure profile is fully anonymized."""
    # Remove any PII
    profile["name"] = f"Student {hash(str(profile)) % 10000}"
    
    # Remove any location data
    for key in ["location", "city", "state", "school", "high_school"]:
        if key in profile:
            profile.pop(key)
    
    return profile


def collect_from_text_file(file_path: str, output_path: str = "data/student_profiles.json"):
    """
    Collect profiles from a text file containing Reddit posts.
    
    Each post should be separated by a clear delimiter (e.g., "---").
    """
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by delimiter
    posts = content.split("---")
    
    profiles = []
    for post in posts:
        post = post.strip()
        if not post:
            continue
        
        profile = parse_reddit_post(post)
        if profile:
            profile = anonymize_profile(profile)
            profiles.append(profile)
            print(f"✓ Parsed profile: {len(profiles)}")
    
    # Load existing profiles
    existing = []
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            existing = json.load(f)
    
    # Merge and save
    all_profiles = existing + profiles
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_profiles, f, indent=2)
    
    print(f"\n✓ Added {len(profiles)} profiles")
    print(f"✓ Total profiles: {len(all_profiles)}")


def main():
    """Main function."""
    print("=" * 60)
    print("Reddit Profile Collector")
    print("=" * 60)
    print("\nThis script helps parse Reddit posts into student profiles.")
    print("IMPORTANT: Always anonymize data and respect Reddit's ToS.\n")
    
    file_path = input("Enter path to text file with Reddit posts: ").strip()
    
    if not file_path:
        print("No file specified. Exiting.")
        return
    
    collect_from_text_file(file_path)
    
    print("\n✓ Collection complete!")
    print("\nNext steps:")
    print("1. Review the profiles in data/student_profiles.json")
    print("2. Manually verify and enrich the data")
    print("3. Remove any profiles with identifying information")


if __name__ == "__main__":
    main()

