> **📄 요약 ·** 문서 이력·계보 대장 — 구조 개편 연대기, 폐기 경로 → 현재 경로 매핑, 문서별 유래. 옛 경로가 어딘가에 남아 있으면 이 문서의 매핑 표로 해석한다. 구조를 옮길 때마다 §1·§2에 추가.

# 📜 문서 이력 (HISTORY)

## 1. 구조 개편 연대기

| 시점 | 개편 | 내용 |
|---|---|---|
| ~2026-06 | 초기 산출물 | `~/Desktop/study/study_AI_AGENT/project/a/b test/output/`에 산출물 생성 (현재 `s12-mid-reflection-tracking-report.md` 1건 잔존 — 참조용, 이 프로젝트의 진실 원천 아님). |
| 2026-06-22 | 레이어 정리 | `projects/a:b test`에서 흩어진 문서를 넘버링 레이어 폴더(00~05)로 정리. 중복 `github.md` 삭제. |
| 2026-06-22 | **재배치(하이브리드)** | 1차 넘버링 레이어(00~04) 폐기 → **공통 `_common/` vs 실험전용 `experiments/<실험>/`** 구조로 전환. `query.md` → 실험별 `queries.md` 분리. `03_report` 리포트·`04_script` 공지 → `01_reflection/`. 데이터구조맵 → `_common/`. `05_memory/`만 잔존. |
| 2026-06-22 ~ 07-13 | analytics 축적 | 분석 노트·검토 리포트 6건이 `analytics/` 폴더에 쌓임 — INDEX 미등재 상태로 지도 밖에 존재. |
| 2026-07-13 | **analytics 해체** | 원칙(공통 vs 인스턴스)에 맞춰 6건 재배치, 사본 1건·빈 파일 1건 삭제, 폐기 경로 참조 갱신. 상세는 §3. |
| 2026-07-13 | **넘버링 + notes/** | 최상위 폴더 넘버링 재도입: `_common`→`00_common` · `experiments`→`01_experiments` · `ideas`→`02_ideas` · `05_memory`→`03_memory`. 실험별 실측/검토 노트 폴더 `01_experiments/<실험>/notes/` 신설, 노트 4건 이동. 전 문서 상대 링크 일괄 갱신 + 존재 검증. ⚠️ 문서에 나오는 플랫폼 레포(pseudo-lab 쪽)의 `experiments/` 폴더는 **이 프로젝트 폴더가 아니므로** 개명 대상 아님(platform.md·implementation-spec·jira-backlog의 "실험 등록서" 언급). |
| 2026-07-13 | **04_results 신설** | 실험 결과 보고서 레이어 추가 — `04_results/1차_준실험_중간결과.md`(1차 회고 노출 종료 중간결과: 퍼널·균형검사·DAU/MAU·Health Score·need_more_data 판정). 원자료·재현 쿼리는 `01_experiments/01_reflection/notes/round1-results.md`(1~3차 기입)에 유지, 보고서는 참조만(복제 금지). INDEX 트리·구조 원칙 표·진행 상태 동반 갱신 + 링크 존재 검증 완료. |

## 2. 폐기 경로 → 현재 경로 매핑

옛 문서 본문에 아래 경로가 나오면 오른쪽으로 읽는다. **왼쪽 경로들은 디스크에 더 이상 존재하지 않는다.**

### 2026-06-22 재배치분 (구 00~04 레이어)

| 폐기 경로 | 현재 경로 |
|---|---|
| `00_playbook/experiment-playbook.md` | `00_common/playbook.md` |
| `01_platform/platform-architecture.md` | `00_common/platform.md` |
| `02_experiments/s12-mid-reflection/experiment-spec.md` | `01_experiments/01_reflection/experiment-spec.md` |
| `02_experiments/s12-mid-reflection/analysis-plan.md` | `01_experiments/01_reflection/analysis-plan.md` |
| `02_experiments/s12-mid-reflection/data-definition.md` | `01_experiments/01_reflection/data-definition.md` |
| `query.md` (통합본) | 실험별 분리: `01_experiments/<실험>/queries.md` |
| `03_report/데이터구조_맵.md` | `00_common/data-structure-map.md` |
| `03_report/` 리포트 · `04_script/` 공지 | `01_experiments/01_reflection/report.md` · `announcement.md` |

### 2026-07-13 넘버링분 (당일 두 차례 개편 누적)

| 폐기 경로 | 현재 경로 |
|---|---|
| `_common/` | `00_common/` |
| `experiments/` | `01_experiments/` |
| `ideas/` | `02_ideas/` |
| `05_memory/` | `03_memory/` |
| `analytics/` (해체) | §3 참조 |

## 3. 2026-07-13 analytics 해체 매핑

| 구 위치 (`analytics/`) | 처리 | 현재 위치 | 판단 근거 |
|---|---|---|---|
| `실험_트래킹리포트.md` | 이동 | `01_experiments/01_reflection/notes/` | 회고(s12-mid-reflection) 트래킹 현황 — 실험 전용 |
| `round1-results.md` | 이동 | `01_experiments/01_reflection/notes/` | 회고 1차 D1 실측 노트(session_id null·UTC·smoke) — 실험 전용 |
| `사이드바실험_검토리포트.md` | 이동 | `01_experiments/02_sidebar/notes/` | 사이드바 설계 vs D1 실측 교차검증 — 실험 전용 |
| `사이드바설계서_피드백.md` | 이동 | `01_experiments/02_sidebar/notes/` | 사이드바 설계서·백로그 피드백 — 실험 전용 |
| `준실험트래킹원칙.md` | 이동 | `00_common/` | 트래킹 요건 명세, 두 실험(회고+사이드바) 모두 대상 — 공통 |
| `사이드바실험설계.md` | **삭제** | (원본: `01_experiments/02_sidebar/experiment-spec.md`) | 서식만 제거된 사본(diff로 실물 대조 확인, 검토리포트도 "설계서 사본"으로 명기) — 복제 금지 원칙 |
| — 루트 `refe.md` | **삭제** | — | 0줄 빈 파일 |

같이 수행한 참조 정비:
- `실험_트래킹리포트.md` §8 부록 — §2의 폐기 경로 7건을 현재 경로(상대 링크)로 갱신.
- `사이드바실험_검토리포트.md` — 이동에 맞춰 상대 링크 수정(playbook·준실험트래킹원칙·회고 노트 2건), 사본 링크는 원본 spec으로 대체.
- `준실험트래킹원칙.md`·`사이드바설계서_피드백.md` — 상단 한줄요약 규약 준수하도록 추가.
- `INDEX.md` — 트리·구조 원칙 표·구조 이력에 반영. "별도 analytics 폴더 금지" 규칙 명문화.
- 넘버링 개편 시 워크스페이스 `../CLAUDE.md`의 a:b test 경로 참조도 동반 갱신(변경 이력 기재). 전 상대 링크 존재 검증 완료.

## 4. 문서별 유래 메모

- **`01_experiments/01_reflection/notes/실험_트래킹리포트.md`** — 2026-06-22 작성 회고 트래킹 현황. 재배치 이전 구조 기준으로 작성돼 부록에 폐기 경로가 남아 있던 것을 07-13 갱신.
- **`01_experiments/01_reflection/notes/round1-results.md`** — 회고 1차 실측 문답 노트(2026-07-13). 발견 이슈: 노출 119건 session_id 전부 null, 시각 기준 UTC(KST 변환 필요), 6/27 선행 데이터는 별도 실험의 smoke test, 장애 구간(6/30~7/1) 일별 0건.
- **`00_common/준실험트래킹원칙.md`** — K 작성(2026-06-22) 트래킹 요건 명세. 수신: L(적재). 핵심: 분모=노출(배정 아님).
- **`01_experiments/02_sidebar/notes/사이드바실험_검토리포트.md`** — 2026-07-13 설계 vs D1 실측 교차검증 초안. 계측 계약 4건 불일치(experiment_id·session_id·노출 소스·시간대) 발견.
- **`01_experiments/02_sidebar/notes/사이드바설계서_피드백.md`** — K의 설계서·백로그 피드백. 검토리포트와 세트.
- **외부 잔존물** — `~/Desktop/study/study_AI_AGENT/project/a/b test/output/s12-mid-reflection-tracking-report.md`: 초기 산출물. 실험 슬러그만 공유할 뿐 이 프로젝트 문서의 출처 아님. 이 프로젝트에서 관리하지 않음.

## 5. 갱신 규칙

구조를 옮기거나 문서를 삭제하면 **같은 커밋(세션) 안에서**:
1. 이 문서 §1 연대기에 한 줄 + 매핑 표 추가.
2. `INDEX.md` 트리·구조 이력 갱신 (워크스페이스 `../CLAUDE.md`가 이 프로젝트 경로를 참조하면 그것도).
3. 이동 문서의 상대 링크를 수정하고 존재 검증(`[ -e ]`)까지 수행.
