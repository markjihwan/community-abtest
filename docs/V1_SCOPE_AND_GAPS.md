# V1 Scope and Gaps

## 1. Purpose

이 문서는 외부 experimentation platform 레퍼런스 목록을 기준으로, 현재 `abtest` 문서 체계에서 `무엇이 빠져 있는지`, `무엇은 아직 과한지`, `v1에서 어디까지 할지`를 정리한 문서다.

## 2. Current Shape

지금까지 문서 구조를 보면 `abtest`는 아래 영역을 이미 상당히 잘 다루고 있다.

- 실험 철학과 cohort/quasi-experiment 해석
- 통계 기초와 test design
- ratio metrics, multiple testing, sequential, variance reduction
- novelty/network effects, peeking, SRM, 품질 리스크
- KPI, metric dictionary, decision rule
- 데이터 스키마와 통계 컬럼
- 정책 베이스와 실험 설계 정책

즉, 현재 강점은 `통계/정책/실험 해석` 레이어다.

## 3. What Is Still Missing

외부 레퍼런스 리스트와 비교했을 때, 아직 비어 있거나 얕은 영역은 아래와 같다.

### 1. Result Usage Policy

실험 결과를 언제, 누구에게, 어떤 형식으로 공유하고 어떻게 의사결정에 반영할지에 대한 상위 정책이 아직 없다.

현재 필요성:

- `ship/hold/rollback` 이후 후속 절차 정의
- 실험 리뷰 cadence
- 실험 보고서 템플릿

### 2. Data Policy

무엇을 수집하고, 얼마나 보관하고, 누가 접근하는지에 대한 정책 문서가 아직 없다.

현재 필요성:

- 개인정보 최소 수집 원칙
- raw event 보관 기간
- 분석 접근 권한

### 3. Participant Policy

누가 실험 대상이 되는지, 고지/동의 방식은 무엇인지, 참여자 보호 원칙이 아직 문서화되지 않았다.

현재 필요성:

- cohort 실험 대상 정의
- 민감한 실험의 제외 기준
- 실험 공정성 원칙

### 4. Trust and Review Process

대기업 사례에서 중요한 `experiment review`, `analysis review`, `quality gate review` 프로세스가 아직 체크리스트 수준을 넘지 않았다.

### 5. Dashboard / Reporting Layer

지금은 KPI와 스키마는 있지만, 결과를 실제로 어떻게 보여줄지에 대한 reporting structure 문서가 없다.

## 4. What Is Probably Too Much for V1

아래는 중요하지만, 지금 당장 `v1 플랫폼 범위`로 넣기에는 과할 가능성이 높다.

### 1. Multi-Arm Bandits

흥미롭지만 현재 프로젝트의 cohort 기반 운영 구조와는 우선순위가 맞지 않을 수 있다.

### 2. Full Online Multiple Testing

실험 포트폴리오가 매우 커졌을 때 의미가 커진다. 지금은 family-level correction 원칙 정도면 충분하다.

### 3. Full ML-Based Variance Reduction

개념적으로 중요하지만, 현재는 CUPED / 단순 regression adjustment 정도가 현실적이다.

### 4. Switchback as Default Design

문서상 위치는 잘 잡았지만, 지금 기본 설계가 되면 복잡도만 크게 늘 수 있다.

### 5. Causal ML / Counterfactual Stack

장기적으로는 가치가 있지만, v1의 핵심은 trustworthy experimentation이지 causal modeling 플랫폼이 아니다.

## 5. Recommended V1 Scope

현재 문서 흐름을 기준으로, `abtest v1`은 아래 범위로 자르는 것이 좋아 보인다.

### Must Have

- cohort-based experiment registry
- experiment policy and approval metadata
- North Star / guardrail / supporting KPI 체계
- metric dictionary
- event log + weekly activity + operational load
- metric snapshot + experiment result
- data quality checks
- decision log
- basic Bayesian interpretation
- basic sequential option
- ratio metric support

### Should Have

- CUPED-ready pre-experiment covariate fields
- A/A test support metadata
- SRM checks
- reporting template
- result usage policy

### Nice to Have Later

- full online multiple testing
- switchback metadata
- ML variance reduction
- bandit support
- causal inference modules

## 6. Recommended Document Priorities

지금 이후 문서 우선순위는 아래가 자연스럽다.

1. `RESULT_USAGE_POLICY.md`
2. `DATA_POLICY.md`
3. `PARTICIPANT_POLICY.md`
4. `REPORTING_TEMPLATE.md` 또는 `DASHBOARD_SPEC.md`

## 7. One-Line Summary

현재 `abtest`는 이미 `실험 해석과 정책` 문서 기반은 강하다. 이제 v1에서는 범위를 넓히기보다 `결과 활용`, `데이터 정책`, `참여자 정책`, `리포팅 구조`를 채워서 플랫폼의 운영 완성도를 높이는 편이 맞다.
