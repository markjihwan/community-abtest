# KPI Table

## 1. Purpose

이 문서는 `abtest` 프로젝트에서 실제 운영과 실험 판단에 사용할 KPI를 우선순위 중심으로 정리한 표다.

핵심 원칙은 아래와 같다.

- North Star는 하나만 둔다.
- Supporting KPI는 병목과 맥락을 설명한다.
- Guardrail은 개선안의 부작용을 감시한다.
- Leading Indicator는 조기 신호 탐색용으로만 쓴다.

## 2. KPI Hierarchy

| 구분 | 역할 | 대표 질문 |
| --- | --- | --- |
| North Star | 최종 성과 판단 | 이 프로그램은 실제로 더 잘 끝났는가 |
| Supporting KPI | 병목과 원인 파악 | 어디서 꺾였고 어디서 좋아졌는가 |
| Guardrail KPI | 부작용 감시 | 성과는 올랐지만 다른 중요한 것이 망가지지 않았는가 |
| Leading Indicator | 조기 신호 탐색 | 초반에 위험이나 기회 신호가 보이는가 |

## 3. Core KPI Table

| 우선순위 | KPI | 분류 | 정의 | 기준 단위 | 확인 주기 | 의사결정 활용 |
| --- | --- | --- | --- | --- | --- | --- |
| P0 | 완주율 | North Star | `최종 제출 완료 인원 / 첫 참여 인원` | cohort | 기수 종료 시, 주간 추정 | 최종 성과 판단 |
| P0 | 중도 이탈률 | Guardrail | `중도 이탈 인원 / 첫 참여 인원` | cohort | 주간 | 부작용 감시 |
| P0 | 1주차 출석률 | Supporting KPI | `1주차 출석 인원 / 첫 참여 인원` | cohort | 주간 | 초반 진입 장벽 파악 |
| P0 | 2주차 생존율 | Supporting KPI | `2주차까지 유지 인원 / 첫 참여 인원` | cohort | 주간 | 초기 유지 확인 |
| P0 | 3주차 리텐션 | Guardrail | `3주차까지 유지 인원 / 첫 참여 인원` (이탈 사유 기록 병행) | cohort | 주간 | 이탈 가속 여부 감시 |
| P0 | 4주차 생존율 | Supporting KPI | `4주차까지 유지 인원 / 첫 참여 인원` | cohort | 주간 | 중반 유지 확인 |
| P1 | 첫 참여율 | Funnel KPI | `첫 참여 인원 / 승인 인원` | cohort | 주간 | 승인 이후 전환 파악 |
| P1 | 승인율 | Funnel KPI | `승인 인원 / 신청 인원` | cohort | 모집 기간 중, 기수 종료 시 | 모집 품질 확인 |
| P1 | 재참여율 | Retention KPI | `다음 기수 재참여 인원 / 해당 cohort 종료 인원` | cohort | 기수 종료 후 | 장기 가치 판단 |
| P1 | 운영 부담 | Guardrail | 멘토 시간, 수동 대응, 리마인드 횟수 묶음 | cohort, week | 주간 | 지속 가능성 판단 |
| P1 | 결과물 제출률 | Outcome KPI | `결과물 제출 인원 / 첫 참여 인원` | cohort | 주간, 기수 종료 시 | 완주 이전 성과 확인 |
| P2 | 발표 횟수 | Leading Indicator | 발표 수행 횟수 | participant, cohort | 주간 | 완주 선행 신호 탐색 |
| P2 | 피드백 횟수 | Leading Indicator | 주고받은 피드백 총횟수 | participant, cohort | 주간 | 참여 강도 탐색 |
| P2 | 상호작용 수 | Leading Indicator | 댓글, 멘션, 공동 작업, 멘토 교류 합 | participant, cohort | 주간 | 협업 활성도 탐색 |
| P2 | lurker 전환율 | Growth KPI | `기여 행동 시작 인원 / 관찰 대상 비기여 인원` | cohort | 주간, 기수 종료 시 | 기여 전환 파악 |

## 4. Recommended Dashboard View

운영 대시보드는 아래 순서로 보는 것이 좋다.

### Executive View

- 완주율
- 중도 이탈률
- 4주차 생존율
- 재참여율

### Weekly Operation View

- 첫 참여율
- 1주차 출석률
- 2주차 생존율
- 운영 부담

### Exploration View

- 발표 횟수
- 피드백 횟수
- 상호작용 수
- lurker 전환율

## 5. KPI Interpretation Rule

### North Star

완주율은 최종 성과 판단에만 사용한다. 다른 지표가 좋아도 완주율이 개선되지 않으면 핵심 성과가 개선되었다고 보지 않는다.

### Supporting KPI

Supporting KPI는 `왜 그런 결과가 나왔는가`를 설명하는 용도다. 예를 들어 완주율이 하락했을 때, 1주차 출석률과 2주차 생존율을 통해 어디서 병목이 생겼는지 확인한다.

### Guardrail KPI

Guardrail은 성과 개선을 무효화할 수 있는 지표다. 예를 들어 완주율이 소폭 상승했더라도 운영 부담이 과도하게 증가하거나 중도 이탈률이 나빠지면 채택을 보류할 수 있다.

### Leading Indicator

Leading Indicator는 인과 변수로 확정하지 않는다. 의사결정 보조 신호로만 사용하며, `발표를 많이 해서 완주했다`가 아니라 `완주 가능성이 높은 사람에게서 발표가 자주 관찰되었다` 수준으로 해석한다.

## 6. Minimal KPI Set for MVP

처음부터 모든 지표를 정교하게 쌓기 어렵다면 아래 최소 세트부터 시작한다.

| 우선순위 | KPI | 이유 |
| --- | --- | --- |
| 1 | 완주율 | 최종 성과 판단의 기준점 |
| 2 | 1주차 출석률 | 초반 이탈의 첫 신호 |
| 3 | 2주차 생존율 | 유지 곡선의 핵심 분기점 |
| 4 | 중도 이탈률 | 부작용 감시 |
| 5 | 운영 부담 | 실험 지속 가능성 판단 |
| 6 | 재참여율 | 장기 가치 확인 |

## 7. Practical Notes

- KPI는 cohort 간 동일 정의를 유지해야 한다.
- `완주율`, `결과물 제출률`, `재참여율`은 outcome 중심 지표다.
- `발표 횟수`, `피드백 횟수`, `상호작용 수`는 leading indicator다.
- `운영 부담`은 반드시 수치화해서 기록해야 한다.
- KPI 표는 실험 설계, 대시보드 설계, 데이터 스키마 설계의 기준 문서로 사용한다.
