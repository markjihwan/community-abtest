> **📄 요약 ·** 전체 폴더 지도 + 진행 상태. 모든 문서 상단엔 한줄요약이 있음. **👉 개발자는 [`00_common/ENGINEERING.md`](00_common/ENGINEERING.md)부터** (두 실험 dev TODO 한곳).
> **🌐 공용 지침 ·** 워크스페이스 공통 작업원칙·거버넌스는 [`../CLAUDE.md`](../CLAUDE.md). 이 프로젝트의 `00_common/`(playbook·scripts) vs `01_experiments/<실험>/` 구조가 그 "공통자산 vs 인스턴스 분리" 원칙의 레퍼런스 구현이다.

# 실험 플랫폼 문서 인덱스

가짜연구소 성장시스템 **완주율/참여 개선** 실험 문서 모음.
구조 원칙: **공통(모든 실험 적용) = `00_common/` · 실험전용(한 실험만) = `01_experiments/<실험>/`**.

## 📂 폴더 구조 (하이브리드)

```
.
├── INDEX.md                              ← 본 문서
├── 00_common/                              ← 🔧 모든 실험 공통
│   ├── ENGINEERING.md                    🛠 개발자 진입점 — 두 실험 dev TODO 한곳(우선순위)
│   ├── platform-backlog.md               🧱 공통 백로그(PLAT) — 모든 실험 재사용 기능 티켓
│   ├── 용어집.md                          🔤 처음 보는 분께 — SRM·variant·노출·Guardrail 등 쉬운 풀이
│   ├── playbook.md                       메트릭 카탈로그·배정·quasi-experiment 원칙
│   ├── platform.md                       Claude Code 기반 실험 플랫폼 아키텍처
│   ├── 준실험트래킹원칙.md                 트래킹 요건 명세(분모=노출) — 두 실험 공통
│   ├── discussion.md                     플랫폼 discussion API 가이드(외부 제공)
│   ├── data-structure-map.{md,drawio,png,svg}  ERD·PK·연결구조·데이터량·유의 테이블
│   ├── _gen_diagram.py                   data-structure-map 재생성 스크립트
│   └── scripts/                          통계 도구(표본·SRM·Bayesian·배정) + README
├── 01_experiments/
│   ├── 01_reflection/                    ← 🟢 1차: 12기 중간 회고 (준실험)
│   │   ├── experiment-spec.md            실험계획서 + 기능 개발 정의서
│   │   ├── analysis-plan.md              분석계획서(추정량/공변량/SQL 골격/판정)
│   │   ├── data-definition.md            DB/이벤트 정의(event_log, reflection)
│   │   ├── queries.md                    청강생 보정 검증 쿼리
│   │   ├── report.md                     참여자 공유용 현황 리포트
│   │   ├── announcement.md               Discord 공지 스크립트
│   │   └── notes/                        📝 실측/검토 노트
│   │       ├── 실험_트래킹리포트.md        회고 트래킹 현황 리포트(6/22)
│   │       └── round1-results.md         1차 D1 실측 노트(session_id null·UTC·smoke)
│   └── 02_sidebar/                       ← 🟢 2차: 사이드바 내비 A/B (무작위)
│       ├── experiment-spec.md            실험 설계서(가설/KPI/배정/계측/대시보드)
│       ├── analysis-plan.md              분석계획서(SRM 게이트/퍼널/Bayesian/표본 분류)
│       ├── data-definition.md            event_log 통합 스키마·이벤트 카탈로그
│       ├── implementation-spec.md        Task #1~15 실행 산출물·상태보드
│       ├── jira-backlog.md               🛠 구현 백로그(Jira 티켓: AC·DoD·추정·의존성)
│       ├── queries.md                    퍼널/CTR/SRM/Guardrail 쿼리
│       └── notes/                        📝 실측/검토 노트
│           ├── 사이드바실험_검토리포트.md   설계 vs D1 실측 교차검증(계측 계약 4건 불일치)
│           └── 사이드바설계서_피드백.md     설계서·백로그 분석가 피드백(K)
├── 02_ideas/                                ← 🟡 미착수 아이디어
│   ├── sidebar-navigation-abtest.md      (2차로 승격된 원본 컨셉)
│   └── lovable-mockup-test.md            Lovable 목업 5페이지 테스트 메모
├── 03_memory/
│   ├── RESUME_2026-06-22.md              🧠 세션 핸드오프 — 재개 진입점
│   └── HISTORY.md                        📜 문서 이력·계보 — 개편 연대기·폐기 경로 매핑
└── 04_results/                              ← 📊 실험 결과 보고서
    └── 1차_준실험_중간결과.md              1차 회고 중간결과(퍼널·균형검사·Health Score·판정)
```

## 🗂 구조 원칙

| 구분 | 위치 | 무엇 |
|---|---|---|
| 공통 | `00_common/` | playbook · platform · scripts · 데이터구조맵 · discussion (모든 실험에 적용) |
| 실험전용 | `01_experiments/<실험>/` | 그 실험의 spec · analysis · data-definition · queries · report · announcement |
| 아이디어 | `02_ideas/` | 아직 착수 안 한 실험 컨셉 |
| 메모리 | `03_memory/` | 세션 핸드오프(재개 진입점) + 문서 이력(HISTORY) |
| 분석 노트·리포트 | `01_experiments/<실험>/notes/` 또는 `00_common/` | 한 실험 전용 실측/검토 노트 → 그 실험의 `notes/` · 두 실험 공통 명세 → `00_common/` (별도 analytics 폴더 금지) |
| 결과 보고서 | `04_results/` | 실험별 중간/최종 결과 **보고서**(종합·판정). 원자료·재현 쿼리는 각 실험 `notes/`에 두고 여기서 참조만(복제 금지) |

> 새 실험을 추가할 땐 `01_experiments/03_<이름>/` 폴더를 만들고 그 실험 문서를 전부 그 안에 둔다. 공통 자산은 절대 실험별로 복제하지 않는다.

## 📊 진행 상태

- **🟢 1차 (`01_reflection`)** — 12기 중간 회고, 준실험(작성자 vs 미작성자), `experiment_id='s12-mid-reflection'`. 노출 6/28~7/12 **종료**(연장 배포 반영). 중간결과: [`04_results/1차_준실험_중간결과.md`](04_results/1차_준실험_중간결과.md) — 탐색 실험·need_more_data, 완주율은 시즌 종료 후.
- **🟢 2차 (`02_sidebar`)** — 사이드바 내비 A/B, 무작위 50:50, `experiment_id='sidebar-nav-v1'`. 설계 8태스크 완료 / 플랫폼 코드 5 + 배포·판정 2 미완(상세 implementation-spec).
- **🟡 아이디어** — Lovable 목업 테스트.

## 🧹 구조 이력 (상세: [`03_memory/HISTORY.md`](03_memory/HISTORY.md))
- **2026-06-22 초기**: 흩어진 문서 → 레이어 폴더(00~05) 정리, 중복 `github.md` 삭제.
- **2026-06-22 재배치(하이브리드)**: 공통 → `00_common/`, 실험전용 → `01_experiments/<실험>/`. `query.md`를 실험별 `queries.md`로 분리. 03_report 리포트·04_script 공지를 `01_reflection/`로, 데이터구조맵을 `00_common/`으로 이동.
- **2026-07-13 analytics 해체**: 지도 미등재였던 `analytics/`(6건)를 원칙대로 재배치 — 회고 노트 2건 → `01_reflection/`, 사이드바 검토 2건 → `02_sidebar/`, 공통 트래킹 명세 1건 → `00_common/`. 설계서 사본·빈 `refe.md` 삭제. 트래킹리포트 부록의 폐기 경로(00_playbook 등) 참조를 현재 경로로 갱신.
- **2026-07-13 넘버링 + notes/**: 최상위 폴더 넘버링 도입 — `_common`→`00_common` · `experiments`→`01_experiments` · `ideas`→`02_ideas` · `05_memory`→`03_memory`. 실험별 실측/검토 노트 폴더 `notes/` 신설(노트 4건 이동). 전 문서 상대 링크 일괄 갱신(플랫폼 레포의 `experiments/` 경로는 대상 아님 — 원형 유지).
- **2026-07-13 04_results 신설**: 실험 결과 보고서 레이어 추가 — `04_results/1차_준실험_중간결과.md`(1차 회고 중간결과 종합). 원자료·재현 쿼리는 `01_reflection/notes/round1-results.md`에 유지, 보고서는 참조만.
