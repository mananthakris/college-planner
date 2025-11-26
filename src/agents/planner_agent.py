"""
Planner Agent: Creates a 4-year roadmap for the student.
Uses Google ADK Agent for intelligent planning.
"""
from typing import Dict, Any
import json
from ..models import (
    StudentProfile, FourYearPlan, YearlyPlan, Grade,
    SimilarProfile, Opportunity
)
from ..config import get_gemini_model
from ..utils.adk_helper import run_agent_sync, extract_json_from_response


def _create_planner_agent():
    """
    Create a Google ADK Agent for 4-year planning.
    
    Returns:
        ADK Agent instance configured for planning
    """
    try:
        from google.adk.agents import Agent
        from google.adk.tools import FunctionTool
        from ..tools.agent_tools import (
            get_opportunities_tool,
            find_similar_profiles_tool,
            search_by_college_tool,
            search_by_major_tool
        )
        
        agent = Agent(
            name="planner_agent",
            model=get_gemini_model(),
            description="Creates comprehensive 4-year roadmaps for students based on their profile and similar successful students",
            instruction="""You are a college planning agent. Your task is to create a detailed 4-year high school roadmap.

Given a student profile and similar successful student profiles, you should:
1. Analyze the student's interests, target colleges, and target majors
2. Review what similar successful students did in each grade year
3. Create a comprehensive plan for each of the 4 years (9th, 10th, 11th, 12th grade)
4. Include courses, extracurriculars, competitions, internships, test prep, and goals for each year
5. Generate an overall strategy and key milestones

For each year, provide:
- Courses: Specific course recommendations aligned with interests and target majors
- Extracurriculars: Activities that build depth in interests
- Competitions: Relevant competitions for the grade level
- Internships: Summer programs or internships (typically for juniors/seniors)
- Test Prep: Standardized test preparation timeline
- Goals: Year-specific goals
- Rationale: Explanation for the year's plan

You have access to tools to query the database:
- get_opportunities: Get relevant opportunities for a specific grade level and interests
- find_similar_profiles: Find students with similar interests and majors
- search_by_college: Find students who targeted a specific college
- search_by_major: Find students pursuing a specific major

Use these tools to gather additional context when creating the plan, especially if you need more information about opportunities or similar students beyond what's provided in the initial context.

Return your response as structured JSON matching the FourYearPlan format.""",
            tools=[
                FunctionTool(get_opportunities_tool),
                FunctionTool(find_similar_profiles_tool),
                FunctionTool(search_by_college_tool),
                FunctionTool(search_by_major_tool)
            ]
        )
        return agent
    except ImportError as e:
        raise ImportError(
            f"google-adk is not available. Please activate your virtual environment and install: pip install google-adk\n"
            f"Original error: {e}"
        )


def get_planner_agent():
    """Get or create the planner agent instance."""
    global _planner_agent_instance
    if _planner_agent_instance is None:
        _planner_agent_instance = _create_planner_agent()
    return _planner_agent_instance


# Global agent instance (lazy initialization)
_planner_agent_instance = None


def plan(
    profile: StudentProfile,
    retrieval: Dict[str, Any]
) -> FourYearPlan:
    """
    Create a comprehensive 4-year plan based on profile and similar students.
    Uses ADK Agent when available, falls back to rule-based planning.
    
    Args:
        profile: The student's profile
        retrieval: Dictionary with similar_profiles and opportunities
        
    Returns:
        FourYearPlan object with detailed roadmap
    """
    # Try using ADK Agent
    try:
        agent = get_planner_agent()
        return _plan_with_agent(profile, retrieval, agent)
    except (ImportError, RuntimeError) as e:
        print(f"Warning: ADK Planner Agent unavailable ({e}). Using rule-based planning.")
    
    # Fallback to rule-based planning
    return _plan_rule_based(profile, retrieval)


def _plan_with_agent(
    profile: StudentProfile,
    retrieval: Dict[str, Any],
    agent
) -> FourYearPlan:
    """Create plan using ADK Agent."""
    similar_profiles = retrieval.get("similar_profiles", [])
    opportunities = retrieval.get("opportunities", [])
    
    # Prepare context for the agent
    similar_profiles_summary = []
    for sp in similar_profiles[:3]:  # Top 3
        similar_profiles_summary.append({
            "interests": sp.profile.interests,
            "target_majors": sp.profile.target_majors,
            "target_colleges": sp.profile.target_colleges,
            "colleges_admitted": sp.colleges_admitted,
            "extracurriculars": sp.profile.extracurriculars
        })
    
    opportunities_summary = [{
        "name": opp.name,
        "type": opp.type,
        "grade_levels": [g.value for g in opp.grade_levels],
        "description": opp.description
    } for opp in opportunities[:10]]
    
    prompt = f"""Create a comprehensive 4-year high school plan for this student:

Student Profile:
- Name: {profile.name}
- Current Grade: {profile.current_grade.name} ({profile.current_grade.value})
- Interests: {', '.join(profile.interests)}
- Target Majors: {', '.join(profile.target_majors) if profile.target_majors else 'Not specified'}
- Target Colleges: {', '.join(profile.target_colleges) if profile.target_colleges else 'Not specified'}
- Academic Strengths: {', '.join(profile.academic_strengths) if profile.academic_strengths else 'Not specified'}
- Current Extracurriculars: {', '.join(profile.extracurriculars) if profile.extracurriculars else 'None'}

Similar Successful Students:
{json.dumps(similar_profiles_summary, indent=2)}

Available Opportunities:
{json.dumps(opportunities_summary, indent=2)}

Create a detailed 4-year plan with:
- freshman_plan: YearlyPlan for 9th grade
- sophomore_plan: YearlyPlan for 10th grade  
- junior_plan: YearlyPlan for 11th grade
- senior_plan: YearlyPlan for 12th grade
- overall_strategy: String describing the overall approach
- key_milestones: List of key milestones

For each YearlyPlan, include:
- grade: Grade enum value (FRESHMAN=9, SOPHOMORE=10, JUNIOR=11, SENIOR=12)
- courses: List of course names
- extracurriculars: List of extracurricular activities
- competitions: List of competitions
- internships: List of internships/programs
- test_prep: List of test preparation activities
- goals: List of goals for the year
- rationale: String explaining the plan

Return ONLY valid JSON matching this structure. Skip years that are before the student's current grade."""

    try:
        response = run_agent_sync(agent, prompt)
        plan_data = extract_json_from_response(response)
        
        if plan_data:
            return _parse_plan_from_json(plan_data, profile)
    except Exception as e:
        print(f"Warning: Error parsing ADK agent response ({e}). Falling back to rule-based planning.")
    
    # Fallback if agent response parsing fails
    return _plan_rule_based(profile, retrieval)


def _parse_plan_from_json(plan_data: dict, profile: StudentProfile) -> FourYearPlan:
    """Parse plan from JSON response."""
    try:
        # Parse yearly plans
        def parse_yearly_plan(year_key: str, grade: Grade) -> YearlyPlan:
            year_data = plan_data.get(year_key, {})
            return YearlyPlan(
                grade=grade,
                courses=year_data.get('courses', []),
                extracurriculars=year_data.get('extracurriculars', []),
                competitions=year_data.get('competitions', []),
                internships=year_data.get('internships', []),
                test_prep=year_data.get('test_prep', []),
                goals=year_data.get('goals', []),
                rationale=year_data.get('rationale', '')
            )
        
        freshman_plan = parse_yearly_plan('freshman_plan', Grade.FRESHMAN)
        sophomore_plan = parse_yearly_plan('sophomore_plan', Grade.SOPHOMORE)
        junior_plan = parse_yearly_plan('junior_plan', Grade.JUNIOR)
        senior_plan = parse_yearly_plan('senior_plan', Grade.SENIOR)
        
        # Parse overall strategy and milestones
        overall_strategy = plan_data.get('overall_strategy', '')
        key_milestones = plan_data.get('key_milestones', [])
        
        return FourYearPlan(
            student_profile=profile,
            freshman_plan=freshman_plan,
            sophomore_plan=sophomore_plan,
            junior_plan=junior_plan,
            senior_plan=senior_plan,
            overall_strategy=overall_strategy,
            key_milestones=key_milestones
        )
    except Exception as e:
        print(f"Warning: Failed to parse JSON plan structure: {e}")
        raise ValueError(f"Failed to parse plan from JSON: {e}")


def _plan_rule_based(
    profile: StudentProfile,
    retrieval: Dict[str, Any]
) -> FourYearPlan:
    """Create plan using rule-based logic (original implementation)."""
    similar_profiles = retrieval.get("similar_profiles", [])
    opportunities = retrieval.get("opportunities", [])
    
    # Determine starting grade
    start_grade = profile.current_grade
    
    # Create plans for each year
    freshman_plan = _create_yearly_plan(
        Grade.FRESHMAN,
        profile,
        similar_profiles,
        opportunities,
        start_grade
    )
    
    sophomore_plan = _create_yearly_plan(
        Grade.SOPHOMORE,
        profile,
        similar_profiles,
        opportunities,
        start_grade
    )
    
    junior_plan = _create_yearly_plan(
        Grade.JUNIOR,
        profile,
        similar_profiles,
        opportunities,
        start_grade
    )
    
    senior_plan = _create_yearly_plan(
        Grade.SENIOR,
        profile,
        similar_profiles,
        opportunities,
        start_grade
    )
    
    # Generate overall strategy
    overall_strategy = _generate_overall_strategy(profile, similar_profiles)
    
    # Identify key milestones
    key_milestones = _identify_milestones(profile, freshman_plan, sophomore_plan, junior_plan, senior_plan)
    
    return FourYearPlan(
        student_profile=profile,
        freshman_plan=freshman_plan,
        sophomore_plan=sophomore_plan,
        junior_plan=junior_plan,
        senior_plan=senior_plan,
        overall_strategy=overall_strategy,
        key_milestones=key_milestones
    )


def _create_yearly_plan(
    grade: Grade,
    profile: StudentProfile,
    similar_profiles: list[SimilarProfile],
    opportunities: list[Opportunity],
    start_grade: Grade
) -> YearlyPlan:
    """Create a plan for a specific grade year."""
    
    # Skip if student has already passed this grade
    if grade.value < start_grade.value:
        return YearlyPlan(
            grade=grade,
            courses=[],
            extracurriculars=[],
            competitions=[],
            internships=[],
            test_prep=[],
            goals=[],
            rationale="Grade already completed"
        )
    
    # Extract courses from similar profiles for this grade
    courses = _recommend_courses(grade, profile, similar_profiles)
    
    # Extract extracurriculars
    extracurriculars = _recommend_extracurriculars(grade, profile, similar_profiles, opportunities)
    
    # Extract competitions
    competitions = _recommend_competitions(grade, profile, opportunities)
    
    # Extract internships
    internships = _recommend_internships(grade, profile, opportunities)
    
    # Test prep recommendations
    test_prep = _recommend_test_prep(grade, profile)
    
    # Set goals
    goals = _set_goals(grade, profile)
    
    # Generate rationale
    rationale = _generate_rationale(grade, profile, courses, extracurriculars)
    
    return YearlyPlan(
        grade=grade,
        courses=courses,
        extracurriculars=extracurriculars,
        competitions=competitions,
        internships=internships,
        test_prep=test_prep,
        goals=goals,
        rationale=rationale
    )


def _recommend_courses(
    grade: Grade,
    profile: StudentProfile,
    similar_profiles: list[SimilarProfile]
) -> list[str]:
    """Recommend courses based on grade, profile, and similar students."""
    courses = []
    
    # Base courses for each grade
    base_courses = {
        Grade.FRESHMAN: ["Algebra I/II", "Biology", "English 9", "World History"],
        Grade.SOPHOMORE: ["Geometry", "Chemistry", "English 10", "US History"],
        Grade.JUNIOR: ["Pre-Calculus", "Physics", "English 11", "AP US History"],
        Grade.SENIOR: ["Calculus", "Advanced Science", "English 12", "AP Government"]
    }
    
    courses.extend(base_courses.get(grade, []))
    
    # Add courses based on interests and majors
    if "Computer Science" in profile.interests or "Computer Science" in profile.target_majors:
        if grade.value >= 10:
            courses.append("AP Computer Science A")
        if grade.value >= 11:
            courses.append("AP Computer Science Principles")
    
    if "Mathematics" in profile.interests or "Engineering" in profile.target_majors:
        if grade.value >= 11:
            courses.append("AP Calculus AB")
        if grade.value >= 12:
            courses.append("AP Calculus BC")
    
    # Science courses - check for Biology, Chemistry, Medicine, or Science interests
    has_biology_interest = any("biology" in i.lower() or "medicine" in i.lower() or "pre-med" in i.lower() 
                               for i in profile.interests + profile.target_majors)
    has_chemistry_interest = any("chemistry" in i.lower() for i in profile.interests + profile.target_majors)
    has_science_interest = any("science" in i.lower() for i in profile.interests + profile.target_majors)
    
    if has_biology_interest or has_chemistry_interest or has_science_interest:
        if grade.value >= 11:
            if has_biology_interest:
                courses.append("AP Biology")
            elif has_chemistry_interest:
                courses.append("AP Chemistry")
            else:
                courses.append("AP Biology")  # Default science AP
    
    # Add courses from similar profiles
    for similar in similar_profiles[:2]:  # Top 2 similar profiles
        if similar.profile.current_grade.value >= grade.value:
            # Extract relevant courses (simplified)
            if grade == Grade.JUNIOR:
                courses.append("AP Statistics")
    
    return list(set(courses))  # Remove duplicates


def _recommend_extracurriculars(
    grade: Grade,
    profile: StudentProfile,
    similar_profiles: list[SimilarProfile],
    opportunities: list[Opportunity]
) -> list[str]:
    """Recommend extracurricular activities."""
    ecs = []
    
    # Continue existing ECs
    for ec in profile.extracurriculars:
        ecs.append(f"Continue: {ec}")
    
    # Add ECs based on interests
    if "Computer Science" in profile.interests:
        ecs.append("Coding Club")
        ecs.append("Hackathons")
    
    if "Mathematics" in profile.interests:
        ecs.append("Math Team")
        ecs.append("Math Olympiad")
    
    if "Science" in profile.interests:
        ecs.append("Science Club")
        ecs.append("Science Fair")
    
    # Add leadership opportunities for upperclassmen
    if grade.value >= 11:
        ecs.append("Student Government or Club Leadership")
    
    # Add relevant opportunities
    for opp in opportunities:
        if opp.type == "extracurricular" and grade in opp.grade_levels:
            ecs.append(opp.name)
    
    return list(set(ecs))


def _recommend_competitions(
    grade: Grade,
    profile: StudentProfile,
    opportunities: list[Opportunity]
) -> list[str]:
    """Recommend competitions."""
    competitions = []
    
    for opp in opportunities:
        if opp.type == "competition" and grade in opp.grade_levels:
            # Check if it aligns with interests
            for interest in profile.interests:
                if interest.lower() in opp.name.lower() or interest.lower() in opp.description.lower():
                    competitions.append(opp.name)
                    break
    
    return competitions


def _recommend_internships(
    grade: Grade,
    profile: StudentProfile,
    opportunities: list[Opportunity]
) -> list[str]:
    """Recommend internships."""
    internships = []
    
    # Internships typically for juniors and seniors
    if grade.value >= 11:
        for opp in opportunities:
            if opp.type == "internship" and grade in opp.grade_levels:
                internships.append(opp.name)
    
    return internships


def _recommend_test_prep(grade: Grade, profile: StudentProfile) -> list[str]:
    """Recommend test preparation activities."""
    test_prep = []
    
    if grade == Grade.JUNIOR:
        test_prep.append("PSAT preparation")
        test_prep.append("SAT/ACT prep course")
        test_prep.append("Take practice tests")
    
    if grade == Grade.SENIOR:
        test_prep.append("Final SAT/ACT preparation")
        test_prep.append("Subject Test preparation (if needed)")
    
    return test_prep


def _set_goals(grade: Grade, profile: StudentProfile) -> list[str]:
    """Set goals for the year."""
    goals = []
    
    if grade == Grade.FRESHMAN:
        goals.append("Maintain strong GPA (3.7+)")
        goals.append("Explore interests and join clubs")
        goals.append("Build foundation in core subjects")
    
    elif grade == Grade.SOPHOMORE:
        goals.append("Maintain or improve GPA")
        goals.append("Take on leadership roles in clubs")
        goals.append("Start building academic profile")
    
    elif grade == Grade.JUNIOR:
        goals.append("Achieve high GPA (3.8+)")
        goals.append("Take challenging AP courses")
        goals.append("Score well on PSAT/SAT/ACT")
        goals.append("Pursue leadership positions")
    
    elif grade == Grade.SENIOR:
        goals.append("Maintain excellent GPA")
        goals.append("Complete college applications")
        goals.append("Finalize test scores")
        goals.append("Secure strong recommendations")
    
    # Add major-specific goals
    if profile.target_majors:
        goals.append(f"Demonstrate commitment to {profile.target_majors[0]}")
    
    return goals


def _generate_rationale(
    grade: Grade,
    profile: StudentProfile,
    courses: list[str],
    extracurriculars: list[str]
) -> str:
    """Generate rationale for the year's plan."""
    rationale = f"This {grade.name.lower()} year plan focuses on "
    
    if grade == Grade.FRESHMAN:
        rationale += "building a strong academic foundation and exploring interests."
    elif grade == Grade.SOPHOMORE:
        rationale += "deepening engagement in areas of interest and taking on more responsibility."
    elif grade == Grade.JUNIOR:
        rationale += "academic excellence, test preparation, and demonstrating leadership."
    elif grade == Grade.SENIOR:
        rationale += "maintaining excellence while completing college applications."
    
    rationale += f" The course selection aligns with your interests in {', '.join(profile.interests[:2])} "
    rationale += f"and your target majors: {', '.join(profile.target_majors[:2])}."
    
    return rationale


def _generate_overall_strategy(
    profile: StudentProfile,
    similar_profiles: list[SimilarProfile]
) -> str:
    """Generate overall strategy for the 4-year plan."""
    strategy = f"Based on your profile and similar successful students, your 4-year strategy should focus on:\n\n"
    
    strategy += f"1. **Academic Excellence**: Maintain a strong GPA while taking challenging courses "
    strategy += f"aligned with your interests in {', '.join(profile.interests[:3])}.\n\n"
    
    strategy += f"2. **Depth in Interests**: Develop deep expertise in {profile.target_majors[0] if profile.target_majors else 'your chosen field'} "
    strategy += "through advanced courses, competitions, and projects.\n\n"
    
    strategy += "3. **Leadership & Impact**: Take on leadership roles in extracurriculars and demonstrate "
    strategy += "initiative through independent projects or research.\n\n"
    
    strategy += "4. **Test Preparation**: Prepare strategically for standardized tests, focusing on "
    strategy += "junior year for optimal timing.\n\n"
    
    if similar_profiles:
        strategy += f"5. **Learn from Success**: Similar students who got into {similar_profiles[0].colleges_admitted[0] if similar_profiles[0].colleges_admitted else 'top colleges'} "
        strategy += "followed similar paths, emphasizing both academic rigor and meaningful extracurricular engagement."
    
    return strategy


def _identify_milestones(
    profile: StudentProfile,
    freshman: YearlyPlan,
    sophomore: YearlyPlan,
    junior: YearlyPlan,
    senior: YearlyPlan
) -> list[str]:
    """Identify key milestones across the 4 years."""
    milestones = []
    
    milestones.append("Freshman: Establish strong academic foundation")
    milestones.append("Sophomore: Begin taking advanced courses")
    milestones.append("Junior: Take PSAT, begin SAT/ACT prep, pursue leadership")
    milestones.append("Senior: Complete college applications, finalize test scores")
    
    if profile.target_majors:
        milestones.append(f"Throughout: Build portfolio in {profile.target_majors[0]}")
    
    return milestones

