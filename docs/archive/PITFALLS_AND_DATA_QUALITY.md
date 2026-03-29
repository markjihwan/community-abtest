# Pitfalls and Data Quality

## 1. Purpose

이 문서는 실험이 `겉보기에는 그럴듯하지만 실제로는 거짓말할 수 있는 방식`을 정리한 문서다.

핵심 목적은 아래와 같다.

- peeking과 optional stopping이 왜 위험한지 이해한다.
- SRM을 `결과`가 아니라 `품질 경보`로 다룬다.
- instrumentation bug, tracking issue, metric churn, seasonality 같은 운영 리스크를 체계적으로 분류한다.
- A/A 테스트와 시뮬레이션을 품질 검증 도구로 위치시킨다.

## 2. Core Principle

실험 플랫폼에서 가장 위험한 것은 `숫자가 없는 것`이 아니라 `믿을 수 없는 숫자가 그럴듯하게 보이는 것`이다.

Kohavi의 발표도 같은 메시지를 반복한다. 좋은 결과가 나왔다고 해서 바로 믿으면 안 되고, 오히려 `너무 좋아 보이는 결과`일수록 더 의심해야 한다.

정책 문장으로 정리하면 아래와 같다.

`실험 결과 해석보다 먼저 실험 품질을 검증한다.`

## 3. Peeking and Optional Stopping

### What It Is

peeking은 실험 도중 결과를 반복해서 보다가 유의해 보이는 순간에 멈추는 행동이다.

optional stopping은 stopping rule 없이 실험을 길게 혹은 짧게 운영하며 원하는 결과가 나오는 시점에 결론을 내리는 것이다.

### Why It Is Dangerous

- false positive가 부풀려질 수 있다.
- p-value 해석 전제가 깨질 수 있다.
- 팀이 결과에 흔들리기 쉬워진다.

### Policy for Our Project

- stopping rule 없는 중간 확인은 의사결정 근거로 쓰지 않는다.
- 최소 관측 기간과 최소 샘플 수를 먼저 정한다.
- 조기 종료는 미리 정의된 조건이 있을 때만 허용한다.

## 4. Sample Ratio Mismatch (SRM)

### What It Is

SRM은 실험에서 기대한 배정 비율과 실제 관측 비율이 통계적으로 유의하게 어긋나는 현상이다.

Wikipedia와 Statsig 설명처럼, 본질적으로는 `배정 혹은 측정 과정에 문제가 있을 수 있다`는 신호다.

### Why It Matters

Microsoft ExP의 핵심 메시지는 명확하다.

- SRM은 selection bias의 증거일 수 있다.
- 빠진 사용자는 무작위로 빠진 것이 아닐 수 있다.
- 오히려 treatment에 가장 크게 반응한 사용자가 빠졌을 수 있다.

MSN 사례에서는 treatment가 사용자 engagement를 크게 높였는데, 그 결과 일부 heavy user가 bot detection에 걸려 분석에서 빠졌고, 처음에는 treatment가 나쁜 것처럼 보였다. 원인을 고친 뒤 결과는 반대로 뒤집혔다.

즉, `SRM이 있는 실험은 그대로 믿지 않는다`.

### Detection

SRM은 보통 기대 비율 대비 관측 비율을 카이제곱 검정으로 점검한다.

Statsig 글은 SRM p-value를 통해 이 불균형을 평가하는 직관을 잘 설명한다. Microsoft는 실험 결과를 보기 전에 SRM 체크를 먼저 통과시키는 것이 성숙한 실험 플랫폼의 핵심 요소라고 설명한다.

### Root Causes

Microsoft ExP 문서의 taxonomy를 기준으로 보면 원인은 대체로 아래 범주로 나뉜다.

- Assignment stage 문제
- Execution stage 문제
- Log processing 문제
- Analysis stage 문제

구체적 예:

- 잘못된 bucketing
- faulty user ID
- carryover effect
- variant별 redirect 차이
- crash rate 차이
- biased trigger 조건
- 잘못된 join 또는 data deletion

### Policy for Our Project

- SRM이 감지되면 먼저 품질 이슈로 분류한다.
- root cause를 모른 채 결과 해석을 진행하지 않는다.
- untriggered와 triggered 분석을 분리해 본다. **단, 이 분리 자체가 새로운 selection bias를 만들 수 있다.** triggered 집합이 treatment에 의해 영향을 받는다면, 분리 후 분석은 SRM보다 더 큰 편향을 낳을 수 있다. 분리 전 triggered 집합의 정의가 treatment와 독립적임을 먼저 확인한다.
- segment별로 SRM이 국소적인지 광범위한지 본다.

## 5. Instrumentation and Event Tracking Issues

### Common Failure Modes

- variant별 이벤트 누락
- 노출 로그와 배정 로그의 분리
- control에는 없는 trigger 조건
- timestamp 지연
- duplicate event
- 잘못된 join key

이런 문제는 숫자를 만들지만, 그 숫자는 신뢰할 수 없게 만든다.

### Practical Rule

- assignment 로그와 exposure 로그는 구분하되 연결 가능해야 한다.
- trigger 분석을 할 때는 counterfactual logging 여부를 먼저 확인한다.
- 대시보드 계산 전에 raw event sanity check를 수행한다.

## 6. Metric Churn, Seasonality, Environment Changes

실험이 틀리는 이유는 통계 자체보다 운영 환경 변화인 경우도 많다.

예:

- metric 정의가 중간에 바뀜
- 공휴일이나 시험 기간으로 행동 패턴이 변함
- 앱 버전, 브라우저, 서버 환경이 바뀜
- 동시에 다른 운영 변화가 들어감

Kohavi 발표에서도 before/after 비교가 시간 관련 요인 때문에 왜 위험한지 강조한다.

### Policy for Our Project

- metric 정의는 실험 중 변경하지 않는다.
- seasonality note를 남긴다.
- environment change가 있으면 실험 메타데이터에 기록한다.
- freeze window 동안 비계획 운영 변경을 막는다.

## 7. A/A Tests and Simulation

### A/A Tests

Kohavi는 실험 시스템 자체를 검증하지 않으면 안 된다고 강조한다. A/A 테스트에서는 유의 결과가 대체로 균등하게 나와야 하고, p-value 분포도 대체로 균일해야 한다.

현재 프로젝트 정책:

- 새 지표 도입 전 A/A
- 새 배정 로직 도입 전 A/A
- 새 집계 로직 도입 전 A/A

### Simulation

시뮬레이션은 아직 파이프라인 단계는 아니지만, 장기적으로는 아래 검증에 유용하다.

- stopping rule이 과도하게 false positive를 만드는지
- multiple testing 보정이 어느 정도 power를 잃는지
- ratio metric 근사가 안정적인지

## 8. Minimal Quality Gate

실험 결과를 보기 전에 최소한 아래 질문에 답해야 한다.

| 체크 항목 | 질문 |
| --- | --- |
| SRM | 기대 배정 비율과 관측 비율이 일치하는가 |
| Exposure logging | variant별 노출 로그가 정상인가 |
| Trigger condition | biased trigger가 아닌가 |
| Event completeness | 특정 variant에서 누락 이벤트가 없는가 |
| Metric stability | metric 정의와 계산식이 바뀌지 않았는가 |
| Environment | 시즌성/배포/외부 변화가 있었는가 |

## 9. Suggested DB Support

### In `data_quality_check`

- `check_type`
- `check_status`
- `observed_value`
- `expected_value`
- `details`

### Recommended Check Types

- `sample_ratio_mismatch`
- `missing_events`
- `duplicate_events`
- `trigger_bias`
- `timestamp_delay`
- `metric_definition_mismatch`
- `environment_change`

### Useful Extra Metadata

- `quality_severity`
- `root_cause_status`
- `root_cause_note`
- `affected_segment`

## 10. Recommended Resources

- [Trustworthy A/B Tests: Pitfalls in Online Controlled Experiments](https://exp-platform.com/Documents/2017-05-17EmetricsControlledExperimentsPitfallsKohaviNR.pdf)
- [Seven Pitfalls to Avoid When Running Controlled Experiments on the Web](https://www.researchgate.net/publication/221653160_Seven_pitfalls_to_avoid_when_running_controlled_experiments_on_the_web)
- [Diagnosing Sample Ratio Mismatch in A/B Testing](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- [Sample ratio mismatch](https://en.wikipedia.org/wiki/Sample_ratio_mismatch)
- [SRM Checker](https://www.lukasvermeer.nl/srm/microsite/)
- [A quick guide to sample ratio mismatch](https://www.statsig.com/blog/sample-ratio-mismatch)

## 11. Interpretation Rules

- 품질 경고가 있으면 uplift보다 먼저 품질을 본다.
- SRM은 작은 경고가 아니라 실험 신뢰성 경보다.
- 좋은 결과일수록 더 의심한다.
- 실험 플랫폼은 분석 도구이기 전에 품질 검증 시스템이어야 한다.

## 12. Link to Our Documents

- [`TEST_DESIGN_AND_POWER.md`](TEST_DESIGN_AND_POWER.md): stopping rule과 A/A 테스트
- [`EXPERIMENT_POLICY.md`](EXPERIMENT_POLICY.md): freeze rule과 승인 정책
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): data_quality_check 구조
- [`DECISION_RULE.md`](DECISION_RULE.md): 품질 경고가 있을 때 hold/need_more_data로 연결
