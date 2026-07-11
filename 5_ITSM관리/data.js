// ITSM 통합관리대시보드 - 데이터 스냅샷
// 아래 값은 2026-07-11 기준 다음 원본 파일을 집계한 결과입니다.
//   - 3_구성관리/CI.csv          (총 자산수, 카테고리별 자산수)
//   - 1_변경관리/CHANGE.csv      (변경건수)
//   - 2_장애관리/INCIDENT.csv    (장애건수)
// 원본 CSV가 갱신되면 이 파일도 다시 집계해서 갱신해야 합니다(자동 연동 아님).
const ITSM_DASHBOARD_DATA = {
  snapshotDate: '2026-07-11',
  totalAssets: 310,
  assetsByCategory: [
    { category: 'Storage', count: 115 },
    { category: 'VM', count: 30 },
    { category: 'Staff', count: 30 },
    { category: 'PC', count: 30 },
    { category: 'Server', count: 20 },
    { category: 'Internal_Security_Sol', count: 15 },
    { category: 'DMZ_Compute', count: 15 },
    { category: 'Switch', count: 10 },
    { category: 'Network_Security', count: 10 },
    { category: 'L2_PAGE', count: 10 },
    { category: 'Network_Equipment', count: 8 },
    { category: 'L3_PAGE', count: 8 },
    { category: 'L1_PAGE', count: 4 },
    { category: 'Peripheral', count: 3 },
    { category: 'Security_Management', count: 2 }
  ],
  scoreboard: {
    changeCount: 10,
    incidentCount: 0,
    // 구성관리 추가/삭제 건수: 아직 전체 이력 로그는 없고, CHG_20260711_001로
    // 이 대시보드 자신(4개 메뉴 페이지, CFG_WEB_019~022)을 CI로 신규 등록한
    // 건수만 반영했습니다. 과거분/향후분을 포함한 전체 이력을 추적하려면
    // 각 관리 입력창 설계 시 CI 변경이력(added/removed) 로그를 별도로 설계해야 합니다.
    ciAdded: 4,
    ciRemoved: 0
  }
};
