> **📄 요약 ·** 🛠 2차 사이드바 엔지니어 핵심 — Task #1~15 상태보드(완료8/개발핸드오프5/대기2) + §별 명세·레퍼런스. dev 진입점: 00_common/ENGINEERING.md.

# 사이드바 A/B — 구현 명세서 (Task #1~#15 실행 산출물)

| | |
|---|---|
| `experiment_id` | `sidebar-nav-v1` |
| 연결 | [구체화](./experiment-spec.md) · [이벤트 정의](./data-definition.md) · [Playbook](../../00_common/playbook.md) · [scripts/](../../00_common/scripts/) |
| 작성 | 2026-06-22 |

> 이 문서는 15개 태스크의 **설계·분석 산출물을 확정**한 것이다. 통계는 `00_common/scripts/`로 실제 계산했고, 플랫폼 코드 빌드(#7~#10,#12)는 **구현 명세 + 레퍼런스**까지 완료해 개발 핸드오프 상태다. 배포(#14)·판정(#15)은 실험 시작(6/28)·데이터 이후.

> 🔤 용어가 낯설면 [`00_common/용어집.md`](../../00_common/용어집.md) (SRM·variant 프론트 연동·노출 등).
> 📌 **이 문서 = 태스크 관리 허브(상태보드).** 아래 보드에서 진행상태를 관리하고, 각 티켓의 **수용기준(AC)·완료조건(DoD)·추정·의존성**은 [`jira-backlog.md`](./jira-backlog.md)에서 본다. §1~§13은 각 태스크의 구현 명세 상세.

## 📊 상태 보드 (Jira 태스크 관리)
| 태스크 | 상태 | 티켓(상세) | 산출물·명세 |
|---|---|---|---|
| #1 가설·변형 | ✅ 확정 | — | §1 변형 mockup |
| #2 KPI 운영정의 | ✅ 확정 | — | §2 |
| #3 배정 규칙 | ✅ 확정 | — | §3 + `assign_variant.py`(50.02%·sticky 검증) |
| #4 표본·MDE | ✅ 계산 | — | §4 — **탐색 실험으로 분류** |
| #5 이벤트 스키마 | ✅ 문서화 | — | `data-definition.md` |
| #6 노출 보장 | ✅ 설계 | — | §6 |
| #7 event_log 파이프라인 | 📐 To Do | [PLAT-1](../../00_common/platform-backlog.md) 🧱공통 | §7 |
| #8 배정 서비스 | 📐 To Do | [PLAT-2](../../00_common/platform-backlog.md) 🧱공통 | §8 + `assign_variant.py` |
| #9 variant 프론트 | 📐 To Do | [SNAV-9](./jira-backlog.md) 사이드바 | §9 |
| #10 SRM 모니터 | 📐 To Do | [PLAT-3](../../00_common/platform-backlog.md) 🧱공통 | §10 + `srm_check.py` |
| #11 Guardrail | 부분 | [PLAT-4](../../00_common/platform-backlog.md) 🧱훅 + [SNAV-11r](./jira-backlog.md) 등록서 | §11 |
| #12 대시보드 | 📐 To Do | [PLAT-5](../../00_common/platform-backlog.md) 🧱틀 + [SNAV-12](./jira-backlog.md) 구성 | §12 |
| #13 분석 쿼리 | ✅ 작성 | SNAV-13 ✅ | [`queries.md`](./queries.md) |
| #14 배포 | ⏳ 대기(6/28~) | [SNAV-14](./jira-backlog.md) 사이드바 | §13 |
| #15 판정 | ⏳ 대기(非DEV) | [SNAV-15](./jira-backlog.md) 사이드바 | §13 + `bayesian_calc.py` |

> 🧱 **공통(PLAT)** = 모든 실험 재사용: #7·8·10·11(훅)·12(틀) → [`00_common/platform-backlog.md`](../../00_common/platform-backlog.md).
> **사이드바 전용(SNAV)** = #9·12(구성)·13·14·15 → [`jira-backlog.md`](./jira-backlog.md).
> 본 문서 §7·8·10·11·12는 공통 기능을 *사이드바 관점*에서 쓴 명세(티켓은 PLAT에서 관리).

---

## §1. 변형 확정 (#1)
**제거/이동 규칙**: ① 파일 확장자(`.json/.tsx/.md`) 라벨 전부 제거 ② `Projects`·`Events`를 폴더 밖 **최상단 1·2번** 고정 ③ 나머지는 하위 그룹.

```
[ control (현행 IDE 스타일) ]        [ treatment (심플) ]
▾ OPEN_ACADEMY                       ★ Projects
   Projects.tsx                      ★ Events
   Events.json                       ─────────────
▾ COMMUNITY                          Dashboard
   Notice.md                         Community
   Feed.md                           Wiki
▾ TOOLS                              Profile
   Bug_Report.txt
```
> 클릭 타깃·라우팅·페이지는 **양군 동일**(UI 표현만 변경) → 순수 카테고리화 유창성 효과 분리.

## §2. KPI 운영정의 (#2)
| 지표 | 분자(유니크 유저) | 분모 | dedup |
|---|---|---|---|
| 핵심메뉴 CTR (Primary) | `sidebar_item_clicked` & `item_key∈{projects,events}` | `exp_exposure` | user/세션 무관 유저 1회 |
| 등록 전환율 (Primary) | `enrollment_completed` | `exp_exposure` | 유저 1회 |
| 알림 신청 (Secondary) | `project_alert_signup` & `cohort='13'` | `exp_exposure` | 유저 1회 |
| 홈 이탈률 (Guardrail) | 홈 단일 page_view·무클릭 세션 | 홈 진입 세션 | 세션 |
| 첫방문 세션시간 (Guardrail) | median(마지막-처음 이벤트) | 첫 방문 세션 | 세션 |
> 분모는 항상 **노출유저(exposed)**. 배정-only·미노출 유저 제외.

## §3. 배정 규칙 (#3) — 확정 + 검증
- 단위 개인(`user_id`, 비로그인 `anon_id`), 비율 50:50, **결정적 sticky**: `sha256(experiment_id:uid)[:8] % 100 < 50 → treatment`.
- 점진 배포 10→25→50%, 중간 변경 금지, kill switch(상태 off 시 전원 control).
- **검증(`assign_variant.py --selftest 100000`)**: treatment 50.02% / control 49.98%, 재배정 일치(sticky)=True.
- **config JSON**
```json
{ "experiment_id":"sidebar-nav-v1", "status":"running",
  "variants":["control","treatment"], "ratio":{"treatment":0.5},
  "unit":"user_id|anon_id", "targeting":{"platform":"web"},
  "sticky":true, "kill_switch":false }
```

## §4. 표본 크기·분류 (#4) — `calc_sample_size.py` 실행 결과
가용 MAU 500 → 그룹당 ~250. **필요 표본(α=.05, power=.8)**:
| baseline CTR | MDE +3%p | +5%p | +8%p |
|---|---|---|---|
| 15% | 2,402 | 906 | 377 |
| 20% | 2,943 | 1,094 | 447 |
| 25% | 3,397 | 1,251 | 504 |

> **결론: 현 트래픽에선 모두 그룹당 250 초과 → 탐색 실험으로 분류.**
> 결정 실험이 되려면 (a) 큰 효과(MDE ≥ +8%p)를 노리고 (b) **누적 유니크 노출 ≥ ~450/그룹**을 모을 때까지 충분히 길게 운영해야 함. 그 전엔 방향만 보고 ship 단정 금지.

## §6. 노출 보장 설계 (#6)
- 트리거: 사이드바가 **배정 variant로 화면 렌더 완료**된 순간 `exp_exposure` 1회.
- dedup: `(experiment_id, user/anon, session)` 첫 노출만. 클라이언트 sessionStorage 가드.
- 분석 모수 = `exp_exposure` 보유 유저. 미노출 배정 유저 제외(생존자 편향 방지).
```js
// 프론트 의사코드
if (sidebarRendered && !session.hasFired('exp_exposure')) {
  track('exp_exposure', { experiment_id, variant, page });
  session.markFired('exp_exposure');
}
```

## §7. event_log 파이프라인 (#7) — 개발 명세
> 💡 **쉽게:** 사용자 행동(봄·클릭·등록)을 한 줄씩 쌓는 기록 테이블을 새로 만들고 데이터가 들어오게. 모든 분석의 원천. ([용어집](../../00_common/용어집.md))
- 스키마/DDL: `data-definition.md §1`. 적재 **incremental**, `base_date=occurred_at::date`.
- 수집 계약: `POST /ingest/events` body=이벤트 배열, **`id`로 멱등 적재**(중복 무시).
- 회고 실험 `project_reflection_ui_*`도 같은 테이블 사용(공용 인프라).
- 보존/파티션: `base_date` 일 파티션, PII 컬럼 마스킹 정책 적용.

## §8. 배정 서비스 (#8) — 명세 + 레퍼런스
- 레퍼런스 로직: `scripts/assign_variant.py`(결정적·sticky, 검증 완료).
- 서비스 구성: config store(§3 JSON) + `GET /assignment?experiment_id&uid` → `{variant}` + kill switch + 점진 배포(ratio 동적).
- sticky 영속화(선택): `experiment_assignment(uid, experiment_id, variant, assigned_at)`.

## §9. Variant 프론트 연동 (#9) — 명세
> 💡 **쉽게:** 사용자가 받은 버전(variant)대로 사이드바를 실제로 그려주고, 본 순간 '노출' 기록을 남기는 프론트 작업.
- 앱 로드시 `GET /assignment`로 variant 수신 → 사이드바 컴포넌트 분기 렌더 → 렌더 완료 콜백에서 §6 노출 트리거.
- variant 미수신/오류 시 **control 폴백**(안전).

## §10. SRM 모니터 (#10) — 명세 + 레퍼런스
> 💡 **쉽게:** SRM = 50:50으로 나눴는데 실제 비율이 틀어졌는지 매일 점검. 틀어지면 배정/계측 버그 신호라 실험 중단.
- 레퍼런스: `scripts/srm_check.py`(카이제곱). **검증**: 50.4:49.6 → p=0.42 정상 / 54:46 → p=1.3e-15 🚫.
- 일일 배치: 노출 유니크 유저 비율 점검, **p<0.001 시 알림·실험 중단** 트리거.

## §11. Guardrail Hook + 실험 등록서 (#11)
- Hook(Playbook 강제): 등록서에 Guardrail 미정의 시 저장 차단 / `ship` 결론에 Guardrail 미기록 시 차단.
- **실험 등록서 (플랫폼 `experiments/sidebar-nav-v1.md`에 등록할 블록)**
```yaml
experiment_id: sidebar-nav-v1
status: design        # design→running→done
type: randomized_ab
unit: user
ratio: 50:50
primary_kpi: [core_menu_ctr, enrollment_conversion]
guardrail: [home_bounce_rate, first_visit_session_time]   # 필수
decision: null        # ship|hold|rollback|need_more_data
classification: exploratory   # §4 근거
```

## §12. 지표 대시보드 (#12) — 명세
- 레이아웃: `experiment-spec.md §6` ASCII 목업.
- 위젯·데이터소스:
  | 위젯 | 소스 |
  |---|---|
  | 헤더(상태·배정비율·SRM 배지·n) | config + `srm_check.py` |
  | 퍼널(노출→클릭→페이지→등록, variant 병렬) | [`queries.md`](./queries.md) 사이드바 퍼널 쿼리 |
  | KPI 카드(CTR/전환 Δ%p + P(T>C)+신뢰구간) | 쿼리 + `bayesian_calc.py` |
  | Guardrail 패널(이탈률·세션시간, 악화 시 빨강) | 쿼리 |
  | 표본/검정력 트래커 | `calc_sample_size.py` |
  | 판정 배너(4-state) | Playbook 규칙, Guardrail 게이트 |

## §13. 배포(#14)·판정(#15) 플랜 — 대기
- #14: AA 테스트(양군 동일 UI, CTR 차 ≈0 확인) → 계측 QA(`data-definition.md §7`) → 10→50% 점진 → SRM 관찰.
- #15: 퍼널·CTR·전환 variant 비교 → `bayesian_calc.py`로 P(T>C) → Guardrail 확인 → 4-state. **예시**(CTR 12% vs 9.5%): P(T>C)=96.4% → "ship 고려(Guardrail 확인 후)". 단 §4 탐색 분류라 표본 누적 전엔 보수 해석.
