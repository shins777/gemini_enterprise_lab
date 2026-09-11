# 🛠️ Gemini Enterprise Lab - 백엔드 서비스 및 소스 코드 (`src/`)

본 디렉토리는 **Gemini Enterprise** 및 **Google Cloud Vertex AI** 생태계와 연동되는 **맞춤형 Model Context Protocol (MCP) 서버**와 **Vertex AI Reasoning Engine 검색 에이전트**의 프로덕션 수준 소스 코드, 배포 스크립트 및 아키텍처 구현체를 포함하고 있습니다.

---

## 📌 목차

1. [아키텍처 개요](#1-아키텍처-개요)
2. [디렉토리 구성](#2-디렉토리-구성)
3. [모듈 1: 한국 부동산 MCP 서버 (`src/mcp/`)](#3-모듈-1-한국-부동산-mcp-서버-srcmcp)
   - [3.1 데이터 아키텍처 및 20개년 원천 데이터셋](#31-데이터-아키텍처-및-20개년-원천-데이터셋)
   - [3.2 FastMCP 서버 및 제공 도구(Tools)](#32-fastmcp-서버-및-제공-도구tools)
   - [3.3 로컬 테스트 및 구동 가이드](#33-로컬-테스트-및-구동-가이드)
   - [3.4 Cloud Run 컨테이너 빌드 및 배포](#34-cloud-run-컨테이너-빌드-및-배포)
   - [3.5 Gemini Enterprise 에이전트 레지스트리 등록](#35-gemini-enterprise-에이전트-레지스트리-등록)
4. [모듈 2: A2A 호환 검색 에이전트 엔진 (`src/agent/`)](#4-모듈-2-a2a-호환-검색-에이전트-엔진-srcagent)
   - [4.1 Google ADK 및 Gemini 2.5 Flash 코어](#41-google-adk-및-gemini-25-flash-코어)
   - [4.2 Vertex AI Reasoning Engine 원격 배포](#42-vertex-ai-reasoning-engine-원격-배포)
   - [4.3 실시간 스트리밍 대화형 테스트 클라이언트](#43-실시간-스트리밍-대화형-테스트-클라이언트)
   - [4.4 Agent-to-Agent (A2A) 프로토콜 및 로컬 프록시](#44-agent-to-agent-a2a-프로토콜-및-로컬-프록시)
5. [환경 변수 및 설정 가이드](#5-환경-변수-및-설정-가이드)
6. [보안 및 배포 가드레일](#6-보안-및-배포-가드레일)

---

## 1. 아키텍처 개요

`src/` 내의 백엔드 서비스는 엔터프라이즈 생성 AI 연동의 두 가지 핵심 패턴을 실증합니다:

1. **Model Context Protocol (MCP) 서버**: `streamable-http` 및 Server-Sent Events (SSE) 프로토콜을 기반으로 Google Cloud Run에서 실행되며, Gemini Enterprise 에이전트가 20개년 거시경제 및 부동산 시계열 데이터를 도구 형태로 조회할 수 있도록 지원합니다.
2. **A2A (Agent-to-Agent) Reasoning Engine**: Google ADK (Agent Development Kit)와 Gemini 2.5 Flash로 제작되어 Vertex AI Reasoning Engine에 정식 배포된 웹 검색 특화 에이전트로, A2A 표준 인터페이스 및 에이전트 카드를 노출합니다.

```mermaid
flowchart TD
    subgraph "Gemini Enterprise 및 Agent Platform"
        Client[Gemini Enterprise 챗 / 웹 UI]
        Registry[Agent Platform 레지스트리 콘솔]
    end

    subgraph "Cloud Run 서비스 (src/mcp/)"
        MCP_Server["FastMCP 서버 (Streamable-HTTP / SSE)<br/>Port: 8080"]
        CSV[("한국 부동산 20개년 경제 지표<br/>korea_real_estate_20yr_factors.csv")]
        MCP_Server --> CSV
    end

    subgraph "Vertex AI 플랫폼 (src/agent/)"
        ReasoningEngine["Vertex AI Reasoning Engine<br/>Gemini 2.5 Flash + Google ADK"]
        SearchTool["내장 Google Search 원천 색인 도구"]
        ReasoningEngine --> SearchTool
        A2A_Proxy["로컬 A2A 프록시 서버 (FastAPI)<br/>Port: 8000 (.well-known/agent-card.json)"]
    end

    Client -->|1. MCP 도구 호출 (SSE)| MCP_Server
    Client -->|2. A2A 위임 / 원격 스트리밍 질의| ReasoningEngine
    Registry -.->|엔드포인트 등록| MCP_Server
    A2A_Proxy -->|요청 프록시 전달| ReasoningEngine
```

---

## 2. 디렉토리 구성

```text
src/
├── README.md                            # 백엔드 소스 총괄 가이드 문서 (본 문서)
├── .env.example                         # 환경 변수 설정 템플릿
│
├── mcp/                                 # Model Context Protocol (MCP) 서버 모듈
│   ├── README.md                        # MCP 모듈 개요 및 데이터 규격 가이드
│   └── mcp_realestate/                  # 한국 부동산 20개년 요인 분석 MCP 서버
│       ├── server.py                    # FastMCP 서버 및 3개 데이터 추출 도구 구현
│       ├── korea_real_estate_20yr_factors.csv # 표준 영문 헤더로 정리된 2006-2025 데이터셋
│       ├── mcp_config.json              # Gemini Enterprise 에이전트 등록용 메타데이터
│       ├── Dockerfile                   # Cloud Run 컨테이너 빌드 정의 (python:3.11-slim)
│       ├── deploy.sh                    # Cloud Run 자동 빌드 및 배포 스크립트
│       ├── test.py                      # 로컬 MCP 클라이언트 테스트 스크립트
│       └── requirements.txt             # FastMCP, pandas, uvicorn 등 의존성 목록
│
└── agent/                               # 자율형 추론 엔진 및 A2A 에이전트 모듈
    ├── README.md                        # 에이전트 모듈 개요 및 운영 가이드
    └── agent_realestate/                # Vertex AI Reasoning Engine 검색 어시스턴트
        ├── agent.py                     # google_search 도구가 결합된 Google ADK 에이전트
        ├── deploy.py                    # Vertex AI Reasoning Engine 패키징 및 원격 롤아웃
        ├── query_agent.py               # 스트리밍 대화형 테스트 CLI 클라이언트
        ├── a2a_server.py                # 로컬 FastAPI 기반 A2A 호환 프록시 서버
        └── requirements.txt             # google-cloud-aiplatform, google-genai, fastapi 등
```

---

## 3. 모듈 1: 한국 부동산 MCP 서버 (`src/mcp/`)

- **코드 경로**: [`file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate)
- **모듈 가이드**: [`file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/README.md)

### 3.1 데이터 아키텍처 및 20개년 원천 데이터셋

본 서버는 2006년부터 2025년까지의 공식 거시경제 및 주택시장 지표 데이터셋([`korea_real_estate_20yr_factors.csv`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/korea_real_estate_20yr_factors.csv))을 내장하고 있습니다. LLM 에이전트가 오차 없이 도구를 호출할 수 있도록 모든 컬럼 헤더를 표준 영문 스네이크 케이스로 정비했습니다:

| 영문 표준 컬럼명 | 데이터 타입 | 설명 |
| :--- | :--- | :--- |
| `year` | `Integer` | 분석 대상 연도 (2006년 ~ 2025년) |
| `interest_rate` | `Float` | 한국은행 고시 연간 기준금리 (%) |
| `kospi` | `Float` | 기말 기준 종합주가지수 (KOSPI) |
| `seoul_apartment_avg_price` | `Integer` | 서울 권역 아파트 평균 매매 거래 가격 (단위: 만원) |
| `regional_apartment_avg_price` | `Integer` | 지방 5대 광역시 아파트 평균 매매 거래 가격 (단위: 만원) |
| `national_apartment_price_index`| `Float` | 전국 아파트 매매가격 누적 지수 |
| `cpi` | `Float` | 전국 소비자 물가 지수 (CPI) |
| `m2_money_supply` | `Integer` | 기말 기준 광의통화(M2) 총량 (단위: 조원) |
| `unsold_housing` | `Integer` | 전국 미분양 주택 누적 세대수 (단위: 호) |

### 3.2 FastMCP 서버 및 제공 도구(Tools)

[`server.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/server.py)에 FastMCP 프레임워크와 `streamable-http` 전송 규격을 채택하여 3가지 핵심 도구를 제공합니다:

1. **`get_factors_by_year(year: int) -> dict`**: 지정한 특정 연도의 9가지 핵심 거시경제 및 주택시장 지표 집합을 딕셔너리로 즉시 반환합니다.
2. **`get_factors_range(start_year: int, end_year: int) -> list[dict]`**: 시작 연도와 종료 연도를 전달받아 시계열 추이 분석 및 상관관계 도출이 가능하도록 연도별 레코드 배열을 반환합니다.
3. **`get_all_factors() -> list[dict]`**: 20개년 전체 시계열 매트릭스를 반환하여 거시경제 회귀분석 및 장기 차트 생성에 활용됩니다.

### 3.3 로컬 테스트 및 구동 가이드

```bash
cd src/mcp/mcp_realestate

# 1. 의존성 패키지 설치
pip install -r requirements.txt

# 2. FastMCP 서버 로컬 구동 (기본 포트: 8080)
python3 server.py

# 3. 별도 터미널 세션에서 검증용 테스트 클라이언트 실행
python3 test.py
```

### 3.4 Cloud Run 컨테이너 빌드 및 배포

[`Dockerfile`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/Dockerfile)을 기반으로 컨테이너 이미지를 빌드하고 [`deploy.sh`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/deploy.sh)를 통해 Google Cloud Run에 배포합니다:

```bash
cd src/mcp/mcp_realestate

# Google Cloud 인증 토큰 추출 및 환경 변수 설정
export CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)"
export PROJECT_ID="explore-ai-c53f5e43"
export REGION="us-central1"

# Cloud Run 배포 쉘 실행
./deploy.sh
```

**프로덕션 배포 엔드포인트 정보**:
- **URL**: `https://korea-realestate-mcp-277211498595.us-central1.run.app/mcp`
- **Transport**: `SSE` (Server-Sent Events) / `HTTP` (Streamable-HTTP)
- **Region**: `us-central1`

### 3.5 Gemini Enterprise 에이전트 레지스트리 등록

Gemini Enterprise 관리자 콘솔(Agent Platform Admin)에서 배포된 서버를 도구로 등록할 때 [`mcp_config.json`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/mcp_config.json)의 메타데이터를 사용합니다:
- **서버 명칭 (Server Name)**: `Korea Real Estate MCP Server`
- **전송 방식 (Transport)**: `SSE`
- **엔드포인트 주소 (Endpoint)**: `https://korea-realestate-mcp-277211498595.us-central1.run.app/mcp`

---

## 4. 모듈 2: A2A 호환 검색 에이전트 엔진 (`src/agent/`)

- **코드 경로**: [`file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate)
- **모듈 가이드**: [`file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/README.md)

### 4.1 Google ADK 및 Gemini 2.5 Flash 코어

[`agent.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/agent.py)에 정의된 본 모듈은 **Google ADK (Agent Development Kit)**와 **Gemini 2.5 Flash**를 결합한 자율 리서치 에이전트입니다. 원천 검색 색인 접근을 위해 `google_search` 도구가 기본 내장되어 있습니다:

```python
# Google Search 도구가 결합된 ADK 에이전트 코어
agent = Agent(
    model="gemini-2.5-flash",
    system_instruction="You are a professional research assistant specialized in real-time market queries.",
    tools=[google_search],
)
```

본 에이전트는 `to_a2a()` 변환 데코레이터를 적용하여 타 에이전트와의 상호 운용성을 보장합니다.

### 4.2 Vertex AI Reasoning Engine 원격 배포

[`deploy.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/deploy.py) 스크립트는 디렉토리 전체를 바이너리 패키징하여 Google Cloud Storage (GCS)에 스테이징한 뒤 Vertex AI Reasoning Engine 인스턴스로 롤아웃합니다:

```bash
cd src/agent/agent_realestate

# 의존성 패키지 설치
pip install -r requirements.txt

# Vertex AI Reasoning Engine 배포 수행
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
PROJECT_ID="explore-ai-c53f5e43" \
REGION="us-central1" \
GCS_STAGING_BUCKET="gs://run-sources-explore-ai-c53f5e43-us-central1" \
python3 deploy.py
```

**배포 완료된 프로덕션 리소스 식별자**:
- **Resource ID**: `projects/66747595426/locations/us-central1/reasoningEngines/2482267896227561472`
- **구동 위치**: `us-central1`

### 4.3 실시간 스트리밍 대화형 테스트 클라이언트

[`query_agent.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/query_agent.py)를 실행하여 배포된 Reasoning Engine에 실시간 스트리밍 질의를 전송하고 검색 추적 로그를 확인할 수 있습니다:

```bash
cd src/agent/agent_realestate
python3 query_agent.py
```

### 4.4 Agent-to-Agent (A2A) 프로토콜 및 로컬 프록시

[`a2a_server.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/a2a_server.py)는 표준화된 A2A 규격을 충족하는 로컬 FastAPI 프록시를 구동합니다:

```bash
cd src/agent/agent_realestate
python3 a2a_server.py
```
- **로컬 서비스 접근 경로**: `http://localhost:8000`
- **A2A 에이전트 인터페이스 카드**: `http://localhost:8000/.well-known/agent-card.json`

---

## 5. 환경 변수 및 설정 가이드

중앙 환경 변수 설정 템플릿은 [`src/.env.example`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/.env.example)에 정의되어 있습니다. 템플릿을 복사하여 로컬 설정 파일을 구성합니다:

```bash
cp src/.env.example src/.env
```

| 환경 변수명 | 필수 여부 | 기본값 / 예시값 | 설명 |
| :--- | :---: | :--- | :--- |
| `PROJECT_ID` | **필수** | `explore-ai-c53f5e43` | Cloud Run 및 Vertex AI 리소스를 프로비저닝할 타겟 GCP 프로젝트 ID |
| `REGION` | 선택 | `us-central1` | Google Cloud 주요 배포 리전 위치 |
| `GCS_STAGING_BUCKET` | **필수** | `gs://run-sources-explore-ai-c53f5e43-us-central1` | Reasoning Engine 바이너리 빌드 스테이징 버킷 경로 |
| `CLOUDSDK_AUTH_ACCESS_TOKEN`| 선택 | 동적 발급 토큰 | ADC 인증 우회 및 CLI 자동화용 액세스 토큰 |
| `HOST` / `PORT` | 선택 | `0.0.0.0` / `8080` | FastMCP 서버 바인딩 호스트 및 포트 |
| `REASONING_ENGINE_RESOURCE_NAME` | 선택 | `projects/.../reasoningEngines/...` | 배포 완료된 Reasoning Engine 고유 리소스 경로 |
| `A2A_HOST` / `A2A_PORT` | 선택 | `0.0.0.0` / `8000` | 로컬 A2A 프록시 서버 바인딩 호스트 및 포트 |

---

## 6. 보안 및 배포 가드레일

> [!CAUTION]
> **엄격한 비밀정보 격리 및 Git 거버넌스 규칙**  
> [`GEMINI.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/GEMINI.md) 준수 사항:
> 1. **비밀정보 노출 절대 금지**: `src/.env` 또는 개인 액세스 토큰, 서비스 계정 키 파일이 포함된 파일은 절대 스테이징, 커밋 또는 푸시하지 않습니다.
> 2. **`.gitignore` 확인**: 모든 Git 작업 전에 `src/.env` 파일이 정상적으로 Git 추적에서 제외되고 있는지 확인합니다.
> 3. **안전한 템플릿만 커밋**: 플레이스홀더만 포함된 템플릿 파일([`src/.env.example`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/.env.example))만 버전 관리에 포함될 수 있습니다.
> 4. **Cloud Run 인그레스 제어**: 실습 테스트 편의를 위해 비인증 허용(`--allow-unauthenticated`)이 설정되어 있으나, 운영 환경에서는 Cloud IAM OIDC 토큰 인증을 권장합니다.
