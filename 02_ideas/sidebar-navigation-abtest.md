> **📄 요약 ·** 사이드바 A/B 원본 컨셉(IF/THEN/BECAUSE). → 정식 설계는 01_experiments/02_sidebar/로 승격됨.

추가 a/b test 컨셉
Cover
주요 참고 자료
메타 : https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/
카테고리 테스트
📝 [A/B Test] Sidebar Navigation Optimization for Categorization Fluency

🛠️ IF: 무엇을 어떻게 바꾸는가? (개입) 핵심 액션: 사이드바 메뉴에서 감성 요소였던 .json, .tsx, .md 같은 파일 확장자를 과감히 지우고, 유저가 가장 많이 찾는 핵심 메뉴(Projects, Events)를 폴더 깊숙한 곳에서 꺼내 최상단에 배치합니다.

의도: 겉보기에 예쁜 '개발자 가상 작업공간'이라는 콘셉트보다, 유저가 원하는 메뉴를 스트레스 없이 찾는 '실질적 기능성'에 우선순위를 두겠다는 뜻입니다.

📈 THEN: 어떤 비즈니스 결과를 기대하는가? (지표) 기대 효과: 핵심 메뉴로 진입하는 클릭률(CTR)이 눈에 띄게 오르고, 길목이 부드러워진 덕분에 최종 목적인 스터디/행사 등록률(Enrollment Rate)까지 연쇄적으로 상승합니다. 혹은 13기 프로젝트 알림 신청 과 같은 전환율 관련 항목이 상승

의도: 탐색 단계에서 발생하는 자잘한 이탈(Drop-off)을 막아주면, 최종 목적지인 '유저 참여(Conversion)'라는 큰 지표까지 자연스럽게 견인할 수 있다는 퍼널(Funnel) 논리입니다.

🧠 BECAUSE: 왜 이런 현상이 일어나는가? (심리학적 근거) 이 가설의 가장 핵심이 되는 뇌 과학적 분석입니다.

2차 해독 과정(Secondary Decoding Process)의 제거: 현재 UI에서는 유저가 Events.json이라는 메뉴를 볼 때 뇌에서 [Events.json] ➡️ '어라, 개발 파일인가?' ➡️ '아하, 캘린더/행사 메뉴구나!'라는 추가적인 해석 과정을 거쳐야 합니다. 아주 찰나의 순간이지만 뇌의 연산 장치를 쓰게 만드는 '인지적 마찰'입니다.

범주화 유창성(Categorization Fluency)의 극대화: 확장자를 지우고 메뉴를 밖으로 꺼내놓으면 유저의 뇌는 생각할 필요도 없이 [Projects = 스터디], [Events = 행사]로 직관적으로 분류(Categorization)해 버립니다. 메뉴를 해석하는 데 드는 에너지가 '0'에 수렴하기 때문에, 행동(클릭)까지 막힘없이 매끄럽게(Fluency) 이어지게 됩니다.

📊 A/B Test Design & Metrics Test Method: 50:50 정석 A/B Test (동일 기수 내 개인 단위 무작위 배정)

실험군: 확장자가 제거되고 핵심 메뉴가 상단에 노출된 심플 사이드바 대조군: 현재의 IDE 스타일 사이드바 유지 (Status Quo)

Primary KPI: 스터디(Projects) 및 행사(Events) 페이지 진입률(CTR) 및 등록 전환율 🔼 Guardrail: 메인 홈 이탈률(Bounce Rate), 첫 방문 유저의 세션 시간 (컨셉이 사라져 브랜드 매력이 감소하는지 감시)