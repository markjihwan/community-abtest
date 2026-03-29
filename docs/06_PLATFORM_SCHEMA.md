# 06 Platform Schema

## Purpose

이 문서는 실험 플랫폼을 데이터 구조로 어떻게 담을지 정리한 문서다.

## Covers

- experiment, variant, assignment, event, metric snapshot, result 구조
- data quality, decision log, learning note
- statistical columns와 metadata

## Read These

- [`DATA_SCHEMA.md`](archive/DATA_SCHEMA.md)
- [`STATISTICAL_COLUMNS.md`](archive/STATISTICAL_COLUMNS.md)

## Key Takeaways

- 원천 이벤트와 집계 테이블을 분리한다.
- 사람과 기수 참여를 분리한다.
- metric 정의와 통계 컬럼을 메타데이터로 남긴다.
- 결과값뿐 아니라 품질과 결정도 저장한다.
