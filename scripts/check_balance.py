#!/usr/bin/env python3
"""
공변량 균형 검사 — SMD (Standardized Mean Difference) 계산
treatment / control 그룹 간 사전 특성 비교

Usage:
    python check_balance.py --csv data.csv --treatment treatment_flag
    echo '{"prior_exp":[0,1,0,1],"attend":[3,4,2,5]}' | python check_balance.py --json --treatment-col idx

Input CSV 형식:
    treatment_flag, prior_cohort_experience_flag, attendance_count_pre, assignment_submit_count_pre
    1, 0, 3, 2
    0, 1, 5, 4
    ...
"""

import argparse
import csv
import json
import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from typing import List


def smd(group1: List[float], group2: List[float]) -> float:
    """
    Standardized Mean Difference.
    pooled SD 기준 (Austin 2009 방식).
    """
    n1, n2 = len(group1), len(group2)
    if n1 < 2 or n2 < 2:
        return float("nan")

    mean1 = sum(group1) / n1
    mean2 = sum(group2) / n2

    var1 = sum((x - mean1) ** 2 for x in group1) / (n1 - 1)
    var2 = sum((x - mean2) ** 2 for x in group2) / (n2 - 1)

    pooled_sd = math.sqrt((var1 + var2) / 2)
    if pooled_sd == 0:
        return 0.0

    return (mean1 - mean2) / pooled_sd


def smd_binary(p1: float, p2: float) -> float:
    """이진 변수용 SMD."""
    denom = math.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
    if denom == 0:
        return 0.0
    return (p1 - p2) / denom


def assess(val: float) -> str:
    abs_val = abs(val)
    if abs_val <= 0.1:
        return "✅ 균형 (≤0.1)"
    elif abs_val <= 0.2:
        return "⚠️  경계 (0.1–0.2)"
    else:
        return "❌ 불균형 (>0.2) — 보정 필요"


def run_from_csv(filepath: str, treatment_col: str) -> None:
    rows = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        print("데이터 없음", file=sys.stderr)
        sys.exit(1)

    covariates = [c for c in rows[0].keys() if c != treatment_col]
    treatment_group = [r for r in rows if r[treatment_col].strip() in ("1", "True", "true")]
    control_group = [r for r in rows if r[treatment_col].strip() in ("0", "False", "false")]

    print(f"\n=== 공변량 균형 검사 ===")
    print(f"  Treatment N: {len(treatment_group)}, Control N: {len(control_group)}")
    print(f"\n  {'공변량':<35} {'Treatment 평균':>15} {'Control 평균':>15} {'SMD':>8}  판단")
    print("  " + "-" * 85)

    imbalanced = []
    for cov in covariates:
        try:
            g1 = [float(r[cov]) for r in treatment_group]
            g2 = [float(r[cov]) for r in control_group]
        except (ValueError, KeyError):
            continue

        m1 = sum(g1) / len(g1) if g1 else float("nan")
        m2 = sum(g2) / len(g2) if g2 else float("nan")

        # 이진 변수 판단 (값이 0/1만 있으면)
        unique_vals = set(g1 + g2)
        if unique_vals <= {0.0, 1.0}:
            val = smd_binary(m1, m2)
        else:
            val = smd(g1, g2)

        label = assess(val)
        print(f"  {cov:<35} {m1:>15.3f} {m2:>15.3f} {val:>8.3f}  {label}")

        if abs(val) > 0.1:
            imbalanced.append(cov)

    print()
    if imbalanced:
        print(f"  ⚠️  불균형 공변량: {', '.join(imbalanced)}")
        print("     → 공변량 보정 로지스틱 회귀 또는 PSM 고려")
    else:
        print("  ✅ 모든 공변량 SMD ≤ 0.1 — 층화 분석 가능")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="공변량 균형 검사 (SMD)")
    parser.add_argument("--csv", help="입력 CSV 파일 경로")
    parser.add_argument("--treatment", default="treatment_flag", help="treatment 컬럼명 (default: treatment_flag)")
    args = parser.parse_args()

    if args.csv:
        run_from_csv(args.csv, args.treatment)
    else:
        parser.print_help()
        print("\n사용 예:\n  python check_balance.py --csv data.csv --treatment treatment_flag")
