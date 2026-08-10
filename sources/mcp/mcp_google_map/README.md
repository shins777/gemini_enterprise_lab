# 🗺️ Google Maps MCP Server (구글 맵 MCP 서버)

본 디렉토리는 Google Maps API를 통해 위치 탐색, 지오코딩 및 두 지점 간 이동 거리/시간 계산 도구를 제공하는 Model Context Protocol (MCP) 서버 구현체입니다. 구글 Cloud Run에 배포하고 Agent Platform에 즉시 연동하여 사용할 수 있도록 설계되었습니다.

---

## 🛠️ 포함된 도구 (Included Tools)

1. `search_location`: Google Maps Places API 및 Geocoding API를 활용하여 지정된 명칭, 주소 또는 주요 관심 지점(POI)을 정밀하게 탐색하고 위도/경도 좌표 및 장소 ID를 수집합니다.
2. `search_restaurants`: 특정 지역(예: 강남역, 서울역 등)의 평점이 높고 인기 있는 주변 맛집 5곳을 엄선하여 이름, 평점, 리뷰 개수 및 주소 등을 리턴합니다.
3. `calculate_distance`: 출발지와 목적지 좌표 또는 주소 간의 도보, 자전거, 대중교통, 자동차 기준 실제 이동 거리(미터) 및 예상 이동 시간(초)을 실시간 산출합니다.

---

## 📂 파일 구조 (File Structure)

* `server.py`: FastMCP 프레임워크와 `streamable-http` 전송 프로토콜을 사용해 구현된 비동기 파이썬 MCP 서버 코어.
* `requirements.txt`: 서버 작동에 필요한 httpx, fastmcp 등의 파이썬 라이브러리 목록.
* `Dockerfile`: Cloud Run 배포용 가벼운 경량화 컨테이너 이미지 정의 파일.
* `deploy.sh`: 한 번의 실행으로 구글 클라우드에 전체 배포 프로세스를 수행하는 쉘 스크립트.
* `mcp_config.json`: 에이전트 오케스트레이터 및 클라이언트 연동 규격을 정의하는 매니페스트 파일.

---

## ⚙️ 로컬 테스트 및 구동 방법 (Local Setup & Testing)

1. 구글 맵스 API 키 환경 변수 등록:
   ```bash
   export GOOGLE_MAPS_API_KEY="AIzaSyBQFudqoZejRXBcq5OB9Pjv6XCYDD6wVj0"
   ```

2. 필수 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```

3. 로컬에서 FastMCP 가동:
   ```bash
   python3 server.py
   ```
   * 서버가 성공적으로 시작되면 로컬 환경의 `http://0.0.0.0:8080/mcp` 엔드포인트로 MCP 요청 처리가 시작됩니다.

---

## ☁️ Cloud Run 프로덕션 배포 가이드 (Deployment)

본 프로젝트는 구글 클라우드 프로젝트 `explore-ai-aa934711`에 완전하게 구축 완료되어 정상 작동 중입니다.

* **최종 배포 URL:** `https://google-maps-mcp-66747595426.us-central1.run.app/mcp`
* **배포 리전:** `us-central1`

수정 사항을 클라우드 빌드를 통해 원격 재배포하려면 아래 명령어를 이용할 수 있습니다.

```bash
# ADC 인증을 우회하여 로컬 권한으로 안전하게 빌드 배포 처리
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
gcloud run deploy google-maps-mcp \
  --source . \
  --project explore-ai-aa934711 \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_MAPS_API_KEY=AIzaSyBQFudqoZejRXBcq5OB9Pjv6XCYDD6wVj0" \
  --port 8080
```

---

## 📋 Agent Platform 연동 규격 (Agent Registry Settings)

본 MCP 서비스를 Agent Platform Agent Registry에 등록하여 에이전트의 실시간 플러그인 툴로 연결하고자 할 경우 아래 세부 사양을 참고하십시오.

1. **서비스 URL 설정:** `https://google-maps-mcp-66747595426.us-central1.run.app/mcp`
2. **전송 프로토콜:** `HTTP` 또는 `SSE` (Streamable-HTTP 사양이 백엔드에 기본 탑재되어 있습니다)
3. **인증 가이드:** 개발/테스트 목적일 때는 Unauthenticated(인증 없음)를 허용하거나, 보안이 필요한 기업 도메인 내부 정책일 경우 OIDC Identity Token을 발급받아 인가 처리를 완료하십시오.
