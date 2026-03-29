# Variance Reduction

## 1. Purpose

이 문서는 더 많은 사용자를 모으지 않고도 실험의 power를 높일 수 있는 분산 감소 기법을 정리한다.

핵심 목적은 아래와 같다.

- stratification과 post-stratification을 언제 쓰는지 이해한다.
- regression adjustment와 covariate adjustment의 역할을 정리한다.
- CUPED / CUPAC이 언제 효과가 있고 언제 무리인지 구분한다.
- pre-experiment, in-experiment covariate를 어떻게 조합할지 생각한다.
- ML 기반 variance reduction을 과장 없이 위치시킨다.

## 2. Core Principle

Microsoft ExP의 핵심 메시지는 아주 분명하다.

`Variance reduction은 데이터 자체의 분산을 줄이는 것이 아니라, treatment effect estimator의 standard error를 낮추는 것이다.`

즉, 분산 감소는:

- 신뢰성 자체를 마법처럼 높여주는 것이 아니고
- bias를 없애는 것도 아니며
- 잘못된 실험을 좋은 실험으로 바꿔주지도 않는다

대신 잘 설계된 실험에서 `더 좁은 confidence interval`, `더 높은 power`, `더 작은 MDE`를 가능하게 한다.

## 3. Stratification and Post-Stratification

### Stratification

실험 전 사용자나 실험 단위를 중요한 특성별로 층화해 배정하는 방식이다.

유용한 상황:

- 특정 속성이 outcome에 강하게 연관될 때
- treatment/control baseline balance를 더 잘 맞추고 싶을 때

### Post-Stratification

실험 후 분석 단계에서 strata 정보를 반영해 추정치를 개선하는 방식이다.

유용한 상황:

- 실험 전 완벽한 층화가 어려웠을 때
- 인구구성 차이를 분석 단계에서 보정하고 싶을 때

현재 프로젝트 적용:

- cohort 기반 환경에서는 완전한 stratified randomization이 어렵더라도
- `기존 참여 이력`, `신규/기존 참여자`, `기수 유형` 같은 층 정보를 분석 단계에서 활용할 수 있다

## 4. Regression Adjustment

regression adjustment는 outcome과 상관 있는 covariate를 사용해 treatment effect 추정의 precision을 높이는 접근이다.

Microsoft 문서가 설명하듯, randomization은 unbiasedness를 보장하지만 precision은 별개 문제다. regression adjustment는 이 precision을 높이는 쪽에 기여한다.

실무적으로는 아래처럼 이해하면 된다.

- difference-in-means: 가장 단순한 baseline
- regression-adjusted estimator: 같은 unbiased 목표를 더 낮은 standard error로 추정

현재 프로젝트에선 regression adjustment를 `고급 옵션`이 아니라, 잘 정의된 covariate가 있을 때 현실적인 확장 옵션으로 본다.

## 5. CUPED

### What It Is

CUPED는 `Controlled experiment Using Pre-Experiment Data`다.

Statsig와 Spotify 모두 같은 핵심을 강조한다.

- pre-exposure data를 사용한다
- outcome과 상관 높은 covariate를 쓴다
- variance를 줄여 velocity를 높인다

### Why It Works

Statsig 설명의 핵심은, pre-period value와 post-period outcome의 상관이 높을수록 variance reduction 효과가 커진다는 점이다.

즉, 중요한 것은:

- covariate가 pre-treatment여야 하고
- outcome과 상관이 높아야 하며
- assignment와 독립이어야 한다

### Best Use Cases

Statsig는 CUPED가 특히 `existing user experiments`에서 강하다고 설명한다. 기존 사용자에겐 historical data가 있기 때문이다.

현재 프로젝트에서도 아래 상황이 잘 맞는다.

- 이전 기수 출석률
- 과거 활동 점수
- 신청 전 engagement proxy
- 첫 주 이전의 안정적 사전 특성

### Limitations

- 신규 사용자만 있는 실험에는 적용이 어렵다
- historical data가 없으면 강한 효과를 기대하기 어렵다
- treatment 영향을 받은 변수를 covariate로 쓰면 안 된다

## 6. CUPAC and Combining Covariates

CUPED의 아이디어를 넓히면, 하나의 pre-period metric뿐 아니라 더 풍부한 covariate 묶음을 활용하는 방향으로 갈 수 있다.

즉 아래처럼 생각할 수 있다.

- pre-experiment metric 1개 사용
- 여러 pre-experiment feature 사용
- pre + 일부 안정적인 in-experiment baseline feature 조합

다만 현재 프로젝트에서는 원칙이 필요하다.

### Policy

- 기본은 pre-experiment covariate 우선
- treatment 이후에 영향을 받을 수 있는 변수는 매우 조심해서 사용
- 조정 변수는 해석 가능성을 해치지 않는 범위에서 늘린다

## 7. ML-Based Variance Reduction

NeurIPS 2021 논문은 ML을 사용해 covariate에서 outcome을 더 잘 예측하면, 추가적인 variance reduction을 얻을 수 있다고 설명한다.

핵심 포인트:

- nonlinear 관계가 있으면 ML이 선형 조정보다 더 나을 수 있다
- 하지만 중요한 것은 `formal guarantee`가 있는 regression-adjusted estimator여야 한다
- 논문은 cross-fitting과 regression adjustment를 결합해 consistency와 CI coverage를 보장하는 방향을 제시한다

### Practical Meaning

ML 기반 variance reduction은 `아무 모델이나 넣어서 예측 잘하면 된다`는 뜻이 아니다.

우리 프로젝트에서의 현실적 해석:

- 초기 단계: CUPED나 간단한 regression adjustment면 충분
- 데이터가 충분히 쌓인 뒤: ML proxy 기반 variance reduction 검토
- 항상 non-inferiority safeguard가 있어야 한다

Microsoft와 NeurIPS 쪽 흐름을 같이 보면, 고급 방법일수록 `precision 개선`보다 `추정량의 보장`이 더 중요하다.

## 8. Practical Rules for Our Project

### 1. 분산 감소는 기본 설계를 대신하지 않는다

randomization 문제, SRM, instrumentation bug가 있는 실험은 CUPED를 써도 구제되지 않는다.

### 2. pre-experiment covariate를 우선 사용한다

가장 안전한 choice다.

### 3. 신규 사용자 실험에서는 기대치를 낮춘다

historical data가 적으면 variance reduction 효과가 제한적이다.

### 4. covariate는 outcome 상관성과 독립성을 같이 본다

상관만 높고 treatment에 영향받는 변수는 위험하다.

### 5. ML 기반 방법은 마지막 단계다

설명 가능성과 운영 안정성을 먼저 확보한 뒤 도입한다.

## 9. Suggested DB Support

### In participation or user-level pre-period data

- `prior_attendance_rate`
- `preprogram_activity_score`
- `application_engagement_score`
- `historical_completion_flag`
- `preperiod_metric_value`

### In experiment metadata

- `variance_reduction_method`
- `covariate_set_name`
- `uses_pre_experiment_data`
- `covariate_eligibility_rule`

### In experiment_result or analysis metadata

- `variance_reduction_method`
- `covariate_correlation`
- `vr_applied_flag`
- `vr_notes`

## 10. Recommended Resources

- [Microsoft ExP - Deep Dive into Variance Reduction](https://www.microsoft.com/en-us/research/articles/deep-dive-into-variance-reduction/)
- [Statsig - CUPED Explained](https://www.statsig.com/blog/cuped)
- [Understanding CUPED](https://matteocourthoud.github.io/post/cuped/)
- [Spotify Confidence - Variance Reduction (CUPED)](https://confidence.spotify.com/docs/experiments/stats/variance-reduction)
- [Online Experiments Tricks — Variance Reduction](https://www.topbots.com/online-experiments-variance-reduction/)
- [Machine Learning for Variance Reduction in Online Experiments](https://proceedings.neurips.cc/paper/2021/file/488b084119a1c7a4950f00706ec7ea16-Paper.pdf)

## 11. Interpretation Rules

- variance reduction은 bias fix가 아니다.
- 좋은 covariate는 pre-treatment이고 outcome과 상관이 높다.
- CUPED는 existing-user 환경에서 특히 강하다.
- ML 기반 방법은 정교하지만, 보장 있는 추정량으로 써야 한다.

## 12. Link to Our Documents

- [`TEST_DESIGN_AND_POWER.md`](TEST_DESIGN_AND_POWER.md): power와 MDE
- [`STATISTICAL_COLUMNS.md`](STATISTICAL_COLUMNS.md): variance reduction 관련 메타데이터
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): pre-experiment covariate 저장 구조
- [`PITFALLS_AND_DATA_QUALITY.md`](PITFALLS_AND_DATA_QUALITY.md): 잘못된 실험을 분산 감소로 덮지 않기
