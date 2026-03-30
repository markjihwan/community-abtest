# CLAUDE.md — ABTest Experiment Platform

## 이 프로젝트가 무엇인가

커뮤니티/러닝 프로그램(가짜연구소) 운영 환경에서 실험을 설계하고 해석하기 위한 플랫폼이다.

**핵심 전제: 이 프로젝트는 randomized A/B test 환경이 아니다.**
운영 단위가 기수(cohort) 중심이고, 제품 수정이 어렵고, 참여자가 자기선택으로 집단에 들어온다.
따라서 모든 실험은 **cohort 기반 quasi-experiment**로 설계하고 해석한다.

---

## 판단 원칙 (흔들리지 말 것)

1. **Guardrail이 최우선이다.** Bayesian 결과나 p-value가 아무리 좋아도, guardrail 지표가 훼손되면 ship하지 않는다.
2. **North Star는 완주율이다.** 변경 시 반드시 이유를 명시해야 한다.
3. **p-value 단독으로 결론 내리지 않는다.** Bayesian 해석을 우선하고, p-value는 참고용이다.
4. **표본이 부족하면 탐색 실험으로 분류한다.** 결정 실험으로 다루지 않는다.
5. **결론은 반드시 명시한다.** ship / hold / rollback / need_more_data 중 하나로.

---

## Skills 구조

이 레포는 Claude Code Skills로 워크플로우가 구성되어 있다. 사용자 요청에 따라 아래 Skills가 자동으로 발동된다.

| Skill | 언제 쓰나 |
|---|---|
| `experiment-register` | 실험 시작 전 요건 점검 |
| `metrics-definition` | 지표 정의 및 우선순위 확정 |
| `experiment-design` | 실험 설계 (MDE, 표본, stopping rule) |
| `validity-check` | SRM, peeking, network effect 등 타당도 점검 |
| `knowledge-audit` | 기존 지식 검증 또는 새 방법론 해석 |
| `experiment-decision` | 결과 해석 및 ship/hold/rollback 판정 |
| `advanced-analysis` | CUPED, sequential testing, ratio metrics |

**Skills 흐름:**
```
experiment-register → experiment-design → validity-check → [실험] → experiment-decision
```

---

## MCP 설정

`docs/` 폴더가 `abtest-docs` MCP 서버로 마운트되어 있다.
Skills에서 문서를 읽을 때 `mcp__abtest-docs__read_file`로 호출한다.

---

## 갭 추적 원칙 (Syneidesis)

모든 분석에서 결론 전에 반드시 점검한다:
- `[Gap:Assumption]` — 검증하지 않은 가정
- `[Gap:Procedural]` — 빠진 분석 단계
- `[Gap:Consideration]` — 고려하지 않은 외부 요인

갭이 있으면 결론 전에 사용자에게 먼저 알린다.

---

## 실험 이력

실험 등록서는 `experiments/` 폴더에 저장한다.
새 실험은 `experiments/TEMPLATE.md`를 복사해서 시작한다.

진행 중인 실험:
- `experiments/12ki_w7_magical_week.md` — 12기 W7 Magical Week 준실험 (Decision: 2026-07)
