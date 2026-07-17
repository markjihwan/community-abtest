> **📄 요약 ·** 2차 사이드바 분석계획 — 무작위 A/B(인과 가능), SRM 게이트·퍼널·Bayesian·표본 분류(=탐색). 분석가용.

# 사이드바 내비 A/B — 분석계획서 (Analysis Plan)

| 항목 | 값 |
|---|---|
| 실험명 | Sidebar Navigation Optimization for Categorization Fluency |
| `experiment_id` | `sidebar-nav-v1` |
| 설계 유형 | **무작위 A/B** (50:50, 개인 단위) |
| 노출 기간 | 2026-06-28 ~ (누적) |
| 작성일 | 2026-06-22 |
| 상태 | 계획 (pre-registration) |
| 연결 문서 | [실험 spec](./experiment-spec.md) · [데이터 정의](./data-definition.md) · [실행 명세](./implementation-spec.md) · [쿼리](./queries.md) · [Playbook](../../00_common/playbook.md) · [scripts](../../00_common/scripts/) |

---

## 0. 분석의 성격 (한 줄)

> **무작위 배정**이므로 회고 준실험과 달리 선택편향 통제(SMD/PSM)가 불필요하고 **인과 해석이 가능**하다. 단, 그 인과 주장은 **(1) 노출(exposure) 정의의 유효성**과 **(2) SRM 무결성** 두 전제 위에서만 성립한다 — 이 둘이 깨지면 무작위성도 무효다.

---

## 1. 핵심 질문 & 가설

- **핵심 질문**: 확장자 제거 + 핵심메뉴 상단 배치(treatment)가 핵심메뉴 CTR과 등록 전환을 높이는가?
- **가설**: 범주화 유창성 ↑ → treatment의 핵심메뉴 CTR·전환 > control.
- **귀무**: `CTR_treatment − CTR_control = 0`.

---

## 2. 모집단 & 분기 정의

### 2-1. 분석 모집단 (가장 중요)
> **`exp_exposure`가 발생한 유저**(= 배정 variant 사이드바를 실제로 본 사람)로 고정한다.
> 배정만 되고 미노출인 유저는 제외 → **노출 편향 차단**(회고 실험의 생존자 편향과 동일 교훈).

### 2-2. 비교군 분기
| 군 | 정의 |
|---|---|
| control | 결정적 배정 결과 control (현행 IDE 사이드바) |
| treatment | 결정적 배정 결과 treatment (확장자 제거·핵심메뉴 상단) |
> 배정: `sha256(experiment_id:uid)[:8] % 100 < 50 → treatment`, sticky. 레퍼런스 `00_common/scripts/assign_variant.py`(검증: 50.02%·sticky=True).

### 2-3. 노출 정의 유효성 (분모·무작위성의 전제)
- `exp_exposure`는 **세션당 1회**, 사이드바 렌더 시점에 발생(dedup).
- 클릭/전환 이벤트의 `variant`는 **반드시 같은 세션 노출의 variant와 일치**해야 함(불일치 = 계측 버그 → 무효).

---

## 3. 데이터 소스 맵
| 소스 | 키/필드 | 용도 |
|---|---|---|
| `event_log` | `event_name`, `variant`, `experiment_id`, `user_id/anon_id`, `session_id`, `properties` | 퍼널·CTR·전환·Guardrail |
| `exp_exposure` | 노출 유니크 유저 | **분모** + SRM |
| `sidebar_item_clicked` | `item_key∈{projects,events}` | CTR 분자 |
| `enrollment_completed` / `project_alert_signup` | 전환 | Primary/Secondary |
| assignment config | variant·ratio·status | SRM 기대비율 |
> 스키마·이벤트 카탈로그 상세: [`data-definition.md`](./data-definition.md). `event_log`는 incremental(중복 없음).

---

## 4. 분석 트랙

### T0 — SRM 무결성 검증 (선행 게이트)
노출 유니크 유저 비율이 50:50에서 벗어났는지 카이제곱. **`p<0.001`이면 분석 중단·배정 점검.** → `queries.md S2` + `00_common/scripts/srm_check.py`(검증: 50.4:49.6→정상 / 54:46→차단).

### T1 — Primary: 퍼널 + CTR/전환 (variant 비교)
`노출 → 핵심메뉴 클릭 → 대상 페이지뷰 → 등록` 퍼널을 variant별로. CTR=클릭/노출, 전환=등록/노출. → `queries.md S1`.
- 유의성: **Bayesian P(T>C)** (`00_common/scripts/bayesian_calc.py`). p-value 단독 결론 금지.

### T2 — Guardrail
홈 이탈률(단일 page_view·무클릭 세션), 첫 방문 세션시간 variant 비교. → `queries.md S3`.

### T3 — 세그먼트 (사후, 설명용)
device · 유입 source · 신규/기존 · page. 이질효과 탐색. **단독 성공 판정 금지.**

### T4 — AA 사전검증
배포 전 동일 UI 양군에서 CTR 차이가 통계적으로 0에 수렴하는지 확인(계측·배정 무결성).

---

## 5. Guardrail 모니터링
| Guardrail | 정의 | 차단 규칙 |
|---|---|---|
| 홈 이탈률(Bounce) | 단일 page_view·무클릭 세션 / 홈 진입 세션 | 악화 시 ship 불가 |
| 첫 방문 세션시간 | median(마지막-처음 이벤트) | 악화 시 ship 불가 |
> **Guardrail 훼손 시 Primary 결과와 무관하게 ship하지 않는다.**

---

## 6. 표본 크기 & 실험 분류 게이트
`00_common/scripts/calc_sample_size.py` 실행(α=.05, power=.8): MAU 500 → 그룹당 250.
| baseline CTR | +3%p | +5%p | +8%p |
|---|---|---|---|
| 15% | 2,402 | 906 | 377 |
| 20% | 2,943 | 1,094 | 447 |
| 25% | 3,397 | 1,251 | 504 |

> **결론: 현 트래픽은 전 시나리오 필요표본(>250) 미달 → 탐색 실험으로 분류.**
> 결정 실험화 조건 = (MDE ≥ +8%p) AND (**누적 유니크 노출 ≥ ~450/그룹**까지 장기 운영). 그 전엔 방향만, ship 단정 금지.

---

## 7. 최종 판정 기준 (Playbook 3-6)
| 판정 | 조건 |
|---|---|
| `ship` | P(T>C) ≥ 95% + Guardrail 이상 없음 + 표본 게이트 통과 |
| `hold` | P(T>C) < 80% 또는 Control 우위 |
| `rollback` | Guardrail 훼손 또는 Primary 악화 |
| `need_more_data` | 80~90% 또는 표본 부족(탐색 분류 상태) |
> Guardrail 우선. SRM(T0) 미통과 시 어떤 판정도 내리지 않는다.

---

## 8. 계측 체크리스트 (배포 전 필수)
> 상세: [`data-definition.md §7`](./data-definition.md). 핵심:
- [ ] `exp_exposure` 세션당 1회·렌더 시점 발생 (분모 정확성)
- [ ] 클릭/전환 `variant` = 노출 variant 100% 일치
- [ ] 비로그인→로그인 `anon_id↔user_id` 연결
- [ ] `item_key`/`enroll_type`/`page` enum 준수
- [ ] AA 테스트로 양군 CTR 차 ≈ 0 확인

---

## 9. 분석 타임라인
| 시점 | 가능한 분석 |
|---|---|
| ~배포 전 | AA·계측 QA(T4), 모수·배정 확정 |
| 6/28~ 점진배포 | T0 SRM 일일 점검, Guardrail 모니터 |
| 누적 중 | T1 퍼널·CTR(방향), T3 세그먼트 탐색 |
| 표본 게이트 통과 후 | **T1 Bayesian 판정 → 4-state**(Guardrail 확인 후) |

---

## 10. 해석 원칙 (Playbook 3-5 + 무작위 보정)
**허용** ✓
- "treatment 그룹은 control보다 핵심메뉴 CTR이 X%p 높았다"
- (무작위라) "사이드바 개입이 CTR을 높였을 가능성이 높다" — **SRM·노출 정의 유효 전제**

**불허** ✗
- SRM(T0)이 깨진 채 내리는 결론
- 노출 정의를 무시한 분모(배정-only 포함)
- 표본 게이트 미통과 상태의 ship 단정
