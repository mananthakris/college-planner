import { useState } from 'react';
import './StudentForm.css';

// Move ListInput outside the component to prevent recreation on each render
const ListInput = ({ label, field, dataField, placeholder, required = false, 
                     currentInput, setCurrentInput, formData, addToList, removeFromList }) => (
  <div className="form-section">
    <h2>{label} {required && <span className="required">*</span>}</h2>
    <div className="list-input-group">
      <input
        type="text"
        value={currentInput[field]}
        onChange={(e) => setCurrentInput({ ...currentInput, [field]: e.target.value })}
        onKeyPress={(e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            addToList(dataField, currentInput[field]);
          }
        }}
        placeholder={placeholder}
      />
      <button type="button" onClick={() => addToList(dataField, currentInput[field])}>
        Add
      </button>
    </div>
    <div className="tag-list">
      {formData[dataField].map((item, index) => (
        <span key={index} className="tag">
          {item}
          <button type="button" onClick={() => removeFromList(dataField, index)}>×</button>
        </span>
      ))}
    </div>
  </div>
);

function StudentForm({ onSubmit, loading, error }) {
  const [formData, setFormData] = useState({
    name: '',
    current_grade: 9,
    interests: [],
    academic_strengths: [],
    courses_taken: [],
    courses_planned: [],
    extracurriculars: [],
    achievements: [],
    target_colleges: [],
    target_majors: [],
    gpa: '',
    test_scores: {
      SAT: '',
      ACT: ''
    }
  });

  const [currentInput, setCurrentInput] = useState({
    interest: '',
    academic_strength: '',
    course_taken: '',
    course_planned: '',
    extracurricular: '',
    achievement: '',
    target_college: '',
    target_major: ''
  });

  const addToList = (field, value) => {
    if (value.trim()) {
      setFormData(prev => ({
        ...prev,
        [field]: [...prev[field], value.trim()]
      }));
      setCurrentInput(prev => ({ ...prev, [field]: '' }));
    }
  };

  const removeFromList = (field, index) => {
    setFormData(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index)
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate required fields
    if (!formData.name.trim()) {
      alert('Please enter your name');
      return;
    }
    if (formData.interests.length === 0) {
      alert('Please add at least one interest');
      return;
    }
    if (formData.target_majors.length === 0) {
      alert('Please add at least one target major');
      return;
    }
    if (formData.target_colleges.length === 0) {
      alert('Please add at least one target college');
      return;
    }
    
    // Prepare data for API
    const submitData = {
      ...formData,
      gpa: formData.gpa ? parseFloat(formData.gpa) : null,
      test_scores: {
        ...(formData.test_scores.SAT && { SAT: parseInt(formData.test_scores.SAT) }),
        ...(formData.test_scores.ACT && { ACT: parseInt(formData.test_scores.ACT) })
      }
    };

    onSubmit(submitData);
  };

  return (
    <form className="student-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h2>Basic Information</h2>
        
        <div className="form-group">
          <label>Name <span className="required">*</span></label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            placeholder="Your name"
          />
        </div>

        <div className="form-group">
          <label>Current Grade <span className="required">*</span></label>
          <select
            value={formData.current_grade}
            onChange={(e) => setFormData({ ...formData, current_grade: parseInt(e.target.value) })}
            required
          >
            <option value={9}>9th Grade (Freshman)</option>
            <option value={10}>10th Grade (Sophomore)</option>
            <option value={11}>11th Grade (Junior)</option>
            <option value={12}>12th Grade (Senior)</option>
          </select>
        </div>

        <div className="form-group">
          <label>GPA (Optional)</label>
          <input
            type="number"
            step="0.01"
            min="0"
            max="5"
            value={formData.gpa}
            onChange={(e) => setFormData({ ...formData, gpa: e.target.value })}
            placeholder="e.g., 3.8"
          />
        </div>
      </div>

      <div className="form-section">
        <h2>Test Scores (Optional)</h2>
        
        <div className="form-row">
          <div className="form-group">
            <label>SAT Score</label>
            <input
              type="number"
              value={formData.test_scores.SAT}
              onChange={(e) => setFormData({
                ...formData,
                test_scores: { ...formData.test_scores, SAT: e.target.value }
              })}
              placeholder="e.g., 1500"
            />
          </div>

          <div className="form-group">
            <label>ACT Score</label>
            <input
              type="number"
              value={formData.test_scores.ACT}
              onChange={(e) => setFormData({
                ...formData,
                test_scores: { ...formData.test_scores, ACT: e.target.value }
              })}
              placeholder="e.g., 34"
            />
          </div>
        </div>
      </div>

      <ListInput 
        label="Interests" 
        field="interest" 
        dataField="interests"
        placeholder="e.g., Computer Science, Engineering"
        required={true}
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Academic Strengths" 
        field="academic_strength" 
        dataField="academic_strengths"
        placeholder="e.g., Math, Science, Writing"
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Target Majors" 
        field="target_major" 
        dataField="target_majors"
        placeholder="e.g., Computer Science, Engineering"
        required={true}
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Target Colleges" 
        field="target_college" 
        dataField="target_colleges"
        placeholder="e.g., MIT, Stanford, UC Berkeley"
        required={true}
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Courses Taken" 
        field="course_taken" 
        dataField="courses_taken"
        placeholder="e.g., AP Calculus, AP Physics"
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Courses Planned" 
        field="course_planned" 
        dataField="courses_planned"
        placeholder="e.g., AP Chemistry, AP Biology"
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Extracurriculars" 
        field="extracurricular" 
        dataField="extracurriculars"
        placeholder="e.g., Robotics Club, Debate Team"
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      <ListInput 
        label="Achievements" 
        field="achievement" 
        dataField="achievements"
        placeholder="e.g., Science Fair Winner, Math Olympiad"
        currentInput={currentInput}
        setCurrentInput={setCurrentInput}
        formData={formData}
        addToList={addToList}
        removeFromList={removeFromList}
      />

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      <button type="submit" className="submit-button" disabled={loading}>
        {loading ? 'Creating Your Plan...' : 'Generate 4-Year Plan'}
      </button>
    </form>
  );
}

export default StudentForm;

