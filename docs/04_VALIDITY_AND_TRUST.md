# 04 Validity and Trust

## Purpose

이 문서는 실험이 왜 조용히 거짓말할 수 있는지, 그리고 어떤 상황에서 해석 전제가 깨지는지를 정리한 문서다.

## Covers

- peeking, optional stopping, multiple looks
- SRM, instrumentation bugs, event tracking issues
- metric churn, seasonality, environment changes
- novelty, primacy, habituation
- network effects, cluster randomization, switchback

## Read These

- [`PITFALLS_AND_DATA_QUALITY.md`](PITFALLS_AND_DATA_QUALITY.md)
- [`NOVELTY_AND_NETWORK_EFFECTS.md`](NOVELTY_AND_NETWORK_EFFECTS.md)
- [`SEQUENTIAL_TESTING.md`](SEQUENTIAL_TESTING.md) — peeking 문제와 always-valid 해법

## Key Takeaways

- uplift보다 먼저 품질을 본다.
- SRM은 작은 경고가 아니라 신뢰성 경보다.
- 결과를 중간에 여러 번 보면 false positive rate가 올라간다.
- short-term uplift와 long-term value를 구분한다.
- interference가 있으면 unit과 design부터 다시 본다.
