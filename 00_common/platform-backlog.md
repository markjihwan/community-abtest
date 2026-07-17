> **📄 요약 ·** 실험 플랫폼 **공통 백로그**(PLAT 티켓) — 한 번 만들면 모든 실험이 재사용하는 기능. event_log·배정 서비스·SRM·Guardrail 훅·대시보드 프레임워크. 실험전용 작업은 각 `01_experiments/<실험>/jira-backlog.md`.

# 🧱 플랫폼 공통 백로그 (PLAT)

> 🔤 용어 낯설면 [`용어집.md`](./용어집.md) · 개발 진입점 [`ENGINEERING.md`](./ENGINEERING.md).
> **분류 기준**: *"다음 실험이 `experiment_id`만 바꿔 그대로 쓰나?"* → **예 = 여기(PLAT)**. 사이드바라서 필요 = 실험전용(SNAV).

## 📋 백로그 요약
| 키 | 원래 # | 제목 | 컴포넌트 | 추정 | 소비자 | 상태 |
|---|---|---|---|---|---|---|
| **PLAT-1** | #7 | event_log 적재 인프라 | Backend/Data | 5 | **전 실험**(회고+사이드바…) | To Do 🔴 Blocker |
| **PLAT-2** | #8 | 실험 배정 서비스 | Backend | 3 | 모든 무작위 A/B | To Do |
| **PLAT-3** | #10 | SRM 모니터 | Backend/Data | 2 | 모든 무작위 A/B | To Do |
| **PLAT-4** | #11 | Guardrail Hook | Platform | 2 | 전 실험(안전장치) | To Do (등록서는 실험별) |
| **PLAT-5** | #12 | 실험 지표 대시보드 **프레임워크** | Frontend/Data | 8 | 전 실험(지표만 config) | To Do |

> 첫 소비자: PLAT-1은 회고+사이드바 둘 다(6/28), PLAT-2~5는 사이드바가 최초. **3차 실험부턴 PLAT 재사용 — 새로 안 만듦.**

## 🔗 PLAT 내부 의존성
```
PLAT-1 (event_log) ─┬─> PLAT-3 (SRM)
PLAT-2 (배정) ──────┘
PLAT-1 ─> PLAT-5 (대시보드)
PLAT-4 (Guardrail 훅) ── 독립
```

---

## PLAT-1 · event_log 적재 인프라
> 💡 **쉽게:** 사용자 행동(봄·클릭·등록)을 한 줄씩 쌓는 기록 테이블 + 데이터 수집. 모든 분석의 원천. 회고·사이드바 공용.
- **타입** Story · **우선순위** 🔴 Blocker · **컴포넌트** Backend/Data · **추정** 5 · **Blocks** PLAT-3, PLAT-5 + 전 실험
- **AC**
  - [ ] `event_log` 테이블 생성 — 스키마/DDL [`사이드바 data-definition §1`](../01_experiments/02_sidebar/data-definition.md) (공통 스키마)
  - [ ] `POST /ingest/events`(배열), **`id` 멱등 적재**(중복 무시)
  - [ ] 핵심 차원(experiment_id·variant·user_id/anon_id·session_id·occurred_at) 상위 컬럼 + `properties`(JSON)
  - [ ] `base_date=occurred_at::date` 파티션, **incremental**(재집계 중복 없음)
  - [ ] 회고 이벤트(`project_reflection_ui_*`)도 동일 테이블 수용
  - [ ] PII 마스킹 정책
- **DoD**: 샘플 이벤트 적재·조회, 동일 id 2회→1건(멱등 테스트).

## PLAT-2 · 실험 배정 서비스
> 💡 **쉽게:** 각 사용자를 control/treatment 중 '항상 같은 쪽'으로 자동 배정 + 문제 시 끄는 kill switch. experiment_id만 바꾸면 어느 실험이든 동작.
- **타입** Story · **우선순위** 🟠 High · **컴포넌트** Backend · **추정** 3 · **Blocks** PLAT-3
- **레퍼런스** [`scripts/assign_variant.py`](./scripts/assign_variant.py)(검증 50.02%·sticky=True)
- **AC**
  - [ ] config 저장: `experiment_id, variants, ratio, targeting, status, kill_switch`
  - [ ] `GET /assignment?experiment_id&uid` → `{variant}` — `sha256(experiment_id:uid)[:8]%100 < ratio*100`
  - [ ] **sticky**(같은 uid 항상 같은 variant), `kill_switch=on`→전원 control, 점진 배포(ratio 동적)
  - [ ] (선택) `experiment_assignment` 영속 테이블
- **DoD**: 10만 uid ~50:50·재호출 일치·kill switch 동작.

## PLAT-3 · SRM 모니터
> 💡 **쉽게:** 50:50으로 나눴는데 실제 비율이 틀어졌는지 매일 점검. 틀어지면 버그 신호 → 실험 중단.
- **타입** Task · **우선순위** 🟡 Medium · **컴포넌트** Backend/Data · **추정** 2 · **Blocked by** PLAT-1, PLAT-2
- **레퍼런스** [`scripts/srm_check.py`](./scripts/srm_check.py)(50.4:49.6→정상 / 54:46→차단)
- **AC**
  - [ ] 일일 배치: `exp_exposure` 유니크 유저 비율 카이제곱
  - [ ] `p<0.001` 시 알림 + 실험 상태 플래그
  - [ ] 대시보드(PLAT-5) SRM 배지 연동
- **DoD**: 의도적 불균형(54:46)으로 알림 트리거 검증.

## PLAT-4 · Guardrail Hook
> 💡 **쉽게:** 안전지표(Guardrail) 빠뜨린 채 실험 등록·출시 못하게 막는 코드 잠금장치.
- **타입** Task · **우선순위** 🟡 Medium · **컴포넌트** Platform · **추정** 2
- **AC**
  - [ ] 실험 등록 저장 시 `guardrail` 필드 없으면 거부
  - [ ] 판정 `ship`인데 Guardrail 체크 기록 없으면 거부
- **DoD**: Guardrail 없는 등록 시도 차단(테스트). (실험별 등록서 작성은 각 실험 SNAV)

## PLAT-5 · 실험 지표 대시보드 프레임워크
> 💡 **쉽게:** 실험 현황을 한 화면에서 보는 대시보드의 **재사용 틀**(퍼널·KPI카드·Guardrail·SRM·판정). 실험마다 지표만 config로 갈아끼움.
- **타입** Story · **우선순위** 🟡 Medium · **컴포넌트** Frontend/Data · **추정** 8 · **Blocked by** PLAT-1
- **AC (프레임워크)**
  - [ ] 헤더(상태·기간·배정비율·SRM 배지·n), 퍼널(variant 병렬), KPI 카드(Δ%p+P(T>C)+신뢰구간), Guardrail 패널(악화 시 빨강), 표본/검정력 트래커, 4-state 판정 배너
  - [ ] **실험별 지표는 config로 주입**(쿼리/KPI 정의를 experiment가 제공)
  - [ ] 통계: [`scripts/bayesian_calc.py`](./scripts/bayesian_calc.py)·[`scripts/calc_sample_size.py`](./scripts/calc_sample_size.py)
- **DoD**: 더미 config로 전 위젯 렌더, Guardrail 악화 시 ship 배너 차단.
