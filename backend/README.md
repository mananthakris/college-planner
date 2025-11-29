# Backend API Setup

## Installation

The backend requires both the main project dependencies AND backend-specific dependencies.

### Step 1: Install Main Project Dependencies

```bash
# From project root, with venv activated
cd college-planner
source venv/bin/activate

# Install main project dependencies (google-adk, etc.)
pip install -r requirements.txt
```

### Step 2: Install Backend Dependencies

```bash
# Still in project root with venv activated
pip install -r backend/requirements.txt
```

### Step 3: Set API Key

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### Step 4: Run Backend

```bash
# From project root
cd backend
python api.py
```

Or from project root:
```bash
python backend/api.py
```

## Troubleshooting

### "No module named 'google.adk'"
- Make sure virtual environment is activated: `source venv/bin/activate`
- Install main dependencies: `pip install -r requirements.txt`

### "No module named 'pydantic._internal._signature'"
- This is a pydantic version conflict
- Reinstall with correct versions: `pip install -r backend/requirements.txt --force-reinstall`

### "Failed to import main project modules"
- Make sure you're running from project root or backend directory
- Verify virtual environment is activated
- Check that all dependencies are installed

## Quick Setup (All at Once)

```bash
cd college-planner
source venv/bin/activate
pip install -r requirements.txt
pip install -r backend/requirements.txt
export GOOGLE_API_KEY="your-key"
cd backend
python api.py
```

