from google.adk.agents.llm_agent import Agent
from analyzer_agent.analyzer_tool import analyze_sow_with_rag

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    description="Orchestrates presales SOW analysis",
    instruction="""
When a user provides an SOW:
1. Call analyze_sow_with_rag
2. Use the structured output to prepare client clarification questions
""",
    tools=[analyze_sow_with_rag]
)
