# 요청이력 (REQUEST_CI_MAP, REQUEST_INCIDENT_MAP)

## 개요
이 폴더는 요청관리(`REQUEST`)와 구성관리(`CI`)·장애관리(`INCIDENT`) 사이의 **N:M 관계를 연결하는 중간(연결) 테이블 2종**을 보관합니다.
상위 도메인 설명은 [8_요청관리](../README.md), 구성관리는 [3_구성관리](../../3_구성관리/README.md), 장애관리는 [2_장애관리](../../2_장애관리/README.md)를 참고하세요.

## 파일 목록
| 파일명 | 설명 | 건수 |
|---|---|---|
| REQUEST_CI_MAP.csv | 어떤 요청이 어떤 CI에 영향을 줬는지(발급/변경) 매핑 | 0건(스키마만 우선 반영) |
| REQUEST_INCIDENT_MAP.csv | 어떤 요청이 장애로 확대(에스컬레이션)됐는지 매핑 | 0건(스키마만 우선 반영) |

## 필드 정의 — REQUEST_CI_MAP
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** |
| REQ_ID | 요청 ID | **FK → ../REQUEST.csv** |
| CI_ID | 영향받은 구성항목 ID | **FK → ../../3_구성관리/CI.csv** |
| NOTE | 연결 근거 메모 | |

## 필드 정의 — REQUEST_INCIDENT_MAP
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** |
| REQ_ID | 요청 ID | **FK → ../REQUEST.csv** |
| INCIDENT_ID | 확대된 장애 ID | **FK → ../../2_장애관리/INCIDENT.csv** |
| NOTE | 연결 근거 메모 | |

## 참고 및 관리 방법
- 요청 처리 완료 시 [`../REQUEST.csv`](../REQUEST.csv) 상태 갱신과 함께, 영향받은 CI가 있으면 REQUEST_CI_MAP에, 장애로 확대됐으면 REQUEST_INCIDENT_MAP에 행을 추가합니다.

## 작업 업데이트 이력
| 날짜 | 내용 | 작업자 |
|---|---|---|
| 2026-07-11 | `요청이력` 폴더 신설, `REQUEST_CI_MAP.csv` 스키마(헤더) 생성 | Claude |
| 2026-07-11 | RAW/erd-참고용.png 검토 후 REQ→INC 흐름 반영, `REQUEST_INCIDENT_MAP.csv` 신규(스키마만) | Claude |
