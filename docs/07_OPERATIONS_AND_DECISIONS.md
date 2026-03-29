# 07 Operations and Decisions

## Purpose

이 문서는 실험을 실제로 운영할 때 필요한 체크리스트와 최종 판단 규칙을 묶는다.

## Covers

- 실험 전/중/후 운영 체크리스트
- ship / hold / rollback / need_more_data 기준
- Bayesian 해석과 guardrail 기반 판단

## Read These

- [`OPERATION_GUIDE.md`](OPERATION_GUIDE.md)
- [`DECISION_RULE.md`](DECISION_RULE.md)

## Key Takeaways

- 운영 체크리스트와 최종 의사결정은 분리해서 본다.
- 작은 표본 결과는 운영 근사치로 해석한다.
- sequential, CUPED, Bayesian 결과도 guardrail보다 우선하지 않는다.
