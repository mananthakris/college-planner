"""
Evaluation tools for assessing plan quality and student progress.
"""
from typing import Dict, Any, List
from ..models import FourYearPlan, StudentProfile, Critique


def evaluate_plan_quality(plan: FourYearPlan, profile: StudentProfile) -> Dict[str, Any]:
    """
    Comprehensive evaluation of plan quality.
    
    Args:
        plan: The 4-year plan to evaluate
        profile: The student profile
        
    Returns:
        Dictionary with evaluation metrics
    """
    metrics = {
        "course_rigor": _evaluate_course_rigor(plan),
        "extracurricular_depth": _evaluate_extracurricular_depth(plan),
        "alignment_score": _evaluate_alignment(plan, profile),
        "progression_score": _evaluate_progression(plan),
        "test_prep_score": _evaluate_test_prep(plan),
        "overall_score": 0.0
    }
    
    # Calculate overall score
    metrics["overall_score"] = (
        metrics["course_rigor"] * 0.25 +
        metrics["extracurricular_depth"] * 0.20 +
        metrics["alignment_score"] * 0.25 +
        metrics["progression_score"] * 0.15 +
        metrics["test_prep_score"] * 0.15
    )
    
    return metrics


def _evaluate_course_rigor(plan: FourYearPlan) -> float:
    """Evaluate the rigor of courses across 4 years."""
    all_courses = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_courses.extend(yearly_plan.courses)
    
    # Count AP/Honors courses
    ap_count = sum(1 for course in all_courses if "AP" in course or "Honors" in course)
    
    # Score based on number of AP courses (target: 4-6 for competitive colleges)
    if ap_count >= 6:
        return 1.0
    elif ap_count >= 4:
        return 0.8
    elif ap_count >= 2:
        return 0.6
    else:
        return 0.4


def _evaluate_extracurricular_depth(plan: FourYearPlan) -> float:
    """Evaluate depth and consistency of extracurriculars."""
    all_ecs = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_ecs.extend(yearly_plan.extracurriculars)
    
    unique_ecs = len(set(all_ecs))
    
    # Check for leadership mentions
    leadership_count = sum(
        1 for ec in all_ecs
        if "leadership" in ec.lower() or "president" in ec.lower() or "officer" in ec.lower()
    )
    
    # Score based on diversity and leadership
    diversity_score = min(unique_ecs / 5.0, 1.0)
    leadership_score = min(leadership_count / 2.0, 1.0)
    
    return (diversity_score * 0.6 + leadership_score * 0.4)


def _evaluate_alignment(plan: FourYearPlan, profile: StudentProfile) -> float:
    """Evaluate how well the plan aligns with student interests and goals."""
    all_courses = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_courses.extend(yearly_plan.courses)
    
    # Check interest alignment
    interest_matches = sum(
        1 for interest in profile.interests
        if any(interest.lower() in course.lower() for course in all_courses)
    )
    interest_score = interest_matches / max(len(profile.interests), 1)
    
    # Check major alignment
    major_score = 0.0
    if profile.target_majors:
        major = profile.target_majors[0].lower()
        all_courses_str = " ".join([c.lower() for c in all_courses])
        
        if "computer science" in major:
            major_score = 1.0 if "computer" in all_courses_str else 0.5
        elif "engineering" in major:
            major_score = 1.0 if "calculus" in all_courses_str else 0.5
        elif "biology" in major or "pre-med" in major:
            major_score = 1.0 if "biology" in all_courses_str else 0.5
        else:
            major_score = 0.7  # Generic alignment
    
    return (interest_score * 0.5 + major_score * 0.5)


def _evaluate_progression(plan: FourYearPlan) -> float:
    """Evaluate academic progression across years."""
    # Check that each year has courses
    years_with_courses = sum(
        1 for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]
        if len(yearly_plan.courses) > 0
    )
    
    if years_with_courses == 4:
        return 1.0
    elif years_with_courses == 3:
        return 0.75
    elif years_with_courses == 2:
        return 0.5
    else:
        return 0.25


def _evaluate_test_prep(plan: FourYearPlan) -> float:
    """Evaluate test preparation strategy."""
    # Check if junior year has test prep
    has_junior_prep = len(plan.junior_plan.test_prep) > 0
    # Check if senior year has final prep
    has_senior_prep = len(plan.senior_plan.test_prep) > 0
    
    if has_junior_prep and has_senior_prep:
        return 1.0
    elif has_junior_prep:
        return 0.7
    elif has_senior_prep:
        return 0.5
    else:
        return 0.3

