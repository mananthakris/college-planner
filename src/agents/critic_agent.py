"""
Critic Agent: Evaluates and critiques plans, acting as a loop agent for refinement.
"""
from typing import Dict, Any
from ..models import StudentProfile, FourYearPlan, Critique


def critique(
    profile: StudentProfile,
    plan: FourYearPlan,
    max_iterations: int = 3
) -> Critique:
    """
    Critique a plan and determine if it needs revision.
    This acts as a loop agent that can trigger plan refinement.
    
    Args:
        profile: The student's profile
        plan: The 4-year plan to critique
        max_iterations: Maximum number of critique iterations
        
    Returns:
        Critique object with evaluation
    """
    strengths = _identify_strengths(profile, plan)
    weaknesses = _identify_weaknesses(profile, plan)
    suggestions = _generate_suggestions(profile, plan, weaknesses)
    score = _calculate_score(profile, plan)
    needs_revision = _needs_revision(score, weaknesses)
    
    return Critique(
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
        score=score,
        needs_revision=needs_revision
    )


def _identify_strengths(profile: StudentProfile, plan: FourYearPlan) -> list[str]:
    """Identify strengths of the plan."""
    strengths = []
    
    # Check alignment with interests
    all_courses = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_courses.extend(yearly_plan.courses)
    
    interest_alignment = any(
        any(interest.lower() in course.lower() for course in all_courses)
        for interest in profile.interests
    )
    
    if interest_alignment:
        strengths.append("Course selection aligns well with student interests")
    
    # Check progression
    if len(plan.freshman_plan.courses) > 0 and len(plan.senior_plan.courses) > 0:
        strengths.append("Shows clear academic progression across 4 years")
    
    # Check extracurricular depth
    all_ecs = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_ecs.extend(yearly_plan.extracurriculars)
    
    if len(set(all_ecs)) >= 3:
        strengths.append("Includes diverse extracurricular activities")
    
    # Check test prep
    if any("SAT" in prep or "ACT" in prep for prep in plan.junior_plan.test_prep):
        strengths.append("Includes appropriate test preparation timeline")
    
    # Check leadership opportunities
    leadership_mentions = sum(
        1 for ec in all_ecs
        if "leadership" in ec.lower() or "president" in ec.lower() or "officer" in ec.lower()
    )
    if leadership_mentions > 0:
        strengths.append("Includes leadership development opportunities")
    
    return strengths


def _identify_weaknesses(profile: StudentProfile, plan: FourYearPlan) -> list[str]:
    """Identify weaknesses in the plan."""
    weaknesses = []
    
    # Check if plan addresses target colleges
    if profile.target_colleges and not plan.overall_strategy:
        weaknesses.append("Plan doesn't clearly address target college requirements")
    
    # Check course rigor progression
    ap_courses = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        ap_courses.extend([c for c in yearly_plan.courses if "AP" in c])
    
    if len(ap_courses) < 3 and profile.target_colleges:
        # Top colleges typically expect more AP courses
        top_college_keywords = ["ivy", "stanford", "mit", "caltech", "harvard", "yale", "princeton"]
        if any(keyword in college.lower() for college in profile.target_colleges for keyword in top_college_keywords):
            weaknesses.append("May need more AP courses for competitive college admissions")
    
    # Check if major-specific courses are included
    if profile.target_majors:
        major = profile.target_majors[0].lower()
        all_courses_str = " ".join([
            c.lower() for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]
            for c in yearly_plan.courses
        ])
        
        if "computer science" in major and "computer" not in all_courses_str:
            weaknesses.append("Missing computer science courses for CS major")
        elif "engineering" in major and "calculus" not in all_courses_str:
            weaknesses.append("Missing calculus for engineering major")
        elif "biology" in major and "biology" not in all_courses_str:
            weaknesses.append("Missing biology courses for biology major")
    
    # Check for balance
    if len(plan.senior_plan.courses) > 6:
        weaknesses.append("Senior year course load may be too heavy with college applications")
    
    # Check for summer opportunities
    if not any("summer" in opp.lower() or "internship" in opp.lower() 
               for yearly_plan in [plan.sophomore_plan, plan.junior_plan]
               for opp in yearly_plan.internships):
        weaknesses.append("Consider adding summer programs or internships")
    
    return weaknesses


def _generate_suggestions(
    profile: StudentProfile,
    plan: FourYearPlan,
    weaknesses: list[str]
) -> list[str]:
    """Generate suggestions to improve the plan."""
    suggestions = []
    
    # Address weaknesses
    for weakness in weaknesses:
        if "AP courses" in weakness:
            suggestions.append("Consider adding 2-3 more AP courses in areas of interest")
        elif "computer science" in weakness.lower():
            suggestions.append("Add computer science courses starting in sophomore or junior year")
        elif "calculus" in weakness.lower():
            suggestions.append("Ensure calculus is taken by junior year for engineering")
        elif "biology" in weakness.lower():
            suggestions.append("Include AP Biology or advanced biology courses")
        elif "summer" in weakness.lower():
            suggestions.append("Explore summer programs, research opportunities, or internships")
        elif "course load" in weakness.lower():
            suggestions.append("Consider reducing senior year course load to focus on applications")
    
    # General suggestions
    if profile.target_colleges:
        suggestions.append(f"Research specific requirements for {profile.target_colleges[0]}")
    
    if not plan.junior_plan.competitions:
        suggestions.append("Consider participating in competitions related to your interests")
    
    if len(plan.senior_plan.extracurriculars) < 2:
        suggestions.append("Maintain consistent extracurricular involvement through senior year")
    
    return suggestions


def _calculate_score(profile: StudentProfile, plan: FourYearPlan) -> float:
    """Calculate an overall score for the plan (0-1)."""
    score = 0.0
    max_score = 0.0
    
    # Course alignment (0.25)
    all_courses = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_courses.extend(yearly_plan.courses)
    
    interest_match = sum(
        1 for interest in profile.interests
        if any(interest.lower() in course.lower() for course in all_courses)
    )
    course_score = min(interest_match / max(len(profile.interests), 1), 1.0)
    score += course_score * 0.25
    max_score += 0.25
    
    # Progression (0.2)
    if (len(plan.freshman_plan.courses) > 0 and len(plan.sophomore_plan.courses) > 0 and
        len(plan.junior_plan.courses) > 0 and len(plan.senior_plan.courses) > 0):
        score += 0.2
    max_score += 0.2
    
    # Extracurricular diversity (0.2)
    all_ecs = []
    for yearly_plan in [plan.freshman_plan, plan.sophomore_plan, plan.junior_plan, plan.senior_plan]:
        all_ecs.extend(yearly_plan.extracurriculars)
    
    unique_ecs = len(set(all_ecs))
    ec_score = min(unique_ecs / 5.0, 1.0)  # Target: 5+ unique ECs
    score += ec_score * 0.2
    max_score += 0.2
    
    # Test prep (0.15)
    if any("SAT" in prep or "ACT" in prep for prep in plan.junior_plan.test_prep):
        score += 0.15
    max_score += 0.15
    
    # Major alignment (0.2)
    if profile.target_majors:
        major = profile.target_majors[0].lower()
        all_courses_str = " ".join([c.lower() for c in all_courses])
        
        if "computer science" in major and "computer" in all_courses_str:
            score += 0.2
        elif "engineering" in major and "calculus" in all_courses_str:
            score += 0.2
        elif "biology" in major and "biology" in all_courses_str:
            score += 0.2
        else:
            score += 0.1  # Partial credit
    max_score += 0.2
    
    # Normalize
    if max_score > 0:
        return min(score / max_score, 1.0)
    
    return 0.5  # Default score


def _needs_revision(score: float, weaknesses: list[str]) -> bool:
    """Determine if the plan needs revision."""
    # Needs revision if score is low or has critical weaknesses
    if score < 0.6:
        return True
    
    # Critical weaknesses that require revision
    critical_keywords = ["missing", "need", "too heavy", "consider"]
    if any(keyword in weakness.lower() for weakness in weaknesses for keyword in critical_keywords):
        if len(weaknesses) >= 2:
            return True
    
    return False

