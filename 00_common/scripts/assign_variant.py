#!/usr/bin/env python3
"""결정적 sticky 배정 (sidebar-nav-v1).
hash(user_id + experiment_id) % 100 < bucket → treatment. 같은 입력 → 항상 같은 결과(sticky).
의존성: 표준 라이브러리만. 운영 구현(F1)의 레퍼런스 + self-test.

사용:
  python3 assign_variant.py --user 230f3a47 --experiment sidebar-nav-v1
  python3 assign_variant.py --selftest 100000
"""
import argparse, hashlib

def assign(uid, experiment_id, ratio=0.5):
    h = hashlib.sha256(f"{experiment_id}:{uid}".encode()).hexdigest()
    bucket = int(h[:8], 16) % 100          # 0..99
    return "treatment" if bucket < ratio * 100 else "control"

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--user")
    ap.add_argument("--experiment", default="sidebar-nav-v1")
    ap.add_argument("--ratio", type=float, default=0.5)
    ap.add_argument("--selftest", type=int)
    a = ap.parse_args()
    if a.selftest:
        from collections import Counter
        c = Counter(assign(f"user_{i}", a.experiment, a.ratio) for i in range(a.selftest))
        t = c["treatment"]; n = a.selftest
        # stickiness 확인: 같은 id 재배정 일치
        sticky_ok = all(assign(f"user_{i}", a.experiment) == assign(f"user_{i}", a.experiment) for i in range(1000))
        print(f"selftest N={n}: treatment={t} ({t/n:.2%}) control={c['control']} ({c['control']/n:.2%})")
        print(f"sticky(재배정 일치)={sticky_ok}")
    elif a.user:
        print(assign(a.user, a.experiment, a.ratio))
    else:
        ap.error("--user 또는 --selftest 필요")
