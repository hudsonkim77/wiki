"""전체 13개 도메인(1·2·3·6~15번 폴더) CSV 컬럼의 한글 라벨 공통 정의.
표 헤더 치환(CHG_20260712_003)에서 쓰던 것을 전체 관리 페이지로 확장하며 한 곳으로 모았다.
"""

COLUMN_LABELS_KO = {
    "MAP_ID": "매핑 ID", "CI_ID": "구성항목 ID", "NOTE": "비고", "STATUS": "상태",
    "OWNER_TEAM": "담당 부서",
    "CHG_TICKET_ID": "변경 티켓 ID", "CHG_TITLE": "변경 제목", "CHG_TYPE": "변경 유형",
    "REQUEST_TEAM": "요청 부서", "REQUESTER_ID": "요청자 ID", "APPROVER_ID": "승인자 ID",
    "CHG_STATUS": "변경 상태", "PLANNED_DT": "계획 일시", "APPLIED_DT": "적용 일시",
    "ROLLBACK_YN": "롤백 여부", "IMPACT_LEVEL": "영향도", "RELATED_DESC": "상세 내용",
    "TRIGGERED_BY_INCIDENT_ID": "촉발 장애 ID", "WORK_NOTE": "작업 메모",
    "INCIDENT_ID": "장애 ID", "INCIDENT_TITLE": "장애 제목", "SEVERITY": "심각도",
    "DETECTED_DT": "감지 일시", "RESOLVED_DT": "복구 일시", "ROOT_CAUSE": "근본 원인",
    "ACTION_TAKEN": "조치 내용", "HANDLER_ID": "처리자 ID", "INCIDENT_STATUS": "장애 상태",
    "CAUSED_BY_CHG_TICKET_ID": "원인 변경 ID", "IMPACT_DESC": "영향 내용",
    "CI_NAME": "자산명", "HOST_NAME": "호스트명", "CI_TYPE": "자산 유형",
    "CI_CATEGORY": "자산 분류", "DEPTH_LEVEL": "계층 깊이", "PARENT_CI_ID": "상위 자산 ID",
    "LOCATION_OR_URL": "위치/URL", "IP_ADDRESS": "IP 주소", "OS_VERSION": "OS 버전",
    "SERIAL_NUM": "일련번호", "ADMIN_USER_ID": "관리자 ID", "INST_DT": "설치 일시",
    "HISTORY_ID": "이력 ID", "ACTION": "조치 구분", "ACTION_DT": "조치 일시", "ACTION_BY": "조치자",
    "PROBLEM_ID": "문제 ID", "PROBLEM_TITLE": "문제 제목", "PROBLEM_TYPE": "문제 유형",
    "WORKAROUND": "임시 회피책", "PERMANENT_FIX": "영구 조치",
    "DEPLOY_ID": "배포 ID", "DEPLOY_NAME": "배포명", "DEPLOY_TYPE": "배포 유형",
    "DEPLOY_STATUS": "배포 상태", "DEPLOYED_DT": "배포 일시", "DESC": "설명",
    "REQ_ID": "요청 ID", "REQ_TITLE": "요청 제목", "REQ_TYPE": "요청 유형",
    "REQUESTED_DT": "요청 일시", "COMPLETED_DT": "완료 일시", "ASSIGNED_TEAM": "담당 부서",
    "SLA_ID": "SLA ID", "SERVICE_NAME": "서비스명", "METRIC_TYPE": "지표 유형",
    "TARGET_VALUE": "목표치", "PERIOD": "측정 주기", "MEASURED_VALUE": "측정치",
    "BREACH_YN": "위반 여부",
    "BASELINE_ID": "베이스라인 ID", "BASELINE_NAME": "베이스라인명", "VERSION": "버전",
    "BASELINE_TYPE": "베이스라인 유형", "CREATED_DT": "생성 일시", "APPROVED_DT": "승인 일시",
    "RESOLVED_PROBLEM_ID": "조치 문제 ID",
    "BASELINE_VERSION": "베이스라인 버전(스냅샷)", "BASELINE_AREA": "베이스라인 영역",
    "OPS_ID": "운영상태 ID", "CHECK_DT": "점검 일시", "METRIC_SUMMARY": "지표 요약",
    "EVENT_ID": "이벤트 ID", "EVENT_TITLE": "이벤트 제목", "EVENT_TYPE": "이벤트 유형",
    "SOURCE_OPS_ID": "감지 운영상태 ID", "EVENT_STATUS": "이벤트 상태",
    "ESCALATED_INCIDENT_ID": "확대 장애 ID",
    "TEST_ID": "테스트 ID", "TEST_TYPE": "테스트 유형", "TEST_RESULT": "테스트 결과",
    "TESTED_DT": "테스트 일시", "TESTER_TEAM": "테스트 담당 부서",
    "INTERFACE_ID": "연계 ID", "INTERFACE_NAME": "연계명",
    "EXTERNAL_SYSTEM_NAME": "외부 시스템명", "PROTOCOL": "프로토콜",
    "LAST_CHECK_DT": "최종 점검 일시", "VALIDATED_BY_TEST_ID": "검증 테스트 ID",
    "BACKUP_ID": "백업 ID", "ACTION_TYPE": "조치 유형", "BACKUP_DT": "백업 일시",
    "RETENTION_UNTIL_DT": "보관 만료일", "RESTORED_FROM_BACKUP_ID": "복원 원본 백업 ID",
}


def ko_labels(columns):
    """주어진 컬럼 목록 순서를 유지하며 {원본컬럼: 한글라벨} 딕셔너리를 만든다."""
    return {c: COLUMN_LABELS_KO.get(c, c) for c in columns}
