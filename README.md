# College Planner - Multi-Agent System

A sophisticated multi-agent system that helps high school students create personalized 4-year roadmaps for college admissions. The system analyzes student profiles, finds similar successful students, and generates actionable plans to strengthen college applications.

## 🎯 Overview

This system uses a multi-agent architecture where specialized agents work together to:
1. **Profile Agent**: Normalizes and processes student input (interests, courses, ECs, etc.)
2. **Retrieval Agent**: Finds similar successful student profiles and relevant opportunities
3. **Planner Agent**: Creates a comprehensive 4-year roadmap
4. **Critic Agent**: Evaluates and critiques plans (acts as a loop agent for refinement)
5. **Explainer Agent**: Generates user-friendly final output

## 🏗️ Architecture

```
Student Input
    ↓
Profile Agent (Normalize)
    ↓
Retrieval Agent (Find Similar Profiles & Opportunities)
    ↓
Planner Agent (Create 4-Year Plan)
    ↓
Critic Agent (Evaluate & Critique) ←──┐
    ↓                                  │
    └─── Loop until quality threshold ─┘
    ↓
Explainer Agent (Generate Final Output)
    ↓
User-Friendly Plan
```

## 📋 Features

- **Personalized Planning**: Creates customized 4-year roadmaps based on student interests and goals
- **Similarity Matching**: Finds and learns from profiles of successful students
- **Iterative Refinement**: Critic agent loops to improve plan quality
- **Comprehensive Evaluation**: Scores plans across multiple dimensions
- **Actionable Recommendations**: Provides specific next steps and improvements

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd college-planner

# Install dependencies (if needed)
pip install -r requirements.txt
```

### Basic Usage

```python
from src import run_pipeline

# Student profile input
profile_input = {
    "name": "Alex Johnson",
    "current_grade": 9,
    "interests": ["Computer Science", "Mathematics", "Robotics"],
    "academic_strengths": ["Math", "Science"],
    "courses_taken": [],
    "extracurriculars": ["Robotics Club"],
    "target_colleges": ["MIT", "Stanford", "UC Berkeley"],
    "target_majors": ["Computer Science", "Engineering"]
}

# Run the pipeline
result = run_pipeline(profile_input, max_iterations=3, min_score_threshold=0.7)

# Access results
print(result["explanation"].summary)
print(result["explanation"].plan_overview)
```

### Running the Example

```bash
python main.py
```

This will run a complete example and save results to `output/college_plan.json`.

## 📁 Project Structure

```
college-planner/
├── src/
│   ├── __init__.py
│   ├── models.py              # Data models (StudentProfile, FourYearPlan, etc.)
│   ├── orchestrator.py        # Main pipeline coordinator
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── profile_agent.py   # Normalizes student input
│   │   ├── retrieval_agent.py # Finds similar profiles
│   │   ├── planner_agent.py   # Creates 4-year plans
│   │   ├── critic_agent.py    # Evaluates plans (loop agent)
│   │   └── explainer_agent.py # Generates final output
│   └── tools/
│       ├── __init__.py
│       ├── data_loader.py     # Loads profiles and opportunities
│       └── evaluation.py     # Plan evaluation metrics
├── main.py                    # Entry point with example
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🔧 Configuration

### Pipeline Parameters

- `max_iterations` (default: 3): Maximum number of critique-plan refinement loops
- `min_score_threshold` (default: 0.7): Minimum quality score to accept (0-1)

### Data Files

The system looks for data files in the `data/` directory:
- `data/student_profiles.json`: Historical successful student profiles
- `data/opportunities.json`: Available opportunities (competitions, programs, etc.)

If these files don't exist, the system uses sample data for development.

## 📊 Output Format

The pipeline returns a dictionary with:

- `profile`: Normalized StudentProfile object
- `plan`: FourYearPlan with detailed yearly breakdowns
- `critique`: Critique with strengths, weaknesses, and suggestions
- `explanation`: User-friendly Explanation with summary, recommendations, and next steps
- `iterations`: Number of refinement iterations performed
- `final_score`: Final quality score (0-1)

## 🎓 How It Works

### 1. Profile Normalization
The Profile Agent takes raw student input and normalizes it into a structured `StudentProfile` with:
- Interests and academic strengths
- Current courses and extracurriculars
- Target colleges and majors
- Test scores and GPA (optional)

### 2. Similarity Retrieval
The Retrieval Agent:
- Loads historical successful student profiles
- Calculates similarity based on interests, majors, and strengths
- Finds relevant opportunities matching the student's grade and interests

### 3. Plan Generation
The Planner Agent creates a 4-year plan with:
- **Courses**: Recommended courses for each year, aligned with interests
- **Extracurriculars**: Activities and clubs
- **Competitions**: Relevant competitions and contests
- **Internships**: Summer programs and internships
- **Test Prep**: SAT/ACT preparation timeline
- **Goals**: Year-specific objectives

### 4. Critique & Refinement Loop
The Critic Agent evaluates plans on:
- Course rigor and progression
- Alignment with interests and majors
- Extracurricular depth and leadership
- Test preparation strategy

If the score is below threshold or critical weaknesses are found, the plan is refined and re-evaluated.

### 5. Final Explanation
The Explainer Agent generates:
- Executive summary
- Plan overview and strategy
- Year-by-year detailed breakdown
- Key recommendations
- Immediate next steps

## 🔮 Future Enhancements

- **LLM Integration**: Use OpenAI/Anthropic for more sophisticated planning and critique
- **Vector Search**: Enhanced similarity matching using embeddings
- **Real Data**: Integration with actual student profile databases
- **Web Interface**: User-friendly web application
- **Progress Tracking**: Track student progress against the plan
- **College-Specific Requirements**: Detailed requirements for specific colleges

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Enhanced similarity algorithms
- More sophisticated plan refinement
- Additional evaluation metrics
- Better data loading and management
- Integration with external APIs

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

Built to make expert college counseling affordable and accessible to all students.
