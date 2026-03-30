---
name: experiment-design
description: 커뮤니티/러닝 실험을 설계한다.
  사용자가 "실험 설계", "AB 테스트 계획", "기수 비교 어떻게 해",
  "MDE 얼마로 잡아야 해", "샘플 사이즈 계산" 등을 요청할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `01_FOUNDATIONS.md` — 실험 철학, 통계 기초, test design

## Step 2: 실험 유형 확인
사용자에게 먼저 확인한다:
- randomized A/B test인가, cohort 기반 비교인가?
- 기수(코호트) 단위로 배정되는가, 개인 단위인가?

cohort 기반이면: 선택 편향, 시간 효과 가능성을 명시적으로 언급한다.

## Step 3: 갭 점검 (Syneidesis)
설계 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 검증되지 않은 가정 (예: 기수 간 동질성)
- `[Gap:Procedural]` 빠진 단계 (예: baseline 데이터 확보 여부)
- `[Gap:Consideration]` 외부 요인 (예: 시즌, 커리큘럼 변경)

갭이 있으면 설계 전에 사용자에게 알리고 확인을 받는다.

## Step 4: 설계 확정
다음 순서로 확정한다:
1. **North Star Metric** — 완주율을 기본으로, 변경 시 이유 명시
2. **MDE** — 실질적으로 의미있는 최소 효과 크기
3. **표본 크기** — 기수당 인원 × 기수 수
4. **실험 기간** — 기수 단위로 몇 기수?
5. **Stopping rule** — 언제 멈출 것인가

## Step 5: 표본 판단
- 표본이 충분하면: 결정 실험으로 진행
- 표본이 부족하면: **탐색 실험**으로 분류하고 결론 한계를 명시

## 출력 형식
```
실험 유형: [randomized / cohort 기반]
North Star: [지표명]
MDE: [%]
표본: [기수당 N명 × M기수]
기간: [M기수]
Stopping rule: [조건]
분류: [결정 실험 / 탐색 실험]
갭: [있으면 목록, 없으면 "없음"]
```

## 다음 단계

설계 완료 후:
- 실험 신뢰도가 의심된다면 → `validity-check`
- 지표 정의가 흔들린다면 → `metrics-definition`
- 분석 방법(층화, CUPED 등)이 확정되지 않았다면 → `knowledge-audit`
- 위 항목이 모두 해소됐다면 → `experiment-register`로 등록
