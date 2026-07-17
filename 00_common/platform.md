> **📄 요약 ·** Claude Code 기반 실험 플랫폼 아키텍처(docs/.claude/hooks 3레이어)와 미구현 항목. 사이드바 실험이 여기 '웹 플랫폼 실험' 항목.

실험 플랫폼 WORKFLOW (w.skills)
실험 플랫폼 BACKGROUND
— 도메인 지식을 AI에 붙이는 법


Background
"이건 랜덤 배정이 아니니까 선택편향을 봐야 해"

"guardrail 지표가 훼손되면 다른 결과가 아무리 좋아도 ship하면 안 돼"

"p-value 단독으로 결론 내리지 마"

Claude Code 기반 레포에 이 판단 기준을 직접 심기로 했다.

적용점
한 줄로 요약하면:

실험 지식을 Claude Code에 붙여서, 매번 가르치지 않아도 알아서 원칙대로 분석하는 실험 플랫폼

구조는 세 레이어로 나뉜다.

docs/     ← 지식 베이스 (MCP로 Claude에 연결)
.claude/  ← 워크플로우 + 판단 원칙 (Skills + Agent)
hooks/    ← 안전장치 (guardrail 없이 결론 못 냄)
핵심 설계 결정 3가지
1. 지식과 워크플로우를 분리했다
Agent → "어떻게 행동할지" (원칙과 경계만)
Skill → "무엇을 할지" (실제 워크플로우만)
docs/ → "무엇을 알고 있는지" (지식 베이스)
섞으면 지침이 충돌하거나 중복된다. 분리하면 각자 독립적으로 업데이트할 수 있다.

2. Syneidesis 패턴을 모든 Skill에 심었다
결론 전에 반드시 갭을 먼저 표면화한다.

[Gap:Assumption]     검증하지 않은 가정
[Gap:Procedural]     빠진 분석 단계
[Gap:Consideration]  고려하지 않은 외부 요인
이게 없으면 Claude가 그럴 듯한 결론을 자신있게 내놓고 사용자가 흔들린다. 갭을 먼저 보여주면 사용자가 판단 권한을 가져간다.

3. 검증 루프를 autoresearch 패턴으로 설계했다
karpathy/autoresearch에서 영감을 받았다. 핵심은:

기준 먼저 정하기 → 단위별 테스트 → PASS/FAIL 명확히 → 반복

"참고할 만하다"로 끝내지 않는다. PSM vs 층화 분석 같은 방법론 선택도 이 루프로 돌렸다. 200명 / 4셀 / 셀당 50명 → 층화 분석 ADOPT. 판정이 명확하다.

실제로 어떻게 쓰이나
12기 W7 Magical Week 실험을 설계하는 과정이 첫 번째 사용 사례였다.

나: "11기 vs 12기 완주율 비교하려는데 어떻게 해야 해?"

Claude (experiment-design 발동):

[Gap:Assumption] 두 기수가 동질한 집단이라는 가정 미확인
[Gap:Procedural] 사전 특성 데이터 확보 여부 미확인
[Gap:Consideration] 두 기수 사이 운영 방식 변경 여부

→ 이 갭들이 해소되지 않으면 결과 해석에 한계가 있습니다.
  계속 진행하기 전에 확인해주세요.
갭을 먼저 짚어준 다음 설계로 넘어갔다. 향후 고려 : MDE, 표본 크기, 층화 기준, ITT/ATT 분리

"비노출 = 그 기간에 접속 안 한 사람일 수 있습니다. 비노출 = 이미 이탈한 사람 편향이 생깁니다."

그래서 전원 알림 발송으로 노출을 보장하고, participation_level을 notified_only / visited / partial / full 4단계로 나눴다.

안전장치: Hooks
실험 플랫폼에서 가장 중요한 원칙은 guardrail이 최우선이다. Bayesian 결과가 아무리 좋아도 guardrail 지표가 훼손되면 ship하지 않는다.

이걸 코드로 강제했다.

# experiments/*.md에 Guardrail 없이 저장 시도 시
🚫 Guardrail 지표가 정의되지 않았습니다.

# ship 결론인데 Guardrail 상태 미기록 시
🚫 [ship 차단] Guardrail 체크 결과가 명시되지 않았습니다.

Claude가 흔들리지 않게 워크플로우에 판단 원칙 수립

전체 구조
community-abtest/
│
├── CLAUDE.md                    ← Claude Code 진입점
├── .mcp.json                    ← docs/ MCP 마운트
│
├── .claude/
│   ├── agents/abtest-analyst.md ← 판단 원칙
│   ├── skills/                  ← 7개 워크플로우
│   │   ├── experiment-register/
│   │   ├── metrics-definition/
│   │   ├── experiment-design/
│   │   ├── validity-check/
│   │   ├── knowledge-audit/
│   │   ├── experiment-decision/
│   │   └── advanced-analysis/
│   ├── hooks/                   ← 안전장치
│   └── settings.json
│
├── docs/                        ← 지식 베이스 (MCP 연결)
└── experiments/                 ← 실험 등록서
    ├── TEMPLATE.md
    └── 12ki_w7_magical_week.md
Skills는 순서대로 연결되어 있다:

experiment-register
  → experiment-design
    → validity-check
      → knowledge-audit (방법 의심 시)
        → experiment-decision
          → advanced-analysis (need_more_data 시)
어떤 컴퓨터에서도 동일하게
설정이 모두 레포 안에 있다. .mcp.json은 상대경로를 쓴다.

git clone <repo>
cd community-abtest
claude

Node.js와 jq만 설치되어 있으면 어디서든 동일한 환경이 된다.

아직 남은 것들
experiment-monitor — W8~W10 guardrail 중간 체크 (미구현)
웹 플랫폼 실험 — pseudo-lab.com MAU 500명 기반 A/B 테스트 (Lovable 조사 후)
advanced-analysis 보완 — 층화 분석 섹션 추가
마치며
AI에게 도메인 지식을 가르치는 게 아니라, 도메인 지식이 워크플로우로 작동하게 만들어야 한다.

문서만 있으면 검색 도구다. Skills가 있어야 판단 도구가 된다.