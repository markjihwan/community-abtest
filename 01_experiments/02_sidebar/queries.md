> **📄 요약 ·** 2차 사이드바 분석 쿼리(퍼널/CTR/SRM/Guardrail). event_log 적재(#7) 후 실행. CTE 미지원→서브쿼리.

# 사이드바 A/B (`sidebar-nav-v1`) — 분석 쿼리 (Task #13)

> 전제: `event_log` 적재(Task #7) 후 실행. incremental이라 `base_date` 중복 없음. **CTE 미지원 → 서브쿼리.** `json_extract`로 properties 추출.

## S1. variant별 퍼널 + CTR/전환 (유니크 유저)
```sql
SELECT variant,
  COUNT(DISTINCT CASE WHEN event_name='exp_exposure' THEN COALESCE(user_id,anon_id) END) AS exposed,
  COUNT(DISTINCT CASE WHEN event_name='sidebar_item_clicked'
        AND json_extract(properties,'$.item_key') IN ('projects','events')
        THEN COALESCE(user_id,anon_id) END) AS core_clickers,
  COUNT(DISTINCT CASE WHEN event_name='page_view'
        AND json_extract(properties,'$.page') IN ('projects','events')
        THEN COALESCE(user_id,anon_id) END) AS reached,
  COUNT(DISTINCT CASE WHEN event_name='enrollment_completed' THEN COALESCE(user_id,anon_id) END) AS enrolled
FROM event_log
WHERE experiment_id='sidebar-nav-v1' AND base_date >= '2026-06-28'
GROUP BY variant
```
→ CTR = core_clickers/exposed, 전환 = enrolled/exposed. (Δ%p, P(T>C)는 `bayesian_calc.py` 입력)

## S2. SRM 입력 (노출 유니크 유저 비율) → `srm_check.py`
```sql
SELECT variant, COUNT(DISTINCT COALESCE(user_id,anon_id)) AS exposed_users
FROM event_log
WHERE experiment_id='sidebar-nav-v1' AND event_name='exp_exposure' AND base_date >= '2026-06-28'
GROUP BY variant
```

## S3. Guardrail — 홈 이탈률(단일 page_view·무클릭 세션) by variant
```sql
SELECT variant,
  COUNT(*) AS home_sessions,
  SUM(CASE WHEN clicks=0 AND views=1 THEN 1 ELSE 0 END) AS bounced,
  ROUND(SUM(CASE WHEN clicks=0 AND views=1 THEN 1 ELSE 0 END)*100.0/NULLIF(COUNT(*),0),1) AS bounce_rate
FROM (
  SELECT session_id, variant,
    SUM(CASE WHEN event_name='page_view' THEN 1 ELSE 0 END) AS views,
    SUM(CASE WHEN event_name='sidebar_item_clicked' THEN 1 ELSE 0 END) AS clicks
  FROM event_log
  WHERE experiment_id='sidebar-nav-v1' AND base_date >= '2026-06-28'
  GROUP BY session_id, variant
) t
GROUP BY variant
```
