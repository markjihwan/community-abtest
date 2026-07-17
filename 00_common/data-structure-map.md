> **📄 요약 ·** PseudoLab 데이터 ERD·PK·연결구조·데이터량·유의 테이블 한눈에. 쿼리 전 필독. (png/svg 이미지 동봉)

# 📐 데이터 구조 맵 — 한눈에 보기

> 작성일: 2026-06-22 · 보조 문서 ([분석현황 리포트](../01_experiments/01_reflection/report.md)의 부록)
> 목적: "어떤 테이블이 무엇으로 연결되고, 무엇을 볼 때 어디를 봐야 하며, 어디에 데이터가 많고 무엇을 조심할지"를 한 장에 정리.

---

## 1. 연결 구조 (ERD 한눈에)

```
                         ┌──────────────────────────────┐
   dl_profiles(id)       │   공통 조인 키 (universal keys) │
   = 유저 마스터          │   user_id    = dl_profiles.id   │
        │                │   project_id = dl_projects.id   │
        │ user_id        │   session_id = dl_project_sessions.id │
        │                └──────────────────────────────┘
        │
        ├──< dl_project_applications (user_id, *_project_id)   ── 지원/승인(첫 참여 후보)
        │
        ├──< dl_project_members (id PK; project_id, user_id)   ── 멤버십·role(runner/builder/member)
        │                                                         ⚠ auditor 구분 없음
   dl_projects(id) = 프로젝트 마스터 (status, cohort)
        │ project_id
        ├──< dl_project_sessions (id PK; project_id)           ── 세션·week_number·일정
        │          │ session_id
        │          └──< dl_project_attendance (session_id, user_id) ── 출석 원자 이벤트(present)
        │
        └──< dl_project_tasks (id PK; project_id, assignee_id) ── 태스크·status(done) (완주 신호 후보)

   ─────────────────────────────────────────────────────────────────────────
   집계 마트(dm_*) = 위 원본을 미리 계산해 둔 "정본"  (base_date 아님 → as_of_date!)
   ─────────────────────────────────────────────────────────────────────────
   dm_member_weekly_attendance   grain=(project_id, user_id, week_number)  ⭐ participant_type(regular/auditor)
   dm_project_weekly_attendance  grain=(project_id, week_number)           ⭐ regular_/auditor_ 분리 컬럼
   dm_user_daily_activity        grain=(user_id, activity_date, metric_key) 개인 일별 활동 통합
```

**핵심 한 줄**: 모든 연결의 축은 **`user_id`(=`dl_profiles.id`)** 와 **`project_id`(=`dl_projects.id`)**. 출석은 `세션(session_id)`을 거쳐 붙는다.

---

## 2. 주요 테이블 PK / 연결키 / 적재방식

| 테이블 | PK | 외래키(연결) | 적재 | 행수 | 무엇 |
|---|---|---|---|---|---|
| `dl_profiles` | `id` | — (id=user_id) | snapshot | 62,731 | 유저 마스터·사전 공변량 |
| `dl_projects` | `id` | — (id=project_id) | snapshot | ~8,760* | 프로젝트 마스터(status, cohort) |
| `dl_project_members` | `id` | project_id, user_id | snapshot | 24,636 | 멤버십·role ⚠auditor없음 |
| `dl_project_sessions` | `id` | project_id | snapshot | 22,404 | 세션·week_number |
| `dl_project_attendance` | `id` | **session_id**, user_id | **incremental** | 1,721 | 출석 이벤트(status=present) |
| `dl_project_tasks` | `id` | project_id, assignee_id, parent_task_id | snapshot | 4,042 | 태스크·status(done) |
| `dl_project_applications` | `id` | user_id, *_project_id | snapshot | 16,695 | 지원·승인(season=기수) |
| `dm_member_weekly_attendance` | (proj,user,week)+as_of_date | project_id, user_id | as_of_date | **133,919** | ⭐출석 정본·청강생 분리 |
| `dm_project_weekly_attendance` | (proj,week)+as_of_date | project_id | as_of_date | 14,882 | ⭐프로젝트 출석·regular/auditor 분리 |
| `dm_user_daily_activity` | (user,date,metric)+ | user_id | as_of_date | 13,058 | 개인 일별 활동 통합 |

\* `dl_projects`는 manifest상 23,652로 표시되나 라이브 실측 8,760(스냅샷 30일×292). **manifest row_count는 근사치 — 정확 수치는 쿼리로.**

---

## 3. "무엇을 볼 때 어디를 보나" (용도 → 테이블 라우팅)

| 보고 싶은 것 | 가야 할 곳 | 필수 필터 |
|---|---|---|
| 출석률 / 리텐션 / 이탈 / 완주 진행 | **`dm_member_weekly_attendance`** | `as_of_date=MAX` + `participant_type='regular'` + `member_status='active'` |
| 프로젝트 단위 출석(청강생 분리) | **`dm_project_weekly_attendance`** | `as_of_date=MAX` (regular_attendance_rate 사용) |
| 멤버 구성·역할(runner/builder) | `dl_project_members` | `base_date=MAX` + `status='active'` (※청강생 못 거름) |
| 세션 일정·주차 | `dl_project_sessions` | `base_date=MAX` |
| 출석 원자 이벤트 | `dl_project_attendance` | (incremental, 필터 불필요) |
| 완주/산출물 신호 후보 | `dl_project_tasks`(status=done) · `session_submissions`(현재 빈 테이블) | `base_date=MAX` |
| 첫 참여·승인(완주율 분모) | `dl_project_applications` | `season`(기수), `status` |
| 사전 공변량(activity_score·experience_level·cohorts) | `dl_profiles` | `base_date=MAX` |
| 개인 GitHub/활동 추이 | `dm_user_daily_activity` · `dm_user_qualitative_activity` | `as_of_date=MAX` |

---

## 4. 어디에 데이터가 많은가 (행수 Top)

| 순위 | 테이블 | 행수 | 성격 |
|---|---|---|---|
| 1 | `dm_member_weekly_attendance` | 133,919 | ⚠ as_of_date 90개 중복(실제 grain 2,526 → 약 53× 부풀림) |
| 2 | `dl_profiles` | 62,731 | PII·snapshot |
| 3 | `dl_project_members` | 24,636 | snapshot |
| 4 | `dl_projects` | ~8,760(실측) | snapshot |
| 5 | `dl_project_sessions` | 22,404 | snapshot |
| 6 | `dl_project_applications` | 16,695 | PII·snapshot |
| 7 | `dm_user_daily_activity` | 13,058 | PII |
| — | `dl_profile_careers` / `dl_registration_submissions` / `dl_blogs` | 12,220 / 9,891 / 6,660 | 경력·가입·콘텐츠 |

---

## 5. ⚠️ 유의해서 봐야 하는 DB (함정 모음)

1. **as_of_date 중복 (dm_* 마트 전체)** — 행수가 가장 많아 보이지만 대부분 날짜 스냅샷 중복. `dm_member_weekly_attendance`는 133,919행이나 실제 고유 grain은 2,526뿐. **반드시 `as_of_date=(SELECT MAX...)`**.
2. **base_date 중복 (snapshot 군: projects/members/sessions/profiles/tasks/applications)** — 미필터 집계 시 수십 배(예: projects 30×). **`base_date=MAX`**.
3. **청강생 오염 (dl_project_members)** — `role`에 auditor 없음 → 출석/완주는 `dl_*` 말고 **dm 마트 + `participant_type='regular'`**.
4. **PII 테이블 (has_pii=true)** — `profiles`, `project_applications`, `registration_submissions`, `dm_member_weekly_attendance`, `dm_user_daily_activity`, `*_submissions` 등. 외부 공유·집계 시 개인정보 주의(이메일·이름·연락처 포함).
5. **manifest row_count = 근사치** — 실제와 다를 수 있음(projects 23,652 vs 라이브 8,760). 정확 수치는 쿼리로 확인.
6. **빈 테이블 (row_count 0) 다수** — `session_submissions`, `action_items`, `builder_onboarding`, `xp_history`, `notifications` 등. 분석 전 **존재/적재 여부 먼저 확인**.

---

## 6. 회고 실험 관점 — 결국 이 4개를 본다

| 목적 | 테이블 | 비고 |
|---|---|---|
| 출석/리텐션/이탈 (Guardrail·Supporting) | `dm_member_weekly_attendance` | regular만, as_of_date=MAX |
| 완주율 분모(첫 참여) | `dl_project_applications` (status/season) | 정의 확정 필요 |
| 완주율 분자(완주 신호) | `dl_project_tasks`(done) or 마지막 출석 주차 프록시 | **확정 TODO** |
| 사전 공변량(편향 통제) | `dl_profiles` (activity_score, experience_level, cohorts) | 6/28 스냅샷 박제 필요 |
| 회고 행동(노출→작성) | `event_log`, `reflection` | **아직 미적재(6/28~)** |
