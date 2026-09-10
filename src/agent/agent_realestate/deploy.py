#!/usr/bin/env python3
import os
try:
    from dotenv import load_dotenv
    # Load .env from current dir or project/src root
    load_dotenv()
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))
except ImportError:
    pass
import vertexai
from vertexai.agent_engines import AdkApp
from vertexai.preview import reasoning_engines
from agent import root_agent

def main():
    # 구글 클라우드 플랫폼 환경 설정을 주입받아 초기화합니다.
    PROJECT_ID = os.getenv("PROJECT_ID", "explore-ai-c53f5e43")
    REGION = os.getenv("REGION", "us-central1")
    STAGING_BUCKET = os.getenv("GCS_STAGING_BUCKET", f"gs://run-sources-{PROJECT_ID}-{REGION}")

    print(f"Vertex AI 환경 초기화 시작: project='{PROJECT_ID}', region='{REGION}', staging_bucket='{STAGING_BUCKET}'...")
    vertexai.init(
        project=PROJECT_ID,
        location=REGION,
        staging_bucket=STAGING_BUCKET
    )

    print("root_agent를 관리하고 감싸는 AdkApp 인스턴스를 동적으로 구성합니다...")
    app = AdkApp(agent=root_agent)

    print("구글 버텍스 AI 에이전트 엔진(Reasoning Engine)으로 리소스 패키징 및 업로드를 시작합니다...")
    remote_engine = reasoning_engines.ReasoningEngine.create(
        app,
        requirements=[
            "google-adk[a2a]",
            "a2a-sdk",
            "sse-starlette",
            "google-cloud-aiplatform[adk,agent_engines]",
        ],
        display_name="Search Agent Engine (A2A)",
        description="구글 ADK 프레임워크와 제미나이 2.5 플래시, 구글 검색 도구가 긴밀히 통합된 A2A 호환 검색 어시스턴트 에이전트 엔진입니다."
    )

    print("\n==========================================")
    print("🎉 에이전트 엔진 프로덕션 배포 완료!")
    print(f"구글 클라우드 프로젝트 ID: {PROJECT_ID}")
    print(f"리소스 원격 식별코드 (Resource Name): {remote_engine.resource_name}")
    print("==========================================")

    return remote_engine

if __name__ == "__main__":
    main()
