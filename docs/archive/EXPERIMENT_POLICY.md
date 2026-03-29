# Experiment Policy

## 1. Purpose

이 문서는 `abtest` 플랫폼에서 `어떤 조건이 갖춰져야 실험을 시작할 수 있는지`, `누가 어떤 기준으로 승인하는지`, `실험 단위와 변형을 어떻게 정의하는지`, `동시 운영 시 어떤 충돌 규칙을 따르는지`를 정리한 상위 정책 문서다.

이 문서는 운영 체크리스트보다 상위 레이어이며, 개별 실험 실행 전에 따라야 하는 공통 규칙을 정의한다.

## 2. Policy Scope

이 문서는 다음 다섯 영역을 다룬다.

- 실험 등록 요건
- 실험 승인 기준
- 실험 단위 정의
- Variant 정의 규칙
- 중복 및 충돌 규칙

이 문서는 아직 참여자 정책, 데이터 정책, 결과 활용 정책까지 포함하지 않는다. 해당 영역은 별도 정책 문서에서 다룬다.

## 3. Experiment Registration Requirements

실험으로 등록되려면 아래 항목이 모두 준비되어야 한다.

### Required Fields

1. 실험명
2. 실험 목적
3. 명시적 가설
4. 실험 변수
5. Primary metric
6. Guardrail metric
7. 관측 기간
8. 판단 시점 또는 decision deadline
9. 실험 오너

추가로 가능하면 아래 항목도 함께 기록한다.

- 예상 리스크
- 대상 cohort
- 분석 방식
- 최소 기대 효과
- 중단 조건

### Registration Rule

아래 조건을 모두 만족해야 `registered` 상태로 인정한다.

- 가설이 문장으로 명확히 적혀 있다.
- `무엇을 바꾸는지`와 `무엇이 좋아져야 하는지`가 구분되어 있다.
- Primary metric이 1개로 고정되어 있다.
- Guardrail이 1개 이상 지정되어 있다.
- 관측 기간이 명시되어 있다.
- 실험 책임자가 지정되어 있다.

### Registration Rejection Cases

아래 중 하나라도 해당하면 등록 불가다.

- 가설 없이 아이디어만 있는 경우
- Primary metric이 2개 이상으로 흔들리는 경우
- Guardrail이 없는 경우
- 변경 내용이 너무 넓어서 무엇이 효과를 냈는지 구분할 수 없는 경우
- 실험 종료 기준이 없는 경우

## 4. Experiment Approval Policy

### Approval Principle

실험 등록과 실험 승인은 분리한다.

- 등록: 실험 정의가 문서화되었는가
- 승인: 지금 이 실험을 실제로 돌려도 되는가

### Approval Criteria

아래 항목을 기준으로 승인 여부를 판단한다.

- 목적이 현재 운영 우선순위와 맞는가
- 변경 범위가 단일 실험으로 다룰 수 있을 만큼 좁은가
- Primary metric과 Guardrail이 충분히 정의되었는가
- 관측 기간과 판단 시점이 현실적인가
- 기존 실험과 충돌하지 않는가
- 오너가 결과 해석과 후속 액션을 책임질 수 있는가

### Approval Outcomes

승인 결과는 아래 중 하나다.

- `approved`
- `approved_with_conditions`
- `rejected`

### Conditional Approval Cases

아래 상황은 조건부 승인으로 둘 수 있다.

- Guardrail 정의는 있으나 threshold가 아직 모호한 경우
- 예상 표본이 작아 exploratory experiment로만 운영하는 경우
- 기존 cohort 운영과 겹치지만 영향 범위가 제한적인 경우

조건부 승인 시 반드시 보완 항목과 재확인 시점을 함께 기록한다.

## 5. Experiment Unit Definition

### Default Unit

현재 기본 실험 단위는 `cohort`다.

즉, 기본 정책상 하나의 실험은 아래처럼 정의한다.

`한 기수 또는 기수 간 비교를 통해 특정 운영 변화의 영향을 평가하는 단위`

### Default Interpretation

- 기본 운영 환경은 randomized participant-level A/B가 아니다.
- 기본 비교 단위는 cohort-based comparative experiment다.
- 문서상 분류는 quasi-experiment로 기록한다.

### Exception Cases

아래 조건에서는 예외적으로 더 작은 단위를 사용할 수 있다.

- 동일 cohort 내에서 명확한 소그룹 분리가 가능한 경우
- 운영 개입이 그룹 단위로 독립적으로 적용되는 경우
- 배정 규칙과 오염 가능성이 문서화된 경우

예외 단위를 쓰는 경우 반드시 아래를 함께 기록한다.

- assignment unit
- assignment method
- contamination risk

### Identifier Rule

실험 식별자는 재사용하지 않는다.

- `experiment_id`는 전역 고유값
- `variant_key`는 실험 내부 고유값
- `cohort_id`는 운영 단위 고유값

## 6. Variant Definition Rule

### Single Change Principle

하나의 실험은 가능한 한 `하나의 핵심 변화`만 검증해야 한다.

좋은 예:

- 리마인드 메시지 빈도 변경
- 첫 주 온보딩 세션 구조 변경
- 피드백 방식 변경

나쁜 예:

- 온보딩, 과제, 멘토링, 평가 방식을 한 번에 모두 변경

### Control Policy

모든 실험은 원칙적으로 control을 명시한다.

- control: 현재 운영 기준안
- treatment: 바꾸려는 운영안

cohort 비교 환경에서도 control은 `기준 cohort` 또는 `기존 운영안`으로 명시한다.

### Variant Documentation Rule

각 variant는 아래 항목이 기록되어야 한다.

- variant name
- variant role
- description
- expected mechanism
- 적용 대상

### Mid-Experiment Change Policy

실험 시작 후 variant 정의를 바꾸는 것은 원칙적으로 금지한다.

예외적으로 변경이 필요하면 아래 절차를 따른다.

- 변경 이유 기록
- 기존 결과와 이후 결과 분리
- 필요 시 새 실험으로 재등록

## 7. Overlap and Conflict Policy

### Basic Rule

동일한 대상, 동일한 시점, 동일한 KPI에 영향을 줄 수 있는 실험은 동시에 운영하지 않는다.

### Conflict Types

다음은 충돌 가능성이 높은 케이스다.

- 같은 cohort에 두 개 이상의 onboarding 변경 실험
- 같은 cohort에 같은 guardrail을 흔들 수 있는 운영 변경
- 동일 기간에 결과 해석을 혼동시키는 메시지/과제/평가 구조 변경

### Allowed Overlap Cases

아래는 제한적으로 허용할 수 있다.

- 완전히 다른 funnel 단계에 작동하는 실험
- 서로 다른 cohort에 독립적으로 적용되는 실험
- exploration 성격이며 영향 범위가 매우 작은 실험

### Freeze Rule

실험 시작 이후 아래 구간에서는 비계획 변경을 금지한다.

- 실험 시작 직후 초기 안정화 구간
- decision deadline 직전 해석 구간

권장 표현:

`변경 금지 기간(freeze window)을 두고, 해당 기간에는 variant 외 운영 요소를 임의로 수정하지 않는다.`

## 8. Required DB Metadata for This Policy

이 정책을 DB에 반영하려면 최소한 아래 메타데이터가 필요하다.

- `experiment_name`
- `hypothesis`
- `experiment_type`
- `assignment_unit`
- `assignment_method`
- `primary_metric_id`
- `guardrail_metric_list`
- `decision_deadline`
- `status`
- `owner_id`
- `approval_status`
- `approval_note`
- `conflict_check_status`

## 9. Practical Summary

이 문서의 핵심은 아래와 같다.

- 실험은 아이디어가 아니라 등록 요건을 갖춘 단위여야 한다.
- 등록과 승인은 분리한다.
- 기본 실험 단위는 cohort다.
- variant는 단일 핵심 변화를 중심으로 정의한다.
- 같은 해석 공간을 흔드는 동시 실험은 금지하거나 강하게 제한한다.
