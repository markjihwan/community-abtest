# Metric Dictionary

## Metric Design Principle

모든 지표는 아래 원칙을 따른다.

- 분자와 분모가 명확해야 한다.
- 기준 시점이 명확해야 한다.
- 운영 중 재정의하지 않는다.
- cohort 간 비교 가능해야 한다.

## 1. North Star Metric

### Completion Rate

- 한글명: 완주율
- 정의: `최종 제출 완료 인원 / 첫 참여 인원`
- 권장 단위: cohort
- 해석 목적: 프로그램의 최종 성과 측정
- 비고: 기본 North Star Metric

## 2. Funnel Metrics

### Application Rate

- 한글명: 신청 수
- 정의: 실험/기수별 신청 완료 인원 수
- 해석 목적: 유입 규모 파악

### Approval Rate

- 한글명: 승인율
- 정의: 승인 인원 / 신청 인원
- 해석 목적: 선발 단계 전환 파악

### First Participation Rate

- 한글명: 첫 참여율
- 정의: 첫 참여 인원 / 승인 인원
- 해석 목적: 실제 참여 시작 전환 파악

### Week 1 Attendance Rate

- 한글명: 1주차 출석률
- 정의: 1주차 출석 인원 / 첫 참여 인원
- 해석 목적: 초반 진입 장벽 확인

### Final Completion Rate

- 한글명: 최종 완주율
- 정의: 완주 인원 / 첫 참여 인원
- 해석 목적: 프로그램 종료 성과 확인

## 3. Retention Metrics

### Weekly Survival Rate

- 한글명: 주차별 생존율
- 정의: n주차까지 참여를 유지한 인원 / 첫 참여 인원
- 예시: 2주차 생존율, 3주차 생존율, 4주차 생존율
- 해석 목적: 시간 경과에 따른 잔존 추이 파악

### Rejoin Rate

- 한글명: 재참여율
- 정의: 다음 기수에 다시 참여한 인원 / 해당 cohort 종료 인원
- 해석 목적: 장기 만족도와 재유입 가능성 측정

## 4. Guardrail Metrics

### Drop-off Rate

- 한글명: 중도 이탈률
- 정의: 중도 이탈 인원 / 첫 참여 인원
- 해석 목적: 개선안이 이탈을 증가시키는지 감시

### Weekly Attendance Rate

- 한글명: 주차별 출석률
- 정의: 해당 주차 출석 인원 / 첫 참여 인원
- 해석 목적: 참여 품질 유지 여부 확인

### Operational Load

- 한글명: 운영 부담
- 정의: 운영 리소스 사용량을 나타내는 보조 지표 묶음
- 예시: 멘토 개입 시간, 공지/리마인드 발송 횟수, 운영자 수동 대응 건수
- 해석 목적: 성과 개선이 과도한 운영 비용으로 만들어진 것인지 확인

## 5. Behavioral and Leading Indicators

### Presentation Count

- 한글명: 발표 횟수
- 정의: 개인 또는 cohort 단위 발표 수행 횟수
- 해석 목적: 완주 가능성의 선행 신호 탐색
- 주의: 인과 해석 금지

### Feedback Count

- 한글명: 피드백 횟수
- 정의: 주고받은 피드백 총횟수
- 해석 목적: 참여 강도 파악

### Interaction Count

- 한글명: 상호작용 수
- 정의: 댓글, 멘션, 공동 작업, 멘토/동료 교류의 합 또는 세부 지표
- 해석 목적: 협업 활성도 측정
- 비고: 향후 network 분석 확장 가능
