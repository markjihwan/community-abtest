# 실험 등록서 v2: 12기 W7 Magical Week 참여 효과 준실험 평가

> v2 변경 내용: 핵심 가정 명시, Treatment binary cut 확정, SMD 균형 검사 대응 흐름 추가,
> 표본 크기 및 MDE 계산 항목 추가, Spillover 처리 방법 확정, 해석 주의문 강화

> **참조 문서:** 메트릭 정의, 하이브리드 배정 방식, Quasi-experiment 설계 원칙은
> [`docs/EXPERIMENT_PLAYBOOK.md`](../docs/EXPERIMENT_PLAYBOOK.md)를 기준으로 한다.
> 이 문서는 12기 W7 실험에 특정된 결정사항만 기재한다.

---

## 기본 정보

```
실험명:       12기 W7 Magical Week 참여 효과에 대한 준실험 평가
실험 타입:    Quasi-experiment
분석 타입:    Within-cohort observational comparison
상태:         등록 중 (Treatment 정의 확정 대기)
```

---

## 배경

12기는 이미 진행 중인 상황으로 온보딩 등 1~2주차 설계가 불가능하다.
W7 Magical Week 기간에 새로운 이벤트를 기획하여, 이 이벤트 주간의 특정 행동이
이후 완주율과 잔존율에 어떤 차이를 만드는지 평가한다.

현재 참여자 집단은 이전 경험 여부가 섞여 있는 비동질적 집단이다.
- 11기를 수강하고 종료한 사람
- 12기만 참여 중인 사람
- 11기를 마친 뒤 12기도 다시 참여 중인 사람

단순 비교 시 기수 차이 외에 재참여 경험, 적응도, 사전 몰입도 차이가 함께 반영될 가능성이 크다.

### 왜 준실험인가

- 시점상 randomization이 어렵다.
- "참여자가 더 잘했는가"가 아니라 "특정 행동이 이후 완주 가능성을 높였는가"에 더 가깝다.
- 따라서 인과 추론이 아닌 조건부 연관성 수준으로 해석한다.

---

## 분석 질문

> 12기 참여자 중 Magical Week 핵심 행동 참여자는 비참여자보다
> 이후 완주율과 후기 주차 잔존율이 더 높은가?

---

## 핵심 분석 가정 (명시 필수)

이 분석은 아래 가정이 성립할 때 quasi-causal 해석이 가능하다.
가정이 충족되지 않으면 인과 해석을 포기하고 연관성 기술에 머문다.

### [가정 1] Conditional Independence

W7 이전 특성(prior_cohort_experience, 출석률, 과제 제출 수 등)을
통제했을 때, Magical Week 참여 여부는 이후 완주율과 독립적이다.

즉, "W7 이전에 비슷한 특성을 가진 사람들 사이에서는 참여 여부가 사실상 무작위에 가깝다"는 가정이다.

**가정 검증 방법:** 균형 검사(SMD)로 treatment/control 간 사전 특성 차이를 확인한다.
SMD > 0.2인 공변량이 있으면 이 가정은 의심스럽다.

### [가정 2] SUTVA 부분 충족 (Spillover 제한적)

팀 내 Spillover는 존재할 수 있다.
같은 team_id 내에 treatment 참여자가 있으면 동일 팀 control도 영향을 받을 수 있다.
→ 이를 완전히 차단할 수 없으므로, team_id를 공변량으로 통제하고 결과 해석 시 명시한다.

### [가정 불충족 시 해석 제약]

| 상황 | 해석 수준 |
|---|---|
| SMD ≤ 0.1, Spillover 낮음 | 조건부 quasi-causal 해석 가능 |
| SMD 0.1~0.2 또는 Spillover 의심 | 연관성 수준으로만 해석, 가정 위반 명시 |
| SMD > 0.2 | 탐색 실험으로 재분류, 인과 해석 금지 |

---

## Treatment 정의

### Binary Cut (사전 확정 — 분석 후 변경 금지)

```
Treatment = 1  →  magical_week_mission_completed_at IS NOT NULL
Treatment = 0  →  magical_week_mission_completed_at IS NULL
```

- Treatment 기준은 **핵심 미션 완료** 단일 조건으로 고정한다.
- `magical_week_participation_level`은 보조 분석(dose-response)에만 사용하며
  primary 판단 기준으로 사용하지 않는다.
- 이 기준은 W7 시작 전 확정하며 실험 중간에 변경하지 않는다.

### 노출 설계 원칙

노출 여부를 접속 여부에 맡기지 않는다.
W7 시작 시 카카오톡/슬랙/이메일로 **200명 전원에게 발송**하여 노출을 보장한다.
이후 실제 접속 여부(`visited_w7_flag`)와 미션 완료 여부를 분리해서 로깅한다.

### 로깅 항목

| 컬럼 | 설명 |
|---|---|
| `magical_week_notified_at` | 전원 알림 발송 시점 |
| `visited_w7_flag` | W7 기간(4/26~5/2) 실제 접속 여부 |
| `magical_week_joined_at` | 이벤트 참여 의사 표명 / 등록 시점 |
| `magical_week_mission_completed_at` | 핵심 미션 완료 시점 (Treatment = 1 기준) |
| `magical_week_participation_level` | notified_only / visited / partial / full |

---

## 표본 크기 및 실험 분류

### 사전 계산 항목 (W7 시작 전 확정)

```
전체 참여자 N:              ___명  (12기 등록자)
예상 treatment 참여율:      ___%   (운영진 추정)
  → Treatment n:           ___명
  → Control n:             ___명

현재 완주율 (baseline):     ___%   (11기 또는 12기 초반 추정)
감지 목표 MDE:              ___%p  (절대 차이)

→ calc_sample_size.py 실행:
  python scripts/calc_sample_size.py --baseline 0.XX --mde 0.XX
```

### 실험 분류 기준

| 조건 | 분류 |
|---|---|
| 그룹당 n ≥ 30, MDE 감지 가능 | 결정 실험 — ship/hold 판단 가능 |
| 그룹당 n < 30 또는 MDE 너무 큼 | **탐색 실험** — 방향 탐색만 가능, 결론 내리지 않음 |

> 표본이 부족하면 탐색 실험으로 재분류한다. 결정 실험으로 다루지 않는다. (CLAUDE.md 원칙 #4)

---

## 데이터 설계

### Analysis Unit
`participant within cohort 12` — 개별 참여자, 약 200명

### Feature Grain (W7 이전 시점 고정)

| 컬럼 | 설명 |
|---|---|
| `prior_cohort_experience_flag` | 과거 기수 참여 이력 1회 이상 여부 (기수 간격 무관) |
| `attendance_count_pre_w7` | W1~W6 출석 횟수 |
| `assignment_submit_count_pre_w7` | W1~W6 과제 제출 수 |
| `community_activity_count_pre_w7` | W1~W6 게시글 작성 수 |
| `message_exposure_count_pre_w7` | W1~W6 메시지 노출 수 |
| `mentor_group_id` | 멘토 그룹 ID |
| `team_id` | 팀 ID |

### Treatment Grain
`participant` — W7 핵심 미션 완료 여부 (binary)

### Outcome Grain
`participant-week` (W8 이후) — 주차별 출석, 과제 제출, active 여부

### Final Evaluation Grain
`participant` — 최종 완주 여부

---

## 지표

### Primary KPI
- **완주율** (완주자 수 / 등록자 수)

> 완주율이 개선되지 않으면 실험 성공으로 단정하지 않는다.

### Supporting KPI
- W8~W10 주차별 출석률 (잔존율)
- W8~W10 과제 제출률
- `participation_level` 단계별 완주율 (dose-response 보조 분석)

### Guardrail
- 비참여자의 W8 이탈률이 W7 이전 대비 **10% 이상 증가** 시 → hold
- 3주차 리텐션(W9 기준) 악화 시 → 재검토

> Guardrail이 훼손되면 Primary KPI 결과와 무관하게 ship하지 않는다. (CLAUDE.md 원칙 #1)

---

## 분석 방법

### Step 1. 균형 검사 (SMD)

W7 이전 특성 기준으로 treatment/control 간 균형을 확인한다.

```bash
python scripts/check_balance.py --csv data.csv --treatment treatment_flag
```

**균형 검사 결과에 따른 대응:**

| SMD | 대응 |
|---|---|
| ≤ 0.1 | 균형 충족 — 층화 분석 진행 |
| 0.1~0.2 | 공변량 보정 로지스틱 회귀 사용 (prior_exp + attendance + submit → outcome) |
| > 0.2 | 해석 제한 명시 또는 탐색 실험으로 재분류 |

### Step 2. 층화 분석 (Stratified Analysis)

균형 충족 시 아래 2×2 구조로 층화한다.

|  | 출석 상위 50% | 출석 하위 50% |
|---|---|---|
| **prior 경험 있음** | 셀 A | 셀 B |
| **prior 경험 없음** | 셀 C | 셀 D |

셀당 평균 약 50명. 각 셀 내에서 W7 참여자 vs 비참여자 완주율 비교.

> 셀당 n < 20이면 `stratification_check.py`로 확인 후 층화 분류 단순화 또는 공변량 회귀로 대체.

### Step 3. Bayesian 완주율 비교

```bash
python scripts/bayesian_calc.py \
  --t-success [완주자] --t-total [treatment_n] \
  --c-success [완주자] --c-total [control_n]
```

- P(Treatment > Control) ≥ 95%: ship 고려
- P(Treatment > Control) 80~95%: need_more_data 또는 탐색 분류
- Guardrail 상태를 함께 확인한다

### Step 4. ITT / ATT 분리 분석

| 분석 | 대상 | 기준 | 해석 |
|---|---|---|---|
| ITT (Intent-to-Treat) | 전원 200명 | `magical_week_notified_at` | 알림 발송 자체의 효과 |
| ATT (Average Treatment on Treated) | 미션 완료자 | `magical_week_mission_completed_at` | 실제 수행의 효과 |
| 이탈 분석 | W7 미접속자 | `visited_w7_flag = 0` | 이미 이탈한 집단 별도 파악 |

> ITT와 ATT 결과가 같은 방향이면 알림 발송 자체도 효과가 있다는 근거.
> 방향이 다르면 알림은 효과 없고 실제 수행만 유효함을 의미.

### Step 5. Spillover 확인 및 처리

**처리 방식 (사전 확정):**
team_id를 공변량으로 통제하고 개인 단위 분석을 유지한다.
팀 내 참여율을 추가 공변량으로 포함하여 Spillover 영향을 부분 통제한다.

**Spillover 크기 확인:**
- `team_id` 기준 within-team vs between-team 완주율 방향 비교
- 두 결과가 같은 방향이면 Spillover 영향이 작다는 근거
- 방향이 다르면 결과 해석 시 Spillover 가능성을 명시한다

---

## 해석 주의문

**허용하지 않는 해석:**

```
✗  "Magical Week 참여가 완주율을 높였다" (인과 주장)
✗  "참여하면 완주할 가능성이 X% 높아진다" (개인 예측)
✗  "비참여자는 의지가 부족했다" (속성 귀인)
```

**허용하는 해석:**

```
✓  "참여 그룹은 비참여 그룹보다 완주율이 X%p 높았다"
✓  "W7 이전 특성을 통제한 후에도 참여 그룹의 완주율이 더 높았다"
✓  "이 차이가 Magical Week 개입에서 비롯됐을 가능성이 있다"
✓  "관측되지 않은 교란변수의 영향을 배제할 수 없어 인과 추론이 아닌 연관성 수준으로 해석한다"
```

**인과 해석은 randomized 실험이 가능해진 이후로 미룬다.**

---

## 엔지니어링 구현 계획

### Pre-W7 Feature 스냅샷 (4/25 실행)

W7 시작 전날(4/25) 딱 한 번 실행한다. 이후 W7 행동이 섞이면 공변량이 오염된다.

```sql
INSERT INTO participant_feature_snapshot
SELECT
    p.participant_id,
    p.cohort_id,
    '2026-04-25'                                      AS snapshot_date,

    CASE WHEN prev.cohort_id IS NOT NULL
         THEN 1 ELSE 0 END                            AS prior_cohort_experience_flag,

    COUNT(CASE WHEN wa.week_number <= 6
               AND wa.attended_flag = 1
               THEN 1 END)                            AS attendance_count_pre_w7,

    SUM(CASE WHEN wa.week_number <= 6
             THEN wa.deliverable_submitted_flag
             ELSE 0 END)                              AS assignment_submit_count_pre_w7,

    SUM(CASE WHEN wa.week_number <= 6
             THEN wa.comment_count + wa.feedback_count
             ELSE 0 END)                              AS community_activity_count_pre_w7,

    COALESCE(msg.exposure_count, 0)                   AS message_exposure_count_pre_w7,
    p.mentor_group_id,
    p.team_id

FROM cohort_participation p
LEFT JOIN weekly_activity wa
    ON p.participant_id = wa.participant_id
    AND p.cohort_id = wa.cohort_id
LEFT JOIN cohort_participation prev
    ON p.participant_id = prev.participant_id
    AND prev.cohort_id != p.cohort_id
LEFT JOIN message_exposure_log msg
    ON p.participant_id = msg.participant_id
    AND msg.logged_before = '2026-04-26'

WHERE p.cohort_id = 12
GROUP BY p.participant_id, p.cohort_id, ...;
```

> 주의: `message_exposure_log` 테이블 존재 여부 확인 필요. 없으면 해당 컬럼 제외.

### Treatment 로깅 설계 (4/26 W7 시작 시 ON)

```
event_name                            트리거 시점
-------------------------------------------------------
magical_week_notified                 200명 전원 알림 발송 시
magical_week_visited                  W7 기간(4/26~5/2) 접속 확인 시
magical_week_joined                   이벤트 참여 의사 표명 / 등록 시
magical_week_mission_completed        핵심 미션 완료 확인 시 (Treatment = 1)
magical_week_reminder_sent            리마인드 메시지 발송 시
```

```sql
INSERT INTO event_log (
    participant_id, cohort_id, experiment_id,
    event_name, event_time, event_properties_json, source_system
) VALUES (
    :participant_id, 12, :experiment_id,
    'magical_week_mission_completed',
    NOW(),
    '{"participation_level": "full", "mission_type": "TBD"}',
    'operation'
);
```

| participation_level 값 | 설명 |
|---|---|
| `notified_only` | 알림 받았으나 W7 기간 미접속 |
| `visited` | 접속했으나 이벤트 미참여 |
| `partial` | 참여했으나 미션 미완료 |
| `full` | 핵심 미션 완료 (Treatment = 1) |

### Outcome 수집 (W8 이후 자동)

기존 `weekly_activity` 테이블이 W8~W10 주차를 자동으로 커버한다.
별도 추가 작업 없이 `week_number >= 8` 필터로 분석 가능.

---

## 타임라인

```
4/07 (D-19)    treatment 정의 확정 + 로깅 이벤트명 확정
               표본 크기 계산 완료 → 실험 분류(결정/탐색) 확정
4/14 (D-12)    로깅 코드 개발 완료 + QA
4/21 (D-5)     pre-W7 스냅샷 쿼리 검증 완료
4/25 (D-1)     ★ pre-W7 feature 스냅샷 실행 (W6 종료 후)
4/26           ★ W7 시작 + treatment 로깅 ON
5/02           W7 종료
5/03~          W8+ weekly_activity 수집 (자동)
7월            균형 검사 → 분석 방법 확정 → Bayesian 계산 → decision_log 기록
```

---

## 프로덕트 관점 확정 항목

| 항목 | 내용 |
|---|---|
| 실험명 | 12기 W7 Magical Week 참여 효과 준실험 평가 |
| 실험 타입 | Quasi-experiment |
| 분석 타입 | Within-cohort observational comparison |
| Treatment 정의 | magical_week_mission_completed_at IS NOT NULL |
| Primary outcome | 완주율 |
| Supporting KPI | W8~W10 잔존율, 과제 제출률, dose-response |
| Guardrail | 비참여자 W8 이탈률 +10% 초과, 3주차 리텐션 악화 |
| 해석 주의문 | 인과 해석 금지, 연관성 수준으로만 기술 |
| Decision deadline | 2026-07월 (12기 종료) |

---

## 등록 체크리스트

| 항목 | 상태 |
|---|---|
| 가설 | ✅ |
| 실험 단위 | ✅ |
| 핵심 분석 가정 명시 | ✅ |
| Treatment binary cut 확정 | ⏳ 운영진 협의 중 (4/7 확정 목표) |
| 표본 크기 및 실험 분류 | ⏳ Treatment 확정 후 calc_sample_size.py 실행 |
| Primary + Guardrail 지표 | ✅ |
| 균형 검사 대응 흐름 | ✅ |
| 분석 방법 (ITT/ATT/층화/Bayesian) | ✅ |
| Spillover 처리 방법 확정 | ✅ (공변량 통제 + 개인 단위 유지) |
| 해석 주의문 (허용/금지 명시) | ✅ |
| Pre-W7 스냅샷 쿼리 | ✅ |
| Treatment 로깅 설계 | ✅ |
| Decision deadline | ✅ |

**등록 가능 여부: 조건부 가능 — Treatment 정의 + 표본 크기 계산 확정 후 최종 등록 (목표: 4/7)**