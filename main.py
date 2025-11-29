"""
Main entry point for the College Planner application.
"""
import json
from src import run_pipeline


def main():
    """Run the college planner with example input."""
    # Example student profile input
    example_profile = {
        "name": "Alex Johnson",
        "current_grade": 10,
        "interests": ["Pre-Med", "Biology", "Neuroscience"],
        "academic_strengths": ["Science", "History", "Problem Solving", "French"],
        "courses_taken": ["AP CSP", "AP French", "AP US History", "AP Human Geography", "AP Pre-Calculus", "AP Physics 1"],
        "courses_planned": [],
        "extracurriculars": ["Research", "Nursing Home Volunteering", "Orchestra", "Science Fair", "Biology Olympiad"],
        "achievements": ["Science Fair Regional Winner", "Science Fair State Finalist", "Viola Regional Winner", "Viola All-State","MIT Poster Project","Columbia Poster Project","UT HSRA"],
        "target_colleges": ["UT Austin", "Stanford", "Northwestern", "Washington University in St. Louis","Emory University", "Baylor University BS/MD","Boston University", "University of Houston BS/MD"],
        "target_majors": ["Neuroscience", "BioChemistry","Pre-Med"],
        "gpa": 4.0,
        "test_scores": {}
    }
    
    print("=" * 80)
    print("COLLEGE PLANNER - Multi-Agent System")
    print("=" * 80)
    print("\nProcessing student profile...")
    print(f"Student: {example_profile['name']}")
    print(f"Grade: {example_profile['current_grade']}")
    print(f"Interests: {', '.join(example_profile['interests'])}")
    print(f"Target Colleges: {', '.join(example_profile['target_colleges'])}")
    print("\n" + "=" * 80 + "\n")
    
    # Run the pipeline
    result = run_pipeline(example_profile, max_iterations=3, min_score_threshold=0.7)
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS")
    print("=" * 80 + "\n")
    
    # Summary
    print(result["explanation"].summary)
    print("\n")
    
    # Plan Overview
    print(result["explanation"].plan_overview)
    print("\n")
    
    # Year by Year
    print("=" * 80)
    print("YEAR-BY-YEAR BREAKDOWN")
    print("=" * 80 + "\n")
    for year_name, breakdown in result["explanation"].year_by_year.items():
        print(breakdown)
        print("-" * 80 + "\n")
    
    # Key Recommendations
    print("=" * 80)
    print("KEY RECOMMENDATIONS")
    print("=" * 80 + "\n")
    for i, rec in enumerate(result["explanation"].key_recommendations, 1):
        print(f"{i}. {rec}")
    print("\n")
    
    # Next Steps
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80 + "\n")
    for i, step in enumerate(result["explanation"].next_steps, 1):
        print(f"{i}. {step}")
    print("\n")
    
    # Critique Summary
    print("=" * 80)
    print("PLAN EVALUATION")
    print("=" * 80 + "\n")
    print(f"Overall Score: {result['critique'].score:.0%}")
    print(f"Iterations: {result['iterations']}")
    print(f"\nStrengths:")
    for strength in result["critique"].strengths:
        print(f"  ✓ {strength}")
    print(f"\nAreas for Improvement:")
    for weakness in result["critique"].weaknesses:
        print(f"  • {weakness}")
    print("\n")
    
    # Save to file
    output_file = "output/college_plan.json"
    try:
        import os
        os.makedirs("output", exist_ok=True)
        
        # Convert to JSON-serializable format
        output = {
            "profile": {
                "name": result["profile"].name,
                "current_grade": result["profile"].current_grade.value,
                "interests": result["profile"].interests,
                "target_colleges": result["profile"].target_colleges,
                "target_majors": result["profile"].target_majors
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
                "suggestions": result["critique"].suggestions
            },
            "iterations": result["iterations"]
        }
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Note: Could not save to file: {e}")


if __name__ == "__main__":
    main()

