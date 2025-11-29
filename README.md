# College Planner - Multi-Agent System

A sophisticated multi-agent system that helps high school students create personalized 4-year roadmaps for college admissions. The system analyzes student profiles, finds similar successful students, and generates actionable plans to strengthen college applications.

**Available as both a command-line tool and a modern web interface!**

## 🎯 Overview

This system uses a sophisticated multi-agent architecture powered by **Google ADK (Agent Development Kit)** where specialized AI agents work together with database tools to create personalized college preparation plans:

1. **Profile Agent**: Normalizes and processes student input (natural language or structured data)
2. **Retrieval Agent**: Finds similar successful student profiles and relevant opportunities (6 database tools)
3. **Planner Agent**: Creates comprehensive 4-year roadmaps with dynamic queries (4 database tools)
4. **Critic Agent**: Evaluates and critiques plans with data-driven benchmarks (4 database tools)
5. **Explainer Agent**: Generates user-friendly explanations with concrete examples (3 database tools)

All agents use Google's Gemini models through ADK with **17 tool instances** enabling dynamic database queries. Plans achieve **80-90% quality scores** consistently with 2-3 iterations of refinement.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Student Profile Input                        │
│  {name, grade, interests, courses, ECs, target colleges, etc.} │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Profile Agent  │
                    │   (Normalize)   │
                    │  Uses ADK       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Retrieval Agent │
                    │  (Find Similar  │
                    │   Profiles &    │
                    │  Opportunities) │
                    │  6 DB Tools     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Planner Agent  │
                    │ (Create 4-Year  │
                    │      Plan)      │
                    │  4 DB Tools     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Critic Agent   │
                    │   (Evaluate)    │
                    │  4 DB Tools     │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────▼─────┐    ┌──────▼──────┐
              │ Score >=  │    │ Score <     │
              │ Threshold │    │ Threshold   │
              │ & No      │    │ OR Critical │
              │ Critical  │    │ Weaknesses  │
              │ Issues?   │    │ Found?      │
              └─────┬─────┘    └──────┬──────┘
                    │                 │
                    │                 │
                    │    ┌────────────┘
                    │    │ Refine Plan
                    │    │ (Loop)
                    │    └──┐
                    │       │
                    └───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Explainer    │
                    │    Agent      │
                    │ (Generate     │
                    │ Final Output) │
                    │  3 DB Tools   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ User-Friendly │
                    │ 4-Year Plan   │
                    └───────────────┘
```

### How It Works

1. **Profile Agent** processes raw student input and normalizes it into structured data
2. **Retrieval Agent** queries the database to find similar successful students and relevant opportunities
3. **Planner Agent** creates a detailed 4-year plan using insights from similar profiles
4. **Critic Agent** evaluates the plan, identifies weaknesses, and determines if refinement is needed
5. If the plan needs improvement, it loops back to the Planner with specific feedback
6. **Explainer Agent** generates a user-friendly explanation with recommendations and next steps

## 📋 Features

### Core Capabilities
- 🎯 **Personalized Planning**: Creates customized 4-year roadmaps based on student interests and goals
- 🤖 **AI-Powered Agents**: All 5 agents use Google ADK with Gemini models for intelligent decision-making
- 🔧 **Database Tools**: 17 tool instances enabling agents to dynamically query student profiles and opportunities
- 🔍 **Similarity Matching**: Finds and learns from profiles of successful students using weighted scoring
- 🔄 **Iterative Refinement**: Critic agent loops to improve plan quality (typically 2-3 iterations)
- 📊 **Comprehensive Evaluation**: Scores plans across multiple dimensions (rigor, alignment, progression, test prep)
- 💡 **Actionable Recommendations**: Provides specific next steps and improvements with concrete examples

### Technical Features
- 📝 **Natural Language Input**: Can parse free-form text descriptions of students
- 🗂️ **Structured Output**: Returns JSON-formatted plans with year-by-year breakdowns
- 🛡️ **Rule-Based Fallbacks**: All agents have fallback logic if ADK unavailable
- 🔕 **Clean Output**: Warning suppression for ADK function calls
- ⚡ **High Quality**: Achieves 80-90% plan quality consistently
- 🔐 **Privacy First**: Anonymized data, no PII storage
- 🌐 **Web Interface**: Modern React UI with FastAPI backend for easy interaction

## 🚀 Quick Start

You can use the College Planner in two ways:
1. **Command Line Interface** - Run `python3 main.py` or test scripts
2. **Web Interface** - Modern React UI (see [Web UI Setup](#-web-ui-react--fastapi) below)

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

## 🛠️ Agent Tools

All agents use Google ADK's `FunctionTool` to query the database dynamically during planning and evaluation:

### Available Database Tools

**Search & Retrieval:**
- `search_profiles_tool` - Search by interests (returns matching profiles)
- `search_by_major_tool` - Find students by target major
- `search_by_college_tool` - Find students targeting specific colleges
- `find_similar_profiles_tool` - Calculate similarity scores and rank matches
- `get_profile_statistics_tool` - Database statistics and benchmarks

**Opportunities:**
- `get_opportunities_tool` - Get relevant competitions, internships, programs by grade/interests

### Tool Distribution by Agent

| Agent | Tools | Purpose |
|-------|-------|---------|
| **RetrievalAgent** | 6 tools | Comprehensive search and profile matching |
| **PlannerAgent** | 4 tools | Dynamic planning with database queries |
| **CriticAgent** | 4 tools | Benchmark against successful students |
| **ExplainerAgent** | 3 tools | Provide concrete examples and context |

**Total**: 17 tool instances working together to create data-driven, personalized plans.

See [DATABASE_TOOLS_GUIDE.md](DATABASE_TOOLS_GUIDE.md) for detailed tool documentation.

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

## 🌐 Web UI (React + FastAPI)

The project includes a modern web interface for easy interaction with the College Planner system.

### Prerequisites

- **Node.js 18+** and npm (for React frontend)
- **Python 3.10+** with virtual environment
- **Google API Key** (`GOOGLE_API_KEY` environment variable)
- **All main project dependencies** installed (from Quick Start above)

### Quick Start

You'll need **two terminal windows** - one for the backend and one for the frontend.

#### Terminal 1: Backend API

```bash
# Navigate to project root
cd college-planner

# Activate virtual environment
source venv/bin/activate

# Install main project dependencies (if not already installed)
pip install -r requirements.txt

# Install backend API dependencies (first time only)
pip install -r backend/requirements.txt

# Set API key (if not already set)
export GOOGLE_API_KEY="your-api-key-here"

# Start the FastAPI server
cd backend
python api.py
```

✅ Backend will run on **http://localhost:8000**

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

#### Terminal 2: React Frontend

Open a **new terminal** and run:

```bash
# Navigate to frontend directory
cd college-planner/frontend

# Install Node.js dependencies (first time only)
npm install

# Start the development server
npm run dev
```

✅ Frontend will run on **http://localhost:3000** (or next available port)

You should see:
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:3000/
```

#### Step 3: Use the Web Interface

1. Open your browser and go to **http://localhost:3000**
2. Fill out the student profile form:
   - **Basic Info**: Name, grade, GPA
   - **Test Scores**: SAT/ACT (optional)
   - **Interests & Strengths**: Academic interests, strengths
   - **Targets**: Target majors and colleges (required)
   - **Activities**: Courses, extracurriculars, achievements
3. Click **"Generate 4-Year Plan"**
4. View your personalized plan with year-by-year breakdown, recommendations, and evaluation

### Web UI Features

- ✅ **User-Friendly Form**: All fields from `main.py` as interactive inputs
- ✅ **Tag-Based Lists**: Easy add/remove for interests, courses, extracurriculars
- ✅ **Real-Time Validation**: Required fields clearly marked
- ✅ **Beautiful Results Display**: Organized year-by-year plan view
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Error Handling**: Clear error messages with troubleshooting hints

### Troubleshooting

**Backend Issues:**

- **Port 8000 already in use**: Change port in `backend/api.py` or kill the process using it
- **Import errors**: 
  - Verify virtual environment is activated: `which python` should show `venv/bin/python`
  - Install all dependencies: `pip install -r requirements.txt && pip install -r backend/requirements.txt`
- **API key errors**: 
  - Check `GOOGLE_API_KEY` is set: `echo $GOOGLE_API_KEY`
  - Export in the same terminal: `export GOOGLE_API_KEY="your-key"`

**Frontend Issues:**

- **Node.js not found**: Install Node.js 18+: `brew install node` (macOS) or download from [nodejs.org](https://nodejs.org/)
- **npm install fails**: 
  - Clear cache: `npm cache clean --force`
  - Delete and reinstall: `rm -rf node_modules package-lock.json && npm install`
- **Port 3000 in use**: Vite will automatically use the next available port

**Connection Issues:**

- **CORS errors**: Verify backend is running on port 8000 and frontend connects to `http://localhost:8000`
- **"Failed to fetch"**: 
  - Check backend is running: `curl http://localhost:8000/`
  - Check browser console for detailed errors
- **API 500 errors**: Check backend terminal logs for detailed error messages

**For more detailed troubleshooting, see [WEB_UI_SETUP.md](WEB_UI_SETUP.md)**

### Expected Output

With all agents using ADK and database tools, you should see high-quality plans:

```
✓ Plan Quality Score: 85%
✓ Iterations: 3

📚 KEY COURSES BY YEAR:
  Freshman: 7 courses (0 AP)
  Sophomore: 7 courses (1 AP)
    AP: Honors Organic Chemistry (or AP Chemistry if available)
  Junior: 7 courses (5 AP)
    AP: AP Biology, AP Chemistry, AP English Language
  Senior: 6 courses (4 AP)
    AP: AP Physics C (if applicable), AP English Literature

🎯 KEY EXTRACURRICULARS:
  • Hospital Volunteer (seek leadership opportunities)
  • Science Club (member)
  • Research Assistant (University Lab)
  • Math Club
  • Debate Team

💡 TOP RECOMMENDATIONS:
  1. **Accelerate Math if Possible**: Consider AP Calculus BC by junior year
  2. **Integrate Computer Science**: Add AP CS A for modern research skills
  3. **Seek Research Opportunities**: Target university programs or local labs

📊 EVALUATION:
  Strengths: 9
  Weaknesses: 5
```

**Key Improvements with ADK Tools:**
- ✅ Dynamic queries during planning (not just static context)
- ✅ Data-driven critiques comparing against successful students
- ✅ Concrete examples from similar profiles in explanations
- ✅ Specific opportunities mentioned by grade level
- ✅ Better course sequences based on real successful patterns

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
├── src/                        # Python source code
│   ├── __init__.py
│   ├── models.py              # Data models (StudentProfile, FourYearPlan, etc.)
│   ├── orchestrator.py        # Main pipeline coordinator
│   ├── agents/                # AI agents
│   │   ├── __init__.py
│   │   ├── profile_agent.py   # Normalizes student input
│   │   ├── retrieval_agent.py # Finds similar profiles
│   │   ├── planner_agent.py   # Creates 4-year plans
│   │   ├── critic_agent.py    # Evaluates plans (loop agent)
│   │   └── explainer_agent.py # Generates final output
│   ├── tools/                 # Database and utility tools
│   │   ├── __init__.py
│   │   ├── data_loader.py     # Loads profiles and opportunities
│   │   ├── database.py         # Database interface
│   │   ├── agent_tools.py      # Database tools for agents
│   │   └── evaluation.py      # Plan evaluation metrics
│   └── utils/                  # Utility functions
│       └── adk_helper.py      # ADK integration helpers
├── backend/                    # FastAPI backend for web UI
│   ├── api.py                  # REST API endpoints
│   └── requirements.txt        # Backend dependencies
├── frontend/                    # React frontend for web UI
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── components/
│   │   │   ├── StudentForm.jsx # Profile input form
│   │   │   └── ResultsDisplay.jsx # Plan results display
│   │   └── index.jsx          # React entry point
│   ├── package.json           # Node.js dependencies
│   └── vite.config.js         # Vite configuration
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
├── main.py                     # CLI entry point with example
├── test_simple.py              # Quick comparison test
├── test_natural_language.py   # Natural language test
├── requirements.txt            # Python dependencies
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

The system includes real anonymized student profiles collected from public sources. To expand the database further, see [DATA_SOURCES.md](DATA_SOURCES.md) for:
- Legitimate sources for student profiles (r/collegeresults, etc.)
- Privacy and ethics guidelines (always anonymize!)
- Data collection best practices
- Tools and scripts for collecting profiles

### Collection Scripts

```bash
# Interactive profile collection
python3 scripts/collect_profiles.py

# Parse Reddit posts (r/collegeresults)
# Copy posts to a text file, separate with '---', then:
python3 scripts/reddit_collector.py

# Enrich and validate profiles
python3 scripts/enrich_profiles.py
```

**Note**: All collected data is anonymized (no names, schools, locations) before storage to ensure privacy compliance.

## 🚀 Next Steps

**Phase 1 Complete!** ✅ All 5 agents now use ADK with 17 database tools.

See [NEXT_STEPS.md](NEXT_STEPS.md) for the roadmap ahead:
- **Priority 1**: Expand database with more real anonymized profiles
- **Priority 2**: Build additional validation tools (course prerequisites, college requirements)
- **Priority 3**: Create orchestrator agent for improved coordination
- **Priority 4**: Production features (web interface, deployment, monitoring)

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

**Warning about "non-text parts in the response"**

You may see this warning when first running the system:
```
Warning: there are non-text parts in the response: ['function_call', 'function_call']
```

**This is normal and harmless!** It just means agents are successfully using their database tools (function calls). The warning comes from Google's generativeai library when agents use tools. Most occurrences are suppressed; one may appear on first tool usage.

For more detailed setup instructions, see [SETUP.md](SETUP.md).

## 🔮 Future Enhancements

- **Vector Search**: Enhanced similarity matching using embeddings (sentence-transformers)
- **Orchestrator Agent**: Parent ADK agent coordinating all sub-agents
- **Web Interface**: User-friendly web application with Flask/FastAPI backend
- **Progress Tracking**: Track student progress against the plan
- **College-Specific Requirements**: Database of requirements for specific colleges
- **Additional Tools**: Course prerequisite validator, admission requirements lookup
- **Production Database**: Migration to PostgreSQL with pgvector for semantic search



##  Acknowledgments

Built to make expert college counseling affordable and accessible to all students.
Inspired by ADK samples from the google's ADK samples repo and the public notebook examples 
from the Kaggle Google Agents Intensive Course.