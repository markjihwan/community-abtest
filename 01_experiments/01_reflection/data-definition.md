> **📄 요약 ·** 1차 회고 DB/이벤트 정의(event_log: project_reflection_ui_*, reflection 테이블). 🛠 적재 대상 — 00_common/ENGINEERING.md §2.

12기 회고 관련 DB는 주로 event_log와 reflection입니다. event_log.event_name은 project_reflection_ui_viewed, project_reflection_ui_clicked를 카탈로그에 등록하고, properties JSON에는 experiment_id, placement_key, project_id, project_cohort, user_project_role, source가 들어올 수 있다고 정의해주세요.
제출 완료 데이터는 reflection 테이블에서 experiment_id = 's12-mid-reflection' 기준으로 보면 되고, 유저별 중복/완료 기준은 user_id + experiment_id입니다.

이번 12기 회고는 준실험이라 control/treatment variant 로그는 없습니다. 실제로 쌓이는 로그는 회고 UI 노출(project_reflection_ui_viewed), 클릭(project_reflection_ui_clicked), 최종 제출(reflection)입니다.
분석은 viewed → clicked → submitted 퍼널 중심으로 보고, 제출 완료는 reflection.experiment_id = 's12-mid-reflection' 기준으로 집계하면 됩니다.