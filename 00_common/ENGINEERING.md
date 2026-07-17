# 🛠 엔지니어링 TODO — 개발자 진입점

> **📄 요약 ·** 개발자가 봐야 할 **단일 진입점**. 두 실험에 걸친 개발 작업을 우선순위로 모음. 상세 명세는 각 항목의 링크 참조. 태스크 번호는 `TaskList`(#7~#15)와 1:1.

> 🔤 **용어가 낯설면** [`용어집.md`](./용어집.md) 먼저 — SRM·variant 프론트 연동·노출·Guardrail 등 쉬운 풀이.

## 0. 한눈에
- **키스톤 = `event_log` 적재 인프라(현재 없음).** 두 실험 공용 — 이게 없으면 회고·사이드바 **둘 다 분석 불가**. 여기부터.
- 사이드바 상세 상태/명세: [`01_experiments/02_sidebar/implementation-spec.md`](../01_experiments/02_sidebar/implementation-spec.md) (상태보드 = 완료8/핸드오프5/대기2)
- **백로그(Jira 티켓)**: 🧱공통 [`platform-backlog.md`](./platform-backlog.md)(PLAT-1~5, 모든 실험 재사용) · 사이드바 전용 [`jira-backlog`](../01_experiments/02_sidebar/jira-backlog.md)(SNAV)
- 통계 도구는 준비됨(레퍼런스): [`00_common/scripts/`](./scripts/)

---

## 1. 🔴 공용 인프라 (먼저)
- [ ] **`event_log` 테이블 + 적재 파이프라인** (#7)
  - 스키마/DDL·멱등 적재: [`02_sidebar/data-definition.md §1`](../01_experiments/02_sidebar/data-definition.md)
  - **두 실험 공용**: 회고 `project_reflection_ui_viewed/clicked` + 사이드바 이벤트 모두 같은 테이블.

## 2. 🔴 1차 회고 — 6/28(노출 시작) 전 필수
- [ ] **reflection 이벤트/테이블 적재** — `project_reflection_ui_*`, `reflection`(`experiment_id='s12-mid-reflection'`) → [`01_reflection/data-definition.md`](../01_experiments/01_reflection/data-definition.md)
- [ ] **6/28 사전 스냅샷 박제** — 출석·발표·산출물·activity (공변량). *지나가면 복원 불가.* → [`01_reflection/analysis-plan.md §8`](../01_experiments/01_reflection/analysis-plan.md)
- [ ] 전원 노출 보장(알림 발송 연동)

## 3. 🟡 2차 사이드바 — 명세 완료, 코드만 남음
> **👉 Jira 티켓(수용기준·완료조건·추정·의존성): [`02_sidebar/jira-backlog.md`](../01_experiments/02_sidebar/jira-backlog.md)** — "무엇이 구현 필요/완료"가 여기 가장 명확.
> §별 상세 명세 + 레퍼런스 코드: [`02_sidebar/implementation-spec.md`](../01_experiments/02_sidebar/implementation-spec.md).
- [ ] **#8 배정 서비스** — config·결정적 버킷팅·sticky·kill switch. 레퍼런스 [`scripts/assign_variant.py`](./scripts/assign_variant.py) (검증 50.02%·sticky)
- [ ] **#9 variant 프론트 연동** — 사이드바 A/B 렌더 + **노출(`exp_exposure`) 트리거**(분모). data-definition §3
- [ ] **#10 SRM 모니터** — 일일 카이제곱, p<0.001 알림. 레퍼런스 [`scripts/srm_check.py`](./scripts/srm_check.py)
- [ ] **#12 지표 대시보드** — 퍼널·KPI·Guardrail·SRM·판정. implementation-spec §12
- [ ] **#14 AA·계측 QA → 점진 배포(10→50%)**

## 4. 참고 (개발 아님)
- 분석/판정은 분석가 몫: 각 실험 `analysis-plan.md` (SRM 게이트→Bayesian→4-state).
- 통계 도구 준비됨: `00_common/scripts/` (표본·SRM·Bayesian·배정).
- 전체 폴더 지도: [`INDEX.md`](../INDEX.md).

---

## 의존 순서 (요약)
```
#7 event_log  ──┬─> (회고) reflection 적재·사전 스냅샷  ── 6/28 전
                └─> (사이드바) #8 배정 → #9 프론트+노출 → #10 SRM → #12 대시보드 → #14 배포
```
> `event_log`(#7)가 모든 것의 선행. 회고는 시점(6/28) 때문에, 사이드바는 분석 분모 때문에 둘 다 event_log에 묶임.
