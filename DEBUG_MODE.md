# Debug Mode Guide

Debug mode provides detailed logging to help diagnose issues with agent responses and JSON parsing.

## 🚀 Quick Start

### Enable Debug Mode

**Option 1: Environment Variable (Temporary)**
```bash
export DEBUG_MODE=1
python3 main.py
```

**Option 2: Inline (One Command)**
```bash
DEBUG_MODE=1 python3 main.py
```

**Option 3: .env File (Permanent)**
```bash
# Add to .env file:
DEBUG_MODE=1
```

### Disable Debug Mode

```bash
# Unset the variable
unset DEBUG_MODE

# Or set to 0
export DEBUG_MODE=0
```

## 📊 What Debug Mode Shows

When enabled, debug mode provides detailed output at each stage:

### 1. Agent Response (`run_agent_sync`)
- Response type and length
- Number of events processed
- First 1000 characters of response

### 2. JSON Extraction (`extract_json_from_response`)
- Response length
- First 500 characters
- Which extraction method was tried
- Success/failure of each attempt
- Extracted JSON keys (if successful)

### 3. Agent-Specific Debugging
- **PlannerAgent**: Shows extracted plan structure and keys
- **CriticAgent**: Shows extracted critique keys
- **ExplainerAgent**: Shows extracted explanation keys
- Full exception tracebacks on errors

## 🔍 Example Debug Output

```
================================================================================
DEBUG [run_agent_sync]: Agent Response
================================================================================
Response type: <class 'str'>
Response length: 2345 characters
Number of events processed: 3
Response (first 1000 chars):
```json
{
  "freshman_plan": {
    "courses": ["Algebra I", "Biology"],
    ...
  }
}
```
================================================================================

================================================================================
DEBUG [extract_json]: Attempting to extract JSON
================================================================================
Response length: 2345 characters
First 500 chars:
```json
{
  "freshman_plan": {
...
DEBUG [extract_json]: Found JSON in markdown code block
DEBUG [extract_json]: ✓ Successfully parsed JSON from markdown
DEBUG [extract_json]: Keys: ['freshman_plan', 'sophomore_plan', 'junior_plan', 'senior_plan', 'overall_strategy', 'key_milestones']
================================================================================

================================================================================
DEBUG [planner_agent]: JSON Extraction Result
================================================================================
Extracted type: <class 'dict'>
Extracted keys: ['freshman_plan', 'sophomore_plan', 'junior_plan', 'senior_plan', 'overall_strategy', 'key_milestones']
Has freshman_plan: True
Has sophomore_plan: True
================================================================================
```

## 🐛 Troubleshooting with Debug Mode

### Issue: JSON is None

**What to look for:**
1. Check `DEBUG [run_agent_sync]` - Is there a response?
2. Check `DEBUG [extract_json]` - What does the response look like?
3. Check if JSON is malformed or missing

**Common causes:**
- Agent only made tool calls (no text response)
- Response is plain text, not JSON
- JSON is malformed or incomplete
- Response is empty

### Issue: Wrong JSON Structure

**What to look for:**
- Check `DEBUG [planner_agent]: Extracted keys` - Are expected keys present?
- Check if keys match expected structure

## 💡 Tips

1. **Enable for debugging**: Use when investigating JSON parsing issues
2. **Disable for production**: Turn off for cleaner output
3. **Selective debugging**: Debug output appears for all agents, so you'll see the full pipeline flow
4. **Save output**: Redirect to file for analysis:
   ```bash
   DEBUG_MODE=1 python3 main.py > debug_output.txt 2>&1
   ```

## 🔧 Configuration

Debug mode is controlled by the `DEBUG_MODE` environment variable:
- `1`, `true`, `yes`, `on` → Debug enabled
- `0`, `false`, `no`, `off` (or unset) → Debug disabled

The check is case-insensitive.

