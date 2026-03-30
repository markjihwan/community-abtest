# 실험 등록서: 12기 W7 Magical Week 참여 효과 준실험 평가

## 기본 정보

```
실험명:       12기 W7 Magical Week 참여 효과에 대한 준실험 평가
실험 타입:    Quasi-experiment
분석 타입:    Within-cohort observational comparison
상태:         등록 중 (Treatment 정의 확정 대기)
```

## 배경

12기는 이미 진행 중인 상황으로 온보딩 등 1~2주차 설계가 불가능하다.
W7 Magical Week 기간에 새로운 이벤트를 기획하여, 이 이벤트 주간의 특정 행동이
이후 완주율과 잔존율에 어떤 차이를 만드는지 평가한다.

현재 참여자 집단은 이전 경험 여부가 섞여 있는 비동질적 집단이다.
- 11기를 수강하고 종료한 사람
- 12기만 참여 중인 사람
- 11기를 마친 뒤 12기도 다시 참여 중인 사람

단순 비교 시 기수 차이 외에 재참여 경험, 적응도, 사전 몰입도 차이가 함께 반영될 가능성이 크다.

## 분석 질문

> 12기 참여자 중 Magical Week 핵심 행동 참여자는 비참여자보다
> 이후 완주율과 후기 주차 잔존율이 더 높은가?

## Treatment 정의

> ⏳ 운영진 협의 후 확정 예정

**로깅 항목 (확정):**

| 컬럼 | 설명 |
|------|------|
| `magical_week_exposed_at` | 노출 시점 |
| `magical_week_joined_at` | 참여 시점 |
| `magical_week_mission_completed_at` | 완료 시점 |
| `magical_week_participation_level` | 단계 (노출 / 부분 완료 / 완전 완료) |

## 데이터 설계

### Analysis Unit
`participant within cohort 12` — 개별 참여자, 약 200명

### Feature Grain (W7 이전 시점 고정)

| 컬럼 | 설명 |
|------|------|
| `prior_cohort_experience_flag` | 11기 경험 여부 |
| `attendance_count_pre_w7` | W1~W6 출석 횟수 |
| `assignment_submit_count_pre_w7` | W1~W6 과제 제출 수 |
| `community_activity_count_pre_w7` | W1~W6 게시글 작성 수 |
| `message_exposure_count_pre_w7` | W1~W6 메시지 노출 수 |
| `mentor_group_id` | 멘토 그룹 ID |
| `team_id` | 팀 ID |

### Treatment Grain
`participant` — W7 핵심 미션 완료 여부

### Outcome Grain
`participant-week` (W8 이후) — 주차별 출석, 과제 제출, active 여부

### Final Evaluation Grain
`participant` — 최종 완주 여부

## 지표

### Primary
- **완주율** (완주자 수 / 등록자 수)

### Supporting KPI
- W8~W10 주차별 출석률 (잔존율)
- W8~W10 과제 제출률
- `participation_level` 단계별 완주율 (dose-response)

### Guardrail
> 비참여자의 W8 이탈률이 W7 이전 대비 **10% 이상 증가** 시 → hold

## 분석 방법

### 층화 분석 (Stratified Analysis)

**층화 기준:**

|  | 출석 상위 50% | 출석 하위 50% |
|---|---|---|
| **11기 경험 있음** | 셀 A | 셀 B |
| **11기 경험 없음** | 셀 C | 셀 D |

셀당 평균 약 50명. 각 셀 내에서 W7 참여자 vs 비참여자 완주율 비교.

### Spillover 확인
- `team_id`, `mentor_group_id` 기준 within-team vs between-team 완주율 방향 비교
- 두 결과가 같은 방향이면 Spillover 영향이 작다는 근거

### ITT / ATT 분리 분석

| 분석 | 기준 | 해석 |
|------|------|------|
| ITT (Intent-to-Treat) | `magical_week_exposed_at` | 노출 자체의 효과 |
| ATT (Average Treatment on Treated) | `magical_week_mission_completed_at` | 실제 수행의 효과 |

## 해석 주의문

> "관측된 W7 이전 특성이 유사한 집단 내에서 Magical Week 참여자가 비참여자보다
> 완주율이 높았다. 단, 관측되지 않은 교란변수의 영향을 배제할 수 없어
> 인과 추론이 아닌 연관성 수준으로 해석한다."

## 엔지니어링 구현 계획

### Pre-W7 Feature 스냅샷 (4/25 실행)

W7 시작 전날(4/25) 딱 한 번 실행한다. 이후 W7 행동이 섞이면 공변량이 오염된다.

```sql
-- participant_feature_snapshot 테이블 (또는 별도 스냅샷 테이블)
INSERT INTO participant_feature_snapshot
SELECT
    p.participant_id,
    p.cohort_id,
    '2026-04-25'                                      AS snapshot_date,

    -- 11기 경험 여부
    CASE WHEN prev.cohort_id IS NOT NULL
         THEN 1 ELSE 0 END                            AS prior_cohort_experience_flag,

    -- W1~W6 출석
    COUNT(CASE WHEN wa.week_number <= 6
               AND wa.attended_flag = 1
               THEN 1 END)                            AS attendance_count_pre_w7,

    -- W1~W6 과제 제출
    SUM(CASE WHEN wa.week_number <= 6
             THEN wa.deliverable_submitted_flag
             ELSE 0 END)                              AS assignment_submit_count_pre_w7,

    -- W1~W6 커뮤니티 활동
    SUM(CASE WHEN wa.week_number <= 6
             THEN wa.comment_count + wa.feedback_count
             ELSE 0 END)                              AS community_activity_count_pre_w7,

    -- W1~W6 메시지 노출 (operational_load 또는 별도 로그 참조)
    COALESCE(msg.exposure_count, 0)                   AS message_exposure_count_pre_w7,

    p.mentor_group_id,
    p.team_id

FROM cohort_participation p
LEFT JOIN weekly_activity wa
    ON p.participant_id = wa.participant_id
    AND p.cohort_id = wa.cohort_id
LEFT JOIN cohort_participation prev
    ON p.participant_id = prev.participant_id
    AND prev.cohort_id != p.cohort_id          -- 이전 기수 경험
LEFT JOIN message_exposure_log msg
    ON p.participant_id = msg.participant_id
    AND msg.logged_before = '2026-04-26'

WHERE p.cohort_id = 12
GROUP BY p.participant_id, p.cohort_id, ...;
```

> 주의: `message_exposure_log` 테이블 존재 여부 확인 필요. 없으면 해당 컬럼 제외.

---

### Treatment 로깅 설계 (4/26 W7 시작 시 ON)

event_log에 4가지 이벤트를 추가한다:

```sql
-- event_log 추가 이벤트 정의
event_name                            트리거 시점
-------------------------------------------------------
magical_week_exposed                  참여자에게 W7 이벤트 안내 발송 시
magical_week_joined                   이벤트 참여 의사 표명 / 등록 시
magical_week_mission_completed        핵심 미션 완료 확인 시
magical_week_reminder_sent            리마인드 메시지 발송 시 (노출 로그)
```

```sql
-- event_log 삽입 예시
INSERT INTO event_log (
    participant_id,
    cohort_id,
    experiment_id,
    event_name,
    event_time,
    event_properties_json,
    source_system
) VALUES (
    :participant_id,
    12,
    :experiment_id,
    'magical_week_mission_completed',
    NOW(),
    '{"participation_level": "full", "mission_type": "TBD"}',
    'operation'
);
```

participation_level 값 정의 (운영진 확정 후 채울 것):

| 값 | 설명 |
|---|---|
| `exposed` | 안내만 받음 |
| `partial` | 참여했으나 미션 미완료 |
| `full` | 핵심 미션 완료 |

---

### Outcome 수집 (W8 이후 자동)

기존 `weekly_activity` 테이블이 W8~W10 주차를 자동으로 커버한다.
별도 추가 작업 없이 week_number >= 8 필터로 분석 가능.

---

## 타임라인

```
3/30 (오늘)     treatment 정의 운영진 협의 시작
4/07 (D-19)    treatment 정의 확정 + 로깅 이벤트명 확정
4/14 (D-12)    로깅 코드 개발 완료 + QA
4/21 (D-5)     pre-W7 스냅샷 쿼리 검증 완료
4/25 (D-1)     ★ pre-W7 feature 스냅샷 실행 (W6 종료 후)
4/26           ★ W7 시작 + treatment 로깅 ON
5/02           W7 종료
5/03~          W8+ weekly_activity 수집 (자동)
7월            분석 실행 → decision_log 기록
```

---

## 일정

| 항목 | 일정 |
|------|------|
| Treatment 확정 | 2026-04-07 (운영진 협의) |
| pre-W7 스냅샷 실행 | 2026-04-25 |
| W7 실행 + 로깅 ON | 2026-04-26 |
| W7 종료 | 2026-05-02 |
| Decision deadline | 2026-07월 (12기 종료) |

## 등록 체크리스트

| 항목 | 상태 |
|------|------|
| 가설 | ✅ |
| 실험 단위 | ✅ |
| Treatment 정의 | ⏳ 운영진 협의 중 (4/7 확정 목표) |
| Primary + Guardrail 지표 | ✅ |
| 분석 방법 | ✅ |
| Spillover 통제 | ✅ |
| ITT / ATT 분리 | ✅ |
| 해석 주의문 | ✅ |
| Pre-W7 스냅샷 쿼리 | ✅ |
| Treatment 로깅 설계 | ✅ |
| Decision deadline | ✅ |

**등록 가능 여부: 조건부 가능 — Treatment 정의 확정 후 최종 등록 (목표: 4/7)**
