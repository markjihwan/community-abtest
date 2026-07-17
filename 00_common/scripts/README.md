> **📄 요약 ·** 실험 통계 도구 4종(표본·SRM·Bayesian·배정) — 표준 라이브러리만, 두 실험 공용. 실행 검증됨.

# scripts/ — 실험 통계 도구 (표준 라이브러리만, 두 실험 공용)

Playbook(3-2~3-4)이 참조하는 분석 스크립트. 의존성 없음(python3 3.8+).

| 스크립트 | 용도 | 예시 |
|---|---|---|
| `calc_sample_size.py` | 두 비율 A/B 표본 크기·실험 분류 | `python3 calc_sample_size.py --baseline 0.20 --mde 0.05` |
| `srm_check.py` | SRM 카이제곱(배정 비율 이상) | `python3 srm_check.py --control 5040 --treatment 4960` |
| `bayesian_calc.py` | P(Treatment>Control) + 4-state 판정 | `python3 bayesian_calc.py --t-success 120 --t-total 1000 --c-success 95 --c-total 1000` |
| `assign_variant.py` | 결정적 sticky 배정(레퍼런스) | `python3 assign_variant.py --selftest 100000` |

검증된 출력(2026-06-22): 배정 50.02%·sticky=True · SRM 50.4:49.6→정상/54:46→차단 · Bayesian 12% vs 9.5%→P=96.4%.
사이드바 표본: MAU 500에선 전 시나리오 탐색 분류(필요 n 377~3397/그룹 > 250).
