import { useState } from 'react';
import StudentForm from './components/StudentForm';
import ResultsDisplay from './components/ResultsDisplay';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch('http://localhost:8000/api/plan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: response.statusText }));
        throw new Error(errorData.detail || `Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎓 College Planner</h1>
        <p>Create your personalized 4-year high school roadmap</p>
      </header>

      <main className="app-main">
        {!results ? (
          <StudentForm onSubmit={handleSubmit} loading={loading} error={error} />
        ) : (
          <ResultsDisplay results={results} onReset={() => setResults(null)} />
        )}
      </main>
    </div>
  );
}

export default App;

