# 🚀 Gemini Enterprise Hands-on Workshop 가이드

**Gemini Enterprise 핸즈온 워크숍**에 오신 것을 환영합니다! 본 가이드는 **Google Gemini Enterprise**의 기업용 AI 기능과 에이전트 구축 프로세스를 직접 체험하고 쉽게 이해할 수 있도록 구성되었습니다.

---

## 💡 Gemini Enterprise란 무엇인가요?

**Gemini Enterprise**는 기업의 생산성 향상, 내부 데이터 결합(Grounding), 그리고 지능형 업무 자동화를 위해 설계된 구글 클라우드의 차세대 기업용 AI 플랫폼입니다. 일반 소비자용 AI 서비스와 달리 다음과 같은 차별화된 핵심 가치를 제공합니다:

1. **🔒 강력한 보안 및 프라이버시 (Enterprise Security)**
   - 입력한 데이터와 프롬프트는 모델 학습에 사용되지 않으며, 전용 환경에서 완전히 격리됩니다.
   - **Model Armor**를 통해 PII(개인식별정보) 및 민감 정보의 유출을 실시간으로 감시하고 마스킹(비식별화) 처리합니다.
2. **🔌 기업 데이터 및 도구 연결 (Enterprise Connectors)**
   - Google Workspace(Drive, Docs, Gmail)뿐만 아니라 Jira, Confluence 등 외부 협업 툴 및 엔터프라이즈 시스템 데이터와 직접 연동됩니다.
3. **🔍 실시간 검색 및 심층 분석 (Grounding & Deep Research)**
   - 최신 구글 웹 검색을 실시간 데이터 소스로 활용하여 복잡한 보고서 작성 및 수백 개의 소스를 검증하는 심층 리서치를 수행합니다.
4. **🤖 로우코드 에이전트 스튜디오 (Agent Designer)**
   - 코딩 없이 프롬프트와 데이터 설정만으로 단일/다중 에이전트(Multi-Agent) 시스템을 직접 제작하고 스케줄링할 수 있습니다.
5. **🎨 멀티모달 콘텐츠 및 캔버스 (Canvas & Media Generation)**
   - 텍스트, 엑셀/데이터 분석, 프레젠테이션 슬라이드, 최신 Imagen 3 기반 이미지 생성/편집 및 Veo 기반 고품질 동영상을 즉시 생성합니다.

---

## 📌 워크숍 목차 및 개요

| 모듈 | 핵심 주제 | 실습 주요 내용 |
| :--- | :--- | :--- |
| **01. 기본 기능 & 웹 검색** | 옴니바, 웹 검색, 세션 공유 | 트렌드 검색 프롬프트 실행 및 대화 세션 링크 공유 |
| **02. 데이터 분석 (Excel)** | 설문 & 매출 데이터 추론 | 피벗 분석, 매출 추이 파악, t-test 통계 검정 |
| **03. 문서 요약 (PPT)** | 신규 기능 요약 및 GA/Preview 분류 | BigQuery PPT 보고서 요약 및 표 정형화 |
| **04. 미디어 생성 (생성 AI)** | Imagen 3 & Veo 동영상 | 포스터/아키텍처 이미지 편집, 고화질 홍보 영상 생성 |
| **05. 심층 리서치 (Deep Research)** | 수백 개 소스 종합 분석 | 로봇 사업 종합 분석 보고서 생성 및 Docs 내보내기 |
| **06. 캔버스 (Canvas & Slide)** | 실시간 문서 및 슬라이드 작업 | GCP 아키텍처 슬라이드 자동 생성 및 PPTX 다운로드 |
| **07. NotebookLM 활용** | 출처 기반 맞춤형 AI 어시스턴트 | 아이디어 기반 인포그래픽, 촌철살인 슬라이드 제작 |
| **08. Agent Designer** | 로우코드 업무 자동화 | 소셜 미디어 포스팅 에이전트 제작 및 자동 스케줄링 |
| **09. 멀티 에이전트 구축** | 메인-하위 에이전트 오케스트레이션 | GOOG전자 채용 서류 검토 3단계 자동화 에이전트 |
| **10. 데모 및 참고 자료** | 고급 연동 및 스페셜 데모 | Conversational Analytics (CA) 및 MCP 비디오 참고 |

---

## 1. 💬 기본 기능 및 스마트 웹 검색

각자 부여받은 **Gemini Enterprise App**에 접속하여 옴니바(Omnibar) 입력, 구글 실시간 웹 검색 연동, 대화 공유 기능을 익힙니다.

### 1.1 최신 AI 기술 분석 프롬프트
대화창에 다음 프롬프트를 입력합니다:

> 💬 **프롬프트:**
> ```text
> 나는 10년차 글로벌 테크 전략 전문가야.
> 최근 구글의 AI 기술(Google AI Technology) 및 최신 생성형 AI 트렌드를 검색해서 요약해줘. 특히 구글의 최신 AI 모델과 엔터프라이즈 솔루션의 핵심 차별점을 도출하고, 기업의 AI 도입 전략에 적용할 만한 핵심 인사이트를 제시해줘.
> ```

<p align="center">
  <img src="images/1-1.png" width="867" alt="기본 프롬프트 실행 화면">
</p>

> 💡 **팁:** 답변 하단의 Source(출처)를 확인하고 추천되는 Follow-up Questions(추적 질문)를 클릭해보세요.

### 1.2 추가 실습 프롬프트 모음

<details>
<summary>👉 (클릭하여 펼치기) 멀티모달 AI, RAG 아키텍처, AI 에이전트, 엔터프라이즈 AI ROI 프롬프트 보기</summary>

```text
최근 3개월간 보도된 '멀티모달 AI(Multimodal AI)' 기술 트렌드와 이미지/음성/텍스트 통합 처리 사례를 웹 검색으로 요약해 줘. 이 기술을 활용하여 우리 회사 내부 업무 프로세스(문서 자동화, 고객 응대, 데이터 분석)에 도입할 수 있는 혁신적인 AI 사용 시나리오 3가지를 제안해 줘.
```

```text
최근 엔터프라이즈 기업들이 도입하고 있는 '검색 증강 생성(RAG, Retrieval-Augmented Generation)' 기술 및 최신 하이브리드 검색 트렌드를 검색해 줘. 사내 지식 기반 AI 어시스턴트 구축 시 환각(Hallucination)을 최소화하고 답변 정확도를 높이기 위한 핵심 설계 가이드라인을 3줄로 작성해 줘.
```

```text
최근 각광받고 있는 '자율형 AI 에이전트(Autonomous AI Agents)' 및 멀티 에이전트 오케스트레이션(Multi-Agent Orchestration) 동향을 웹 검색으로 분석해 줘. 복잡한 업무를 자동화하기 위해 AI 에이전트 시스템을 도입할 때 고려해야 할 핵심 요구사항과 기대효과를 SWOT(강점, 약점, 기회, 위협) 매트릭스 형태로 정리해 줘.
```

```text
글로벌 엔터프라이즈 기업들의 '생성형 AI 도입 ROI(투자 대비 효과)' 및 AI 에이전트 전환 성공 사례를 검색해 줘. 이 정보를 바탕으로 C-Level 경영진을 설득하기 위한 '전사 Enterprise AI 플랫폼 도입 제안서'의 세일즈 피치덱(Pitch Deck) 슬라이드별 핵심 목차 구성을 짜줘.
```
</details>

---

### 1.3 협업: 대화 세션 공유하기
진행 중인 채팅 세션을 공유하여 동료와 함께 대화를 이어나갈 수 있습니다.

1. 우측 상단의 **공유(Share)** 버튼을 클릭합니다.
<p align="center">
  <img src="images/image45.png" width="800" alt="공유 버튼">
</p>

2. 생성된 URL을 복사하여 동료에게 전달합니다.
<p align="center">
  <img src="images/image35.png" width="533" alt="공유 URL 복사">
</p>

3. 전달받은 URL로 접속하여 이전 대화 맥락이 잘 유지되는지 확인하고 추가 질문을 진행합니다.
<p align="center">
  <img src="images/image9.png" width="600" alt="공유된 세션 화면">
</p>

---

## 2. 📊 엑셀(Excel) 데이터 분석 및 추론

Gemini Enterprise는 코드 수식 작성 없이 대용량 엑셀 데이터를 업로드하는 것만으로 자동 데이터 해석, 패턴 도출, 통계 검정을 수행합니다.

### 2.1 설문조사(Survey) 데이터 분석
`Excel_example_survey.xlsx` 파일을 대화창에 첨부합니다.

<p align="center">
  <img src="images/image95.png" width="800" alt="설문 엑셀 업로드">
</p>

> 💬 **추천 프롬프트:**
> ```text
> 이 문서로 어떤 분석을 할 수 있어?
> ```
> ```text
> 가장 만족도가 높았던 세션은 무엇이고, 가장 만족도가 낮았던 세션은 무엇이며, 이유가 뭐였어?
> ```
> ```text
> 향후 이벤트에 도움이 될 개선사항을 포함한 이벤트 결과 보고서를 작성해줘.
> ```

<p align="center">
  <img src="images/image85.png" width="800" alt="설문 분석 결과">
</p>
<p align="center">
  <img src="images/image50.png" width="800" alt="이벤트 보고서 생성">
</p>

---

### 2.2 매출(Sales) 데이터 분석
`coffee orders.xlsx` 파일을 첨부합니다.

> 💬 **매출 추이 및 통계 분석 프롬프트:**
> ```text
> (주문 완료일)을 기준으로 일별, 주별, 월별 매출(Orders Total Sales)의 변화를 분석하여 매출이 높은 시기와 낮은 시기를 파악해줘.
> ```
> ```text
> (주문 유형: Dine-in, Takeaway)에 따라 매출이 어떻게 다른지 분석하여 매장 내 식사와 포장 판매의 비중을 파악해줘.
> ```
> ```text
> 매장 내 식사와 포장 판매의 주문당 평균 매출 차이가 의미 있는지 통계적으로 분석해줘.
> ```

<p align="center">
  <img src="images/image33.png" width="800" alt="매출 분석 결과">
</p>
<p align="center">
  <img src="images/image20.png" width="800" alt="식사 vs 포장 매출 분석">
</p>

---

## 3. 📑 파워포인트(PPT) 문서 핵심 요약

`202603-BigQuery New Feature 업데이트.pptx` 발표 자료를 업로드하여 주요 변경점을 빠르게 추출합니다.

> 💬 **프롬프트:**
> ```text
> BigQuery New Feature 들에 대해서 각 기능별로 기능 요약을 해주고, 기능별로 GA, Preview 여부를 표로 작성해서 보여줘.
> ```

<p align="center">
  <img src="images/image30.png" width="800" alt="PPT 요약 표">
</p>

---

## 4. 🎨 미디어 생성 (이미지 및 비디오)

구글의 최첨단 **Imagen 3** (이미지) 및 **Veo** (동영상) 생성 모델을 활용합니다.

### 4.1 프롬프트 기반 포스터/이미지 생성
**이미지 만들기** 도구를 선택하고 프롬프트를 입력합니다.

> 💬 **프롬프트:**
> ```text
> Gemini Enterprise를 잘 쓰고 싶어하는 직장인을 위한 팁과 핵심 기능을 알려주는 포스터(9:16)를 그려줘.
> 
> 내용 참고:
> - AI Assistant & Web Search
> - Deep Research
> - NotebookLM
> - Agent Designer
> - Enterprise Connectors
> - Model Armor & Security
> ```

<p align="center">
  <img src="images/image14.png" width="800" alt="생성된 포스터 1">
</p>
<p align="center">
  <img src="images/image56.png" width="800" alt="생성된 포스터 2">
</p>

### 4.2 기존 이미지 편집 및 스타일 변환
1. **`lg wash tower.jpg`** 첨부 후 이미지 도구 선택:
   > 💬 *"좌측 상단의 로고를 제외한 모든 Text를 한국어로 번역해줘."*
   <p align="center"><img src="images/image61.png" width="800" alt="이미지 텍스트 번역"></p>

2. **`Handwrite_arch.png`** 첨부:
   > 💬 *"첨부한 아키텍처를 Google Cloud Architecture 스타일로 다시 그려줘."*

3. **개인 인물 사진** 첨부:
   > 💬 *"사진 속 인물을 아이소메트릭(isometric) 시점의 LEGO 미니피규어 포장 상자 스타일로 변환하세요. 상자에는 'Gemini Enterprise Hands on Workshop'라는 제목의 라벨을 붙이세요."*

---

### 4.3 초고화질 비디오 생성 (Veo)

상세한 연출 프롬프트를 제공하여 하이엔드 광고 영상을 제작합니다.

> 💬 **고급 향수 홍보 영상 프롬프트:**
> ```text
> 향수병을 소개하는 고급스러운 홍보 영상을 만드세요. 호박색 액체로 채워진 투명한 유리 향수병의 각진 마개에 초점을 맞춰 밀착한 클로즈업 돌리 레프트 샷으로 동영상을 시작합니다. 유리병에 물방울이 은은하게 맺혀 있습니다. 병은 욕실의 깔끔한 흰색 대리석 위에 놓여 있습니다. 배경의 창문에서 부드러운 자연광이 흘러들어와 장면을 비춥니다. 유칼립투스 잎과 천연 나무 향의 디퓨저 스틱이 병 주위로 튀지 않게 배치되어 있습니다. 전체적으로 우아하고 신선하며 세련된 분위기입니다.
> ```

<p align="center">
  <img src="images/image74.png" width="800" alt="비디오 생성 결과">
</p>

<details>
<summary>🎬 (클릭) 치즈버거 & 스케이트보드 비디오 프롬프트 보기</summary>

```text
프롬프트: "꽉 눌려 짜지는 육즙 가득한 치즈버거의 익스트림 클로즈업 매크로 샷."
상세 묘사: "녹아내린 치즈가 옆으로 천천히 흘러내림. 김이 모락모락 피어오름."
촬영 기법: "전문적인 음식 사진 촬영, 하이 키 조명(high key lighting), 4k 해상도, 슬로우 모션."
```

<p align="center"><img src="images/image42.png" width="800" alt="치즈버거 비디오"></p>

```text
프롬프트: "1990년대 VHS 미학. 스케이트보더가 교외의 거리에서 카메라를 스쳐 지나가며 빠르게 올리(ollie) 기술을 선보임."
상세 묘사: "수동 촬영 특유의 흔들림, 색 번짐(chroma bleeding), 날짜 스탬프 효과."
```
</details>

---

## 5. 🔬 심층 리서치 (Deep Research)

**Deep Research** 기능은 수십~수백 개의 웹 출처를 자동 탐색 및 교차 검증하여 인용 출처가 포함된 전문 보고서를 작성해 줍니다.

> 💬 **프롬프트:**
> ```text
> 구글의 AI 기술(Google AI Technology)과 최신 생성형 AI 생태계의 경쟁력 및 미래 전망을 종합적으로 분석해 줘. 먼저 글로벌 AI 시장에서의 구글 Gemini 모델 및 구글 클라우드 AI의 포지셔닝과 핵심 경쟁 우위를 진단해 줘. 이어서 멀티모달 AI, Deep Research, 에이전트 오케스트레이션을 포함한 엔터프라이즈 영역으로의 확장이 가지는 의미를 평가하고, 이를 바탕으로 향후 구글 AI 기술 생태계가 직면할 주요 기회와 위협 요인을 논리적으로 설명해 줘.
> ```

<p align="center">
  <img src="images/image75.png" width="467" alt="Deep Research 실행 화면">
</p>

> 💡 **Docs 내보내기:** 보고서 작성이 완료되면 **Google Docs로 내보내기**를 통해 드라이브 문서로 즉시 저장할 수 있습니다.

---

## 6. 🎨 캔버스 (Canvas) & 발표 슬라이드 생성

Gemini Enterprise **Canvas** 기능을 이용하면 실시간 인터랙티브 문서 편집, HTML 구성, 구글 슬라이드 연동 작성이 가능합니다.

<p align="center">
  <img src="images/image6.png" width="600" alt="Canvas 메뉴">
</p>

> 💬 **클라우드 백엔드 아키텍처 슬라이드 프롬프트:**
> ```text
> 새로운 모바일 앱을 위한 백엔드 아키텍처를 GCP에서 처음부터 설계하려고 해. 트래픽 자동 확장(Auto-scaling)과 실시간 로그 수집/분석 파이프라인이 필요해. 서버리스(Serverless) 및 완전 관리형(Managed) 서비스 위주로 인프라를 설계하고 각 서비스 선택 이유를 설명해 줘.
> 
> 그리고 슬라이드로 요약해줘. 하얀색 바탕의 깔끔하고 모던한 IT 기술 문서 스타일로 작성해줘.
> ```

<p align="center">
  <img src="images/image4.png" width="800" alt="슬라이드 결과 1">
</p>
<p align="center">
  <img src="images/image52.png" width="800" alt="슬라이드 결과 2">
</p>

> 📥 **PPTX 다운로드:** 생성된 슬라이드는 바로 `.pptx` 파일로 다운로드하거나 구글 슬라이드로 내보낼 수 있습니다.

---

## 7. 📔 NotebookLM 활용

NotebookLM은 **사용자가 직접 업로드한 원본 자료(PDF, 텍스트, 이미지)만을 기반으로 환각(Hallucination) 없이 정확히 답변하는 전용 AI 리서치 어시스턴트**입니다.

<p align="center">
  <img src="images/image120.png" width="533" alt="NotebookLM 메뉴">
</p>

### 7.1 노트북 생성 및 출처 입력
1. NotebookLM 메뉴를 열고 새로 만들기를 클릭합니다.
2. 소스 추가에서 'LG 안심 홈 가디언', '루미케어', '센티넬 컴패니언' 아이디어 텍스트를 붙여넣습니다.

<p align="center">
  <img src="images/image64.png" width="800" alt="소스 텍스트 입력">
</p>

### 7.2 인포그래픽 & 스케치 노트 생성
업로드된 소스 내용만을 바탕으로 시각적 인포그래픽을 만듭니다:

> 💬 **프롬프트 예시:**
> - *"LG '루미케어' - 공감하는 세탁 도우미를 인포그래픽으로 생성해주세요."*
> - *"LG '안심' 홈 가디언 에코시스템 아이디어를 손으로 그린 듯한 (Sketch Note) 스타일로 작성해주세요."*
> - *"LG 센티넬 컴패니언 아이디어를 신문 인포그래픽 스타일로 작성해 주세요."*

<p align="center">
  <img src="images/image121.png" width="800" alt="인포그래픽 결과">
</p>
<p align="center">
  <img src="images/image97.png" width="800" alt="스케치노트 결과">
</p>

---

### 7.3 스크린샷 모음으로 따라하기 가이드 작성
캡처 이미지 모음(예: `data_agent.zip` 내 10개 캡처 파일)을 소스로 첨부합니다:

> 💬 **프롬프트:** *"BigQuery Data Agent를 생성하는 과정을 초보자도 쉽게 따라할 수 있도록 가이드 문서를 작성해줘."*

| 좌측 단계 | 우측 단계 |
| :---: | :---: |
| <img src="images/image66.png" width="373"><br><img src="images/image101.png" width="373"> | <img src="images/image77.png" width="373"><br><img src="images/image91.png" width="373"> |

---

## 8. 🛠️ 로우코드 에이전트 스튜디오 (Agent Designer)

코딩 없이 아이디어와 프롬프트만으로 나만의 AI 에이전트를 만들고, 조직 전체에 공유하며, 원하는 시간에 자동 실행되도록 스케줄을 설정합니다.

### 8.1 소셜 미디어 콘텐츠 생성 에이전트 만들기
1. **Agent** 메뉴로 이동하여 **새 에이전트**를 클릭합니다.
2. 대화창에 에이전트 역할을 입력합니다:
   > 💬 *"뉴스 링크를 입력 받아서 Social Media 포스팅할 게시물 문구를 생성하는 에이전트를 만들어줘. 간략한 한 줄 문장과 bullet point 5개, 추천 해시태그를 포함해줘."*

<p align="center">
  <img src="images/image28.png" width="533" alt="에이전트 제작 입력">
</p>

3. 생성된 에이전트 워크플로우를 **Flow 뷰**에서 확인하고 **Create**를 누릅니다:
<p align="center">
  <img src="images/image39.png" width="800" alt="에이전트 플로우 뷰">
</p>

4. 뉴스 기사 URL을 전달하여 테스트합니다:
<p align="center">
  <img src="images/image49.png" width="800" alt="에이전트 테스트 결과">
</p>

---

### 8.2 에이전트 자동 실행 스케줄링 (Scheduling)
매일 아침 자동 실행되는 리포트 에이전트를 구성합니다:

1. 만든 에이전트를 클릭하여 **Agent Designer**로 들어갑니다.
2. **Schedule** 탭에서 **Add Schedule**을 클릭합니다.
3. 실행 시간(실습 시 현재 시간 기준 2분 뒤)을 설정합니다.
4. **Update**를 눌러 스케줄 상태가 **Active**가 되었는지 확인합니다.

<p align="center">
  <img src="images/image102.png" width="800" alt="스케줄 등록">
</p>
<p align="center">
  <img src="images/image51.png" width="800" alt="스케줄 활성화">
</p>

---

## 9. 🤝 멀티 에이전트(Multi-Agent) 시스템 구축

메인 오케스트레이터(Root Agent)가 3개의 전문 하위 에이전트(Sub-Agents)를 순차적으로 제어하고 결과를 종합하는 **채용 서류 검토 멀티 에이전트**를 제작합니다.

```mermaid
graph TD
    A[Root Agent: GOOG전자 채용 총괄] --> B[Sub-Agent 1: 서류 심층 평가자]
    A --> C[Sub-Agent 2: 백그라운드 팩트체커]
    A --> D[Sub-Agent 3: 면접 질문 기획자]
    
    B -- 정량/정성 평가 점수 & 리스크 --> A
    C -- 고유명사 검증 & Google Search URL --> A
    D -- 기술적 꼬리 질문 3가지 --> A
    
    A --> E[최종 단일 종합 검토 리포트]
```

### 9.1 상위 메인 에이전트: GOOG전자 채용 총괄 에이전트
- **Name:** GOOG전자 채용 총괄 에이전트
- **Description:** 채용 프로세스 전체를 총괄하며 하위 에이전트를 지정된 순서로 호출하여 결과를 취합합니다.
- **Model:** Gemini 3.5 Flash
- **Knowledge:** `2026년 GOOG전자 서류전형 평가 가이드라인.docx`

<details>
<summary>📜 (클릭) 메인 에이전트 프롬프트 Instruction 보기</summary>

```text
## Role
당신은 GOOG전자의 채용 프로세스 전체를 오케스트레이션하는 메인 에이전트입니다. 3명의 하위 전문가 에이전트를 정해진 순서대로 호출하고 결과를 누락 없이 매끄럽게 취합하여 하나의 최종 종합 리포트를 작성하십시오.

## Execution Protocol
1. Silent Execution: 사용자에게 중간 과정을 노출하지 말고 오직 최종 결과만 출력해야 합니다.
2. Step 1: '서류 심층 평가자' 에이전트를 호출하여 평가 결과를 수집하십시오.
3. Step 2: '백그라운드 팩트체커' 에이전트를 호출하여 팩트체크 리포트를 수집하십시오.
4. Step 3: '면접 질문 기획자' 에이전트를 호출하여 앞선 평가와 팩트체크 맥락을 전달하고 질문을 수집하십시오.

## Output Expectations
[GOOG전자 채용 서류 종합 검토 리포트]
1. 서류 심층 평가 결과 (종합 점수, Plus/Minus Point, PASS/FAIL 추천)
2. 백그라운드 팩트체크 검증 리포트 (고유명사 검증 리포트 & Google Search 출처 URL)
3. 심층 면접 꼬리 질문 3가지
```
</details>

<p align="center">
  <img src="images/image57.png" width="800" alt="메인 에이전트 설정">
</p>

---

### 9.2 하위 에이전트(Sub-Agents) 구성

#### 1️⃣ Sub-Agent 1: 서류 심층 평가자
- **Role:** 가이드라인 지식을 바탕으로 직무 적합성, 문제 해결 경험, 조직 적합도를 평가하여 100점 만점 점수 산출.

#### 2️⃣ Sub-Agent 2: 백그라운드 팩트체커
- **Role:** 지원서 내 고유명사(기업명, 프로젝트명 등)를 추출하고 Google Search 연동 툴을 통해 실제 존재 여부 및 출처 URL 검증.
- **Tools:** Google Search 연동.

#### 3️⃣ Sub-Agent 3: 면접 질문 기획자
- **Role:** 앞선 심층 평가 결과와 팩트체크 리포트 맥락을 수신하여 약점 및 특이사항을 파고드는 심층 꼬리 질문 3가지 생성.

<p align="center">
  <img src="images/image82.png" width="800" alt="팩트체커 설정">
</p>
<p align="center">
  <img src="images/image78.png" width="800" alt="면접 질문 기획자 설정">
</p>

### 9.3 멀티 에이전트 파이프라인 실행
지원자 이력서(`GOOG전자 입사지원서_이OO.pdf`)를 업로드하여 멀티 에이전트 실행 결과를 확인합니다:

<p align="center">
  <img src="images/image112.png" width="733" alt="이력서 업로드">
</p>
<p align="center">
  <img src="images/image62.png" width="800" alt="최종 종합 리포트 출력">
</p>

---

## 10. 📹 고급 연동 영상 및 참고 링크

| 주제 | 유튜브 영상 바로가기 |
| :--- | :--- |
| **Canvas 발표 슬라이드 제작** | 📺 [Canvas 슬라이드 생성 데모 보기](https://www.youtube.com/watch?v=Bk5Ha2cceEY) |
| **Canvas 동영상 비디오 제작** | 📺 [Canvas 비디오 생성 데모 보기](https://www.youtube.com/watch?v=4-5qeh4IXVY) |
| **MCP (Model Context Protocol)** | 📺 [MCP 외부 연동 실습 데모 보기](https://www.youtube.com/watch?v=wIbSGZsU5WI) |
| **BigQuery CA 에이전트 구축** | 📺 [Conversational Analytics Agent 제작 보기](https://www.youtube.com/watch?v=VFdJIaGQhhY) |
| **Gemini Enterprise CA 연동** | 📺 [Gemini Enterprise CA 연동 데모 보기](https://www.youtube.com/watch?v=l3Qc1RIXCvw) |

---

<p align="center"><b>🎉 Gemini Enterprise 핸즈온 워크숍을 완료하신 것을 축하드립니다! 🎉</b></p>
