# Experiment Policy Base

## 1. Purpose

이 문서는 `abtest` 실험 플랫폼을 실행하기 전에 먼저 고정해야 하는 운영 정책의 기준 문서다.

지금 단계의 목적은 파이프라인 구현이 아니라, `무엇을 실험으로 볼 것인가`, `어떻게 해석할 것인가`, `어떤 기준으로 기록할 것인가`를 정하는 것이다.

## 2. Core Policy

### 1. 실험 단위 정책

현재 기본 실험 단위는 `기수(cohort)`다.

- 이상적 구조: randomized A/B test
- 현재 기본 구조: cohort-based comparative experiment
- 정책 표현: `준실험(quasi-experiment)` 기반 운영

즉, `10기 vs 11기` 같은 비교는 실험으로 취급하되, 랜덤 A/B와 같은 강도의 인과 해석은 하지 않는다.

### 2. North Star 정책

North Star Metric은 `완주율` 하나로 고정한다.

기본 정의:

`완주율 = 최종 제출 완료 인원 / 첫 참여 인원`

운영 중 아래 정의를 혼용하지 않는다.

- 신청자 기준 완주율
- 첫 참여자 기준 완주율
- 실제 학습 시작자 기준 완주율

### 3. Metric 역할 분리 정책

모든 지표는 아래 네 역할 중 하나로 분류한다.

- North Star
- Supporting KPI
- Guardrail KPI
- Leading Indicator

정책상 `Leading Indicator`는 의사결정 보조 신호이지, 최종 채택 판단 기준이 아니다.

### 4. 해석 정책

- cohort 비교 결과는 운영 의사결정용 근사치로 해석한다.
- correlation 결과는 인과로 해석하지 않는다.
- p-value 또는 단일 수치 하나만으로 결론 내리지 않는다.
- effect size, interval, guardrail, sample size를 함께 본다.

### 5. 의사결정 정책

최종 실험 상태는 아래 네 가지 중 하나만 사용한다.

- `ship`
- `hold`
- `rollback`
- `need_more_data`

모든 결정은 이유와 함께 기록한다.

### 6. 학습 축적 정책

성공한 실험뿐 아니라 실패한 실험과 보류된 실험도 기록한다.

특히 아래 항목은 반드시 남긴다.

- 가설
- 결과 요약
- 반직관적 결과 여부
- 다음 기수에 반영할 액션

## 3. Minimum Policy Questions

실험을 시작하기 전에 아래 질문에 답할 수 있어야 한다.

| 질문 | 정책상 필요한 답 |
| --- | --- |
| 무엇을 바꾸는가 | 실험 변수 |
| 무엇을 좋아지게 만들고 싶은가 | primary metric |
| 무엇이 나빠지면 안 되는가 | guardrail |
| 언제까지 보고 판단할 것인가 | decision deadline |
| 누구 책임으로 운영하는가 | owner |
| 이 결과를 어디까지 믿을 것인가 | randomized vs cohort comparison 구분 |

## 4. Policy Objects to Store in DB

정책은 문서에만 두지 말고, 나중에 DB 메타데이터로도 관리 가능해야 한다.

권장 저장 대상:

- 실험 타입
- 분석 타입
- primary metric
- guardrail metric 목록
- decision deadline
- minimum sample rule
- stopping rule
- interpretation note

## 5. Within-Cohort Hybrid Assignment Policy

cohort 단위 비교(기수 간 비교)가 기본이지만, 같은 기수 내에서 treatment/control을 나누는 **within-cohort 하이브리드 방식**도 운영한다.

### 배정 단위

- **개인(individual) 단위**로 배정한다.
- 팀 단위 배정은 하지 않는다.

### 배정 방식

- 개발팀이 로직으로 구현한다. 데이터 팀이나 운영팀이 수동 배정하지 않는다.
- 배정 결과는 데이터로 저장되어야 하며, 실험 참여 기록과 함께 관리한다.

### 오염 방지: 세그먼트 분리

같은 기수 내 treatment/control 간 오염을 줄이기 위해, 배정 전에 참여 이력 기준으로 세그먼트를 먼저 분리한다.

| 세그먼트 | 정의 | 비고 |
|---|---|---|
| `new` | 현재 기수가 첫 참여 | 신규 참여자 |
| `returning` | 과거 기수 참여 이력이 한 번이라도 있음 (기수 간격 무관) | 재참여자 |

- treatment/control 배정은 **세그먼트 내에서** 이루어진다.
- `new`와 `returning`을 섞어서 배정하지 않는다.
- 세그먼트 간 완주율 기저값이 다를 수 있으므로 분석 시 세그먼트별로 분리하여 해석한다.

### 제약 사항

- 같은 primary metric을 쓰는 실험은 동시에 진행하지 않는다 (간섭 방지).
- 배정 비율 모니터링(SRM 체크)은 실험 기간 내 주기적으로 수행한다.

---

## 6. Practical Summary

정책 베이스의 핵심은 아래와 같다.

- 실험 단위는 우선 cohort 중심으로 본다.
- within-cohort 하이브리드 배정 시 세그먼트(신규/재참여)를 먼저 분리한다.
- North Star는 완주율 하나로 고정한다.
- 지표 역할을 섞지 않는다.
- 해석 강도를 실험 구조에 맞춘다.
- 결정과 학습을 모두 기록한다.
