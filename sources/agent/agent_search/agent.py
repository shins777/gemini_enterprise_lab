from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from google.adk.a2a.utils.agent_to_a2a import to_a2a

# Google ADK Agent 클래스를 사용하여 검색 전용 에이전트를 정의합니다.
# 제미나이 2.5 플래시 모델을 기반으로 하며 구글 검색 도구가 직접 바인딩되어 탑재됩니다.
root_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    description='A search agent that gathers detailed information on any user request using Google Search.',
    instruction='You are a helpful Search Assistant. Use the google_search tool to look up detailed information on the user\'s query, analyze the search results, and explain them in detail to the user.',
    tools=[google_search]
)

# 생성된 ADK 에이전트를 차세대 Agent-to-Agent (A2A) 호환 프로토콜 웹 어플리케이션으로 마이그레이션 및 래핑합니다.
a2a_app = to_a2a(root_agent)
