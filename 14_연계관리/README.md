# 연계 관리

## 개요
이 문서는 내부 시스템과 외부 시스템 간 연동(인터페이스) 현황을 관리하는 기준을 안내합니다. `RAW/erd-참고용.png`의 **INT(연계관리)** 항목에 대응합니다.

## 목적
- 어떤 내부 CI가 어떤 외부 시스템과 연동되어 있는지 추적합니다.
- 연동이 최신 테스트/형상(베이스라인) 기준으로 검증됐는지 확인합니다.

## 연계 관리 프로세스
- (작성 예정) 연동 정의 → 테스트관리(TST)·형상관리(SCM) 결과로 검증 → 운영 반영 → 정기 점검 단계별 절차

## 필드 정의 (INTERFACE 테이블)

| 필드명 | 설명 | 비고 |
|---|---|---|
| INTERFACE_ID | 연계 고유 ID | **PK**. 예: `INT_20260711_001` |
| INTERFACE_NAME | 연계명 | |
| EXTERNAL_SYSTEM_NAME | 외부 시스템명 | |
| PROTOCOL | 연동 방식 | REST/SFTP/DB Link 등 |
| STATUS | 상태 | 정상/점검중/장애 |
| LAST_CHECK_DT | 최근 점검 일시 | |
| OWNER_TEAM | 담당 부서 | |
| VALIDATED_BY_TEST_ID | 검증 근거 테스트 ID | FK → [13_테스트관리](../13_테스트관리/README.md) TEST_CASE.TEST_ID (선택) |
| BASELINE_ID | 검증 근거 베이스라인 ID | FK → [10_형상관리](../10_형상관리/README.md) BASELINE.BASELINE_ID (선택) |

## 구성관리와의 연결
- 연계 1건은 여러 내부 CI를 통할 수 있고(예: 앱서버+DB 동시 연동), CI 1건도 여러 외부 연계에 관여할 수 있어 **N:M** 관계입니다.
- 실제 연결은 **`INTERFACE_CI_MAP` 중간 테이블**을 통해 관리하며, 데이터 파일은 [연계이력/](연계이력/README.md) 폴더에 둡니다.

## 테스트관리·형상관리와의 연결
- 참고 그림의 "TST → INT", "SCM → INT" 흐름대로, 연계 1건의 최신 검증 근거(테스트·베이스라인)는 각각 최대 1건이라 **N:1** 관계이며 `VALIDATED_BY_TEST_ID`/`BASELINE_ID` FK로 직접 연결합니다.

## 생성된 테이블 파일
| 파일 위치 | 설명 | 건수 |
|---|---|---|
| `INTERFACE.csv` (이 폴더) | 위 필드 정의를 구현한 연계 마스터 테이블 | 0건(스키마만 우선 반영) |
| [`연계이력/INTERFACE_CI_MAP.csv`](연계이력/README.md) | INTERFACE-CI 중간(연결) 테이블 | 0건(스키마만 우선 반영) |

## 참고 및 관리 방법
- (작성 예정) 외부 시스템 장애 시 대응 절차, 정기 점검 주기

## 변경 이력
| 날짜 | 내용 | 작성자 |
|---|---|---|
| 2026-07-11 | RAW/erd-참고용.png(통합 ITSM 13단계 운영 흐름도) 반영 스캐폴딩 작업으로 INTERFACE 테이블 필드 정의 및 구성관리와의 N:M 관계(INTERFACE_CI_MAP), 테스트관리·형상관리와의 N:1 관계(직접 FK) 신설. 실제 연계 데이터가 없어 스키마(헤더)만 우선 반영 | Claude |
| 2026-07-12 | Streamlit `pages/14_연계관리.py`를 읽기 전용 조회에서 실제 등록/조회 CRUD 화면으로 교체 — 상태 선택 → 조회, 연계 등록(폼, VALIDATED_BY_TEST_ID·BASELINE_ID FK selectbox 포함)/삭제. `CHG_20260712_004`로 변경 이력 등록 | Claude |
