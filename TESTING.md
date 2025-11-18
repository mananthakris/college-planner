# Testing Guide

## Quick Test

Run the simple test to see Engineering vs Pre-Med profiles:

```bash
python3 test_simple.py
```

This will show:
- Plan quality scores
- Key courses by year
- Extracurricular recommendations
- Top recommendations
- Evaluation metrics

## Detailed Test

For comprehensive output with full year-by-year breakdowns:

```bash
python3 test_profiles.py
```

This includes:
- Complete plan summaries
- Year-by-year detailed breakdowns
- All recommendations and next steps
- Full evaluation details
- Saves JSON files to `output/` directory

## Test Profiles

### Engineering Student
- **Name**: Jordan Martinez
- **Grade**: 9 (Freshman)
- **Interests**: Engineering, Physics, Mathematics, Robotics
- **Target Majors**: Mechanical Engineering, Aerospace Engineering
- **Target Colleges**: MIT, Stanford, Caltech, Georgia Tech

### Pre-Med Student
- **Name**: Maya Patel
- **Grade**: 9 (Freshman)
- **Interests**: Medicine, Biology, Chemistry, Healthcare
- **Target Majors**: Biology, Pre-Med, Biochemistry
- **Target Colleges**: Johns Hopkins, Harvard, Yale, Duke

## Expected Differences

The system should generate different plans based on:

1. **Course Recommendations**:
   - Engineering: More math/physics focus, Calculus emphasis
   - Pre-Med: More biology/chemistry focus, AP Biology emphasis

2. **Extracurriculars**:
   - Engineering: Robotics, Math Olympiad, Engineering competitions
   - Pre-Med: Hospital volunteering, Science research, Biology competitions

3. **Test Prep**:
   - Both: SAT/ACT prep in junior year
   - Engineering: May emphasize Math Subject Tests
   - Pre-Med: May emphasize Science Subject Tests

## Custom Testing

You can create your own test by modifying the profiles in `test_simple.py`:

```python
my_profile = {
    "name": "Your Name",
    "current_grade": 9,  # or 10, 11, 12
    "interests": ["Your", "Interests"],
    "academic_strengths": ["Your", "Strengths"],
    "courses_taken": [],
    "courses_planned": [],
    "extracurriculars": ["Your", "ECs"],
    "achievements": [],
    "target_colleges": ["College", "List"],
    "target_majors": ["Your", "Majors"],
    "gpa": None,
    "test_scores": {}
}

result = run_pipeline(my_profile)
```

## Output Files

Detailed results are saved to `output/` directory:
- `jordan_martinez_plan.json` (Engineering)
- `maya_patel_plan.json` (Pre-Med)

Each file contains the complete plan, evaluation, and recommendations in JSON format.

