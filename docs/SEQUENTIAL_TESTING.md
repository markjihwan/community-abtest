# Sequential Testing

## 1. Purpose

이 문서는 실험 도중 결과를 여러 번 확인하더라도 Type I error를 통제할 수 있게 해주는 sequential testing의 핵심 개념을 정리한다.

핵심 목적은 아래와 같다.

- group sequential tests와 alpha-spending의 역할을 이해한다.
- always-valid / anytime-valid p-value가 무엇을 해결하는지 정리한다.
- SPRT의 위치를 이해한다.
- fixed-horizon 대비 장단점을 분리한다.
- 실험 플랫폼에서 sequential을 어떻게 실용적으로 구현하는지 정리한다.

## 2. Core Principle

Sequential testing의 핵심은 단순하다.

`중간 확인 자체가 문제는 아니고, 중간 확인을 fixed-horizon 규칙으로 해석하는 것이 문제다.`

GrowthBook 문서도 같은 메시지를 준다. frequentist fixed-sample test는 미리 정한 표본 수나 시점에서 한 번만 결론을 내릴 때 nominal false positive rate를 보장한다. 중간중간 보고 멈추면 false positive rate가 부풀려진다.

Sequential testing은 이 문제를 해결하면서 `look early and often`을 가능하게 해준다.

## 3. Why Not Just Use Fixed-Horizon?

고전적 fixed-horizon test는 단순하고 익숙하다.

장점:

- 해석이 쉽다
- 구현이 단순하다
- 많은 팀이 이미 익숙하다

단점:

- 중간 확인에 취약하다
- 조기 중단/조기 채택이 어렵다
- 안전한 velocity를 낮출 수 있다

Wish 사례는 이 점을 아주 직관적으로 보여준다. 고정 표본 t-test를 기반으로 peeking하면 false positive rate가 크게 올라간다. 해당 글의 시뮬레이션에서는 A/A test에서 false positive rate가 대략 `4.7%`에서 `21%` 수준으로 뛰었다.

**주의: 이 수치는 Wish의 특정 시뮬레이션 조건(peeking 횟수, 표본 규모, 실험 기간 등)에서 나온 값이다.** 실제 false positive 상승폭은 peeking 횟수, 확인 시점, 표본 크기에 따라 크게 달라진다. 이 수치를 범용 기준으로 해석하지 않는다.

## 4. Group Sequential Tests and Alpha-Spending

### Group Sequential Tests

GST는 데이터를 `배치` 또는 `interim analysis` 단위로 보면서도 전체 Type I error를 통제하는 고전적 접근이다.

핵심 아이디어:

- 중간 분석 시점을 미리 정하거나 규칙화한다
- 각 중간 분석에서 사용할 경계(boundary)를 조정한다
- 전체 alpha budget을 시간에 따라 나눠 쓴다

### Alpha-Spending

alpha-spending은 전체 유의수준을 한 번에 다 쓰지 않고, 분석이 진행됨에 따라 조금씩 소비하는 방식이다.

이 방식의 장점:

- 조기 종료를 허용한다
- 전체 FWER를 통제한다

현재 프로젝트 해석:

- 실험을 매주 볼 필요가 있다면 GST나 유사 sequential framework가 자연스럽다
- 하지만 중간 분석 시점과 stopping rule이 사전에 정해져 있어야 한다

## 5. Always-Valid / Anytime-Valid p-values

### What They Are

always-valid p-value는 실험을 언제 멈추고 보더라도 Type I error control을 유지하도록 설계된 p-value다.

Wish 문서의 핵심 메시지도 여기에 있다.

- 사람들은 실제로 peek한다
- 실험 플랫폼은 그 현실을 무시하지 말고, statistical procedure를 바꿔야 한다

### Why They Matter

- 실험자가 중간중간 결과를 보는 현실과 잘 맞는다
- 고정 horizon discipline을 강제하지 않아도 된다
- 플랫폼 수준 자동화에 적합하다

### Tradeoff

GrowthBook도 분명히 말하듯, sequential methods는 fixed-horizon보다 보통 interval이 더 넓다. 즉:

- false positive control은 유지할 수 있다
- 대신 같은 시점에서 precision은 다소 손해를 볼 수 있다

## 6. Sequential Probability Ratio Test (SPRT)

SPRT는 관측이 들어올 때마다 증거를 누적해, 두 가설 중 어느 쪽이 더 타당한지 비교하며 조기에 멈출 수 있게 하는 고전적 sequential 방법이다.

실무적 위치:

- 순차 의사결정의 원형 같은 방법
- 강력하지만 구현/가정이 다소 까다로울 수 있다
- 현대 실험 플랫폼에선 GST나 confidence sequence 계열이 더 자주 보인다

현재 프로젝트에서는 SPRT를 `개념적으로 알아둘 고전적 프레임`으로 두고, 기본 운영 방법으로는 GST / anytime-valid 계열을 더 우선한다.

## 7. Practical Implementation in Platforms

### GrowthBook

GrowthBook은 frequentist engine에서 sequential testing을 제공하고, implementation으로 `asymptotic confidence sequences` 계열을 사용한다. 문서상 핵심은 다음과 같다.

- peeking 문제를 해결한다
- confidence interval 대신 confidence sequence를 사용한다
- tuning parameter `N*`를 실험자가 보통 의사결정을 내리는 sample size 근처로 설정한다

이건 플랫폼 구현 관점에서 중요하다.

- sequential on/off가 실험 설정으로 존재해야 하고
- tuning parameter를 메타데이터로 저장해야 하며
- 일반 CI와 sequential CI를 구분해 보여줘야 한다

### Wish

Wish는 always-valid p-value를 통해 experimenter가 adaptively conclude해도 false positive rate를 통제하려 했다.

실무적 메시지:

- 사람은 peek한다
- 플랫폼은 사용자를 훈련시키는 것만으로는 부족하다
- 통계 엔진이 인간 행동을 수용해야 한다

### Spotify

Spotify는 longitudinal data에서 `peeking problem 2.0`을 지적한다.

핵심은 이렇다.

- 일반 sequential test는 보통 한 unit당 한 번 측정되는 상황을 전제로 한다
- 하지만 longitudinal metric에서는 같은 unit이 여러 시점에 반복 측정된다
- 이 경우 intermittent analyses 사이의 covariance structure가 더 복잡해진다

그래서 Spotify는 longitudinal context에서 GST를 사용하되, estimand, estimator, sufficient statistics, within-unit covariance를 명확히 다뤄야 한다고 설명한다.

이건 우리 프로젝트에 특히 중요하다.

- cohort-based metric
- weekly retention
- open-ended longitudinal behavior

이런 metric을 sequential로 보려면 단순 cross-sectional thinking만으로는 부족하다.

## 8. Tradeoffs vs Fixed-Horizon Tests

### Sequential 장점

- 조기 중단 가능
- 조기 채택 가능
- 실험 velocity 향상 가능
- peeking 현실에 더 잘 맞음

### Sequential 단점

- 설정이 더 복잡함
- interval이 더 넓을 수 있음
- platform metadata와 구현 요구사항이 많아짐
- longitudinal data에서는 잘못 쓰면 false positive inflation이 다시 생길 수 있음

## 9. Practical Rules for Our Project

### 1. Fixed-horizon을 기본, sequential을 명시적 옵션으로 둔다

모든 실험에 무조건 sequential을 켜기보다, 운영상 조기 판단 필요성이 있는 실험에 우선 적용한다.

### 2. Sequential 사용 시 사전 메타데이터가 필요하다

- interim check cadence
- minimum observation window
- stopping rule
- tuning parameter 또는 boundary rule

### 3. Longitudinal metric에는 추가 주의가 필요하다

weekly retention, repeated attendance처럼 한 unit이 여러 번 관측되는 경우에는 단순 sequential 해석을 과신하지 않는다.

### 4. Sequential은 품질 검증을 대체하지 않는다

SRM, instrumentation bug, metric churn이 있으면 sequential testing을 써도 결과는 신뢰할 수 없다.

## 10. Suggested DB Support

### In experiment metadata

- `sequential_enabled`
- `sequential_method`
- `sequential_tuning_parameter`
- `interim_check_cadence`
- `minimum_observation_window`
- `stopping_rule_note`

### In experiment_result

- `analysis_method`
- `sequential_boundary_status`
- `decision_ready_flag`
- `analysis_run_at`

### Optional Later

- `alpha_spending_rule`
- `always_valid_p_value`
- `confidence_sequence_lower`
- `confidence_sequence_upper`

## 11. Recommended Resources

- [GrowthBook - Sequential Testing](https://docs.growthbook.io/statistics/sequential)
- [Wish tackles peeking with always-valid p-values](https://towardsdatascience.com/wish-tackles-peeking-with-always-valid-p-values-8a0782ac9654)
- [Calculating Always-Valid p-values in R](https://rviews.rstudio.com/2019/08/22/calculating-always-valid-p-values-in-r/)
- [Sequential Testing at Booking.com](https://blog.booking.com/sequential-testing-at-booking-com-650954a569c7)
- [Sequential Testing at Spotify, longitudinal data Part 1](https://engineering.atspotify.com/2023/07/bringing-sequential-testing-to-experiments-with-longitudinal-data-part-1-the-peeking-problem-2-0)
- [Sequential Testing at Spotify, longitudinal data Part 2](https://engineering.atspotify.com/2023/07/bringing-sequential-testing-to-experiments-with-longitudinal-data-part-2-sequential-testing/)
- [Sequential Testing Keeps the World Streaming - Netflix Part 2](https://netflixtechblog.com/sequential-testing-keeps-the-world-streaming-netflix-part-2-counting-processes-da6805341642)

## 12. Interpretation Rules

- peeking은 금지하는 것만으로 해결되지 않는다.
- sequential testing은 `언제 봐도 되는 규칙`을 제공하는 쪽에 가깝다.
- fixed-horizon보다 보통 precision tradeoff가 있다.
- longitudinal metric을 sequential로 볼 때는 within-unit dependence를 명시적으로 고려해야 한다.

## 13. Link to Our Documents

- [`TEST_DESIGN_AND_POWER.md`](TEST_DESIGN_AND_POWER.md): stopping rule과 peeking 기본
- [`PITFALLS_AND_DATA_QUALITY.md`](PITFALLS_AND_DATA_QUALITY.md): peeking과 품질 리스크
- [`STATISTICAL_COLUMNS.md`](STATISTICAL_COLUMNS.md): sequential metadata 컬럼
- [`DECISION_RULE.md`](DECISION_RULE.md): 조기 종료와 ship/hold 판단
