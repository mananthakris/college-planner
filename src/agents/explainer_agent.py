"""
Explainer Agent: Generates user-friendly final output.
Uses Google ADK Agent for natural language generation.
"""
from typing import Dict, Any
import json
import warnings
from ..models import StudentProfile, FourYearPlan, Critique, Explanation, Grade
from ..config import get_gemini_model, is_debug_mode
from ..utils.adk_helper import run_agent_sync, extract_json_from_response


def _create_explainer_agent():
    """
    Create a Google ADK Agent for explanation generation.
    
    Returns:
        ADK Agent instance configured for explanation
    """
    try:
        from google.adk.agents import Agent
        from google.adk.tools import FunctionTool
        from ..tools.agent_tools import (
            find_similar_profiles_tool,
            search_by_college_tool,
            get_opportunities_tool
        )
        
        agent = Agent(
            name="explainer_agent",
            model=get_gemini_model(),
            description="Generates user-friendly, comprehensive explanations of 4-year plans for students",
            instruction="""You are an explanation agent. Your task is to generate clear, helpful explanations of 4-year high school plans.

Given a student profile, their 4-year plan, and a critique, you should create:
1. A high-level summary that introduces the plan and highlights key points
2. A plan overview that explains the overall strategy
3. Year-by-year breakdowns with detailed information for each grade
4. Key recommendations based on the critique
5. Immediate next steps for the student

Your explanations should be:
- Clear and easy to understand for high school students
- Encouraging and supportive
- Actionable with specific recommendations
- Well-formatted with proper structure

You have access to tools to enhance your explanations:
- find_similar_profiles: Find success stories of similar students to provide examples
- search_by_college: Get context about what students who got into target colleges did
- get_opportunities: Look up specific opportunities to mention in recommendations

Use these tools to provide concrete examples and specific opportunities when generating explanations.

Return your response as structured JSON with:
- summary: String with high-level overview
- plan_overview: String describing the overall strategy
- year_by_year: Dictionary mapping year names to detailed breakdowns
- key_recommendations: List of important recommendations
- next_steps: List of immediate action items""",
            tools=[
                FunctionTool(find_similar_profiles_tool),
                FunctionTool(search_by_college_tool),
                FunctionTool(get_opportunities_tool)
            ]
        )
        return agent
    except ImportError as e:
        raise ImportError(
            f"google-adk is not available. Please activate your virtual environment and install: pip install google-adk\n"
            f"Original error: {e}"
        )


def get_explainer_agent():
    """Get or create the explainer agent instance."""
    global _explainer_agent_instance
    if _explainer_agent_instance is None:
        _explainer_agent_instance = _create_explainer_agent()
    return _explainer_agent_instance


# Global agent instance (lazy initialization)
_explainer_agent_instance = None


def explain(
    profile: StudentProfile,
    plan: FourYearPlan,
    critique: Critique
) -> Explanation:
    """
    Generate a comprehensive, user-friendly explanation of the plan.
    Uses ADK Agent when available, falls back to rule-based explanation.
    
    Args:
        profile: The student's profile
        plan: The 4-year plan
        critique: The critique of the plan
        
    Returns:
        Explanation object with formatted output
    """
    # Try using ADK Agent
    try:
        agent = get_explainer_agent()
        return _explain_with_agent(profile, plan, critique, agent)
    except (ImportError, RuntimeError) as e:
        print(f"Warning: ADK Explainer Agent unavailable ({e}). Using rule-based explanation.")
    
    # Fallback to rule-based explanation
    return _explain_rule_based(profile, plan, critique)


def _explain_with_agent(
    profile: StudentProfile,
    plan: FourYearPlan,
    critique: Critique,
    agent
) -> Explanation:
    """Generate explanation using ADK Agent."""
    # Prepare plan and critique summary
    plan_data = {
        "overall_strategy": plan.overall_strategy,
        "key_milestones": plan.key_milestones,
        "years": {
            "freshman": {
                "courses": plan.freshman_plan.courses,
                "extracurriculars": plan.freshman_plan.extracurriculars,
                "competitions": plan.freshman_plan.competitions,
                "internships": plan.freshman_plan.internships,
                "test_prep": plan.freshman_plan.test_prep,
                "goals": plan.freshman_plan.goals,
                "rationale": plan.freshman_plan.rationale
            },
            "sophomore": {
                "courses": plan.sophomore_plan.courses,
                "extracurriculars": plan.sophomore_plan.extracurriculars,
                "competitions": plan.sophomore_plan.competitions,
                "internships": plan.sophomore_plan.internships,
                "test_prep": plan.sophomore_plan.test_prep,
                "goals": plan.sophomore_plan.goals,
                "rationale": plan.sophomore_plan.rationale
            },
            "junior": {
                "courses": plan.junior_plan.courses,
                "extracurriculars": plan.junior_plan.extracurriculars,
                "competitions": plan.junior_plan.competitions,
                "internships": plan.junior_plan.internships,
                "test_prep": plan.junior_plan.test_prep,
                "goals": plan.junior_plan.goals,
                "rationale": plan.junior_plan.rationale
            },
            "senior": {
                "courses": plan.senior_plan.courses,
                "extracurriculars": plan.senior_plan.extracurriculars,
                "competitions": plan.senior_plan.competitions,
                "internships": plan.senior_plan.internships,
                "test_prep": plan.senior_plan.test_prep,
                "goals": plan.senior_plan.goals,
                "rationale": plan.senior_plan.rationale
            }
        }
    }
    
    prompt = f"""Generate a comprehensive, user-friendly explanation of this 4-year high school plan:

Student: {profile.name}
Current Grade: {profile.current_grade.name}
Interests: {', '.join(profile.interests)}
Target Majors: {', '.join(profile.target_majors) if profile.target_majors else 'Not specified'}
Target Colleges: {', '.join(profile.target_colleges) if profile.target_colleges else 'Not specified'}

Plan Details:
{json.dumps(plan_data, indent=2)}

Critique:
- Score: {critique.score:.0%}
- Strengths: {', '.join(critique.strengths[:3]) if critique.strengths else 'None'}
- Weaknesses: {', '.join(critique.weaknesses[:3]) if critique.weaknesses else 'None'}
- Suggestions: {', '.join(critique.suggestions[:3]) if critique.suggestions else 'None'}

Generate a clear, encouraging explanation with:
- summary: High-level overview (markdown formatted)
- plan_overview: Overall strategy explanation (markdown formatted)
- year_by_year: Dictionary with keys like "Freshman Year (9th Grade)", "Sophomore Year (10th Grade)", etc., each containing detailed markdown breakdown
- key_recommendations: List of important recommendations
- next_steps: List of immediate action items

Return ONLY valid JSON."""

    try:
        # Suppress warnings from ADK library about non-text parts (function calls)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*non-text parts.*")
            warnings.filterwarnings("ignore", category=UserWarning)
            
            response = run_agent_sync(agent, prompt)
        
        if is_debug_mode():
            print("\n" + "="*80)
            print("DEBUG [explainer_agent]: Explanation Response")
            print("="*80)
            print(f"Response length: {len(str(response))} characters")
            print("="*80 + "\n")
        
        explanation_data = extract_json_from_response(response)
        
        if is_debug_mode():
            print("DEBUG [explainer_agent]: Extracted explanation keys:", 
                  list(explanation_data.keys()) if explanation_data else "None")
        
        if explanation_data:
            return Explanation(
                summary=explanation_data.get("summary", ""),
                plan_overview=explanation_data.get("plan_overview", ""),
                year_by_year=explanation_data.get("year_by_year", {}),
                key_recommendations=explanation_data.get("key_recommendations", []),
                next_steps=explanation_data.get("next_steps", [])
            )
    except Exception as e:
        print(f"Warning: Error parsing ADK agent response ({e}). Falling back to rule-based explanation.")
    
    # Fallback if agent response parsing fails
    return _explain_rule_based(profile, plan, critique)


def _explain_rule_based(
    profile: StudentProfile,
    plan: FourYearPlan,
    critique: Critique
) -> Explanation:
    """Generate explanation using rule-based logic (original implementation)."""
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

