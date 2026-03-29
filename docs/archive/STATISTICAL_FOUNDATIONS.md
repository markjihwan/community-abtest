# Statistical Foundations

## 1. Purpose

이 문서는 `abtest` 프로젝트에서 실험 결과를 해석하고 DB 스키마를 설계하기 전에 알아야 할 통계 기초를 정리한 문서다.

목표는 고급 통계 이론을 깊게 설명하는 것이 아니라, 아래 질문에 답할 수 있도록 기반을 만드는 것이다.

- 왜 randomization이 중요한가
- p-value와 confidence interval은 무엇을 말해주는가
- 작은 샘플 환경에서 어떤 해석 실수를 조심해야 하는가
- bootstrap은 언제 유용한가

## 2. Minimum Topics

아래 항목은 advanced topic으로 가기 전에 반드시 이해해야 한다.

| 주제 | 왜 중요한가 | 우리 프로젝트에서의 의미 |
| --- | --- | --- |
| Randomization, independence, sampling | 실험 결과의 신뢰성 기초 | cohort 비교가 왜 진짜 A/B와 다른지 이해 |
| Null / alternative hypotheses | 통계적 판단의 출발점 | 변화가 우연인지 아닌지 해석 |
| Type I / II errors | 잘못된 결론의 비용 이해 | 잘못 채택하거나 좋은 아이디어를 놓치는 위험 관리 |
| p-values, significance level, power | 전통적 검정의 핵심 개념 | frequentist 결과를 읽을 수 있게 함 |
| Confidence intervals | 효과 크기와 불확실성 해석 | uplift를 단일 숫자가 아니라 범위로 보기 |
| z-test, t-test, chi-square test | 기본 비교 도구 | 비율, 평균, 범주형 차이 판단 |
| Bootstrap intuition | 분포 가정이 약할 때 유연한 추정 | 작은 표본, 비정규 분포 환경 보완 |

## 3. Why This Matters for ABTest

우리 프로젝트는 완전한 randomized A/B보다 `cohort-based quasi-experiment` 비중이 크다. 그래서 통계 기초를 아는 목적도 단순히 검정 공식을 쓰기 위해서가 아니다.

중요한 이유는 아래와 같다.

- 랜덤 배정이 없을 때 어떤 해석 한계가 생기는지 이해해야 한다.
- p-value 하나만 보고 의사결정하면 안 되는 이유를 이해해야 한다.
- 작은 샘플에서 confidence interval과 Bayesian 확률 해석을 함께 보는 이유를 이해해야 한다.
- bootstrap과 CUPED 같은 보조 기법이 언제 필요한지 판단할 수 있어야 한다.

## 4. Recommended Reading Path

### Step 1. 입문 과정

[`Udacity - A/B Testing`](https://www.udacity.com/course/ab-testing--ud257)는 실험 개요, metric 선택, 실험 설계, 결과 분석을 한 번에 훑기 좋다.

확인 포인트:

- A/B 테스트가 무엇인지
- 어떤 metric을 선택해야 하는지
- 실험 설계와 결과 분석이 어떻게 이어지는지

### Step 2. Statistical Significance

[`Analytics Toolkit - Statistical Significance in A/B Testing`](https://blog.analytics-toolkit.com/2017/statistical-significance-ab-testing-complete-guide/)는 통계적 유의성의 의미와 흔한 오해를 실무 관점에서 잘 정리한다.

중점 포인트:

- random variability 이해
- statistical significance의 실제 의미
- 흔한 오해와 misuse
- significance level과 sample size 선택

[`Data36 - Statistical Significance in A/B Testing`](https://data36.com/statistical-significance-in-ab-testing/)는 계산 감각을 조금 더 쉽게 잡는 입문용으로 좋다.

중점 포인트:

- p-value 직관
- 유의성 계산 흐름
- 실무에서 왜 충분한 표본이 필요한지

### Step 3. Confidence Intervals

[`CXL - Confidence Intervals: A Guide for A/B Testing`](https://cxl.com/blog/confidence-intervals/)는 단일 p-value보다 `효과 크기와 불확실성 범위`를 같이 봐야 한다는 점을 이해하는 데 좋다.

중점 포인트:

- interval이 의미하는 것
- interval과 decision making의 관계
- uplift를 범위로 해석하는 습관

### Step 4. Bootstrapping

[`Getir - A/B Testing with Bootstrapping`](https://medium.com/getir/bootstrapping-for-a-b-testing-893f01fa6700)는 실무 맥락에서 bootstrap 직관을 잡는 데 도움이 된다.

[`Statistics By Jim - Introduction to Bootstrapping in Statistics`](https://statisticsbyjim.com/hypothesis-testing/bootstrapping/)은 bootstrap의 개념과 예제를 차분하게 설명한다.

중점 포인트:

- bootstrap sample이 무엇인지
- 분포 가정이 강하지 않을 때 왜 유용한지
- 작은 표본과 복잡한 metric에서 어떻게 보조적으로 쓸 수 있는지

## 5. Interpretation Rules for Our Project

이 자료들을 읽을 때 `abtest` 프로젝트에 맞춰 특히 아래 원칙을 기억하면 좋다.

### 1. p-value는 최종 답이 아니다

p-value는 우연 가능성에 대한 하나의 신호일 뿐이다. 실제 운영에서는 아래를 함께 봐야 한다.

- 효과 크기
- confidence interval
- sample size
- guardrail 변화

### 2. Confidence interval은 매우 중요하다

우리 프로젝트는 표본이 크지 않을 가능성이 높기 때문에, `좋아 보인다`보다 `얼마나 불확실한가`를 같이 봐야 한다.

### 3. Bootstrap은 작은 샘플 환경에서 유용할 수 있다

완주율, 결과물 제출률, 주차별 유지율처럼 분포 가정이 단순하지 않은 지표에서는 bootstrap이 보조 추정 도구로 쓸 만하다.

### 4. Randomization이 없으면 causal claim을 약하게 해야 한다

cohort 비교는 quasi-experiment이므로, 통계 검정을 하더라도 결과는 `운영 의사결정용 근사치`로 해석하는 것이 안전하다.

## 6. Reference List

- Udacity: https://www.udacity.com/course/ab-testing--ud257
- Analytics Toolkit: https://blog.analytics-toolkit.com/2017/statistical-significance-ab-testing-complete-guide/
- Data36: https://data36.com/statistical-significance-in-ab-testing/
- CXL: https://cxl.com/blog/confidence-intervals/
- Getir: https://medium.com/getir/bootstrapping-for-a-b-testing-893f01fa6700
- Statistics By Jim: https://statisticsbyjim.com/hypothesis-testing/bootstrapping/

## 7. Link to Our Documents

이 통계 기초 문서는 아래 문서들과 연결된다.

- [`EXPERIMENT_FRAMEWORK.md`](EXPERIMENT_FRAMEWORK.md): randomized A/B와 cohort comparison의 차이
- [`KPI_TABLE.md`](KPI_TABLE.md): 어떤 지표를 primary, guardrail, leading으로 볼지
- [`DECISION_RULE.md`](DECISION_RULE.md): Bayesian, effect size, guardrail 기반 판단 규칙
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): metric snapshot, experiment result, data quality check 테이블 설계

## 8. Practical Summary

이 단계의 핵심은 통계를 많이 아는 것이 아니라, 실험 결과를 과신하지 않는 해석 습관을 만드는 것이다.

- randomization이 없는 비교는 더 조심해서 읽는다.
- p-value보다 effect size와 interval을 같이 본다.
- bootstrap은 보조 도구로 이해한다.
- 실험 결과는 항상 KPI, guardrail, 표본 크기와 함께 해석한다.
