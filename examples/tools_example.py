"""
Example: How Database Tools Work with ADK Agents

This demonstrates the difference between:
1. Manual database queries (current)
2. Agent with tools (Week 3)
"""
from src.tools.database import get_database
from src.agents.profile_agent import normalize


def example_1_manual_query():
    """
    Example 1: Manual database query (current approach)
    You have to do all the work yourself.
    """
    print("=" * 60)
    print("Example 1: Manual Database Query")
    print("=" * 60)
    
    # Step 1: You query the database
    db = get_database()
    profiles = db.search_by_interests(["Computer Science", "Mathematics"], top_k=5)
    
    # Step 2: You filter results
    mit_profiles = [p for p in profiles if "MIT" in p.target_colleges]
    
    # Step 3: You format the results
    print(f"Found {len(mit_profiles)} profiles interested in CS/Math targeting MIT")
    for profile in mit_profiles:
        print(f"  - {profile.name}: {', '.join(profile.target_majors)}")
    
    print("\n❌ Problem: You have to write all the query logic yourself")


def example_2_with_tools():
    """
    Example 2: Agent with tools (Week 3 approach)
    Agent queries database automatically.
    """
    print("\n" + "=" * 60)
    print("Example 2: Agent with Database Tools")
    print("=" * 60)
    
    # This is what it will look like (after implementing tools)
    print("""
    # Create agent with tools
    agent = get_retrieval_agent()  # Has search_profiles tool
    
    # Agent queries database itself
    result = agent.run('''
        Find students interested in Computer Science and Math 
        who are targeting MIT. Show me their majors and GPAs.
    ''')
    
    # Agent automatically:
    # 1. Calls search_profiles_tool("Computer Science, Math")
    # 2. Filters for MIT
    # 3. Formats the results
    # 4. Returns answer
    
    print(result)
    """)
    
    print("✅ Benefit: Agent handles all the query logic!")


def example_3_tool_workflow():
    """
    Example 3: How tools work step-by-step
    """
    print("\n" + "=" * 60)
    print("Example 3: Tool Workflow")
    print("=" * 60)
    
    print("""
    User Query: "Find similar students to me"
    
    Agent Process:
    ┌─────────────────────────────────────────┐
    │ 1. Agent receives query                │
    │ 2. Agent decides: "I need to search"   │
    │ 3. Agent calls: search_profiles_tool() │
    │    └─> Tool queries database           │
    │    └─> Tool returns results            │
    │ 4. Agent processes results             │
    │ 5. Agent calls: find_similar_profiles()│
    │    └─> Tool calculates similarity      │
    │    └─> Tool returns top matches        │
    │ 6. Agent synthesizes all information   │
    │ 7. Agent returns final answer          │
    └─────────────────────────────────────────┘
    
    You don't write any of this - the agent does it!
    """)


def example_4_real_use_case():
    """
    Example 4: Real use case comparison
    """
    print("\n" + "=" * 60)
    print("Example 4: Real Use Case")
    print("=" * 60)
    
    print("""
    SCENARIO: Student asks "What did CS students who got into MIT do?"
    
    WITHOUT TOOLS (Current):
    ┌──────────────────────────────────────┐
    │ You write code:                      │
    │ 1. db.search_by_major("CS")         │
    │ 2. Filter for MIT                   │
    │ 3. Extract courses, ECs, GPA        │
    │ 4. Format results                   │
    │ 5. Pass to agent                    │
    └──────────────────────────────────────┘
    ❌ You do all the work
    
    WITH TOOLS (Week 3):
    ┌──────────────────────────────────────┐
    │ You just ask:                        │
    │ agent.run("What did CS students...") │
    │                                      │
    │ Agent automatically:                 │
    │ 1. Calls search_by_major_tool("CS") │
    │ 2. Calls search_by_college_tool("MIT")│
    │ 3. Analyzes results                  │
    │ 4. Returns answer                   │
    └──────────────────────────────────────┘
    ✅ Agent does all the work
    """)


def main():
    """Run all examples."""
    example_1_manual_query()
    example_2_with_tools()
    example_3_tool_workflow()
    example_4_real_use_case()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
    Database Tools allow agents to:
    
    1. Query database automatically
       - No need to pre-fetch data
       - Agent decides what to search
    
    2. Handle natural language
       - User: "Find students like me"
       - Agent translates to database queries
    
    3. Chain operations
       - Search → Filter → Analyze → Return
       - All done by agent
    
    4. Make intelligent decisions
       - Agent can refine searches
       - Agent can combine multiple queries
       - Agent adapts to results
    
    Next: See DATABASE_TOOLS_GUIDE.md for implementation details
    """)


if __name__ == "__main__":
    main()

