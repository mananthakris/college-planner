# Agent Architecture - BaseAgent Class System

## Overview

The multi-agent system now uses a `BaseAgent` class that follows Google ADK patterns, providing a consistent interface for all agents while maintaining full backward compatibility.

## Architecture

### BaseAgent Class

All agents inherit from `BaseAgent`, which provides:
- Standardized initialization with name and description
- Optional Gemini integration
- Common interface via `run()` method
- Consistent agent metadata

```python
class BaseAgent(ABC):
    def __init__(self, name: str, description: str, use_gemini: bool = False)
    @abstractmethod
    def run(self, *args, **kwargs) -> Any
```

### Current Agent Classes

1. **ProfileAgent** (extends BaseAgent)
   - Parses natural language input using Gemini
   - Normalizes structured input
   - Uses Gemini for intelligent extraction

2. **RetrievalAgent** (extends BaseAgent)
   - Finds similar profiles from database
   - Filters relevant opportunities
   - Uses database search methods

3. **PlannerAgent** (function-based, can be converted)
4. **CriticAgent** (function-based, can be converted)
5. **ExplainerAgent** (function-based, can be converted)

## Usage

### Class-Based Usage (New)

```python
from src.agents import ProfileAgent, RetrievalAgent

# Create agent instances
profile_agent = ProfileAgent(use_gemini=True)
retrieval_agent = RetrievalAgent()

# Use the run() method
profile = profile_agent.run(input_data)  # Can be dict or string
retrieval = retrieval_agent.run(profile)
```

### Legacy Function-Based Usage (Still Works)

```python
from src.agents.profile_agent import normalize, parse_natural_language
from src.agents.retrieval_agent import run_retrieval

# Legacy functions still work
profile = normalize(profile_dict)
profile = parse_natural_language("I'm a freshman...")
retrieval = run_retrieval(profile)
```

## Benefits

1. **Consistency**: All agents follow the same pattern
2. **Extensibility**: Easy to add new agents by extending BaseAgent
3. **Gemini Integration**: Built-in support for Google Generative AI
4. **Backward Compatible**: Legacy functions still work
5. **Type Safety**: Better IDE support and type checking

## Multi-Agent Architecture Preserved

The full multi-agent system is intact:

```
ProfileAgent → RetrievalAgent → PlannerAgent → CriticAgent → ExplainerAgent
```

All agents work together through the orchestrator, which supports both:
- Class-based agents (ProfileAgent, RetrievalAgent)
- Function-based agents (PlannerAgent, CriticAgent, ExplainerAgent)

## Migration Path

To convert remaining agents to use BaseAgent:

```python
class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PlannerAgent",
            description="Creates 4-year roadmaps",
            use_gemini=False  # or True if you want Gemini
        )
    
    def run(self, profile: StudentProfile, retrieval: Dict) -> FourYearPlan:
        # Existing plan() logic here
        return self.plan(profile, retrieval)
```

## Testing

Run the test script to verify everything works:

```bash
python3 test_agent_classes.py
```

This tests:
- ✓ BaseAgent class architecture
- ✓ ProfileAgent and RetrievalAgent functionality
- ✓ Legacy function compatibility
- ✓ Full multi-agent pipeline

## Next Steps

1. **Convert Remaining Agents**: Migrate PlannerAgent, CriticAgent, ExplainerAgent to BaseAgent
2. **Add Agent Tools**: Implement tool calling for agents (e.g., database queries)
3. **Agent Communication**: Add inter-agent messaging
4. **Agent State**: Add state management for agents
5. **Vector Search**: Add to RetrievalAgent for semantic matching

