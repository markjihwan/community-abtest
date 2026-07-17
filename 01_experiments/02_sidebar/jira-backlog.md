> **📄 요약 ·** 2차 사이드바 **실험 전용** 구현 백로그(SNAV 티켓). 공통 플랫폼 기능(event_log·배정·SRM·Guardrail훅·대시보드 틀)은 [`00_common/platform-backlog.md`](../../00_common/platform-backlog.md)(PLAT)에 있고 여기선 그걸 **의존**으로만 참조.

# 사이드바 A/B — 실험 전용 백로그 (SNAV)

> 출처 명세: [`experiment-spec.md`](./experiment-spec.md) · [`implementation-spec.md`](./implementation-spec.md) · [`data-definition.md`](./data-definition.md) · [`analysis-plan.md`](./analysis-plan.md).
> 🔤 용어 [`00_common/용어집.md`](../../00_common/용어집.md) · 🧱 공통 기능 [`00_common/platform-backlog.md`](../../00_common/platform-backlog.md).
> **분류**: 사이드바라서 필요한 것만 여기. "어느 실험이든 필요"면 PLAT로 갔음.

## 📋 백로그 요약
| 키 | 원래 # | 제목 | 컴포넌트 | 추정 | 상태 | 의존(PLAT) |
|---|---|---|---|---|---|---|
| **SNAV-9** | #9 | Variant UI 렌더 + 노출 | Frontend | 5 | **To Do (DEV)** | PLAT-1, PLAT-2 |
| **SNAV-11r** | #11 | 사이드바 실험 등록(config·등록서) | Config | 1 | **부분**(등록서 ✅) | PLAT-4 |
| **SNAV-12** | #12 | 사이드바 대시보드 구성 | Frontend/Data | 3 | **To Do (DEV)** | PLAT-5, SNAV-13 |
| SNAV-13 | #13 | 분석 쿼리 | Analytics | — | ✅ **Done** ([`queries.md`](./queries.md)) | PLAT-1 |
| **SNAV-14** | #14 | AA·계측 QA → 점진 배포 | QA/Release | 3 | **To Do** (게이트) | SNAV-9, PLAT-1, PLAT-3 |
| SNAV-15 | #15 | 결과 분석·4-state 판정 | Analytics | 2 | **Blocked**(데이터 후·非DEV) | SNAV-14, SNAV-12 |

> **사이드바 전용 DEV**: SNAV-9·12 (+11r config) · QA SNAV-14. **완료**: SNAV-13. **데이터 후**: SNAV-15.
> 사이드바 추정 ~12 pts + 공통 PLAT ~20 pts(별도, 재사용).

## 🔗 의존성 (PLAT 위에 얹힘)
```
[공통] PLAT-1 event_log, PLAT-2 배정 ─> SNAV-9 (렌더+노출) ─┐
[공통] PLAT-5 대시보드 틀 ─> SNAV-12 (지표 config) ────────┤
SNAV-13(쿼리 ✅) ─> SNAV-12                                  ├─> SNAV-14 (QA·배포) ─> SNAV-15 (판정)
[공통] PLAT-3 SRM ──────────────────────────────────────────┘
SNAV-11r (등록서) ── PLAT-4(훅)가 강제
```
**권장 순서**: (PLAT-1,2 먼저) → SNAV-9 → SNAV-12 → SNAV-11r → SNAV-14 → SNAV-15.

---

## SNAV-9 · Variant UI 렌더 + 노출
> 💡 **쉽게:** 배정받은 버전(variant)대로 사이드바를 실제로 그려주고, 본 순간 '노출' 기록을 남기는 프론트 작업. (배정 자체는 PLAT-2가 해줌)
- **타입** Story · **우선순위** 🟠 High · **컴포넌트** Frontend · **추정** 5 · **Blocked by** PLAT-1(event_log), PLAT-2(배정)
- **설명**: PLAT-2에서 variant 받아 사이드바 A/B 렌더 + 노출 트리거. 변형 정의 [`experiment-spec.md §1`](./experiment-spec.md), 노출 설계 [`implementation-spec.md §6`](./implementation-spec.md).
- **AC**
  - [ ] 앱 로드 시 `GET /assignment`(PLAT-2)로 variant 수신
  - [ ] `treatment`: 확장자 제거 + Projects/Events 최상단 / `control`: 현행 IDE 사이드바
  - [ ] variant 미수신·오류 시 **`control` 폴백**
  - [ ] 사이드바 렌더 완료 시 `exp_exposure` **세션당 1회**(sessionStorage 가드)
  - [ ] `sidebar_item_clicked`(`item_key, position, variant`), 클릭/전환 variant = 노출 variant 일치
- **DoD**: 양 variant 렌더, 노출/클릭이 event_log(PLAT-1)에 정확 적재, 세션당 노출 1회.

## SNAV-11r · 사이드바 실험 등록 (config·등록서)
> 💡 **쉽게:** 이 실험을 플랫폼에 등록하는 설정 파일 작성(안전장치 PLAT-4가 Guardrail 누락을 막아줌).
- **타입** Task · **우선순위** 🟡 Medium · **컴포넌트** Config · **추정** 1 · **상태** 부분(등록서 ✅) · **Blocked by** PLAT-4
- **설명**: 등록서 YAML 블록은 [`implementation-spec.md §11`](./implementation-spec.md)에 작성됨. 플랫폼 `experiments/sidebar-nav-v1.md`에 반영만 남음.
- **AC**: [ ] config에 `primary_kpi·guardrail·ratio·classification(exploratory)` 포함해 등록 (Guardrail 필수 — PLAT-4 통과)
- **DoD**: 등록 성공, Guardrail 누락 시 PLAT-4가 차단함을 확인.

## SNAV-12 · 사이드바 대시보드 구성
> 💡 **쉽게:** PLAT-5(대시보드 틀)에 **사이드바 지표·쿼리를 연결**해 이 실험 화면을 띄움. 틀은 공통, 지표만 이 실험 것.
- **타입** Story · **우선순위** 🟡 Medium · **컴포넌트** Frontend/Data · **추정** 3 · **Blocked by** PLAT-5, SNAV-13
- **AC**
  - [ ] PLAT-5 프레임워크에 sidebar-nav-v1 config 주입(퍼널·CTR·전환·Guardrail 지표 정의)
  - [ ] 퍼널/CTR 쿼리 연결 — [`queries.md S1`](./queries.md), Guardrail S3, SRM 배지(PLAT-3)
  - [ ] KPI 카드 P(T>C)·표본 트래커 표시
- **DoD**: 사이드바 실험 대시보드가 더미·실데이터로 렌더, Guardrail 게이트 동작.

## SNAV-13 · 분석 쿼리  ✅ Done
- 퍼널/CTR/SRM/Guardrail 쿼리 작성 완료 → [`queries.md`](./queries.md). (event_log=PLAT-1 적재 후 실행)

## SNAV-14 · AA·계측 QA → 점진 배포
> 💡 **쉽게:** 배포 전 '양쪽 같은 화면(AA)'으로 거짓 차이 없는지 + 계측 정확한지 점검 후 조금씩 켬.
- **타입** Task · **우선순위** 🟠 High(게이트) · **컴포넌트** QA/Release · **추정** 3 · **Blocked by** SNAV-9, PLAT-1, PLAT-3
- **AC**
  - [ ] AA: 양군 동일 UI에서 CTR 차 통계적 0 확인
  - [ ] 계측 QA: [`data-definition.md §7`](./data-definition.md) 체크리스트 전 항목 통과
  - [ ] 10% 배포 → SRM(PLAT-3) 정상 → 50% 확대
- **DoD**: QA 100%, SRM green, 50% 도달.

## SNAV-15 · 결과 분석 & 4-state 판정 (非DEV)
> 💡 **쉽게:** 데이터 쌓인 뒤 분석가가 'treatment가 정말 나았나' 따져 출시/보류/되돌림 결정(코드 아님).
- **타입** Task · **우선순위** ⚪ Post-data · **컴포넌트** Analytics · **추정** 2 · **Blocked by** SNAV-14, SNAV-12
- **AC**
  - [ ] T0 SRM(PLAT-3) 통과 확인(미통과 시 판정 안 함)
  - [ ] 퍼널·CTR·전환 variant 비교 → `bayesian_calc.py` P(T>C) → Guardrail → 4-state 기록
  - [ ] **주의**: 표본 탐색 분류([`analysis-plan.md §6`](./analysis-plan.md))라 누적 노출 ≥~450/그룹 전엔 보수 해석
