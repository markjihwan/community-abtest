# ABTest Experiment Platform

`abtest`는 커뮤니티/러닝 프로그램 운영 환경에서 실험을 설계하고 해석하기 위한 문서 중심 프로젝트다.

이 프로젝트는 이상적인 랜덤 A/B 테스트를 지향하되, 실제 운영에서는 기수 단위 비교가 중심이 되는 환경을 전제로 한다. 따라서 본 문서 세트는 `randomized A/B test`와 `cohort-based comparative experiment`를 구분해서 설명한다.

## Core Principle

본 프로젝트의 실험 평가는 랜덤 A/B 테스트가 어려운 운영 환경을 고려하여, 기수 단위 cohort 비교를 기반으로 수행한다.
핵심 성과는 완주율을 North Star Metric으로 두고, Funnel 분석으로 단계별 이탈을 파악하며, Retention 분석으로 지속 참여를 측정한다.
최종 효과 판단은 Bayesian 기반 확률 해석을 중심으로 수행하고, 필요 시 Sequential Testing과 CUPED를 보조적으로 활용한다.

## Start Here

지금부터는 문서를 `핵심 7개 + 부록` 구조로 읽는 것을 권장한다.

## Core Docs

- [`docs/01_FOUNDATIONS.md`](docs/01_FOUNDATIONS.md): 실험 철학, 통계 기초, test design의 입문 묶음
- [`docs/02_EXPERIMENT_POLICY.md`](docs/02_EXPERIMENT_POLICY.md): 실험 등록, 승인, 데이터/참여자/결과 활용 정책 묶음
- [`docs/03_METRICS.md`](docs/03_METRICS.md): metric 정의와 KPI 우선순위
- [`docs/04_VALIDITY_AND_TRUST.md`](docs/04_VALIDITY_AND_TRUST.md): peeking, SRM, novelty, network effect, 품질 리스크
- [`docs/05_ADVANCED_METHODS.md`](docs/05_ADVANCED_METHODS.md): ratio metrics, multiple testing, variance reduction, sequential testing
- [`docs/06_PLATFORM_SCHEMA.md`](docs/06_PLATFORM_SCHEMA.md): 데이터 스키마와 통계 컬럼 설계
- [`docs/07_OPERATIONS_AND_DECISIONS.md`](docs/07_OPERATIONS_AND_DECISIONS.md): 운영 체크리스트와 최종 판단 기준

## Appendix

- [`docs/COMMUNITY_BENCHMARKS.md`](docs/COMMUNITY_BENCHMARKS.md): 외부 사례와 벤치마크
- [`docs/V1_SCOPE_AND_GAPS.md`](docs/V1_SCOPE_AND_GAPS.md): 현재 범위 점검과 v1 우선순위
- [`docs/REFERENCE_MAP.md`](docs/REFERENCE_MAP.md): 기존 세부 문서와 새 그룹 문서의 매핑
- [`docs/archive/`](docs/archive): 수정 전 세부 문서 아카이브

## Recommended Reading Order

1. [`docs/01_FOUNDATIONS.md`](docs/01_FOUNDATIONS.md)
2. [`docs/02_EXPERIMENT_POLICY.md`](docs/02_EXPERIMENT_POLICY.md)
3. [`docs/03_METRICS.md`](docs/03_METRICS.md)
4. [`docs/04_VALIDITY_AND_TRUST.md`](docs/04_VALIDITY_AND_TRUST.md)
5. [`docs/06_PLATFORM_SCHEMA.md`](docs/06_PLATFORM_SCHEMA.md)
6. [`docs/07_OPERATIONS_AND_DECISIONS.md`](docs/07_OPERATIONS_AND_DECISIONS.md)
7. [`docs/05_ADVANCED_METHODS.md`](docs/05_ADVANCED_METHODS.md)

## 프로젝트 구조

```
community-abtest/
│
├── CLAUDE.md                        ← Claude Code 진입점 (맥락 + 판단 원칙)
├── .mcp.json                        ← MCP 설정 (docs/ 마운트)
│
├── .claude/
│   ├── agents/
│   │   └── abtest-analyst.md        ← 판단 원칙 + Syneidesis 갭 추적
│   └── skills/
│       ├── experiment-register/     ← 실험 등록 & 승인 체크리스트
│       ├── metrics-definition/      ← 지표 정의 & 우선순위
│       ├── experiment-design/       ← 실험 설계 워크플로우
│       ├── validity-check/          ← SRM, peeking, network effect 점검
│       ├── knowledge-audit/         ← 지식 검증 루프 (autoresearch 패턴)
│       ├── experiment-decision/     ← ship/hold/rollback/need_more_data 판정
│       └── advanced-analysis/       ← CUPED, sequential, ratio metrics
│
├── docs/                            ← MCP로 마운트되는 지식 베이스
│   ├── 01_FOUNDATIONS.md
│   ├── 02_EXPERIMENT_POLICY.md
│   ├── 03_METRICS.md
│   ├── 04_VALIDITY_AND_TRUST.md
│   ├── 05_ADVANCED_METHODS.md
│   ├── 06_PLATFORM_SCHEMA.md
│   ├── 07_OPERATIONS_AND_DECISIONS.md
│   ├── SKILL_GUIDE.md               ← Skills 활용 가이드
│   └── archive/                     ← 세부 문서 원본
│
├── scripts/                         ← 결정론적 계산 스크립트 (표준 라이브러리만 사용)
│   ├── calc_sample_size.py          ← 완주율 기반 표본 크기 계산 (Cohen's h)
│   ├── check_balance.py             ← 공변량 균형 검사 (SMD)
│   ├── bayesian_calc.py             ← Bayesian P(T>C) 계산 (Beta-Binomial)
│   └── stratification_check.py     ← 층화 분석 가능 여부 (셀당 20명 기준)
│
└── experiments/                     ← 실험 등록서 저장소
    ├── TEMPLATE.md                  ← 실험 등록서 템플릿
    └── 12ki_w7_magical_week.md      ← 12기 W7 Magical Week 준실험
```

## Claude Code 연동

이 레포는 Claude Code와 함께 사용할 수 있도록 Agent + Skills가 구성되어 있다.

### 시작 방법

아래 두 가지가 설치되어 있어야 한다:
- **Node.js** — MCP 서버 실행용
- **jq** — Hook 스크립트 JSON 파싱용

```bash
# jq 설치 (Windows)
winget install jqlang.jq

# jq 설치 (Mac)
brew install jq
```

이후 이 레포 디렉토리에서 `claude`를 실행하면 MCP가 자동으로 `./docs`를 마운트한다.

```bash
git clone <this-repo>
cd community-abtest
claude
```

### Agent

- `abtest-analyst` — 실험 분석 전문가. 판단 원칙과 Syneidesis(갭 추적) 패턴이 내장되어 있다.

### Skills

| Skill | 트리거 예시 |
|---|---|
| `experiment-register` | "실험 시작 전에 뭐 해야 해" |
| `metrics-definition` | "지표 어떻게 정의해", "guardrail 뭐로 잡아" |
| `experiment-design` | "실험 설계해줘", "샘플 사이즈 계산" |
| `validity-check` | "SRM 의심돼", "이 실험 믿어도 돼?" |
| `knowledge-audit` | "이 내용 맞아?", "새 논문 적용 가능해?" |
| `experiment-decision` | "결과 어떻게 봐", "이거 올려도 돼?" |
| `advanced-analysis` | "CUPED 써야 해?", "sequential testing 가능해?" |

Skills는 순서대로 연결되어 있다: `experiment-register` → `experiment-design` → `validity-check` → `experiment-decision`

## Experiments

실제 실험 등록서는 [`experiments/`](experiments/) 폴더에 저장한다.

- [`experiments/12ki_w7_magical_week.md`](experiments/12ki_w7_magical_week.md): 12기 W7 Magical Week 참여 효과 준실험 평가

## Note

기존 세부 문서는 `docs/archive/`로 이동해 보관한다. 앞으로는 새 그룹 문서를 기준으로 읽고, 세부 문서는 필요할 때만 참고하는 구조를 권장한다.
