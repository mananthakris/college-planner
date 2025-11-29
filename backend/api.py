"""
FastAPI backend for College Planner web interface.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Add parent directory to path to import src
# This allows the backend to import from the main project
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from src import run_pipeline
except ImportError as e:
    raise ImportError(
        f"Failed to import main project modules. Make sure:\n"
        f"1. Virtual environment is activated: source venv/bin/activate\n"
        f"2. Main project dependencies are installed: pip install -r requirements.txt\n"
        f"3. Backend dependencies are installed: pip install -r backend/requirements.txt\n"
        f"Original error: {e}"
    )

app = FastAPI(title="College Planner API")

# CORS middleware to allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StudentProfileInput(BaseModel):
    name: str
    current_grade: int
    interests: List[str]
    academic_strengths: List[str]
    courses_taken: List[str]
    courses_planned: List[str]
    extracurriculars: List[str]
    achievements: List[str]
    target_colleges: List[str]
    target_majors: List[str]
    gpa: Optional[float] = None
    test_scores: Dict[str, float] = {}


@app.get("/")
def read_root():
    return {"message": "College Planner API is running"}


@app.post("/api/plan")
async def create_plan(profile: StudentProfileInput):
    """
    Create a 4-year college plan for a student.
    """
    try:
        # Convert Pydantic model to dict
        profile_dict = profile.model_dump()
        
        # Run the pipeline
        result = run_pipeline(
            profile_dict,
            max_iterations=3,
            min_score_threshold=0.7
        )
        
        # Convert result to JSON-serializable format
        response = {
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
            "iterations": result["iterations"],
            "freshman_plan": {
                "courses": result["plan"].freshman_plan.courses,
                "extracurriculars": result["plan"].freshman_plan.extracurriculars,
                "competitions": result["plan"].freshman_plan.competitions,
                "internships": result["plan"].freshman_plan.internships,
                "test_prep": result["plan"].freshman_plan.test_prep,
                "goals": result["plan"].freshman_plan.goals,
                "rationale": result["plan"].freshman_plan.rationale
            },
            "sophomore_plan": {
                "courses": result["plan"].sophomore_plan.courses,
                "extracurriculars": result["plan"].sophomore_plan.extracurriculars,
                "competitions": result["plan"].sophomore_plan.competitions,
                "internships": result["plan"].sophomore_plan.internships,
                "test_prep": result["plan"].sophomore_plan.test_prep,
                "goals": result["plan"].sophomore_plan.goals,
                "rationale": result["plan"].sophomore_plan.rationale
            },
            "junior_plan": {
                "courses": result["plan"].junior_plan.courses,
                "extracurriculars": result["plan"].junior_plan.extracurriculars,
                "competitions": result["plan"].junior_plan.competitions,
                "internships": result["plan"].junior_plan.internships,
                "test_prep": result["plan"].junior_plan.test_prep,
                "goals": result["plan"].junior_plan.goals,
                "rationale": result["plan"].junior_plan.rationale
            },
            "senior_plan": {
                "courses": result["plan"].senior_plan.courses,
                "extracurriculars": result["plan"].senior_plan.extracurriculars,
                "competitions": result["plan"].senior_plan.competitions,
                "internships": result["plan"].senior_plan.internships,
                "test_prep": result["plan"].senior_plan.test_prep,
                "goals": result["plan"].senior_plan.goals,
                "rationale": result["plan"].senior_plan.rationale
            }
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

