# Data Schema

## 1. Design Goal

이 스키마는 단순 운영 로그 저장이 아니라 `실험 설계 -> 참여자 배정 -> 이벤트 수집 -> KPI 계산 -> 결과 판정 -> 학습 축적`까지 이어지는 구조를 목표로 한다.

따라서 아래 여섯 가지를 동시에 만족해야 한다.

- cohort 비교가 가능해야 한다.
- Funnel과 Retention 계산이 가능해야 한다.
- 실험 채택 의사결정에 필요한 Guardrail 계산이 가능해야 한다.
- 실험 정의와 버전 이력을 남길 수 있어야 한다.
- 데이터 품질 검증이 가능해야 한다.
- 실험에서 얻은 학습을 다음 기수에 재사용할 수 있어야 한다.

## 2. Schema Layers

권장 스키마는 아래 다섯 레이어로 나눈다.

| 레이어 | 역할 | 대표 테이블 |
| --- | --- | --- |
| Master | 기준 정보 관리 | `program`, `cohort`, `participant` |
| Experiment | 실험 설계와 배정 | `experiment`, `experiment_variant`, `assignment` |
| Event | 활동 로그 수집 | `event_log`, `weekly_activity`, `operational_load` |
| Analytics | KPI 계산과 결과 저장 | `metric_catalog`, `metric_snapshot`, `experiment_result` |
| Governance | 품질 검증과 학습 기록 | `data_quality_check`, `decision_log`, `learning_note` |

## 3. Core Tables

### Program

커뮤니티/프로그램 단위의 상위 엔터티다.

- `program_id`
- `program_name`
- `program_type`
- `program_status`
- `created_at`
- `updated_at`

### Cohort

기수 단위 운영 정보를 저장한다.

- `cohort_id`
- `program_id`
- `cohort_name`
- `cohort_number`
- `start_date`
- `end_date`
- `operator_id`
- `cohort_status`
- `season_tag`
- `notes`

### Participant

참여자 기준 엔터티다. 기수와 독립된 사람 식별자를 둔다.

- `participant_id`
- `external_user_id`
- `joined_community_at`
- `participant_type`
- `profile_segment`
- `created_at`
- `updated_at`

### Cohort Participation

한 명이 여러 기수에 참여할 수 있으므로, 참여 이력은 별도 브리지 테이블로 관리한다.

- `cohort_participation_id`
- `participant_id`
- `cohort_id`
- `applied_at`
- `approved_at`
- `first_attended_at`
- `completed_flag`
- `completed_at`
- `dropped_flag`
- `dropped_at`
- `drop_reason`
- `rejoin_next_cohort_flag`
- `prior_attendance_rate`
- `preprogram_activity_score`
- `application_engagement_score`
- `week1_intensity_score`

## 4. Experiment Layer

### Experiment

실험 자체를 정의하는 테이블이다.

- `experiment_id`
- `program_id`
- `experiment_name`
- `experiment_type`
- `analysis_type`
- `hypothesis`
- `primary_metric_id`
- `start_date`
- `end_date`
- `status`
- `owner_id`
- `decision_deadline`
- `created_at`
- `updated_at`

권장 값 예시:

- `experiment_type`: `randomized_ab`, `cohort_comparison`, `quasi_experiment`
- `analysis_type`: `bayesian`, `frequentist`, `sequential`, `bayesian_sequential`

### Experiment Variant

실험군과 대조군 정의 테이블이다.

- `variant_id`
- `experiment_id`
- `variant_key`
- `variant_name`
- `variant_role`
- `description`
- `allocation_ratio`
- `is_control`

### Assignment

누가 어떤 실험군에 속했는지 저장한다. cohort 비교 환경에서도 이 테이블은 필요하다.

- `assignment_id`
- `experiment_id`
- `variant_id`
- `participant_id`
- `cohort_id`
- `assigned_at`
- `assignment_unit`
- `assignment_method`
- `assignment_reason`

권장 값 예시:

- `assignment_unit`: `participant`, `cohort`
- `assignment_method`: `random`, `manual`, `cohort_based`

## 5. Event Layer

### Event Log

모든 원천 이벤트는 가능한 한 정규화된 로그로 먼저 저장한다.

- `event_id`
- `participant_id`
- `cohort_id`
- `experiment_id`
- `event_name`
- `event_time`
- `event_value`
- `event_properties_json`
- `source_system`
- `ingested_at`

권장 이벤트 이름:

- `application_submitted`
- `application_approved`
- `first_session_attended`
- `weekly_session_attended`
- `presentation_submitted`
- `feedback_sent`
- `comment_posted`
- `collaboration_logged`
- `deliverable_submitted`
- `program_completed`
- `cohort_rejoined`

### Weekly Activity

분석 편의를 위한 주차별 집계 테이블이다.

- `weekly_activity_id`
- `participant_id`
- `cohort_id`
- `week_number`
- `attended_flag`
- `presentation_count`
- `feedback_count`
- `comment_count`
- `collaboration_count`
- `mentor_interaction_count`
- `deliverable_submitted_flag`
- `activity_score`
- `created_at`

### Operational Load

운영 리소스 사용량을 기록한다.

- `operational_load_id`
- `cohort_id`
- `experiment_id`
- `week_number`
- `mentor_minutes`
- `manual_intervention_count`
- `reminder_sent_count`
- `operator_hours`
- `issue_count`
- `recorded_at`

## 6. Analytics Layer

### Metric Catalog

지표 정의를 메타데이터로 관리한다. KPI 정의 변경을 방지하기 위한 핵심 테이블이다.

- `metric_id`
- `metric_name`
- `metric_display_name`
- `metric_category`
- `metric_role`
- `formula_text`
- `numerator_definition`
- `denominator_definition`
- `grain`
- `direction`
- `is_active`
- `created_at`

권장 값 예시:

- `metric_category`: `funnel`, `retention`, `outcome`, `guardrail`, `leading`
- `metric_role`: `north_star`, `supporting`, `guardrail`, `leading_indicator`
- `direction`: `higher_is_better`, `lower_is_better`

### Metric Snapshot

계산된 KPI 값을 시점별로 저장한다.

- `metric_snapshot_id`
- `metric_id`
- `experiment_id`
- `variant_id`
- `cohort_id`
- `snapshot_date`
- `window_type`
- `metric_value`
- `numerator_value`
- `denominator_value`
- `sample_size`
- `calculated_at`

### Experiment Result

실험별 최종 또는 중간 분석 결과를 저장한다.

- `experiment_result_id`
- `experiment_id`
- `analysis_run_at`
- `primary_metric_id`
- `control_variant_id`
- `treatment_variant_id`
- `uplift_value`
- `uplift_unit`
- `probability_b_beats_a`
- `guardrail_risk_score`
- `minimum_effect_threshold`
- `sample_size`
- `analysis_notes`

## 7. Governance Layer

### Data Quality Check

실험 신뢰성을 보장하기 위한 품질 검증 테이블이다.

- `quality_check_id`
- `experiment_id`
- `check_date`
- `check_type`
- `check_status`
- `observed_value`
- `expected_value`
- `details`

권장 체크 예시:

- `sample_ratio_mismatch`
- `missing_events`
- `timestamp_delay`
- `metric_definition_mismatch`

### Decision Log

실험 의사결정 이력을 저장한다.

- `decision_id`
- `experiment_id`
- `decision_date`
- `decision_type`
- `decision_status`
- `decision_reason`
- `approved_by`
- `next_action`

권장 값 예시:

- `decision_status`: `ship`, `hold`, `rollback`, `need_more_data`

### Learning Note

실험에서 얻은 학습을 재사용 가능한 형태로 기록한다.

- `learning_note_id`
- `experiment_id`
- `title`
- `summary`
- `is_counterintuitive`
- `related_metric_id`
- `recommended_action`
- `created_by`
- `created_at`

이 테이블은 Microsoft/Booking의 `flywheel` 관점에서 특히 중요하다. 즉 실험은 결과 저장으로 끝나는 것이 아니라, 조직 학습 자산으로 축적되어야 한다.

## 8. Minimum Required Fields by Use Case

### Funnel 계산 필수

- `participant_id`
- `cohort_id`
- `applied_at`
- `approved_at`
- `first_attended_at`
- `completed_flag`

### Retention 계산 필수

- `participant_id`
- `cohort_id`
- `week_number`
- `attended_flag`

### Guardrail 계산 필수

- `participant_id`
- `cohort_id`
- `dropped_flag`
- `mentor_minutes`
- `manual_intervention_count`

### Leading Indicator 탐색 필수

- `presentation_count`
- `feedback_count`
- `comment_count`
- `collaboration_count`

### 실험 판정 필수

- `experiment_id`
- `variant_id`
- `metric_id`
- `metric_value`
- `probability_b_beats_a`
- `decision_status`

## 9. Recommended Keys and Relationships

핵심 연결 관계는 아래와 같다.

- `program 1:N cohort`
- `participant 1:N cohort_participation`
- `cohort 1:N cohort_participation`
- `program 1:N experiment`
- `experiment 1:N experiment_variant`
- `experiment 1:N assignment`
- `participant 1:N assignment`
- `experiment 1:N experiment_result`
- `metric_catalog 1:N metric_snapshot`
- `experiment 1:N decision_log`
- `experiment 1:N data_quality_check`
- `experiment 1:N learning_note`

## 10. Recommended Implementation Notes

### 1. 원천 이벤트와 집계 테이블을 분리한다

`event_log`는 가능한 한 원본 그대로 보존하고, `weekly_activity`, `metric_snapshot`은 파생 테이블로 운영한다.

### 2. 사람과 기수 참여를 분리한다

`participant`와 `cohort_participation`을 나누지 않으면 재참여율, 과거 공변량, 기수 간 비교가 어려워진다.

### 3. 지표 정의를 코드가 아니라 테이블에도 남긴다

`metric_catalog`가 없으면 운영 중 KPI 해석이 흔들릴 가능성이 크다.

### 4. 실험 결과뿐 아니라 품질과 의사결정을 같이 저장한다

실험 플랫폼에서 중요한 것은 `값`만이 아니라 `믿을 수 있는가`, `무슨 결정을 했는가`까지 남기는 것이다.

### 5. 학습 자산 테이블을 반드시 둔다

counterintuitive result, 실패한 실험, 보류한 실험도 모두 조직의 자산이다.

## 11. MVP Schema Recommendation

처음부터 모든 테이블을 구현하기 어렵다면 아래 최소 세트부터 시작한다.

### 반드시 구현

- `cohort`
- `participant`
- `cohort_participation`
- `event_log`
- `weekly_activity`
- `operational_load`
- `metric_catalog`
- `metric_snapshot`

### 2단계에서 추가

- `experiment`
- `experiment_variant`
- `assignment`
- `experiment_result`
- `decision_log`

### 3단계에서 추가

- `data_quality_check`
- `learning_note`

## 12. Practical Summary

현재 초안은 운영 데이터 관점에서는 출발점으로 충분했지만, 실험 플랫폼 DB로 보기에는 아래가 부족했다.

- 실험 정의 테이블
- variant 및 assignment 테이블
- KPI 메타데이터 테이블
- 실험 결과 저장 테이블
- 데이터 품질 검증 테이블
- 학습 기록 테이블

이 보강안을 기준으로 가면 `가짜연구소형 cohort 실험 운영 DB`로 확장 가능한 구조를 만들 수 있다.
