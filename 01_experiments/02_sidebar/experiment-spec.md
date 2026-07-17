> **📄 요약 ·** 2차 사이드바 A/B 실험 설계서 — 가설·KPI·배정(무작위)·계측·대시보드. 🛠 플랫폼 기능은 §5 — 00_common/ENGINEERING.md.

# 사이드바 내비게이션 A/B 테스트 — 실험 구체화 정의서

| 항목 | 값 |
|---|---|
| 실험명 | Sidebar Navigation Optimization for Categorization Fluency |
| `experiment_id` | `sidebar-nav-v1` |
| 유형 | **진짜 무작위 A/B** (50:50, 개인 단위) — 회고 준실험과 다름 |
| 대상 | pseudo-lab.com 웹 플랫폼 방문 유저 (로그인 멤버 기준, MAU ~500) |
| 작성일 | 2026-06-22 · 상태: 설계 구체화 |
| 연결 | [Playbook](../../00_common/playbook.md) · [플랫폼 아키텍처](../../00_common/platform.md)의 "웹 플랫폼 실험" 항목이 곧 이 실험 |

---

## 0. 용어 빠른 설명 (처음 보는 분께)
> 전체 풀이는 [`00_common/용어집.md`](../../00_common/용어집.md). 이 문서 핵심만:

| 용어 | 쉽게 |
|---|---|
| **control / treatment** | control=기존 사이드바 그대로 / treatment=확장자 뺀 새 사이드바 |
| **variant(변형)** | 사용자에게 보여주는 버전(control 또는 treatment) |
| **노출(exposure)** | 사이드바를 **실제로 본** 기록. 비율 계산의 분모 = '본 사람' |
| **CTR(클릭률)** | 본 사람 중 핵심메뉴를 클릭한 비율 |
| **전환율** | 본 사람 중 스터디/행사 **등록까지** 간 비율 |
| **Guardrail** | 망가지면 안 되는 안전지표(이탈률·세션시간). 나빠지면 **출시 금지** |
| **SRM** | 50:50으로 나눴는데 실제 비율이 틀어진 것 → **배정/계측 버그 신호, 실험 중단** |
| **Bayesian P(T>C)** | "treatment가 더 좋을 확률" %. ≥95%면 출시 고려 |
| **MDE** | 잡아낼 수 있는 **최소 차이**. 작을수록 표본 많이 필요 |

---

## 1. 가설 (IF / THEN / BECAUSE)

- **IF (개입)**: 사이드바에서 파일 확장자(`.json/.tsx/.md`)를 제거하고, 핵심 메뉴(**Projects, Events**)를 폴더 깊은 곳에서 꺼내 **최상단**에 배치.
- **THEN (기대결과)**: 핵심 메뉴 진입 **CTR ↑** → 스터디/행사 **등록 전환율 ↑** (+ 13기 프로젝트 알림 신청 전환 ↑). 탐색 단계 이탈(Drop-off) 감소.
- **BECAUSE (근거)**: **2차 해독 과정 제거** + **범주화 유창성(Categorization Fluency)** 극대화 → 메뉴 해석 인지 비용 ≈ 0 → 클릭까지 매끄럽게 연결.

**변형(Variant)**
| 군 | UI |
|---|---|
| control | 현행 IDE 스타일 사이드바(확장자 노출, 핵심 메뉴 하위) — Status Quo |
| treatment | 확장자 제거 + Projects/Events 최상단 노출 심플 사이드바 |

---

## 2. KPI 구조 (Playbook 계층 매핑)

| 계층 | 지표 | 운영 정의(operational) |
|---|---|---|
| **Primary** | 핵심메뉴 CTR | (Projects 또는 Events 클릭한 노출유저) / (노출유저), variant별 |
| **Primary** | 등록 전환율 | (스터디/행사 등록 완료 유저) / (노출유저) |
| Secondary | 알림 신청 전환 | (13기 프로젝트 알림 신청 유저) / (노출유저) |
| **Guardrail** | 메인 홈 이탈률(Bounce) | 단일 페이지·무행동 세션 / 세션 (브랜드 매력 훼손 감시) |
| **Guardrail** | 첫 방문 세션 시간 | 첫 방문 유저 세션 길이 median (악화 시 ship 불가) |
| Funnel | 탐색 퍼널 | 노출 → 핵심메뉴 클릭 → 대상 페이지뷰 → 등록 |

> **분모는 "노출유저(exposed)"** — 사이드바를 실제로 본 사람. 배정만 되고 미노출이면 분모에서 제외(정확한 CTR의 전제).

---

## 3. 배정 & 통계 설계

| 항목 | 결정 |
|---|---|
| 배정 단위 | 개인(user_id), 비로그인은 anon/device id |
| 비율 | 50:50 (점진 배포 가능: 10→50%) |
| 배정 방식 | **결정적 해시** `hash(user_id + experiment_id) % 100` → sticky(고정), 중간 변경 금지 |
| SRM | 배정 비율 일일 점검(카이제곱), 이상 시 실험 중단 |
| 표본/MDE | baseline CTR 확보 후 `calc_sample_size.py`로 산정. MAU 500이면 **결정 vs 탐색** 사전 분류 필수 |
| 판정 | Bayesian P(T>C) ≥ 95% → ship 고려(Guardrail 확인 후) / 4-state |
| 오염 방지 | 동일 Primary KPI 쓰는 실험 동시 진행 금지 |

> **가정**: 무작위 배정이므로 회고 실험과 달리 선택편향 통제 불필요 → **인과 해석 가능**(randomized). 단 SRM·노출 정의가 깨지면 무효.

---

## 4. 트래킹 / 계측 설계 ⭐ (무엇을 설정해야 하나)

> 📄 **실제 이벤트 스키마·DDL·예시 payload·분석쿼리는 [`data-definition.md`](./data-definition.md)** 에 구체화(Task #5).

> 현재 플랫폼에 범용 이벤트 테이블이 **없음**(`dl_page_views`는 빈 테이블, `event_log`는 미존재). **이벤트 적재부터 만들어야 함.**

### 4-1. 발생시켜야 할 이벤트
| 이벤트 | 시점 | 용도 |
|---|---|---|
| `exp_exposure` | 사이드바가 배정 variant로 렌더된 순간 | **분모(노출)** — 가장 중요 |
| `sidebar_item_clicked` | 사이드바 항목 클릭 | CTR 분자 |
| `page_view` | 페이지 진입 | 핵심페이지 도달·Bounce 계산 |
| `enrollment_completed` | 스터디/행사 등록 완료 | 전환 분자 |
| `project_alert_signup` | 13기 알림 신청 | 보조 전환 |
| `session_start` / 종료 신호 | 세션 경계 | Guardrail 세션시간·Bounce |

### 4-2. 공통 properties (모든 이벤트에 심기)
```
experiment_id   = 'sidebar-nav-v1'
variant         = 'control' | 'treatment'
user_id         (또는 anon_id)
session_id
item_key        = 'projects' | 'events' | ... (클릭 이벤트)
position        = 사이드바 내 순서(인덱스)
page            = 'home' | 'projects' | 'events' | ...
source          = 유입 경로
ts, device
```

### 4-3. 계측 원칙
- **노출 보장**: 배정 ≠ 노출. `exp_exposure`가 없으면 그 유저는 분석 제외(회고 실험의 생존자 편향과 동일 교훈).
- **클릭-노출 짝**: 클릭 이벤트는 반드시 같은 variant·session으로 노출 이벤트와 연결 가능해야 함.
- **dedup**: CTR은 유니크 유저 기준(중복 클릭 1회 처리).

---

## 5. 플랫폼에 추가돼야 할 기능 ⭐

| # | 기능 | 설명 |
|---|---|---|
| F1 | **실험 배정 서비스** | config(experiment_id·variants·ratio·targeting·status) + 결정적 버킷팅 + sticky + **kill switch** |
| F2 | **Variant 플래그 전달** | 프론트가 배정 variant를 받아 사이드바 A/B 렌더 |
| F3 | **이벤트 적재 파이프라인 + `event_log` 테이블** | 4장의 이벤트/properties를 수집·저장 (현재 부재) |
| F4 | **SRM 모니터** | 배정 비율 일일 점검·알림 |
| F5 | **Guardrail Hook** | 등록서에 Guardrail 없으면 저장 차단 / ship 결론 시 Guardrail 미기록 차단 (Playbook 강제) |
| F6 | **실험 등록서** | `experiments/sidebar-nav-abtest.md` (플랫폼 레포 구조에 등록) |

---

## 6. 지표 관리 — 플랫폼 내 대시보드 설계 ⭐ (나중에 어떻게 보여줄까)

**실험 대시보드 1페이지 구성**
```
┌───────────────────────────────────────────────────────────────┐
│ sidebar-nav-v1   [running]  6/2X~   배정 50.2:49.8  ✅SRM OK     │
│ n(control)=___  n(treatment)=___   노출유저=___                 │
├──────────────────────┬────────────────────────────────────────┤
│ 퍼널 (control|treat)  │ KPI 카드                                 │
│ 노출 ████ | ████      │ 핵심메뉴 CTR  C __%  T __%  Δ__%p        │
│ 클릭 ██   | ███       │   P(T>C)=__%  [신뢰구간]                 │
│ 페이지 █  | ██        │ 등록 전환율   C __%  T __%  Δ__%p        │
│ 등록  ▏   | █         │ 알림 신청     C __%  T __%               │
├──────────────────────┴────────────────────────────────────────┤
│ Guardrail   홈 이탈률 C__% T__%  | 첫방문 세션 C__s T__s  ⚠/✅   │
│ 표본/검정력  현재 n / 필요 n __%  · 유의까지 약 __일             │
│ 판정 배너    [ship | hold | rollback | need_more_data]  (Guardrail 우선) │
└───────────────────────────────────────────────────────────────┘
```
- **퍼널**은 variant 나란히 비교, 각 단계 전환율 표기.
- **KPI 카드**는 절대값 + Δ%p + **Bayesian P(T>C)** + 신뢰구간.
- **Guardrail 패널**은 악화 시 빨강 경고, ship 자동 차단 연동.
- **판정 배너**는 Playbook 규칙으로 자동 산출, Guardrail 훼손 시 ship 불가.

---

## 7. 분석 & 판정 흐름
1. AA/계측 QA → 점진 배포 → SRM 확인(깨지면 중단).
2. 퍼널·CTR·전환 variant 비교 → Bayesian P(T>C).
3. Guardrail 확인(이탈률·세션시간) → 4-state 판정.
4. 해석: randomized라 인과 가능하나 SRM·노출 정의 유효성 먼저 확인.

> 표본 부족(MAU 500) 시 **탐색 실험**으로 분류, 방향만 보고 ship 단정 금지.
