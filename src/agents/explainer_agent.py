"""
Explainer Agent: Generates user-friendly final output.
"""
from typing import Dict, Any
from ..models import StudentProfile, FourYearPlan, Critique, Explanation, Grade


def explain(
    profile: StudentProfile,
    plan: FourYearPlan,
    critique: Critique
) -> Explanation:
    """
    Generate a comprehensive, user-friendly explanation of the plan.
    
    Args:
        profile: The student's profile
        plan: The 4-year plan
        critique: The critique of the plan
        
    Returns:
        Explanation object with formatted output
    """
    summary = _generate_summary(profile, plan, critique)
    plan_overview = _generate_plan_overview(plan)
    year_by_year = _generate_year_by_year(plan)
    key_recommendations = _generate_key_recommendations(profile, plan, critique)
    next_steps = _generate_next_steps(profile, plan)
    
    return Explanation(
        summary=summary,
        plan_overview=plan_overview,
        year_by_year=year_by_year,
        key_recommendations=key_recommendations,
        next_steps=next_steps
    )


def _generate_summary(profile: StudentProfile, plan: FourYearPlan, critique: Critique) -> str:
    """Generate a high-level summary."""
    summary = f"## 4-Year College Preparation Plan for {profile.name}\n\n"
    
    summary += f"Based on your interests in {', '.join(profile.interests[:3])} "
    summary += f"and your goal of attending {', '.join(profile.target_colleges[:2]) if profile.target_colleges else 'top colleges'}, "
    summary += "this personalized roadmap will help you build a strong college application.\n\n"
    
    summary += f"**Plan Quality Score: {critique.score:.0%}**\n\n"
    
    if critique.score >= 0.8:
        summary += "Your plan is well-structured and aligned with your goals. "
    elif critique.score >= 0.6:
        summary += "Your plan is solid but could benefit from some refinements. "
    else:
        summary += "Your plan needs some adjustments to better align with your goals. "
    
    summary += "See the recommendations below for specific improvements.\n\n"
    
    summary += f"**Target Majors**: {', '.join(profile.target_majors) if profile.target_majors else 'To be determined'}\n"
    summary += f"**Current Grade**: {profile.current_grade.name}\n"
    
    return summary


def _generate_plan_overview(plan: FourYearPlan) -> str:
    """Generate an overview of the entire plan."""
    overview = "## Plan Overview\n\n"
    overview += plan.overall_strategy + "\n\n"
    
    overview += "### Key Milestones:\n"
    for i, milestone in enumerate(plan.key_milestones, 1):
        overview += f"{i}. {milestone}\n"
    
    return overview


def _generate_year_by_year(plan: FourYearPlan) -> Dict[str, str]:
    """Generate detailed year-by-year breakdown."""
    year_breakdowns = {}
    
    for yearly_plan, year_name in [
        (plan.freshman_plan, "Freshman Year (9th Grade)"),
        (plan.sophomore_plan, "Sophomore Year (10th Grade)"),
        (plan.junior_plan, "Junior Year (11th Grade)"),
        (plan.senior_plan, "Senior Year (12th Grade)")
    ]:
        breakdown = f"### {year_name}\n\n"
        
        if yearly_plan.courses:
            breakdown += "**Courses:**\n"
            for course in yearly_plan.courses:
                breakdown += f"- {course}\n"
            breakdown += "\n"
        
        if yearly_plan.extracurriculars:
            breakdown += "**Extracurriculars:**\n"
            for ec in yearly_plan.extracurriculars:
                breakdown += f"- {ec}\n"
            breakdown += "\n"
        
        if yearly_plan.competitions:
            breakdown += "**Competitions:**\n"
            for comp in yearly_plan.competitions:
                breakdown += f"- {comp}\n"
            breakdown += "\n"
        
        if yearly_plan.internships:
            breakdown += "**Internships/Programs:**\n"
            for intern in yearly_plan.internships:
                breakdown += f"- {intern}\n"
            breakdown += "\n"
        
        if yearly_plan.test_prep:
            breakdown += "**Test Preparation:**\n"
            for prep in yearly_plan.test_prep:
                breakdown += f"- {prep}\n"
            breakdown += "\n"
        
        if yearly_plan.goals:
            breakdown += "**Goals:**\n"
            for goal in yearly_plan.goals:
                breakdown += f"- {goal}\n"
            breakdown += "\n"
        
        breakdown += f"**Rationale:** {yearly_plan.rationale}\n"
        
        year_breakdowns[year_name] = breakdown
    
    return year_breakdowns


def _generate_key_recommendations(
    profile: StudentProfile,
    plan: FourYearPlan,
    critique: Critique
) -> list[str]:
    """Generate key recommendations."""
    recommendations = []
    
    # Add critique suggestions
    recommendations.extend(critique.suggestions[:5])  # Top 5 suggestions
    
    # Add plan-specific recommendations
    if critique.strengths:
        recommendations.append(f"✅ Strengths: {', '.join(critique.strengths[:2])}")
    
    # Add profile-specific recommendations
    if profile.target_colleges:
        recommendations.append(f"Research specific admission requirements for {profile.target_colleges[0]}")
    
    if not profile.gpa:
        recommendations.append("Track your GPA throughout high school to ensure you meet target college requirements")
    
    return recommendations


def _generate_next_steps(profile: StudentProfile, plan: FourYearPlan) -> list[str]:
    """Generate immediate next steps."""
    next_steps = []
    
    current_grade = profile.current_grade
    
    if current_grade == Grade.FRESHMAN:
        next_steps.append("Review freshman year plan and start building relationships with teachers")
        next_steps.append("Join clubs and activities that align with your interests")
        next_steps.append("Focus on maintaining strong grades in all courses")
    elif current_grade == Grade.SOPHOMORE:
        next_steps.append("Review sophomore year plan and consider taking more challenging courses")
        next_steps.append("Take on leadership roles in existing extracurriculars")
        next_steps.append("Start exploring potential majors and career paths")
    elif current_grade == Grade.JUNIOR:
        next_steps.append("Begin SAT/ACT preparation and take practice tests")
        next_steps.append("Take on significant leadership roles")
        next_steps.append("Start researching colleges and building your college list")
        next_steps.append("Consider taking AP courses in your areas of interest")
    elif current_grade == Grade.SENIOR:
        next_steps.append("Finalize college list and application strategy")
        next_steps.append("Complete all standardized tests")
        next_steps.append("Request recommendation letters from teachers")
        next_steps.append("Begin working on college essays")
    
    next_steps.append("Review this plan with your school counselor or college advisor")
    next_steps.append("Update your plan as your interests and goals evolve")
    
    return next_steps

