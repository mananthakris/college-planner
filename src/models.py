"""
Data models for the college planner system.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class Grade(Enum):
    """High school grade levels."""
    FRESHMAN = 9
    SOPHOMORE = 10
    JUNIOR = 11
    SENIOR = 12


@dataclass
class StudentProfile:
    """Normalized student profile."""
    name: str
    current_grade: Grade
    interests: List[str]
    academic_strengths: List[str]
    courses_taken: List[str]
    courses_planned: List[str]
    extracurriculars: List[str]
    achievements: List[str]
    target_colleges: List[str]
    target_majors: List[str]
    gpa: Optional[float] = None
    test_scores: Dict[str, float] = field(default_factory=dict)
    additional_info: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SimilarProfile:
    """Profile of a similar successful student."""
    profile: StudentProfile
    similarity_score: float
    colleges_admitted: List[str]
    final_major: Optional[str] = None


@dataclass
class Opportunity:
    """Academic or extracurricular opportunity."""
    name: str
    type: str  # "academic", "extracurricular", "competition", "internship", etc.
    grade_levels: List[Grade]
    description: str
    requirements: List[str]
    benefits: List[str]
    deadline: Optional[str] = None


@dataclass
class YearlyPlan:
    """Plan for a specific grade year."""
    grade: Grade
    courses: List[str]
    extracurriculars: List[str]
    competitions: List[str]
    internships: List[str]
    test_prep: List[str]
    goals: List[str]
    rationale: str


@dataclass
class FourYearPlan:
    """Complete 4-year roadmap."""
    student_profile: StudentProfile
    freshman_plan: YearlyPlan
    sophomore_plan: YearlyPlan
    junior_plan: YearlyPlan
    senior_plan: YearlyPlan
    overall_strategy: str
    key_milestones: List[str]


@dataclass
class Critique:
    """Critique of a plan."""
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    score: float  # 0-1
    needs_revision: bool


@dataclass
class Explanation:
    """Final explanation for the user."""
    summary: str
    plan_overview: str
    year_by_year: Dict[str, str]
    key_recommendations: List[str]
    next_steps: List[str]

