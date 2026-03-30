# Claude Code Skills 활용 가이드
## — 커뮤니티 실험 플랫폼에 AI를 붙이는 법

---

## 왜 Skills를 만들었나

이 레포에는 A/B 테스트 지식이 잘 정리되어 있습니다. 하지만 문서만 있으면 Claude는 그냥 검색만 합니다.

**"guardrail보다 Bayesian 결과가 우선하지 않는다"** 같은 판단 기준은, 사용자가 "그런데 Bayesian으로는 유의한데?"라고 물을 때 Claude가 흔들리지 않으려면 워크플로우로 박혀 있어야 합니다.

Skills는 Claude Code에게 **"이 도구를 쓸 때 이렇게 생각하고 이렇게 행동해라"** 를 가르치는 겁니다. MCP가 도구라면, Skill은 그 도구를 쓰는 전문가의 판단력입니다.

---

## 구조

```
.claude/
  agents/
    abtest-analyst.md       ← "어떻게 행동할지" (원칙/경계)
  skills/
    experiment-register/    ← "무엇을 할지" (워크플로우)
    metrics-definition/
    experiment-design/
    validity-check/
    knowledge-audit/
    experiment-decision/
    advanced-analysis/
.mcp.json                   ← docs/ 폴더를 MCP로 마운트
```

**핵심 설계 원칙:**
- Agent에는 원칙과 경계만
- Skill에는 실제 워크플로우만
- 섞으면 지침이 충돌하거나 중복됨

---

## 시작하기

Node.js가 설치된 환경에서:

```bash
git clone <this-repo>
cd community-abtest
claude
```

MCP가 자동으로 `./docs`를 마운트합니다. 이후 자연어로 질문하면 Claude가 알아서 적절한 Skill을 발동합니다.

---

## Skills 전체 흐름

```
① 기획
  experiment-register → metrics-definition

② 설계 & 검증
  experiment-design → validity-check → knowledge-audit (필요 시)

③ 실험 실행

④ 결과 판단
  experiment-decision → advanced-analysis (need_more_data 시)
                      → ship / hold / rollback
```

---

## Skill별 사용법

### 1. `experiment-register` — 실험 등록 & 승인 절차

**언제:** 실험을 시작하기 전, 요건이 갖춰졌는지 확인할 때

**트리거 예시:**
```
"실험 시작 전에 뭐 해야 해?"
"승인 기준이 뭐야?"
"데이터 수집 어떻게 해?"
```

**하는 일:**
- 가설, 실험 단위, variant 정의, 지표, MDE/표본/기간, stopping rule 체크
- 데이터 정책 및 참여자 보호 조건 확인
- 등록 가능 여부 판정

**다음:** `metrics-definition` 또는 `experiment-design`

---

### 2. `metrics-definition` — 지표 정의 & 우선순위

**언제:** 어떤 지표를 볼지 정해야 할 때

**트리거 예시:**
```
"완주율 말고 뭐 봐야 해?"
"guardrail 지표가 뭔데?"
"KPI 뭐로 잡아야 해?"
```

**하는 일:**
- North Star(완주율) 고정
- Funnel / Retention / Guardrail / Leading Indicator 계층 정의
- 분자/분모 명시

**핵심 원칙:** Funnel과 Retention은 섞지 않는다. Leading indicator는 인과가 아니라 조기 신호로 해석한다.

**다음:** `experiment-design`

---

### 3. `experiment-design` — 실험 설계

**언제:** 실험을 어떻게 구성할지 설계할 때

**트리거 예시:**
```
"11기 vs 12기 완주율 비교하려는데 어떻게 해?"
"MDE 얼마로 잡아야 해?"
"샘플 사이즈 계산해줘"
```

**하는 일:**
1. randomized vs cohort 기반 먼저 확인
2. Gap 점검 (`[Gap:Assumption]`, `[Gap:Procedural]`, `[Gap:Consideration]`)
3. MDE → 표본 → 기간 → stopping rule 순서로 확정
4. 결정 실험 / 탐색 실험 분류

**다음:** `validity-check`

---

### 4. `validity-check` — 타당도 점검

**언제:** 실험의 신뢰도가 의심될 때

**트리거 예시:**
```
"SRM 의심돼"
"novelty effect 아닌가?"
"peeking 했어"
"이 실험 믿어도 돼?"
```

**체크 항목:**
- SRM (Sample Ratio Mismatch)
- Peeking
- Novelty Effect
- Network Effect / Spillover
- 선택 편향, 역사 효과, 성숙 효과

**판정:** 신뢰 가능 / 주의 필요 / 신뢰 불가

**다음:**
- 신뢰 가능 → `experiment-register`
- 주의/불가 → `experiment-design` 재검토

---

### 5. `knowledge-audit` — 지식 검증 (루프)

**언제:** 문서 내용이 맞는지 의심되거나, 새로운 방법론을 도입할지 판단할 때

**트리거 예시:**
```
"이 내용 맞아?"
"PSM vs 층화 분석 뭐가 나아?"
"새 논문 나왔는데 우리한테 적용 가능해?"
```

**핵심 구조 (autoresearch 루프):**
```
기준 먼저 정하기 → 단위별 테스트 → PASS/FAIL 명확히 → 반복
```

**Mode A (기존 지식 검증):** PASS / FAIL / CONDITIONAL
**Mode B (새 지식 해석):** ADOPT / REJECT / PARTIAL

"참고할 만하다"로 끝내지 않는다. 각 claim마다 판정을 내리고 후속 조치까지 명시한다.

---

### 6. `experiment-decision` — 결과 해석 & 판단

**언제:** 실험 결과가 나왔을 때

**트리거 예시:**
```
"결과 어떻게 봐?"
"이거 올려도 돼?"
"완주율 차이 해석해줘"
```

**순서:**
1. Guardrail 먼저 (훼손되면 다른 결과 무관하게 hold/rollback)
2. Bayesian 해석 (P(treatment > control))
3. p-value는 참고용만
4. 명시적 결론 4가지 중 하나

| 결론 | 조건 |
|---|---|
| **ship** | guardrail 안전 + North Star 개선 + 갭 없음 |
| **hold** | guardrail 경계선 or 표본 부족 |
| **rollback** | guardrail 훼손 |
| **need_more_data** | 방향은 있으나 불확실성 큼 |

---

### 7. `advanced-analysis` — 고급 분석

**언제:** need_more_data 판정 후, 또는 특수한 분석 상황

**트리거 예시:**
```
"CUPED 써야 해?"
"중간에 결과 봤는데 괜찮아?"
"여러 지표 동시에 보면 문제 있어?"
```

**주의:** 고급 방법은 기본 설계 문제를 고쳐주지 않는다. 설계가 잘못됐으면 먼저 `experiment-design`으로 돌아갈 것.

---

## Syneidesis 패턴 — 모든 Skill에 내장된 것

epistemic-protocols의 Syneidesis 철학을 코딩 컨벤션으로 구현한 것입니다.

모든 Skill은 결론 전에 **갭을 먼저 표면화**합니다:

```
[Gap:Assumption]     검증하지 않은 가정
[Gap:Procedural]     빠진 분석 단계
[Gap:Consideration]  고려하지 않은 외부 요인
```

갭이 하나라도 있으면 결론 전에 사용자에게 먼저 알립니다. 이게 없으면 Claude가 그럴 듯한 결론을 자신있게 내놓고 사용자가 흔들리는 상황이 생깁니다.

---

## 실제 적용 사례: 12기 W7 Magical Week

이 Skill들을 실제로 써서 만든 실험이 [`experiments/12ki_w7_magical_week.md`](../experiments/12ki_w7_magical_week.md)입니다.

**흐름 요약:**

```
1. experiment-design 발동
   → "cohort 기반이죠? 선택편향 가능성 있습니다"
   → [Gap:Assumption] 두 집단 동질성 미확인

2. knowledge-audit (루프)
   → PSM vs 층화 분석 검증
   → 200명 / 4셀 / 셀당 50명 → 층화 분석 ADOPT

3. 노출 설계 문제 발견
   → "비노출 = 이탈자 편향"
   → 전원 알림 발송으로 노출 보장

4. 분석 구조 확정
   → ITT (전원 200명) / ATT (미션 완료자) / 이탈 분석 3-way
```

**핵심 결정들:**
- PSM 대신 층화 분석 (현실적 구현 가능성)
- 접속 기반 노출 대신 능동적 전원 알림 발송
- participation_level: notified_only / visited / partial / full

---

## MCP 구조

```json
{
  "mcpServers": {
    "abtest-docs": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./docs"]
    }
  }
}
```

Skill이 문서를 읽을 때 `mcp__abtest-docs__read_file`로 호출합니다. 파일 경로가 Skill에 하드코딩되지 않으므로, docs 위치가 바뀌어도 `.mcp.json`만 수정하면 됩니다.

---

## 참고

- [epistemic-protocols](https://github.com/jongwony/epistemic-protocols) — Syneidesis, Analogia, Epharmoge 패턴
- [autoresearch](https://github.com/karpathy/autoresearch) — 루프 기반 검증 구조
