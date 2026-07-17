> **📄 요약 ·** 모든 실험 공통 기준 — 메트릭 계층(North Star/Guardrail/Supporting)·하이브리드 배정·quasi-experiment 원칙·4-state 판정. 새 실험은 이 문서를 전제로 개별 결정만 등록.


1차 실험_PLAYBOOK_메트릭정의
Experiment Playbook
(작성일시 : 260406) (추가 업데이트 예정)

이 문서는 모든 실험에 공통으로 적용되는 세 가지 기준을 담는다.

메트릭 카탈로그 — 어떤 지표를 왜, 어떤 우선순위로 쓰나
하이브리드 배정 방식 — treatment/control을 어떻게 나누나
Quasi-experiment 설계 원칙 — cohort 환경 특성 때문에 추가로 고려해야 할 것들
개별 실험 등록서는 이 문서를 전제로, 실험별 구체적 결정사항만 기재한다.

1. 메트릭 카탈로그
1-1. KPI 계층 구조
실험 KPI는 최종 성과 판단 지표와 그 성과를 설명하거나 보호하는 하위 지표를 구분해서 설계한다. 상위 지표는 "이 실험이 성과를 냈는가?"를 판단하는 기준이고, 하위 지표는 "왜 그런 결과가 나왔는가?" 또는 "성과를 내는 과정에서 훼손된 것은 없는가?"를 판단하는 기준이다.

이는 상위 지표를 하위 입력 지표로 분해해 관리하는 Metric Hierarchy 방식과, 실험 지표를 Primary / Secondary / Guardrail로 구분하는 실험 설계 원칙을 결합한 구조다.

구분	역할	해석 원칙
North Star / Primary KPI	실험의 최종 성과 판단	이 지표가 개선되지 않으면 실험 성공으로 보지 않음
Guardrail KPI	부작용 감시	악화 시 전체 적용(ship) 불가 또는 재검토
Supporting KPI	병목 위치 및 변화 경로 파악	성공 여부 판단보다 원인 진단에 사용
Leading Indicator	조기 신호 탐색	선행 신호로만 사용하며 인과 해석 금지
Funnel / Retention KPI	운영 구조 및 단계별 흐름 점검	모집–참여–유지–종료 후 재참여 흐름 확인
계층별 배치 원칙

North Star는 프로그램의 최종 목적과 가장 직접적으로 연결되는 1개 핵심 지표로 둔다.
Guardrail은 North Star 개선 과정에서 훼손되면 안 되는 지표를 둔다.
Supporting KPI는 North Star의 입력 요소 또는 중간 단계 지표로 구성한다.
Leading Indicator는 조기 관측용으로 두되, 결과 해석의 근거 지표로 사용하지 않는다.
지표 간 관계는 가능하면 상위 결과 = 하위 입력의 합/차/전환 구조로 설명 가능해야 한다.
1-2. KPI 카탈로그
North Star / Primary KPI
지표	정의	주의사항
완주율	최종 제출 완료 인원 / 첫 참여 인원	현재 기수 한정 적용. 빌더 자체 입력 구조로 상향 편향 가능성 있음 — 해석 시 명시 필요
완주율은 이 플랫폼의 Primary KPI다. 다른 지표가 좋아도 완주율이 개선되지 않으면 "최종 성과 개선"으로 단정하지 않는다.

Guardrail KPI (P0)
지표	정의	역할
4주차 리텐션	4주 유지 인원 / 첫 참여 인원	완주율 개선이 조기 이탈 증가를 동반하지 않는지 확인
중도 이탈률	이탈 인원 / 첫 참여 인원	실험이 참여 지속성을 훼손했는지 확인
운영 부담	멘토 시간 + 수동 대응 + 리마인드 횟수	성과 개선이 운영 비용 급증을 동반하는지 감시 (향후 수치화 필수)
3주차 리텐션 이탈 사유 분류

코드	의미
no_response	연락 두절
voluntary_dropout	자발적 이탈 (사유 기재)
no_show_presentation	발표 노쇼
schedule_conflict	일정 충돌
unknown	사유 미확인
Guardrail이 악화되면 Primary KPI 결과와 무관하게 적용하지 않는다.

Supporting KPI (P0)
지표	정의	역할
1주차 출석률	1주차 출석 / 첫 참여	초기 적응 구간 병목 파악
2주차 생존율	2주 유지 / 첫 참여	초반 이탈 여부 파악
3주차 생존율	3주 유지 / 첫 참여	중반 유지력 파악
Supporting KPI는 완주율을 설명하는 입력 지표다. 단독으로 실험 성공을 선언하는 기준이 아니다.

Funnel / Retention KPI (P1)
지표	정의	역할
첫 참여율	첫 참여 / 승인	승인 이후 실제 참여 전환 확인
재참여율	다음 기수 재참여 / 종료	종료 후 재유입 확인
발표(post) 진행률	발표(post) / 첫 참여	종료 단계 산출물 이행 확인
Leading Indicator (P2)
지표	해석 원칙
발표 횟수	완주 가능성의 조기 신호. "발표가 완주를 만든다"로 인과 해석 금지
피드백 횟수	참여 강도 및 몰입도 관측용
상호작용 수	댓글 + 멘션 + 교류 합. 커뮤니티 활성 조기 신호
Leading Indicator는 조기 관측용이다. 결과가 애매할 때 보조로 볼 수 있지만 인과 근거로 삼지 않는다.

1-3. KPI 설계 원칙
상위 지표와 하위 지표의 연결성 Supporting KPI는 완주율에 실제로 영향을 줄 수 있는 하위 입력 지표여야 한다. Leading Indicator는 행동 강도의 조기 신호로 위치를 명확히 구분한다.

MECE 분해 우선 완주율 하나만 볼 것이 아니라 초기 출석 → 중간 생존 → 최종 제출 구조로 나누어 어느 단계에서 차이가 났는지 파악한다.

지표는 판단용·설명용·관측용을 분리

용도	지표
판단용	완주율, Guardrail
설명용	출석률, 생존율, 제출률
관측용	발표 횟수, 피드백 횟수, 상호작용 수
지표 Owner 지정

구분	Owner
North Star / Guardrail	운영 리드 또는 PM
Supporting KPI	세션 운영 / 멘토링 운영 담당
Leading Indicator	커뮤니티 / 운영 분석 담당
2. 하이브리드 배정 방식
cohort 간 비교(기수 vs 기수)가 기본이지만, 같은 기수 내에서 treatment/control을 나누는 within-cohort 하이브리드 방식을 병행한다. 배포 전후 비교는 시즈널리티 영향을 받을 수 있으므로, 실험군/대조군을 동시에 두는 편이 더 적절하다.

2-1. 배정 규칙
항목	결정 사항
배정 단위	개인(individual) 단위
배정 주체	개발팀이 로직으로 구현
실험군 / 대조군	같은 기수 안에서 동시 노출
동시 실험	같은 Primary KPI를 쓰는 실험은 동시 진행 금지
실험 비율	처음부터 50:50 고정이 아니라 점진 배포 가능
SRM 모니터링	실험 기간 중 배정 비율 정기 확인
중간 변경 금지	실험 중간에 결론 또는 배정 로직 변경 금지
2-2. 오염 방지: 세그먼트 선분리
배정 전에 참여 이력 기준으로 먼저 세그먼트를 나누고, 세그먼트 내부에서만 treatment/control을 배정한다.

세그먼트	정의
new	현재 기수가 첫 참여
returning	과거 기수 참여 이력 1회 이상 (기수 간격 무관)
new와 returning은 섞어 배정하지 않는다.
두 세그먼트는 완주율의 기저값이 다를 수 있으므로 결과 해석도 분리한다.
전체 결과가 null이어도 세그먼트별 차이는 사후 분석에서 확인할 수 있다. 단, 이는 사후 해석이지 Primary KPI 판단을 대체하지 않는다.
3. Quasi-experiment 설계 원칙
이 플랫폼의 실험 환경은 전형적인 A/B test와 다르다. 제품 수정이 어렵고, 운영 단위가 기수(cohort) 중심이며, 참여자가 자기선택으로 집단에 들어온다. 따라서 모든 실험은 cohort 기반 quasi-experiment로 설계하고 해석한다.

3-1. 핵심 분석 가정 (매 실험마다 명시)
실험 등록서에 아래 두 가정의 성립 여부와 검증 방법을 반드시 기재한다.

[가정 1] Conditional Independence

W7 이전 특성 등 사전 공변량을 통제했을 때, treatment 배정 여부는 outcome과 독립적이다.

검증 방법: 균형 검사(SMD)로 treatment/control 간 사전 특성 차이를 확인한다.

[가정 2] SUTVA 부분 충족

팀·멘토 그룹 내 Spillover는 존재할 수 있다. 완전 차단이 어려우므로 team_id를 공변량으로 통제하고 해석 시 명시한다.

3-2. 균형 검사 → 분석 방법 결정 흐름
실험 분석 전에 반드시 균형 검사를 수행하고, 결과에 따라 분석 방법을 확정한다.

python scripts/check_balance.py --csv data.csv --treatment treatment_flag

SMD	대응
≤ 0.1	균형 충족 → 층화 분석 진행
0.1 ~ 0.2	공변량 보정 로지스틱 회귀 사용
> 0.2	해석 제한 명시 또는 탐색 실험으로 재분류
층화 분석 가능 여부는 셀당 최소 20명 기준으로 확인한다.

python scripts/stratification_check.py --csv data.csv --treatment treatment_flag --strata prior_exp attendance_bucket

3-3. 표본 크기 및 실험 분류
실험 시작 전 표본 크기를 계산하고, 탐색/결정 실험을 사전에 분류한다.

python scripts/calc_sample_size.py --baseline 0.XX --mde 0.XX

조건	분류
그룹당 n ≥ 30, MDE 감지 가능	결정 실험 — ship/hold 판단 가능
그룹당 n < 30 또는 MDE 너무 큼	탐색 실험 — 방향 탐색만 가능, 결론 내리지 않음
3-4. Bayesian 결과 해석 기준
python scripts/bayesian_calc.py --t-success N --t-total N --c-success N --c-total N

P(Treatment > Control)	판단
≥ 95%	ship 고려 가능 (Guardrail 확인 후)
90 ~ 95%	Guardrail 확인 후 판단
80 ~ 90%	need_more_data 또는 탐색 실험 재분류
< 80% 또는 Control 우위	hold / rollback 검토
3-5. 해석 원칙
허용하지 않는 해석

✗  "개입이 완주율을 높였다" (인과 주장)
✗  "참여하면 완주할 가능성이 X% 높아진다" (개인 예측)
허용하는 해석

✓  "treatment 그룹은 control 그룹보다 완주율이 X%p 높았다"
✓  "사전 특성을 통제한 후에도 treatment 그룹의 완주율이 더 높았다"
✓  "이 차이가 해당 개입에서 비롯됐을 가능성이 있다"
✓  "관측되지 않은 교란변수의 영향을 배제할 수 없어 연관성 수준으로 해석한다"
인과 해석은 randomized 실험이 가능해진 이후로 미룬다.

3-6. 최종 판단 기준
모든 실험의 최종 상태는 아래 네 가지 중 하나로 기록한다.

판단	조건
ship	Primary KPI 개선 + Guardrail 이상 없음
hold	불확실 또는 표본 부족
rollback	Guardrail 훼손 또는 Primary KPI 악화
need_more_data	방향은 있으나 신뢰도 부족
Guardrail이 훼손되면 Primary KPI 결과와 무관하게 ship하지 않는다.

