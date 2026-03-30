# 실험 등록서: [실험명]

## 기본 정보

```
실험명:
실험 타입:    [randomized_ab / cohort_comparison / quasi_experiment]
분석 타입:    [within-cohort observational comparison / between-cohort comparison]
상태:         [등록 중 / 진행 중 / 완료 / 보류]
```

## 배경

<!-- 왜 이 실험을 하는가? 어떤 문제를 해결하려는가? -->

## 분석 질문

> <!-- "X는 Y보다 Z가 더 높은가?" 형태로 작성 -->

## Treatment 정의

> ⏳ 확정 예정 / ✅ 확정

| 컬럼 | 설명 |
|------|------|
| `treatment_exposed_at` | 노출 시점 |
| `treatment_completed_at` | 완료 시점 |
| `treatment_participation_level` | 단계 정의 |

## 데이터 설계

### Analysis Unit
`participant within cohort [N]` — 개별 참여자, 약 [N]명

### Feature Grain ([기준 시점] 고정)

| 컬럼 | 설명 |
|------|------|
| `prior_cohort_experience_flag` | 이전 기수 경험 여부 |
| `attendance_count_pre_treatment` | 사전 출석 횟수 |
| `assignment_submit_count_pre_treatment` | 사전 과제 제출 수 |

### Treatment Grain
`participant` — [treatment 정의]

### Outcome Grain
`participant-week` — [outcome 측정 방식]

### Final Evaluation Grain
`participant` — [최종 판단 기준]

## 지표

### Primary
- **완주율** (완주자 수 / 등록자 수)

### Supporting KPI
- <!-- 잔존율, 과제 제출률 등 -->

### Guardrail
> <!-- 어떤 지표가 얼마 이상 훼손되면 hold인가? -->

## 분석 방법

### 방법 선택
- [ ] 층화 분석 (셀당 20명+ 확보 시)
- [ ] 공변량 보정 로지스틱 회귀 (표본 부족 시)
- [ ] PSM (사후 업그레이드)

### ITT / ATT 분리

| 분석 | 대상 | 기준 | 해석 |
|------|------|------|------|
| ITT | 전원 | 노출 기준 | 노출 자체의 효과 |
| ATT | 완료자 | 완료 기준 | 실제 수행의 효과 |

### Spillover 확인
- `team_id`, `mentor_group_id` 기준 within/between 비교

## 해석 주의문

> "관측된 사전 특성이 유사한 집단 내에서 [treatment] 참여자가 비참여자보다
> [outcome]이 높았다. 단, 관측되지 않은 교란변수의 영향을 배제할 수 없어
> 인과 추론이 아닌 연관성 수준으로 해석한다."

## 일정

| 항목 | 일정 |
|------|------|
| Treatment 확정 | |
| Pre-스냅샷 실행 | |
| 실험 시작 | |
| 실험 종료 | |
| Decision deadline | |

## 등록 체크리스트

| 항목 | 상태 |
|------|------|
| 가설 | ⏳ |
| 실험 단위 | ⏳ |
| Treatment 정의 | ⏳ |
| Primary + Guardrail 지표 | ⏳ |
| 분석 방법 | ⏳ |
| Spillover 통제 | ⏳ |
| ITT / ATT 분리 | ⏳ |
| 해석 주의문 | ⏳ |
| Decision deadline | ⏳ |

**등록 가능 여부: [가능 / 조건부 가능 — 사유 / 불가 — 사유]**
