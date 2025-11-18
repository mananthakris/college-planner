"""
Example usage of the College Planner system.
"""
from src import run_pipeline


def example_1_freshman_cs_student():
    """Example: Freshman student interested in Computer Science."""
    profile = {
        "name": "Alex Johnson",
        "current_grade": 9,
        "interests": ["Computer Science", "Mathematics", "Robotics"],
        "academic_strengths": ["Math", "Science", "Problem Solving"],
        "courses_taken": [],
        "courses_planned": [],
        "extracurriculars": ["Robotics Club"],
        "achievements": [],
        "target_colleges": ["MIT", "Stanford", "UC Berkeley"],
        "target_majors": ["Computer Science", "Engineering"],
        "gpa": None,
        "test_scores": {}
    }
    
    result = run_pipeline(profile, max_iterations=3, min_score_threshold=0.7)
    
    print("\n" + "="*80)
    print("EXAMPLE 1: Freshman CS Student")
    print("="*80)
    print(result["explanation"].summary)
    print(f"\nFinal Score: {result['final_score']:.0%}")
    print(f"Iterations: {result['iterations']}")
    return result


def example_2_sophomore_premed_student():
    """Example: Sophomore student interested in Pre-Med."""
    profile = {
        "name": "Sarah Chen",
        "current_grade": 10,
        "interests": ["Biology", "Medicine", "Research"],
        "academic_strengths": ["Biology", "Chemistry", "Writing"],
        "courses_taken": ["Biology", "Chemistry", "Algebra II"],
        "courses_planned": [],
        "extracurriculars": ["Science Club", "Hospital Volunteer"],
        "achievements": ["Science Fair Regional Winner"],
        "target_colleges": ["Johns Hopkins", "Harvard", "Yale"],
        "target_majors": ["Biology", "Pre-Med"],
        "gpa": 3.8,
        "test_scores": {}
    }
    
    result = run_pipeline(profile, max_iterations=3, min_score_threshold=0.7)
    
    print("\n" + "="*80)
    print("EXAMPLE 2: Sophomore Pre-Med Student")
    print("="*80)
    print(result["explanation"].summary)
    print(f"\nFinal Score: {result['final_score']:.0%}")
    print(f"Iterations: {result['iterations']}")
    return result


if __name__ == "__main__":
    # Run examples
    example_1_freshman_cs_student()
    example_2_sophomore_premed_student()

