# SLA이력 (SLA_INCIDENT_MAP, SLA_OPS_MAP)

## 개요
이 폴더는 서비스수준관리(`SLA`)와 장애관리(`INCIDENT`)·운영상태관리(`OPS_STATUS`) 사이의 **N:M 관계를 연결하는 중간(연결) 테이블 2종**을 보관합니다.
상위 도메인 설명은 [9_서비스수준관리](../README.md), 장애관리는 [2_장애관리](../../2_장애관리/README.md), 운영상태관리는 [11_운영상태관리](../../11_운영상태관리/README.md)를 참고하세요.

## 파일 목록
| 파일명 | 설명 | 건수 |
|---|---|---|
| SLA_INCIDENT_MAP.csv | 어떤 장애가 어떤 SLA 항목의 목표 미달(breach)에 영향을 줬는지 매핑 | 0건(스키마만 우선 반영) |
| SLA_OPS_MAP.csv | 어떤 운영상태 점검이 어떤 SLA 항목의 실적 근거가 됐는지 매핑 | 0건(스키마만 우선 반영) |

## 필드 정의 — SLA_INCIDENT_MAP
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** |
| SLA_ID | SLA 항목 ID | **FK → ../SLA.csv** |
| INCIDENT_ID | 장애 ID | **FK → ../../2_장애관리/INCIDENT.csv** |
| BREACH_YN | 목표 미달 여부 | |
| NOTE | 연결 근거 메모 | |

## 필드 정의 — SLA_OPS_MAP
| 필드명 | 설명 | 비고 |
|---|---|---|
| MAP_ID | 매핑 고유 ID | **PK** |
| SLA_ID | SLA 항목 ID | **FK → ../SLA.csv** |
| OPS_ID | 운영상태 점검 ID | **FK → ../../11_운영상태관리/OPS_STATUS.csv** |
| NOTE | 연결 근거 메모 | |

## 참고 및 관리 방법
- 주기별 SLA 평가 시 [`../SLA.csv`](../SLA.csv)의 STATUS가 "미달"이면 원인이 된 장애를 SLA_INCIDENT_MAP에, 예방 실적 근거로 삼은 운영상태 점검은 SLA_OPS_MAP에 행 단위로 추가합니다.

## 작업 업데이트 이력
| 날짜 | 내용 | 작업자 |
|---|---|---|
| 2026-07-11 | `SLA이력` 폴더 신설, `SLA_INCIDENT_MAP.csv` 스키마(헤더) 생성 | Claude |
| 2026-07-11 | RAW/erd-참고용.png 검토 후 OPS→SLA 흐름 반영, `SLA_OPS_MAP.csv` 신규(스키마만) | Claude |
