"""
Critic Agent: Evaluates and critiques plans, acting as a loop agent for refinement.
Uses Google ADK Agent for intelligent critique.
"""
from typing import Dict, Any
import json
import warnings
from ..models import StudentProfile, FourYearPlan, Critique
from ..config import get_gemini_model
from ..utils.adk_helper import run_agent_sync, extract_json_from_response


def _create_critic_agent():
    """
    Create a Google ADK Agent for plan critique.
    
    Returns:
        ADK Agent instance configured for critique
    """
    try:
        from google.adk.agents import Agent
        from google.adk.tools import FunctionTool
        from ..tools.agent_tools import (
            find_similar_profiles_tool,
            search_by_college_tool,
            search_by_major_tool,
            get_profile_statistics_tool
        )
        
        agent = Agent(
            name="critic_agent",
            model=get_gemini_model(),
            description="Evaluates and critiques 4-year plans, identifying strengths, weaknesses, and improvement suggestions",
            instruction="""You are a plan critique agent. Your task is to evaluate 4-year high school plans.

Given a student profile and their 4-year plan, you should:
1. Identify strengths of the plan (course alignment, progression, extracurricular depth, etc.)
2. Identify weaknesses (missing courses, lack of rigor, gaps in preparation, etc.)
3. Generate specific suggestions for improvement
4. Calculate an overall quality score (0.0 to 1.0)
5. Determine if the plan needs revision (boolean)

Evaluate based on:
- Alignment with student interests and target majors/colleges
- Academic progression and rigor
- Extracurricular depth and leadership opportunities
- Test preparation timeline
- Balance and feasibility

You have access to tools to help with evaluation:
- find_similar_profiles: Find successful students with similar interests/majors to compare against
- search_by_college: See what students who got into target colleges did
- search_by_major: See course patterns for students pursuing the same major
- get_profile_statistics: Get database statistics to understand benchmarks

Use these tools to make data-driven critiques. Compare the plan against what successful similar students did.

Return your response as structured JSON with:
- strengths: List of identified strengths
- weaknesses: List of identified weaknesses
- suggestions: List of improvement suggestions
- score: Float between 0.0 and 1.0
- needs_revision: Boolean indicating if plan needs changes""",
            tools=[
                FunctionTool(find_similar_profiles_tool),
                FunctionTool(search_by_college_tool),
                FunctionTool(search_by_major_tool),
                FunctionTool(get_profile_statistics_tool)
            ]
        )
        return agent
    except ImportError as e:
        raise ImportError(
            f"google-adk is not available. Please activate your virtual environment and install: pip install google-adk\n"
            f"Original error: {e}"
        )


def get_critic_agent():
    """Get or create the critic agent instance."""
    global _critic_agent_instance
    if _critic_agent_instance is None:
        _critic_agent_instance = _create_critic_agent()
    return _critic_agent_instance


# Global agent instance (lazy initialization)
_critic_agent_instance = None


def critique(
    profile: StudentProfile,
    plan: FourYearPlan,
    max_iterations: int = 3
) -> Critique:
    """
    Critique a plan and determine if it needs revision.
    Uses ADK Agent when available, falls back to rule-based critique.
    This acts as a loop agent that can trigger plan refinement.
    
    Args:
        profile: The student's profile
        plan: The 4-year plan to critique
        max_iterations: Maximum number of critique iterations
        
    Returns:
        Critique object with evaluation
    """
    # Try using ADK Agent
    try:
        agent = get_critic_agent()
        return _critique_with_agent(profile, plan, agent)
    except (ImportError, RuntimeError) as e:
        print(f"Warning: ADK Critic Agent unavailable ({e}). Using rule-based critique.")
    
    # Fallback to rule-based critique
    return _critique_rule_based(profile, plan)


def _critique_with_agent(
    profile: StudentProfile,
    plan: FourYearPlan,
    agent
) -> Critique:
    """Critique plan using ADK Agent."""
    # Prepare plan summary for agent
    plan_summary = {
        "freshman": {
            "courses": plan.freshman_plan.courses,
            "extracurriculars": plan.freshman_plan.extracurriculars,
            "competitions": plan.freshman_plan.competitions,
            "goals": plan.freshman_plan.goals
        },
        "sophomore": {
            "courses": plan.sophomore_plan.courses,
            "extracurriculars": plan.sophomore_plan.extracurriculars,
            "competitions": plan.sophomore_plan.competitions,
            "goals": plan.sophomore_plan.goals
        },
        "junior": {
            "courses": plan.junior_plan.courses,
            "extracurriculars": plan.junior_plan.extracurriculars,
            "test_prep": plan.junior_plan.test_prep,
            "goals": plan.junior_plan.goals
        },
        "senior": {
            "courses": plan.senior_plan.courses,
            "extracurriculars": plan.senior_plan.extracurriculars,
            "goals": plan.senior_plan.goals
        },
        "overall_strategy": plan.overall_strategy,
        "key_milestones": plan.key_milestones
    }
    
    prompt = f"""Evaluate this 4-year high school plan:

Student Profile:
- Interests: {', '.join(profile.interests)}
- Target Majors: {', '.join(profile.target_majors) if profile.target_majors else 'Not specified'}
- Target Colleges: {', '.join(profile.target_colleges) if profile.target_colleges else 'Not specified'}
- Current Grade: {profile.current_grade.name}
- Academic Strengths: {', '.join(profile.academic_strengths) if profile.academic_strengths else 'Not specified'}

4-Year Plan:
{json.dumps(plan_summary, indent=2)}

Evaluate the plan and return JSON with:
- strengths: List of plan strengths
- weaknesses: List of plan weaknesses  
- suggestions: List of improvement suggestions
- score: Float 0.0-1.0 (overall quality)
- needs_revision: Boolean (true if plan needs changes)"""

    try:
        # Suppress warnings from ADK library about non-text parts (function calls)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*non-text parts.*")
            warnings.filterwarnings("ignore", category=UserWarning)
            
            response = run_agent_sync(agent, prompt)
        
        critique_data = extract_json_from_response(response)
        
        if critique_data:
            return Critique(
                strengths=critique_data.get("strengths", []),
                weaknesses=critique_data.get("weaknesses", []),
                suggestions=critique_data.get("suggestions", []),
                score=float(critique_data.get("score", 0.5)),
                needs_revision=bool(critique_data.get("needs_revision", False))
            )
    except Exception as e:
        print(f"Warning: Error parsing ADK agent response ({e}). Falling back to rule-based critique.")
    
    # Fallback if agent response parsing fails
    return _critique_rule_based(profile, plan)


def _critique_rule_based(
    profile: StudentProfile,
    plan: FourYearPlan
) -> Critique:
    """Critique plan using rule-based logic (original implementation)."""
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

