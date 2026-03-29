# Novelty and Network Effects

## 1. Purpose

이 문서는 `SUTVA가 깨지는 상황`을 다룬다. 즉, treatment effect가 시간에 따라 변하거나, 한 사용자의 처치가 다른 사용자에게 영향을 주는 경우를 정리한다.

핵심 목적은 아래와 같다.

- novelty effect와 primacy effect를 구분한다.
- short-term metric과 long-term impact를 혼동하지 않는다.
- user 간 interference가 있을 때 왜 일반 A/B가 깨지는지 이해한다.
- cluster randomization과 switchback을 언제 고려해야 하는지 정리한다.

## 2. Core Principle

이 문서의 핵심은 두 문장으로 요약할 수 있다.

- novelty/primacy는 `없애야 할 통계적 오류`가 아니라 `시간에 따라 달라지는 treatment effect`다.
- network effect가 강하면 `individual-level randomized A/B`의 해석 전제가 깨질 수 있다.

즉, 문제는 분석 공식을 바꾸는 것보다 먼저 `실험 단위와 시간 축을 올바르게 설계하는 것`이다.

## 3. Novelty and Primacy

### Novelty Effect

Statsig는 novelty effect를 `새로움 때문에 단기적으로 반응이 본래 가치보다 일시적으로 벗어나는 현상`으로 설명한다. 특히 고빈도 제품에서 자주 나타나며, 이를 무시하면 잘못된 제품 결정을 내릴 수 있다고 말한다.

논문 `Novelty and Primacy: A Long-Term Estimator for Online Experiments`도 novelty를 `새 기술을 쓰고 싶어 하는 욕구가 시간이 지나며 줄어드는 현상`으로 설명한다.

### Primacy Effect

같은 논문은 primacy를 `도입 후 학습과 적응으로 engagement가 점차 커지는 현상`으로 설명한다. 즉 novelty와 반대로 효과가 시간이 갈수록 커질 수 있다.

### Why They Matter

둘 다 공통적으로 `초기 cumulative uplift`만 보면 long-term impact를 잘못 추정하게 만든다.

현재 프로젝트에선 아래가 특히 중요하다.

- 첫 주 반응이 높다고 장기 가치가 높다고 단정하지 않는다.
- 반대로 초기 반응이 낮아도 habituation 이후 좋아질 수 있다.

## 4. Short-Term vs Long-Term Metrics

논문은 long-term estimator의 중요성을 강조한다. treatment effect가 시간이 지나며 안정화되지 않으면, 짧은 실험 결과를 그대로 ship decision에 쓰는 것은 위험하다.

특히 아래 구분이 중요하다.

- short-term reaction metric
- stabilized long-term behavior metric

우리 프로젝트에 적용하면:

- 단기: 1주차 출석률, 첫 발표율, 첫 피드백 반응
- 장기: 4주차 생존율, 완주율, 재참여율

### Practical Rule

- novelty가 의심되면 cumulative view만 보지 않는다.
- `daily effect` 또는 `days since exposure` view를 함께 본다.
- 효과가 안정화되기 전에는 장기 영향이라고 말하지 않는다.

## 5. Learning Effects and Habituation

논문은 novelty/primacy를 넓게 보면 `user-learning` 문제로 다룬다.

즉 사용자는:

- 처음엔 신기해서 더 많이 반응할 수 있고
- 시간이 지나며 익숙해져 반응이 줄 수 있고
- 반대로 익숙해지며 더 잘 활용하게 되어 반응이 늘 수 있다

현재 프로젝트에 맞는 해석:

- onboarding 실험은 novelty가 강하게 붙을 수 있다
- 협업 도구나 피드백 포맷 변화는 primacy가 나타날 수 있다
- 장기 판단은 short-term uplift와 분리해야 한다

## 6. When SUTVA Breaks

SUTVA가 깨진다는 것은 한 사용자의 처치 효과가 다른 사용자에게 독립적이지 않다는 뜻이다.

대표 예:

- 커뮤니티 피드백 문화 변화
- 멘토 개입 방식 변화
- marketplace 구조
- 추천/매칭/배차 시스템

DoorDash는 네트워크 효과가 강한 문제에서 단순 A/B가 비효율적이라고 설명한다. 한쪽 treatment 변화가 시스템 전체 수요/공급 균형을 바꾸기 때문에, control과 treatment를 사용자 단위로 독립 비교하기 어렵다.

## 7. Cluster Randomization

### What It Is

개별 사용자 대신 `지역`, `매장`, `조`, `기수`, `클래스` 같은 클러스터 단위로 무작위 배정하는 방식이다.

### When It Helps

- 사용자 간 상호작용이 강할 때
- treatment contamination 위험이 높을 때
- 운영 개입이 원래 그룹 단위일 때

### Tradeoff

- 해석은 더 정직해질 수 있다
- 하지만 표본 효율은 떨어질 수 있다

현재 프로젝트에서는 사실상 `cohort-based comparative experiment` 자체가 cluster 단위 접근에 가깝다.

## 8. Switchback Experiments

### What It Is

Bojinov 등은 switchback experiment를 `한 실험 단위가 시간에 따라 control과 treatment를 번갈아 노출받는 설계`로 설명한다.

DoorDash 설명도 비슷하다. 네트워크 효과가 강한 지역/마켓플레이스 문제에서 특정 지역에 대해 시간 블록별로 control과 treatment를 번갈아 적용한다.

### Why It Matters

switchback은 아래 상황에서 유용하다.

- individual randomization이 interference 때문에 깨질 때
- cluster를 고정 treatment로 두면 구조적 편향이 클 때
- 시간대별 수요/공급 변동을 고려해야 할 때

### Costs and Risks

- carryover effect 위험
- 시간 블록 설계가 잘못되면 해석 오류
- 시즌성, 시간대 패턴과 treatment가 섞일 수 있음

### Practical Rule

현재 프로젝트에서는 switchback이 당장 기본 설계는 아니다. 다만 아래 상황에서는 장기적으로 검토할 수 있다.

- 멘토 운영 방식이 특정 시간대/세션 단위로 바뀌는 경우
- 실시간 매칭이나 협업 룰이 그룹 전체에 즉시 영향을 주는 경우
- 사용자 간 직접 간섭이 강한 경우

## 9. Practical Rules for Our Project

### 1. novelty는 보정하지 말고 관찰한다

Statsig는 novelty를 통계적으로 억지 보정할 대상이 아니라 treatment effect의 일부로 본다. 우리도 같은 입장을 취한다.

### 2. 장기 판단은 long-term metric으로 한다

ship decision은 short-term spike보다 아래 지표에 더 무게를 둔다.

- 4주차 생존율
- 완주율
- 재참여율

### 3. interference가 의심되면 unit부터 다시 본다

분석 방법을 바꾸기 전에 아래를 먼저 검토한다.

- assignment unit
- contamination risk
- cluster 가능성
- time-based randomization 필요성

### 4. switchback은 고급 설계로 분류한다

기본 설계가 아니라, network effect가 명확할 때만 고려한다.

## 10. Suggested DB Support

이 주제를 지원하려면 아래 메타데이터가 있으면 좋다.

### In experiment metadata

- `assignment_unit`
- `assignment_method`
- `interference_risk_level`
- `novelty_risk_flag`
- `long_term_metric_id`
- `stabilization_window_days`

### Optional Later

- `cluster_id`
- `time_block_id`
- `switchback_period`
- `carryover_risk_note`

## 11. Recommended Resources

- [Statsig - Novelty effects](https://www.statsig.com/blog/novelty-effects)
- [Novelty and Primacy: A Long-Term Estimator for Online Experiments](https://arxiv.org/pdf/2102.12893)
- [Statsig - Switchback experiments](https://www.statsig.com/blog/switchback-experiments)
- [DoorDash - Switchback tests under network effects](https://careersatdoordash.com/blog/switchback-tests-and-randomized-experimentation-under-network-effects-at-doordash/)
- [Design and Analysis of Switchback Experiments](https://arxiv.org/abs/2009.00148)
- [Nextmv - Introducing switchback testing](https://www.nextmv.io/blog/introducing-switchback-testing-a-b-testing-for-decision-models-with-network-effects)

## 12. Interpretation Rules

- short-term uplift는 long-term value와 다를 수 있다.
- novelty/primacy는 시간에 따라 변하는 treatment effect다.
- user 간 간섭이 강하면 user-level A/B 결과를 과신하지 않는다.
- cluster 또는 switchback은 해석 정직성을 높이기 위한 설계 선택이다.

## 13. Link to Our Documents

- [`TEST_DESIGN_AND_POWER.md`](TEST_DESIGN_AND_POWER.md): 기간, 안정화, stopping rule
- [`EXPERIMENT_POLICY.md`](EXPERIMENT_POLICY.md): assignment unit과 contamination risk
- [`KPI_TABLE.md`](KPI_TABLE.md): short-term vs long-term metric 역할 분리
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): assignment_method, long-term metadata 반영
