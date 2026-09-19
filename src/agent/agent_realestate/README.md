# 🤖 Real Estate & Search Custom Agent (`agent_realestate`)
### — Google ADK & A2A 호환 Vertex AI Reasoning Engine 패키지 —

본 모듈은 차세대 에이전트 연동 표준 인터페이스인 **A2A (Agent-to-Agent)** 기술 규격을 충족하며, **Google ADK (Agent Development Kit)**를 기반으로 빌드된 실시간 웹 검색 및 부동산·시장 동향 분석 커스텀 에이전트 패키지입니다.

**Gemini 2.5 Flash**의 텍스트 추론 성능과 실시간 **Google Search** 도구를 융합하여 사용자의 질문(예: 최신 부동산 매매·전세 시장 동향, 금리·대출 규제 영향 등)에 대해 실시간 정보를 검색·분석하여 스트리밍으로 반환하며, **Vertex AI Reasoning Engine (Agent Engine)**에 배포하여 **Gemini Enterprise Workflow Builder (`Existing agents`)** 등에서 즉시 호출할 수 있습니다.

> 🔗 **관련 스킬 명세서**: [`.agents/skills/agent-realestate/SKILL.md`](file:///Users/hangsik/Documents/my_project/gemini_enterprise_lab/.agents/skills/agent-realestate/SKILL.md)

---

## 📂 파일 구성 및 레이아웃 (Project Structure)

```text
agent_realestate/
├── agent.py              # Google ADK 기반 에이전트 코어 선언 및 A2A(to_a2a) 매핑 변환
├── deploy.py             # Vertex AI Reasoning Engine 원격 패키징 및 배포 스크립트
├── query_agent.py        # 배포된 원격 Reasoning Engine에 실시간 스트리밍 질의를 보내는 클라이언트
├── a2a_server.py         # 로컬 프록시 구동용 FastAPI/Uvicorn A2A 호환 웹 서버 규격
├── requirements.txt      # Google ADK, A2A SDK 및 Vertex AI 플랫폼 패키지 의존성 정의서
└── README.md             # 본 가이드 문서
```

---

## 🚀 배포 리소스 구성 정보 (Deployment Configuration)

보안을 위해 실제 GCP 프로젝트 ID 및 리소스 고유 번호는 `.env` 파일 또는 실행 시점 환경 변수로 주입합니다.

- **대상 프로젝트 ID (`PROJECT_ID`):** `your-gcp-project-id` (환경 변수 주입)
- **구동 리전 (`REGION`):** `us-central1`
- **스테이징 버킷 (`GCS_STAGING_BUCKET`):** `gs://run-sources-${PROJECT_ID}-${REGION}`
- **Reasoning Engine 리소스 식별자 형식 (`REASONING_ENGINE_RESOURCE_NAME`):**
  ```text
  projects/{YOUR_PROJECT_NUMBER}/locations/us-central1/reasoningEngines/{YOUR_REASONING_ENGINE_ID}
  ```

---

## ⚙️ 실행 및 배포 절차 (How to Build & Deploy)

### 1. 사전 GCP 인증 및 스테이징 버킷 준비
배포를 실행하기 전 대상 GCP 프로젝트에 로그인하고 Application Default Credentials (ADC) 및 스테이징 버킷을 준비합니다.
```bash
# 1. gcloud CLI 및 ADC 인증
gcloud auth login
gcloud auth application-default login

# 2. 대상 프로젝트 설정
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"
gcloud config set project "${PROJECT_ID}"
gcloud auth application-default set-quota-project "${PROJECT_ID}"

# 3. 필수 API 활성화 및 GCS 스테이징 버킷 생성
gcloud services enable aiplatform.googleapis.com storage.googleapis.com --project="${PROJECT_ID}"
gcloud storage buckets create "gs://run-sources-${PROJECT_ID}-${REGION}" --project="${PROJECT_ID}" --location="${REGION}"
```

### 2. 패키지 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. Vertex AI Reasoning Engine에 배포 (`deploy.py`)
로컬의 ADK 에이전트를 패키징하여 Vertex AI Reasoning Engine으로 배포합니다.
```bash
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
PROJECT_ID="your-gcp-project-id" \
REGION="us-central1" \
GCS_STAGING_BUCKET="gs://run-sources-your-gcp-project-id-us-central1" \
python3 deploy.py
```
- 배포가 완료되면 콘솔에 출력되는 `projects/{YOUR_PROJECT_NUMBER}/locations/us-central1/reasoningEngines/{YOUR_REASONING_ENGINE_ID}` 값을 복사하여 `.env` 파일의 `REASONING_ENGINE_RESOURCE_NAME`에 설정합니다.

### 4. 원격 에이전트 스트리밍 질의 테스트 (`query_agent.py`)
정식 배포된 Vertex AI 백엔드 에이전트 인스턴스로 세션을 생성하고 최근 부동산 시장 동향에 대한 실시간 검색·분석 스트리밍 응답을 확인합니다.
```bash
PROJECT_ID="your-gcp-project-id" \
REGION="us-central1" \
REASONING_ENGINE_RESOURCE_NAME="projects/YOUR_PROJECT_NUMBER/locations/us-central1/reasoningEngines/YOUR_REASONING_ENGINE_ID" \
python3 query_agent.py
```

### 5. 로컬 A2A 서버 구동 (`a2a_server.py`)
로컬 환경에서 A2A 프로토콜 호환 웹 서버 및 Well-known Agent Card JSON 명세를 검증할 때 사용합니다.
```bash
python3 a2a_server.py
```
* **로컬 서버 접근 경로:** `http://localhost:8000`
* **에이전트 인터페이스 명세 카드:** `http://localhost:8000/.well-known/agent-card.json`

---

## 💡 개발 유의사항 및 트러블슈팅 (Architecture & Troubleshooting)

* **로컬-클라우드 패키지 버전 고정 (`deploy.py`):**
  `ReasoningEngine.create()`는 로컬의 `AdkApp` 객체를 `cloudpickle`로 직렬화하여 컨테이너로 전송합니다. 로컬 환경과 클라우드 컨테이너 간의 `google-adk` 및 `pydantic` 버전이 다르면 역직렬화 시점(`canonical_model` / `_resolved_model` 참조)에 `TypeError: 'NoneType' object is not subscriptable` 오류가 발생할 수 있으므로, `deploy.py`의 `requirements` 리스트에는 로컬 환경과 동일한 버전(예: `google-adk[a2a]==2.6.3`, `pydantic==2.13.4`, `google-cloud-aiplatform[adk,agent_engines]==1.163.0`)을 명시적으로 고정해야 합니다.
* **환경 변수 빈 문자열 폴백 처리:**
  상위 `.env` 파일에 `REASONING_ENGINE_RESOURCE_NAME=""`과 같이 빈 문자열이 정의된 경우 `os.getenv("...", DEFAULT)`는 빈 문자열(`""`)을 그대로 반환하여 `ValueError: Resource is not a valid resource id.`를 유발할 수 있습니다. 코드 내에서는 `os.getenv("...") or DEFAULT_VALUE` 패턴을 사용하여 안전하게 기본값으로 폴백하도록 구현되어 있습니다.
* **Google Search 툴 통합:**
  `agent.py` 내부에 지정된 `tools=[google_search]` 구문은 에이전트가 별도의 외부 API 키 없이도 Google의 실시간 검색 색인(Grounding Index)을 활용할 수 있게 합니다.
