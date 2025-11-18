"""
Simple test script for Engineering and Pre-Med profiles.
Run: python3 test_simple.py
"""
from src import run_pipeline


def test_profile(name, profile_dict):
    """Test a single profile and print key results."""
    print(f"\n{'='*80}")
    print(f"TESTING: {name}")
    print(f"{'='*80}\n")
    
    print(f"Student: {profile_dict['name']}")
    print(f"Grade: {profile_dict['current_grade']}")
    print(f"Interests: {', '.join(profile_dict['interests'])}")
    print(f"Target Majors: {', '.join(profile_dict['target_majors'])}")
    print(f"Target Colleges: {', '.join(profile_dict['target_colleges'][:3])}")
    print("\nRunning pipeline...\n")
    
    result = run_pipeline(profile_dict, max_iterations=3, min_score_threshold=0.7)
    
    print(f"✓ Plan Quality Score: {result['final_score']:.0%}")
    print(f"✓ Iterations: {result['iterations']}")
    
    # Show key courses by year
    print("\n📚 KEY COURSES BY YEAR:")
    for year_name, yearly_plan in [
        ("Freshman", result['plan'].freshman_plan),
        ("Sophomore", result['plan'].sophomore_plan),
        ("Junior", result['plan'].junior_plan),
        ("Senior", result['plan'].senior_plan)
    ]:
        if yearly_plan.courses:
            ap_courses = [c for c in yearly_plan.courses if "AP" in c]
            print(f"  {year_name}: {len(yearly_plan.courses)} courses ({len(ap_courses)} AP)")
            if ap_courses:
                print(f"    AP: {', '.join(ap_courses[:3])}")
    
    # Show key extracurriculars
    print("\n🎯 KEY EXTRACURRICULARS:")
    all_ecs = []
    for yearly_plan in [
        result['plan'].freshman_plan,
        result['plan'].sophomore_plan,
        result['plan'].junior_plan,
        result['plan'].senior_plan
    ]:
        all_ecs.extend(yearly_plan.extracurriculars)
    unique_ecs = list(set(all_ecs))[:5]
    for ec in unique_ecs:
        print(f"  • {ec}")
    
    # Show top recommendations
    print("\n💡 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(result['explanation'].key_recommendations[:3], 1):
        print(f"  {i}. {rec}")
    
    # Show evaluation
    print("\n📊 EVALUATION:")
    print(f"  Strengths: {len(result['critique'].strengths)}")
    if result['critique'].weaknesses:
        print(f"  Weaknesses: {len(result['critique'].weaknesses)}")
        print(f"    • {result['critique'].weaknesses[0]}")
    
    return result


# Engineering Profile
engineering_profile = {
    "name": "Jordan Martinez",
    "current_grade": 9,
    "interests": ["Engineering", "Physics", "Mathematics", "Robotics"],
    "academic_strengths": ["Math", "Physics", "Problem Solving"],
    "courses_taken": [],
    "courses_planned": [],
    "extracurriculars": ["Robotics Club", "Engineering Club"],
    "achievements": [],
    "target_colleges": ["MIT", "Stanford", "Caltech", "Georgia Tech"],
    "target_majors": ["Mechanical Engineering", "Aerospace Engineering"],
    "gpa": None,
    "test_scores": {}
}

# Pre-Med Profile
premed_profile = {
    "name": "Maya Patel",
    "current_grade": 9,
    "interests": ["Medicine", "Biology", "Chemistry", "Healthcare"],
    "academic_strengths": ["Biology", "Chemistry", "Writing", "Research"],
    "courses_taken": [],
    "courses_planned": [],
    "extracurriculars": ["Science Club", "Hospital Volunteer"],
    "achievements": [],
    "target_colleges": ["Johns Hopkins", "Harvard", "Yale", "Duke"],
    "target_majors": ["Biology", "Pre-Med", "Biochemistry"],
    "gpa": None,
    "test_scores": {}
}

if __name__ == "__main__":
    print("\n" + "="*80)
    print("COLLEGE PLANNER - ENGINEERING vs PRE-MED TEST")
    print("="*80)
    
    eng_result = test_profile("ENGINEERING STUDENT", engineering_profile)
    premed_result = test_profile("PRE-MED STUDENT", premed_profile)
    
    print(f"\n{'='*80}")
    print("COMPARISON SUMMARY")
    print(f"{'='*80}\n")
    print(f"{'Metric':<25} {'Engineering':<20} {'Pre-Med':<20}")
    print("-" * 65)
    eng_score = f"{eng_result['final_score']:.1%}"
    premed_score = f"{premed_result['final_score']:.1%}"
    print(f"{'Final Score':<25} {eng_score:<20} {premed_score:<20}")
    print(f"{'Iterations':<25} {eng_result['iterations']:<20} {premed_result['iterations']:<20}")
    print(f"{'Strengths':<25} {len(eng_result['critique'].strengths):<20} {len(premed_result['critique'].strengths):<20}")
    print(f"{'Weaknesses':<25} {len(eng_result['critique'].weaknesses):<20} {len(premed_result['critique'].weaknesses):<20}")
    
    print("\n✓ Testing complete! Check the detailed output above.")
    print("  For full details, run: python3 test_profiles.py\n")

