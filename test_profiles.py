"""
Test script for Engineering and Pre-Med student profiles.
"""
import json
import os
from src import run_pipeline


def print_section_header(title, char="=", width=80):
    """Print a formatted section header."""
    print("\n" + char * width)
    print(title.center(width))
    print(char * width + "\n")


def print_profile_info(profile):
    """Print profile information."""
    print(f"Student Name: {profile['name']}")
    print(f"Current Grade: {profile['current_grade']}")
    print(f"Interests: {', '.join(profile['interests'])}")
    print(f"Academic Strengths: {', '.join(profile['academic_strengths'])}")
    print(f"Target Colleges: {', '.join(profile['target_colleges'])}")
    print(f"Target Majors: {', '.join(profile['target_majors'])}")
    if profile.get('gpa'):
        print(f"Current GPA: {profile['gpa']}")
    if profile.get('extracurriculars'):
        print(f"Current ECs: {', '.join(profile['extracurriculars'])}")


def display_results(result, save_to_file=True):
    """Display comprehensive results."""
    # Summary
    print_section_header("PLAN SUMMARY")
    print(result["explanation"].summary)
    
    # Plan Overview
    print_section_header("OVERALL STRATEGY")
    print(result["explanation"].plan_overview)
    
    # Year by Year Breakdown
    print_section_header("YEAR-BY-YEAR BREAKDOWN")
    for year_name, breakdown in result["explanation"].year_by_year.items():
        print(breakdown)
        print("-" * 80 + "\n")
    
    # Key Recommendations
    print_section_header("KEY RECOMMENDATIONS")
    for i, rec in enumerate(result["explanation"].key_recommendations, 1):
        print(f"{i}. {rec}")
    
    # Next Steps
    print_section_header("IMMEDIATE NEXT STEPS")
    for i, step in enumerate(result["explanation"].next_steps, 1):
        print(f"{i}. {step}")
    
    # Evaluation Details
    print_section_header("PLAN EVALUATION")
    print(f"Overall Quality Score: {result['critique'].score:.1%}")
    print(f"Refinement Iterations: {result['iterations']}")
    print(f"Needs Revision: {'Yes' if result['critique'].needs_revision else 'No'}")
    
    print("\n✓ STRENGTHS:")
    for strength in result["critique"].strengths:
        print(f"  • {strength}")
    
    if result["critique"].weaknesses:
        print("\n⚠ AREAS FOR IMPROVEMENT:")
        for weakness in result["critique"].weaknesses:
            print(f"  • {weakness}")
    
    if result["critique"].suggestions:
        print("\n💡 SUGGESTIONS:")
        for suggestion in result["critique"].suggestions[:5]:  # Top 5
            print(f"  • {suggestion}")
    
    # Save to file
    if save_to_file:
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/{result['profile'].name.lower().replace(' ', '_')}_plan.json"
        
        output = {
            "profile": {
                "name": result["profile"].name,
                "current_grade": result["profile"].current_grade.value,
                "interests": result["profile"].interests,
                "academic_strengths": result["profile"].academic_strengths,
                "target_colleges": result["profile"].target_colleges,
                "target_majors": result["profile"].target_majors,
                "gpa": result["profile"].gpa,
                "extracurriculars": result["profile"].extracurriculars
            },
            "plan_summary": result["explanation"].summary,
            "plan_overview": result["explanation"].plan_overview,
            "year_by_year": result["explanation"].year_by_year,
            "recommendations": result["explanation"].key_recommendations,
            "next_steps": result["explanation"].next_steps,
            "evaluation": {
                "score": result["critique"].score,
                "strengths": result["critique"].strengths,
                "weaknesses": result["critique"].weaknesses,
                "suggestions": result["critique"].suggestions,
                "needs_revision": result["critique"].needs_revision
            },
            "iterations": result["iterations"],
            "final_score": result["final_score"]
        }
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")


def test_engineering_student():
    """Test with an engineering-focused student profile."""
    print_section_header("TEST 1: ENGINEERING STUDENT", char="#")
    
    profile = {
        "name": "Jordan Martinez",
        "current_grade": 9,
        "interests": ["Engineering", "Physics", "Mathematics", "Robotics"],
        "academic_strengths": ["Math", "Physics", "Problem Solving", "Design"],
        "courses_taken": [],
        "courses_planned": [],
        "extracurriculars": ["Robotics Club", "Engineering Club"],
        "achievements": [],
        "target_colleges": ["MIT", "Stanford", "Caltech", "Georgia Tech"],
        "target_majors": ["Mechanical Engineering", "Aerospace Engineering"],
        "gpa": None,
        "test_scores": {}
    }
    
    print("PROFILE INPUT:")
    print_profile_info(profile)
    print("\n" + "=" * 80)
    print("PROCESSING...")
    print("=" * 80)
    
    # Run pipeline
    result = run_pipeline(profile, max_iterations=3, min_score_threshold=0.7)
    
    # Display results
    display_results(result)
    
    return result


def test_premed_student():
    """Test with a pre-med focused student profile."""
    print_section_header("TEST 2: PRE-MED STUDENT", char="#")
    
    profile = {
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
    
    print("PROFILE INPUT:")
    print_profile_info(profile)
    print("\n" + "=" * 80)
    print("PROCESSING...")
    print("=" * 80)
    
    # Run pipeline
    result = run_pipeline(profile, max_iterations=3, min_score_threshold=0.7)
    
    # Display results
    display_results(result)
    
    return result


def compare_results(engineering_result, premed_result):
    """Compare the two results side by side."""
    print_section_header("COMPARISON: ENGINEERING vs PRE-MED", char="#")
    
    print(f"{'Metric':<30} {'Engineering':<25} {'Pre-Med':<25}")
    print("-" * 80)
    print(f"{'Student Name':<30} {engineering_result['profile'].name:<25} {premed_result['profile'].name:<25}")
    eng_score = f"{engineering_result['final_score']:.1%}"
    premed_score = f"{premed_result['final_score']:.1%}"
    print(f"{'Final Score':<30} {eng_score:<25} {premed_score:<25}")
    print(f"{'Iterations':<30} {engineering_result['iterations']:<25} {premed_result['iterations']:<25}")
    print(f"{'Strengths Count':<30} {len(engineering_result['critique'].strengths):<25} {len(premed_result['critique'].strengths):<25}")
    print(f"{'Weaknesses Count':<30} {len(engineering_result['critique'].weaknesses):<25} {len(premed_result['critique'].weaknesses):<25}")
    
    # Course counts
    eng_courses = sum(
        len(yearly_plan.courses)
        for yearly_plan in [
            engineering_result['plan'].freshman_plan,
            engineering_result['plan'].sophomore_plan,
            engineering_result['plan'].junior_plan,
            engineering_result['plan'].senior_plan
        ]
    )
    premed_courses = sum(
        len(yearly_plan.courses)
        for yearly_plan in [
            premed_result['plan'].freshman_plan,
            premed_result['plan'].sophomore_plan,
            premed_result['plan'].junior_plan,
            premed_result['plan'].senior_plan
        ]
    )
    print(f"{'Total Courses Recommended':<30} {eng_courses:<25} {premed_courses:<25}")
    
    # AP courses
    eng_ap = sum(
        len([c for c in yearly_plan.courses if "AP" in c])
        for yearly_plan in [
            engineering_result['plan'].freshman_plan,
            engineering_result['plan'].sophomore_plan,
            engineering_result['plan'].junior_plan,
            engineering_result['plan'].senior_plan
        ]
    )
    premed_ap = sum(
        len([c for c in yearly_plan.courses if "AP" in c])
        for yearly_plan in [
            premed_result['plan'].freshman_plan,
            premed_result['plan'].sophomore_plan,
            premed_result['plan'].junior_plan,
            premed_result['plan'].senior_plan
        ]
    )
    print(f"{'AP Courses Recommended':<30} {eng_ap:<25} {premed_ap:<25}")


def main():
    """Run all tests."""
    print_section_header("COLLEGE PLANNER - PROFILE TESTING", char="#")
    print("Testing the multi-agent system with Engineering and Pre-Med profiles\n")
    
    # Run tests
    engineering_result = test_engineering_student()
    premed_result = test_premed_student()
    
    # Compare results
    compare_results(engineering_result, premed_result)
    
    print_section_header("TESTING COMPLETE", char="#")
    print("✓ Engineering profile test completed")
    print("✓ Pre-Med profile test completed")
    print("\nCheck the 'output/' directory for detailed JSON results.")


if __name__ == "__main__":
    main()

