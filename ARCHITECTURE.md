# Architecture Overview

## Multi-Agent System Flow

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
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Retrieval Agent │
                    │  (Find Similar  │
                    │   Profiles &    │
                    │  Opportunities) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Planner Agent  │
                    │ (Create 4-Year  │
                    │      Plan)      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Critic Agent   │
                    │   (Evaluate)   │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────▼─────┐    ┌──────▼──────┐
              │ Score >=  │    │ Score <     │
              │ Threshold │    │ Threshold   │
              │ & No      │    │ OR Critical │
              │ Critical   │    │ Weaknesses  │
              │ Issues?    │    │ Found?      │
              └─────┬─────┘    └──────┬──────┘
                    │                 │
                    │                 │
                    │    ┌────────────┘
                    │    │
                    │    ▼
                    │  Refine Plan
                    │    │
                    └────┘
                    │
                    ▼
            ┌───────────────┐
            │ Explainer     │
            │ Agent         │
            │ (Generate     │
            │ Final Output) │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ User-Friendly │
            │ 4-Year Plan   │
            └───────────────┘
```

## Agent Responsibilities

### Profile Agent
- **Input**: Raw student profile dictionary
- **Output**: Normalized `StudentProfile` object
- **Function**: Converts various input formats into structured data

### Retrieval Agent
- **Input**: Normalized student profile
- **Output**: Similar profiles + relevant opportunities
- **Function**: 
  - Calculates similarity scores based on interests, majors, strengths
  - Filters opportunities by grade level and interests

### Planner Agent
- **Input**: Student profile + retrieval results
- **Output**: `FourYearPlan` with yearly breakdowns
- **Function**: 
  - Creates course recommendations for each year
  - Suggests extracurriculars, competitions, internships
  - Sets goals and generates rationale

### Critic Agent (Loop Agent)
- **Input**: Student profile + plan
- **Output**: `Critique` with score, strengths, weaknesses, suggestions
- **Function**:
  - Evaluates plan quality (0-1 score)
  - Identifies strengths and weaknesses
  - Determines if revision is needed
  - Provides specific improvement suggestions

### Explainer Agent
- **Input**: Profile + plan + critique
- **Output**: `Explanation` with user-friendly format
- **Function**:
  - Generates executive summary
  - Creates year-by-year breakdown
  - Provides recommendations and next steps

## Data Models

### Core Models
- `StudentProfile`: Normalized student information
- `FourYearPlan`: Complete 4-year roadmap
- `YearlyPlan`: Plan for a specific grade year
- `Critique`: Evaluation of a plan
- `Explanation`: Final user-facing output
- `SimilarProfile`: Matched profile with similarity score
- `Opportunity`: Academic/extracurricular opportunity

## Evaluation Metrics

The Critic Agent evaluates plans on:
1. **Course Rigor** (25%): Number and difficulty of courses
2. **Extracurricular Depth** (20%): Diversity and leadership
3. **Alignment Score** (25%): Match with interests and majors
4. **Progression Score** (15%): Academic progression across years
5. **Test Prep Score** (15%): Standardized test preparation strategy

## Iteration Logic

The orchestrator implements a refinement loop:
1. Generate initial plan
2. Critique the plan
3. If score < threshold OR critical weaknesses → refine plan
4. Re-critique refined plan
5. Repeat until score >= threshold OR max iterations reached
6. Generate final explanation

## Extensibility

The system is designed to be extended with:
- **LLM Integration**: Replace rule-based logic with LLM calls
- **Vector Search**: Use embeddings for better similarity matching
- **Real Data**: Connect to actual student profile databases
- **Web Interface**: Add API endpoints and frontend
- **Progress Tracking**: Monitor student progress against plan

