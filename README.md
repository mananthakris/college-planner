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

### Prerequisites

- **Python 3.10 or higher** (required for Google ADK)
- pip (Python package manager)
- Google account (for API key)

**Check your Python version:**
```bash
python3 --version
# If it shows 3.9 or lower, you need Python 3.10+
```

**If you need Python 3.10+:**
- **macOS (Homebrew)**: `brew install python@3.12`
- **macOS (without Homebrew)**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3.10` or `sudo yum install python3.10`

### Installation

#### 1. Create a Virtual Environment with Python 3.10+

**Option A: If you have Python 3.10+ installed:**

```bash
# Navigate to project directory
cd college-planner

# Check available Python versions
which python3.12 python3.11 python3.10  # Find the highest available

# Create virtual environment with specific Python version
# Use the highest version you have (3.12, 3.11, or 3.10)
python3.12 -m venv venv  # or python3.11 or python3.10

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Verify Python version in venv
python --version  # Should show 3.10, 3.11, or 3.12

# Your terminal prompt should now show (venv)
```

**Option B: If default python3 is 3.9 or lower:**

```bash
# Find Python 3.10+ on your system
which python3.12 python3.11 python3.10

# Use the specific version to create venv
/opt/homebrew/bin/python3.12 -m venv venv  # Adjust path as needed

# Or if installed via Homebrew:
python3.12 -m venv venv

# Activate
source venv/bin/activate

# Verify
python --version
```

#### 2. Install Dependencies

```bash
# Make sure virtual environment is activated (you should see (venv))
# Upgrade pip first
pip install --upgrade pip

# Install all requirements including Google ADK
pip install -r requirements.txt
```

This installs:
- `google-adk` (Agent Development Kit)
- `google-generativeai` (for Gemini API)
- Other dependencies

#### 3. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey) or [AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)

#### 4. Set Up Environment Variables

**Option A: Environment Variable (Recommended)**

```bash
# Add to your shell profile (~/.zshrc or ~/.bashrc)
echo 'export GOOGLE_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc

# Or set temporarily for current session
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: .env File**

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit .env and add your Google API key
nano .env  # or use your preferred editor

# Add this line:
GOOGLE_API_KEY=your-api-key-here
```

**Note**: If using `.env` file, you may need to install `python-dotenv`:
```bash
pip install python-dotenv
```

#### 5. Verify Setup

```bash
# Test ADK installation
python3 -c "from google.adk.agents import Agent; print('✓ ADK installed')"

# Test API key
python3 -c "
import os
key = os.getenv('GOOGLE_API_KEY')
if key:
    print(f'✓ API key found: {key[:10]}...')
else:
    print('⚠ API key not found. Set GOOGLE_API_KEY environment variable.')
"
```

### Quick Test: Run Pipeline with Example Profiles

Test the system with sample profiles:

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Test with Engineering profile
python3 -c "
from src import run_pipeline

result = run_pipeline({
    'name': 'Alex',
    'current_grade': 9,
    'interests': ['Engineering', 'Mathematics', 'Robotics'],
    'target_colleges': ['MIT', 'Stanford'],
    'target_majors': ['Engineering']
}, max_iterations=2)

print(f'Score: {result[\"final_score\"]:.1%}')
print(f'Plan created: {len(result[\"plan\"].freshman_plan.courses)} courses in freshman year')
"

# Test with Pre-Med profile
python3 -c "
from src import run_pipeline

result = run_pipeline({
    'name': 'Sarah',
    'current_grade': 9,
    'interests': ['Biology', 'Medicine'],
    'target_colleges': ['Johns Hopkins', 'Harvard'],
    'target_majors': ['Biology', 'Pre-Med']
}, max_iterations=2)

print(f'Score: {result[\"final_score\"]:.1%}')
print(f'Plan created: {len(result[\"plan\"].freshman_plan.courses)} courses in freshman year')
"
```

Or use the example scripts:

```bash
# Quick comparison test
python3 test_simple.py  # Engineering vs Pre-Med comparison

# Test natural language parsing
python3 test_natural_language.py

# Full example with detailed output
python3 main.py
```

### Running Tests

Run the automated test suite:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Or run individual test files
python3 tests/test_profile_agent.py
python3 tests/test_database.py
python3 tests/test_agent_tools.py
python3 tests/test_retrieval_agent.py
python3 tests/test_pipeline.py

# Or use the test runner
python3 tests/run_all_tests.py
```

**Test Coverage:**
- ✅ Profile Agent (normalization, natural language parsing)
- ✅ Database (search, queries)
- ✅ Agent Tools (all 6 database tools)
- ✅ Retrieval Agent (ADK agent creation, retrieval)
- ✅ Full Pipeline (end-to-end testing)

### Basic Usage

**Using Structured Input:**

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

**Using Natural Language (with ADK):**

```python
from src.agents.profile_agent import parse_natural_language
from src.agents.retrieval_agent import run_retrieval

# Parse natural language input
text = "I'm a freshman interested in computer science and math. I want to go to MIT or Stanford."
profile = parse_natural_language(text)

# Use with retrieval agent (uses ADK with database tools)
retrieval = run_retrieval(profile)
print(f"Found {len(retrieval['similar_profiles'])} similar profiles")
```

Results are saved to `output/college_plan.json`.

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
│       ├── database.py         # Database interface
│       ├── agent_tools.py      # Database tools for agents
│       └── evaluation.py      # Plan evaluation metrics
├── tests/                      # Automated test suite
│   ├── test_profile_agent.py
│   ├── test_database.py
│   ├── test_agent_tools.py
│   ├── test_retrieval_agent.py
│   ├── test_pipeline.py
│   └── run_all_tests.py
├── scripts/                    # Utility scripts
│   ├── collect_profiles.py
│   ├── reddit_collector.py
│   └── enrich_profiles.py
├── data/                       # Data files
│   └── student_profiles.json
├── main.py                     # Entry point with example
├── test_simple.py              # Quick comparison test
├── test_natural_language.py   # Natural language test
├── requirements.txt            # Dependencies
└── README.md                   # This file
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

## 📊 Data Collection

To populate the database with real student profiles, see [DATA_SOURCES.md](DATA_SOURCES.md) for:
- Legitimate sources for student profiles
- Privacy and ethics guidelines
- Data collection best practices
- Tools and scripts for collecting profiles

### Collection Scripts

```bash
# Interactive profile collection
python3 scripts/collect_profiles.py

# Parse Reddit posts (r/collegeresults)
python3 scripts/reddit_collector.py

# Enrich and validate profiles
python3 scripts/enrich_profiles.py
```

## 🚀 Next Steps

For integrating more agents and real data, see [NEXT_STEPS.md](NEXT_STEPS.md) for:
- Converting remaining agents to ADK
- Multi-agent orchestration
- Real anonymized data integration
- Enhanced features (vector search, tools, etc.)

## 🔧 Troubleshooting

### Common Issues

**"google-adk not found" or "Python version too old"**
```bash
# Make sure venv is activated
source venv/bin/activate

# Check Python version (must be 3.10+)
python --version

# If it's 3.9 or lower, recreate venv with Python 3.10+
deactivate
rm -rf venv
python3.12 -m venv venv  # Use your Python 3.10+ version
source venv/bin/activate
python --version  # Verify

# Then install ADK
pip install google-adk

# Verify installation
python3 -c "from google.adk.agents import Agent; print('✓ ADK installed')"
```

**"API key not found"**
```bash
# Check if it's set
echo $GOOGLE_API_KEY

# If empty, set it:
export GOOGLE_API_KEY="your-key-here"

# Or use .env file
cp .env.sample .env
# Then edit .env and add: GOOGLE_API_KEY=your-key-here
```

**"Module not found" errors**
```bash
# Make sure you're in the project directory
pwd  # Should show: .../college-planner

# Make sure venv is activated
which python  # Should show: .../venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

**Virtual environment not activating**
```bash
# On macOS/Linux, make sure you use:
source venv/bin/activate

# On Windows, use:
venv\Scripts\activate

# If that doesn't work, recreate the venv:
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

For more detailed setup instructions, see [SETUP.md](SETUP.md).

## 🔮 Future Enhancements

- **LLM Integration**: Enhanced planning and critique with advanced models
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
