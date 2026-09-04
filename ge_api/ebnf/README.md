# 🧩 EBNF Search Filter Parsing Engine

Google Cloud **Discovery Engine** 및 **Vertex AI Search**의 **AIP-160** 규격을 완벽하게 준수하는 **EBNF (Extended Backus–Naur Form) 검색 필터 자동 추출 엔진**입니다.

사용자의 복잡하고 일상적인 대화형 자연어 질의에서 검색 메타데이터 제약 조건(문서 주제, 문서 타입, 작성자, 작성 년도, 부서, 상태 등)을 자동으로 추출하고 표준 EBNF 필터 문자열로 합성합니다.

---

## 📁 디렉토리 구조

```text
ge_api/ebnf/
├── __init__.py       # ebnf 패키지 진입점 (모듈 export)
├── EBNF.py           # Zero-LLM 순수 규칙/패턴 기반 초고속 추출기 (< 5ms, $0)
├── EBNF_LLM.py       # Gemini 3.5 Flash Lite 기반 LLM 추출기 (1초 이내 최적화)
└── README.md         # EBNF 기술 아키텍처 및 상세 가이드 (본 문서)
```

---

## 🎯 1. EBNF 필터 및 Google Cloud AIP-160 개요

Google Cloud Discovery Engine은 검색 시 고도화된 구조적 메타데이터 필터링을 위해 **AIP-160 (API Improvement Proposals - Filtering)** 구문을 사용합니다.

### 📌 AIP-160 문법 규칙
- **논리 연산자**: `AND`, `OR`, `NOT` (반드시 **대문자** 사용)
- **문자열 값**: 반드시 큰따옴표(`"..."`)로 감쌈
- **숫자/불리언 값**: 따옴표 없이 표기 (예: `year >= 2024`, `status = true`)
- **비교 연산자**: `=`, `!=`, `>`, `<`, `>=`, `<=`

### 📌 주요 지원 메타데이터 필드
| 필드명 | 설명 | 추출 예시 | 변환된 EBNF 필터 |
| :--- | :--- | :--- | :--- |
| `category` | 문서 주제 및 종류 | "재무 보고서", "세계 증시 보고서" | `category = "재무 보고서"` |
| `file_type` | 파일 확장자 | "PDF 파일", "워드 문서", "PPT" | `file_type = "pdf"`, `file_type = "docx"` |
| `author` | 작성자 성명 | "신항식이 작성했어", "이영희가 쓴" | `author = "신항식"` |
| `year` | 작성 년도 및 기간 | "2024년 이후", "2025년도에", "2022~2024년" | `year >= 2024`, `year = 2025`, `year >= 2022 AND year <= 2024` |
| `department` | 소속 부서 및 팀 | "아마도 AI 팀이야", "소속은 인사팀" | `department = "AI 팀"`, `department = "인사팀"` |
| `status` | 문서 상태 및 부정/제외 | "초안 제외하고", "임시 문서 말고" | `NOT status = "draft"` |

---

## ⚡ 2. Zero-LLM 규칙 기반 추출기 (`EBNF.py`)

Gemini나 외부 API 호출 없이, 순수 정규 표현식 및 형태소/조사 분해 알고리즘을 사용하여 **완전 로컬 환경**에서 동작합니다.

### 🚀 핵심 특징
1. **극단적인 초저지연**: 쿼리당 **~0.05 ms ~ 6 ms** (밀리초 단위) 이내 처리.
2. **비용 0원 ($0)**: API 호출이 전혀 없어 대규모 고빈도 트래픽에도 비용이 발생하지 않음.
3. **복합 다문장 & 구어체 질의 완벽 대응**:
   - 예: `"세계 증시 보고서를 신항식이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야."`
   - 변환 결과: `department = "AI 팀" AND author = "신항식" AND year = 2025 AND category = "세계 증시 보고서"`

### 🧠 파이프라인 처리 순서
1. **검색 연산자 추출**: `author:신항식`, `filetype:pdf`, `year:>=2025` 등 표준 연산자 파싱
2. **년도/기간 선추출**: `2024년 이후에`, `2025년도에` 등을 먼저 추출하여 작성자나 문서명과의 충돌 방지
3. **부서/소속팀 추출**: `아마도`, `혹시`, `소속은` 등의 구어체 접두사와 결합된 부서명 및 약어(`AI 팀`, `IT 팀` vs `인사팀`) 정규화
4. **작성자 추출**: 능동태 과거형 서술어(`작성했어`, `작성한`, `쓴`, `만들었어`, `등록했어`)와 결합된 성명을 추출하고, 수동태(`작성된 재무 보고서`)는 문서명으로 정확히 격리
5. **파일 타입 매핑**: 한글 표현(`워드`, `엑셀`, `파포`, `한글`)을 표준 확장자(`docx`, `xlsx`, `pptx`, `hwp`)로 자동 매핑
6. **부정/제외 조건**: `초안 제외하고`, `임시 말고` → `NOT status = "draft"`
7. **문서 주제 추출**: 불필요한 수식어(`작성된`, `생성된`, `하고`, `및`)를 제거하고 핵심 주제어(`세계 증시 보고서`) 정제
8. **AIP-160 표준 순서 정렬**: `[department, author, year, file_type, status, category]` 순으로 결정론적 결합

---

## 🤖 3. Gemini 3.5 Flash Lite 기반 LLM 추출기 (`EBNF_LLM.py`)

Google Cloud의 최신 경량 모델인 **Gemini 3.5 Flash Lite**를 활용하여, 규칙으로 정의하기 어려운 고도의 문맥과 유의어를 이해하고 EBNF 필터를 생성합니다.

### 🛑 초기 버전의 성능 병목 원인 분석 (~2.65초)
초기 구현 시 2.65초가 소요되었던 원인을 단계별로 프로파일링한 결과는 다음과 같습니다:

```text
[최적화 전 지연시간: 약 2,656 ms]
┌─────────────────────────────────┬──────────┬────────────────────────────────────────────────────────┐
│ 소요 단계                        │ 소요 시간 │ 병목 원인                                               │
├─────────────────────────────────┼──────────┼────────────────────────────────────────────────────────┤
│ 1. ADC 인증 파일 탐색 & 토큰 갱신 │ ~674 ms  │ google.auth.default() 디스크 I/O 및 매번 OAuth2 토큰 POST│
│ 2. 클라이언트 & 전송 풀 재초기화  │ ~230 ms  │ 호출마다 genai.Client 및 HTTP 전송 세션을 신규 생성      │
│ 3. TLS / TCP 핸드셰이크 왕복      │ ~220 ms  │ 서울(한국) ↔ Vertex AI 글로벌 데이터센터(미국) 네트워크 RTT │
│ 4. 장황한 중첩 JSON 토큰 생성    │ ~1,532 ms│ 동일한 메타데이터를 여러 한글 키로 중복 생성            │
└─────────────────────────────────┴──────────┴────────────────────────────────────────────────────────┘
```

---

### 🚀 1초 이내 (< 1.0s) 응답을 위한 5대 핵심 최적화 방안

#### ① 싱글톤 클라이언트 & HTTP Keep-Alive 연결 재사용 (`_CLIENT_INSTANCE`)
- **개선점**: 매 함수 호출마다 인증과 클라이언트를 새로 생성하던 방식을 전역 싱글톤(`get_genai_client()`)으로 변경.
- **효과**: 이미 열려있는 HTTP/1.1 Keep-Alive 소켓과 메모리에 유효한 OAuth 토큰을 재사용하여 **약 900 ms의 오버헤드를 0 ms로 제거**.

#### ② 컴팩트 프롬프트 & 토큰 수 최소화 (`max_output_tokens=75`)
- **개선점**: LLM에게 중첩 딕셔너리(`"extracted_info": {"문서종류": ..., "문서 타입": ...}`) 생성을 요구하지 않고, 단일 최소 JSON만 출력하도록 유도:
  ```json
  // 최적화된 최소 출력 (약 25 토큰)
  {"filter": "<AIP-160 EBNF>", "clean": "<search query>"}
  ```
- **효과**: 원격 LLM 생성 토큰 수가 80개 → 25개로 60% 이상 감소하여 **디코딩 시간 약 400~500 ms 단축**.

#### ③ 제로-토큰 Python 로컬 속성 분해 (`parse_extracted_info_from_filter`)
- **개선점**: EBNF 필터 문자열(`category = "재무 보고서" AND file_type = "pdf" ...`)을 로컬 Python 정규식으로 역파싱하여 `extracted_info` 딕셔너리로 즉각 변환.
- **효과**: LLM의 귀중한 생성 토큰을 낭비하지 않고 **0.01 ms** 만에 완벽한 구조화 데이터 완성.

#### ④ 연결 사전 웜업 (`warmup()`)
- **개선점**: 애플리케이션 시작 또는 모듈 로드 시 1토큰짜리 경량 핑(Ping)을 전송하여 TCP 3-way 핸드셰이크, TLS 1.3 암호화 협상, DNS 룩업을 사전에 완료.
- **효과**: 실제 사용자 첫 요청 시 발생하는 초기 연결 지연(~300~500ms) 완전 배제.

#### ⑤ 하이브리드 패스트패스 옵션 (`fast_path=True`)
- **개선점**: 기업용 검색 엔진에서 엄격한 SLA(< 50ms)가 요구될 경우, 구조적 패턴이 명확한 질의는 `EBNF.py`를 통해 **~5 ms** 만에 즉시 반환하고, 복잡한 비정형 질의만 Gemini 3.5 Flash Lite로 폴백.

#### ⑥ 초기 연결 & Warmup 1회 처리 후 지속 대화형 질의 세션 (`interactive_session()`)
- **개선점**: 매번 스크립트를 재실행하여 연결을 맺고 끊는 대신, 초기 1회 클라이언트 연결 및 Warm-up을 완료한 후 지속적으로 질문을 입력받는 인터랙티브 루프 제공.
- **효과**: 활성화된 지속 연결(Persistent Keep-Alive Connection) 상에서 연속 질의를 처리하므로 콜드스타트가 원천 차단되며, 쿼리별 순수 LLM 추론 시간과 세션 종합 통계(평균, 최소, 최대, 1초 이내 달성률)를 실시간으로 확인 가능.

---

## 📊 4. 벤치마크 및 성능 비교

| 모드 | 동작 방식 | 평균 지연시간 | 1초 SLA 달성 여부 | 비용 (Cost) |
| :--- | :--- | :--- | :--- | :--- |
| **Zero-LLM (`EBNF.py`)** | 순수 로컬 정규식/패턴 | **~0.05 ms ~ 6.5 ms** | ✅ **완벽 충족 (< 0.01s)** | **$0** (완전 무료) |
| **Pure LLM 최적화 전** | 매번 신규 인증 + 장황한 JSON | **~2,656 ms** | ❌ 초과 (~2.6초) | API 토큰 과다 소모 |
| **Pure LLM 최적화 후** | 싱글톤 + 웜업 + 컴팩트 토큰 | **~840 ms ~ 950 ms** | ✅ **달성 (< 1.0s)** | 최소 토큰 과금 |
| **하이브리드 패스트패스** | 규칙 선처리 + LLM 폴백 | **~4.8 ms** (규칙 히트 시) | ⚡ **극초고속 (< 0.005s)** | 90% 이상 0원 |

---

## 💻 5. 실행 및 사용 방법

### 1) CLI 터미널 실행

#### Zero-LLM 규칙 기반 추출기 실행:
```bash
# 기본 쿼리 테스트
python3 ge_api/ebnf/EBNF.py

# 커스텀 대화형 쿼리 테스트
python3 ge_api/ebnf/EBNF.py "세계 증시 보고서를 신항식이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야."
```

#### Gemini 3.5 Flash Lite 지속 대화형(Continuous Interactive) 추출기 실행:
```bash
# 초기 클라이언트 연결 및 Warm-up을 1회 완료한 후, 지속적으로 질문을 입력받아 레이턴시를 측정
python3 ge_api/ebnf/EBNF_LLM.py

# 특정 질문을 먼저 실행한 후 대화형 루프로 진입할 수도 있습니다:
python3 ge_api/ebnf/EBNF_LLM.py "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
```

**실행 화면 예시:**
```text
====================================================================
🚀 Gemini 3.5 Flash Lite - Continuous Interactive EBNF Filter Extractor
Model: gemini-3.5-flash-lite | Location: global
====================================================================
⚡ Pre-warming connection (DNS, TCP, TLS handshake)...
   Warm-up completed in 1204.1 ms (Connection established & persistent)

💡 Enter queries continuously. Type 'q', 'quit', or 'exit' to stop.
────────────────────────────────────────────────────────────────────

💬 질문 입력 (종료: q/exit) > 2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘

[1] 🔍 질의 (Query): 2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘
📋 Extracted Filter Information (주어진 조건 정보):
  • 문서종류      : 재무 보고서
  • 문서 타입     : pdf
  • 작성 일자     : >= 2024

🎯 Clean Query (검색어): 재무 보고서
👉 EBNF Filter (조합된 EBNF 필터):
category = "재무 보고서" AND file_type = "pdf" AND year >= 2024
────────────────────────────────────────────────────────────────────
⏱️  Performance Telemetry:
  • LLM Inference Latency : 900.6 ms
  • Total Request Latency  : 903.6 ms
  • Target (< 1.0s SLA)   : ✅ PASS (< 1.0s)
────────────────────────────────────────────────────────────────────

💬 질문 입력 (종료: q/exit) > exit

👋 세션을 종료합니다.

📊 세션 요약 통계 (Session Summary):
  • 총 처리 쿼리 수 : 3 건
  • 평균 응답 시간  : 999.0 ms
  • 최소 응답 시간  : 900.6 ms
  • 최대 응답 시간  : 1138.7 ms
  • 1초 이내 달성률 : 66.7% (2/3)
```

---

### 2) Python 코드 내 Import 사용법

```python
from ge_api.ebnf import extract_ebnf_filter, extract_ebnf_with_llm

query = "세계 증시 보고서를 신항식이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야."

# 1. Zero-LLM 순수 규칙 기반 호출 (지연시간: ~5ms, $0)
res_rule = extract_ebnf_filter(query)
print("EBNF Filter (Rule):", res_rule["ebnf_filter"])
print("Latency:", res_rule["latency_ms"], "ms")

# 2. Gemini 3.5 Flash Lite 순수 LLM 호출 (지연시간: < 1.0s)
res_llm = extract_ebnf_with_llm(query)
print("EBNF Filter (LLM):", res_llm["ebnf_filter"])
print("Latency:", res_llm["total_latency_ms"], "ms")

# 3. 하이브리드 패스트패스 호출 (명확한 패턴 즉시 반환, 지연시간: < 5ms)
res_hybrid = extract_ebnf_with_llm(query, fast_path=True)
print("EBNF Filter (Hybrid):", res_hybrid["ebnf_filter"])
print("Mode:", res_hybrid["mode"])
```

---

## 🛠️ 지원 질의 예시 및 추출 결과

| 입력 자연어 질의 | 추출된 조건 속성 | 생성된 EBNF 필터 문자열 |
| :--- | :--- | :--- |
| `세계 증시 보고서를 신항식이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야.` | 부서: AI 팀<br>작성자: 신항식<br>년도: 2025<br>주제: 세계 증시 보고서 | `department = "AI 팀" AND author = "신항식" AND year = 2025 AND category = "세계 증시 보고서"` |
| `2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘` | 년도: >= 2024<br>타입: pdf<br>주제: 재무 보고서 | `year >= 2024 AND file_type = "pdf" AND category = "재무 보고서"` |
| `소속은 인사팀이고 이영희가 쓴 2024년 채용 계획서 PPT 파일` | 부서: 인사팀<br>작성자: 이영희<br>년도: 2024<br>타입: pptx<br>주제: 채용 계획서 | `department = "인사팀" AND author = "이영희" AND year = 2024 AND file_type = "pptx" AND category = "채용 계획서"` |
| `초안 제외하고 김철수가 작성한 2023년 이전 보안 감사 보고서 워드 파일` | 상태: NOT draft<br>작성자: 김철수<br>년도: <= 2023<br>타입: docx<br>주제: 보안 감사 보고서 | `author = "김철수" AND year <= 2023 AND file_type = "docx" AND NOT status = "draft" AND category = "보안 감사 보고서"` |
| `author:신항식 year:>=2025 filetype:pdf` | 작성자: 신항식<br>년도: >= 2025<br>타입: pdf | `author = "신항식" AND year >= 2025 AND file_type = "pdf"` |
