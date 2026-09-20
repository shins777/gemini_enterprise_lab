# 🚀 Gemini Enterprise Lab - 통합 마스터 플랫폼 가이드

**Gemini Enterprise Lab** 리포지토리에 오신 것을 환영합니다.  
본 프로젝트는 **Gemini Enterprise (구글 제미나이 엔터프라이즈)** 및 **Google Cloud Vertex AI** 생태계를 기반으로 구축된 핸즈온 랩 실습 가이드, 자율형 AI 에이전트 스킬, 프로덕션 백엔드 마이크로서비스, 그리고 프로그래밍 방식의 엔터프라이즈 API 클라이언트 도구를 집대성한 통합 플랫폼입니다.

노코드 기반의 단일 및 멀티스텝 비즈니스 워크플로를 제작하는 비즈니스 실무자부터, 멀티모달 미디어를 창작하는 크리에이터, Model Context Protocol (MCP) 서버 및 Vertex AI Reasoning Engine(Google ADK / A2A)을 설계·배포하는 클라우드 소프트웨어 엔지니어까지 엔드투엔드(End-to-End) 자산을 제공합니다.

---

## 📌 목차

1. [전체 시스템 아키텍처 개요](#1-전체-시스템-아키텍처-개요)
2. [리포지토리 디렉토리 구조](#2-리포지토리-디렉토리-구조)
3. [4대 핵심 영역 심층 분석](#3-4대-핵심-영역-심층-분석)
   - [영역 1: 핸즈온 랩 실습 커리큘럼 (`ge_lab/`)](#영역-1-핸즈온-랩-실습-커리큘럼-ge_lab)
   - [영역 2: 자율형 워크스페이스 스킬 (`.agents/skills/`)](#영역-2-자율형-워크스페이스-스킬-agentsskills)
   - [영역 3: 백엔드 마이크로서비스 및 분산 에이전트 인프라 (`src/`)](#영역-3-백엔드-마이크로서비스-및-분산-에이전트-인프라-src)
   - [영역 4: 엔터프라이즈 API 제품군 및 EBNF 검색 엔진 (`ge_api/`)](#영역-4-엔터프라이즈-api-제품군-및-ebnf-검색-엔진-ge_api)
4. [상호 연동 매트릭스 (Interoperability Matrix)](#4-상호-연동-매트릭스-interoperability-matrix)
5. [환경 변수 설정 및 Google Cloud 인증](#5-환경-변수-설정-및-google-cloud-인증)
6. [빠른 시작 가이드 (Quick Start)](#6-빠른-시작-가이드-quick-start)
7. [보안 가드레일 및 엔터프라이즈 데이터 프라이버시](#7-보안-가드레일-및-엔터프라이즈-데이터-프라이버시)

---

## 1. 전체 시스템 아키텍처 개요

본 저장소는 Gemini Enterprise 플랫폼의 상호 유기적인 4개 레이어를 통합 지원합니다:

```mermaid
flowchart TD
    subgraph "1. 사용자 인터페이스 및 핸즈온 랩 레이어 (ge_lab/)"
        UI["Gemini Enterprise 웹 어플리케이션<br/>(챗, 인터랙티브 캔버스, Agent Designer, Workflow Builder, 스마트 수신함)"]
        Labs["ge_lab/<br/>(4대 트랙 총 30개 실무 랩 매뉴얼)"]
        UI <--> Labs
    end

    subgraph "2. 자율형 AI 에이전트 스킬 레이어 (.agents/)"
        SkillsCatalog[".agents/skills/<br/>(YAML 규격, 프롬프트 템플릿, 검증 체크리스트 6대 스킬)"]
        AgentCore["AI 에이전트 런타임 / Jetski / Pair-Programming Assistant"]
        SkillsCatalog --> AgentCore
        AgentCore -.->|자동 탐색 및 작업 가이드| UI
    end

    subgraph "3. 엔터프라이즈 API 및 검색 엔진 (ge_api/)"
        StreamAssist["Stream Assist API<br/>(실시간 스트리밍, 사내 그라운딩 인용, 사고과정 모니터링)"]
        EBNF["EBNF 필터 추출 엔진<br/>(Zero-LLM &lt; 5ms 규칙 기반 & Gemini 3.5 Flash Lite)"]
        Discovery["Discovery Engine API<br/>(커스텀 generationSpec 모델 호출)"]
    end

    subgraph "4. 프로덕션 백엔드 인프라 서비스 (src/)"
        MCP["Cloud Run 기반 FastMCP 서버<br/>(한국 부동산 20개년 경제 지표 분석 / Streamable HTTP)"]
        A2A["Vertex AI Reasoning Engine<br/>(Google ADK 기반 A2A 호환 검색 에이전트)"]
    end

    UI -->|도구(Tool) 호출| MCP
    UI -->|전문 에이전트 위임 / 연동| A2A
    StreamAssist --> UI
    EBNF --> Discovery
```

---

## 2. 리포지토리 디렉토리 구조

```text
gemini_enterprise_lab/
├── README.md                            # 리포지토리 마스터 가이드 문서 (본 문서)
├── GEMINI.md                            # 워크스페이스 보안 규칙, 비밀정보 격리 및 스킬 자동 탐색 원칙
│
├── .agents/                             # 자율형 AI 에이전트 워크스페이스 스킬 저장소
│   ├── README.md                        # 스킬 카탈로그 총괄 및 스킬 작성 명세서
│   └── skills/
│       ├── ge-general/                  # Gemini Enterprise 10대 핵심 기능 검증 스킬 (v1.1.0)
│       ├── media-gen/                   # Imagen 3 및 Veo 기반 멀티모달 미디어 생성/편집 스킬 (v1.1.0)
│       ├── nocode-basic/                # 노코드 단일 에이전트 및 워크플로우 에이전트 제작 스킬 (v1.0.0)
│       ├── nocode-advance/              # 수동 빌더 기반 8단계 심화 워크플로우 에이전트 오케스트레이션 스킬 (v1.0.0)
│       ├── agent-realestate/            # Google ADK & A2A 프로토콜 Vertex AI 검색 에이전트 개발/배포 스킬 (v1.0.0)
│       └── build-mcp-server/            # Cloud Run 상의 Streamable HTTP FastMCP 서버 구축/배포 스킬 (v1.0.0)
│
├── ge_lab/                              # 실무 중심 단계별 핸즈온 랩 커리큘럼 (총 30개 랩)
│   ├── README.md                        # 핸즈온 랩 마스터 포털 및 커리큘럼 매트릭스
│   ├── ge_general/                      # 트랙 1: 엔터프라이즈 일반 핵심 기능 (10개 랩)
│   │   ├── ge_general.md                # 10대 핵심 기능 종합 실습 가이드
│   │   └── resources/                   # UI 스크린샷 및 테스트용 데이터
│   ├── media_gen/                       # 트랙 2: 멀티모달 미디어 생성 및 편집 (9개 랩)
│   │   ├── ge_media.md                  # Imagen 3 및 Veo 실무 제작 매뉴얼
│   │   └── resources/                   # 브랜드 자산, 프롬프트 예시 및 UI 화면
│   ├── nocode_basic/                    # 트랙 3: 노코드 및 입문 워크플로우 에이전트 스튜디오 (4개 랩)
│   │   ├── nocode_basic.md              # 대화형 단일 에이전트 & 프롬프트 워크플로우 매뉴얼
│   │   └── resources/                   # 비주얼 빌더 단계별 스크린샷
│   └── nocode_advance/                  # 트랙 4: 심화 워크플로우 에이전트 오케스트레이션 (7개 랩)
│       ├── nocode_advance.md            # 빈 캔버스 수동 조립 기반 부동산 자문 파이프라인 매뉴얼
│       └── resources/                   # 워크플로 노드 스크린샷 및 다이어그램
│
├── ge_api/                              # 엔터프라이즈 API 제품군 및 프로그래밍 도구
│   ├── README.md                        # ge_api 모듈 종합 개요 및 퀵스타트
│   ├── ebnf/                            # 초저지연 EBNF 검색 필터 자동 추출 엔진
│   │   ├── EBNF.py                      # Zero-LLM 순수 규칙 기반 필터 추출기 (< 5ms, 비용 $0)
│   │   └── EBNF_LLM.py                  # Gemini 3.5 Flash Lite 기반 대화형 필터 추출기
│   ├── stream_assist/                   # 실시간 스트리밍 및 엔터프라이즈 사내 데이터 추출 클라이언트
│   │   └── stream_assist.py             # AssistantService.StreamAssist 파이썬 클라이언트
│   └── discovery_engine/                # Discovery Engine 커스텀 모델 호출 모듈
│       └── call_gemini_3_5_flash_lite.py # generationSpec.modelId 지정 유틸리티
│
└── src/                                 # 프로덕션 백엔드 서비스 및 에이전트 소스
    ├── README.md                        # 백엔드 소스 총괄 가이드 및 배포 절차
    ├── .env.example                     # 환경 변수 설정 템플릿
    ├── mcp/                             # Model Context Protocol (MCP) 마이크로서비스
    │   └── mcp_realestate/              # 한국 부동산 20개년 경제 지표 FastMCP 서버 (Cloud Run)
    │       ├── server.py                # Streamable HTTP FastMCP 서버 구현
    │       ├── korea_real_estate_20yr_factors.csv # 2006~2025년 20개년 공공 통계 데이터셋
    │       ├── mcp_config.json          # 에이전트 레지스트리 등록 메타데이터
    │       ├── Dockerfile               # 컨테이너 빌드 정의
    │       └── deploy.sh                # Cloud Run 원클릭 배포 스크립트
    └── agent/                           # Vertex AI Reasoning Engine 에이전트
        └── agent_realestate/            # Google ADK 기반 A2A 호환 검색 에이전트
            ├── agent.py                 # RealEstateSearchAgent 구현 (Google Search 도구)
            ├── deploy.py                # Vertex AI Reasoning Engine 배포 스크립트
            ├── query_agent.py           # 실시간 스트리밍 대화형 CLI 질의 도구
            └── a2a_server.py            # Agent-to-Agent (A2A) 프로토콜 로컬 프록시 서버
```

---

## 3. 4대 핵심 영역 심층 분석

### 영역 1: 핸즈온 랩 실습 커리큘럼 (`ge_lab/`)

- **마스터 포털**: [`ge_lab/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/README.md)
- **대상 독자**: 비즈니스 기획자, 마케팅 실무자, HR 채용 담당자, 리스크 분석가 및 클라우드 솔루션 엔지니어.
- **특징**: 별도 로컬 코딩 없이 Gemini Enterprise 공식 웹 앱에서 100% 브라우저 기반으로 즉시 수행할 수 있는 실무 검증 매뉴얼.

| 실습 트랙 | 매뉴얼 경로 | 랩 수 | 핵심 기술 및 파운데이션 모델 | 주요 학습 내용 |
| :--- | :--- | :---: | :--- | :--- |
| **트랙 1: 일반 핵심 기능** | [`ge_lab/ge_general/ge_general.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/ge_general/ge_general.md) | 10개 랩 | Gemini Core LLM, Google Search, Drive/Gmail/Jira 커넥터, Canvas, Smart Inbox | 논리 추론, 사내 협업 데이터 그라운딩(인용), 전문 에이전트 위임, MCP 도구 연동, 슬라이드 내보내기 |
| **트랙 2: 멀티모달 미디어 제작** | [`ge_lab/media_gen/ge_media.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/media_gen/ge_media.md) | 9개 랩 | Imagen 3 (T2I, Inpainting, Image-to-Image), Veo (T2V, Image-to-Video, Video-to-Video) | 4K 상용 제품 샷, 카피 여백 배너, 다이어그램 인포그래픽, 시네마틱 B-roll, 9:16 모바일 세로형 숏폼 영상 |
| **트랙 3: 노코드 기본 에이전트** | [`ge_lab/nocode_basic/nocode_basic.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_basic/nocode_basic.md) | 4개 랩 | Agent Designer 대화 모드, Builder 모드, 조직 공유/Cron 스케줄링, 1-Prompt 워크플로우 | 채용 평가관 에이전트 생성, 지식(PDF) 바인딩, 뉴스 수집/위협 수준 분기/HITL 승인/Google Drive 자동 저장 |
| **트랙 4: 심화 워크플로 오케스트레이션** | [`ge_lab/nocode_advance/nocode_advance.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_advance/nocode_advance.md) | 7개 랩 | Workflow Builder 빈 캔버스, JSON Schema 구조화, MCP 서버 연동, HITL 승인, Gmail/Drive 액션 | 이메일 송신 트리거(`When an email is sent`), `MCP Realestate`, `Realest_research`, 조건 분기, 사람 승인 후 이메일/드라이브 저장 |

---

### 영역 2: 자율형 워크스페이스 스킬 (`.agents/skills/`)

- **스킬 포털**: [`.agents/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/README.md)
- **대상 독자**: 자율형 AI 에이전트(Jetski, Gemini Pair-Programming Assistant) 및 AI 워크플로 설계자.
- **특징**: 표준화된 Jetski / Agent Skill 명세를 기반으로 AI 에이전트가 도메인 지식과 실행 절차를 자율 로딩하여 작업을 수행.

| 스킬명 | 버전 | 스킬 경로 | 대응 핸즈온 랩 / 구현 리소스 |
| :--- | :---: | :--- | :--- |
| **`ge-general`** | `1.1.0` | [`file:///.agents/skills/ge-general/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/ge-general/SKILL.md) | [`ge_lab/ge_general/ge_general.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/ge_general/ge_general.md) |
| **`media-gen`** | `1.1.0` | [`file:///.agents/skills/media-gen/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/media-gen/SKILL.md) | [`ge_lab/media_gen/ge_media.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/media_gen/ge_media.md) |
| **`nocode-basic`** | `1.0.0` | [`file:///.agents/skills/nocode-basic/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/nocode-basic/SKILL.md) | [`ge_lab/nocode_basic/nocode_basic.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_basic/nocode_basic.md) |
| **`nocode-advance`** | `1.0.0` | [`file:///.agents/skills/nocode-advance/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/nocode-advance/SKILL.md) | [`ge_lab/nocode_advance/nocode_advance.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_advance/nocode_advance.md) |
| **`agent-realestate`** | `1.0.0` | [`file:///.agents/skills/agent-realestate/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/agent-realestate/SKILL.md) | [`src/agent/agent_realestate/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/README.md) |
| **`build-mcp-server`**| `1.0.0` | [`file:///.agents/skills/build-mcp-server/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/build-mcp-server/SKILL.md) | [`src/mcp/mcp_realestate/deploy.sh`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/deploy.sh) |

---

### 영역 3: 백엔드 마이크로서비스 및 분산 에이전트 인프라 (`src/`)

- **백엔드 포털**: [`src/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/README.md)
- **대상 독자**: 클라우드 아키텍트, 백엔드 개발자 및 엔터프라이즈 AI 플랫폼 엔지니어.
- **특징**: 기업의 내부 데이터와 외부 API를 Gemini Enterprise 및 Vertex AI에 연결하는 프로덕션 마이크로서비스.

#### 1. 한국 부동산 20개년 FastMCP 서버 ([`src/mcp/mcp_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate))
- **프로토콜 및 프레임워크**: `FastMCP` (Streamable HTTP / SSE 전송 규격 지원).
- **데이터셋**: 2006년부터 2025년까지의 공식 통계 20개년 데이터셋([`korea_real_estate_20yr_factors.csv`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/korea_real_estate_20yr_factors.csv)).
  - 포함 지표: 한국은행 기준금리, 전국/서울 아파트 평균 매매가격, 전국 주택담보대출 잔액, 전국 주택건설 인허가 실적, 전국 미분양 주택수, 광의통화(M2), 전국 아파트 매매가격지수.
- **제공 도구(Tools)**:
  - `get_factors_by_year(year: int)`: 특정 단일 연도의 7대 거시경제 및 부동산 지표 조회.
  - `get_factors_range(start_year: int, end_year: int)`: 연도 구간별 시계열 데이터 조회.
  - `get_all_factors()`: 2006~2025년 전체 20개년 데이터셋 반환.
- **배포 엔드포인트**: `https://korea-realestate-mcp-277211498595.us-central1.run.app/mcp` (Google Cloud Run).

#### 2. Vertex AI Reasoning Engine 검색 에이전트 ([`src/agent/agent_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate))
- **프레임워크 및 모델**: Google ADK (Agent Development Kit) & Gemini 2.5 Flash.
- **표준 및 인터페이스**: 구글 검색 도구(`google_search`) 내장 및 Agent-to-Agent (A2A) 표준 래퍼(`to_a2a()`).
- **배포 인스턴스**: `projects/66747595426/locations/us-central1/reasoningEngines/2482267896227561472`.
- **지원 도구**:
  - 실시간 스트리밍 대화형 질의 CLI: [`query_agent.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/query_agent.py)
  - 원격 배포 관리 스크립트: [`deploy.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/deploy.py)
  - 로컬 Agent-to-Agent 프록시 서버: [`a2a_server.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/a2a_server.py)

---

### 영역 4: 엔터프라이즈 API 제품군 및 EBNF 검색 엔진 (`ge_api/`)

- **API 포털**: [`ge_api/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/README.md)
- **대상 독자**: 풀스택 개발자, 검색 엔진 엔지니어 및 API 연동 담당자.
- **특징**: Discovery Engine 및 AIP-160 표준 검색 필터링을 위한 초고속 파이썬 라이브러리 및 실시간 스트리밍 클라이언트.

#### 1. EBNF 필터 자동 추출 엔진 ([`ge_api/ebnf/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/ebnf))
- **`EBNF.py`**: Zero-LLM 순수 정규식 및 규칙 기반 필터 추출기 (< 5ms, 비용 $0).
  - 작성자, 연도/날짜, 파일 확장자(PDF, DOCX 등), 카테고리를 AIP-160 필터 표현식으로 고속 변환.
- **`EBNF_LLM.py`**: Gemini 3.5 Flash Lite 기반 복합 의도 지속 대화형 필터 추출기.
  - 1초 이내 초저지연 처리 및 실시간 레이턴시 프로파일링 제공.

#### 2. 실시간 그라운딩 Stream Assist 클라이언트 ([`ge_api/stream_assist/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/stream_assist))
- Gemini Enterprise `AssistantService.StreamAssist` 프로토콜 기반 파이썬 클라이언트.
- 토큰 실시간 스트리밍, 사내 데이터 그라운딩 출처(Citation) 매핑, 모델 사고 과정(Thoughts Step) 실시간 모니터링 지원.

#### 3. Discovery Engine 커스텀 모델 호출 모듈 ([`ge_api/discovery_engine/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/discovery_engine))
- `generationSpec.modelId`를 직접 지정하여 호출하는 Discovery Engine 특화 모듈.

---

## 4. 상호 연동 매트릭스 (Interoperability Matrix)

각 구성 요소가 상호 간에 어떻게 유기적으로 연동되는지 보여주는 매핑 테이블입니다:

| 사용자 핸즈온 랩 (`ge_lab/`) | 자동화 스킬 (`.agents/skills/`) | 백엔드 서비스 (`src/`) | 프로그래밍 API (`ge_api/`) |
| :--- | :--- | :--- | :--- |
| **트랙 1: 일반 기능** (`ge_general.md`) | `ge-general` | FastMCP 부동산 서버 (`mcp_realestate`) | `stream_assist.py`, `EBNF.py` |
| **트랙 2: 미디어 제작** (`ge_media.md`) | `media-gen` | - | - |
| **트랙 3: 노코드 기초** (`nocode_basic.md`) | `nocode-basic` | - | - |
| **트랙 4: 노코드 심화** (`nocode_advance.md`) | `nocode-advance` | FastMCP (`mcp_realestate`), Reasoning Engine (`agent_realestate`) | - |
| **백엔드 배포 가이드** (`src/README.md`) | `build-mcp-server`, `agent-realestate` | Cloud Run MCP 컨테이너, Vertex AI Reasoning Engine | `discovery_engine` |

---

## 5. 환경 변수 설정 및 Google Cloud 인증

### 5.1 중앙 환경 설정 템플릿
[`src/.env.example`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/.env.example)을 복사하여 로컬 환경 설정 파일(`.env`)을 생성합니다:

```bash
# 설정 템플릿 복사 (주의: .env 파일은 절대 커밋하지 마십시오)
cp src/.env.example src/.env
```

| 주요 환경 변수명 | 권장값 / 예시 | 상세 용도 |
| :--- | :--- | :--- |
| `PROJECT_ID` | `explore-ai-c53f5e43` | Cloud Run 및 Vertex AI 리소스를 구동할 대상 GCP 프로젝트 ID |
| `REGION` | `us-central1` | Google Cloud 주요 배포 리전 |
| `GCS_STAGING_BUCKET` | `gs://run-sources-explore-ai-c53f5e43-us-central1` | Reasoning Engine 패키징 아티팩트 스테이징 버킷 |
| `HOST` / `PORT` | `0.0.0.0` / `8080` | 로컬 FastMCP 서버 바인딩 호스트 및 포트 |
| `A2A_HOST` / `A2A_PORT` | `0.0.0.0` / `8000` | 로컬 Agent-to-Agent 프록시 서버 바인딩 호스트 및 포트 |

### 5.2 Google Cloud 인증 (ADC) 설정
로컬 터미널에서 Google Cloud Application Default Credentials (ADC)를 활성화합니다:

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project explore-ai-c53f5e43
```

---

## 6. 빠른 시작 가이드 (Quick Start)

### 단계 1: Zero-LLM EBNF 검색 필터 추출 (< 5ms)
```bash
python3 ge_api/ebnf/EBNF.py "2025년도에 홍길동이 작성한 AI 규제 보고서 PDF 문서를 찾아줘."
```

### 단계 2: Gemini Enterprise 실시간 스트리밍 질의
```bash
python3 ge_api/stream_assist/stream_assist.py "국내외 생성형 AI 도입 전략을 2줄로 요약해줘."
```

### 단계 3: 로컬 FastMCP 부동산 서버 실행 및 검증
```bash
cd src/mcp/mcp_realestate
pip install -r requirements.txt
python3 server.py
```

### 단계 4: Vertex AI Reasoning Engine 원격 질의 테스트
```bash
cd src/agent/agent_realestate
pip install -r requirements.txt
python3 query_agent.py
```

### 단계 5: 핸즈온 랩 실습 진행
[`ge_lab/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/README.md) 포털에서 원하는 트랙을 선택하여 실습을 진행합니다:
- **엔터프라이즈 일반 기능 실습**: [`ge_lab/ge_general/ge_general.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/ge_general/ge_general.md)
- **멀티모달 이미지 및 비디오 제작**: [`ge_lab/media_gen/ge_media.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/media_gen/ge_media.md)
- **노코드 기초 에이전트 스튜디오**: [`ge_lab/nocode_basic/nocode_basic.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_basic/nocode_basic.md)
- **심화 워크플로우 에이전트 오케스트레이션**: [`ge_lab/nocode_advance/nocode_advance.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_advance/nocode_advance.md)

---

## 7. 보안 가드레일 및 엔터프라이즈 데이터 프라이버시

> [!IMPORTANT]
> **엄격한 비밀정보 보호 및 엔터프라이즈 컴플라이언스 원칙**  
> [`GEMINI.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/GEMINI.md) 준수 가이드라인:
> 1. **비밀정보 유출 절대 방지**: `.env` 파일, 개인 API 키(`GOOGLE_API_KEY`, `GEMINI_API_KEY`), 서비스 계정 비공개 키, 액세스 토큰은 절대로 스테이징하거나 커밋/푸시하지 않습니다.
> 2. **안전한 템플릿만 커밋 허용**: 플레이스홀더 값만 담긴 예시 템플릿(예: `.env.example`)만 버전 관리에 포함됩니다.
> 3. **엔터프라이즈 프라이버시 경계**: Gemini Enterprise 웹 앱 내에서 입력된 모든 프롬프트, 사내 업로드 문서 및 지식 파일은 Google 기본 파운데이션 모델 재학습에 일체 활용되지 않으며 테넌트 내에서 격리 보호됩니다.
> 4. **사전 점검 필수**: Git 커밋 또는 푸시 작업을 진행하기 전 반드시 `git status`와 스테이징 변경점을 점검하여 민감한 정보가 포함되어 있지 않은지 확인하십시오.