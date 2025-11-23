# Next Steps: Agent Integration & Real Data

This guide outlines the roadmap for integrating more ADK agents and using real anonymized student data.

## 🎯 Phase 1: Convert Remaining Agents to ADK

### Current Status
- ✅ **ProfileAgent**: Uses ADK Agent
- ✅ **RetrievalAgent**: Uses ADK Agent  
- ⏳ **PlannerAgent**: Function-based (needs conversion)
- ⏳ **CriticAgent**: Function-based (needs conversion)
- ⏳ **ExplainerAgent**: Function-based (needs conversion)

### Step 1: Convert PlannerAgent to ADK

**File**: `src/agents/planner_agent.py`

```python
from google.adk.agents import Agent
from ..config import get_gemini_model

def _create_planner_agent():
    """Create ADK Agent for planning."""
    return Agent(
        name="planner_agent",
        model=get_gemini_model(),
        description="Creates comprehensive 4-year roadmaps for students",
        instruction="""You are a college planning agent. Your task is to:
        1. Analyze student profile and similar successful students
        2. Create a detailed 4-year plan with courses, ECs, competitions, internships
        3. Ensure progression from freshman to senior year
        4. Align plan with student interests and target colleges/majors
        5. Include test preparation timeline
        6. Set appropriate goals for each year
        
        Return a structured plan with rationale for each year.""",
        tools=[]  # Can add database tools later
    )
```

**Action Items**:
1. Create `_create_planner_agent()` function
2. Modify `plan()` to use ADK agent when available
3. Keep function-based fallback
4. Add agent instance getter: `get_planner_agent()`

### Step 2: Convert CriticAgent to ADK

**File**: `src/agents/critic_agent.py`

```python
def _create_critic_agent():
    """Create ADK Agent for critique."""
    return Agent(
        name="critic_agent",
        model=get_gemini_model(),
        description="Evaluates and critiques 4-year plans",
        instruction="""You are a critique agent. Your task is to:
        1. Evaluate plan quality across multiple dimensions
        2. Identify strengths and weaknesses
        3. Calculate a quality score (0-1)
        4. Provide specific improvement suggestions
        5. Determine if plan needs revision
        
        Be thorough but constructive in your critique.""",
        tools=[]
    )
```

**Action Items**:
1. Create ADK agent wrapper
2. Use agent to enhance critique quality
3. Keep existing evaluation logic as fallback

### Step 3: Convert ExplainerAgent to ADK

**File**: `src/agents/explainer_agent.py`

```python
def _create_explainer_agent():
    """Create ADK Agent for explanation."""
    return Agent(
        name="explainer_agent",
        model=get_gemini_model(),
        description="Generates user-friendly explanations of plans",
        instruction="""You are an explanation agent. Your task is to:
        1. Create clear, user-friendly summaries
        2. Explain the plan in accessible language
        3. Provide actionable recommendations
        4. Generate next steps
        5. Make complex information digestible for high school students
        
        Write in a supportive, encouraging tone.""",
        tools=[]
    )
```

**Action Items**:
1. Create ADK agent wrapper
2. Use agent for better explanations
3. Keep template-based fallback

## 🔗 Phase 2: Multi-Agent Orchestration with ADK

### Step 4: Create Root Orchestrator Agent

Create a parent agent that coordinates all sub-agents:

**File**: `src/agents/orchestrator_agent.py` (new)

```python
from google.adk.agents import Agent
from .profile_agent import get_profile_agent
from .retrieval_agent import get_retrieval_agent
from .planner_agent import get_planner_agent
from .critic_agent import get_critic_agent
from .explainer_agent import get_explainer_agent

def create_orchestrator_agent():
    """Create root orchestrator agent with sub-agents."""
    sub_agents = [
        get_profile_agent(),
        get_retrieval_agent(),
        get_planner_agent(),
        get_critic_agent(),
        get_explainer_agent()
    ]
    
    # Filter out None values (if ADK not installed)
    sub_agents = [a for a in sub_agents if a is not None]
    
    return Agent(
        name="college_planner_orchestrator",
        model=get_gemini_model(),
        description="Orchestrates the multi-agent college planning system",
        instruction="""You coordinate multiple specialized agents to create 
        comprehensive college preparation plans. Delegate tasks to appropriate 
        sub-agents and synthesize their outputs.""",
        sub_agents=sub_agents,
        tools=[]
    )
```

## 📊 Phase 3: Real Anonymized Data Integration

### Step 5: Data Collection Workflow

1. **Collect from Reddit** (`r/collegeresults`):
   ```bash
   # Use the collection script
   python3 scripts/collect_profiles.py
   ```

2. **Anonymize Data**:
   - Remove names → Use "Student 1", "Student 2", etc.
   - Remove specific school names → Use "Large Public High School"
   - Remove locations → Use generic descriptions
   - Remove email/phone numbers

3. **Validate Data Quality**:
   - Ensure all required fields present
   - Check data consistency
   - Verify anonymization

### Step 6: Data Enrichment

Add missing fields to collected profiles:

```python
# scripts/enrich_profiles.py
def enrich_profile(profile):
    """Add missing fields with defaults."""
    profile.setdefault("colleges_admitted", [])
    profile.setdefault("final_major", None)
    profile.setdefault("gpa", None)
    profile.setdefault("test_scores", {})
    return profile
```

### Step 7: Database Migration

Migrate from JSON to a proper database:

**Option A: SQLite** (simple, file-based)
```python
import sqlite3

def migrate_to_sqlite(json_file, db_file):
    """Migrate JSON profiles to SQLite."""
    # Implementation
    pass
```

**Option B: Vector Database** (for semantic search)
- Use Pinecone, Weaviate, or Chroma
- Generate embeddings for profiles
- Enable semantic similarity search

## 🛠️ Phase 4: Enhanced Features

### Step 8: Add Tools to Agents

Enable agents to use tools (database queries, API calls):

```python
from google.adk.tools import Tool

# Database query tool
def search_profiles_tool(query: str) -> List[Dict]:
    """Tool for searching profiles."""
    db = get_database()
    return db.search_by_interests(query.split(","))

# Add to agent
agent = Agent(
    name="retrieval_agent",
    tools=[
        Tool(
            name="search_profiles",
            description="Search student profiles by interests",
            function=search_profiles_tool
        )
    ]
)
```

### Step 9: Add Vector Search

Implement semantic similarity:

```python
# Install: pip install sentence-transformers
from sentence_transformers import SentenceTransformer

def generate_embeddings(profiles):
    """Generate embeddings for profiles."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # Generate embeddings
    # Store in vector database
    pass
```

### Step 10: Agent State Management

Track conversation/planning state:

```python
# Use ADK's state management
agent = Agent(
    name="planner_agent",
    state={"current_iteration": 0, "previous_plans": []}
)
```

## 📋 Implementation Checklist

### Immediate (Week 1-2)
- [ ] Convert PlannerAgent to ADK
- [ ] Convert CriticAgent to ADK
- [ ] Convert ExplainerAgent to ADK
- [ ] Test all agents work together

### Short-term (Week 3-4)
- [ ] Collect 50-100 real anonymized profiles
- [ ] Validate and enrich collected data
- [ ] Update database with real profiles
- [ ] Test retrieval with real data

### Medium-term (Month 2)
- [ ] Create orchestrator agent
- [ ] Add tools to agents
- [ ] Implement vector search
- [ ] Improve similarity matching

### Long-term (Month 3+)
- [ ] Migrate to proper database (SQL/Vector)
- [ ] Add agent state management
- [ ] Implement agent communication
- [ ] Build web interface

## 🚀 Quick Start: Convert One Agent

Here's a template to convert any agent:

```python
# In src/agents/[agent_name]_agent.py

from google.adk.agents import Agent
from ..config import get_gemini_model

def _create_[agent_name]_agent():
    """Create ADK Agent."""
    try:
        return Agent(
            name="[agent_name]_agent",
            model=get_gemini_model(),
            description="[Description]",
            instruction="""[Detailed instructions]""",
            tools=[]
        )
    except ImportError:
        return None

def [existing_function](...):
    """Enhanced with ADK Agent."""
    agent = _create_[agent_name]_agent()
    
    if agent:
        try:
            # Use ADK agent
            result = agent.run(prompt)
            return process_result(result)
        except Exception as e:
            print(f"ADK Agent error: {e}. Using fallback.")
    
    # Fallback to existing function logic
    return [existing_function_logic](...)

_[agent_name]_agent_instance = None

def get_[agent_name]_agent():
    """Get or create agent instance."""
    global _[agent_name]_agent_instance
    if _[agent_name]_agent_instance is None:
        _[agent_name]_agent_instance = _create_[agent_name]_agent()
    return _[agent_name]_agent_instance
```

## 📚 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Samples](https://github.com/google/adk-samples/tree/main/python/agents)
- [DATA_SOURCES.md](DATA_SOURCES.md) - For finding real profiles
- [SETUP.md](SETUP.md) - For environment setup

## 💡 Tips

1. **Start Small**: Convert one agent at a time, test thoroughly
2. **Keep Fallbacks**: Always maintain function-based fallbacks
3. **Test Incrementally**: Test each agent before moving to next
4. **Document Changes**: Update documentation as you go
5. **Version Control**: Commit after each agent conversion

## 🎯 Success Metrics

- All 5 agents use ADK
- 100+ real anonymized profiles in database
- Vector search working
- Orchestrator coordinating agents
- System produces high-quality plans

