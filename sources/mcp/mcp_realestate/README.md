# 🏠 Korea Real Estate MCP Server (한국 부동산 지표분석 MCP 서버)

본 디렉토리는 지난 20개년(2006년 ~ 2025년)간의 한국은행 기준금리, 코스피(KOSPI) 종가, 서울 및 지방 5대광역시 아파트 평균 거래가, 전국 미분양 주택 호수 등의 경제 핵심 인프라 원천 데이터를 표준화된 인프라로 수록하고, 제미나이 에이전트가 이를 자유롭게 검색 및 분석할 수 있도록 도구를 지원하는 Model Context Protocol (MCP) 서버 구현체입니다.

---

## 📊 변환 완료된 영문 표준 데이터셋 (English Database Spec)
에이전트 연동 호환성과 특수기호 파싱 이슈를 해소하기 위해 원본 한국어 헤더를 완벽한 영문 표준 명칭으로 교체 및 재설계했습니다.

* **원천 파일:** `korea_real_estate_20yr_factors.csv`

| 영문 표준 컬럼명 | 데이터 형식 | 설명 |
| :--- | :--- | :--- |
| `year` | `integer` | 연도 범위 (2006년 ~ 2025년) |
| `interest_rate` | `float` | 한국은행 고시 연간 기준금리 (%) |
| `kospi` | `float` | 기말 기준 종합주가지수 (KOSPI) |
| `seoul_apartment_avg_price` | `integer` | 서울 아파트 평균매매가 (단위: 만원) |
| `regional_apartment_avg_price` | `integer` | 지방 5대광역시 아파트 평균매매가 (단위: 만원) |
| `national_apartment_price_index` | `float` | 전국 아파트 매매가격 누적 지수 |
| `cpi` | `float` | 소비자물가지수 (CPI) |
| `m2_money_supply` | `integer` | 기말 기준 광의통화(M2) 통화량 (단위: 조원) |
| `unsold_housing` | `integer` | 전국 미분양주택 미분양 세대 잔여분 (단위: 호) |

---

## 🛠️ 제공 도구 (Server Tools)

1. `get_factors_by_year`: 지정 연도 한 해에 매핑되는 기준금리, 부동산 평균가격 등 9가지 핵심 경제 지표 집합을 딕셔너리로 단번에 추출합니다.
2. `get_factors_range`: 시작 연도와 끝 연도를 입력받아 시계열 추이 분석이 가능하도록 해당 범위 내의 연도별 원천 데이터 레코드를 수집 및 배열 형태로 리턴합니다.
3. `get_all_factors`: 데이터베이스 파일 내에 축적된 20개년 전체 시계열 매트릭스 정보를 반환합니다. 상관 분석이나 선형 추론 도구를 생성할 때 유용하게 연계될 수 있습니다.

---

## ⚙️ 로컬 Setup 및 사전 검증 가이드 (Setup)

1. **가상 환경 필수 패키지 설치:**
   ```bash
   pip install -r requirements.txt
   ```

2. **서버 수동 구동 테스트:**
   ```bash
   python3 server.py
   ```
   * 서버 시작 확인 로그: `Real Estate FastMCP Server on 0.0.0.0:8080 with streamable-http...`

---

## ☁️ Cloud Run 프로덕션 배포 가이드 (Cloud Run Deployment)

* **최종 배포 주소:** `https://korea-realestate-mcp-66747595426.us-central1.run.app/mcp`
* **타겟 지역:** `us-central1`

수정된 마이그레이션 변경점을 아티팩트 레지스트리에 도커 이미지 빌드 후 즉시 롤아웃하려면 아래와 같이 클라우드 런 배포 쉘 라인을 가동하십시오.

```bash
# ADC 원격 세션을 상속받아 Cloud Run 배포 실행
CLOUDSDK_AUTH_ACCESS_TOKEN="$(gcloud auth application-default print-access-token)" \
gcloud run deploy korea-realestate-mcp \
  --source . \
  --project explore-ai-aa934711 \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

---

## 📋 Agent Registry 등록 속성정의

제미나이 어시스턴트에서 본 데이터셋을 고유한 지식 소스(Datasource)로 삼게 하려면 아래의 주소를 등록 콘솔에 추가하여 마칩니다.

* **엔드포인트 주소:** `https://korea-realestate-mcp-66747595426.us-central1.run.app/mcp`
* **Transport:** `SSE` (백엔드가 FastMCP streamable-http 규격이므로 SSE로 매끄럽게 핸드셰이크가 이루어집니다)
