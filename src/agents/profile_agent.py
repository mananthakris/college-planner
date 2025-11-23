"""
Profile Agent: Normalizes and processes student input.
Uses Google ADK Agent class for proper integration.
"""
from typing import Dict, Any, Optional
import json
from ..models import StudentProfile, Grade
from ..config import get_gemini_model


def _create_profile_agent():
    """
    Create a Google ADK Agent for profile processing.
    
    Returns:
        ADK Agent instance configured for profile normalization
    """
    try:
        from google.adk.agents import Agent
        
        agent = Agent(
            name="profile_agent",
            model=get_gemini_model(),
            description="Normalizes student input and parses natural language descriptions into structured profiles",
            instruction="""You are a profile normalization agent. Your task is to extract structured student information 
            from natural language input or dictionaries. You should:
            1. Parse natural language descriptions of students
            2. Extract: name, grade, interests, academic strengths, courses, extracurriculars, achievements, target colleges, target majors, GPA, test scores
            3. Normalize the data into a consistent format
            4. Return structured JSON with all extracted information
            
            Always be thorough and extract as much information as possible from the input.""",
            tools=[]  # Can add tools later if needed
        )
        return agent
    except ImportError:
        print("Warning: google-adk not installed. Using fallback implementation.")
        return None


def normalize(profile_input: Dict[str, Any]) -> StudentProfile:
    """
    Normalize raw student input into a structured StudentProfile.
    
    Args:
        profile_input: Raw dictionary with student information
        
    Returns:
        Normalized StudentProfile object
    """
    # Extract and normalize grade
    current_grade = _normalize_grade(profile_input.get("current_grade", 9))
    
    # Extract lists, ensuring they're lists
    interests = _ensure_list(profile_input.get("interests", []))
    academic_strengths = _ensure_list(profile_input.get("academic_strengths", []))
    courses_taken = _ensure_list(profile_input.get("courses_taken", []))
    courses_planned = _ensure_list(profile_input.get("courses_planned", []))
    extracurriculars = _ensure_list(profile_input.get("extracurriculars", []))
    achievements = _ensure_list(profile_input.get("achievements", []))
    target_colleges = _ensure_list(profile_input.get("target_colleges", []))
    target_majors = _ensure_list(profile_input.get("target_majors", []))
    
    # Extract optional fields
    gpa = profile_input.get("gpa")
    test_scores = profile_input.get("test_scores", {})
    name = profile_input.get("name", "Student")
    additional_info = profile_input.get("additional_info", {})
    
    return StudentProfile(
        name=name,
        current_grade=current_grade,
        interests=interests,
        academic_strengths=academic_strengths,
        courses_taken=courses_taken,
        courses_planned=courses_planned,
        extracurriculars=extracurriculars,
        achievements=achievements,
        target_colleges=target_colleges,
        target_majors=target_majors,
        gpa=gpa,
        test_scores=test_scores,
        additional_info=additional_info
    )


def parse_natural_language(natural_language_input: str) -> StudentProfile:
    """
    Parse natural language input into a structured StudentProfile using ADK Agent.
    
    Args:
        natural_language_input: Free-form text describing the student
        
    Returns:
        Normalized StudentProfile object
        
    Example:
        input_text = "I'm a freshman interested in computer science and math. 
                     I want to go to MIT or Stanford. I'm in robotics club."
        profile = parse_natural_language(input_text)
    """
    # Try using ADK Agent
    agent = _create_profile_agent()
    
    if agent:
        try:
            # Use ADK Agent to parse
            prompt = f"""Extract student information from the following natural language description and return it as a JSON object.

Student description:
{natural_language_input}

Extract the following information and return ONLY valid JSON (no markdown, no code blocks):
{{
    "name": "student name or 'Student' if not mentioned",
    "current_grade": number (9, 10, 11, or 12) or null,
    "interests": ["list", "of", "interests"],
    "academic_strengths": ["list", "of", "strengths"],
    "courses_taken": ["list", "of", "courses"],
    "courses_planned": ["list", "of", "planned", "courses"],
    "extracurriculars": ["list", "of", "extracurriculars"],
    "achievements": ["list", "of", "achievements"],
    "target_colleges": ["list", "of", "colleges"],
    "target_majors": ["list", "of", "majors"],
    "gpa": number or null,
    "test_scores": {{"SAT": number, "ACT": number}} or {{}}
}}

Return only the JSON object, nothing else."""

            # Run the ADK agent
            response = agent.run(prompt)
            
            # Extract JSON from response
            response_text = str(response).strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            profile_dict = json.loads(response_text)
            
            # Normalize the extracted data
            return normalize(profile_dict)
            
        except Exception as e:
            print(f"Warning: ADK Agent error ({e}). Falling back to rule-based parsing.")
    
    # Fallback to rule-based parsing
    return _fallback_natural_language_parse(natural_language_input)


def _fallback_natural_language_parse(text: str) -> StudentProfile:
    """
    Fallback rule-based parser for natural language when ADK/Gemini unavailable.
    """
    text_lower = text.lower()
    
    # Extract grade
    grade = 9  # default
    if "freshman" in text_lower or "9th" in text_lower:
        grade = 9
    elif "sophomore" in text_lower or "10th" in text_lower:
        grade = 10
    elif "junior" in text_lower or "11th" in text_lower:
        grade = 11
    elif "senior" in text_lower or "12th" in text_lower:
        grade = 12
    
    # Extract interests (simple keyword matching)
    interests = []
    interest_keywords = {
        "computer science": "Computer Science",
        "cs": "Computer Science",
        "engineering": "Engineering",
        "math": "Mathematics",
        "mathematics": "Mathematics",
        "biology": "Biology",
        "chemistry": "Chemistry",
        "physics": "Physics",
        "medicine": "Medicine",
        "pre-med": "Pre-Med",
        "robotics": "Robotics"
    }
    
    for keyword, interest in interest_keywords.items():
        if keyword in text_lower:
            interests.append(interest)
    
    # Extract colleges (common names)
    target_colleges = []
    college_keywords = {
        "mit": "MIT",
        "stanford": "Stanford",
        "harvard": "Harvard",
        "yale": "Yale",
        "princeton": "Princeton",
        "caltech": "Caltech",
        "berkeley": "UC Berkeley",
        "uc berkeley": "UC Berkeley"
    }
    
    for keyword, college in college_keywords.items():
        if keyword in text_lower:
            target_colleges.append(college)
    
    # Extract majors
    target_majors = []
    if "engineering" in text_lower:
        target_majors.append("Engineering")
    if "computer science" in text_lower or "cs" in text_lower:
        target_majors.append("Computer Science")
    if "biology" in text_lower or "pre-med" in text_lower:
        target_majors.append("Biology")
    
    # Extract extracurriculars
    extracurriculars = []
    if "robotics" in text_lower:
        extracurriculars.append("Robotics Club")
    if "volunteer" in text_lower:
        extracurriculars.append("Volunteering")
    
    profile_dict = {
        "name": "Student",
        "current_grade": grade,
        "interests": interests,
        "academic_strengths": [],
        "courses_taken": [],
        "courses_planned": [],
        "extracurriculars": extracurriculars,
        "achievements": [],
        "target_colleges": target_colleges,
        "target_majors": target_majors,
        "gpa": None,
        "test_scores": {}
    }
    
    return normalize(profile_dict)


def _normalize_grade(grade_input: Any) -> Grade:
    """Convert various grade inputs to Grade enum."""
    if isinstance(grade_input, Grade):
        return grade_input
    
    if isinstance(grade_input, int):
        return Grade(grade_input)
    
    if isinstance(grade_input, str):
        grade_lower = grade_input.lower()
        if "freshman" in grade_lower or "9" in grade_lower:
            return Grade.FRESHMAN
        elif "sophomore" in grade_lower or "10" in grade_lower:
            return Grade.SOPHOMORE
        elif "junior" in grade_lower or "11" in grade_lower:
            return Grade.JUNIOR
        elif "senior" in grade_lower or "12" in grade_lower:
            return Grade.SENIOR
    
    return Grade.FRESHMAN  # Default


def _ensure_list(value: Any) -> list:
    """Ensure value is a list."""
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        # Split by comma if it's a string
        return [item.strip() for item in value.split(",") if item.strip()]
    return [value]


# ADK Agent instance (lazy initialization)
_profile_agent_instance = None

def get_profile_agent():
    """Get or create the ADK profile agent instance."""
    global _profile_agent_instance
    if _profile_agent_instance is None:
        _profile_agent_instance = _create_profile_agent()
    return _profile_agent_instance
