# 🚀 Gemini Enterprise Lab (구글 제미나이 엔터프라이즈 실습 가이드)

본 저장소는 **Gemini Enterprise (제미나이 엔터프라이즈)** 및 **Vertex AI Agent Platform** 환경에서 구동되는 고성능, 프로덕션 등급의 맞춤형 **MCP (Model Context Protocol) 서버**와 **A2A (Agent-to-Agent) 검색 에이전트**의 배포 및 연동 자산을 포함하고 있습니다.

---

## 📂 프로젝트 구조 (Project Structure)

저장소의 전체 구조는 다음과 같이 깔끔하고 모듈화되어 관리됩니다.

```tree
gemini_enterprise_lab/
├── mcp/                             # MCP (Model Context Protocol) 서버 모듈
│   ├── mcp_google_map/              # Google Maps MCP 서버 (FastMCP)
│   │   ├── server.py                # 구글 맵 탐색 & 거리 계산 기능 구현
│   │   ├── mcp_config.json          # Agent Platform 등록용 MCP 메타데이터 설정
│   │   ├── Dockerfile               # Cloud Run 컨테이너 빌드 정의
│   │   ├── deploy.sh                # 자동화 배포 스크립트
│   │   └── README.md                # 구글 맵 MCP 한글 가이드
│   │
│   └── mcp_realestate/              # 한국 부동산 20개년 요인 분석 MCP 서버
│       ├── server.py                # 부동산 지표 및 금리 데이터 질의 구현
│       ├── korea_real_estate_20yr_factors.csv # 영문 헤더로 정리된 부동산 데이터셋
│       ├── mcp_config.json          # Agent Platform 등록용 MCP 메타데이터 설정
│       ├── Dockerfile               # Cloud Run 컨테이너 빌드 정의
│       ├── deploy.sh                # 자동화 배포 스크립트
│       └── README.md                # 부동산 MCP 한글 가이드
│
├── agent/                           # Reasoning Engine 검색 에이전트 모듈
│   └── agent_search/                # A2A 호환 검색 에이전트 (Google ADK 기반)
│       ├── agent.py                 # 구글 검색 도구가 결합된 ADK 에이전트 선언
│       ├── deploy.py                # Vertex AI Agent Engine 배포용 스크립트
│       ├── query_agent.py           # 배포된 Reasoning Engine 실시간 질의 클라이언트
│       ├── a2a_server.py            # 로컬 프록시용 A2A API 서버 규격 구현
│       ├── requirements.txt         # 에이전트 실행에 필요한 의존성 패키지 목록
│       └── README.md                # 에이전트 엔진 배포 및 연동 한글 가이드
│
└── README.md                        # 본 마스터 한글 가이드 문서
```

---

## 🌐 1. MCP 서버 Cloud Run 배포 & 등록 가이드

실습 환경의 구글 클라우드 프로젝트 `explore-ai-aa934711`에 완전히 배포 완료된 실시간 MCP 서버 리소스 세부 정보입니다.

### 📍 배포 리소스 요약 (Deployed Resources)

| MCP 서버 이름 | 클라우드 런 배포 URL (HTTP Endpoint) | 지역 (Region) | 인증 방식 (Auth) |
| :--- | :--- | :--- | :--- |
| **Google Maps MCP Server** | `https://google-maps-mcp-66747595426.us-central1.run.app/mcp` | `us-central1` | Unauthenticated / GCP OIDC |
| **Korea Real Estate MCP Server** | `https://korea-realestate-mcp-66747595426.us-central1.run.app/mcp` | `us-central1` | Unauthenticated / GCP OIDC |

### 🛠️ 수동 빌드 & 배포 방법
만약 수정된 소스 코드를 반영하여 클라우드 런에 재배포하려면 각 MCP 서버 디렉토리 내부에서 다음 명령어를 실행하십시오. (ADC 액세스 토큰 사용 기준)

```bash
# 1. 대상 MCP 서버 디렉토리로 이동
cd mcp/mcp_google_map  # 또는 mcp/mcp_realestate

# 2. 클라우드 런에 소스 코드 기반 빌드 및 배포 수행
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
gcloud run deploy [서비스-이름] \
  --source . \
  --project explore-ai-aa934711 \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

### 📋 Agent Platform 등록 절차 (Agent Registry)
배포된 MCP 서버들을 제미나이 에이전트에서 도구(Tool)로 연동하기 위해 **Agent Platform**에 등록해야 합니다.

1. **Agent Platform Admin Console** (Gemini Enterprise Admin)에 접속합니다.
2. **Agent Registry** ➔ **MCP Server Registration** 메뉴로 이동합니다.
3. **Add Custom MCP Server** 단추를 누르고 아래 값을 입력합니다.

#### Google Maps MCP 설정
* **Server Name:** `Google Maps MCP Server`
* **Transport:** `SSE` (Server-Sent Events) 또는 `HTTP` (Streamable-HTTP)
* **Server URL / SSE Endpoint:** `https://google-maps-mcp-66747595426.us-central1.run.app/mcp`
* **Authentication:** `GCP IAM OIDC token` 또는 `Unauthenticated`

#### Korea Real Estate MCP 설정
* **Server Name:** `Korea Real Estate MCP Server`
* **Transport:** `SSE` (Server-Sent Events) 또는 `HTTP` (Streamable-HTTP)
* **Server URL / SSE Endpoint:** `https://korea-realestate-mcp-66747595426.us-central1.run.app/mcp`
* **Authentication:** `GCP IAM OIDC token` 또는 `Unauthenticated`

---

## 🤖 2. Search Agent Engine (Reasoning Engine) 가이드

Google ADK와 Gemini 2.5 Flash를 결합하여 제작된 구글 검색 기반의 **A2A 호환 검색 에이전트**를 구글 클라우드 Vertex AI Reasoning Engine 서비스에 배포 및 테스팅하는 법을 다룹니다.

### 📍 배포 리소스 요약 (Vertex AI Reasoning Engine)
* **프로젝트 ID (Project ID):** `explore-ai-aa934711`
* **위치 (Location):** `us-central1`
* **Reasoning Engine 고유 리소스 경로:**
  ```text
  projects/66747595426/locations/us-central1/reasoningEngines/2482267896227561472
  ```

### 🚀 배포/재배포 실행 (Deployment)
로컬에 구성된 에이전트 파이썬 정의를 가공하여 Vertex AI Agent Engine에 빌드 및 배포하려면 아래 환경 변수를 주입하고 배포 스크립트를 수행하십시오.

```bash
cd agent/agent_search

# 의존성 패키지 설치
pip install -r requirements.txt

# 에이전트 엔진 배포 실행
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
GCP_PROJECT="explore-ai-aa934711" \
GCP_LOCATION="us-central1" \
GCS_STAGING_BUCKET="gs://run-sources-explore-ai-aa934711-us-central1" \
python3 deploy.py
```

### 🧪 배포된 에이전트 테스트 (Query Client)
배포가 정상적으로 완료되면 스트리밍 질의 클라이언트를 실행하여 생성된 Reasoning Engine이 실시간 구글 검색 도구를 활용하여 답변을 산출하는지 확인할 수 있습니다.

```bash
cd agent/agent_search
python3 query_agent.py
```

---

## 📈 3. 한국 부동산 20개년 데이터셋 명세 (Korean Real Estate Dataset Spec)

에이전트가 보다 일관성 있고 표준화된 명칭으로 질의할 수 있도록 기존 한국어 헤더 구조를 **완벽한 영문 표준 카멜/스네이크 케이스 포맷**으로 교체 및 마이그레이션했습니다.

### 📊 헤더 변환 테이블 (CSV Headers Translation)

| 기존 한글 헤더 (Korean) | 변경된 영문 헤더 (English) | 데이터 타입 (Type) | 상세 설명 (Description) |
| :--- | :--- | :--- | :--- |
| `연도` | `year` | `Integer` | 분석 대상 연도 (2006 ~ 2025) |
| `한국은행 기준금리` | `interest_rate` | `Float` | 한국은행 공시 연간 기준금리 (%) |
| `KOSPI 지수 기말` | `kospi` | `Float` | 연도 기말 종가 기준 KOSPI 종합지수 |
| `서울 아파트 평균매매가 - 만원` | `seoul_apartment_avg_price` | `Integer` | 서울 권역 아파트 평균 매매 거래 가격 (단위: 만원) |
| `지방 5대광역시 평균매매가 - 만원` | `regional_apartment_avg_price` | `Integer` | 5대 광역시 평균 매매 거래 가격 (단위: 만원) |
| `전국 아파트 매매가격지수` | `national_apartment_price_index` | `Float` | 전국 아파트 매매 가격 누적 지수 |
| `소비자물가지수` | `cpi` | `Float` | 전국 소비자 물가 지수 (CPI) |
| `M2 통화량 - 조원 기말` | `m2_money_supply` | `Integer` | 광의통화 M2 총량 (단위: 조원) |
| `전국 미분양주택 - 호` | `unsold_housing` | `Integer` | 미분양 누적 주택 잔여 세대수 (단위: 호) |

---

## 💡 개발자를 위한 아키텍처 참고사항 (Developer Architecture Notes)

1. **FastMCP와 Streamable-HTTP:** 본 실습 가이드에 활용된 MCP 서버들은 파이썬 FastMCP 프레임워크 상에서 가동되며, 기존의 표준 `stdio` 입출력 방식 대신 클라우드 네이티브 서버 환경에 최적화된 **`streamable-http`** 전송 규격을 채택하여 빌드되었습니다. 이로 인해 무상태(Stateless) 아키텍처인 구글 Cloud Run 환경에서 완전한 멀티스레드 기반 비동기 API 엔드포인트 연동이 보장됩니다.
2. **Google ADK & A2A Wrapper:** `agent_search` 폴더 내의 에이전트는 차세대 에이전트 오케스트레이션 설계 모델인 **Agent-to-Agent (A2A)** 표준을 준수합니다. Google ADK가 제공하는 `to_a2a()` 변환 데코레이터를 거쳐 빌드된 이 엔진은 Vertex AI 상에서 독립적인 인스턴스로 분리되어 동작하면서도 타 에이전트 카드를 해석하고 프록시를 통해 유연하게 메시지를 중계 및 오케스트레이션할 수 있습니다.
3. **IAM 최소 권한 법칙:** Cloud Run과 Vertex AI 간 리소스 빌드업 시 발생하던 스토리지 및 아티팩트 권한 충돌은 기본 Compute Engine 서비스 계정에 권한을 유기적으로 바인딩함으로써 해결되었으며, 실제 프로덕션 수준의 인프라 전환 시에는 개별 사용자 세분화 정책을 권장합니다.