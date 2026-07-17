#!/usr/bin/env python3
"""두 비율 비교 A/B 표본 크기 계산 (그룹당 n).
Playbook 3-3 연동. 의존성: 표준 라이브러리만 (statistics.NormalDist).

사용:
  python3 calc_sample_size.py --baseline 0.20 --mde 0.05
  python3 calc_sample_size.py            # 시나리오 그리드 출력
"""
import argparse, math
from statistics import NormalDist

def n_per_group(p1, mde, alpha=0.05, power=0.8, two_sided=True):
    p2 = p1 + mde
    pbar = (p1 + p2) / 2
    z_a = NormalDist().inv_cdf(1 - alpha / (2 if two_sided else 1))
    z_b = NormalDist().inv_cdf(power)
    num = (z_a * math.sqrt(2 * pbar * (1 - pbar)) +
           z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (mde ** 2))

def classify(n, traffic_per_arm):
    if n <= traffic_per_arm and n >= 30:
        return "결정 실험 가능"
    if n > traffic_per_arm:
        return f"탐색 실험(필요 n={n} > 가용 {traffic_per_arm})"
    return "탐색(그룹당 n<30)"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", type=float)
    ap.add_argument("--mde", type=float)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--mau", type=int, default=500, help="가용 모수(노출). 절반이 그룹당")
    a = ap.parse_args()
    arm = a.mau // 2
    if a.baseline and a.mde:
        n = n_per_group(a.baseline, a.mde, a.alpha, a.power)
        print(f"baseline={a.baseline:.0%} mde=+{a.mde:.0%} → 그룹당 n={n} | 그룹당 가용={arm} → {classify(n, arm)}")
    else:
        print(f"# 시나리오 그리드 (alpha={a.alpha}, power={a.power}, 가용 MAU={a.mau} → 그룹당 {arm})")
        print(f"{'baseline':>9} {'MDE':>6} {'n/그룹':>8}  분류")
        for p1 in (0.15, 0.20, 0.25):
            for mde in (0.03, 0.05, 0.08):
                n = n_per_group(p1, mde, a.alpha, a.power)
                print(f"{p1:>8.0%} {('+'+format(mde,'.0%')):>6} {n:>8}  {classify(n, arm)}")
