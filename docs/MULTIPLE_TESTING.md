# Multiple Testing

## 1. Purpose

이 문서는 하나의 실험에서 `variant가 많고`, `metric이 많고`, `segment/slice가 많을 때` 생기는 false discovery 문제를 어떻게 이해하고 다룰지 정리한 기초 문서다.

핵심 목적은 아래와 같다.

- FWER와 FDR 차이를 구분한다.
- Bonferroni, Holm, Benjamini-Hochberg, Hochberg의 위치를 정리한다.
- 여러 metric과 여러 slice를 동시에 볼 때 family를 어떻게 정의할지 정한다.
- 실험이 시간에 따라 연속적으로 쌓이는 환경에서 online multiple testing이 왜 필요한지 이해한다.

## 2. Why This Matters

metric 하나만 보면 단순하지만, 실제 실험에서는 아래가 동시에 늘어난다.

- variant 수
- goal metric 수
- segment 수
- 실험 수

이때 유의해 보이는 결과 중 일부는 우연히 나온 false positive일 가능성이 커진다.

`False Discovery in A/B Testing` 논문은 실제 A/B 테스트 데이터에서 5% 유의수준 기준으로도 유의 결과 중 상당 부분이 false discovery일 수 있음을 보여준다. 특히 원문은 `5% significance`에서도 유의 결과 중 대략 `1 in 5` 정도가 field에서 효과가 없을 수 있다고 설명한다.

## 3. FWER vs FDR

### FWER

FWER는 `적어도 하나의 false positive가 나올 확률`을 통제한다.

장점:

- 더 보수적이다.
- 실수 허용이 매우 낮은 환경에 적합하다.

단점:

- 테스트 수가 많아질수록 지나치게 엄격해질 수 있다.
- power가 크게 줄 수 있다.

### FDR

FDR는 `유의하다고 나온 결과 중 false positive 비율`을 통제한다.

장점:

- 탐색적 분석과 다중 metric 환경에 더 현실적이다.
- FWER보다 power를 덜 잃는다.

단점:

- 개별 결과에 대한 보장은 더 약하다.

### Practical Recommendation

현재 프로젝트에서는 아래처럼 생각하는 것이 현실적이다.

- 핵심 의사결정용 primary metric: 더 보수적으로 본다
- exploratory metric, slice 분석: FDR 중심이 더 적합하다

## 4. Main Procedures

### Bonferroni

가장 단순한 보정이다. 각 검정 임계값을 매우 보수적으로 낮춘다.

위치:

- 이해는 쉽다
- 실제 운영에는 지나치게 보수적일 수 있다

### Holm

Holm은 Bonferroni보다 덜 보수적이면서 FWER를 통제한다.

위치:

- 보수적 의사결정에 적합
- 실무에서는 Bonferroni보다 보통 더 낫다

### Benjamini-Hochberg

BH는 FDR를 통제하는 대표 절차다.

위치:

- metric과 slice가 많은 환경에서 현실적
- 독립 또는 양의 상관 구조 가정이 자주 언급된다

### Hochberg

Hochberg는 step-up 기반의 FWER 통제 절차로, 일부 상황에서는 Holm보다 덜 보수적일 수 있다.

위치:

- FWER를 유지하면서 power를 조금 더 확보하려는 경우 고려 가능
- 적용 가정과 해석을 이해한 상태에서 써야 한다

## 5. Defining a Family of Tests

다중 검정에서 가장 중요한 질문 중 하나는 `무엇을 하나의 family로 볼 것인가`다.

GrowthBook 문서의 핵심도 여기에 있다. 모든 것을 전부 한 family로 묶으면 power가 너무 떨어지고, 반대로 family를 너무 작게 쪼개면 false positive가 늘어난다.

현재 프로젝트 권장안은 아래와 같다.

### Default Family

하나의 실험 안에서 아래 조합을 한 family 후보로 본다.

- 모든 primary / goal metric
- 모든 treatment vs control 비교
- 같은 결과 뷰에서 함께 제시되는 slice

### Guardrail and Secondary Metrics

guardrail은 해석 방식이 약간 다르다.

- guardrail은 주로 `악화 여부 감시` 목적이다.
- primary와 완전히 같은 방식으로 family에 넣을지 여부는 정책적으로 분리해둘 수 있다.

현재 프로젝트에서는 아래처럼 두는 것이 좋다.

- primary/goal metric family: multiple testing correction 적용 대상
- guardrail: 별도 감시 레이어로 유지

### Slice Policy

세그먼트 분석은 false discovery 위험이 특히 크다.

따라서 slice 결과는 기본적으로 아래처럼 다룬다.

- 기본 결과보다 약한 증거로 해석
- exploratory label 부여
- correction 없이 strong claim 금지

## 6. Multiple Metrics and Multiple Slices

metric이 많고 slice가 많아질수록 실험 하나가 사실상 수십 개 검정이 된다.

예:

- metric 4개
- variant 비교 2개
- segment 3개

그러면 이미 다수 검정이 발생한다.

실무 규칙:

- primary metric은 사전에 고정
- secondary metric은 설명용
- slice는 탐색용 우선
- 보고서에서는 adjusted와 unadjusted를 구분

## 7. Online / Sequential Multiple Testing

전통적 BH 같은 절차는 `모든 p-value가 한 번에 주어진다`는 배치 상황에 잘 맞는다.

하지만 실험 플랫폼은 보통 아래와 같다.

- 실험이 시간에 따라 하나씩 도착한다
- 각 실험 종료 시 바로 결정을 내려야 한다

이럴 때는 online multiple testing이 필요할 수 있다.

Robertson, Wason, Ramdas의 리뷰는 이런 환경에서 온라인 FDR/FWER 통제 방법론이 지난 15년간 발전해 왔다고 정리한다.

현재 프로젝트 권장안:

- 지금 단계에서는 batch형 multiple correction 이해를 우선
- 실험이 누적되고 조직 전체 포트폴리오를 관리하기 시작하면 online multiple testing을 검토

즉, 지금 바로 구현 필수는 아니지만 `장기 플랫폼 정책`에는 포함해야 한다.

## 8. Practical Rules for Our Project

### 1. Primary metric은 사전 지정한다

multiple testing 부담을 줄이는 가장 좋은 방법은 primary metric을 미리 고정하는 것이다.

### 2. Slice 분석은 기본적으로 exploratory다

세그먼트별 uplift는 흥미롭지만, strong evidence로 바로 승격하지 않는다.

### 3. 보고서에는 adjusted 여부를 명시한다

`p_value`와 `adjusted_p_value`를 구분하지 않으면 해석 오류가 생긴다.

### 4. 보정은 목적에 따라 다르게 쓴다

- 엄격한 launch decision: FWER 쪽이 더 적합할 수 있다
- 탐색적 인사이트 탐색: FDR 쪽이 더 적합하다

### 5. 모든 실험을 한꺼번에 보정하지는 않는다

family를 합리적으로 정의하지 않으면 power가 과도하게 줄어든다.

## 9. Suggested DB Support

### In `experiment_result`

- `p_value`
- `adjusted_p_value`
- `multiple_testing_method`
- `test_family_id`
- `is_primary_metric`
- `is_slice_result`

### In metadata or reporting layer

- `family_definition_note`
- `correction_scope`
- `analysis_batch_id`

현재 단계에서는 컬럼을 다 넣지 않아도 되지만, 최소한 아래는 나중을 위해 염두에 두는 것이 좋다.

- `adjusted_p_value`
- `multiple_testing_method`
- `test_family_id`

## 10. Recommended Resources

- [GrowthBook Docs - Multiple Testing Corrections](https://docs.growthbook.io/statistics/multiple-corrections)
- [False Discovery in A/B Testing](https://ron-berman.com/papers/fdr.pdf)
- [Online multiple hypothesis testing](https://www.repository.cam.ac.uk/items/d6fe2e20-c3c1-45ec-a4bb-63ef81e0a30c)
- [Statsig - Hochberg procedure](https://www.statsig.com/perspectives/hochberg-procedure-false-discoveries)

## 11. Interpretation Rules

- unadjusted significance는 최종 결론으로 바로 쓰지 않는다.
- metric과 slice가 많아질수록 false discovery 위험은 커진다.
- primary metric과 exploratory metric을 문서상 분리한다.
- 조직 수준 실험 포트폴리오가 커지면 online multiple testing을 검토한다.

## 12. Link to Our Documents

- [`TEST_DESIGN_AND_POWER.md`](TEST_DESIGN_AND_POWER.md): stopping rule과 설계 기초
- [`STATISTICAL_COLUMNS.md`](STATISTICAL_COLUMNS.md): adjusted p-value 등 통계 컬럼 후보
- [`EXPERIMENT_POLICY.md`](EXPERIMENT_POLICY.md): primary metric 사전 지정 정책
- [`DECISION_RULE.md`](DECISION_RULE.md): 최종 launch decision과 연결
