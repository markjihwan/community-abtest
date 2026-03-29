# Ratio Metrics

## 1. Purpose

이 문서는 `CTR`, `ARPU`, `active user당 conversion`, `participant당 제출 수`처럼 `분자/분모로 정의되는 지표`를 실험에서 어떻게 다뤄야 하는지 정리한 기초 문서다.

핵심 목적은 아래와 같다.

- ratio metric을 단순 평균처럼 다루는 실수를 줄인다.
- variance와 interval을 어떻게 근사할지 감을 잡는다.
- 언제 표준 검정이 깨지는지 이해한다.
- delta method, Fieller, bootstrap 중 어떤 접근이 현실적인지 정리한다.

## 2. What Counts as a Ratio Metric

아래와 같은 지표는 ratio metric으로 본다.

- CTR = 클릭 수 / 노출 수
- ARPU = 매출 / 사용자 수
- conversion per active user = 전환 수 / 활성 사용자 수
- submissions per participant = 제출 수 / 참여자 수

우리 프로젝트에 맞는 예시는 아래와 같다.

- 발표율 = 발표 수 / 첫 참여 인원
- 피드백율 = 피드백 수 / 활성 참여자 수
- 주차별 과제 제출률 = 제출 수 / 해당 주차 활성 인원

## 3. Core Principle

ratio metric은 가능하면 `sum(numerator) / sum(denominator)` 형태로 보고, 그 위에서 분산과 불확실성을 추정한다.

즉, 아래처럼 생각하는 것이 기본이다.

`ratio = numerator_sum / denominator_sum`

이 접근이 중요한 이유는 사용자 단위 분모가 다르거나, 노출/활성 수가 제각각인 환경에서 단순 평균 비교가 왜곡될 수 있기 때문이다.

## 4. Why Standard Tests Often Break

표준 t-test나 z-test가 항상 바로 쓰기 어려운 이유는 아래와 같다.

- ratio는 두 확률변수의 함수다.
- 분모 변동성이 크면 분산 구조가 복잡해진다.
- 사용자마다 분모 크기가 다를 수 있다.
- randomization unit과 analysis unit이 다를 수 있다.

예를 들어 `노출당 클릭`을 분석하면서 페이지뷰 단위로 보거나, `active user당 conversion`을 분석하면서 활성 여부가 treatment에 의해 변하면 해석이 흔들릴 수 있다.

## 5. Delta Method

### What It Is

delta method는 `복잡한 함수 형태의 지표`를 큰 표본에서 근사적으로 정규분포처럼 다루게 해주는 방법이다.

ratio metric에서는 특히 `sum(X) / sum(Y)` 꼴의 지표에서 매우 자주 쓰인다.

### Why It Matters

- 계산이 빠르다.
- 대규모 실험 환경에 잘 맞는다.
- bootstrap보다 운영 비용이 낮다.
- ratio metric의 approximate variance를 구하는 실무 표준 접근 중 하나다.

### Our Default Recommendation

현재 프로젝트에서는 ratio metric의 기본 추정 방법으로 `delta method`를 우선 고려하는 것이 현실적이다.

이유:

- 현재 문서 체계가 `metric_snapshot`, `experiment_result` 중심이라 summary-statistics 기반 접근과 잘 맞는다.
- cohort 기반 운영에서도 구현 복잡도를 과하게 높이지 않는다.

## 6. Fieller and Bootstrap

### Fieller

Fieller는 ratio에 대해 더 직접적인 interval 접근을 제공할 수 있지만, 실무에서는 해석과 구현이 더 어렵다.

권장 위치:

- 특수한 ratio metric에서 interval 안정성이 특히 중요할 때
- 분석팀이 충분히 이해하고 있을 때

### Bootstrap

bootstrap은 분포 가정이 약한 환경에서 유용한 대안이다.

권장 위치:

- 작은 표본
- 비정규 분포
- delta method 근사가 불안한 경우
- 복잡한 파생 metric

현재 프로젝트 권장안:

- 기본은 delta method
- 필요 시 bootstrap으로 보강
- Fieller는 고급 옵션

## 7. Practical Rules for Our Project

### 1. Ratio metric은 문서상 분자/분모를 반드시 고정한다

예:

- 발표율 = 발표 수 / 첫 참여 인원
- 피드백율 = 피드백 수 / 활성 참여자 수

분모가 흔들리면 해석도 흔들린다.

### 2. 분모가 treatment 영향을 받을 수 있는지 먼저 본다

예를 들어 `active user당 conversion`에서 active user 정의 자체가 treatment에 의해 바뀐다면, ratio 해석이 꼬일 수 있다.

### 3. 가능하면 absolute metric도 함께 저장한다

ratio만 보면 무엇이 변했는지 놓칠 수 있다.

같이 보면 좋은 값:

- numerator_sum
- denominator_sum
- ratio_value

### 4. sample size와 interval 없이 ratio만 보여주지 않는다

ratio metric은 보기보다 불안정할 수 있으므로 아래를 함께 본다.

- sample_size
- confidence interval 또는 credible interval
- baseline_value
- variant_value

## 8. Suggested DB Support

ratio metric을 잘 다루려면 DB에서 아래 정보를 함께 남기는 것이 좋다.

### In `metric_snapshot`

- `metric_value`
- `numerator_value`
- `denominator_value`
- `sample_size`
- `standard_error`
- `confidence_interval_lower`
- `confidence_interval_upper`

### In `experiment_result`

- `baseline_value`
- `variant_value`
- `uplift_value`
- `analysis_method`
- `confidence_interval_lower`
- `confidence_interval_upper`
- `probability_b_beats_a`

### Optional Later

- `ratio_method`
- `bootstrap_iterations`
- `fieller_interval_lower`
- `fieller_interval_upper`

## 9. Recommended Resources

- [Applying the Delta Method in Metric Analytics: A Practical Guide with Novel Ideas](https://arxiv.org/pdf/1803.06336)
- [The Delta Method in A/B Testing](https://www.aleksjpages.com/blog/delta-method-in-AB-testing)
- [Applying Delta Method for A/B Tests Analysis](https://medium.com/%40ahmadnuraziz3/applying-delta-method-for-a-b-tests-analysis-8b1d13411c22)
- [DataCamp - Ratio metrics and the delta method](https://campus.datacamp.com/courses/ab-testing-in-python/practical-considerations-and-making-decisions?ex=8)

## 10. Interpretation Rules

- ratio metric은 단순 평균처럼 취급하지 않는다.
- 먼저 분자/분모 정의를 고정한다.
- 기본 해석은 delta method 중심으로 둔다.
- 작은 표본이나 복잡한 metric은 bootstrap 보강을 고려한다.
- ratio 결과는 absolute sums와 함께 본다.

## 11. Link to Our Documents

- [`STATISTICAL_FOUNDATIONS.md`](STATISTICAL_FOUNDATIONS.md): bootstrap과 interval 해석 기초
- [`STATISTICAL_COLUMNS.md`](STATISTICAL_COLUMNS.md): ratio metric에 필요한 컬럼
- [`METRIC_DICTIONARY.md`](METRIC_DICTIONARY.md): ratio metric 정의 고정
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): numerator/denominator 저장 구조
