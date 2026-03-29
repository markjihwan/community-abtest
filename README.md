# ABTest Experiment Platform

`abtest`는 커뮤니티/러닝 프로그램 운영 환경에서 실험을 설계하고 해석하기 위한 문서 중심 프로젝트다.

이 프로젝트는 이상적인 랜덤 A/B 테스트를 지향하되, 실제 운영에서는 기수 단위 비교가 중심이 되는 환경을 전제로 한다. 따라서 본 문서 세트는 `randomized A/B test`와 `cohort-based comparative experiment`를 구분해서 설명한다.

## Core Principle

본 프로젝트의 실험 평가는 랜덤 A/B 테스트가 어려운 운영 환경을 고려하여, 기수 단위 cohort 비교를 기반으로 수행한다.
핵심 성과는 완주율을 North Star Metric으로 두고, Funnel 분석으로 단계별 이탈을 파악하며, Retention 분석으로 지속 참여를 측정한다.
최종 효과 판단은 Bayesian 기반 확률 해석을 중심으로 수행하고, 필요 시 Sequential Testing과 CUPED를 보조적으로 활용한다.

## Start Here

지금부터는 문서를 `핵심 7개 + 부록` 구조로 읽는 것을 권장한다.

## Core Docs

- [`docs/01_FOUNDATIONS.md`](docs/01_FOUNDATIONS.md): 실험 철학, 통계 기초, test design의 입문 묶음
- [`docs/02_EXPERIMENT_POLICY.md`](docs/02_EXPERIMENT_POLICY.md): 실험 등록, 승인, 데이터/참여자/결과 활용 정책 묶음
- [`docs/03_METRICS.md`](docs/03_METRICS.md): metric 정의와 KPI 우선순위
- [`docs/04_VALIDITY_AND_TRUST.md`](docs/04_VALIDITY_AND_TRUST.md): peeking, SRM, novelty, network effect, 품질 리스크
- [`docs/05_ADVANCED_METHODS.md`](docs/05_ADVANCED_METHODS.md): ratio metrics, multiple testing, variance reduction, sequential testing
- [`docs/06_PLATFORM_SCHEMA.md`](docs/06_PLATFORM_SCHEMA.md): 데이터 스키마와 통계 컬럼 설계
- [`docs/07_OPERATIONS_AND_DECISIONS.md`](docs/07_OPERATIONS_AND_DECISIONS.md): 운영 체크리스트와 최종 판단 기준

## Appendix

- [`docs/COMMUNITY_BENCHMARKS.md`](docs/COMMUNITY_BENCHMARKS.md): 외부 사례와 벤치마크
- [`docs/V1_SCOPE_AND_GAPS.md`](docs/V1_SCOPE_AND_GAPS.md): 현재 범위 점검과 v1 우선순위
- [`docs/REFERENCE_MAP.md`](docs/REFERENCE_MAP.md): 기존 세부 문서와 새 그룹 문서의 매핑
- [`docs/archive/`](docs/archive): 수정 전 세부 문서 아카이브

## Recommended Reading Order

1. [`docs/01_FOUNDATIONS.md`](docs/01_FOUNDATIONS.md)
2. [`docs/02_EXPERIMENT_POLICY.md`](docs/02_EXPERIMENT_POLICY.md)
3. [`docs/03_METRICS.md`](docs/03_METRICS.md)
4. [`docs/04_VALIDITY_AND_TRUST.md`](docs/04_VALIDITY_AND_TRUST.md)
5. [`docs/06_PLATFORM_SCHEMA.md`](docs/06_PLATFORM_SCHEMA.md)
6. [`docs/07_OPERATIONS_AND_DECISIONS.md`](docs/07_OPERATIONS_AND_DECISIONS.md)
7. [`docs/05_ADVANCED_METHODS.md`](docs/05_ADVANCED_METHODS.md)

## Note

기존 세부 문서는 `docs/archive/`로 이동해 보관한다. 앞으로는 새 그룹 문서를 기준으로 읽고, 세부 문서는 필요할 때만 참고하는 구조를 권장한다.
