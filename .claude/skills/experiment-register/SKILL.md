---
name: experiment-register
description: 실험 등록과 승인 절차를 안내한다.
  "실험 어떻게 등록해", "승인 기준이 뭐야", "실험 시작 전에 뭐 해야 해",
  "데이터 수집 어떻게 해", "참여자한테 고지 해야 해?" 등을 요청할 때 사용한다.
---

# 워크플로우

## Step 1: 문서 로드
`mcp__abtest-docs__read_file`로 다음을 읽는다:
- `02_EXPERIMENT_POLICY.md` — 등록, 승인, 데이터/참여자/결과 정책

## Step 2: 갭 점검 (Syneidesis)
등록 전에 다음을 TodoWrite로 기록한다:
- `[Gap:Assumption]` 실험 단위(cohort)가 명확히 정의되어 있는가?
- `[Gap:Procedural]` 등록과 승인이 분리되어 있는가?
- `[Gap:Consideration]` 참여자 보호 조건이 충족되었는가?

## Step 3: 등록 요건 확인
다음 항목이 모두 갖춰져야 등록 가능하다:

### 필수 항목
- [ ] 실험 목적과 가설
- [ ] 실험 단위 (cohort 기수 명시)
- [ ] variant 정의 (control / treatment 각각)
- [ ] North Star Metric + Guardrail 지표
- [ ] MDE, 표본 크기, 기간
- [ ] Stopping rule

### 데이터 정책
- 필요한 데이터만 수집한다
- 접근 권한은 최소화한다
- 수집 항목과 보관 기간을 명시한다

### 참여자 보호
- 참여자 고지 방식을 명시한다
- 실험 성공 여부와 무관하게 보호 조건을 적용한다

## Step 4: 승인 기준 확인
등록과 승인은 분리한다:
- 등록 → 실험 담당자가 작성
- 승인 → 별도 검토자가 확인

승인 전에 실험을 시작하지 않는다.

## Step 5: 결과 기록 원칙
- 실험 성공 여부와 무관하게 결과를 기록한다
- 결론은 의사결정에 반영된 내용까지 기록한다

## 출력 형식
```
등록 체크리스트:
  - 가설: [O/X]
  - 실험 단위: [O/X]
  - variant 정의: [O/X]
  - 지표 (North Star + Guardrail): [O/X]
  - MDE/표본/기간: [O/X]
  - Stopping rule: [O/X]
  - 데이터 정책: [O/X]
  - 참여자 보호: [O/X]

갭: [있으면 목록, 없으면 "없음"]
등록 가능 여부: [가능 / 불가 - 이유]
```

## 다음 단계

등록 가능 판정 후:
- 지표가 아직 정의되지 않았다면 → `metrics-definition`
- 실험 설계로 넘어갈 준비가 됐다면 → `experiment-design`
