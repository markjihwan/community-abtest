---
name: validity-check
description: 실험의 내적 타당도를 점검한다.
  "SRM 의심돼", "novelty effect 아닌가", "peeking 했어", "network effect
  있을 것 같은데", "이 실험 믿어도 돼?" 등 실험 품질 리스크를 언급할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `04_VALIDITY_AND_TRUST.md` — 타당도 리스크 전체 목록

## Step 2: 갭 점검 (Syneidesis)
점검 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 놓친 가정 (예: 코호트 간 외부 조건이 동일하다)
- `[Gap:Procedural]` 미실시 체크 (예: SRM 미확인)
- `[Gap:Consideration]` 추가 고려 요인 (예: 플랫폼 변경, 운영 이슈)

## Step 3: 리스크 항목 체크
사용자가 언급한 리스크부터 시작하고, 나머지도 순서대로 확인한다:

### SRM (Sample Ratio Mismatch)
- 배정 비율과 실제 참여 비율이 다른가?
- 다르면 → 실험 결과를 신뢰할 수 없음, 원인 조사 필요

### Peeking
- 중간에 결과를 보고 결정을 내렸는가?
- 그랬다면 → p-value 인플레이션 가능성, sequential testing으로 재분석 필요

### Novelty Effect
- 신규 기능에 대한 일시적 반응인가?
- 판단 기준: 효과가 기수 후반부에서도 유지되는가?

### Network Effect
- 처치군과 대조군 간 상호작용이 있는가? (같은 커뮤니티 내 소통)
- 있다면 → SUTVA 위반, 결과 해석 주의

### 기타 타당도 위협
- 선택 편향: 코호트 자체의 특성이 다른가?
- 역사 효과: 해당 기간에 외부 이벤트가 있었는가?
- 성숙 효과: 시간이 지나면서 자연스럽게 변하는 지표인가?

## Step 4: 종합 판정

| 판정 | 기준 |
|------|------|
| **신뢰 가능** | 리스크 항목 없음 또는 모두 통제됨 |
| **주의 필요** | 일부 리스크 있으나 결과 해석에 한계 명시 가능 |
| **신뢰 불가** | SRM 확인, peeking으로 분석 오염, network effect 통제 불가 |

## 출력 형식
```
점검 항목:
- SRM: [없음 / 의심 / 확인됨]
- Peeking: [없음 / 있음]
- Novelty Effect: [없음 / 의심 / 확인됨]
- Network Effect: [없음 / 의심 / 확인됨]
- 기타: [해당 항목]

갭: [있으면 목록, 없으면 "없음"]
종합 판정: [신뢰 가능 / 주의 필요 / 신뢰 불가]
권고: [한 줄 요약]
```

## 다음 단계

- **신뢰 가능** → `experiment-register`로 등록 진행
- **주의 필요** → 설계 보완 후 `experiment-design`으로 돌아가 재확인
- **신뢰 불가** → `experiment-design`으로 돌아가 실험 단위/설계 재검토
- 분석 방법 자체가 의심된다면 → `knowledge-audit`
