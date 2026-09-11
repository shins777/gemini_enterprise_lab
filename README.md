# 🚀 Gemini Enterprise Lab - 통합 마스터 플랫폼 가이드

**Gemini Enterprise Lab** 리포지토리에 오신 것을 환영합니다.  
본 프로젝트는 **Gemini Enterprise (구글 제미나이 엔터프라이즈)** 및 **Google Cloud Vertex AI** 생태계를 기반으로 구축된 핸즈온 랩 실습 가이드, 자율형 AI 에이전트 스킬, 프로덕션 백엔드 마이크로서비스, 그리고 프로그래밍 방식의 엔터프라이즈 API 클라이언트 도구를 집대성한 통합 플랫폼입니다.

노코드 기반의 AI 업무 에이전트를 제작하는 비즈니스 실무자부터, 멀티모달 미디어를 창작하는 마케터, Model Context Protocol (MCP) 서버 및 Vertex AI Reasoning Engine을 설계·배포하는 클라우드 소프트웨어 엔지니어까지 엔드투엔드(End-to-End) 자산을 제공합니다.

---

## 📌 목차

1. [전체 시스템 아키텍처 개요](#1-전체-시스템-아키텍처-개요)
2. [리포지토리 디렉토리 구조](#2-리포지토리-디렉토리-구조)
3. [4대 핵심 영역 심층 분석](#3-4대-핵심-영역-심층-분석)
   - [영역 1: 핸즈온 랩 실습 커리큘럼 (`ge_lab/`)](#영역-1-핸즈온-랩-실습-커리큘럼-ge_lab)
   - [영역 2: 자율형 워크스페이스 스킬 (`.agents/`)](#영역-2-자율형-워크스페이스-스킬-agents)
   - [영역 3: 백엔드 마이크로서비스 및 MCP 서버 (`src/`)](#영역-3-백엔드-마이크로서비스-및-mcp-서버-src)
   - [영역 4: 엔터프라이즈 API 제품군 및 EBNF 엔진 (`ge_api/`)](#영역-4-엔터프라이즈-api-제품군-및-ebnf-엔진-ge_api)
4. [환경 변수 설정 및 Google Cloud 인증](#4-환경-변수-설정-및-google-cloud-인증)
5. [빠른 시작 가이드 (Quick Start)](#5-빠른-시작-가이드-quick-start)
6. [보안 가드레일 및 엔터프라이즈 데이터 프라이버시](#6-보안-가드레일-및-엔터프라이즈-데이터-프라이버시)

---

## 1. 전체 시스템 아키텍처 개요

본 저장소는 Gemini Enterprise 플랫폼의 유기적인 4개 레이어를 통합 지원합니다:

```mermaid
flowchart TD
    subgraph "1. 사용자 인터페이스 및 웹 앱 레이어"
        UI["Gemini Enterprise 웹 어플리케이션<br/>(챗, 인터랙티브 캔버스, Agent Designer, 스마트 수신함)"]
        Labs["ge_lab/<br/>(실무 핸즈온 랩 매뉴얼)"]
    end

    subgraph "2. 자율형 AI 에이전트 스킬 레이어 (.agents/)"
        SkillsCatalog[".agents/skills/<br/>YAML 규격, 프롬프트 템플릿 및 검증 체크리스트"]
        AgentCore["AI 에이전트 런타임 / Jetski"]
        SkillsCatalog --> AgentCore
    end

    subgraph "3. 엔터프라이즈 API 및 검색 엔진 (ge_api/)"
        StreamAssist["Stream Assist API<br/>(실시간 스트리밍 & 사내 그라운딩 인용)"]
        EBNF["EBNF 필터 추출 엔진<br/>(Zero-LLM < 5ms 및 초저지연 Flash Lite)"]
        Discovery["Discovery Engine API<br/>(커스텀 generationSpec 모델 호출)"]
    end

    subgraph "4. 프로덕션 백엔드 인프라 서비스 (src/)"
        MCP["Cloud Run 기반 FastMCP 서버<br/>(한국 부동산 20개년 경제 지표 분석)"]
        A2A["Vertex AI Reasoning Engine<br/>(A2A 호환 검색 에이전트 & Google ADK)"]
    end

    Labs -.->|사용자 랩 실습 가이드 제공| UI
    AgentCore -->|자율 워크플로우 자동화 지원| UI
    UI -->|도구(Tool) 호출| MCP
    UI -->|에이전트 위임| A2A
    StreamAssist --> UI
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
│       ├── ge-general/                  # Gemini Enterprise 10대 핵심 기능 검증 스킬
│       ├── media-gen/                   # Imagen 3 및 Veo 기반 멀티모달 미디어 생성/편집
│       ├── nocode-agent/                # 노코드 단일 에이전트 및 멀티스텝 워크플로우 에이전트
│       └── build-mcp-server/            # Cloud Run 상의 Streamable HTTP MCP 서버 배포
│
├── ge_lab/                              # 실무 중심 단계별 핸즈온 랩 커리큘럼
│   ├── README.md                        # 핸즈온 랩 마스터 포털 및 커리큘럼 매트릭스
│   ├── ge_general/                      # 트랙 1: 엔터프라이즈 일반 핵심 기능 (10개 랩)
│   ├── media_gen/                       # 트랙 2: 멀티모달 미디어 생성 및 편집 (9개 랩)
│   ├── nocode_agent/                    # 트랙 3: 노코드 및 워크플로우 에이전트 스튜디오 (4개 랩)
│   └── agent_platform/                  # 트랙 4: 에이전트 플랫폼 및 인프라 연동 확장
│
├── ge_api/                              # 엔터프라이즈 API 제품군 및 프로그래밍 도구
│   ├── README.md                        # ge_api 모듈 종합 개요 및 퀵스타트
│   ├── ebnf/                            # 초저지연 EBNF 검색 필터 자동 추출 엔진
│   ├── stream_assist/                   # 실시간 스트리밍 및 엔터프라이즈 사내 데이터 추출 클라이언트
│   └── discovery_engine/                # Discovery Engine 커스텀 모델 호출 모듈
│
└── src/                                 # 프로덕션 백엔드 서비스 및 에이전트 소스
    ├── README.md                        # 백엔드 소스 총괄 가이드 및 배포 절차
    ├── .env.example                     # 환경 변수 설정 템플릿
    ├── mcp/                             # Model Context Protocol (MCP) 마이크로서비스
    │   └── mcp_realestate/              # 한국 부동산 20개년 요인 분석 FastMCP 서버 (Cloud Run)
    └── agent/                           # Vertex AI Reasoning Engine 검색 에이전트
        └── agent_realestate/            # Google ADK 기반 A2A 호환 검색 에이전트
```

---

## 3. 4대 핵심 영역 심층 분석

### 영역 1: 핸즈온 랩 실습 커리큘럼 (`ge_lab/`)

- **포털 가이드**: [`ge_lab/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/README.md)
- **대상 독자**: 비즈니스 기획자, 마케팅 실무자, HR 채용 담당자, 솔루션 엔지니어.
- **특징**: 별도 로컬 코딩 없이 브라우저의 Gemini Enterprise 공식 앱에서 즉시 수행 가능한 100% 웹 기반 실습 매뉴얼.

| 실습 트랙 | 매뉴얼 경로 | 모듈 수 | 핵심 기술 및 파운데이션 모델 |
| :--- | :--- | :---: | :--- |
| **엔터프라이즈 일반 기능** | [`ge_lab/ge_general/ge_general.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/ge_general/ge_general.md) | 10개 랩 | Direct Q&A, Web Grounding, 사내 커넥터 (Drive/Gmail/Jira), 인터랙티브 캔버스, 스마트 수신함, MCP |
| **멀티모달 미디어 제작** | [`ge_lab/media_gen/ge_media.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/media_gen/ge_media.md) | 9개 랩 | Imagen 3 (제품 샷, 대화형 인페인팅, 인포그래픽, 배너), Veo (B-roll, 모션 비디오, 9:16 세로형 영상) |
| **노코드 에이전트 스튜디오** | [`ge_lab/nocode_agent/nocode_agent.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_agent/nocode_agent.md) | 4개 랩 | Agent Designer, 비주얼 빌더, Cron 스케줄링, 위협 수준 조건 분기, 사람 필수 승인(HITL), Google Drive 저장 |

---

### 영역 2: 자율형 워크스페이스 스킬 (`.agents/`)

- **포털 가이드**: [`.agents/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/README.md)
- **대상 독자**: 자율형 AI 코딩 에이전트 (Jetski, DeepMind 에이전트 도구) 및 AI 어시스턴트.
- **특징**: 표준화된 Jetski / Agent Skill 명세를 기반으로 AI 에이전트가 자율적으로 도메인 지식을 로딩하여 사용자 작업을 자동화.

에이전트는 `.agents/skills/*/*/SKILL.md`를 재귀 탐색하여 필요한 스킬을 자동으로 호출합니다:
- [**`ge-general`**](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/ge-general/SKILL.md): 10대 핵심 기능 검증 시나리오 및 체크리스트.
- [**`media-gen`**](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/media-gen/SKILL.md): 시각적 연출을 위한 조명, 카메라 렌즈, 프롬프트 엔지니어링 지침.
- [**`nocode-agent`**](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/nocode-agent/SKILL.md): 단일 에이전트 및 다단계 워크플로우 에이전트 설계 스펙.
- [**`build-mcp-server`**](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/build-mcp-server/SKILL.md): Cloud Run 컨테이너 빌드 및 배포 절차.

---

### 영역 3: 백엔드 마이크로서비스 및 MCP 서버 (`src/`)

- **포털 가이드**: [`src/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/README.md)
- **대상 독자**: 클라우드 엔지니어, 백엔드 개발자 및 엔터프라이즈 AI 시스템 아키텍트.
- **특징**: 기업 내부 데이터와 외부 도구를 Gemini Enterprise 및 Vertex AI에 연결하는 프로덕션 레디 마이크로서비스.

#### 1. 한국 부동산 20개년 MCP 서버 ([`src/mcp/mcp_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate))
- **프레임워크**: `FastMCP` (`streamable-http` / SSE 전송 규격).
- **데이터셋**: 2006년부터 2025년까지의 공식 거시경제 및 아파트 매매 지표 20개년 데이터셋([`korea_real_estate_20yr_factors.csv`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/mcp/mcp_realestate/korea_real_estate_20yr_factors.csv)).
- **제공 도구**: `get_factors_by_year`, `get_factors_range`, `get_all_factors`.
- **배포 주소**: `https://korea-realestate-mcp-277211498595.us-central1.run.app/mcp` (Google Cloud Run).

#### 2. Vertex AI Reasoning Engine 검색 에이전트 ([`src/agent/agent_realestate/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate))
- **프레임워크**: Google ADK (Agent Development Kit) & Gemini 2.5 Flash.
- **기능 및 표준**: 구글 검색 도구 내장 및 Agent-to-Agent (A2A) 표준 래퍼(`to_a2a()`).
- **배포 인스턴스**: `projects/66747595426/locations/us-central1/reasoningEngines/2482267896227561472`.
- **클라이언트 도구**: 실시간 스트리밍 대화형 CLI([`query_agent.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/query_agent.py)) 및 로컬 A2A 프록시 서버([`a2a_server.py`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/agent/agent_realestate/a2a_server.py)).

---

### 영역 4: 엔터프라이즈 API 제품군 및 EBNF 엔진 (`ge_api/`)

- **포털 가이드**: [`ge_api/README.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/README.md)
- **대상 독자**: 풀스택 개발자, 검색 엔지니어 및 API 연동 담당자.
- **특징**: Discovery Engine 및 AIP-160 검색 필터링을 위한 초고속 파이썬 라이브러리.

#### 1. EBNF 필터 자동 추출 엔진 ([`ge_api/ebnf/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/ebnf))
- **`EBNF.py`**: Zero-LLM 순수 규칙 기반 초저지연 필터 추출기 (< 5ms, 비용 $0).
- **`EBNF_LLM.py`**: Gemini 3.5 Flash Lite 기반 1초 이내 처리 지속 대화형 추출기 (실시간 레이턴시 측정).

#### 2. 실시간 그라운딩 Stream Assist 클라이언트 ([`ge_api/stream_assist/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/stream_assist))
- Gemini Enterprise `AssistantService.StreamAssist` 파이썬 클라이언트로 실시간 응답 스트리밍, 사내 데이터 인용(Citation), 모델 사고 과정(Thoughts) 모니터링 지원.

#### 3. Discovery Engine 커스텀 모델 호출 모듈 ([`ge_api/discovery_engine/`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_api/discovery_engine))
- `generationSpec.modelId`를 직접 지정하여 호출하는 특화 유틸리티.

---

## 4. 환경 변수 설정 및 Google Cloud 인증

### 4.1 중앙 환경 설정 템플릿
[`src/.env.example`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/src/.env.example)을 복사하여 로컬 환경 설정 파일(`.env`)을 생성합니다:

```bash
# 설정 템플릿 복사 (주의: .env 파일은 절대 커밋하지 마십시오)
cp src/.env.example src/.env
```

| 주요 환경 변수명 | 기본값 / 예시 | 용도 |
| :--- | :--- | :--- |
| `PROJECT_ID` | `explore-ai-c53f5e43` | Cloud Run 및 Vertex AI 리소스를 구동할 대상 GCP 프로젝트 ID |
| `REGION` | `us-central1` | Google Cloud 주 배포 리전 |
| `GCS_STAGING_BUCKET` | `gs://run-sources-explore-ai-c53f5e43-us-central1` | Reasoning Engine 빌드용 바이너리 아티팩트 스테이징 버킷 |
| `HOST` / `PORT` | `0.0.0.0` / `8080` | 로컬 FastMCP 서버 바인딩 호스트 및 포트 |
| `A2A_HOST` / `A2A_PORT` | `0.0.0.0` / `8000` | 로컬 A2A 프록시 서버 바인딩 호스트 및 포트 |

### 4.2 Google Cloud 인증 (ADC) 설정
터미널에서 Application Default Credentials (ADC)를 활성화합니다:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project explore-ai-c53f5e43
```

---

## 5. 빠른 시작 가이드 (Quick Start)

### 단계 1: Zero-LLM EBNF 검색 필터 추출 (< 5ms)
```bash
python3 ge_api/ebnf/EBNF.py "2025년도에 홍길동이 작성한 AI 규제 보고서 PDF 문서를 찾아줘."
```

### 단계 2: Gemini Enterprise 실시간 스트리밍 질의
```bash
python3 ge_api/stream_assist/stream_assist.py "국내외 생성형 AI 도입 전략을 2줄로 요약해줘."
```

### 단계 3: 로컬 FastMCP 부동산 서버 구동
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
- **노코드 및 워크플로우 에이전트**: [`ge_lab/nocode_agent/nocode_agent.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/ge_lab/nocode_agent/nocode_agent.md)

---

## 6. 보안 가드레일 및 엔터프라이즈 데이터 프라이버시

> [!IMPORTANT]
> **엄격한 비밀정보 보호 및 엔터프라이즈 컴플라이언스 원칙**  
> [`GEMINI.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/GEMINI.md) 준수 가이드라인:
> 1. **비밀정보 유출 절대 방지**: `.env` 파일, 개인 API 키(`GOOGLE_API_KEY`), 서비스 계정 비공개 키, 액세스 토큰은 절대로 스테이징하거나 커밋/푸시하지 않습니다.
> 2. **안전한 템플릿만 커밋 허용**: 플레이스홀더 값만 담긴 예시 템플릿(예: `.env.example`)만 버전 관리에 포함됩니다.
> 3. **엔터프라이즈 프라이버시 경계**: Gemini Enterprise 웹 앱 내에서 입력된 모든 프롬프트, 사내 업로드 문서 및 지식 파일은 Google 기본 파운데이션 모델 재학습에 일체 활용되지 않으며 테넌트 내에서 격리 보호됩니다.
> 4. **사전 점검 필수**: Git 커밋 또는 푸시 작업을 진행하기 전 반드시 `git status`와 스테이징 변경점을 점검하여 민감한 정보가 포함되어 있지 않은지 확인하십시오.