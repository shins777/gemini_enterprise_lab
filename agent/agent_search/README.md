# 🤖 Search Agent Engine - Vertex AI Reasoning Engine (A2A 호환 검색 에이전트)

본 모듈은 차세대 에이전트 연동 표준 인터페이스인 **A2A (Agent-to-Agent)** 기술 규격을 충족하며, 구글이 개발한 **Google ADK (Agent Development Kit)**를 기반으로 빌드된 프리미엄 웹 검색 전용 어시스턴트 에이전트 패키지입니다. 

**Gemini 2.5 Flash**의 강력한 텍스트 분석 성능과 실시간 Google Search 핵심 도구를 융합하여 질문이 도달했을 때 능동적으로 정보를 검색, 조립 및 정리하여 유저에게 반환합니다.

---

## 📂 파일 구성 및 레이아웃 (Project Structure)

```tree
agent_search/
├── agent.py              # Google ADK 기반 에이전트 코어 선언 및 A2A 매핑 변환
├── deploy.py             # Vertex AI Reasoning Engine 원격 배포 및 롤아웃 수행 스크립트
├── query_agent.py        # 배포된 원격 리즈닝 엔진에 실시간 질의를 날리는 테스트 세션 클라이언트
├── a2a_server.py         # 로컬 프록시 구동용 FastAPI/Uvicorn A2A 호환 웹 서버 규격
├── requirements.txt      # Google ADK 및 AI 플랫폼 연동 패키지 디펜던시 정의서
└── README.md             # 본 가이드 문서 (한글 전용)
```

---

## 🚀 배포 리소스 정보 (Deployed Production Info)

구글 클라우드 플랫폼 **`explore-ai-aa934711`** 리전의 공식 엔터프라이즈 Vertex AI 리즈닝 엔진 정보입니다.

- **대상 프로젝트 ID (GCP Project ID):** `explore-ai-aa934711`
- **구동 위치 (Region Location):** `us-central1`
- **Reasoning Engine 공식 고유 식별자 (Resource Name):**
  ```text
  projects/66747595426/locations/us-central1/reasoningEngines/2482267896227561472
  ```

---

## ⚙️ 실행 및 가동 절차 (How to Run)

### 1. 패키지 설치
우선 파이썬 가상환경 또는 개발 환경 세션상에 ADK 및 에이전트 엔진 패키지 의존성을 수립합니다.
```bash
pip install -r requirements.txt
```

### 2. Vertex AI 리즈닝 엔진에 배포/재배포 (Deploy)
새로운 코드 업데이트 사항이 존재하거나, 다른 테넌트의 클라우드 버킷 환경에 엔진을 다시 프로비저닝하고자 할 때 유효합니다.
```bash
# 구글 ADC 인증 액세스 토큰을 추출하여 원격 환경 배포 커맨드 가동
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
GCP_PROJECT="explore-ai-aa934711" \
GCP_LOCATION="us-central1" \
GCS_STAGING_BUCKET="gs://run-sources-explore-ai-aa934711-us-central1" \
python3 deploy.py
```

### 3. 클라이언트 원격 질의 확인 (Interactive Query Test)
정식 롤아웃된 Vertex AI 백엔드 에이전트 인스턴스로 비동기 스트리밍 요청 세션을 생성하고 실시간 서칭 응답을 화면에 송출해 보는 도구입니다.
```bash
python3 query_agent.py
```

### 4. 로컬 A2A 서버 구동 (Local Hosting)
로컬에서 다른 오케스트레이터 에이전트와 로컬 루프백 테스트 및 Well-known JSON 카드 검증을 수행하기 위해 FastAPI 프레임워크 기반 프록시를 오픈합니다.
```bash
python3 a2a_server.py
```
* **로컬 서버 접근 경로:** `http://localhost:8000`
* **에이전트 인터페이스 명세 카드:** `http://localhost:8000/.well-known/agent-card.json`

---

## 💡 개발 어드바이스 및 주의사항 (Architecture & Troubleshooting)

* **Google Search 툴 통합:** `agent.py` 내부에 지정된 `tools=[google_search]` 구문은 에이전트가 별도의 복잡한 서칭 플러그인 연동 없이 구글의 원천 검색 색인(Index)에 접근할 수 있게 만듭니다.
* **tar.gz 압축 패키징 빌드:** `deploy.py` 구동 시, 내부 패키징 엔진이 이 디렉토리 전체 모듈을 바이너리 객체화하고 `GCS_STAGING_BUCKET`에 아티팩트로 임시 업로드한 뒤 컴파일러에 전달하는 방식으로 배포 처리를 마무리합니다.
* **A2A Wrapper 경고 메시지:** 실행 로그 출력 중 나타나는 `[EXPERIMENTAL] to_a2a` 메시지는 파이썬 ADK SDK 내부에서 프록시 및 디스패처에 적용된 호환성 표시 목적의 경고로 작동에는 아무런 부작용을 끼치지 않으므로 무시해도 안전합니다.
