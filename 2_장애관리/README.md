# 장애 관리

## 개요
이 문서는 서비스 장애 발생 시 인지, 대응, 복구, 재발 방지까지의 처리 기준을 안내합니다.

## 목적
- 장애를 신속히 감지·대응하고, 원인과 조치 내역을 기록해 재발을 방지합니다.

## 장애 대응 프로세스
- (작성 예정) 감지 → 초기 대응 → 원인 분석 → 복구 → 사후 회고(포스트모템) 단계별 절차

## 필드 정의 (INCIDENT 테이블)
`CFG.csv`(구성관리 CI 마스터)에는 장애 관련 필드가 없어, 구성관리·변경관리와의 연결 관계를 고려해 신규로 설계했습니다.

| 필드명 | 설명 | 비고 |
|---|---|---|
| INCIDENT_ID | 장애 고유 ID | **PK** |
| INCIDENT_TITLE | 장애 제목 | |
| SEVERITY | 심각도 | 예: SEV1~SEV4 |
| DETECTED_DT | 최초 감지 일시 | |
| RESOLVED_DT | 복구 완료 일시 | |
| ROOT_CAUSE | 원인 분석 내용 | |
| ACTION_TAKEN | 조치 내용 | |
| HANDLER_ID | 담당자 ID | FK → 구성관리 CI.CI_ID (HUMAN 유형) |
| INCIDENT_STATUS | 진행 상태 | 예: 대응중/복구/종료 |
| CAUSED_BY_CHG_TICKET_ID | 원인이 된 변경 티켓 ID | FK → 변경관리 CHANGE.CHG_TICKET_ID (선택, 변경으로 유발된 장애인 경우만) |

## 구성관리·변경관리와의 연결
- 장애 1건은 여러 CI에 영향을 줄 수 있고, CI 1건도 여러 장애 이력을 가질 수 있어 **N:M** 관계입니다.
- 실제 연결은 **`INCIDENT_CI_MAP` 중간 테이블**을 통해 관리합니다. 설계 근거(ERD)는 [3_구성관리](../3_구성관리/README.md), 데이터 파일은 장애 도메인 하위의 [장애이력/](장애이력/README.md) 폴더에 둡니다.
- 변경이 원인이 된 장애는 `CAUSED_BY_CHG_TICKET_ID` 필드로 [1_변경관리](../1_변경관리/README.md)의 CHANGE 테이블과 직접 연결합니다(1건의 장애는 원인 변경이 최대 1건이므로 중간 테이블 없이 FK로 처리).

## 생성된 테이블 파일
| 파일 위치 | 설명 | 건수 |
|---|---|---|
| `INCIDENT.csv` (이 폴더) | 위 필드 정의를 구현한 장애 마스터 테이블 | 1건 — 첫 실제 장애(`INC_20260711_001`) 등록 |
| [`장애이력/INCIDENT_CI_MAP.csv`](장애이력/README.md) | INCIDENT-CI 중간(연결) 테이블 | 1건 |

## 장애 이력 목록
| 장애 ID | 발생일시 | 영향 시스템 | 심각도 | 원인 | 조치 내용 | 복구일시 | 담당자 |
|---|---|---|---|---|---|---|---|
| INC_20260711_001 | 2026-07-11 14:00 | CFG_WEB_019 (ITSM 통합관리대시보드, Streamlit `홈.py`) | SEV3 | `CHG_20260711_003`의 `CHANGE.csv` `RELATED_DESC` 필드에 쉼표가 포함됐으나 따옴표로 감싸지 않아 컬럼이 12개→14개로 밀려 `pandas.read_csv`가 `ParserError`로 실패 | 해당 필드를 큰따옴표로 감싸 12개 컬럼으로 복원, 전체 CSV(CI/CHANGE/INCIDENT/CHANGE_CI_MAP/INCIDENT_CI_MAP) pandas 재검증 후 커밋·push하여 Streamlit Cloud 자동 재배포 | 2026-07-11 14:10 | USR_001 |

## 참고 및 관리 방법
- 장애 발생 시 최초 감지 시각과 복구 완료 시각을 반드시 기록합니다.
- (작성 예정) 심각도(SEV) 등급 기준, 에스컬레이션 절차

## 변경 이력
| 날짜 | 내용 | 작성자 |
|---|---|---|
| 2026-07-11 | INCIDENT 테이블 필드 신규 설계, 구성관리 CI와의 N:M 관계(INCIDENT_CI_MAP) 및 변경관리 CHANGE와의 FK 관계(CAUSED_BY_CHG_TICKET_ID) 명시 | Claude |
| 2026-07-11 | 개념 설계한 INCIDENT 테이블을 이 폴더에 `INCIDENT.csv`(헤더만)로 생성. 중간테이블은 `장애이력/` 폴더를 신설하여 `INCIDENT_CI_MAP.csv`(헤더만)로 생성. 실제 장애 데이터가 없어 두 파일 모두 스키마만 우선 반영 | Claude |
| 2026-07-11 | 첫 실제 장애 `INC_20260711_001`(Streamlit `홈.py` CHANGE.csv 파싱 에러) 등록. `CAUSED_BY_CHG_TICKET_ID`로 `CHG_20260711_003`과 연결하고, `장애이력/INCIDENT_CI_MAP.csv`에 `MAP_0001`로 `CFG_WEB_019`와의 영향 관계 추가 | Claude |
