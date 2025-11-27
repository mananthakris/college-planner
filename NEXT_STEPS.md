# Next Steps: Agent Integration & Real Data

This guide outlines the roadmap for integrating more ADK agents and using real anonymized student data.

**Last Updated**: All 5 agents now use ADK with database tools! Phase 1 complete. Ready for Phase 2 (orchestrator) and Phase 3 (real data integration).

## ✅ Phase 1 Complete: All Agents Using ADK with Tools

### Current Status
- ✅ **ProfileAgent**: Uses ADK Agent (parses natural language input)
- ✅ **RetrievalAgent**: Uses ADK Agent with 6 database tools (search_profiles, search_by_major, search_by_college, find_similar_profiles, get_opportunities, get_profile_statistics)
- ✅ **PlannerAgent**: Uses ADK Agent with 4 database tools (get_opportunities, find_similar_profiles, search_by_college, search_by_major)
- ✅ **CriticAgent**: Uses ADK Agent with 4 database tools (find_similar_profiles, search_by_college, search_by_major, get_profile_statistics)
- ✅ **ExplainerAgent**: Uses ADK Agent with 3 database tools (find_similar_profiles, search_by_college, get_opportunities)

### Agent Tools Summary

| Agent | Tool Count | Purpose |
|-------|------------|---------|
| ProfileAgent | 0 | Parses student input (doesn't need database) |
| RetrievalAgent | 6 | Comprehensive database search and retrieval |
| PlannerAgent | 4 | Dynamic planning with database queries |
| CriticAgent | 4 | Data-driven evaluation against benchmarks |
| ExplainerAgent | 3 | Examples and context from database |

**Total**: 17 tool instances across agents, all working with suppressed warnings!

### What Was Accomplished

**✅ All Agents Converted to ADK:**
- PlannerAgent now uses FunctionTool with 4 database tools
- CriticAgent now uses FunctionTool with 4 database tools  
- ExplainerAgent now uses FunctionTool with 3 database tools
- All agents have fallback to rule-based logic
- Warning suppression implemented across all agents

**✅ Tools Implementation:**
- PlannerAgent can dynamically query opportunities and similar profiles during planning
- CriticAgent compares plans against successful students in database
- ExplainerAgent provides concrete examples from similar students
- All using `google.adk.tools.FunctionTool` for proper tool integration

**✅ Testing:**
- Plan quality scores: 80-90% consistently
- Iterative refinement working (2-3 iterations)
- All agents tested end-to-end successfully

## 🎯 Recommended Priority Order

Based on current state, here are the most impactful next steps:

### Priority 1: Real Data Integration (Highest Impact) 🌟
**Why**: Current database has a few (10) real anonymized student profiles. Adding upto 50 dramatically improve plan quality.

**Steps**:
1. Collect 50-100 anonymized profiles from r/collegeresults using existing script
2. Clean and validate the data (remove PII, ensure completeness)
3. Replace current sample data with real profiles
4. Test similarity matching with real data

**Estimated Time**: 1-2 weeks  
**Expected Impact**: Better recommendations, more realistic plans, higher quality scores

### Priority 2: Additional Tool Development (Medium Impact)
**Why**: Agents need more sophisticated tools for validation and requirements checking.

**Key Tools to Build**:
1. Course prerequisite validator (prevents invalid sequences)
2. College requirements lookup (ensures alignment with target schools)
3. Plan rigor calculator (scores academic challenge level)

**Estimated Time**: 1 week  
**Expected Impact**: Fewer planning errors, better alignment with colleges

### Priority 3: Orchestrator Agent (Medium-Low Impact)
**Why**: Currently orchestration is manual. ADK orchestrator could improve coordination.

**Note**: This is lower priority because manual orchestration is working well. Focus on data quality first.

**Estimated Time**: 1 week  
**Expected Impact**: More sophisticated agent coordination, better error handling

### Priority 4: Production Features (Future)
**Why**: Only needed when ready to deploy for real users.

**Includes**: Web interface, authentication, deployment, monitoring

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

### Step 8: ✅ Tools Added to All Agents

**Status**: ✅ COMPLETE - All agents now have database tools!

**Implemented Tools by Agent:**

**RetrievalAgent (6 tools):**
- ✅ `search_profiles_tool` - Search by interests
- ✅ `search_by_major_tool` - Search by major
- ✅ `search_by_college_tool` - Search by college
- ✅ `find_similar_profiles_tool` - Similarity matching
- ✅ `get_opportunities_tool` - Get opportunities by grade/interests
- ✅ `get_profile_statistics_tool` - Database statistics

**PlannerAgent (4 tools):**
- ✅ `get_opportunities_tool` - Query opportunities dynamically
- ✅ `find_similar_profiles_tool` - Find patterns from similar students
- ✅ `search_by_college_tool` - See what students targeting colleges did
- ✅ `search_by_major_tool` - Analyze course patterns by major

**CriticAgent (4 tools):**
- ✅ `find_similar_profiles_tool` - Compare against successful students
- ✅ `search_by_college_tool` - Benchmark against college targets
- ✅ `search_by_major_tool` - Validate major-specific requirements
- ✅ `get_profile_statistics_tool` - Understand database benchmarks

**ExplainerAgent (3 tools):**
- ✅ `find_similar_profiles_tool` - Provide success story examples
- ✅ `search_by_college_tool` - Give context about target colleges
- ✅ `get_opportunities_tool` - Mention specific opportunities

**Key Implementation Notes:**
- All tools use `google.adk.tools.FunctionTool` wrapper
- Tools are passed as list to Agent constructor
- Warning suppression added for clean output
- All agents have fallback to rule-based logic

**Next Tools to Add:**
- Course prerequisite validation tool
- College admission requirements lookup tool
- Rigor/competitiveness calculator tool

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

### ✅ Phase 1 Complete (Weeks 1-2)
- ✅ Convert PlannerAgent to ADK with tools
- ✅ Convert CriticAgent to ADK with tools
- ✅ Convert ExplainerAgent to ADK with tools
- ✅ Add database tools to all agents
- ✅ Test all agents work together
- ✅ Suppress ADK warnings

### Immediate Next Steps (Week 3)
- [ ] **Fully suppress remaining warning** - Add warning filter at app entry point
- [ ] **Add course prerequisite validation tool** - Help PlannerAgent validate course sequences
- [ ] **Add college requirements lookup tool** - Query admission requirements for target colleges
- [ ] **Improve error handling** - Better handling when API calls fail
- [ ] **Add logging** - Track agent tool usage and performance

### Short-term (Weeks 3-4) - Real Data Integration
- [ ] **Collect 50-100 real anonymized profiles** from r/collegeresults
- [ ] **Validate and enrich collected data** - Ensure quality and completeness
- [ ] **Update database with real profiles** - Replace synthetic data
- [ ] **Test retrieval with real data** - Verify similarity matching works
- [ ] **Add more opportunities** - Expand opportunities database

### Medium-term (Month 2) - Advanced Features
- [ ] **Create orchestrator agent** - Parent agent coordinating sub-agents
- [ ] **Implement vector search** - Semantic similarity using embeddings
- [ ] **Add agent state management** - Track conversation and iteration history
- [ ] **Improve similarity matching** - Better algorithms for finding similar students
- [ ] **Add caching** - Cache agent responses to reduce API calls

### Long-term (Month 3+) - Production Ready
- [ ] **Migrate to proper database** - PostgreSQL with pgvector for semantic search
- [ ] **Build web interface** - Flask/FastAPI backend + React frontend
- [ ] **Add authentication** - User accounts and saved plans
- [ ] **Deploy to cloud** - AWS/GCP/Heroku deployment
- [ ] **Add monitoring** - Track usage, performance, errors
- [ ] **Create API documentation** - OpenAPI/Swagger docs



## 📚 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Samples](https://github.com/google/adk-samples/tree/main/python/agents)
- [DATA_SOURCES.md](DATA_SOURCES.md) - For finding real profiles
- [SETUP.md](SETUP.md) - For environment setup
- [DATABASE_TOOLS_GUIDE.md](DATABASE_TOOLS_GUIDE.md) - Complete guide on database tools (RetrievalAgent already implements this)

## 💡 Tips

1. **Start Small**: Convert one agent at a time, test thoroughly
2. **Keep Fallbacks**: Always maintain function-based fallbacks
3. **Test Incrementally**: Test each agent before moving to next
4. **Document Changes**: Update documentation as you go
5. **Version Control**: Commit after each agent conversion

## 🎯 Success Metrics

### Phase 1 ✅ (Complete)
- ✅ All 5 agents use ADK
- ✅ All agents have database tools (17 tools total)
- ✅ Warning suppression implemented
- ✅ Plan quality 80-90%
- ✅ End-to-end testing successful

### Phase 2-4 (In Progress)
- [ ] 100+ real anonymized profiles in database
- [ ] Vector search working
- [ ] Orchestrator coordinating agents
- [ ] Additional validation tools (prerequisites, requirements)
- [ ] Web interface deployed

## 📝 Lessons Learned

### Tool Integration
1. **Use `FunctionTool`**, not `Tool` - ADK expects `google.adk.tools.FunctionTool(function)` format
2. **FunctionTool extracts metadata** - Name and description come from function docstrings
3. **Warning suppression** - Add `warnings.catch_warnings()` around `run_agent_sync()` calls
4. **Tool calls are normal** - "non-text parts" warnings just mean agents are using tools successfully

### Agent Design
1. **Keep fallbacks** - All agents have rule-based fallback for when ADK unavailable
2. **Lazy initialization** - Use global instances with getter functions for efficiency
3. **JSON parsing** - Use greedy regex `\{.*\}` not non-greedy `\{.*?\}` for nested JSON
4. **Tool selection** - Give agents access to relevant tools, not all tools

### Performance
1. **Plan quality improved** - 75% → 90% after adding tools to PlannerAgent
2. **Iterations reduced** - With better tools, fewer iterations needed
3. **More specific** - Dynamic queries produce more tailored recommendations
4. **Database is key** - Quality of data directly impacts plan quality

## 🚀 Quick Commands

```bash
# Test the system
python3 test_simple.py

# Test with more profiles
python3 test_profiles.py

# Run all unit tests
python3 tests/run_all_tests.py

# Collect real data (when ready)
python3 scripts/reddit_collector.py

# Activate environment
source venv/bin/activate
```

