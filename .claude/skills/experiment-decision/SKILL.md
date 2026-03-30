---
name: experiment-decision
description: 실험 결과를 해석하고 ship/hold/rollback/need_more_data를 판단한다.
  사용자가 "결과 어떻게 봐", "이거 올려도 돼", "통계적으로 유의한가",
  "완주율 차이 해석해줘" 등을 요청할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `07_OPERATIONS_AND_DECISIONS.md` — 판단 기준, 결정 규칙
- `03_METRICS.md` — guardrail 지표 정의 확인

## Step 2: 갭 점검 (Syneidesis)
판단 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 검증되지 않은 가정 (예: 두 코호트가 동질하다)
- `[Gap:Procedural]` 빠진 분석 (예: SRM 체크, novelty effect 확인)
- `[Gap:Consideration]` 외부 요인 (예: 해당 기수의 특수한 이벤트)

갭이 있으면 결론 전에 사용자에게 알리고 확인을 받는다.

## Step 3: Guardrail 체크 (최우선)
guardrail 지표를 **먼저** 확인한다:
- guardrail 지표가 하나라도 훼손되었는가?
- 훼손되었으면 → 다른 지표 결과와 무관하게 **hold 또는 rollback**

## Step 4: North Star 해석
- Bayesian 해석 우선: P(treatment > control) 계산
- p-value는 참고용으로만 제시, 단독 결론 금지
- 효과 크기(practical significance)를 함께 제시

## Step 5: 보조 분석 확인
필요 시 `05_ADVANCED_METHODS.md` 참조:
- Sequential testing 적용 여부
- CUPED로 분산 감소 가능한지

## Step 6: 결론 명시
반드시 다음 중 하나로 결론을 낸다:

| 결론 | 조건 |
|------|------|
| **ship** | guardrail 안전 + North Star 개선 + 갭 없음 |
| **hold** | guardrail 경계선 or 표본 부족 or 갭 미해소 |
| **rollback** | guardrail 훼손 |
| **need_more_data** | 효과 방향은 있으나 불확실성이 큼 |

## 출력 형식
```
Guardrail: [안전 / 경계 / 훼손]
North Star: P(treatment > control) = [%], 효과 크기 = [%p]
보조 분석: [해당 없음 / sequential / CUPED]
갭: [있으면 목록, 없으면 "없음"]
결론: [ship / hold / rollback / need_more_data]
근거: [한 줄 요약]
```

## 다음 단계

- **ship** → 완료. 결과를 `decision_log`에 기록
- **need_more_data** → `advanced-analysis` (CUPED/sequential로 불확실성 줄이기 시도)
- **hold** → `validity-check`로 원인 재점검
- **rollback** → `validity-check` + `experiment-design`으로 재설계
