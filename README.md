# ABTest Experiment Platform

`abtest`는 커뮤니티/러닝 프로그램 운영 환경에서 실험을 설계하고 해석하기 위한 문서 중심 프로젝트다.

이 프로젝트는 이상적인 랜덤 A/B 테스트를 지향하되, 실제 운영에서는 기수 단위 비교가 중심이 되는 환경을 전제로 한다. 따라서 본 문서 세트는 `randomized A/B test`와 `cohort-based comparative experiment`를 구분해서 설명한다.

## Core Principle

본 프로젝트의 실험 평가는 랜덤 A/B 테스트가 어려운 운영 환경을 고려하여, 기수 단위 cohort 비교를 기반으로 수행한다.
핵심 성과는 완주율을 North Star Metric으로 두고, Funnel 분석으로 단계별 이탈을 파악하며, Retention 분석으로 지속 참여를 측정한다.
최종 효과 판단은 Bayesian 기반 확률 해석을 중심으로 수행하고, 필요 시 Sequential Testing과 CUPED를 보조적으로 활용한다.

## Document Map

- [`docs/EXPERIMENT_FRAMEWORK.md`](docs/EXPERIMENT_FRAMEWORK.md): 실험 철학, 분석 프레임, 해석 원칙
- [`docs/STATISTICAL_FOUNDATIONS.md`](docs/STATISTICAL_FOUNDATIONS.md): A/B 테스트 해석을 위한 통계 기초 레이어
- [`docs/TEST_DESIGN_AND_POWER.md`](docs/TEST_DESIGN_AND_POWER.md): 실험 설계, 표본 수, 기간, stopping rule 기초
- [`docs/RATIO_METRICS.md`](docs/RATIO_METRICS.md): CTR, ARPU, per-user conversion 같은 ratio metric 해석 기초
- [`docs/MULTIPLE_TESTING.md`](docs/MULTIPLE_TESTING.md): 다중 검정과 false discovery 통제 기초
- [`docs/PITFALLS_AND_DATA_QUALITY.md`](docs/PITFALLS_AND_DATA_QUALITY.md): peeking, SRM, 계측 오류, 품질 검증 원칙
- [`docs/NOVELTY_AND_NETWORK_EFFECTS.md`](docs/NOVELTY_AND_NETWORK_EFFECTS.md): novelty, primacy, cluster, switchback 설계 기초
- [`docs/VARIANCE_REDUCTION.md`](docs/VARIANCE_REDUCTION.md): CUPED, stratification, ML 기반 분산 감소 기초
- [`docs/SEQUENTIAL_TESTING.md`](docs/SEQUENTIAL_TESTING.md): group sequential, always-valid, SPRT 기초
- [`docs/EXPERIMENT_POLICY_BASE.md`](docs/EXPERIMENT_POLICY_BASE.md): 실험 플랫폼 운영을 위한 정책 베이스
- [`docs/EXPERIMENT_POLICY.md`](docs/EXPERIMENT_POLICY.md): 실험 설계 정책과 승인/충돌 규칙
- [`docs/RESULT_POLICY.md`](docs/RESULT_POLICY.md): 결과 공유 방식, 의사결정 반영 절차, 결과 기록 보관
- [`docs/DATA_POLICY.md`](docs/DATA_POLICY.md): 데이터 수집 범위, 보관 기간, 접근 권한, 품질 기준
- [`docs/PARTICIPANT_POLICY.md`](docs/PARTICIPANT_POLICY.md): 실험 대상 정의, 고지 원칙, 그룹 배정 규칙, 참여자 보호
- [`docs/METRIC_DICTIONARY.md`](docs/METRIC_DICTIONARY.md): North Star, Funnel, Retention, Guardrail 지표 정의
- [`docs/KPI_TABLE.md`](docs/KPI_TABLE.md): 운영용 KPI 표와 우선순위
- [`docs/DATA_SCHEMA.md`](docs/DATA_SCHEMA.md): 이벤트/엔터티/필드 설계 초안
- [`docs/STATISTICAL_COLUMNS.md`](docs/STATISTICAL_COLUMNS.md): DB에 넣을 통계 컬럼 설계 원칙
- [`docs/DECISION_RULE.md`](docs/DECISION_RULE.md): 실험 채택, 보류, 중단 기준
- [`docs/OPERATION_GUIDE.md`](docs/OPERATION_GUIDE.md): 실험 전/중/후 운영 체크리스트
- [`docs/COMMUNITY_BENCHMARKS.md`](docs/COMMUNITY_BENCHMARKS.md): 다른 커뮤니티/학습 플랫폼의 데이터 활용 사례와 적용 포인트

## Recommended Reading Order

1. 실험 구조와 해석 원칙은 [`docs/EXPERIMENT_FRAMEWORK.md`](docs/EXPERIMENT_FRAMEWORK.md)부터 읽는다.
2. 통계 기초는 [`docs/STATISTICAL_FOUNDATIONS.md`](docs/STATISTICAL_FOUNDATIONS.md)에서 정리한다.
3. 실험 설계와 표본 수 기초는 [`docs/TEST_DESIGN_AND_POWER.md`](docs/TEST_DESIGN_AND_POWER.md)에서 정리한다.
4. ratio metric 해석은 [`docs/RATIO_METRICS.md`](docs/RATIO_METRICS.md)에서 정리한다.
5. 다중 검정은 [`docs/MULTIPLE_TESTING.md`](docs/MULTIPLE_TESTING.md)에서 정리한다.
6. 품질 리스크는 [`docs/PITFALLS_AND_DATA_QUALITY.md`](docs/PITFALLS_AND_DATA_QUALITY.md)에서 정리한다.
7. novelty와 network effect는 [`docs/NOVELTY_AND_NETWORK_EFFECTS.md`](docs/NOVELTY_AND_NETWORK_EFFECTS.md)에서 정리한다.
8. 분산 감소는 [`docs/VARIANCE_REDUCTION.md`](docs/VARIANCE_REDUCTION.md)에서 정리한다.
9. sequential testing은 [`docs/SEQUENTIAL_TESTING.md`](docs/SEQUENTIAL_TESTING.md)에서 정리한다.
10. 정책 베이스는 [`docs/EXPERIMENT_POLICY_BASE.md`](docs/EXPERIMENT_POLICY_BASE.md)에서 고정한다.
11. 실험 설계 정책은 [`docs/EXPERIMENT_POLICY.md`](docs/EXPERIMENT_POLICY.md)에서 구체화한다.
12. 운영 지표 정의는 [`docs/METRIC_DICTIONARY.md`](docs/METRIC_DICTIONARY.md)에서 고정한다.
13. 실제 운영용 지표 우선순위는 [`docs/KPI_TABLE.md`](docs/KPI_TABLE.md)에서 본다.
14. 데이터 적재 규칙은 [`docs/DATA_SCHEMA.md`](docs/DATA_SCHEMA.md)에 맞춘다.
15. 통계 컬럼 원칙은 [`docs/STATISTICAL_COLUMNS.md`](docs/STATISTICAL_COLUMNS.md)에서 본다.
16. 실험 운영은 [`docs/OPERATION_GUIDE.md`](docs/OPERATION_GUIDE.md)의 체크리스트를 따른다.
17. 최종 판단은 [`docs/DECISION_RULE.md`](docs/DECISION_RULE.md)을 따른다.
18. 외부 사례 참고는 [`docs/COMMUNITY_BENCHMARKS.md`](docs/COMMUNITY_BENCHMARKS.md)에서 본다.
