"""
Orchestrator: Coordinates the multi-agent system for college planning.
"""
from typing import Dict, Any, Optional
from .models import StudentProfile, FourYearPlan, Critique, Explanation
from .agents import profile_agent, retrieval_agent, planner_agent, critic_agent, explainer_agent


def run_pipeline(
    profile_input: Dict[str, Any],
    max_iterations: int = 3,
    min_score_threshold: float = 0.7
) -> Dict[str, Any]:
    """
    Run the complete multi-agent pipeline with iterative refinement.
    
    Args:
        profile_input: Raw student profile input dictionary
        max_iterations: Maximum number of critique-plan refinement iterations
        min_score_threshold: Minimum critique score to accept (0-1)
        
    Returns:
        Dictionary containing profile, plan, critique, explanation, and iteration info
    """
    # Step 1: Profile Agent - Normalize input
    profile = profile_agent.normalize(profile_input)
    
    # Step 2: Retrieval Agent - Find similar profiles and opportunities
    retrieval = retrieval_agent.run_retrieval(profile)
    
    # Step 3-5: Planner-Critic Loop
    plan = None
    critique = None
    iteration = 0
    iteration_history = []
    
    for iteration in range(max_iterations):
        # Step 3: Planner Agent - Create/refine plan
        if iteration == 0:
            plan = planner_agent.plan(profile, retrieval)
        else:
            # Refine plan based on critique
            plan = _refine_plan(profile, plan, critique, retrieval)
        
        # Step 4: Critic Agent - Evaluate plan
        critique = critic_agent.critique(profile, plan, max_iterations=max_iterations)
        
        iteration_history.append({
            "iteration": iteration + 1,
            "score": critique.score,
            "needs_revision": critique.needs_revision,
            "weaknesses": critique.weaknesses
        })
        
        # Check if plan meets quality threshold
        if critique.score >= min_score_threshold and not critique.needs_revision:
            break
    
    # Step 5: Explainer Agent - Generate final output
    explanation = explainer_agent.explain(profile, plan, critique)
    
    return {
        "profile": profile,
        "plan": plan,
        "critique": critique,
        "explanation": explanation,
        "iterations": iteration + 1,
        "iteration_history": iteration_history,
        "final_score": critique.score
    }


def _refine_plan(
    profile: StudentProfile,
    current_plan: FourYearPlan,
    critique: Critique,
    retrieval: Dict[str, Any]
) -> FourYearPlan:
    """
    Refine the plan based on critique feedback.
    
    This is a simplified refinement - in production, this could use
    LLM-based refinement or more sophisticated planning logic.
    """
    # For now, we'll regenerate the plan with the critique in mind
    # In a more sophisticated system, this would use the critique to
    # make targeted improvements to the existing plan
    
    # Re-run planner with awareness of previous weaknesses
    # The planner can use critique information to adjust recommendations
    refined_plan = planner_agent.plan(profile, retrieval)
    
    # Apply specific fixes based on critique
    if any("AP courses" in w for w in critique.weaknesses):
        # Add more AP courses
        if len([c for c in refined_plan.junior_plan.courses if "AP" in c]) < 2:
            if "Computer Science" in profile.interests:
                refined_plan.junior_plan.courses.append("AP Computer Science A")
            if "Mathematics" in profile.interests:
                refined_plan.junior_plan.courses.append("AP Statistics")
    
    if any("summer" in w.lower() for w in critique.weaknesses):
        # Add summer opportunities
        refined_plan.sophomore_plan.internships.append("Summer Research Program")
        refined_plan.junior_plan.internships.append("Summer Internship")
    
    return refined_plan
