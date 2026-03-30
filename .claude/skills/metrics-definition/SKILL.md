---
name: metrics-definition
description: 실험에서 어떤 지표를 볼지 정의하고 우선순위를 정한다.
  "완주율 말고 뭐 봐야 해", "지표 어떻게 정의해", "KPI 뭐로 잡아야 해",
  "guardrail 지표가 뭔데", "leading indicator 뭐 써야 해" 등을 요청할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `03_METRICS.md` — 지표 정의와 KPI 우선순위

## Step 2: 갭 점검 (Syneidesis)
지표 정의 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 지표의 분모/분자가 명확히 정의되어 있는가?
- `[Gap:Procedural]` Funnel과 Retention을 혼용하고 있지는 않은가?
- `[Gap:Consideration]` leading indicator를 인과로 해석할 위험이 있는가?

## Step 3: 지표 계층 정의

### North Star (1개 고정)
- **완주율** — 변경 시 반드시 이유를 명시해야 함

### Supporting KPI
- Funnel 지표: 단계별 이탈률 (등록 → 1주차 → 중반 → 완주)
- Retention 지표: 주차별 재참여율

> Funnel과 Retention은 섞지 않는다. 각각 독립적으로 해석한다.

### Guardrail 지표
- 훼손되면 North Star 결과와 무관하게 ship하지 않는 지표
- 사용자가 정의하지 않았으면 먼저 확인한다

### Leading Indicator
- 완주 전 조기 신호 (예: 1주차 과제 제출률)
- **인과가 아니라 조기 신호**로만 해석한다

## Step 4: 지표 정의 검증
각 지표에 대해 확인한다:
- 분자가 무엇인가?
- 분모가 무엇인가? (고정되어 있는가?)
- 측정 시점이 언제인가?

## 출력 형식
```
North Star: 완주율 (분자: 완주자 수 / 분모: 등록자 수)
Supporting KPI:
  - Funnel: [단계별 지표]
  - Retention: [주차별 지표]
Guardrail: [지표명 + 기준선]
Leading Indicator: [지표명] (조기 신호, 인과 아님)
갭: [있으면 목록, 없으면 "없음"]
```

## 다음 단계

- 지표 정의 완료 후 설계로 넘어가려면 → `experiment-design`
- 이미 설계 중이고 지표 재확인이 필요했다면 → 다시 `experiment-design`으로 복귀
