# Experiment Decision Rule

## 1. Purpose

이 문서는 실험 결과를 `Ship`, `Hold`, `Rollback`, `Need more data` 중 하나로 결정하기 위한 운영 기준을 정의한다.

본 문서는 기수 기반 cohort 비교 환경을 전제로 하며, 결과 해석은 Bayesian 확률과 Guardrail 안정성을 함께 본다.

## 2. Evaluation Inputs

판단 시 아래 세 요소를 동시에 검토한다.

- Primary metric: 완주율
- Guardrail metrics: 중도 이탈률, 주차별 출석률, 운영 부담
- Effect size: 실제 운영상 의미 있는 최소 개선 폭

## 3. Default Bayesian Criteria

기본 권장 기준은 아래와 같다.

- `P(B > A) > 80%`: 채택 검토 가능
- `P(B > A) > 95%`: 강한 채택 신호
- 최소 효과 크기: `+5%p` 이상
- Guardrail 악화 확률: `20% 미만`

## 4. Sample Size Limitation Warning

**이 플랫폼의 표본 규모는 통계적 검정력이 매우 낮다.**

완주율 +5%p 차이(예: 50% → 55%)를 탐지하려면 이론상 그룹당 약 770명이 필요하다.
현실적인 기수 규모(수십 명 수준)에서는 Bayesian posterior가 매우 넓게 형성되어, 대부분의 실험이 "불확실" 구간에 머물 가능성이 높다.

따라서 이 플랫폼의 분석 결과는 아래 수준으로 해석한다.

- 강한 통계적 증거가 아니라 **운영 의사결정을 위한 근사치**다.
- 작은 샘플에서 나온 `P(B > A) > 95%`는 대규모 실험과 동일한 신뢰도를 보장하지 않는다.
- 누적 기수 데이터가 쌓일수록 해석 신뢰도가 높아진다.

## 5. Sequential Monitoring Rule

중간 점검은 가능하지만, 아래 stopping rule 없이 조기 결론을 내리지 않는다.

- 최소 관측 기간: 2주
- 최소 누적 참여자 수: 50명
- 위 조건 미충족 시: `Need more data`

조기 채택 검토 조건:

- `P(B > A) > 95%`
- 최소 효과 크기 충족
- Guardrail 안정

조기 중단 검토 조건:

- Primary metric 악화 확률이 높음
- Guardrail 악화 신호가 반복적으로 확인됨
- 운영 부담 증가가 허용 범위를 넘음

## 6. Final Decision States

### Ship

아래 조건을 모두 만족하면 채택한다.

- 완주율 개선 확률이 충분히 높음
- 최소 효과 크기를 충족함
- Guardrail 악화가 허용 범위 내임
- 운영팀이 재현 가능하다고 판단함

### Hold

성과 신호는 있으나 바로 배포하지 않는다.

- uplift는 양수지만 불확실성이 큼
- Guardrail 일부가 불안정함
- 운영 비용 증가가 우려됨

### Rollback

개선안 적용을 중단하거나 되돌린다.

- 완주율 악화 가능성이 높음
- 중도 이탈률이 의미 있게 상승함
- 운영 부담이 과도하게 증가함

### Need more data

표본이나 관측 기간이 부족해서 판단을 유예한다.

- 최소 관측 기간 미충족
- 최소 샘플 수 미충족
- cohort 간 구성 차이가 커서 추가 확인 필요

## 7. Interpretation Notes

- cohort 비교 결과는 인과 추정이 아니라 운영 의사결정용 근사치로 해석한다.
- `발표 횟수`, `피드백 횟수`, `상호작용 수`는 선행 신호 후보이지 직접 원인으로 확정하지 않는다.
- Bayesian 결과가 좋아도 Guardrail이 악화되면 즉시 채택하지 않는다.
- Sequential Testing과 CUPED는 보조 도구이며, 적용 조건을 만족할 때만 사용한다.
