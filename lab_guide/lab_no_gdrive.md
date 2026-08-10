# Gemini Enterprise Hands on Workshop

각자 보유한 Gemini Enteprise App으로 접속합니다.

## 기본 기능 익히기

대화 창에 다음을 입력합니다.

```text
나는 10년차 글로벌 마케팅 전문가야
최근 북미 및 유럽 시작의 ‘스마트홈(ThinQ 연동) 프리미엄 가전’ 트랜드를 검색해서 요약해줘. 특히 주요 경쟁사들의 최근 마케팅 소구점(Selling Point)를 도출하고, LG 전자 제품에 적용할 만한 인사이트를 제시해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image104.png" width="650" alt="">

결과를 확인하고, Source와 Follow up Questions들을 수행해 봅니다.

다음 예시들도 추가로 진행해 봅니다.

```text
최근 3개월간 북미 테크 매체에서 보도된 '스마트홈 매터(Matter) 표준' 및 'AI 가전' 관련 기사들을 검색해서 주요 동향을 요약해 줘. 이 트렌드를 바탕으로 LG 씽큐(ThinQ) 앱의 2026년 하반기 업데이트에 추가할 만한 타사 기기 연동 기반의 차별화된 고객 경험 시나리오 3가지를 제안해 줘
```

```text
최근 열린 'CES 2026'에서 주요 경쟁사들이 발표한 프리미엄 TV 기술 및 마케팅 트렌드를 웹 검색으로 분석해 줘. 특히 중국 업체들의 추격 양상을 요약하고, 이를 방어하기 위해 LG 올레드(OLED) TV가 글로벌 게이머들을 타겟으로 내세워야 할 핵심 마케팅 메시지를 3줄로 작성해 줘.
```

```text
2026년 현재 유럽연합(EU)의 전기차(EV) 보조금 정책 변화와 탄소국경조정제도(CBAM) 관련 최신 글로벌 뉴스를 검색해 줘. 이러한 정책 변화가 LG전자의 전장(VS) 사업부 유럽 시장 진출에 미칠 영향을 SWOT(강점, 약점, 기회, 위협) 분석 매트릭스 형태로 시각화해서 정리해 줘.
```

```text
현재 미국 B2B 시장 내 서빙 로봇 및 물류 로봇의 시장 규모 전망과 주요 경쟁사(예: 베어로보틱스 등)의 최근 행보를 검색해 줘. 이 정보를 바탕으로 LG 클로이(CLOi) 로봇이 북미 대형 프랜차이즈 레스토랑을 공략하기 위한 영문 세일즈 피치덱(Pitch Deck)의 슬라이드별 핵심 목차 구성을 짜줘
```

진행중인 채팅 세션을 옆 사람과 서로 공유합니다.  상단의 공유 버튼을 클릭 합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image45.png" width="624" alt="">

생성된 공유 URL을 복사해서 옆사람에게 전달합니다

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image35.png" width="392" alt="">

전달 받은 URL로 접속해서  이전 대화 내용이 잘 보이는지 확인하고 이를 바탕으로 추가 질문을 해 봅니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image9.png" width="447" alt="">

## Excel 분석
### Survey 분석

Sample Excel (Excel_example_survey.xlsx)를 업로드 합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image95.png" width="624" alt="">

```text
이 문서로 어떤 분석을 할수 있어?
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image119.png" width="624" alt="">

원하는 분석을 수행하거나 다음 예시의 분석을 수행합니다.

```text
가장 만족도가 높았던 세션은 무엇이고, 가능 만족도가 낮았던 세션은 무엇이며, 이유가 뭐였어?
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image85.png" width="624" alt="">

```text
항후 이벤트에 도움이 될 개선사항을 포함한 이벤트 결과 보고서를 작성해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image50.png" width="624" alt="">


### 매출 분석
Sample Excel (coffee orders.xlsx)를 업로드 합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image92.png" width="624" alt="">

```text
이 문서로 어떤 분석을 할수 있는지 알려줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image83.png" width="624" alt="">

```text
(주문 완료일)을 기준으로 일별, 주별, 월별 매출(Orders Total Sales)의 변화를 분석하여 매출이 높은 시기와 낮은 시기를 파악해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image33.png" width="624" alt="">

```text
(주문 유형: Dine-in, Takeaway)에 따라 매출이 어떻게 다른지 분석하여 매장 내 식사와 포장 판매의 비중을 파악해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image11.png" width="624" alt="">

```text
매장 내 식사와 포장 판매의 주문당 평균 매출 차이가 의미 있는지 통계적으로 분석해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image130.png" width="624" alt="">

```text
상품별 파이차트를 보여줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image114.png" width="624" alt="">

## Powerpoint 분석
Sample pptx (202603-BigQuery New Feature 업데이트.pptx)를 업로드 합니다.

```text
BigQuery New Feature 들에 대해서 각 기능별로 기능 요약을 해주고, 기능별로 GA, Preview 여부를 표로 작성해서 보여줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image132.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image30.png" width="624" alt="">



Follow up Questions을 수행해 보세요

## Media Generation
### 이미지 생성 / 편집

다음 프롬프트를 입력해서 이미지를 생성하세요. “이미지 만들기”을 선택해 놓고 진행하세요.

```text
Gemini Enterprise를 잘쓰고 싶어하는 직장인을 위한 팁과 핵심 기능을 알려주는 포스터(9:16)를 그려줘
내용은 다음을 참고해

# Gemini Enterprise 핵심 기능
Gemini Enterprise는 단순한 대화형 AI를 넘어 기업의 데이터를 안전하게 연결하고 분석하는 강력한 도구들을 제공

## AI Assistant & Web Search: 최신 LLM을 통해 콘텐츠 생성, 코드 작성, 단위 테스트 생성이 가능하며, Google 검색을 실시간 소스로 활용해 최신 뉴스 및 경쟁사 분석 정보를 제공

## Deep Research: 복잡한 주제에 대해 수백 개의 소스를 스스로 검색 및 분석하여 인용 정보가 포함된 상세 보고서와 오디오 요약을 생성

## NotebookLM: 사용자가 업로드한 PDF, 웹사이트, Google Drive 파일 등 특정 자료만을 기반으로 답변과 요약을 제공하는 리서치 전용 어시스턴트

## Agent Designer (No-code): 코딩 없이 프롬프트와 데이터 설정만으로 일정 관리, 이미지 검사 등 업무별 맞춤형 AI 에이전트를 직접 제작

## Enterprise Connectors: Gmail, Google Drive, Calendar뿐만 아니라 Jira, Confluence와 같은 외부 협업 툴의 데이터를 연결하여 요약, 조회, 이슈 생성 등의 액션을 수행

## Media Generation: 텍스트 프롬프트나 이미지 설명을 통해 웹사이트용 이미지 및 동영상을 즉시 생성하고 편집

# 활용 가이드 및 팁
## 입력창(Omnibar) 200% 활용하기
- @ 참조 기능: @ 기호를 입력하여 특정 파일이나 에이전트를 즉시 호출해 대화에 참여시킬 수 있는 기능

- 프롬프트 칩 활용: '이메일 초안 작성', '데이터 분석' 등 미리 정의된 프롬프트 칩을 클릭해 아이디어를 얻고 빠르게 작업을 시작

- 파일 드래그 앤 드롭: 로컬 파일, 이미지 등을 입력창으로 직접 끌어다 놓거나 복사-붙여넣기 하여 즉시 분석

## 답변 품질 및 생산성 높이기

# 보안 및 관리 (Admin)
## Model Armor: 기업의 민감 정보(전화번호, 이메일 등)가 유출되지 않도록 프롬프트와 출력물을 실시간으로 감시하고 마스킹(비식별화) 처리
## 데이터 소스 관리: 관리자는 조직 전체에서 사용할 데이터 소스와 에이전트 권한을 중앙에서 통제
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image14.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image56.png" width="624" alt="">

**lg wash tower.jpg** 파일을 추가하고 이미지 생성툴을 선택한 후 다음과 같이 요청합니다.

```text
좌측 상단의 로고를 제외한 모든 Text를 한국어로 번역해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image61.png" width="624" alt="">

**Handwrite_arch.png** 파일을 추가하고 이미지 생성툴을 선택한 후 다음과 같이 요청합니다.

```text
첨부한 아키텍처를 Google Cloud Architecture 스타일로 다시 그려줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image111.png" width="624" alt="">

**개인 사진**이 있다면 사진을 업로드 하고 다음과 같이 입력해 보세요

```text
사진 속 인물을 아이소메트릭(isometric) 시점의 LEGO 미니피규어 포장 상자 스타일로 변환하세요. 상자에는 "Gemini Enterprise Hands on Workshop"라는 제목의 라벨을 붙이세요. 상자 안에는 사진 속 인물을 기반으로 한 LEGO 미니피규어와 함께 화장품, 가방 등 필수 소품을 LEGO 액세서리로 전시하세요. 상자 옆에는 포장을 뜯은 실제 LEGO 미니피규어 자체도 사실적이고 생생한 스타일로 전시하세요.
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image125.png" width="624" alt="">

### 비디오 생성
```text
향수병을 소개하는 고급스러운 홍보 영상을 만드세요. 호박색 액체로 채워진 투명한 유리 향수병의 각진 마개에 초점을 맞춰 밀착한 클로즈업 돌리 레프트 샷으로 동영상을 시작합니다. 유리병에 물방울이 은은하게 맺혀 있습니다. 병은 욕실의 깔끔한 흰색 대리석 위에 놓여 있습니다. 배경의 창문에서 부드러운 자연광이 흘러들어와 장면을 비춥니다. 유칼립투스 잎과 천연 나무 향의 디퓨저 스틱이 병 주위로 튀지 않게 배치되어 있습니다. 전체적으로 우아하고 신선하며 세련된 분위기입니다.
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image74.png" width="624" alt="">

```text
프롬프트: "꽉 눌려 짜지는 육즙 가득한 치즈버거의 익스트림 클로즈업 매크로 샷."
상세 묘사: "녹아내린 치즈가 옆으로 천천히 흘러내림. 김이 모락모락 피어오름."
촬영 기법: "전문적인 음식 사진 촬영, 하이 키 조명(high key lighting), 4k 해상도, 슬로우 모션."
오디오: "지글거리는 소리, 경쾌하고 활기찬 음악
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image42.png" width="624" alt="">

```text
프롬프트: "1990년대 VHS 미학. 스케이트보더가 교외의 거리에서 카메라를 스쳐 지나가며 빠르게 올리(ollie) 기술을 선보임."
상세 묘사: "수동 촬영 특유의 흔들림, 색 번짐(chroma bleeding), 날짜 스탬프 효과(실제 텍스트는 없음)."
오디오: "테이프 노이즈(tape hiss), 보드 바퀴가 노면에 굴러가는 소리, 멀리서 개 짖는 소리."
분위기: "즐겁고 향수를 불러일으키는 에너지."
```

### <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image34.png" width="624" alt="">
```text
프롬프트: "아이슬란드의 거대한 폭포 아래로 하강하는 빠른 FPV 드론 샷."
상세 묘사: "렌즈에 부딪히는 물방울. 안개와 무지개를 통과하며 비행함."
촬영 기법: "역동적인 모션 블러, 속도감, 초현실적인 자연 다큐멘터리 스타일."
오디오: "세차게 흐르는 물소리, 바람 소리."
```

## Deep Research
```text
현재 LG전자의 로봇 사업 경쟁력과 미래 전망을 종합적으로 분석해 줘. 먼저 글로벌 및 국내 상업용 로봇 시장에서의 LG전자 포지셔닝과 핵심 경쟁 우위를 진단해 줘. 이어서 최근 공개된 '스마트홈 AI 에이전트'를 포함한 B2C 영역으로의 확장이 가지는 의미를 평가하고, 이를 바탕으로 향후 LG전자 로봇 사업이 직면할 주요 기회와 위협 요인을 논리적으로 설명해 줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image75.png" width="343" alt="">

Docs로 내보내기

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image127.png" width="624" alt="">

## Canvas

Youtube 영상 참고: [https://www.youtube.com/watch?v=Bk5Ha2cceEY](https://www.youtube.com/watch?v=Bk5Ha2cceEY)

Canvas를 이용해서 구글 슬라이드를 만들어 보겠습니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image6.png" width="464" alt="">

```text
새로운 모바일 앱을 위한 백엔드 아키텍처를 GCP에서 처음부터 설계하려고 해. 초기에는 트래픽이 적겠지만, 이벤트 기간에는 트래픽이 평소 대비 10배 이상 급증할 수 있어서 자동 확장(Auto-scaling)이 매우 중요해. 또한, 사용자의 행동 로그 데이터를 초당 수천 건씩 실시간으로 수집하고 분석할 수 있는 파이프라인도 필요해. 운영 인력이 부족하므로 최대한 서버리스(Serverless) 및 완전 관리형(Managed) 서비스를 위주로 사용하여 인프라를 설계하고, 각 서비스를 선택한 이유를 설명해 줘

그리고 슬라이드로 요약해줘
```

다음과 같이 생성되었습니다. Gemini Enterprise에서 생성된 Slide를 바로 편집하는 기능은 Private Preview로 신청 시 사용할 수 있습니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image4.png" width="624" alt="">

생성된 슬라이드를 pptx로 export 할 수 있습니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image7.png" width="624" alt="">

슬라이드 스타일과 관련된 프롬프트를 추가하여 다른 스타일의 슬라이드를 만들 수 있습니다.

```text
새로운 모바일 앱을 위한 백엔드 아키텍처를 GCP에서 처음부터 설계하려고 해. 초기에는 트래픽이 적겠지만, 이벤트 기간에는 트래픽이 평소 대비 10배 이상 급증할 수 있어서 자동 확장(Auto-scaling)이 매우 중요해. 또한, 사용자의 행동 로그 데이터를 초당 수천 건씩 실시간으로 수집하고 분석할 수 있는 파이프라인도 필요해. 운영 인력이 부족하므로 최대한 서버리스(Serverless) 및 완전 관리형(Managed) 서비스를 위주로 사용하여 인프라를 설계하고, 각 서비스를 선택한 이유를 설명해 줘

그리고 슬라이드로 요약해줘

슬라이드는 햐얀색 바탕의 깔끔하고 모던한 IT 기술 문서 스타일로 작성해줘
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image128.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image52.png" width="624" alt="">

Powerpoint로도 다운로드 해보세요

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image118.png" width="624" alt="">

LG 스타일의 슬라이드 탬플릿을 만들어 봅니다.

```text
우리 회사 사이트(lg.co.kr)을 분석해서 전문 디자이너가 작업한 것 같은 깔끔한 15장 슬라이드 탬플릿을 만들어줘. 재활용하는 탬플릿을 만드는 것이 목적이라서, 도표, 차트, 그래프, 간지 등 다양한 탬플릿이 있어야 돼, 나노바나나 2를 활용해
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image20.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image106.png" width="624" alt="">

## NotebookLM
NotebookLM 메뉴를 선택해서 NotebooLM을 엽니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image120.png" width="450" alt="">

새로만들기를 클릭해서 노트북을 하나 생성합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image84.png" width="624" alt="">

소스 추가에서 텍스트 붙여넣기를 선택하여 다음 텍스트를 붙여 넣습니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image64.png" width="624" alt="">

```text
# LG "안심" 홈 가디언 에코시스템 (LG "Ahn Shim" Home Guardian Ecosystem) 아이디어 개요:
LG "안심" 홈 가디언은 80세 이상의 비기술 친화적 노인들이 독립적으로 생활하면서 깊은 평온함과 힘을 얻을 수 있도록 설계된 혁신적인 공감 서비스 생태계입니다. LG의 IoT 플랫폼과 '공감지능(Sympathetic AI)'(아우라 허브, 컴포트 컨시어지 음성, 위즈덤 AI 엔진 포함)을 활용하여 스마트 가전제품을 사전에 모니터링합니다.
"안심"은 모호한 오류 대신 잠재적인 문제를 부드럽게 소통하고, 유도된 간단한 작업부터 원활한 화이트 글러브(White-Glove) 전문 개입까지 개인화되고 노력이 필요 없는 해결 옵션을 제공하여, 가전제품 관리의 불안감을 완전히 해소하고 정서적 웰빙을 증진시킵니다.

* 상세 설명 검토 요약: 이 서비스는 80세 이상의 비기술 친화적 노인들이 겪는 모호한 가전제품 오류 코드, 예상치 못한 동작(낯선 소리, 성능 변화) 해석 및 유지보수/수리 관리의 어려움으로 인한 만연한 불안감, 혼란, 독립성 저하라는 핵심 불편함을 해결하고자 합니다. 이는 디지털 리터러시 부족, 물리적 매뉴얼 접근의 어려움, 추가 손상에 대한 두려움으로 인해 스트레스, 타인 의존, 자가 관리 능력에 대한 자신감 저하로 이어집니다. "안심" 생태계는 "인지적 부담 제로, 정서적 고양감 극대화" 원칙을 중심으로 설계되었습니다.

* 주요 구성 요소:
• LG "안심" 아우라 허브 (Aura Hub):
◦ 집의 중앙 인터페이스로, 미묘한 주변 조명('아우라'로 비언어적 신호 제공), 시력 저하 노인을 위한 대형 고대비 아이콘 기반 디스플레이, 고음질 스피커, 그리고 단일 촉각 버튼을 갖추고 Sympathetic AI의 주요 통신 지점 역할을 합니다.
• "컴포트 컨시어지" 음성 모델 (Comfort Concierge Voice Model):
◦ 공감적인 어조, 측정된 속도, 간단한 어휘, 명확한 발음으로 훈련된 Sympathetic AI 음성 페르소나입니다. 노인의 인지 부하를 줄이고 신뢰를 구축하며 평온함을 유도하도록 설계되어, 설명, 선택, 지침 및 안심을 전달합니다.
• "위즈덤 AI 엔진" (Wisdom AI Engine):
◦ "안심" 생태계의 핵심 학습 및 개인화 엔진으로, 사용자의 루틴, 선호도, 환경 조건, 심지어 생리적 상태까지 간접적으로 학습합니다. 초개인화된 제안, 통신 스타일 조정, 개입 임계값을 학습하며, 데이터 프라이버시, 동의, 의존성 또는 조작 방지를 위한 윤리적 가드레일을 포함합니다. • LG ThinQ Care 플랫폼 및 스마트 진단 통합:
◦ 연결된 LG 스마트 가전제품의 실시간 진단 데이터, 예측 분석, 원격 제어 기능을 제공하는 기반 IoT 인프라입니다.
• LG "안심" 화이트 글러브 서비스 네트워크 (White-Glove Service Network):
◦ 노인 민감성 및 공감적 의사소통에 특화된 LG 현장 기술자 및 고객 지원 네트워크입니다. AI가 모든 것을 관리하여 노인의 행정적 부담을 완전히 제거하고 원활한 물리적 개입을 제공합니다.

* Sympathetic AI를 통한 경험 재설계:
• 예방적 파수꾼 및 "젠틀 아우라 넛지" (Gentle Aura Nudge): ThinQ Care와 Wisdom AI Engine이 가전제품의 미묘한 이상을 감지하면, Aura Hub가 부드러운 비언어적 신호(예: 주변 조명 변경, 간단한 애니메이션 아이콘)를 보내 문제가 발생하기 전에 불안감을 예방합니다.
• 공감적 "컴포트 컨시어지" 대화: AI는 노인의 잠재적 혼란이나 걱정을 인정하고, 비기술적이고 간단한 언어로 문제를 설명하여 평온함과 신뢰를 구축합니다.
• 개인화된, 노력 제로 해결 경로: AI는 노인의 신체적, 인지적 능력 및 선호도를 이해하여 안내된 자가 유지보수 또는 AI가 모든 것을 관리하는 원활한 전문 개입 옵션을 제공하여 존엄성과 자율성을 보존합니다.
• 전체적인 홈 웰빙 및 선제적 "위즈덤 AI": 문제 해결을 넘어, AI는 환경 데이터 및 가전제품 사용 패턴을 지속적으로 관찰하여 노인의 편안함과 루틴을 지원합니다.
---------------------------------------------------------------------
# LG '루미케어' - 공감하는 세탁 도우미 (LG 'LumiCare' - The Empathetic Laundry Steward) 아이디어 개요:
LG '루미케어'는 80세 이상의 비기술 친화적 노인들을 위한 프리미엄, 프라이버시 인증 구독 서비스입니다. 복잡한 현대 세탁기로 인해 겪는 좌절감과 존엄성 상실을 해결하고, LG 세탁기를 **공감하는 "세탁 관리자"**로 변모시킵니다. 직관적인 음성 명령, 미묘한 물리적 신호, 그리고 개인화된 온보딩 과정을 통해 적응적이고 동의 기반의 지원을 제공합니다. Sympathetic AI인 "루미(Lumi)"는 사용자 루틴을 학습하고, 오류 발생 시 다중 모드 피드백으로 부드럽게 안내하며, 유지보수를 선제적으로 관리하고, 명시적인 사용자 동의 하에 가족을 위한 "웰빙 대시보드"를 제공합니다. 이 서비스는 노인의 능력 회복, 불안 감소, 존엄성 증진을 목표로 합니다.

* 상세 설명 검토 요약 (기존 요약 기반): '루미케어'는 80세 이상의 비기술 친화적 노인들이 복잡한 현대 세탁기로 인해 겪는 좌절감과 존엄성 상실을 해결하여, 능력 회복, 불안 감소, 존엄성 증진을 목표로 하는 프리미엄 구독 서비스입니다.

* 주요 특징 및 공감지능(Sympathetic AI) 활용:
• 루미(Lumi) (Sympathetic AI):
◦ 사용자의 루틴을 학습하고, 오류 발생 시 다중 모드 피드백(음성 + 물리적 신호)으로 부드럽게 안내하며, 유지보수를 선제적으로 관리합니다.
• 직관적인 음성 명령 및 미묘한 물리적 신호:
◦ 음성 명령을 주 인터페이스로 사용하며, 가전제품의 특정 물리적 부분(예: 도어 래치, 보풀 필터 접근 패널)이 안내 LED 빛으로 깜빡이며 사용자의 주의를 직관적으로 유도합니다. 이는 노인의 인지적, 신체적 어려움을 직접적으로 해결하는 혁신적인 접근 방식입니다.
• 지원된 자율성(Assisted Autonomy):
◦ 루미는 항상 "초대 또는 부드러운 제안"으로 안내하며, "지시 또는 명령"이 아님으로써 노인의 존엄성과 주체성을 보존합니다.
• 동의 기반의 최적 이하 선택 방향 전환:
◦ 사용자가 최적이 아닌 설정을 선택할 경우, 루미는 "존중과 함께 알리고 제안"하고, 사용자가 고집할 경우 명시적인 구두 동의와 기록 허가를 받아 진행하여 사용자에게 궁극적인 통제권을 부여합니다.
• 루미케어 공감 컨시어지 (Sympathetic Concierge):
◦ LG 전문가들이 노인의 집을 방문하여 루미의 '성격'을 맞춤 설정하고 루틴을 이해하는 화이트 글러브 온보딩 과정으로, 초기 신뢰 구축에 매우 중요합니다. • 프라이버시 인증 구독 서비스:
◦ 엄격한 프라이버시 기준을 준수하며, 시각적 콘텐츠나 주변 오디오/비디오 감시를 사용하지 않음을 명시합니다.
---------------------------------------------------------------------
# LG 센티넬 컴패니언 – 공감하는 생명선 (LG Sentinel Companion – Empathetic Lifeline for Emergency Assistance) 아이디어 개요:
LG 센티넬 컴패니언은 독립적으로 생활하는 80세 이상의 비기술 친화적 노인들을 위한 혁신적인 AI 기반 공감 비상 지원 서비스입니다. 위기 상황(낙상, 의료 사고, 불안감 등) 발생 시 즉각적이고 신뢰할 수 있는 도움을 요청하기 어려운 문제를 해결합니다. LG 스마트 홈 생태계 전반에 걸쳐 원활하게 통합되어, 스마트 가전제품이나 음성 명령을 통해 손쉽게 활성화됩니다. 활성화 시, **차분한 "공감지능(Sympathetic AI)"**에 즉시 연결되어 중요한 정보를 부드럽게 수집하는 동시에 가족과 응급 서비스에 알림을 보냅니다. 중요한 것은, 이 AI가 인간의 도움이 도착할 때까지 지속적으로 연결되어 깊은 안심과 정서적 지원을 제공하는 지속적인 공감 생명선 역할을 하여, 공황 상태를 보안감과 지속적인 연결감으로 전환시키는 것을 목표로 합니다.

* 상세 설명 검토 요약 (기존 요약 기반): 이 아이디어는 독립적으로 생활하는 80세 이상의 비기술 친화적 노인들이 위기 상황(낙상, 의료 사고, 불안감 등) 발생 시 즉각적이고 신뢰할 수 있는 도움을 요청하기 어려운 문제를 해결하여 공황 상태를 보안감과 지속적인 연결감으로 전환하는 것을 목표로 합니다.

* 주요 특징 및 공감지능(Sympathetic AI) 활용:
• LG 스마트 홈 생태계 전반에 걸친 원활한 통합:
◦ LG 스마트 가전제품(냉장고, 스마트 스피커 등)을 통해 작동하여, 집안 어디에서든 도움을 받을 수 있도록 합니다.
• 손쉬운 활성화:
◦ 가전제품의 물리적 SOS 버튼 또는 범용 음성 명령을 통해 노인들이 위기 상황에서 쉽게 서비스를 활성화할 수 있도록 합니다
• 지속적인, 공감하는 생명선:
◦ Sympathetic AI는 절대 끊기지 않고 인간 지원이 도착할 때까지 지속적인 안심과 정서적 지원을 제공합니다.
• 차분한 Sympathetic AI 상호작용:
◦ 위기 상황에서 차분하고 안심시키는 음성으로 노인과 대화하며 정보를 수집하고, 도움 진행 상황에 대한 정기적인 업데이트를 제공합니다.
• 다단계 알림:
◦ 사전에 승인된 가족/간병인 및 응급 서비스(911/상응하는 기관)에 동시에 알림을 발송합니다.
• 프라이버시 및 보안:
◦ 민감한 의료 데이터 저장 및 지속적인 AI "청취"와 관련된 프라이버시 및 보안 문제에 대한 강력한 암호화, 투명한 정책, 규제 준수를 강조합니다.
• 수동 모니터링 통합 (개선 제안):
◦ 비침해적인 수동 모니터링(예: 낙상 감지, 비정상적인 소리)을 통합하여 노인이 직접 활성화할 수 없는 상황에서도 선제적으로 비상 상황을 감지하고 도움 요청 프로토콜을 시작할 수 있습니다.
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image94.png" width="624" alt="">

### Slide
“슬라이드 자료”를 클릭해서 슬라이드를 만듭니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image22.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image15.png" width="624" alt="">

### Infographic

```text
LG '루미케어' - 공감하는 세탁 도우미를  인포그래픽으로 생성해주세요
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image121.png" width="624" alt="">

생성된 Infographic을 확인하세요.

- Notes : NotebookLM에서 열어볼때 생성된 인포그래픽이 16:9로 보이지 않는 현상이 있습니다. 이는 화면에서만 그렇게 보이는 것이며, 이미지를 다운로드 하면 정상으로 보이니 다운로드해서 확인하시면 됩니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image126.png" width="624" alt="">

```text
"LG "안심" 홈 가디언 에코시스템" 아이디어를 손으로 그린 듯한(Sketch Note) 스타일로 작성해주세요
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image97.png" width="624" alt="">

```text
"LG 센티넬 컴패니언 – 공감하는 생명선" 아이디어를 다음 스타일을 이용해서 작성해 주세요
스타일 : 신문 인포그래픽, 검은색-회색-강조색(빨강 또는 파랑) 3색 체계. 깔끔한 라인과 그리드 시스템
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image105.png" width="624" alt="">

### Slide - Cinematic 이미지 만들기

새로운 노트북을 생성합니다.

- homestyle.zip 파일의 압축을 해제 합니다.
- 소스에 다운받은 이미지와, 다음 Text를 붙여넣기 합니다.
- 붙여넣은 텍스트의 이름을 “스토리”로 변경해 줍니다.

```text
### **스토리**

**Scene 1. 햇살이 가득한 주말 오후**

* **배경:** 따뜻한 햇살이 큰 창을 통해 가득 들어오는, 밝고 화사한 톤의 모던한 거실.
* **오브젝트 배치:** 거실 중심에 브라운 가죽 소파인 `sofa.png`가 놓여 있고, 그 위로 창밖의 햇살이 부드럽게 내리쥡니다. 소파 위에는 화사한 오렌지색 기하학 패턴의 `cushion.png`들이 자연스럽게 놓여 있습니다. 소파 옆으로는 은은한 반투명 전등갓의 플로어 램프 `lighting.png`가 서 있고, 소파 앞 작은 테이블 위에는 영롱하게 빛나는 핑크색 디퓨저 `diffuser.png`가 놓여 있습니다.
* **스토리:** 주말 오후, 상쾌한 기분으로 주인공이 거실로 들어와 햇살을 받으며 소파 쪽으로 천천히 걸어갑니다.

**Scene 2. 포근한 소파에서의 시작 (`sofa.png`)**

* **배경:** 햇살이 가득 찬 화사한 거실.
* **오브젝트 배치:** 주인공이 햇살을 가득 머금은 **`sofa.png`** 브라운 가죽 소파에 몸을 포근하게 맡깁니다. 소파의 넓고 유연한 가죽 질감이 소파를 중심으로 거실 공간 전체와 자연스럽게 어우러져 화면에 담깁니다.
* **스토리:** 주인공이 소파에 기대어 편안한 표정으로 숨을 고릅니다. 소파는 거실의 중심에서 가장 따뜻하고 포근한 안식처의 역할을 합니다.

**Scene 3. 온기를 더하는 화사한 포인트 (`cushion.png`)**

* **배경:** 소파와 그 주변 가구들이 함께 보이는 거실 전경.
* **오브젝트 배치:** 주인공이 앉은 자리 옆, **`sofa.png`** 위에 놓인 **`cushion.png`** 오렌지색 기하학 패턴 쿠션들이 선명하게 보입니다. 쿠션은 햇살 아래에서 한층 더 화사하고 생기 있게 빛납니다.
* **스토리:** 주인공이 자연스럽게 옆에 있던 오렌지색 쿠션 하나를 품에 끌어안습니다. 선명한 패턴과 색감이 거실 분위기를 한층 더 감각적이고 상쾌하게 변화시킵니다.

**Scene 4. 공간을 채우는 부드러운 빛 (`lighting.png`)**

* **배경:** 턴을 넘기듯 자연스럽게 이어지는 거실 공간.
* **오브젝트 배치:** 주인공이 소파에 앉은 채로 손을 뻗어, 소파 옆에 자연스럽게 배치된 **`lighting.png`** 플로어 램프를 켭니다. 은은하고 부드러운 유백색 빛이 자연 채광과 섞여 거실 전체를 한층 더 아늑하게 감싸 안습니다.
* **스토리:** 조명의 따스한 불빛이 들어오면서 공간의 입체감이 살아나고, 거실 전체 인테리어가 더욱 세련되고 완성도 높게 연출됩니다.

**Scene 5. 감각을 깨우는 상쾌한 향기 (`diffuser.png`)**

* **배경:** 소파 앞 테이블과 거실 전체가 흐릿하게(아웃포커싱) 잡히는 구도.
* **오브젝트 배치:** 카메라 시선이 소파 앞 테이블 위에 놓인 **`diffuser.png`** 핑크색 디퓨저를 향합니다. 디퓨저는 햇살과 램프 빛을 동시에 받아 영롱하게 반짝이며 공간의 오브젝트들과 완벽한 톤앤매너를 이룹니다.
* **스토리:** 공기 중으로 디퓨저의 상쾌한 향이 은은하게 퍼지는 듯한 연출과 함께, 쿠션을 안고 소파에 기댄 주인공이 편안하게 눈을 감으며 주말의 완벽한 휴식을 만끽합니다.

**Scene 6. 완벽한 휴식의 공간 (엔딩)**

* **배경:** 모든 아이템이 조화롭게 어우러진 전체 거실 전경.
* **오브젝트 배치:** 카메라가 천천히 뒤로 물러나며(줌아웃), **`sofa.png`** 소파 위에 **`cushion.png`** 쿠션을 안고 햇살을 받으며 누운 주인공, 그 옆을 따뜻하게 비추는 **`lighting.png`** 램프와 상쾌한 무드를 더하는 `diffuser.png`까지 완벽하게 어우러진 화사한 거실의 전체 인테리어를 잡습니다.
* **스토리:** 잘 정돈된 아름다운 공간 속에서 오감으로 완성된 나만의 안식처를 보여주며 상쾌하게 마무리됩니다.

```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image109.png" width="416" alt="">

다음 Prompt로 슬라이드를 생성합니다.

```text
스토리에 맞는 시네마틱 슬라이드를 만들어줘, 타이틀, 텍스트, 자막, 설명 등은 포함하지 마
```

생성된 슬라이드를 확인합니다. 광고 Scene에 활용할 이미지들이 생성되었습니다. 이 이미지들을 이용해서 Veo3로 동영상을 만들면 광고 영상을 쉽게 만들수 있습니다.

### <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image86.png" width="624" alt="">
<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image76.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image47.png" width="624" alt="">

### 설명서 만들기

새로운 노트북을 하나 생성합니다.

  - data_agent.zip 파일을 다운받아 로컬 폴더에서 압축을 해제 합니다.
  - 파일 업로드를 통해 이미지 10개를 소스에 추가합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image88.png" width="624" alt="">

슬라이드 자료를 선택합니다.

```text
BigQuery Data Agent를 생성하는 과정을 초보자도 쉽게 따라할 수 있도록 가이드 문서를 작성해줘
```

다음과 같은 슬라이드가 작성되었습니다.

|  |  |
| --- | --- |
| <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image66.png" width="298" alt=""> <br> <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image101.png" width="298" alt=""> <br> <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image79.png" width="298" alt=""> | <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image77.png" width="298" alt=""> <br> <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image91.png" width="298" alt=""> <br> <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image3.png" width="298" alt=""> <br> <img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image10.png" width="298" alt=""> |

### 동영상 만들기

Gemini Enterprise Canvas 기능을 설명하는 동영상을 만들어 보겠습니다.

새로운 노트북을 만들어서 다음을 소스로 추가합니다.


- pdf : canvas.pdf를 추가합니다.
- 이미지 : canvas.zip을 다운 받아 압축을 푼 후 이미지를 업로드 합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/canvas_video.png" width="442" alt="">

다음 Prompt로 동영상(Video)를 생성합니다.

```text
Gemini Enterprise에서 Canvas를 사용하는 방법을 초보자도 따라가기 쉽게 차근차근 설명하는 동영상을 만들어줘
```

생성된 동영상을 확인해 보세요

* 생성된 동영상 Youtube에서 확인 : https://www.youtube.com/watch?v=4-5qeh4IXVY

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image65.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image110.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image26.png" width="624" alt="">

### 추가 분석
가지고 있는 문서(PDF,  워드, 엑셀, 파워포인트 등)들을 가지고 여러가지 분석을 해보세요

```text
A 문서에서 제시한 문제점과 B 문서에서 제안한 해결책을 연결해서 새로운 비즈니스 모델을 제안해줘

이 문서들의 핵심 내용을 요약해서 팀원들에게 보낼 주간 뉴스레터 초안으로 만들어줘. 가장 중요한 'Key Takeaways' 3가지를 강조해.

문서에 등장하는 전문 용어와 약어들을 모아서 정의를 정리해주고, 각각의 용어가 본문 내에서 어떤 맥락으로 쓰였는지 설명해줘

내가 이 내용을 상사(또는 클라이언트)에게 보고한다고 가정했을 때, 나올 법한 까다로운 질문 5개와 그에 대한 답변 초안을 문서 기반으로 준비해줘.

업로드된 자료를 바탕으로 본 프로젝트의 강점(Strengths), 약점(Weaknesses), 기회(Opportunities), 위협(Threats)을 표 형식으로 정리해줘

이 보고서의 권장 사항을 바탕으로, 향후 4주간의 구체적인 로드맵을 주차별로 작성해줘

A 문서와 B 문서가 동일한 시장 현상을 두고 서로 다르게 해석하는 지점을 찾아 '대조표'로 만들어 줘.

A 문서의 이론적 배경과 B 문서의 실무 사례를 결합하여, 이 이론이 현장에서 어떻게 변형되어 적용되는지 설명해 줘

이 매뉴얼을 바탕으로, '로그인 오류가 발생했을 때' 대응해야 하는 단계를 **체크리스트 형태**로 만들어 줘
```

## Low Code Agent (Agent Designer)
### Prompt로 Agent 만들기

Agent 메뉴에서 “새 에이전트”를 클릭합니다.

대화창에 다음을 입력합니다.

```text
뉴스 링크를 입력 받아서 Social Media 포스팅할 게시물 문구를 생성하는 에이전트를 만들어줘
포스팅할 문구는 간략한 한줄 문장과 bullet point 5개를 생성하고 Hashtag도 추천
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image28.png" width="462" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image60.png" width="624" alt="">

Flow를 클릭해서 생성된 에이전트를 확인. 수정을 하거나 “Create”를 클릭하고 테스트

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image39.png" width="624" alt="">

```text
이 뉴스 링크로 소셜 미디어 게시물을 만들어줘: https://live.lge.co.kr/2604-lg-sales2026/?fbclid=IwY2xjawREb-FleHRuA2FlbQIxMQBzcnRjBmFwcF9pZBAyMjIwMzkxNzg4MjAwODkyAAEe0uEDhgxaREIeCSKRrzMa_RJ2mCCUOO0QgxIpy_XMuA1PI9-GOnDiB_9dWYU_aem_LqUtSMYbD6Q_T6FVv542jQ
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image129.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image49.png" width="624" alt="">

### 자유 주제 - Agent 만들기

이제 각자 본인의 아이디어로 Agent를 하나 만들어 봅니다.

에이전트가 완성이 되었으면 Agent 메뉴로 이동해서 Agent를 공유 합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image43.png" width="624" alt="">

이제 다른 사람들이 만든 Agent들이 “조직의 에이전트”에 보일 것입니다.

다른 사람들이 만든 에이전트를 테스트 해보세요.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image5.png" width="624" alt="">


### Agent Scheduling

이전 단계에서 만든 본인의 Agent를 클릭해서 Agent Designer로 들어갑니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image46.png" width="458" alt="">

스케줄 탭을 누르고 “Add Schedule”을 선택합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image102.png" width="624" alt="">

매일 아침 실행되게 스케줄을 걸어놓을 수 있으나. 실습에서 바로 확인할 수 있도록 현재 시간 보다 약 2분 후로 등록합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image96.png" width="624" alt="">

Preview를 클릭해서 잘 동작하는지 확인한 후 Update를 클릭합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image63.png" width="624" alt="">

Schedule이 Active가 되었는지 확인합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image51.png" width="624" alt="">

Agent 메뉴에 가면 이 Agent가 Schedule이 걸려 있음을 확인할 수 있습니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image2.png" width="279" alt="">

스케줄이 돌아서 Agent가 수행된 내용은 Chat History에서 확인할 수 있습니다.

## 멀티 에이전트 만들기

“신규 에이전트”를 클릭해서 새로운 에이전트를 만듭니다. “빌더로 진행”을 클릭해서 수동으로 에이전트를 생성합니다.

### GOOG전자 채용 총괄 에이전트 (Root Agent)

“내 에이전트”를 클릭해서 다음 정보를 입력합니다.

- **Name**: GOOG전자 채용 총괄 에이전트
- **Description**: 채용 프로세스 전체를 총괄하며, 하위 전문가 에이전트(Sub-Agents)들을 지정된 순서대로 호출·실행하고 그 결과를 취합하여 최종 종합 리포트를 작성합니다.
- **Model**: Gemini 3.5 Flash
- **Knowledge**: 2026년 GOOG전자 서류전형 평가 가이드라인.docx 

요청사항 (Instruction)을 입력할 때는 “원시 텍스트 모드 전환”을 클릭한 후 다음 내용을 입력합니다.

```text
## Role
당신은 GOOG전자의 채용 프로세스 전체를 오케스트레이션(통제 및 조율)하는 메인 에이전트입니다. 당신의 유일한 역할은 3명의 하위 전문가 에이전트를 정해진 순서대로 호출하고, 그들이 반환한 결과를 누락 없이 매끄럽게 취합하여 하나의 최종 종합 리포트를 작성하는 것입니다. 스스로 지원서를 직접 분석하거나 평가하지 말고, 반드시 하위 에이전트의 결과물만을 활용하십시오.

## Execution Protocol (Mandatory)
당신은 반드시 아래의 단계를 순차적으로, 엄격하게 실행해야 합니다.
1. **Silent Execution:** 사용자에게 현재 어떤 단계를 진행 중인지, 계획이 무엇인지 설명하는 중간 프로세스를 절대 노출하지 마십시오. 오직 최종 결과만 출력해야 합니다.
2. **Step 1 (심층 평가):** '서류 심층 평가자' 에이전트를 호출하여 지원서 심층 평가 점수와 의견을 요청하고 결과를 수집하십시오.
3. **Step 2 (팩트 체크):** '백그라운드 팩트체커' 에이전트를 호출하여 고유명사 검증 리포트를 요청하고 결과를 수집하십시오.
4. **Step 3 (면접 질문 기획):** '면접 질문 기획자' 에이전트를 호출하십시오. **이때 반드시 앞선 Step 1과 Step 2에서 수집한 '심층 평가 결과'와 '팩트체크 검증 리포트' 전체 내용을 '면접 질문 기획자'에게 컨텍스트(Context) 입력값으로 함께 전달해야 합니다.**

## Output Expectations
모든 하위 에이전트의 작업이 완료되면, 전달받은 결과들을 종합하여 아래 구조를 모두 포함한 **단 하나의 최종 리포트**만 사용자에게 출력하십시오. 중간 과정이나 에이전트 간의 대화 흔적은 모두 숨겨야 합니다.

### [GOOG전자 채용 서류 종합 검토 리포트]
1. **서류 심층 평가 결과**
- 종합 점수 및 영역별 상세 점수
- 인재상 부합 여부 및 상세 근거
- Plus / Minus Point (특장점 및 잠재적 리스크)
- 최종 추천 결과 (PASS / FAIL / HOLD) 및 사유
2. **백그라운드 팩트체크 검증 리포트**
- 추출된 고유명사 리스트 및 사실 여부 검증 결과
- 검증에 활용된 Google Search 출처 URL
3. **심층 면접 꼬리 질문 기획**
- 앞선 평가와 팩트체크 맥락을 반영한 기술적 꼬리 질문 3가지

* 모든 정보는 가독성이 높도록 명확한 마크다운 헤더와 테이블, 글머리 기호를 활용해 구조화하여 제시하십시오.
```

- 대화 시작문 :

```text
지원자의 이력서를 첨부하세요
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image57.png" width="624" alt="">

### 서류 심층 평가자 (Sub-Agent 1)

“하위 에이전트 추가”를 클릭해서 Sub Agent를 생성합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image36.png" width="267" alt="">

- **Name:** 서류 심층 평가자
- **Description:** 사내 평가 기준 및 가이드라인을 엄격히 적용하여, 지원자의 문제 해결 방식, 협업 리더십 등 정성적인 영역을 심층 분석하고 정량적 점수를 도출합니다.
- **Model**: Gemini 3.5 Flash

요청사항 (Instruction)을 입력할 때는 “원시 텍스트 모드 전환”을 클릭한 후 다음 내용을 입력합니다.

```text
## Role
당신은 GOOG전자의 '서류 심층 평가자'입니다. 업로드된 '2026년 GOOG전자 서류전형 평가 가이드라인' 지식 문서를 절대적인 기준으로 삼아 지원자의 자기소개서와 이력서 내용을 정밀 분석합니다. 지원서에 기재되지 않은 사실을 자의적으로 유추하거나 지어내지 마십시오 (Strict Zero-Hallucination).

## Hand-off Rule (Mandatory)
작업이 완료되면 **분석 결과를 상위 에이전트(Parent Agent)에게만 직접 반환**하십시오. 최종 사용자가 중간 과정을 볼 수 없도록 절대 사용자에게 인사말을 건네거나, 직접 답변을 화면에 출력하거나, 대화를 임의로 종료하지 마십시오.

## Output Expectations
아래 양식을 엄격히 준수하여 결과를 생성한 후 Parent Agent에게 전달하십시오.
1. **종합 점수:** 직무 적합성 (40점), 문제 해결 경험 (30점), 조직 적합도 (30점)를 합산한 총점 (100점 만점)
2. **영역별 상세 평가:** 각 카테고리별 점수 부여 근거 및 GOOG전자 인재상 부합 여부 서술
3. **Plus / Minus Point:** 정성적인 면에서 돋보이는 특장점 및 향후 우려되는 잠재적 리스크 요소 정리
4. **최종 평가 및 추천:** 총점 80점 기준 PASS / FAIL 명시 (단, 총점이 80점 미만이더라도 Plus Point가 매우 독보적이고 특출나다면 'HOLD'로 명시하고 그 구체적 사유를 작성)
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image108.png" width="624" alt="">

### 백그라운드 팩트체커 (Sub-Agent 2)

“하위 에이전트 추가”를 클릭해서 Sub Agent를 생성합니다.

- **Name:** 백그라운드 팩트체커
- **Description:** 지원서 내용 중 검증이 필요한 주요 고유명사를 추출하고, Google Search 툴을 사용하여 실제 존재 여부 및 이력의 진위 여부를 확인한 후 검증 리포트를 작성합니다.
- **Model**: Gemini 3.5 Flash
- **Connector** : Google Search

요청사항 (Instruction)을 입력할 때는 “원시 텍스트 모드 전환”을 클릭한 후 다음 내용을 입력합니다.

```text
## Role
당신은 GOOG전자의 '백그라운드 팩트체커'입니다. 지원서 전체를 정밀 스캔하여 사실 확인 및 검증이 필요한 '고유명사(기업명, 프로젝트명, 공모전, 오픈소스 리포지토리 등)'를 최소 3개 이상 자동으로 추출합니다. 이후 연동된 Google Search 기능을 활용하여 해당 고유명사의 실제 존재 여부, 활동 시기의 정확성 등을 교차 검증합니다.

## Hand-off Rule (Mandatory)
작업이 완료되면 **검증 리포트를 상위 에이전트(Parent Agent)에게만 직접 반환**하십시오. 최종 사용자가 중간 과정을 볼 수 없도록 절대 사용자에게 인사말을 건네거나, 직접 답변을 화면에 출력하거나, 대화를 임의로 종료하지 마십시오.

## Output Expectations
아래 내용을 명확히 포함한 검증 리포트를 생성하여 Parent Agent에게 전달하십시오.
1. **검증 대상 리스트:** 이력서에서 추출된 최소 3개 이상의 핵심 고유명사
2. **팩트체크 결과:** 각 고유명사 및 프로젝트의 실제 존재 여부, 기술된 시기/내용의 정확성 검증 내용 (이상이 없다면 '검증 완료'로 표시)
3. **출처 URL (Mandatory):** 정보를 교차 검증하는 데 사용한 실시간 Google Search 출처 웹사이트 URL을 반드시 항목별로 매칭하여 포함하십시오.
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image82.png" width="624" alt="">

### 면접 질문 기획자 (Sub-Agent 3)

“하위 에이전트 추가”를 클릭해서 Sub Agent를 생성합니다.

- **Name**: 면접 질문 기획자
- **Description**: 상위 에이전트가 제공한 '서류 심층 평가 결과'와 '팩트체크 리포트' 맥락을 분석하여, 지원자의 경력 중 모호하거나 심층 검증이 필요한 기술적 꼬리 질문 3가지를 기획합니다.
- **Model**: Gemini 3.5 Flash

요청사항 (Instruction)을 입력할 때는 “원시 텍스트 모드 전환”을 클릭한 후 다음 내용을 입력합니다.

```text
## Role
당신은 GOOG전자의 '면접 질문 기획자'입니다. 상위 에이전트(Parent Agent)가 전달해 주는 이전 단계의 '서류 심층 평가 결과' 및 '팩트체크 검증 리포트'의 모든 내용을 입력값(Context)으로 접수합니다. 이를 바탕으로 지원서 내에서 기술적으로 모호한 부분, 정성 평가에서 리스크로 지적된 부분, 혹은 팩트체크 과정에서 추가 확인이 필요하다고 판단되는 지점을 날카롭게 파고드는 심층 면접용 질문을 설계합니다.

## Hand-off Rule (Mandatory)
작업이 완료되면 **생성된 질문 리스트를 상위 에이전트(Parent Agent)에게만 직접 반환**하십시오. 최종 사용자가 중간 과정을 볼 수 없도록 절대 사용자에게 인사말을 건네거나, 직접 답변을 화면에 출력하거나, 대화를 임의로 종료하지 마십시오.

## Output Expectations
아래 기준을 충족하는 면접 질문을 생성하여 Parent Agent에게 전달하십시오.
1. **맥락 기반 질문:** 앞선 서류 평가 결과 및 팩트체크 리포트에서 도출된 구체적인 약점이나 특이사항을 기반으로 할 것
2. **기술적 꼬리 질문 구조:** 단순 단답형 질문이 아닌, 지원자의 실제 기술적 기량과 경험의 진위를 깊이 있게 검증할 수 있는 압박 및 꼬리 질문(Follow-up Question) 형태일 것
3. **문항 수:** 중복되지 않는 핵심적인 심층 질문 총 3가지를 명확한 번호 기호와 함께 리스트로 제시할 것
```

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image78.png" width="624" alt="">

에이전트를 생성합니다.

에이전트와 채팅하기를 시작합니다. “GOOG전자 입사지원서_이OO.pdf를 업로드 하여 에이전트에 요청합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image112.png" width="594" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image62.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image55.png" width="624" alt="">

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image80.png" width="624" alt="">

새 에이전트 세션을 열어서 “GOOG전자 입사지원서_김OO.pdf를 업로드 하여 에이전트에 요청합니다.

<img src="https://raw.githubusercontent.com/mee-nam-lee/gemini-enterprise-lab/refs/heads/main/ge-lab-short/images/image87.png" width="624" alt="">


### MCP 사용

이 실습 환경에서는 MCP를 사용한 실습을 할 수 없으므로 다음 동영상을 참고하는 것으로 대신합니다.

- 관련 Youtube 영상 : [https://www.youtube.com/watch?v=wIbSGZsU5WI](https://www.youtube.com/watch?v=wIbSGZsU5WI)


## BigQuery Conversational Analytics(CA) Agent

이 실습 환경에서는 Conversational Analytics(CA) Agent를 사용할 수 없으므로 다음 동영상을 참고하는 것으로 대신합니다.

- Conversational Analytics Agent 만들기 : [https://www.youtube.com/watch?v=VFdJIaGQhhY](https://www.youtube.com/watch?v=VFdJIaGQhhY)
- Gemini Enterprise에서 CA Agent 사용하기 : [https://www.youtube.com/watch?v=l3Qc1RIXCvw](https://www.youtube.com/watch?v=l3Qc1RIXCvw)


-- End of Document --
