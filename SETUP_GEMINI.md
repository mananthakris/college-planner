# Google Gemini Integration Setup

## Overview

The Profile Agent now uses Google's Generative AI (Gemini) to parse natural language input from students. This allows students to describe themselves in free-form text rather than filling out structured forms.

## Setup

### 1. Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### 2. Set Environment Variable

**Option A: Export in terminal**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

**Option B: Create .env file**
```bash
# Install python-dotenv (optional)
pip install python-dotenv

# Create .env file
echo "GOOGLE_API_KEY=your-api-key-here" > .env
```

**Option C: Set in your shell profile**
Add to `~/.zshrc` or `~/.bashrc`:
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Natural Language Input

```python
from src.agents.profile_agent import parse_natural_language
from src.agents.retrieval_agent import run_retrieval

# Student describes themselves naturally
input_text = """
I'm a freshman interested in computer science and math. 
I want to go to MIT or Stanford. I'm in robotics club.
"""

# Parse into structured profile
profile = parse_natural_language(input_text)

# Use with retrieval agent
retrieval = run_retrieval(profile)
```

### Testing

Run the test script:
```bash
python3 test_natural_language.py
```

## Fallback Behavior

If the API key is not set or Gemini is unavailable, the system automatically falls back to rule-based parsing. This ensures the system works even without API access, though with reduced accuracy.

## Database

The system now uses a JSON-based database (`data/student_profiles.json`) to store and query student profiles. This can be easily migrated to:
- SQLite/SQL database
- Vector database (for semantic search)
- Cloud database (Firestore, etc.)

## Next Steps

1. **Add Vector Search**: Use embeddings for semantic similarity matching
2. **Enhance Database**: Migrate to SQL or vector DB for better performance
3. **Add More Profiles**: Populate database with real student profiles
4. **Improve Matching**: Use Gemini to generate better similarity scores

