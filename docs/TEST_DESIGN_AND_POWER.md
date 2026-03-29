# Test Design and Power

## 1. Purpose

이 문서는 `abtest` 프로젝트에서 실험을 `실행 가능하고`, `해석 가능하며`, `표본 부족으로 무의미해지지 않도록` 설계하기 위한 기초 문서다.

핵심 목적은 아래 네 가지다.

- 실험 전 최소 기대 효과를 정의한다.
- 필요한 표본 수와 실험 기간을 대략 계산한다.
- 중간 점검과 stopping rule을 명확히 한다.
- 구현이 맞는지 A/A 테스트로 검증한다.

## 2. Minimum Topics

| 주제 | 왜 중요한가 | 우리 프로젝트에서의 의미 |
| --- | --- | --- |
| MDE and power | 너무 작은 실험을 막기 위함 | cohort 크기가 작을 때 현실적 기대치 설정 |
| Sample size formulas | 필요한 표본 감각 확보 | 완주율, 출석률 같은 비율 지표 계획 |
| Test duration vs traffic | 기간과 표본을 연결 | 기수 운영 주기, 시즌성 반영 |
| Fixed-horizon vs sequential | peeking 문제 방지 | 매주 확인하더라도 흔들리지 않게 함 |
| A/A tests | 구현 검증 | 이벤트/배정/집계가 정상인지 확인 |

## 3. Practical Rules for Our Project

### 1. MDE를 먼저 정한다

실험 시작 전 `얼마나 개선되면 의미 있는가`를 먼저 정해야 한다.

예시:

- 완주율 `+5%p` 이상
- 1주차 출석률 `+7%p` 이상

이 값은 통계적 의미만이 아니라 `운영상 의미 있는 변화`여야 한다.

### 2. 표본 수가 부족하면 exploratory로 분류한다

기수 기반 실험은 표본이 작을 가능성이 높다. 따라서 아래처럼 구분하는 것이 좋다.

- 결정 실험: 최소 표본과 기간을 만족
- 탐색 실험: 방향성 확인용

탐색 실험은 `ship` 근거보다 `다음 실험 설계 학습`에 더 가깝게 해석한다.

### 3. 기간은 트래픽이 아니라 운영 리듬으로도 본다

웹 서비스처럼 연속 트래픽이 있는 환경과 달리, 우리 프로젝트는 기수 운영 리듬이 강하다.

따라서 기간 설정 시 아래를 같이 본다.

- cohort 시작/종료 시점
- 주차별 활동 패턴
- 공휴일, 시험 기간, 시즌성
- 운영 변경 금지 구간

### 4. peeking은 규칙 없이 하지 않는다

중간 점검은 가능하지만, 아래가 없으면 조기 결론을 내리지 않는다.

- 최소 관측 기간
- 최소 샘플 수
- 조기 채택 조건
- 조기 중단 조건

### 5. A/A 테스트를 먼저 고려한다

새 지표, 새 이벤트, 새 배정 방식이 들어갈 때는 A/A 테스트로 구현 이상 여부를 먼저 확인한다.

## 4. MDE and Sample Size Intuition

### MDE

MDE는 `이 정도 차이는 보여야 실험할 가치가 있다`는 최소 효과 크기다.

너무 작게 잡으면:

- 필요한 표본이 과도하게 커진다.
- 현실적으로 실험이 끝나지 않는다.

너무 크게 잡으면:

- 의미 있는 개선을 놓칠 수 있다.

현재 프로젝트에서는 MDE를 통계 공식만으로 정하지 말고 아래를 같이 본다.

- 운영팀이 체감 가능한 변화인가
- 다음 기수 운영안을 바꿀 정도의 차이인가
- 리소스 증가를 감수할 가치가 있는가

### Sample Size

비율 지표에서는 대체로 아래 질문을 먼저 던지면 충분하다.

- baseline 완주율은 어느 정도인가
- treatment가 얼마나 나아져야 의미가 있는가
- 허용할 오탐과 미탐 수준은 어느 정도인가

이후 계산기나 공식을 사용해 대략적인 필요 표본을 잡는다.

## 5. Fixed Horizon vs Sequential

### Fixed-Horizon

장점:

- 해석이 단순하다
- 운영 규칙이 명확하다

단점:

- 작은 표본 환경에서는 느릴 수 있다

### Sequential

장점:

- 중간 판단이 가능하다
- 악화 실험을 더 빨리 중단할 수 있다

단점:

- 규칙 없이 보면 peeking 문제가 생긴다
- 운영자가 결과에 흔들릴 위험이 크다

현재 프로젝트 권장안:

- 기본은 fixed-horizon 사고방식
- 운영상 필요할 때만 sequential rule을 명시해 사용

## 6. A/A Testing Policy

A/A 테스트는 `차이가 없어야 하는 두 그룹`을 비교해 구현 이상을 찾는 과정이다.

아래 상황에서는 A/A 테스트를 우선 고려한다.

- 신규 이벤트 로그 도입
- 신규 배정 로직 도입
- KPI 집계 로직 개편
- 대시보드 계산 방식 변경

확인 포인트:

- assignment가 비정상적으로 치우치지 않았는가
- 특정 variant에만 이벤트 누락이 생기지 않는가
- metric 계산 결과가 비정상적으로 흔들리지 않는가

## 7. Recommended Resources

- [All about Sample-Size Calculations for A/B Testing](https://arxiv.org/pdf/2305.16459)
- [Statsig Sample Size Calculator](https://www.statsig.com/calculator)
- [How Not To Run an A/B Test](https://www.evanmiller.org/how-not-to-run-an-ab-test.html)
- [Convert - Why Statistics Matter in Experimentation](https://www.convert.com/blog/a-b-testing/decode-master-ab-testing-statistics/)
- [p-Hacking and False Discovery in A/B Testing](https://thearf-org-unified-admin.s3.amazonaws.com/MSI/2020/06/MSI_Report_18-130-1.pdf)

## 8. Interpretation Rules for Our Project

- 표본 수가 부족한 실험은 결정 실험이 아니라 탐색 실험으로 라벨링한다.
- MDE는 운영 의미 기준과 함께 정한다.
- stopping rule 없는 중간 확인은 판단 근거로 쓰지 않는다.
- A/A 테스트는 지루한 절차가 아니라 품질 검증의 시작점이다.

## 9. Link to Our Documents

- [`EXPERIMENT_POLICY.md`](EXPERIMENT_POLICY.md): 실험 등록과 승인 전제
- [`DECISION_RULE.md`](DECISION_RULE.md): stopping rule과 최종 상태 정의
- [`STATISTICAL_COLUMNS.md`](STATISTICAL_COLUMNS.md): sample size, effect size, uncertainty 컬럼 반영
- [`DATA_SCHEMA.md`](DATA_SCHEMA.md): experiment result와 data quality 구조

## 10. Practical Summary

- 실험 전 MDE를 먼저 정한다.
- 표본 수와 기간은 함께 설계한다.
- peeking은 rule 없이 하지 않는다.
- 새 구현은 A/A 테스트로 먼저 검증한다.
