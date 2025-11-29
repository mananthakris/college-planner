import './ResultsDisplay.css';

function ResultsDisplay({ results, onReset }) {
  const yearPlans = [
    { name: 'Freshman Year (9th Grade)', data: results.freshman_plan },
    { name: 'Sophomore Year (10th Grade)', data: results.sophomore_plan },
    { name: 'Junior Year (11th Grade)', data: results.junior_plan },
    { name: 'Senior Year (12th Grade)', data: results.senior_plan }
  ];

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>Your 4-Year College Plan</h2>
        <button onClick={onReset} className="reset-button">Create New Plan</button>
      </div>

      <div className="results-summary">
        <div className="score-card">
          <h3>Plan Quality Score</h3>
          <div className="score-value">{(results.evaluation.score * 100).toFixed(0)}%</div>
          <p>Refined over {results.iterations} iteration{results.iterations !== 1 ? 's' : ''}</p>
        </div>
      </div>

      <div className="results-section">
        <h3>Summary</h3>
        <p className="summary-text">{results.plan_summary}</p>
      </div>

      <div className="results-section">
        <h3>Overall Strategy</h3>
        <p className="strategy-text">{results.plan_overview}</p>
      </div>

      <div className="results-section">
        <h3>Year-by-Year Breakdown</h3>
        {yearPlans.map((year, idx) => (
          <div key={idx} className="year-plan">
            <h4>{year.name}</h4>
            {year.data.courses.length > 0 && (
              <div className="plan-category">
                <strong>Courses:</strong>
                <ul>
                  {year.data.courses.map((course, i) => (
                    <li key={i}>{course}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.extracurriculars.length > 0 && (
              <div className="plan-category">
                <strong>Extracurriculars:</strong>
                <ul>
                  {year.data.extracurriculars.map((ec, i) => (
                    <li key={i}>{ec}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.competitions.length > 0 && (
              <div className="plan-category">
                <strong>Competitions:</strong>
                <ul>
                  {year.data.competitions.map((comp, i) => (
                    <li key={i}>{comp}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.internships.length > 0 && (
              <div className="plan-category">
                <strong>Internships:</strong>
                <ul>
                  {year.data.internships.map((intern, i) => (
                    <li key={i}>{intern}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.test_prep.length > 0 && (
              <div className="plan-category">
                <strong>Test Prep:</strong>
                <ul>
                  {year.data.test_prep.map((prep, i) => (
                    <li key={i}>{prep}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.goals.length > 0 && (
              <div className="plan-category">
                <strong>Goals:</strong>
                <ul>
                  {year.data.goals.map((goal, i) => (
                    <li key={i}>{goal}</li>
                  ))}
                </ul>
              </div>
            )}
            {year.data.rationale && (
              <div className="plan-category">
                <strong>Rationale:</strong>
                <p>{year.data.rationale}</p>
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="results-section">
        <h3>Key Recommendations</h3>
        <ol className="recommendations-list">
          {results.recommendations.map((rec, i) => (
            <li key={i}>{rec}</li>
          ))}
        </ol>
      </div>

      <div className="results-section">
        <h3>Next Steps</h3>
        <ol className="next-steps-list">
          {results.next_steps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </div>

      <div className="results-section">
        <h3>Plan Evaluation</h3>
        <div className="evaluation">
          <div className="evaluation-category">
            <h4>Strengths</h4>
            <ul>
              {results.evaluation.strengths.map((strength, i) => (
                <li key={i}>✓ {strength}</li>
              ))}
            </ul>
          </div>
          <div className="evaluation-category">
            <h4>Areas for Improvement</h4>
            <ul>
              {results.evaluation.weaknesses.map((weakness, i) => (
                <li key={i}>• {weakness}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ResultsDisplay;

