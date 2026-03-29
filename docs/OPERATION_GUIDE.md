# Operation Guide

## 1. Purpose

이 문서는 실험을 설계하고 운영하는 담당자가 `실험 전 → 진행 중 → 종료 후` 각 단계에서 해야 할 일을 체크리스트 형태로 정리한 운영 가이드다.

분석 방법론은 `EXPERIMENT_FRAMEWORK.md`, 지표 정의는 `METRIC_DICTIONARY.md`, 최종 판단 기준은 `DECISION_RULE.md`를 참조한다.

---

## 2. Phase 1: 실험 설계 전 (Pre-Experiment)

### 2-1. 실험 조건 확인

- [ ] 이번 기수에서 적용하는 변경사항이 무엇인지 명확히 정의했는가
- [ ] 비교 대상(이전 기수 또는 동시 운영 그룹)이 확정되었는가
- [ ] cohort 간 구성 차이(신청 경로, 모집 방식, 시즌)를 사전에 파악했는가
- [ ] 최소 관측 기간(2주)과 최소 샘플 수(50명)를 충족할 수 있는 규모인가

### 2-2. 지표 정의 고정

- [ ] North Star Metric(완주율)의 분자/분모 기준을 이번 기수 기준으로 명시했는가
  - 기본값: `최종 제출 완료 인원 / 첫 참여 인원`
  - 기준 변경 시 반드시 기록
- [ ] Funnel 단계 정의가 고정되었는가 (`신청 → 승인 → 첫 참여 → 1주차 출석 → 최종 완주`)
- [ ] Retention 기준 주차가 확정되었는가 (1~4주차 생존율 + 재참여율)
- [ ] Guardrail 지표 감시 기준이 설정되었는가
  - 중도 이탈률 허용 범위
  - 운영 부담 지표 기준선

### 2-3. 데이터 수집 준비

- [ ] `DATA_SCHEMA.md` 기준으로 필수 필드가 수집 가능한 상태인가
  - Funnel 필수: `participant_id`, `cohort_id`, `applied_at`, `approved_at`, `first_attended_at`, `completed_flag`
  - Retention 필수: `week_number`, `attended_flag`
  - Guardrail 필수: `dropped_flag`, `mentor_minutes`, `manual_intervention_count`
- [ ] 이벤트 타임스탬프 기준이 UTC 또는 단일 기준으로 통일되어 있는가
- [ ] CUPED 적용 예정이라면, 선행 변수(이전 출석률, 사전 활동 점수 등)를 별도 보관했는가

### 2-4. 실험 메타데이터 기록

아래 항목을 `Cohort` 엔터티에 기록한다.

- `cohort_id`, `cohort_name`
- `program_type`
- `start_date`, `end_date`
- `operator_id`
- `experiment_variant`: 이번 기수에 적용한 변경사항 요약
- `experiment_notes`: 외부 요인, 운영 특이사항 등

---

## 3. Phase 2: 실험 진행 중 (During Experiment)

### 3-1. 주차별 모니터링 항목

매주 아래 항목을 점검한다.

- [ ] 주차별 출석률이 이전 기수 대비 비정상적으로 낮거나 높지 않은가
- [ ] 중도 이탈이 특정 주차에 집중되고 있지 않은가
- [ ] 운영 부담 지표(멘토 개입 시간, 리마인드 발송 횟수)가 기준선을 초과하지 않는가

### 3-2. Sequential Monitoring 규칙

중간 점검은 가능하지만 아래 조건을 지킨다.

- 최소 2주 운영 전에는 조기 판단하지 않는다
- 누적 참여자 50명 미만이면 결과 해석을 보류한다
- 매주 결과를 보더라도 stopping rule 없이 결론을 내리지 않는다

### 3-3. 조기 종료 검토 조건

아래 중 하나라도 해당되면 조기 종료를 검토한다.

- Primary metric(완주율) 악화 가능성이 반복적으로 확인됨
- 중도 이탈률이 기준선을 지속적으로 초과함
- 운영 부담이 허용 범위를 명확히 넘어섬

조기 채택 검토 조건:

- `P(B > A) > 95%` 이고 최소 효과 크기(+5%p) 충족
- Guardrail 지표 모두 안정 상태

### 3-4. 운영 특이사항 기록

운영 중 발생하는 아래 사항은 즉시 기록한다.

- 외부 일정 충돌 (공휴일, 대규모 이벤트 등)
- 운영 방식 변경 (공지 채널, 멘토 교체 등)
- 참여자 구성 변화 (중도 합류, 예외 승인 등)

---

## 4. Phase 3: 실험 종료 후 (Post-Experiment)

### 4-1. 최종 분석 체크리스트

- [ ] North Star Metric(완주율) 최종값 산출 완료
- [ ] Funnel 단계별 전환율 계산 완료
- [ ] 주차별 생존곡선(Retention) 계산 완료
- [ ] Guardrail 지표 최종값 확인 완료
- [ ] Bayesian 기반 `P(B > A)` 계산 완료
- [ ] 최소 효과 크기(+5%p) 충족 여부 확인
- [ ] CUPED 적용 대상이라면, 공변량 보정 후 결과 산출 완료

### 4-2. 의사결정 판단

`DECISION_RULE.md` 기준에 따라 아래 네 상태 중 하나로 결정한다.

| 판단 | 조건 요약 |
| --- | --- |
| **Ship** | 완주율 개선 확률 충분 + 효과 크기 충족 + Guardrail 안정 + 운영 재현 가능 |
| **Hold** | uplift 양수이나 불확실성 큼 또는 Guardrail 일부 불안정 |
| **Rollback** | 완주율 악화 가능성 높음 또는 이탈률 상승 또는 운영 부담 과도 |
| **Need more data** | 최소 관측 기간 또는 샘플 수 미충족 또는 cohort 구성 차이 과도 |

### 4-3. 결과 기록 형식

실험 종료 후 아래 항목을 기록해둔다.

```
cohort_id:
experiment_variant:
기간:
참여자 수 (첫 참여 기준):

[North Star]
완주율: X% (비교 기수: Y%)
P(B > A): Z%
effect size: +N%p

[Funnel]
신청 → 승인: X%
승인 → 첫 참여: X%
첫 참여 → 1주차 출석: X%
첫 참여 → 최종 완주: X%

[Retention]
1주차 생존율: X%
2주차 생존율: X%
3주차 생존율: X%
4주차 생존율: X%
재참여율: X%

[Guardrail]
중도 이탈률: X%
주차별 출석률 이상 여부: Y/N
운영 부담 이상 여부: Y/N

[판단]
결정: Ship / Hold / Rollback / Need more data
근거:
운영 특이사항:
```

### 4-4. 다음 기수 반영 여부 결정

- Ship이면: 다음 기수에 동일 변경사항을 기본 운영으로 포함
- Hold이면: 불확실 요인을 명시하고 재실험 조건 정의
- Rollback이면: 변경사항 제거 후 원래 운영 방식으로 복귀
- Need more data이면: 다음 기수에서 동일 실험을 연장 관측

---

## 5. 빠른 참조

| 단계 | 핵심 확인 포인트 |
| --- | --- |
| 실험 전 | 지표 정의 고정, 데이터 수집 준비, 메타데이터 기록 |
| 진행 중 | 주차별 Guardrail 점검, Sequential rule 준수, 특이사항 기록 |
| 종료 후 | Bayesian 판단 + Guardrail 종합 → Ship/Hold/Rollback/Need more data |
