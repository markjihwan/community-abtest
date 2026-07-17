> **📄 요약 ·** 2차 사이드바 event_log 통합 스키마·이벤트 카탈로그·예시 payload. 🛠 적재 스키마 — 00_common/ENGINEERING.md §1.

# 사이드바 A/B — 데이터 정의서 (이벤트 스키마 / Task #5)

| 항목 | 값 |
|---|---|
| `experiment_id` | `sidebar-nav-v1` |
| 연결 | [실험 구체화](./experiment-spec.md) · [Playbook](../../00_common/playbook.md) |
| 전제 | 플랫폼에 범용 `event_log` 부재(`dl_page_views` 빈 테이블) → **이 스키마로 신규 구축**(Task #7) |
| 설계 원칙 | 회고 실험(`project_reflection_ui_*`)과 **하나의 `event_log`로 공유** |

---

## 1. `event_log` 테이블 스키마 (통합)

> 핵심 차원은 **상위 컬럼으로 승격**(필터·조인 편의), 나머지는 `properties`(JSON).
> 적재 방식: **incremental**(각 행 = 고유 이벤트, `base_date` = 발생일) → 날짜 필터 없이 집계해도 중복 없음.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | text PK | 이벤트 UUID (클라이언트 생성, 멱등 적재 키) |
| `event_name` | text | 아래 카탈로그(§2) 값 |
| `experiment_id` | text | `sidebar-nav-v1` (비실험 이벤트는 null 허용) |
| `variant` | text | `control` \| `treatment` (노출 시점 배정값, null 허용) |
| `user_id` | text | 로그인 유저 (= `dl_profiles.id`) |
| `anon_id` | text | 비로그인 식별자(쿠키/디바이스) |
| `session_id` | text | 세션 식별자 |
| `occurred_at` | timestamp | **클라이언트 발생 시각** (퍼널·순서 판정 기준) |
| `received_at` | timestamp | 서버 수신 시각 |
| `properties` | json(text) | 이벤트별 추가 속성(§2) |
| `base_date` | date | 적재 파티션(=occurred_at 날짜) |
| `load_dt` | timestamp | 적재 시각 |

```sql
-- 제안 DDL (D1/SQLite 기준, 개발팀 검토용)
CREATE TABLE event_log (
  id           TEXT PRIMARY KEY,
  event_name   TEXT NOT NULL,
  experiment_id TEXT,
  variant      TEXT,
  user_id      TEXT,
  anon_id      TEXT,
  session_id   TEXT,
  occurred_at  TEXT NOT NULL,
  received_at  TEXT,
  properties   TEXT,          -- JSON
  base_date    TEXT,
  load_dt      TEXT
);
CREATE INDEX ix_event_exp  ON event_log (experiment_id, event_name, base_date);
CREATE INDEX ix_event_user ON event_log (user_id, session_id);
```

> 식별자 규칙: 로그인=`user_id` 우선, 비로그인=`anon_id`. 로그인 전환 시 `anon_id→user_id` 매핑 테이블로 이어붙임(분석 모수 일관성).

---

## 2. 이벤트 카탈로그 (sidebar-nav-v1)

| event_name | 발생 시점 | 필수 properties | 용도 |
|---|---|---|---|
| `exp_exposure` | 사이드바가 배정 variant로 렌더된 순간(세션당 1회) | `page` | **분모(노출)** |
| `sidebar_item_clicked` | 사이드바 항목 클릭 | `item_key`, `position`, `page` | CTR 분자 |
| `page_view` | 페이지 진입 | `page`, `source` | 핵심페이지 도달·Bounce |
| `enrollment_completed` | 스터디/행사 등록 완료 | `enroll_type`, `target_id` | 등록 전환 |
| `project_alert_signup` | 13기 프로젝트 알림 신청 | `cohort`, `target_id` | 보조 전환 |
| `session_start` | 세션 시작(첫 page_view) | `landing_page`, `is_first_visit` | 세션시간·Bounce(Guardrail) |

**공통 properties(모든 이벤트 권장)**: `device`, `source`, `referrer`, `app_version`.
**상위 컬럼으로 승격**: `experiment_id`, `variant`, `user_id`/`anon_id`, `session_id`, `occurred_at`.

### 예시 payload
```json
// exp_exposure
{ "id":"7b1...","event_name":"exp_exposure","experiment_id":"sidebar-nav-v1",
  "variant":"treatment","user_id":"230f3a47-...","session_id":"s_abc",
  "occurred_at":"2026-06-29T01:12:03Z",
  "properties":{ "page":"home","device":"desktop","app_version":"1.4.0" } }

// sidebar_item_clicked
{ "id":"9c2...","event_name":"sidebar_item_clicked","experiment_id":"sidebar-nav-v1",
  "variant":"treatment","user_id":"230f3a47-...","session_id":"s_abc",
  "occurred_at":"2026-06-29T01:12:09Z",
  "properties":{ "item_key":"projects","position":1,"page":"home" } }

// enrollment_completed
{ "id":"a4d...","event_name":"enrollment_completed","experiment_id":"sidebar-nav-v1",
  "variant":"treatment","user_id":"230f3a47-...","session_id":"s_abc",
  "occurred_at":"2026-06-29T01:13:40Z",
  "properties":{ "enroll_type":"study","target_id":"proj_991" } }
```

**`item_key` 허용값**: `projects`, `events`, `dashboard`, `community`, `wiki`, `profile`, `etc`.
**`enroll_type`**: `study` | `event`. **`page`**: `home`, `projects`, `events`, `project_detail`, `event_detail`, …

---

## 3. 노출(exposure) 규칙 — 분모 정확성 (Task #6)
- `exp_exposure`는 **사이드바가 배정 variant로 실제 화면에 렌더된 순간** 발생. 배정만 되고 미렌더면 발생 안 함.
- **세션당 1회** dedup(같은 `experiment_id`+`session_id`+`user_id`는 첫 노출만 카운트).
- 분석 모수 = `exp_exposure`가 있는 유저. **노출 없는 배정 유저는 제외**(회고 실험의 생존자 편향과 동일 교훈).
- 클릭/전환 이벤트의 `variant`는 반드시 같은 세션 노출의 variant와 일치해야 함(불일치 = 계측 버그).

---

## 4. 지표 → 이벤트 매핑 (퍼널)

```
exp_exposure (노출, 분모)
   └─> sidebar_item_clicked  (item_key ∈ {projects, events})   ← Primary CTR 분자
          └─> page_view      (page ∈ {projects, events})        ← 도달
                 └─> enrollment_completed  또는  project_alert_signup  ← 전환
```

| 지표 | 분자 | 분모 |
|---|---|---|
| 핵심메뉴 CTR | `sidebar_item_clicked` (projects/events) 유니크 유저 | `exp_exposure` 유니크 유저 |
| 등록 전환율 | `enrollment_completed` 유니크 유저 | `exp_exposure` 유니크 유저 |
| 알림 신청 전환 | `project_alert_signup` 유니크 유저 | `exp_exposure` 유니크 유저 |
| 홈 이탈률(Guardrail) | 단일 page_view·무클릭 세션 | 홈 진입 세션 |
| 첫방문 세션시간(Guardrail) | (마지막-처음 이벤트 시각) median | 첫 방문 세션 |

> 모든 비율은 **유니크 유저** 기준(중복 클릭 1회 처리).

---

## 5. 배정(assignment) 데이터
- 배정은 **결정적 해시**라 별도 저장 없이 재현 가능하지만, **SRM·감사를 위해 노출 시 variant를 `exp_exposure`에 기록**(상위 `variant` 컬럼).
- 선택: `experiment_assignment(user_id|anon_id, experiment_id, variant, assigned_at)` 테이블로 sticky 영속화(Task #8). SRM은 이 테이블 또는 `exp_exposure` 유니크 유저 기준.

---

## 6. 분석 쿼리 골격 (Task #13 연동 · 엔진 제약 준수)
> `event_log`는 incremental → `base_date` 중복 없음. **CTE 미지원 → FROM 서브쿼리.** `LIMIT ≤ 100`.

```sql
-- variant별 노출/클릭/전환 + CTR (유니크 유저)
SELECT variant,
  COUNT(DISTINCT CASE WHEN event_name='exp_exposure' THEN COALESCE(user_id,anon_id) END) AS exposed,
  COUNT(DISTINCT CASE WHEN event_name='sidebar_item_clicked'
        AND json_extract(properties,'$.item_key') IN ('projects','events')
        THEN COALESCE(user_id,anon_id) END) AS core_clickers,
  COUNT(DISTINCT CASE WHEN event_name='enrollment_completed' THEN COALESCE(user_id,anon_id) END) AS enrolled
FROM event_log
WHERE experiment_id='sidebar-nav-v1'
  AND base_date >= '2026-06-28'
GROUP BY variant
```
→ CTR = core_clickers / exposed, 전환 = enrolled / exposed. 이 값을 `bayesian_calc.py`(성공/시행수)와 SRM 카이제곱 입력으로 사용.

---

## 7. 계측 QA 체크리스트 (Task #14 전제)
- [ ] `exp_exposure`가 세션당 1회만, 렌더 시점에 발생하는가
- [ ] 클릭/전환의 `variant`가 노출 variant와 100% 일치하는가
- [ ] 비로그인→로그인 전환 시 `anon_id↔user_id` 연결되는가
- [ ] `item_key`/`enroll_type`/`page` 값이 허용 enum을 벗어나지 않는가
- [ ] AA 테스트(양군 동일 UI)에서 CTR 차이가 통계적으로 0에 수렴하는가
- [ ] `base_date` 파티션이 `occurred_at` 기준으로 정확한가
