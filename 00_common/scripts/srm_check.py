#!/usr/bin/env python3
"""SRM(Sample Ratio Mismatch) 카이제곱 점검.
배정 비율이 기대(기본 50:50)에서 유의하게 벗어났는지 확인.
의존성: 표준 라이브러리만.

사용:
  python3 srm_check.py --control 5120 --treatment 4880
  python3 srm_check.py --control 5300 --treatment 4700 --ratio 0.5
"""
import argparse, math
from statistics import NormalDist

def chi_square_p(obs, exp):
    chi2 = sum((o - e) ** 2 / e for o, e in zip(obs, exp))
    # df=1 → p = 2*(1-Phi(sqrt(chi2)))
    p = 2 * (1 - NormalDist().cdf(math.sqrt(chi2)))
    return chi2, p

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", type=int, required=True)
    ap.add_argument("--treatment", type=int, required=True)
    ap.add_argument("--ratio", type=float, default=0.5, help="control 기대 비율")
    ap.add_argument("--alpha", type=float, default=0.001, help="SRM은 보수적으로 0.001 권장")
    a = ap.parse_args()
    n = a.control + a.treatment
    exp = [n * a.ratio, n * (1 - a.ratio)]
    chi2, p = chi_square_p([a.control, a.treatment], exp)
    actual = a.control / n
    flag = "🚫 SRM 의심 — 실험 중단·배정 점검" if p < a.alpha else "✅ 정상"
    print(f"control={a.control} treatment={a.treatment} (실제 {actual:.1%}:{1-actual:.1%})")
    print(f"chi2={chi2:.3f}  p={p:.4g}  (alpha={a.alpha}) → {flag}")
