# 구성 관리 - RAW 데이터 안내

## 개요
이 문서는 `RAW` 폴더에 보관되는 CSV 원본 데이터를 어떻게 참고하고 관리할지에 대한 기준을 안내합니다.

## RAW 폴더 위치
- 경로: `../RAW` (wiki 최상위 디렉토리 기준 `RAW/`)
- 용도: 가공하지 않은 원본 CSV 데이터 보관

## 파일 명명 규칙
- (작성 예정) 예: `YYYYMMDD_데이터명.csv`

## 데이터 목록
| 파일명 | 설명 | 출처 | 최종 수정일 | 비고 |
|---|---|---|---|---|
| CFG.csv (`../RAW`) | CI(자산) 마스터 원본. 서버/네트워크장비/PC/스토리지/웹페이지/인력(HUMAN) 등 구성항목과 계층(부모-자식), 담당자, 최근 변경티켓 정보를 포함 | 자산 실사/CMDB 추출 | 2026-07-11 | 중복 제거 완료(고유 CI 306건, 헤더 포함 307행). 원본은 `../RAW/20260711_CFG_backup.csv`로 보관 |
| CI.csv (이 폴더) | 아래 "CI(자산) 마스터 필드 정의"를 실제 테이블로 구현한 결과물. `../RAW/CFG.csv`(306건)에 [5_ITSM관리](../5_ITSM관리/README.md) 통합관리대시보드 자체를 CI로 등록한 5건(`CFG_WEB_019`~`023`)을 더해 총 311건 | `../RAW/CFG.csv` + 자체 등록 | 2026-07-11 | 이 폴더의 개념 설계를 그대로 반영한 산출 테이블. `pages/3_구성관리.py`의 CI 등록/삭제 화면을 통해서도 직접 수정됨(311건은 스냅샷, 실사용 중 변동 가능) |
| [`구성이력/CI_HISTORY.csv`](구성이력/README.md) | CI 추가/삭제 이력 로그 | 자체 등록 + 실사용 | 2026-07-11 | 4건(최초 백필) + 이후 실사용 누적 |

## CI(자산) 마스터 필드 정의
`CFG.csv`의 컬럼을 분석하여 정리한 필드 정의입니다. 이 테이블이 변경관리·장애관리와 연결되는 **중심(허브) 테이블**입니다.

| 필드명 | 설명 | 비고 |
|---|---|---|
| CI_ID | 구성항목 고유 ID | **PK**. 예: `CFG_SRV_001`, `AST-SEC-007` |
| CI_NAME | 구성항목 명칭 | |
| HOST_NAME | 호스트명 | HUMAN/WEB_PAGE 등 일부 유형은 공란 |
| CI_TYPE | 구성항목 유형 | 예: HARDWARE, NETWORK, WEB_PAGE, HUMAN, Server, Firewall 등 |
| CI_CATEGORY | 구성항목 분류(하위 카테고리) | 예: Storage, VM, Staff, PC, Switch, L1~L3_PAGE 등 |
| DEPTH_LEVEL | 계층 깊이 | 0=최상위, PARENT_CI_ID와 함께 트리 구조 표현 |
| PARENT_CI_ID | 상위 구성항목 ID | **FK → CI.CI_ID (자기참조)** |
| LOCATION_OR_URL | 위치 또는 URL | 물리 장비는 위치, 웹페이지는 경로 |
| IP_ADDRESS | IP 주소 | 해당 없는 유형(PC, 웹페이지, 인력 등)은 공란 |
| OS_VERSION | OS/플랫폼 버전 | |
| SERIAL_NUM | 일련번호 | |
| OWNER_TEAM | 소유/관리 부서 | |
| ADMIN_USER_ID | 담당자 ID | **FK(느슨한 참조) → CI.CI_ID(HUMAN 유형)**. 원본에 `USR_006` vs `CFG_USR_006`처럼 표기 불일치가 있어 정합화 필요 |
| STATUS | 상태 | 예: OPERATIONAL, Active, STANDBY |
| INST_DT | 등록/설치일시 | |
| CHG_TICKET_ID | 최근 관련 변경 티켓 ID | **FK → CHANGE.CHG_TICKET_ID**. 1개 컬럼으로는 CI 1건에 변경 이력 1건만 표현 가능 → 다건 이력은 아래 `CHANGE_CI_MAP` 중간 테이블로 관리 |

## 데이터 모델 및 연관관계 (ERD 요약)
구성관리(CI)를 허브로, 변경관리·장애관리가 N:M으로 연결되는 구조입니다.

```
CI (구성관리) 1 ──< CHANGE_CI_MAP >── N CHANGE (변경관리)
CI (구성관리) 1 ──< INCIDENT_CI_MAP >── N INCIDENT (장애관리)
CHANGE (변경관리) 1 ──< INCIDENT (장애관리)   * 변경이 유발한 장애인 경우 (선택적 FK)
```

- CI 1건은 여러 번의 변경/여러 건의 장애와 연관될 수 있고, 변경/장애 1건도 여러 CI에 영향을 줄 수 있어 **N:M** 관계입니다. 따라서 직접 FK 대신 중간(연결) 테이블을 둡니다.
- 각 도메인의 상세 필드는 [1_변경관리](../1_변경관리/README.md), [2_장애관리](../2_장애관리/README.md) 문서를 참고하세요.

### CHANGE_CI_MAP (변경-구성 연결 테이블)
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** (또는 `CHG_TICKET_ID`+`CI_ID` 복합키로 대체 가능) |
| CHG_TICKET_ID | 변경 티켓 ID | **FK → CHANGE.CHG_TICKET_ID** |
| CI_ID | 영향받은 구성항목 ID | **FK → CI.CI_ID** |
| APPLIED_DT | 해당 CI에 변경이 적용된 일시 | |
| WORK_NOTE | 해당 CI 기준 작업 메모 | |

### INCIDENT_CI_MAP (장애-구성 연결 테이블)
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** (또는 `INCIDENT_ID`+`CI_ID` 복합키로 대체 가능) |
| INCIDENT_ID | 장애 ID | **FK → INCIDENT.INCIDENT_ID** |
| CI_ID | 영향받은 구성항목 ID | **FK → CI.CI_ID** |
| IMPACT_DESC | 해당 CI 기준 영향 내용 | |

## CI 허브에 연결되는 전체 도메인 (2026-07-11 확장)
`RAW/erd-참고용.png`(통합 ITSM 13단계 운영 흐름도)에 맞춰 위키 전체를 13개 도메인으로 재정렬하면서, CI를 허브로 아래 도메인들이 추가로 연결되었습니다. 상세 필드는 각 도메인 문서를 참고하세요.

| 연결 도메인 | 중간테이블/FK | 관계 |
|---|---|---|
| [8_요청관리](../8_요청관리/README.md) REQUEST | REQUEST_CI_MAP | N:M |
| [11_운영상태관리](../11_운영상태관리/README.md) OPS_STATUS | OPS_CI_MAP | N:M |
| [10_형상관리](../10_형상관리/README.md) BASELINE | BASELINE_CI_MAP | N:M |
| [14_연계관리](../14_연계관리/README.md) INTERFACE | INTERFACE_CI_MAP | N:M |
| [15_백업관리](../15_백업관리/README.md) BACKUP | BACKUP_CI_MAP | N:M |
| [12_이벤트관리](../12_이벤트관리/README.md) EVENT | 직접 FK(CI_ID) | N:1 |

전체 13개 도메인 간 연결을 한눈에 보려면 정합성 검토용 ERD(Claude Artifact)를 참고하세요.

## 참고 및 관리 방법
- 원본 데이터는 직접 수정하지 않고, 가공이 필요한 경우 별도 사본을 만들어 작업합니다.
- 데이터 추가/변경 시 위 목록 표를 함께 갱신합니다.
- **[데이터 품질 이슈 – 해결됨, 2026-07-11]** `CFG.csv`에 헤더 행 2회 포함(52번째 줄 재등장), 완전 중복 행 225건, 중복 `CI_ID` 다수(예: `CFG_DEV_001` 등)가 발견되어 아래 기준으로 중복을 제거했습니다.
  1. 원본 전체를 `20260711_CFG_backup.csv`로 백업.
  2. 재등장한 헤더 행 제거.
  3. 완전히 동일한 행은 최초 1건만 유지.
  4. 같은 `CI_ID`인데 내용이 다른 30건(대부분 `CFG_USR_*` 인력 CI)은 필드 밀림(컬럼 하나가 비어야 할 자리가 누락되어 뒤 필드들이 한 칸씩 밀린 경우)으로 확인되어, `STATUS` 필드에 유효한 상태값(OPERATIONAL/Active/STANDBY)이 정상적으로 들어간 행을 정본으로 채택하고 밀린 행은 제거했습니다.
  5. `CFG_TER_064`는 필드 밀림이 아니라 `LOCATION_OR_URL` 값 표기가 다른 순수 콘텐츠 차이(`VDI 클러스터 B` vs `VDI CLUSTER B`)라 자동 판별이 불가능해, 먼저 등장한 값을 잠정 채택했습니다. **데이터 소유자 확인이 필요합니다.**
  - 결과: 원본 563행(중복 헤더 제외) → 정제 후 306건 고유 CI.
- (작성 예정) 버전 관리, 백업 주기, 접근 권한 등

## 변경 이력
| 날짜 | 내용 | 작성자 |
|---|---|---|
| 2026-07-11 | CFG.csv 필드 분석 → CI 마스터 필드 정의, 변경관리/장애관리 연결을 위한 CHANGE_CI_MAP·INCIDENT_CI_MAP 중간 테이블 설계 추가 | Claude |
| 2026-07-11 | CFG.csv 원본을 `20260711_CFG_backup.csv`로 백업 후 중복 제거(563행→306건 고유 CI)하여 CFG.csv 갱신. `CFG_TER_064`는 콘텐츠 차이로 확인 필요 항목으로 남김 | Claude |
| 2026-07-11 | 개념 설계한 CI 테이블을 이 폴더에 `CI.csv`(306건)로 실제 생성 | Claude |
| 2026-07-11 | [5_ITSM관리](../5_ITSM관리/README.md) 통합관리대시보드 자체를 자산으로 등록. `CFG_WEB_019`(메인) 및 하위 메뉴 페이지 `CFG_WEB_020`(변경관리)·`CFG_WEB_021`(장애관리)·`CFG_WEB_022`(구성관리) 4건 추가로 총 310건. `CHG_20260711_001`로 최초 구축 변경 이력 연결 | Claude |
| 2026-07-11 | 이 문서의 ERD 요약(위 "데이터 모델 및 연관관계")을 [5_ITSM관리](../5_ITSM관리/README.md) `구성관리.html` 하단에 SVG+HTML 다이어그램으로 시각화. `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_003`으로 갱신 | Claude |
| 2026-07-11 | 홈 대시보드 최근 사항 3건 기능 추가로 `CFG_WEB_019`의 `CHG_TICKET_ID`를 `CHG_20260711_004`로 갱신 | Claude |
| 2026-07-11 | Streamlit 구성관리 페이지 임베딩 작업으로 `CFG_WEB_022`의 `CHG_TICKET_ID`를 `CHG_20260711_005`로 갱신 | Claude |
| 2026-07-11 | 로고 반영 작업으로 `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_007`로 갱신 | Claude |
| 2026-07-11 | 로고 아이콘 크기 확대 작업으로 `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_008`로 갱신 | Claude |
| 2026-07-11 | `구성이력/CI_HISTORY.csv` 신설(최초 4건 백필) 및 `pages/3_구성관리.py` CI 등록/삭제 화면 구현으로 `CFG_WEB_022`의 `CHG_TICKET_ID`를 `CHG_20260711_009`로 갱신 | Claude |
| 2026-07-11 | 상단 네비 로고 가독성 개선 작업으로 `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_010`으로 갱신 | Claude |
| 2026-07-11 | Streamlit 배포판 로고 폭 확대(st.image) 작업으로 `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_011`로 갱신 | Claude |
| 2026-07-11 | 패널 제목/테두리 스타일 개선 작업으로 `CFG_WEB_019`~`022`의 `CHG_TICKET_ID`를 `CHG_20260711_013`으로 갱신 | Claude |
| 2026-07-11 | 경영관리 메뉴 페이지(`경영관리.html`)를 `CFG_WEB_023`으로 신규 등록(총 311건)하고, ITSM관리·경영관리 메뉴 추가 작업으로 `CFG_WEB_019`~`023`의 `CHG_TICKET_ID`를 `CHG_20260711_014`로 갱신 | Claude |
| 2026-07-12 | ERD 페이지(`ERD.html`)를 `CFG_WEB_024`로 신규 등록(총 312건) | Claude |
| 2026-07-12 | 필드값 없는 항목 정리 — [1_변경관리](../1_변경관리/README.md) CHANGE.csv에서 세부 항목이 전부 공란이던 레거시 티켓 9건을 삭제하면서, 이를 `CHG_TICKET_ID`로 참조하던 CI 60건(레거시 자산의 "최초 등록 변경" 참조)의 값을 공란으로 정리(자산 자체는 그대로 유지, 참조만 해제) | Claude |
| 2026-07-12 | [초기 베이스라인 정의서 v1.0] 작업으로 전체 CI 312건(인력 30·응용 24·인프라 258)을 [10_형상관리](../10_형상관리/README.md)의 공식 베이스라인 `BSL_20260712_002`에 일괄 편입(`BASELINE_CI_MAP`). 자산관리(CMDB)와 형상관리(베이스라인) 간 추적 연결을 이번에 처음으로 실데이터로 채움 | Claude |
