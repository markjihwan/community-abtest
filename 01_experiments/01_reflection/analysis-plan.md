> **📄 요약 ·** 1차 회고 분석계획 — 자기선택 준실험, 청강생/생존자 편향 통제, 추정량·공변량·SQL 골격·4-state 판정. 분석가용.

# 12기 중간 회고 가이드 — 분석계획서 (Analysis Plan)

| 항목 | 값 |
|---|---|
| 실험명 | 프로젝트 성격 기반 중간 회고 가이드 제공 실험 |
| `experiment_id` | `s12-mid-reflection` |
| cohort | 12기 |
| 노출 기간 | 2026-06-28 ~ 2026-07-05 |
| 설계 유형 | **Quasi-experiment** (전원 노출 → 작성 여부 자기선택 비교) |
| 작성일 | 2026-06-22 |
| 상태 | 계획 (pre-registration) |
| 연결 문서 | [실험 spec](./experiment-spec.md) · [데이터 정의](./data-definition.md) · [Playbook](../../00_common/playbook.md) |

---

## 0. 분석의 성격 (한 줄)

> 무작위 배정이 아닌 **자기선택 준실험**이다. 분석의 핵심은 *"작성자가 원래 더 성실한 집단이었던 것 아닌가"* 라는 **선택편향을 통제한 뒤 잔존 연관성을 보는 것**이며, 인과 주장은 하지 않는다.

---

## 1. 핵심 질문 & 가설

- **핵심 질문**: 중간 회고 가이드를 제공했을 때, 회고 작성 여부와 완주율 사이에 (사전 특성 통제 후에도) 양의 연관이 관찰되는가?
- **가설**: 회고 작성 → 프로젝트 성격·산출물 경로 인식 ↑ → 남은 액션 명확화 → 참여 지속 → 완주율 ↑
- **귀무**: 사전 특성 통제 후 작성자/미작성자 완주율 차이 = 0

---

## 2. 모집단 & 분기 정의

### 2-1. 분석 모집단 (가장 중요)
> **12기 참여자 중 2026-06-28 시점 active 상태인 정규(regular) 멤버**로 고정한다.
> - 6/28 이전 이탈자는 회고 작성 자체가 불가능하므로 제외 → **생존자 편향 차단**.
> - **청강생(auditor)은 모집단에서 제외** → **데이터 오염 차단** (아래 2-4).

### 2-4. 청강생(auditor) 제외 — 데이터 오염 차단 (실측 근거)
> 청강생은 완주 의무가 없는 비정규 참여자이므로 완주율/리텐션/이탈 분모·분자에 섞이면 지표가 왜곡된다.
> 12기 실측: 정규 195명(출석률 66.5%) vs 청강생 32명(출석률 74.1%) — 청강생이 멤버의 약 14%이고 출석률이 더 높아 **섞으면 지표가 상향 편향**된다.

**핵심 주의**: `dl_project_members.role`에는 `runner / builder / member`만 있고 **`auditor` 구분이 없다.** 즉 `dl_*` 테이블로는 청강생을 구조적으로 제외할 수 없다. 청강생 구분(`participant_type`)은 **`dm_*` 마트에만** 존재하므로, 출석/리텐션/이탈은 반드시 다음 마트로 산출한다(상세 쿼리는 [`query.md`](./queries.md)):
- `dm_member_weekly_attendance` — `participant_type='regular'`, `member_status='active'`, `as_of_date=MAX` 필터
- `dm_project_weekly_attendance` — `regular_attendance_rate` / `auditor_attended_count` 이미 분리 제공

### 2-2. 비교군 분기
| 군 | 정의 |
|---|---|
| 작성자(writer) | `reflection`에 `experiment_id='s12-mid-reflection'` 제출 완료 (key: `user_id + experiment_id`) |
| 미작성자(non-writer) | 모집단 중 작성 완료하지 않은 자 (단, 노출 단계 분리 — 아래 2-3) |

### 2-3. 노출 단계 분리 (`participation_level`)
> 알림은 *전달*을 보장할 뿐 노출(viewed)을 보장하지 않는다. "안 본 사람"과 "보고 안 쓴 사람"을 반드시 구분한다.

| 단계 | 정의 | 판정 근거 |
|---|---|---|
| `notified_only` | 알림만 받고 회고 UI 미노출 | viewed 이벤트 없음 |
| `visited` | UI 노출(viewed)됨 | `project_reflection_ui_viewed` |
| `partial` | 클릭/시작했으나 미제출 | `..._clicked` / started 有, submitted 無 |
| `full` | 제출 완료 | `reflection` 제출 |

핵심 비교는 **`visited`+ 모집단 내에서 `full` vs (`visited`+`partial`)** — 즉 *볼 기회가 있었던 사람들* 안에서 작성/미작성을 비교한다.

---

## 3. 데이터 소스 맵

| 소스 | 키/필드 | 비고 |
|---|---|---|
| `event_log` | `event_name` ∈ {`project_reflection_ui_viewed`, `project_reflection_ui_clicked`} | 퍼널 |
| `event_log.properties` (JSON) | `experiment_id, placement_key, project_id, project_cohort, user_project_role, source` | 분해축 |
| `reflection` | `user_id, experiment_id`(dedup), 제출시각, 선택 프로젝트성격/산출물유형, 자유서술 3종 | 작성 완료 분기 |
| `dm_member_weekly_attendance` | (project,user,week) 출석·`participant_type`·`member_status` | **출석/리텐션/이탈 정본** — 청강생 제외 가능 |
| `dm_project_weekly_attendance` | 프로젝트-주차 `regular_attendance_rate`·`auditor_attended_count` | regular/auditor 분리 제공 |
| 사전 스냅샷(필수 신규) | 6/28 이전 출석·발표수·산출물수·activity_score·role·project_id | 공변량 — *지금 안 박으면 복원 불가* |
| 완주 결과(시즌 종료 후) | `completed` 여부 | Primary outcome |

> ⚠️ 아래 SQL은 **골격(skeleton)**이다. 실제 테이블/컬럼명에 맞춰 조정한다. properties는 JSON 가정(`->>` 추출).
> ⚠️ **청강생 제외**: 출석/리텐션/이탈은 `dl_project_members`로 산출 금지(`role`에 auditor 없음). `dm_member_weekly_attendance`에 `participant_type='regular'` 필터 필수 — 2-4 참조. `dm_*` 마트는 `base_date`가 아니라 **`as_of_date`** 스냅샷이므로 `as_of_date=(SELECT MAX...)` 필터도 필수.

---

## 4. 분석 트랙

### Track 1 — 노출→작성 퍼널 (Funnel KPI, 운영 진단)

**지표**: `notified → viewed → clicked → submitted` 단계별 전환율 / 이탈 지점. 분해축: `placement_key`, `source`, `user_project_role`, 프로젝트 유형.

```sql
-- 단계별 유니크 유저 수 (12기, 실험기간)
WITH base AS (
  SELECT
    (properties->>'experiment_id')      AS experiment_id,
    (properties->>'user_project_role')  AS role,
    (properties->>'placement_key')      AS placement,
    (properties->>'source')             AS source,
    user_id,
    event_name
  FROM event_log
  WHERE properties->>'experiment_id' = 's12-mid-reflection'
    AND created_at BETWEEN '2026-06-28' AND '2026-07-05'
)
SELECT
  role, placement, source,
  COUNT(DISTINCT CASE WHEN event_name='project_reflection_ui_viewed'  THEN user_id END) AS viewed,
  COUNT(DISTINCT CASE WHEN event_name='project_reflection_ui_clicked' THEN user_id END) AS clicked
FROM base
GROUP BY role, placement, source;
```

```sql
-- viewed → clicked → submitted 전환율 (제출은 reflection 조인)
WITH v AS (
  SELECT DISTINCT user_id FROM event_log
   WHERE event_name='project_reflection_ui_viewed'
     AND properties->>'experiment_id'='s12-mid-reflection'),
c AS (
  SELECT DISTINCT user_id FROM event_log
   WHERE event_name='project_reflection_ui_clicked'
     AND properties->>'experiment_id'='s12-mid-reflection'),
s AS (
  SELECT DISTINCT user_id FROM reflection
   WHERE experiment_id='s12-mid-reflection')
SELECT
  (SELECT COUNT(*) FROM v) AS viewed,
  (SELECT COUNT(*) FROM c) AS clicked,
  (SELECT COUNT(*) FROM s) AS submitted,
  ROUND((SELECT COUNT(*) FROM c)::numeric / NULLIF((SELECT COUNT(*) FROM v),0), 3) AS view_to_click,
  ROUND((SELECT COUNT(*) FROM s)::numeric / NULLIF((SELECT COUNT(*) FROM c),0), 3) AS click_to_submit;
```

```sql
-- viewed → submitted 소요시간(시간 단위), 일자별 작성 곡선용
SELECT r.user_id,
       EXTRACT(EPOCH FROM (r.submitted_at - v.first_viewed))/3600 AS hours_to_submit,
       DATE(r.submitted_at) AS submit_date
FROM reflection r
JOIN (
  SELECT user_id, MIN(created_at) AS first_viewed
  FROM event_log
  WHERE event_name='project_reflection_ui_viewed'
    AND properties->>'experiment_id'='s12-mid-reflection'
  GROUP BY user_id
) v ON v.user_id = r.user_id
WHERE r.experiment_id='s12-mid-reflection';
```

---

### Track 2 — Primary: 작성자 vs 미작성자 완주율 (North Star)

**추정량**: 사전 공변량 통제 후 `writer − non-writer`의 완주율 차이(%p).
**판정 흐름은 Playbook 3-2를 그대로 따른다.**

```sql
-- 분석 마스터 테이블: 모집단 × 분기 × 사전 공변량 × outcome
SELECT
  m.user_id,
  m.project_id,
  m.role,
  CASE WHEN r.user_id IS NOT NULL THEN 1 ELSE 0 END           AS writer_flag,   -- 분기
  pre.attendance_pre, pre.presentation_pre, pre.output_pre,
  pre.activity_score, pre.prior_exp,                                            -- 공변량(회고 이전)
  comp.completed                                                                 AS completion          -- outcome(시즌 종료 후)
FROM cohort12_active_0628 m                       -- 2-1 모집단
LEFT JOIN reflection r
  ON r.user_id = m.user_id AND r.experiment_id='s12-mid-reflection'
LEFT JOIN pre_snapshot_0628 pre ON pre.user_id = m.user_id    -- 계측 체크리스트 항목
LEFT JOIN completion comp       ON comp.user_id = m.user_id;
```

**분석 방법 결정 (Playbook 3-2)** — 마스터 테이블을 CSV로 떨궈 스크립트에 투입:
```bash
# 1) 균형 검사
python scripts/check_balance.py --csv master.csv --treatment writer_flag
#   SMD ≤ 0.1   → 층화 분석
#   0.1 ~ 0.2   → 공변량 보정 로지스틱 회귀 / PSM
#   > 0.2       → 해석 제한 명시 or 탐색 실험 재분류
# 2) 층화 가능 여부 (셀당 ≥20명)
python scripts/stratification_check.py --csv master.csv --treatment writer_flag --strata prior_exp attendance_bucket
# 3) Bayesian 우위 확률
python scripts/bayesian_calc.py --t-success Nw_done --t-total Nw --c-success Nc_done --c-total Nc
```

**공변량 (회고 *이전* 시점 기준)**: `attendance_pre`, `presentation_pre`, `output_pre`(산출물/GitHub), `activity_score`, `prior_exp`(new/returning), `project_id`/유형, `role`.

---

### Track 3 — 메커니즘 검증 (Supporting KPI)

가설 경로가 실제로 작동하는지 — 회고 **전/후** within-person 변화.

```sql
-- 작성자군의 회고 전/후 출석·발표·산출물 변화 (제출시각 기준 분할)
SELECT r.user_id,
       SUM(CASE WHEN a.ts <  r.submitted_at THEN 1 ELSE 0 END) AS attend_before,
       SUM(CASE WHEN a.ts >= r.submitted_at THEN 1 ELSE 0 END) AS attend_after
FROM reflection r
JOIN attendance a ON a.user_id = r.user_id
WHERE r.experiment_id='s12-mid-reflection'
GROUP BY r.user_id;
```
- 추가 점검: 회고에서 **선택한 산출물 유형**(GitHub/발표/문서)을 이후 실제로 등록했는가 → 행동 전환의 직접 증거.

---

### Track 4 — 세그먼트 / 이질 효과 (사후, 설명용)

분해축: `new`/`returning` · 프로젝트 유형(연구/구현/발표/문서/오픈소스) · 프로젝트 규모 · `user_project_role`(runner/builder/member).
> Track 2 모델에 상호작용항을 넣거나 세그먼트별 층화. **세그먼트 결과는 설명용이며 Primary 판정을 대체하지 않는다.**

---

### Track 5 — 회고 응답 내용 분석 (Leading)

- 선택된 프로젝트 성격 / 산출물 유형 분포.
- 자유서술 3종(잘되는 점 / 막히는 점 / 남은 목표 1개) 토픽 분류 → "막히는 점" 군집이 이후 이탈과 연관되는지(조기경보).

---

## 5. Guardrail 모니터링 (Playbook P0)

| Guardrail | 정의 | 차단 규칙 |
|---|---|---|
| 4주차 리텐션 | 4주 유지 / 첫 참여 | 악화 시 ship 불가 |
| 중도 이탈률 | 이탈 / 첫 참여 | 악화 시 ship 불가 |
| 운영 부담 | 멘토 시간 + 수동 대응 + 리마인드 횟수 | 급증 시 재검토 |

> **Guardrail이 훼손되면 Primary 결과와 무관하게 ship하지 않는다.**

---

## 6. 표본 크기 & 실험 분류 게이트

```bash
python scripts/calc_sample_size.py --baseline 0.XX --mde 0.XX
```
| 조건 | 분류 |
|---|---|
| 그룹당 n ≥ 30 & MDE 감지 가능 | **결정 실험** — ship/hold 판단 |
| 그룹당 n < 30 or MDE 과대 | **탐색 실험** — 방향만, 결론 금지 |

> 12기 active n과 작성률 확정 후 이 게이트를 먼저 통과해야 Track 2 판정 가능.

---

## 7. 최종 판정 기준 (Playbook 3-6)

| 판정 | 조건 |
|---|---|
| `ship` | 사전특성 통제 후에도 작성자군 완주율 일관 우위 + Guardrail 이상 없음 |
| `hold` | 방향 있으나 self-selection 가능성 커 보수 해석 |
| `rollback` | Guardrail 훼손 or Primary 악화 |
| `need_more_data` | 작성률/표본 부족으로 판단 유보 |

---

## 8. 계측 체크리스트 (지금 박아둘 것 — 지나가면 복원 불가)

- [ ] **사전 스냅샷**: 6/28 이전 출석·발표·산출물·activity_score·role·project_id 저장 (Track 2 공변량의 전제)
- [ ] **노출 맥락**: `viewed`/`clicked` 이벤트에 `placement_key`, `source` 정확히 적재 (퍼널 분해)
- [ ] **active/이탈 타임스탬프**: 생존자 편향 보정용 상태 변화 기록
- [ ] **dedup 보장**: `reflection`의 `user_id + experiment_id` 유니크 제약
- [ ] 노출 단계(`participation_level`) 도출 가능하도록 viewed/clicked/started/submitted 모두 적재

---

## 9. 분석 타임라인

| 시점 | 가능한 분석 |
|---|---|
| ~6/27 | 계측 검증, 모집단/스냅샷 확정 |
| 6/28~7/5 (노출) | Track 1 퍼널 실시간 모니터, Guardrail 일일 점검 |
| 7/5 직후 | Track 1·3·5(퍼널/메커니즘/내용), 작성률 확정 → 표본 게이트 |
| 시즌 종료 후 | **Track 2 Primary 판정** (완주율 확정), 최종 4-state 기록 |

---

## 10. 해석 원칙 (Playbook 3-5)

**허용** ✓
- "작성자군은 미작성자군보다 완주율이 X%p 높았다"
- "사전 특성 통제 후에도 작성자군 완주율이 더 높았다"
- "회고 작성 여부와 완주율 사이 양의 연관이 관찰되었다"

**불허** ✗
- "회고 가이드가 완주율을 높였다" (인과)
- "회고하면 완주한다" (개인 예측)

> 인과 해석은 randomized 실험이 가능해진 이후로 미룬다.
