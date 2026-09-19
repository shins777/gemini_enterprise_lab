#!/usr/bin/env python3
import os
import json
try:
    from dotenv import load_dotenv
    load_dotenv()
    load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env")))
except ImportError:
    pass
import vertexai
from vertexai.preview import reasoning_engines

# 배포 완료한 Vertex AI Reasoning Engine의 고유 리소스 식별 경로를 환경 변수(REASONING_ENGINE_RESOURCE_NAME)로 지정합니다.
DEFAULT_RESOURCE_NAME = "projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_REASONING_ENGINE_ID"

def query_agent(message: str, user_id: str = "user_1"):
    # 환경 변수로부터 원격 인스턴스 경로와 프로젝트 설정을 수집하고 차선책으로 기본 상수를 연동합니다.
    resource_name = os.getenv("REASONING_ENGINE_RESOURCE_NAME") or DEFAULT_RESOURCE_NAME
    project_id = os.getenv("PROJECT_ID") or "your-gcp-project-id"
    region = os.getenv("REGION") or "us-central1"

    # Vertex AI 프레임워크 세션을 가동 프로젝트 정보와 리전 정보로 개시합니다.
    vertexai.init(project=project_id, location=region)
    engine = reasoning_engines.ReasoningEngine(resource_name)

    # 개별 유저 세션을 식별할 수 있는 메모리 보존형 임시 컨텍스트를 할당받습니다.
    session = engine.create_session(user_id=user_id)
    session_id = session["id"]

    print(f"원격 에이전트 엔진 세션 생성 완료 (ID: {session_id})")
    print(f"사용자 입력 질문: {message}\n")

    # 원격 백엔드의 stream_query 인터페이스를 개방하여 제미나이가 구글 검색 후 답변을 조립 및 도출해내는 전 과정을 청크 단위로 스트리밍 수신합니다.
    response_chunks = engine.execution_api_client.stream_query_reasoning_engine(
        request={
            "name": engine.resource_name,
            "class_method": "stream_query",
            "input": {
                "user_id": user_id,
                "session_id": session_id,
                "message": message
            }
        }
    )

    # 수신된 JSON 스트리밍 청크 패킷들을 바이트 변환 후 파싱하여 디텍팅된 일반 텍스트 문구들을 실시간 화면에 찍어줍니다.
    for chunk in response_chunks:
        data = json.loads(chunk.data.decode("utf-8"))
        if "content" in data and "parts" in data["content"]:
            for part in data["content"]["parts"]:
                if "text" in part:
                    print(part["text"], end="", flush=True)
    print()

if __name__ == "__main__":
    # 기본 테스트로 배포된 에이전트가 실시간 구글 검색을 활용해 '최근 부동산 시장 동향 및 전망'에 대해 분석하도록 질의합니다.
    query_agent("최근 대한민국 부동산 시장(서울 및 수도권·지방 아파트 매매/전세 동향, 금리 및 대출 규제 영향)의 최신 흐름과 향후 전망에 대해 상세히 요약해 줘.")
