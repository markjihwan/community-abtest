#!/usr/bin/env python3
"""
Bayesian 완주율 비교 — Beta-Binomial 모델
P(treatment > control) 계산 + credible interval

Usage:
    python bayesian_calc.py --t-success 42 --t-total 60 --c-success 35 --c-total 58
    python bayesian_calc.py --t-success 42 --t-total 60 --c-success 35 --c-total 58 --samples 100000
"""

import argparse
import math
import random
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def beta_sample(alpha: float, beta: float, n: int, seed: int = 42) -> list:
    """Beta 분포에서 n개 샘플 추출 (표준 라이브러리만 사용)."""
    rng = random.Random(seed)
    samples = []
    for _ in range(n):
        # Gamma 샘플로 Beta 생성
        g1 = _gamma_sample(rng, alpha)
        g2 = _gamma_sample(rng, beta)
        samples.append(g1 / (g1 + g2))
    return samples


def _gamma_sample(rng: random.Random, shape: float) -> float:
    """Marsaglia-Tsang's method for Gamma sampling."""
    if shape < 1:
        return _gamma_sample(rng, shape + 1) * (rng.random() ** (1 / shape))
    d = shape - 1 / 3
    c = 1 / math.sqrt(9 * d)
    while True:
        x = rng.gauss(0, 1)
        v = (1 + c * x) ** 3
        if v <= 0:
            continue
        u = rng.random()
        if u < 1 - 0.0331 * (x**2) ** 2:
            return d * v
        if math.log(u) < 0.5 * x**2 + d * (1 - v + math.log(v)):
            return d * v


def credible_interval(samples: list, level: float = 0.95) -> tuple:
    s = sorted(samples)
    n = len(s)
    lo = s[int(n * (1 - level) / 2)]
    hi = s[int(n * (1 - (1 - level) / 2))]
    return lo, hi


def run(
    t_success: int,
    t_total: int,
    c_success: int,
    c_total: int,
    prior_alpha: float = 1.0,
    prior_beta: float = 1.0,
    n_samples: int = 50000,
    rope_margin: float = 0.0,
) -> None:
    # Posterior: Beta(alpha + successes, beta + failures)
    t_alpha = prior_alpha + t_success
    t_beta_p = prior_beta + (t_total - t_success)
    c_alpha = prior_alpha + c_success
    c_beta_p = prior_beta + (c_total - c_success)

    t_samples = beta_sample(t_alpha, t_beta_p, n_samples, seed=42)
    c_samples = beta_sample(c_alpha, c_beta_p, n_samples, seed=99)

    t_rate = t_success / t_total
    c_rate = c_success / c_total

    prob_t_gt_c = sum(1 for t, c in zip(t_samples, c_samples) if t > c + rope_margin) / n_samples
    prob_c_gt_t = sum(1 for t, c in zip(t_samples, c_samples) if c > t + rope_margin) / n_samples
    prob_rope = 1 - prob_t_gt_c - prob_c_gt_t

    diff_samples = [t - c for t, c in zip(t_samples, c_samples)]
    diff_mean = sum(diff_samples) / len(diff_samples)
    ci_lo, ci_hi = credible_interval(diff_samples)

    t_ci_lo, t_ci_hi = credible_interval(t_samples)
    c_ci_lo, c_ci_hi = credible_interval(c_samples)

    print("\n=== Bayesian 완주율 비교 ===")
    print(f"  사전 분포: Beta({prior_alpha}, {prior_beta}) (무정보 균등 사전)")
    print()
    print(f"  {'':10} {'완주':>8} {'전체':>8} {'관측 완주율':>12} {'95% CI':>22}")
    print("  " + "-" * 65)
    print(f"  {'Treatment':<10} {t_success:>8} {t_total:>8} {t_rate:>12.1%}   [{t_ci_lo:.3f}, {t_ci_hi:.3f}]")
    print(f"  {'Control':<10} {c_success:>8} {c_total:>8} {c_rate:>12.1%}   [{c_ci_lo:.3f}, {c_ci_hi:.3f}]")
    print()
    print(f"  차이 (T - C):     평균 {diff_mean:+.3f}  95% CI [{ci_lo:+.3f}, {ci_hi:+.3f}]")
    print()
    print(f"  P(Treatment > Control): {prob_t_gt_c:.1%}")
    print(f"  P(Control > Treatment): {prob_c_gt_t:.1%}")
    if rope_margin > 0:
        print(f"  P(실질 동등, ±{rope_margin}):     {prob_rope:.1%}")
    print()

    # 판단
    if prob_t_gt_c >= 0.95:
        verdict = "✅ Treatment 우위 확실 (≥95%) — ship 고려 가능"
    elif prob_t_gt_c >= 0.90:
        verdict = "⚠️  Treatment 우위 가능성 높음 (90–95%) — Guardrail 확인 후 판단"
    elif prob_t_gt_c >= 0.80:
        verdict = "⚠️  불확실 (80–90%) — need_more_data 또는 탐색 실험으로 분류"
    elif prob_c_gt_t >= 0.90:
        verdict = "❌ Control 우위 — hold / rollback 고려"
    else:
        verdict = "⚠️  결론 불충분 — need_more_data"

    print(f"  판단: {verdict}")
    print()
    print("  ※ Guardrail 지표 상태를 반드시 함께 확인할 것 (CLAUDE.md 원칙 #1)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bayesian 완주율 비교")
    parser.add_argument("--t-success", type=int, required=True, help="Treatment 완주자 수")
    parser.add_argument("--t-total", type=int, required=True, help="Treatment 전체 참여자 수")
    parser.add_argument("--c-success", type=int, required=True, help="Control 완주자 수")
    parser.add_argument("--c-total", type=int, required=True, help="Control 전체 참여자 수")
    parser.add_argument("--samples", type=int, default=50000, help="MC 샘플 수 (default: 50000)")
    parser.add_argument("--rope", type=float, default=0.0, help="ROPE 마진 (예: 0.02 → ±2%p 동등 구간)")
    parser.add_argument("--prior-alpha", type=float, default=1.0, help="사전 분포 alpha (default: 1)")
    parser.add_argument("--prior-beta", type=float, default=1.0, help="사전 분포 beta (default: 1)")
    args = parser.parse_args()

    run(
        t_success=args.t_success,
        t_total=args.t_total,
        c_success=args.c_success,
        c_total=args.c_total,
        prior_alpha=args.prior_alpha,
        prior_beta=args.prior_beta,
        n_samples=args.samples,
        rope_margin=args.rope,
    )
