# 문제 관리

## 개요
이 문서는 반복되거나 근본 원인이 불명확한 장애를 분석해 재발을 막는 문제 관리 기준을 안내합니다.

## 목적
- 장애의 근본 원인을 파악하고 임시 회피책(workaround)과 영구 조치(permanent fix)를 구분해 관리합니다.
- 동일한 원인으로 반복되는 장애를 줄입니다.

## 문제 처리 프로세스
- (작성 예정) 문제 식별(반응형/능동형) → 조사·진단 → 임시 회피책 적용 → 근본 원인 확정 → 영구 조치 → 종료 단계별 절차

## 필드 정의 (PROBLEM 테이블)
[2_장애관리](../2_장애관리/README.md)의 INCIDENT 테이블과 연결되는 별도 테이블로 설계합니다.

| 필드명 | 설명 | 비고 |
|---|---|---|
| PROBLEM_ID | 문제 고유 ID | **PK**. 예: `PRB_20260711_001` |
| PROBLEM_TITLE | 문제 제목 | |
| PROBLEM_TYPE | 문제 유형 | REACTIVE(장애 발생 후 역추적) / PROACTIVE(선제 발견) |
| ROOT_CAUSE | 근본 원인 분석 내용 | |
| WORKAROUND | 임시 회피책 | |
| PERMANENT_FIX | 영구 조치 내용 | |
| STATUS | 진행 상태 | 등록/조사중/근본원인식별/영구조치/종료 |
| DETECTED_DT | 최초 식별 일시 | |
| RESOLVED_DT | 종료(영구조치 완료) 일시 | |
| OWNER_TEAM | 담당 부서 | |

## 장애관리와의 연결
- 문제 1건은 여러 장애에서 비롯될 수 있고, 장애 1건도 여러 문제 조사에 참고될 수 있어 **N:M** 관계입니다.
- 실제 연결은 **`PROBLEM_INCIDENT_MAP` 중간 테이블**을 통해 관리하며, 데이터 파일은 [문제이력/](문제이력/README.md) 폴더에 둡니다.

## 형상관리와의 관계
- 참고 그림의 "PRB → SCM (Root Cause Analysis → Code & Document Versioning)" 흐름대로, 문제의 영구 조치(PERMANENT_FIX) 결과가 새 베이스라인이 되면 [10_형상관리](../10_형상관리/README.md) BASELINE.csv의 `RESOLVED_PROBLEM_ID`로 이 PROBLEM을 참조합니다(N:1, 직접 FK).

## 생성된 테이블 파일
| 파일 위치 | 설명 | 건수 |
|---|---|---|
| `PROBLEM.csv` (이 폴더) | 위 필드 정의를 구현한 문제 마스터 테이블 | 1건(`PRB_20260711_001`, 조사중) |
| [`문제이력/PROBLEM_INCIDENT_MAP.csv`](문제이력/README.md) | PROBLEM-INCIDENT 중간(연결) 테이블 | 1건 |

## 참고 및 관리 방법
- 동일 CI 또는 동일 증상으로 장애가 2회 이상 반복되면 문제로 등록하는 것을 권장합니다.
- (작성 예정) 문제 우선순위 산정 기준, 근본원인분석(RCA) 절차

## 변경 이력
| 날짜 | 내용 | 작성자 |
|---|---|---|
| 2026-07-11 | ITIL v4 WBS 13개 실무 항목 중 미착수 항목에 대한 도메인 스캐폴딩 작업으로 PROBLEM 테이블 필드 정의 및 장애관리와의 N:M 관계(PROBLEM_INCIDENT_MAP) 신설. 실제 문제 데이터가 없어 스키마(헤더)만 우선 반영 | Claude |
| 2026-07-11 | 첫 실데이터로 `PRB_20260711_001`(정적 HTML/Streamlit 배포판 UI 반영 미동기화가 세션 내 3회 반복된 문제) 등록. `INC_20260711_002`(세 번째 반복 사례)를 `PROBLEM_INCIDENT_MAP`으로 연결. STATUS는 근본조치가 부분적으로만 진행돼(신규 도메인은 Streamlit 전용으로 통일) 아직 "조사중" | Claude |
