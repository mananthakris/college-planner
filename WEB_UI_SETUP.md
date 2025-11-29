# Web UI Setup Guide

Complete guide for running the College Planner web interface locally.

## 📋 Prerequisites

- **Python 3.10+** (already installed for main project)
- **Node.js 18+** and npm
- **Google API Key** (GOOGLE_API_KEY environment variable)
- **All main project dependencies** installed

## 🚀 Quick Start

### Terminal 1: Backend API

```bash
# Navigate to project root
cd college-planner

# Activate virtual environment
source venv/bin/activate

# Install backend dependencies (first time only)
cd backend
pip install -r requirements.txt

# Set API key (if not already set)
export GOOGLE_API_KEY="your-api-key-here"

# Start the FastAPI server
python api.py
```

Backend will run on **http://localhost:8000**

### Terminal 2: React Frontend

```bash
# Navigate to frontend directory
cd college-planner/frontend

# Install Node.js dependencies (first time only)
npm install

# Start the development server
npm run dev
```

Frontend will run on **http://localhost:3000**

### Step 3: Open in Browser

Open **http://localhost:3000** in your browser and start creating plans!

## 📝 Using the Web Interface

1. **Fill out the form** with student information:
   - Basic info (name, grade, GPA)
   - Test scores (optional)
   - Interests, strengths, target majors/colleges
   - Courses, extracurriculars, achievements

2. **Click "Generate 4-Year Plan"**

3. **View your personalized plan**:
   - Year-by-year breakdown
   - Course recommendations
   - Extracurricular suggestions
   - Key recommendations
   - Plan evaluation

4. **Click "Create New Plan"** to start over

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find what's using the port
lsof -i :8000

# Or change port in backend/api.py:
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Module not found errors:**
- Make sure you're in the project root when running backend
- Verify virtual environment is activated
- Check that all main project dependencies are installed

**API key errors:**
- Verify `GOOGLE_API_KEY` is set: `echo $GOOGLE_API_KEY`
- Make sure it's exported in the same terminal session

### Frontend Issues

**npm install fails:**
- Make sure Node.js 18+ is installed: `node --version`
- Try clearing cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then reinstall

**Port 3000 already in use:**
- Vite will automatically try the next available port
- Or change port in `frontend/vite.config.js`

**CORS errors:**
- Make sure backend is running on port 8000
- Check browser console for specific error
- Verify CORS settings in `backend/api.py`

### Connection Issues

**"Failed to fetch" error:**
- Verify backend is running: `curl http://localhost:8000/`
- Check that both servers are running
- Look at browser console for detailed errors

**API returns 500 error:**
- Check backend terminal for error messages
- Verify GOOGLE_API_KEY is set correctly
- Check that all Python dependencies are installed

## 🎨 Development

### Backend Development

The FastAPI backend uses auto-reload:
```bash
# Backend will automatically reload on code changes
python api.py
```

### Frontend Development

Vite provides hot module replacement:
```bash
# Frontend will automatically reload on code changes
npm run dev
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
# Output in frontend/dist/
```

**Backend:**
```bash
# Use a production ASGI server like gunicorn
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.api:app
```

## 📚 API Documentation

Once the backend is running, visit:
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Security Notes

- The web UI is for **local development only**
- For production, add authentication
- Never commit API keys to version control
- Use environment variables for all secrets

