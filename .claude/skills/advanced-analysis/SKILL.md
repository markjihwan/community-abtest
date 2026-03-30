---
name: advanced-analysis
description: 고급 통계/실험 방법을 적용한다.
  "CUPED 써야 해?", "ratio metric 어떻게 다뤄", "여러 지표 동시에 보면 문제 있어?",
  "중간에 결과 봤는데 괜찮아?", "분산 줄이는 방법 있어?",
  "sequential testing 쓰면 돼?" 등을 요청할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `05_ADVANCED_METHODS.md` — ratio metrics, multiple testing, variance reduction, sequential testing

## Step 2: 원칙 확인
고급 방법 적용 전에 반드시 상기한다:
> **고급 방법은 기본 설계 문제를 고쳐주지 않는다.**
> 실험 설계 자체에 문제가 있으면 고급 방법을 써도 결과를 신뢰할 수 없다.

## Step 3: 갭 점검 (Syneidesis)
적용 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 기본 설계(MDE, 표본, stopping rule)가 먼저 확정되었는가?
- `[Gap:Procedural]` 고급 방법이 이 상황에 실제로 필요한가?
- `[Gap:Consideration]` 방법 적용 후 해석이 더 복잡해지지는 않는가?

## Step 4: 상황별 방법 선택

### Ratio Metrics
- 사용 시점: 분자/분모가 둘 다 변할 수 있는 지표 (예: 세션당 완주율)
- 핵심 원칙: numerator와 denominator를 **같이 저장**해야 함
- 분석: delta method 또는 bootstrap으로 분산 추정

### Multiple Testing
- 사용 시점: 지표를 여러 개 동시에 검정할 때
- 핵심 원칙: **family 정의가 핵심** — 어떤 지표들을 한 family로 볼 것인가?
- 보정 방법: Bonferroni (보수적), BH (FDR 통제, 탐색적 실험에 적합)

### Variance Reduction (CUPED)
- 사용 시점: 표본이 부족하거나 효과 크기가 작을 때 검출력 높이기
- 핵심: pre-experiment 공변량으로 estimator의 standard error를 낮춤
- 조건: pre-experiment 데이터가 있어야 함 (이전 기수 데이터)

### Sequential Testing
- 사용 시점: 실험 중간에 결과를 봐야 하는 상황 (peeking 현실 수용)
- 핵심: peeking을 통계 규칙 안으로 가져오는 방법
- 조건: 사전에 sequential 방식으로 설계되어야 함 (사후 적용 불가)
- 주의: experiment-decision Skill의 보조 수단으로만 사용

## 출력 형식
```
적용 방법: [ratio metrics / multiple testing / CUPED / sequential]
적용 이유: [한 줄]
전제 조건 충족 여부: [O/X + 이유]
갭: [있으면 목록, 없으면 "없음"]
적용 가능 여부: [가능 / 불가 - 이유]
결과 해석 시 주의사항: [있으면 명시]
```

## 다음 단계

- 분석 완료 후 → `experiment-decision`으로 최종 판정
