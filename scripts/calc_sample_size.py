#!/usr/bin/env python3
"""
표본 크기 계산 — completion rate (완주율) 기반 two-proportion z-test
cohort-based quasi-experiment 환경용

Usage:
    python calc_sample_size.py --baseline 0.6 --mde 0.1
    python calc_sample_size.py --baseline 0.6 --mde 0.1 --alpha 0.05 --power 0.8
"""

import argparse
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def calc_sample_size(
    baseline: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.8,
    two_sided: bool = True,
) -> dict:
    """
    Two-proportion z-test 기반 표본 크기 계산.

    Args:
        baseline: 대조군 완주율 (예: 0.6)
        mde: 감지하려는 최소 효과 크기 (절대값, 예: 0.1 → 60% → 70%)
        alpha: 유의수준 (default 0.05)
        power: 검정력 (default 0.8)
        two_sided: 양측검정 여부

    Returns:
        dict with n_per_group, n_total, effect_size_cohen_h
    """
    p1 = baseline
    p2 = baseline + mde

    # Cohen's h
    h = 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))

    # z-scores
    if two_sided:
        z_alpha = _z_score(1 - alpha / 2)
    else:
        z_alpha = _z_score(1 - alpha)
    z_beta = _z_score(power)

    n = ((z_alpha + z_beta) / h) ** 2
    n_ceil = math.ceil(n)

    return {
        "baseline": p1,
        "treatment_expected": p2,
        "mde_absolute": mde,
        "alpha": alpha,
        "power": power,
        "two_sided": two_sided,
        "effect_size_cohen_h": round(abs(h), 4),
        "n_per_group": n_ceil,
        "n_total": n_ceil * 2,
    }


def _z_score(p: float) -> float:
    """Inverse normal CDF (rational approximation)."""
    # Abramowitz & Stegun approximation
    if p <= 0 or p >= 1:
        raise ValueError(f"p must be in (0, 1), got {p}")
    c = [2.515517, 0.802853, 0.010328]
    d = [1.432788, 0.189269, 0.001308]
    if p < 0.5:
        t = math.sqrt(-2 * math.log(p))
        sign = -1
    else:
        t = math.sqrt(-2 * math.log(1 - p))
        sign = 1
    num = c[0] + c[1] * t + c[2] * t**2
    den = 1 + d[0] * t + d[1] * t**2 + d[2] * t**3
    return sign * (t - num / den)


def print_result(result: dict) -> None:
    print("\n=== 표본 크기 계산 결과 ===")
    print(f"  기준 완주율 (대조군):   {result['baseline']:.1%}")
    print(f"  예상 완주율 (실험군):   {result['treatment_expected']:.1%}")
    print(f"  MDE (절대 차이):        {result['mde_absolute']:+.1%}")
    print(f"  Cohen's h:              {result['effect_size_cohen_h']}")
    print(f"  유의수준 (alpha):       {result['alpha']}")
    print(f"  검정력 (power):         {result['power']:.0%}")
    print(f"  양측검정:               {'예' if result['two_sided'] else '아니오'}")
    print(f"\n  그룹당 필요 표본:       {result['n_per_group']}명")
    print(f"  총 필요 표본:           {result['n_total']}명")

    n = result["n_per_group"]
    if n > 200:
        note = "⚠️  cohort 규모를 초과할 수 있음 — 탐색 실험으로 분류 고려"
    elif n > 100:
        note = "⚠️  경계 수준 — 표본 확보 가능 여부 확인 필요"
    else:
        note = "✅  cohort 규모 내 확보 가능성 있음"
    print(f"\n  판단: {note}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="완주율 기반 표본 크기 계산")
    parser.add_argument("--baseline", type=float, required=True, help="대조군 완주율 (예: 0.6)")
    parser.add_argument("--mde", type=float, required=True, help="최소 감지 효과 크기, 절대값 (예: 0.1)")
    parser.add_argument("--alpha", type=float, default=0.05, help="유의수준 (default: 0.05)")
    parser.add_argument("--power", type=float, default=0.8, help="검정력 (default: 0.8)")
    parser.add_argument("--one-sided", action="store_true", help="단측검정 사용")
    args = parser.parse_args()

    result = calc_sample_size(
        baseline=args.baseline,
        mde=args.mde,
        alpha=args.alpha,
        power=args.power,
        two_sided=not args.one_sided,
    )
    print_result(result)
