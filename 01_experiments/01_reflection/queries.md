> **📄 요약 ·** 1차 회고 검증 쿼리(출석·리텐션·이탈) — 청강생 제외(dm 마트 + participant_type='regular'). CTE 미지원→서브쿼리.

분석팀_주요 쿼리

# ⚠️ 청강생(auditor) 오염 수정본 (2026-06-22 검증 완료)

## 문제
기존 쿼리는 `dl_project_members` 기반인데, 이 테이블의 `role`에는 `runner / builder / member`만 있고
**`auditor`(청강생) 구분이 없다.** 따라서 `status='active'`만 걸어서는 청강생을 절대 제외할 수 없고,
정규 멤버처럼 분모·분자에 섞여 들어가 모든 출석/리텐션/이탈 지표가 오염된다.

## 근거 (12기, 최신 스냅샷 실측)
| participant_type | 인원 | 출석률 |
|---|---|---|
| 정규(regular) | 195명 | 66.5% |
| 청강생(auditor) | 32명 | 74.1% |

- 청강생이 멤버 베이스의 **약 14%(32/227)**, 게다가 출석률이 정규보다 **높아** 섞이면 지표가 **상향 편향**된다.

## 해결
청강생 구분(`participant_type`)이 존재하는 **`dm_*` 데이터마트**로 전환한다.
- `dm_member_weekly_attendance` — (project, user, week) 단위, `participant_type`, `member_status` 보유
- `dm_project_weekly_attendance` — 프로젝트-주차 단위, `regular_attendance_rate` / `auditor_attended_count` **이미 분리 제공**

## 공통 필터 (반드시)
1. `as_of_date = (SELECT MAX(as_of_date) ...)`  ← dm 마트는 base_date가 아니라 **as_of_date 스냅샷**. 미필터 시 중복.
2. `participant_type = 'regular'`              ← **청강생 제외**
3. `member_status = 'active'`                  ← 기존 status='active' 의도 대체
4. `cohort = '12'`  (필요 시 `AND project_status = 'active'` 추가)

---

## 메트릭 1. 멤버-주차 출석 상세 (정규만)
```sql
SELECT project_id, project_title, user_id, week_number,
       session_count, attended_count, attended, attendance_rate
FROM dm_member_weekly_attendance
WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_member_weekly_attendance)
  AND cohort = '12'
  AND participant_type = 'regular'
  AND member_status = 'active'
ORDER BY project_title, user_id, week_number
LIMIT 100
```

## 메트릭 1_1. 멤버별 출석율 (집계용, 정규만)
```sql
SELECT project_title, user_id,
       SUM(session_count)  AS total_sessions,
       SUM(attended_count) AS attended_count,
       ROUND(SUM(attended_count) * 100.0 / NULLIF(SUM(session_count), 0), 1) AS attendance_rate
FROM dm_member_weekly_attendance
WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_member_weekly_attendance)
  AND cohort = '12'
  AND participant_type = 'regular'
  AND member_status = 'active'
GROUP BY project_title, user_id
ORDER BY project_title, attendance_rate DESC
LIMIT 100
```

## 메트릭 1_2. 프로젝트별 출석율 (정규만) — project 마트 사용
```sql
-- dm_project_weekly_attendance 는 regular/auditor 가 이미 분리돼 있어 가장 안전
SELECT project_title,
       SUM(regular_attended_count)                                  AS regular_attended,
       SUM(regular_attended_count + regular_absent_count)           AS regular_slots,
       ROUND(SUM(regular_attended_count) * 100.0
             / NULLIF(SUM(regular_attended_count + regular_absent_count), 0), 1) AS regular_attendance_rate,
       SUM(auditor_attended_count)                                  AS auditor_attended  -- 참고용(분리 집계)
FROM dm_project_weekly_attendance
WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_project_weekly_attendance)
  AND cohort = '12'
GROUP BY project_title
ORDER BY regular_attendance_rate DESC
LIMIT 100
```

## 메트릭 2. 4주차 리텐션 (정규만)
```sql
-- 정규 기준: w1 출석자 169명 → w4 출석자 140명 → 82.8% (실측)
SELECT project_title,
       COUNT(DISTINCT CASE WHEN week_number = 1 AND attended = 1 THEN user_id END) AS w1_count,
       COUNT(DISTINCT CASE WHEN week_number = 4 AND attended = 1 THEN user_id END) AS w4_count,
       ROUND(COUNT(DISTINCT CASE WHEN week_number = 4 AND attended = 1 THEN user_id END) * 100.0
             / NULLIF(COUNT(DISTINCT CASE WHEN week_number = 1 AND attended = 1 THEN user_id END), 0), 1) AS retention_rate
FROM dm_member_weekly_attendance
WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_member_weekly_attendance)
  AND cohort = '12'
  AND participant_type = 'regular'
  AND member_status = 'active'
GROUP BY project_title
ORDER BY retention_rate DESC
LIMIT 100
```

## 메트릭 3. 이탈율 (정규만)
```sql
-- ⚠️ 이 엔진은 WITH(CTE) 미지원 → FROM 서브쿼리로 작성
-- 이탈 정의: w1 출석했으나 w2 이후 한 번도 출석하지 않음
SELECT project_title,
       COUNT(CASE WHEN w1 = 1 THEN 1 END)                  AS w1_count,
       COUNT(CASE WHEN w1 = 1 AND w2plus = 0 THEN 1 END)   AS dropout_count,
       ROUND(COUNT(CASE WHEN w1 = 1 AND w2plus = 0 THEN 1 END) * 100.0
             / NULLIF(COUNT(CASE WHEN w1 = 1 THEN 1 END), 0), 1) AS dropout_rate
FROM (
  SELECT user_id, project_title,
         MAX(CASE WHEN week_number = 1  AND attended = 1 THEN 1 ELSE 0 END) AS w1,
         MAX(CASE WHEN week_number >= 2 AND attended = 1 THEN 1 ELSE 0 END) AS w2plus
  FROM dm_member_weekly_attendance
  WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_member_weekly_attendance)
    AND cohort = '12'
    AND participant_type = 'regular'
    AND member_status = 'active'
  GROUP BY user_id, project_title
) t
GROUP BY project_title
ORDER BY dropout_rate DESC
LIMIT 100
```

---

## 부록. 청강생 영향 점검 쿼리 (오염 규모 확인용)
```sql
SELECT participant_type,
       COUNT(DISTINCT user_id) AS users,
       SUM(session_count)      AS sessions,
       SUM(attended_count)     AS attended,
       ROUND(SUM(attended_count) * 100.0 / NULLIF(SUM(session_count), 0), 1) AS attendance_rate
FROM dm_member_weekly_attendance
WHERE as_of_date = (SELECT MAX(as_of_date) FROM dm_member_weekly_attendance)
  AND cohort = '12'
GROUP BY participant_type
```

---

## 폐기된 원본 쿼리 (참고용 — 사용 금지)
> 아래는 `dl_project_members` 기반이라 **청강생을 제외하지 못한다.** `role`에 auditor가 없어 구조적으로 보정 불가.
> 보관 목적으로만 남기며, 실제 지표 산출에는 위 dm 마트 버전을 사용한다.

```sql
-- (구) 멤버별 출석율 — 청강생 오염. dl_project_members.role 에 auditor 구분 없음
SELECT p.id AS project_id, p.title, m.user_id, COUNT(s.id) AS total_sessions, ...
FROM dl_project_sessions s
JOIN dl_projects p          ON p.id = s.project_id AND p.base_date = (SELECT MAX(base_date) FROM dl_projects) AND p.status='active' AND p.cohort='12'
JOIN dl_project_members m   ON m.project_id = p.id AND m.base_date = (SELECT MAX(base_date) FROM dl_project_members) AND m.status='active'  -- ← 청강생 못 거름
LEFT JOIN dl_project_attendance a ON a.session_id = s.id AND a.user_id = m.user_id
WHERE s.base_date = (SELECT MAX(base_date) FROM dl_project_sessions) ...
```
