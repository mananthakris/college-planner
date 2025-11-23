# Setup Guide

Complete setup instructions for the College Planner multi-agent system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd college-planner
```

### 2. Create Virtual Environment

Using `venv` (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
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

