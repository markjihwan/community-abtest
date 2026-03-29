# Statistical Columns

## 1. Purpose

이 문서는 `abtest` DB에 어떤 통계 컬럼을 넣을 수 있는지, 그리고 어떤 컬럼은 지금 단계에서 꼭 넣고 어떤 컬럼은 나중에 추가해도 되는지 정리한 문서다.

핵심 원칙은 `통계 컬럼은 많이 넣는 것보다, 해석 가능한 컬럼을 일관되게 넣는 것`이다.

## 2. Where Statistical Columns Belong

통계 컬럼은 모든 테이블에 흩뿌리기보다 아래 두 테이블에 집중하는 것이 좋다.

| 테이블 | 역할 | 통계 컬럼 성격 |
| --- | --- | --- |
| `metric_snapshot` | 특정 시점 KPI 계산 결과 저장 | raw metric + 표본 수 + 기본 구간 |
| `experiment_result` | 실험 비교 결과 저장 | uplift + uncertainty + decision support |

## 3. Minimum Statistical Columns

가장 먼저 넣기 좋은 최소 컬럼은 아래와 같다.

### In `metric_snapshot`

- `metric_value`
- `numerator_value`
- `denominator_value`
- `sample_size`

이 네 개만 있어도 KPI 계산 근거를 다시 확인할 수 있다.

### In `experiment_result`

- `uplift_value`
- `uplift_unit`
- `sample_size`
- `analysis_run_at`

이 네 개만 있어도 실험 비교 결과의 최소 형태는 갖춘다.

## 4. Recommended Statistical Columns

정책과 해석의 일관성을 위해 아래 컬럼까지는 권장한다.

### Effect Size and Uncertainty

- `standard_error`
- `confidence_interval_lower`
- `confidence_interval_upper`
- `credible_interval_lower`
- `credible_interval_upper`

설명:

- frequentist 중심이면 confidence interval
- Bayesian 중심이면 credible interval
- 둘 다 병행하려면 둘 다 둘 수 있다

### Significance and Probability

- `p_value`
- `alpha_level`
- `power_target`
- `probability_b_beats_a`
- `probability_guardrail_regression`

설명:

- `p_value`는 선택 사항이지만 frequentist 해석을 병행할 때 유용하다
- `probability_b_beats_a`는 현재 문서 체계와 가장 잘 맞는 핵심 Bayesian 컬럼이다
- `probability_guardrail_regression`은 guardrail 악화 위험을 수치화하는 데 중요하다

### Experimental Context

- `analysis_method`
- `window_type`
- `baseline_value`
- `variant_value`
- `minimum_effect_threshold`

설명:

- 같은 uplift라도 어떤 방법으로 계산했는지 남겨야 한다
- baseline과 variant 절대값을 남겨야 결과를 재해석하기 쉽다

## 5. Strongly Recommended Column Set

현재 프로젝트 기준으로 가장 실용적인 컬럼 세트는 아래와 같다.

### `metric_snapshot`

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
- `standard_error`
- `confidence_interval_lower`
- `confidence_interval_upper`
- `calculated_at`

### `experiment_result`

- `experiment_result_id`
- `experiment_id`
- `analysis_run_at`
- `analysis_method`
- `primary_metric_id`
- `control_variant_id`
- `treatment_variant_id`
- `baseline_value`
- `variant_value`
- `uplift_value`
- `uplift_unit`
- `confidence_interval_lower`
- `confidence_interval_upper`
- `probability_b_beats_a`
- `probability_guardrail_regression`
- `minimum_effect_threshold`
- `sample_size`
- `decision_ready_flag`
- `analysis_notes`

## 6. Optional Columns for Later

아래 컬럼은 유용하지만 지금 당장 필수는 아니다.

- `adjusted_p_value`
- `multiple_testing_method`
- `bootstrap_iterations`
- `bootstrap_seed`
- `posterior_mean`
- `posterior_std`
- `cuped_adjusted_effect`
- `covariate_balance_score`
- `sample_ratio_mismatch_flag`

이 컬럼들은 아래 상황에서 추가하면 된다.

- 다중 검정을 본격적으로 관리할 때
- bootstrap을 표준 분석 루틴으로 채택할 때
- CUPED를 정식 적용할 때
- 품질 검사를 결과 테이블에서도 빠르게 조회하고 싶을 때

## 7. Recommended Naming Policy

- 확률 값은 `probability_*` 형식으로 통일한다.
- 구간 값은 `_lower`, `_upper`로 통일한다.
- 효과 크기는 `uplift_value`로 통일한다.
- 절대 metric 값은 `baseline_value`, `variant_value`로 분리한다.
- 분석 방식은 `analysis_method` 컬럼으로 명시한다.

## 8. Interpretation Policy for Statistical Columns

### 1. `p_value`는 있어도 주연이 아니다

지금 프로젝트는 Bayesian 중심 의사결정을 지향하므로, `p_value`는 참고 지표로 두되 최종 판단은 `probability_b_beats_a`, effect size, guardrail과 함께 본다.

### 2. interval 컬럼은 반드시 범위 해석에 쓴다

`confidence_interval_lower`, `confidence_interval_upper`가 있다면, 단지 저장만 하지 말고 대시보드와 문서에서 함께 노출해야 한다.

### 3. `sample_size`는 거의 모든 결과와 함께 보여야 한다

작은 표본 환경에서는 sample size가 빠진 uplift나 확률은 오해를 만들기 쉽다.

## 9. Practical Recommendation for Now

지금 단계에서 가장 현실적인 권장안은 아래와 같다.

### 지금 바로 설계에 반영

- `metric_value`
- `numerator_value`
- `denominator_value`
- `sample_size`
- `standard_error`
- `confidence_interval_lower`
- `confidence_interval_upper`
- `uplift_value`
- `baseline_value`
- `variant_value`
- `probability_b_beats_a`
- `probability_guardrail_regression`
- `analysis_method`
- `minimum_effect_threshold`

### 나중에 추가

- `p_value`
- `power_target`
- `bootstrap_iterations`
- `posterior_mean`
- `cuped_adjusted_effect`

## 10. Link to Our Schema

이 문서는 특히 아래 두 테이블과 연결된다.

- [`DATA_SCHEMA.md`](DATA_SCHEMA.md)의 `metric_snapshot`
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md)의 `experiment_result`

필요하다면 다음 단계에서 이 컬럼들을 실제 DDL 수준으로 구체화할 수 있다.
