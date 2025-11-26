# Setup Guide

Complete setup instructions for the College Planner multi-agent system.

## Prerequisites

- **Python 3.10 or higher** (required for Google ADK)
- pip (Python package manager)

**Important**: Google ADK requires Python 3.10+. Python 3.9 will not work.

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd college-planner
```

### 2. Check Python Version

```bash
# Check default Python version
python3 --version

# If it shows 3.9 or lower, check for Python 3.10+
which python3.12 python3.11 python3.10
```

**If you don't have Python 3.10+:**

**macOS (Homebrew):**
```bash
brew install python@3.12
# Then use: python3.12 -m venv venv
```

**macOS (without Homebrew):**
- Download from [python.org](https://www.python.org/downloads/)
- Install Python 3.12

**Linux:**
```bash
sudo apt install python3.10  # Ubuntu/Debian
# or
sudo yum install python3.10  # RHEL/CentOS
```

### 3. Create Virtual Environment

**Using Python 3.10+ (required):**

```bash
# Option 1: If python3 points to 3.10+
python3 -m venv venv

# Option 2: Use specific version
python3.12 -m venv venv  # or python3.11 or python3.10

# Option 3: Use full path (if needed)
/opt/homebrew/bin/python3.12 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Verify Python version in venv
python --version  # Should show 3.10, 3.11, or 3.12

# You should see (venv) in your terminal prompt
```

**If you see Python 3.9 in the venv:**
```bash
# Deactivate and recreate with correct version
deactivate
rm -rf venv
python3.12 -m venv venv  # Use your Python 3.10+ version
source venv/bin/activate
python --version  # Verify it's 3.10+
```

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Makes it easier to manage package versions

### 3. Install Dependencies

```bash
# Make sure virtual environment is activated
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit .env file with your API key
# On macOS/Linux:
nano .env
# or
vim .env

# On Windows:
notepad .env
```

Add your Google API key:
```
GOOGLE_API_KEY=your-actual-api-key-here
```

**Get your API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### 5. Verify Installation

```bash
# Test that everything works
python3 -c "from src import run_pipeline; print('✓ Installation successful!')"
```

## Running the System

### Basic Usage

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Run the main example
python3 main.py

# Or run tests
python3 test_simple.py
python3 test_natural_language.py
```

## Troubleshooting

### Virtual Environment Issues

**Problem**: `python3 -m venv venv` command not found
- **Solution**: Make sure Python 3.8+ is installed. Try `python -m venv venv` instead.

**Problem**: Can't activate virtual environment
- **Solution**: 
  - macOS/Linux: Make sure you use `source venv/bin/activate`
  - Windows: Use `venv\Scripts\activate`
  - Check that the `venv` directory was created successfully

### Package Installation Issues

**Problem**: `pip install` fails
- **Solution**: 
  - Make sure virtual environment is activated
  - Try: `pip install --upgrade pip` first
  - Check your internet connection
  - On some systems, use `pip3` instead of `pip`

**Problem**: `google-adk` package not found
- **Solution**: 
  - The package might not be publicly available yet
  - The system will use fallback implementations
  - Check [Google ADK documentation](https://google.github.io/adk-docs/) for latest installation instructions

### API Key Issues

**Problem**: API key not working
- **Solution**:
  - Verify the key is correct in `.env` file
  - Make sure there are no extra spaces or quotes
  - Check that `GOOGLE_API_KEY` environment variable is set
  - The system will work with rule-based fallback if API key is missing

## Deactivating Virtual Environment

When you're done working:

```bash
# Deactivate the virtual environment
deactivate
```

## Updating Dependencies

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Update all packages
pip install --upgrade -r requirements.txt

# Or update a specific package
pip install --upgrade google-adk
```

## Development Setup

For development, you might want additional tools:

```bash
# Install development dependencies (optional)
pip install pytest black mypy

# Run tests
pytest

# Format code
black src/
```

## Next Steps

- Read [README.md](README.md) for usage examples
- Check [ADK_INTEGRATION.md](ADK_INTEGRATION.md) for ADK-specific setup
- See [TESTING.md](TESTING.md) for testing instructions

