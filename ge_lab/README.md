# 🧪 Gemini Enterprise 핸즈온 랩 포털 (`ge_lab`)

Gemini Enterprise 공식 웹 어플리케이션 환경에서 핵심 기능을 직접 체험하고 검증하는 **4개 트랙, 총 30개 실습 모듈** 매뉴얼입니다.

---

## 📌 트랙 구성 및 바로가기

| 실습 트랙 | 매뉴얼 문서 | 랩 수 | 핵심 대상 및 주요 내용 |
| :--- | :--- | :---: | :--- |
| **트랙 1: 엔터프라이즈 일반 핵심 기능** | [`ge_general/ge_general.md`](ge_general/ge_general.md) | 10 Labs | 비즈니스 실무자: 추론, Google Search 웹 그라운딩, 사내 커넥터, MCP 도구, Interactive Canvas, Smart Inbox |
| **트랙 2: 멀티모달 미디어 생성 및 편집** | [`media_gen/ge_media.md`](media_gen/ge_media.md) | 9 Labs | 마케터/디자이너: Imagen 3 (T2I, 인페인팅, 스타일 변환, 배너), Veo (T2V, I2V, 비디오 편집, 9:16 숏폼) |
| **트랙 3: 노코드 기본 에이전트 스튜디오** | [`nocode_basic/nocode_basic.md`](nocode_basic/nocode_basic.md) | 4 Labs | 현업 기획자: 대화형 단일 에이전트 생성, 지식(PDF) 바인딩, 검색 연동, 프롬프트 기반 워크플로우 (분기/HITL/Drive) |
| **트랙 4: 심화 워크플로우 오케스트레이션** | [`nocode_advance/nocode_advance.md`](nocode_advance/nocode_advance.md) | 7 Labs | 프로세스 설계자: 수동 빈 캔버스 조립, JSON Schema 변수 추출, MCP 연동, Realest_research, HITL 승인, Gmail/Drive |

---

## 🧭 전체 30개 랩 상세 매트릭스

### 🔹 트랙 1: 엔터프라이즈 일반 핵심 기능 (`ge_general`)
> **매뉴얼**: [`ge_general/ge_general.md`](ge_general/ge_general.md)

| 랩 번호 | 실습 모듈명 | 연동 도구 및 모델 | 핵심 검증 목표 |
| :---: | :--- | :--- | :--- |
| **Lab 1** | [일반 질문 처리 (Direct Q&A)](ge_general/ge_general.md#lab-1-일반-질문-처리-direct-qa-reasoning) | Gemini Core LLM | 다단계 논리 추론, SaaS 이탈률 원인 분석 및 외교적 영문 이메일 재작성 |
| **Lab 2** | [Google 검색 연동 (Web Grounding)](ge_general/ge_general.md#lab-2-google-검색-연동-web-grounding-citations) | Google Search 토글 | 최신 공개 데이터 실시간 검색 및 출처(Citation) URL 앵커링 검증 |
| **Lab 3** | [기업 커넥터 연동 (Connectors)](ge_general/ge_general.md#lab-3-기업-커넥터-연동-enterprise-connectors) | Drive / Gmail / Jira | 권한(ACL) 및 보안 경계를 준수하여 사내 협업 저장소 문서 검색 |
| **Lab 4** | [등록된 스킬 사용 (Skill Invocation)](ge_general/ge_general.md#lab-4-등록된-스킬-사용-skill-invocation-execution) | 기업 등록 스킬 | 사전 등록된 전문 업무 스킬(`load_skill`) 선택 및 실행 |
| **Lab 5** | [전문 서브 에이전트 위임 (Delegation)](ge_general/ge_general.md#lab-5-전문-서브-에이전트-위임-specialist-agents-delegation) | 전문 챗 에이전트 | Canvas Agent, Imagen Agent 등으로 지능형 제어권 위임(`transfer_to_agent`) |
| **Lab 6** | [MCP 서버 연동 (MCP Integration)](ge_general/ge_general.md#lab-6-mcp-서버-연동-model-context-protocol) | Model Context Protocol | 표준 프로토콜 기반 외부 데이터베이스 및 텔레메트리 실시간 질의 |
| **Lab 7** | [커스텀 스킬 제작 및 배포 (Custom Skill)](ge_general/ge_general.md#lab-7-커스텀-스킬-제작-및-배포-custom-skill-authoring) | 스킬 스튜디오 | 커스텀 업무 지침 및 스키마 작성, 에이전트 도구 등록 |
| **Lab 8** | [프로젝트 워크스페이스 (Projects Space)](ge_general/ge_general.md#lab-8-프로젝트-워크스페이스-활용-projects-space) | Projects 격리 공간 | 프로젝트별 지식 문서 바인딩 및 세션 간 영구 컨텍스트 유지 |
| **Lab 9** | [스마트 수신함 (Smart Inbox)](ge_general/ge_general.md#lab-9-스마트-수신함-활용-inbox-action-automation) | Smart Inbox | 미확인 이메일/업무 우선순위 능동 분류, 일정 등록 및 답장 초안 자동 생성 |
| **Lab 10** | [인터랙티브 캔버스 & 슬라이드 (Canvas)](ge_general/ge_general.md#lab-10-인터랙티브-캔버스-및-슬라이드-생성-interactive-canvas-presentation-slides) | Canvas / Slides | 독립 편집 공간에서 문서 협업 및 Google Slides 프레젠테이션 즉시 내보내기 |

---

### 🔹 트랙 2: 멀티모달 미디어 생성 및 편집 (`media_gen`)
> **매뉴얼**: [`media_gen/ge_media.md`](media_gen/ge_media.md)

| 랩 번호 | 실습 모듈명 | 기반 모델 및 기능 | 핵심 검증 목표 |
| :---: | :--- | :--- | :--- |
| **Lab 1** | [고해상도 제품 이미지 생성](media_gen/ge_media.md#lab-1-비즈니스-콘셉트-아트-및-고해상도-제품-이미지-생성) | Imagen 3 (Text-to-Image) | 스튜디오 조명 연출 및 매크로 피사계 심도를 반영한 상용 제품 4K 샷 생성 |
| **Lab 2** | [대화형 부분 수정 (In-painting)](media_gen/ge_media.md#lab-2-멀티턴-대화를-통한-부분-수정-in-painting-및-요소-교체) | 대화형 인페인팅 | 대화 맥락을 유지한 채 특정 디자인 요소 교체 및 부분 수정 |
| **Lab 3** | [Image-to-Image 스타일 변환](media_gen/ge_media.md#lab-3-사내-자산-기반-image-to-image-스타일-변환) | 멀티모달 이미지 업로드 | 사내 스케치/로고의 고유 형태를 보존하면서 시각 스타일 변환 |
| **Lab 4** | [비즈니스 인포그래픽 시각화](media_gen/ge_media.md#lab-4-비즈니스-인포그래픽-및-다이어그램-시각화) | 레이아웃 & 다이어그램 합성 | 디지털 마케팅 퍼널 및 클라우드 시스템 아키텍처 다이어그램 직관적 표현 |
| **Lab 5** | [마케팅 배너 제작 (Negative Space)](media_gen/ge_media.md#lab-5-카피라이트-공간negative-space을-고려한-마케팅-배너-제작) | 구도 및 여백 통제 | 광고 카피 문구(Typography) 배치를 위해 의도된 여백을 확보한 광고 배너 |
| **Lab 6** | [시네마틱 B-roll 클립 생성](media_gen/ge_media.md#lab-6-텍스트-프롬프트를-통한-시네마틱-b-roll-클립-생성) | Veo (Text-to-Video) | 카메라 동선(Dolly, Tilt)과 볼류메트릭 조명 지시를 반영한 고화질 영상 제작 |
| **Lab 7** | [정적 이미지 기반 모션 비디오](media_gen/ge_media.md#lab-7-정적-이미지-기반-모션-비디오-생성-image-to-video) | Veo (Image-to-Video) | 정적 제품 렌더링에 자연스러운 물리 역학과 카메라 줌인 모션 부여 |
| **Lab 8** | [대화형 비디오 편집 (분위기 전환)](media_gen/ge_media.md#lab-8-멀티턴-대화형-비디오-분위기-및-환경-전환-video-editing) | Video-to-Video 편집 | 기생성 비디오의 시간대(골든 아워), 기상 조건(비), 컬러 톤 대화형 변경 |
| **Lab 9** | [모바일 맞춤형 숏폼(9:16) 영상](media_gen/ge_media.md#lab-9-소셜-미디어-플랫폼-맞춤형-숏폼916-영상-제작) | 9:16 세로형 합성 | 모바일 소셜 채널용 360도 턴테이블 회전 제품 티저 영상 합성 |

---

### 🔹 트랙 3: 노코드 기본 에이전트 스튜디오 (`nocode_basic`)
> **매뉴얼**: [`nocode_basic/nocode_basic.md`](nocode_basic/nocode_basic.md)

| 랩 번호 | 실습 모듈명 | 연동 도구 및 모드 | 핵심 검증 목표 |
| :---: | :--- | :--- | :--- |
| **Lab 1** | [프롬프트 기반 에이전트 자동 생성](nocode_basic/nocode_basic.md#lab-1-대화형-프롬프트-기반-에이전트-자동-생성) | Agent Designer 대화 모드 | 자연어 대화만으로 전문 역할(시니어 테크 채용 평가관) 에이전트 즉각 구축 |
| **Lab 2** | [맞춤형 에이전트 구성 & 검색 연동](nocode_basic/nocode_basic.md#lab-2-빌더builder-기반-맞춤형-에이전트-수동-구성-검색-도구-연동) | Builder 모드 & Google Search | 지식 베이스(평가 기준 PDF) 바인딩 및 Google Search 도구 연결 |
| **Lab 3** | [에이전트 조직 공유 및 자동 실행](nocode_basic/nocode_basic.md#lab-3-에이전트-조직-공유-및-자동-실행-스케줄링) | 조직 RBAC & Cron 트리거 | 팀/부서 단위 권한 부여 및 주기적(매일 아침) 자동 실행 스케줄 설정 |
| **Lab 4** | [프롬프트 기반 워크플로우 에이전트](nocode_basic/nocode_basic.md#lab-4-프롬프트-기반-워크플로우-에이전트workflow-agent-자동-생성-및-최종-브리핑-구글드라이브에-저장) | 워크플로우 스튜디오 | Google Search 뉴스 수집, 위협 수준 분기, 사람 승인(HITL), Google Drive 자동 저장 |

---

### 🔹 트랙 4: 심화 워크플로우 에이전트 오케스트레이션 (`nocode_advance`)
> **매뉴얼**: [`nocode_advance/nocode_advance.md`](nocode_advance/nocode_advance.md)

| 랩 번호 | 실습 모듈명 | 빌더 노드 및 연동 기술 | 핵심 검증 목표 |
| :---: | :--- | :--- | :--- |
| **Lab 1** | [빈 캔버스 및 메일 송신 트리거 구성](nocode_advance/nocode_advance.md#lab-1-빈-캔버스-생성-및-메일-송신-트리거trigger-구성) | Empty Canvas, Email Trigger | `When an email is sent` 트리거 설정 및 메일 제목 필터링 (`부동산`, `아파트`) |
| **Lab 2** | [질문 분석 구조화 에이전트 노드](nocode_advance/nocode_advance.md#lab-2-step-1-질문분석_구조화_에이전트-knowledge-json-schema) | Knowledge + JSON Schema | 비정형 질문 메일을 6대 핵심 구조화 파라미터(`priority` 등)로 파싱 |
| **Lab 3** | [MCP 서버 연동 (20개년 지표 조회)](nocode_advance/nocode_advance.md#lab-3-step-2-mcp-서버mcp-realestate-연동-20개년-지표-조회) | `MCP Realestate` (Cloud Run) | `get_factors_range` 도구를 호출하여 2006~2025 기준금리/실거래가/미분양 수집 |
| **Lab 4** | [최신 시장 검색 및 종합 보고서 작성](nocode_advance/nocode_advance.md#lab-4-step-3-4-최신-시장-검색realest_research-및-종합-보고서-작성) | `Realest_research` + Gemini | 최신 웹 검색 결과와 20개년 정량 지표를 결합한 통합 자문 보고서 작성 |
| **Lab 5** | [조건 분기 및 사람 승인 (HITL)](nocode_advance/nocode_advance.md#lab-5-step-5-6-조건-분기condition-및-사람-승인request-info) | Condition 노드, Request info | `priority == 'High'` 조건 분기 처리 및 수석 자문역 사람 필수 승인 절차 |
| **Lab 6** | [분기별 액션 (이메일 발송 및 Drive 저장)](nocode_advance/nocode_advance.md#lab-6-step-7-8-분기별-실행-액션-이메일-발송-및-drive-저장) | Gmail Action, Drive Action | 승인 시 Gmail 회신 + Google Drive 보고서 저장, 일반 시 이메일 회신만 실행 |
| **Lab 7** | [시뮬레이션 테스트 및 배포](nocode_advance/nocode_advance.md#lab-7-시뮬레이션-테스트test-및-배포turn-on) | Test Runner, Turn on | 테스트 데이터 주입을 통한 노드별 데이터 흐름 검증 및 프로덕션 활성화 |

---

## 🔒 데이터 보안 및 거버넌스

- **모델 재학습 금지**: Gemini Enterprise에 입력된 모든 데이터는 기본 파운데이션 모델 재학습에 활용되지 않습니다.
- **권한 기반 격리**: Google Workspace ACL을 완벽 준수하여 권한이 있는 문서만 참조됩니다.
- **비밀정보 관리**: 개인 API 키나 토큰, `.env` 파일은 저장소에 절대 커밋하지 않습니다.
