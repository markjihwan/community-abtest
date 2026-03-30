#!/usr/bin/env python3
"""
층화 분석 가능 여부 확인 — 셀당 최소 표본 크기 검사
treatment × strata 교차표 생성 및 분석 방법 추천

Usage:
    python stratification_check.py --csv data.csv --treatment treatment_flag --strata prior_exp cohort_size_bucket
    python stratification_check.py --csv data.csv --treatment treatment_flag --strata prior_exp
"""

import argparse
import csv
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")
from collections import defaultdict
from itertools import product
from typing import List, Dict, Tuple


MIN_CELL_SIZE = 20  # 층화 분석 셀당 최소 권고 인원


def load_csv(filepath: str) -> List[Dict[str, str]]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_crosstab(
    rows: List[Dict],
    treatment_col: str,
    strata_cols: List[str],
) -> Dict[Tuple, Dict[str, int]]:
    """treatment × strata 교차표 생성."""
    counts: Dict[Tuple, Dict[str, int]] = defaultdict(lambda: {"treatment": 0, "control": 0})

    for row in rows:
        t_val = row.get(treatment_col, "").strip()
        strata_key = tuple(row.get(c, "?").strip() for c in strata_cols)

        if t_val in ("1", "True", "true"):
            counts[strata_key]["treatment"] += 1
        elif t_val in ("0", "False", "false"):
            counts[strata_key]["control"] += 1

    return counts


def run(filepath: str, treatment_col: str, strata_cols: List[str]) -> None:
    rows = load_csv(filepath)
    if not rows:
        print("데이터 없음", file=sys.stderr)
        sys.exit(1)

    crosstab = build_crosstab(rows, treatment_col, strata_cols)

    n_treatment = sum(v["treatment"] for v in crosstab.values())
    n_control = sum(v["control"] for v in crosstab.values())

    print(f"\n=== 층화 분석 가능 여부 검사 ===")
    print(f"  Treatment N: {n_treatment}, Control N: {n_control}")
    print(f"  층화 변수: {', '.join(strata_cols)}")
    print(f"  셀 수: {len(crosstab)}")
    print(f"  최소 셀 크기 기준: {MIN_CELL_SIZE}명/셀\n")

    col_width = max(30, sum(len(c) + 3 for c in strata_cols))
    header = f"  {'층 (strata)':<{col_width}} {'Treatment':>12} {'Control':>10}  판단"
    print(header)
    print("  " + "-" * (col_width + 30))

    small_cells = []
    for strata_key, counts in sorted(crosstab.items()):
        label = " / ".join(f"{k}={v}" for k, v in zip(strata_cols, strata_key))
        t = counts["treatment"]
        c = counts["control"]
        ok = t >= MIN_CELL_SIZE and c >= MIN_CELL_SIZE
        flag = "✅" if ok else "❌ 셀 부족"
        print(f"  {label:<{col_width}} {t:>12} {c:>10}  {flag}")
        if not ok:
            small_cells.append((label, t, c))

    print()

    if not small_cells:
        print("  ✅ 모든 셀 충분 — 층화 분석 가능")
        print("     → 각 층별 완주율 비교 후 가중 평균으로 전체 효과 추정")
    else:
        print(f"  ❌ {len(small_cells)}개 셀 부족 → 층화 분석 어려움")
        print()
        print("  권장 대안:")
        print("    1. 공변량 보정 로지스틱 회귀 (표본 부족 시 기본 선택)")
        print("    2. 층화 변수 단순화 (세분류 → 대분류로 병합)")
        print("    3. PSM (사후 업그레이드, 표본 100명+ 이상 확보 시)")
        print()
        print("  ⚠️  표본이 전반적으로 부족하면 탐색 실험으로 재분류 고려 (CLAUDE.md 원칙 #4)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="층화 분석 가능 여부 검사")
    parser.add_argument("--csv", required=True, help="입력 CSV 파일 경로")
    parser.add_argument("--treatment", default="treatment_flag", help="treatment 컬럼명")
    parser.add_argument("--strata", nargs="+", required=True, help="층화 변수 컬럼명 (복수 가능)")
    args = parser.parse_args()

    run(filepath=args.csv, treatment_col=args.treatment, strata_cols=args.strata)
