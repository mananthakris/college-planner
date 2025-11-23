# Google ADK Integration

## Overview

The system now uses the actual **Google ADK (Agent Development Kit)** `Agent` class from `google.adk.agents`. This provides proper agent framework integration following Google's official patterns.

## Installation

```bash
pip install google-adk
```

## ADK Agent Structure

Based on the [Google ADK samples](https://github.com/google/adk-samples/tree/main/python/agents), agents are created using:

```python
from google.adk.agents import Agent

agent = Agent(
    name="agent_name",
    model="gemini-2.5-flash",  # or get_gemini_model()
    description="Agent description",
    instruction="Detailed instructions for the agent",
    tools=[],  # Optional tools
    sub_agents=[]  # Optional sub-agents
)
```

## Current Implementation

### ProfileAgent

Uses ADK Agent for natural language parsing:

```python
from src.agents.profile_agent import parse_natural_language, get_profile_agent

# Get the ADK agent instance
agent = get_profile_agent()

# Use it to parse natural language
profile = parse_natural_language("I'm a freshman interested in CS...")
```

The ADK agent is configured with:
- **Name**: `profile_agent`
- **Model**: Gemini model from config
- **Description**: "Normalizes student input and parses natural language descriptions"
- **Instruction**: Detailed instructions for profile extraction

### RetrievalAgent

Uses ADK Agent for intelligent profile matching:

```python
from src.agents.retrieval_agent import run_retrieval, get_retrieval_agent

# Get the ADK agent instance
agent = get_retrieval_agent()

# Use it for retrieval
retrieval = run_retrieval(profile)
```

## Fallback Behavior

The system has multiple fallback layers:

1. **ADK Agent** (primary) - Uses `google.adk.agents.Agent`
2. **Gemini Direct** (fallback) - Uses `google.generativeai` directly
3. **Rule-based** (final fallback) - Simple keyword matching

This ensures the system works even if ADK is not installed.

## Multi-Agent Architecture

The ADK framework supports sub-agents, which we can use for the full multi-agent system:

```python
from google.adk.agents import Agent

# Create sub-agents
profile_agent = Agent(name="profile_agent", ...)
retrieval_agent = Agent(name="retrieval_agent", ...)
planner_agent = Agent(name="planner_agent", ...)

# Create root orchestrator agent
orchestrator = Agent(
    name="orchestrator",
    sub_agents=[profile_agent, retrieval_agent, planner_agent],
    ...
)
```

## Benefits

1. **Official Framework**: Uses Google's official ADK patterns
2. **Consistency**: Follows ADK best practices
3. **Extensibility**: Easy to add tools and sub-agents
4. **Compatibility**: Works with ADK CLI and tooling
5. **Future-proof**: Ready for ADK features (tools, state, etc.)

## Next Steps

1. **Add Tools**: Implement ADK tools for database queries
2. **Sub-Agents**: Convert all agents to ADK and create orchestrator
3. **Agent Communication**: Use ADK's inter-agent messaging
4. **State Management**: Leverage ADK's state features
5. **CLI Integration**: Use `adk run` command for testing

## References

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Samples](https://github.com/google/adk-samples/tree/main/python/agents)
- [ADK Python Package](https://github.com/google/adk-python)

