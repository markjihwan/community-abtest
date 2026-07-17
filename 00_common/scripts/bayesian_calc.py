#!/usr/bin/env python3
"""Bayesian A/B: P(Treatment > Control) (Beta-Binomial 사후, 몬테카를로).
Playbook 3-4 판단 기준 연동. 의존성: 표준 라이브러리만 (seed 고정 → 재현 가능).

사용:
  python3 bayesian_calc.py --t-success 120 --t-total 1000 --c-success 95 --c-total 1000
"""
import argparse, random

def p_treat_gt_control(ts, tt, cs, ct, draws=200000, seed=42):
    random.seed(seed)
    a_t, b_t = ts + 1, tt - ts + 1
    a_c, b_c = cs + 1, ct - cs + 1
    wins = 0
    for _ in range(draws):
        if random.betavariate(a_t, b_t) > random.betavariate(a_c, b_c):
            wins += 1
    return wins / draws

def verdict(p):
    if p >= 0.95: return "ship 고려 가능 (Guardrail 확인 후)"
    if p >= 0.90: return "Guardrail 확인 후 판단"
    if p >= 0.80: return "need_more_data / 탐색 재분류"
    return "hold / rollback 검토"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--t-success", type=int, required=True)
    ap.add_argument("--t-total", type=int, required=True)
    ap.add_argument("--c-success", type=int, required=True)
    ap.add_argument("--c-total", type=int, required=True)
    ap.add_argument("--draws", type=int, default=200000)
    a = ap.parse_args()
    ct = a.c_success / a.c_total
    tt = a.t_success / a.t_total
    p = p_treat_gt_control(a.t_success, a.t_total, a.c_success, a.c_total, a.draws)
    print(f"control={ct:.2%}  treatment={tt:.2%}  Δ={tt-ct:+.2%}p")
    print(f"P(T>C)={p:.1%} → {verdict(p)}")
