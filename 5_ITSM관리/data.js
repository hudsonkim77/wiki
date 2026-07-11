// ITSM 통합관리대시보드 - 데이터 스냅샷
// 아래 값은 2026-07-11 기준 다음 원본 파일을 집계한 결과입니다.
//   - 3_구성관리/CI.csv          (총 자산수, 카테고리별 자산수)
//   - 1_변경관리/CHANGE.csv      (변경건수)
//   - 2_장애관리/INCIDENT.csv    (장애건수)
// 원본 CSV가 갱신되면 이 파일도 다시 집계해서 갱신해야 합니다(자동 연동 아님).
const ITSM_DASHBOARD_DATA = {
  snapshotDate: '2026-07-11',
  totalAssets: 311,
  // label: 화면 표시용 한글 라벨. category(원본 CI_CATEGORY 코드)는 그대로 두고 표시 문구만 한글로 대체.
  assetsByCategory: [
    { category: 'Storage', label: '스토리지', count: 115 },
    { category: 'VM', label: '가상머신(VM)', count: 30 },
    { category: 'Staff', label: '인력', count: 30 },
    { category: 'PC', label: 'PC', count: 30 },
    { category: 'Server', label: '서버', count: 20 },
    { category: 'Internal_Security_Sol', label: '내부보안솔루션', count: 15 },
    { category: 'DMZ_Compute', label: 'DMZ 서버', count: 15 },
    { category: 'Switch', label: '스위치', count: 10 },
    { category: 'Network_Security', label: '네트워크 보안', count: 10 },
    { category: 'L2_PAGE', label: '웹페이지(2단계)', count: 11 },
    { category: 'Network_Equipment', label: '네트워크 장비', count: 8 },
    { category: 'L3_PAGE', label: '웹페이지(3단계)', count: 8 },
    { category: 'L1_PAGE', label: '웹페이지(1단계)', count: 4 },
    { category: 'Peripheral', label: '주변기기', count: 3 },
    { category: 'Security_Management', label: '보안관제', count: 2 }
  ],
  // 최근 사항 3건(변경/자산등록/장애): 각 도메인 CSV의 가장 최근 행 기준으로 하나씩.
  // 원본이 바뀌면 (특히 장애/자산등록 건이 새로 생기면) 이 배열도 함께 갱신해야 합니다.
  recentItems: [
    {
      type: '변경',
      accent: 'series-2',
      id: 'CHG_20260711_003',
      title: '구성관리 페이지 3D 자산배치도·ERD 다이어그램 신설 및 개인정보처리방침 팝업 적용',
      date: '2026-07-11',
      detail: '홈 대시보드에 최근 변경 요약 노출, 구성관리.html에 가상 5층 건물 3D 자산배치도(5층=전산실)와 CI 허브 ERD 다이어그램 신설, 개인정보처리방침을 팝업(모달)으로 전환. 1_변경관리/CHANGE.csv 참고.'
    },
    {
      type: '자산등록',
      accent: 'series-4',
      id: 'CFG_WEB_019~022',
      title: 'ITSM 통합관리대시보드 신규 자산 등록(4건)',
      date: '2026-07-11',
      detail: '구성관리 CI 마스터에 신규 자산 4건(CFG_WEB_019~022: ITSM 통합관리대시보드 메인 및 변경·장애·구성관리 하위 메뉴 페이지)을 등록. 등록일시 2026-07-11 12:00, 근거 변경티켓 CHG_20260711_001. 3_구성관리/CI.csv 참고.'
    },
    {
      type: '장애',
      accent: 'series-3',
      id: 'INC_20260711_001',
      title: 'Streamlit 홈.py 대시보드 CHANGE.csv 파싱 에러로 서비스 장애',
      date: '2026-07-11',
      detail: '원인: CHG_20260711_003의 RELATED_DESC 필드에 쉼표가 포함됐으나 따옴표로 감싸지 않아 CSV 컬럼이 밀려 pandas ParserError 발생. 조치: 필드를 따옴표로 감싸 복원, 전체 CSV 재검증 후 재배포. 감지 14:00 · 복구 14:10(SEV3). 2_장애관리/INCIDENT.csv 참고.'
    }
  ],
  scoreboard: {
    changeCount: 12,
    incidentCount: 1,
    // 구성관리 추가/삭제 건수: 아직 전체 이력 로그는 없고, CHG_20260711_001로
    // 이 대시보드 자신(4개 메뉴 페이지, CFG_WEB_019~022)을 CI로 신규 등록한
    // 건수만 반영했습니다. 과거분/향후분을 포함한 전체 이력을 추적하려면
    // 각 관리 입력창 설계 시 CI 변경이력(added/removed) 로그를 별도로 설계해야 합니다.
    ciAdded: 4,
    ciRemoved: 0
  }
};
