from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Create the search agent using ADK Agent class
root_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    description='A search agent that gathers detailed information on any user request using Google Search.',
    instruction='You are a helpful Search Assistant. Use the google_search tool to look up detailed information on the user\'s query, analyze the search results, and explain them in detail to the user.',
    tools=[google_search]
)

# Convert ADK agent to A2A (Agent-to-Agent) compatible application
a2a_app = to_a2a(root_agent)
