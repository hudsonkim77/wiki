# ITSM 관리 - 통합관리대시보드

## 개요
이 폴더는 변경관리·장애관리·구성관리 현황을 한 화면에서 보는 **통합관리대시보드**의 소스를 보관합니다.

## 목적
- 총 자산수, 카테고리별 자산 분포, 변경/장애/구성관리 현황을 한눈에 파악합니다.
- [1_변경관리](../1_변경관리/README.md), [2_장애관리](../2_장애관리/README.md), [3_구성관리](../3_구성관리/README.md)로 들어가는 진입점 역할을 합니다.

## 화면 구성
- **상단 메뉴바**: 모든 페이지(`index.html`/`변경관리.html`/`장애관리.html`/`구성관리.html`)에 동일하게 떠 있는 공용 네비게이션. 좌측 로고를 누르면 항상 첫 화면(`index.html`)으로 돌아갑니다. 변경관리/장애관리/구성관리 버튼은 각 페이지로 실제 이동하며, 현재 페이지 버튼은 활성 표시됩니다. 각 페이지의 **입력 화면 내용물**은 아직 설계 전이라 "설계 전" 안내 문구만 있는 placeholder 상태입니다.
- **상단 좌측**: 총 자산수(Hero figure)
- **상단 우측**: 카테고리별 자산 현황 막대바 (카테고리마다 다른 색, 8색 순환)
- **하단 "현황" 스코어보드**: 변경건수 / 장애건수 / 구성관리(추가) / 구성관리(삭제) 4개 지표
- **최근 사항 3건**: 변경/자산등록/장애 각 도메인의 가장 최근 건을 한 줄씩 노출. 행을 클릭하면 세부사항이 펼쳐짐(정적 HTML은 아코디언 토글, Streamlit은 `st.expander`)
- **맨 하단 푸터**: 개인정보처리방침, 이용약관 하이퍼링크

## 파일 구성
이 폴더에는 **정적 HTML 버전**과 **Streamlit(Python) 버전** 두 가지 구현이 함께 있습니다. 실제 배포·서비스는 Streamlit 버전으로 하고, 정적 HTML 버전은 이미 CI로 등록되어 있어 그대로 남겨둔 상태입니다.

| 파일 | 설명 |
|---|---|
| `index.html` | (정적 HTML 버전) 대시보드 메인 화면 |
| `변경관리.html` / `장애관리.html` / `구성관리.html` | (정적 HTML 버전) 상단 메뉴 버튼이 연결되는 각 관리 페이지. "입력 화면은 추후 설계 예정" placeholder만 있음 |
| `style.css` | (정적 HTML 버전) 스타일 (다크/라이트 모드 자동 대응) |
| `nav.js` | (정적 HTML 버전) 모든 페이지가 공유하는 상단 메뉴바 렌더링. `renderNav(activeKey)` 호출로 현재 페이지 버튼을 활성 표시 |
| `script.js` | (정적 HTML 버전) index 화면의 총 자산수/카테고리 막대바/스코어보드 렌더링 |
| `data.js` | (정적 HTML 버전) 대시보드에 쓰이는 데이터 스냅샷 (CSV에서 집계한 값을 하드코딩) |
| `policy-modal.js` | (정적 HTML 버전) 개인정보처리방침 팝업(모달) 컴포넌트. 4개 메뉴 페이지 footer의 `id="privacy-policy-link"` 링크 클릭을 가로채 `개인정보처리방침.md` 본문을 팝업으로 띄움 |
| `개인정보처리방침.md` | 개인정보처리방침 원문(19개 조항). `policy-modal.js`의 `PRIVACY_SECTIONS` 배열이 이 문서를 그대로 옮긴 것이라, 본문 수정 시 두 파일을 함께 갱신해야 함(자동 연동 아님) |
| `홈.py` | (Streamlit 버전) 메인 화면. pandas로 CI/CHANGE/INCIDENT CSV를 직접 읽어 총 자산수·카테고리별 막대바(Altair)·스코어보드를 매번 최신값으로 렌더링(하드코딩 스냅샷 아님) |
| `pages/1_변경관리.py`, `pages/2_장애관리.py` | (Streamlit 버전) Streamlit 표준 멀티페이지 구조. 사이드바에 항상 노출되며 현재는 "입력 화면은 추후 설계 예정" placeholder만 있음 |
| `pages/3_구성관리.py` | (Streamlit 버전) `구성관리.html`의 "자산 배치도(3D)"·"데이터 모델 ERD" 두 패널을 `st.components.v1.html`(iframe)로 그대로 임베딩. 마크업/CSS를 이 파일에 다시 옮겨 적지 않고 `구성관리.html`+`style.css`를 실행 시점에 읽어와 재사용하므로 정적 HTML 버전을 고치면 Streamlit 버전도 함께 갱신됨(둘이 어긋날 일이 없음). CI 등록/조회 입력 화면 자체는 아직 placeholder |
| `../requirements.txt` (repo 루트) | Streamlit Cloud 배포용 의존성(`streamlit`, `pandas`, `altair`) |

## 데이터 출처 및 갱신 방법
`data.js`의 값은 아래 원본을 2026-07-11 기준으로 집계한 **스냅샷**이며, 자동 연동이 아닙니다. 원본이 바뀌면 수동으로 다시 집계해 `data.js`를 갱신해야 합니다.

| 지표 | 출처 | 비고 |
|---|---|---|
| 총 자산수 / 카테고리별 자산 현황 | `../3_구성관리/CI.csv` (310건, `CI_CATEGORY` 기준 집계) | 이 대시보드 자신(4건, `CFG_WEB_019`~`022`)도 CI로 등록되어 포함됨 |
| 변경건수 | `../1_변경관리/CHANGE.csv` (13건) | 이 대시보드 관련 건(`CHG_20260711_001`~`004`) 포함 |
| 장애건수 | `../2_장애관리/INCIDENT.csv` (1건) | 첫 실제 장애 `INC_20260711_001`(`CHG_20260711_003` 배포 중 발생한 CSV 파싱 장애) |
| 구성관리(추가) | `4` | 이 대시보드를 CI로 신규 등록한 건수(`CHG_20260711_001` 1건에 연결된 CI 4건)만 반영한 값. 과거/향후 전체 이력을 담은 로그는 아직 없음 |
| 구성관리(삭제) | `0` — 고정 | CI 삭제 이력을 추적할 로그가 아직 없음 |
| 최근 사항 3건 | `../1_변경관리/CHANGE.csv` / `../2_장애관리/INCIDENT.csv` 각 마지막 행 + 자산등록(고정) | 현황 스코어보드 아래에 변경/자산등록/장애 각 1건씩 노출, 행 클릭 시 세부사항 토글(`data.js`의 `recentItems`, `홈.py`는 `change_df.iloc[-1]`/`incident_df.iloc[-1]`로 매번 계산). 자산등록 건은 이력 로그가 없어 최초 등록(`CHG_20260711_001`)으로 고정 |

## 개인정보처리방침 / 이용약관
- **개인정보처리방침**: 원문을 `개인정보처리방침.md`로 작성 완료했습니다. 4개 메뉴 페이지(`index.html`/`변경관리.html`/`장애관리.html`/`구성관리.html`) footer의 "개인정보처리방침" 링크(`id="privacy-policy-link"`)를 누르면 `policy-modal.js`가 클릭을 가로채 별도 페이지 이동 없이 팝업(모달)으로 본문을 띄웁니다. `href="개인정보처리방침.html"`은 JS 미실행 환경 대비 폴백으로 남겨두었으나 실제 해당 HTML 파일은 없음(정상적으로는 항상 팝업으로 처리됨).
- **이용약관**: 아직 원고가 없어 `이용약관.html` 링크는 그대로 두었습니다(추후 원고 준비 시 같은 팝업 방식으로 맞출 예정).

## 구성관리 페이지(`구성관리.html` / `pages/3_구성관리.py`) 구성
`구성관리.html`은 더 이상 순수 placeholder가 아니라, 아래 두 시각 자료가 상단/하단에 배치되어 있습니다(CI 등록/조회 입력 화면 자체는 여전히 설계 전). 같은 내용이 Streamlit 배포판(`pages/3_구성관리.py`)에도 `st.components.v1.html`을 통해 그대로 임베딩되어, 실제 서비스 URL에서도 동일하게 보입니다.

- **상단 — 가상 5층 건물 자산 배치도(3D)**: `../3_구성관리/CI.csv`의 `OWNER_TEAM` 집계를 근거로 임의 구성한 배치도입니다(실제 사무실 위치와 무관, CSS 3D transform으로 구현). **5층 = 전산실(서버실) 고정**이며, 1~4층에는 나머지 부서를 업무 성격이 비슷한 단위로 묶어 배치했습니다.
  | 층 | 배치 | 근거(자산 건수) |
  |---|---|---|
  | 5F | 전산실(서버실) | 인프라운영팀/Infra_Team/Security_Team 소유 장비 225건(Storage/VM/Server/Switch/Network_Security/Network_Equipment/DMZ_Compute/Internal_Security_Sol/Security_Management) |
  | 4F | 인프라운영팀 · Infra_Team (사무실) | 228건(인프라운영팀 213 + Infra_Team 15) — 5층 전산실을 직접 관리하는 부서라 바로 아래층에 배치 |
  | 3F | 정보화기획팀 · Security_Team (사무실) | 41건(정보화기획팀 6 + Security_Team 35) |
  | 2F | AI융합사업팀 · 혁신성장팀 (사무실) | 24건(AI융합사업팀 21 + 혁신성장팀 3) |
  | 1F | 경영지원팀 (사무실 · 로비) | 17건 |

  각 층에 마우스를 올리면 담당 자산 상세 내역이 표시되고, 항상 보이는 하단 범례로도 층별 배치를 확인할 수 있습니다.
- **하단 — 데이터 모델 ERD**: [3_구성관리 README](../3_구성관리/README.md)의 ERD 요약(CI를 허브로 CHANGE_CI_MAP/INCIDENT_CI_MAP을 통해 CHANGE·INCIDENT와 N:M 연결)을 SVG+HTML 다이어그램으로 재구성했습니다. 원본은 2026-07-11 작성한 주간 보고서(`../4_경영관리/_업무보고/20260711_2주차_데이터모델ERD보고.pdf`)입니다.

## 이 대시보드 자신의 자산(CI) 등록
이 대시보드도 하나의 자산이라 [3_구성관리](../3_구성관리/README.md) CI 마스터에 등록했고, 최초 구축을 [1_변경관리](../1_변경관리/README.md) 변경 이력으로 남겼습니다. 이후 이 화면에 실질적인 수정이 생기면(입력 화면 추가 등) 같은 방식으로 새 CHANGE 티켓 + CHANGE_CI_MAP 행을 추가해 이력을 이어갑니다.

| CI_ID | 페이지 | 계층 |
|---|---|---|
| `CFG_WEB_019` | `index.html` (메인) | L1_PAGE |
| `CFG_WEB_020` | `변경관리.html` | L2_PAGE (부모: `CFG_WEB_019`) |
| `CFG_WEB_021` | `장애관리.html` | L2_PAGE (부모: `CFG_WEB_019`) |
| `CFG_WEB_022` | `구성관리.html` | L2_PAGE (부모: `CFG_WEB_019`) |

최초 구축 변경 티켓: `CHG_20260711_001` ([1_변경관리/CHANGE.csv](../1_변경관리/CHANGE.csv)), 연결 매핑: `MAP_0061`~`MAP_0064` ([변경히스토리/CHANGE_CI_MAP.csv](../1_변경관리/변경히스토리/CHANGE_CI_MAP.csv))

## 배포 (GitHub 연동 + Streamlit)

### GitHub
- 저장소: **https://github.com/hudsonkim77/wiki** (public, `main` 브랜치)
- `wiki` 전체가 그대로 하나의 GitHub 저장소입니다. 새 커밋을 만들면 `git push`로 반영됩니다.

### Streamlit Community Cloud 배포 절차
Streamlit은 파이썬 프레임워크라 정적 HTML을 그대로 올릴 수 없어서, 배포용으로 `홈.py`/`pages/`를 추가했습니다(위 파일 구성 참고). 배포는 아래 단계가 필요하고, 3번까지는 본인 GitHub 로그인 세션이 있어야 하는 단계라 직접 진행해야 합니다.

1. **https://share.streamlit.io** 접속 → GitHub 계정(`hudsonkim77`)으로 로그인
2. "Create app" → "Deploy a public app from GitHub"
3. Repository: `hudsonkim77/wiki`, Branch: `main`, **Main file path: `5_ITSM관리/홈.py`**
4. Deploy 클릭 — repo 루트의 `requirements.txt`(streamlit/pandas/altair)가 자동으로 설치됨

배포된 앱 URL이 나오면 이 표에 기록합니다.

| 배포일 | URL | 비고 |
|---|---|---|
| 2026-07-11 | https://3zunafjfayrwlpemrembwh.streamlit.app/ | Repository `hudsonkim77/wiki`, main file `5_ITSM관리/홈.py`. 배포 직후 카테고리 막대바가 개수 내림차순이 아니라 알파벳순으로 뜨는 버그 발견 → 정렬 수정 후 재배포로 해결(아래 변경 이력 참고) |

### 정적 HTML → Streamlit으로 옮기며 달라진 점
- **상단 메뉴바 → 좌측 사이드바**: Streamlit의 멀티페이지 앱은 사이드바에 페이지 목록을 자동으로 띄우는 방식이 기본이라, `index.html` 버전의 "어디서든 상단 메뉴 유지" 요구사항은 Streamlit에서는 "사이드바에 홈/변경관리/장애관리/구성관리가 항상 노출"되는 형태로 구현됩니다.
- **데이터 하드코딩 → 실시간 집계**: `data.js`는 특정 시점 값을 박아넣은 스냅샷이었지만, `홈.py`는 매 요청마다 `CI.csv`/`CHANGE.csv`/`INCIDENT.csv`를 직접 읽어 집계하므로 원본이 바뀌면 대시보드도 자동으로 갱신됩니다(단, 구성관리 추가/삭제 건수는 아직 전체 이력 로그가 없어 `홈.py`에도 상수로 남아 있음 — 아래 데이터 출처 표 참고).
- **카테고리 막대바**: Altair로 다시 그렸고 색상은 기존 8색 팔레트를 그대로 사용했습니다.
- 로컬에서 `streamlit run 5_ITSM관리/홈.py`로 직접 실행해 데이터·차트가 정상 렌더링되는 것을 확인했습니다.

## 참고 및 관리 방법
- 각 관리(변경/장애/구성관리) 페이지의 실제 입력 화면은 별도 설계 예정입니다. 설계가 끝나면 각 placeholder 페이지의 본문을 실제 화면으로 교체합니다(상단 메뉴바 이동은 이미 구현됨).
- 구성관리 추가/삭제 이력을 담는 전체 로그 테이블이 설계되면 `data.js`의 `ciAdded`/`ciRemoved` 값과 이 README의 데이터 출처 표를 함께 갱신합니다.
- 대시보드 화면 자체에 변화가 생기면(신규 페이지 추가, 레이아웃 변경 등) [3_구성관리](../3_구성관리/README.md) CI.csv와 [1_변경관리](../1_변경관리/README.md) CHANGE.csv/CHANGE_CI_MAP.csv에도 함께 반영합니다.

## 변경 이력
| 날짜 | 내용 | 작성자 |
|---|---|---|
| 2026-07-11 | `5_ITSM관리` 폴더 신설, 통합관리대시보드 소스(`index.html`/`style.css`/`script.js`/`data.js`) 최초 생성. 총 자산수·카테고리별 막대바·변경/장애/구성관리 스코어보드·정책 링크 푸터·상단 관리 메뉴바(입력창은 추후 설계) 구현 | Claude |
| 2026-07-11 | 카테고리별 막대바에 8색 순환 컬러 적용. 상단 메뉴바를 `nav.js` 공용 컴포넌트로 분리하고 `변경관리.html`/`장애관리.html`/`구성관리.html` placeholder 페이지를 신설해 실제 페이지 이동 구현(로고 클릭 시 항상 `index.html`로 복귀, 현재 페이지 버튼 활성 표시). 기존 toast 안내 방식은 제거 | Claude |
| 2026-07-11 | 통합관리대시보드 자신을 CI로 등록(`CFG_WEB_019`~`022`, 4건)하고 최초 구축을 변경 이력(`CHG_20260711_001`, `MAP_0061`~`0064`)으로 연결. `data.js`의 총 자산수(310)·변경건수(10)·구성관리(추가)(4)에 반영 | Claude |
| 2026-07-11 | `wiki` 저장소를 GitHub(`hudsonkim77/wiki`, public)에 연동·push. Streamlit 배포를 위해 `홈.py`+`pages/1_변경관리.py`·`2_장애관리.py`·`3_구성관리.py`(멀티페이지 앱)와 repo 루트 `requirements.txt`를 신규 추가하고 로컬에서 `streamlit run`으로 정상 동작 확인. 이 README에 GitHub 연동 정보와 Streamlit Community Cloud 배포 절차 기록 | Claude |
| 2026-07-11 | Streamlit Community Cloud에 실배포 완료(https://3zunafjfayrwlpemrembwh.streamlit.app/). 배포된 화면 확인 중 카테고리별 막대바가 `Y` 인코딩의 `sort="-x"`가 레이어(막대+값 라벨) 합성 시 의도대로 적용되지 않아 알파벳순으로 뜨는 버그 발견 → `sort=categories`(집계 시 이미 개수 내림차순으로 만든 리스트)로 명시해 수정. 로컬 재검증 후 push하여 Streamlit Cloud 자동 재배포 | Claude |
| 2026-07-11 | 카테고리별 자산 현황 막대바 라벨을 `CI_CATEGORY` 영문 코드에서 한글 표시명으로 변경(`index.html`/`script.js`/`data.js`/`홈.py` 전체 반영, 원본 `CI_CATEGORY` 값은 유지). `CHG_20260711_002`로 변경 이력 등록, GitHub push 후 Streamlit 자동 재배포 완료 | Claude |
| 2026-07-11 | 홈 대시보드 현황 스코어보드 하단에 "최근 변경 요약"(최신 CHANGE 티켓 제목/상세) 노출 추가 — 기존에는 변경건수만 숫자로 보여 실제 변경 내용이 화면에 드러나지 않던 문제 해결(`index.html`/`script.js`/`data.js`/`홈.py`). 구성관리.html에 가상 5층 건물 3D 자산 배치도(5층 전산실 고정)와 CI 허브 ERD 다이어그램 신설. 개인정보처리방침 원문을 `개인정보처리방침.md`로 작성하고 4개 메뉴 페이지 footer 링크를 `policy-modal.js` 팝업(모달) 방식으로 전환. `CHG_20260711_003`으로 변경 이력 등록, 대시보드 CI 4건(`CFG_WEB_019`~`022`) 모두 `CHANGE_REF` 갱신 | Claude |
| 2026-07-11 | **장애**: `CHG_20260711_003` 배포 직후 `CHANGE.csv`의 `RELATED_DESC` 필드에 쉼표가 포함됐으나 따옴표로 감싸지 않아 컬럼이 밀려 Streamlit `홈.py`가 `pandas.read_csv` 단계에서 `ParserError`로 다운(전체 화면 에러). 해당 필드를 따옴표로 감싸 즉시 복구하고 CI/CHANGE/INCIDENT/CHANGE_CI_MAP/INCIDENT_CI_MAP 전체를 pandas로 재검증 후 재배포(감지~복구 10분, SEV3). [2_장애관리](../2_장애관리/README.md)에 `INC_20260711_001`로 정식 등록(`CAUSED_BY_CHG_TICKET_ID`=`CHG_20260711_003`, `INCIDENT_CI_MAP`에 `MAP_0001`로 `CFG_WEB_019` 연결) | Claude |
| 2026-07-11 | 홈 대시보드의 "최근 변경 요약"(변경 1건만 노출)을 "최근 사항 3건"(변경/자산등록/장애 각 1건)으로 확장. 행 클릭 시 세부사항 토글(정적 HTML은 아코디언, Streamlit은 `st.expander`)(`index.html`/`script.js`/`data.js`/`style.css`/`홈.py`). `CHG_20260711_004`로 변경 이력 등록, `CFG_WEB_019`의 `CHANGE_REF` 갱신 | Claude |
| 2026-07-11 | `pages/3_구성관리.py`를 placeholder에서 `구성관리.html`의 3D 자산배치도/ERD 임베딩(`st.components.v1.html`)으로 교체해 Streamlit 실배포판에도 반영. 임베딩 과정에서 ERD 박스가 좁은 컨테이너 폭에서 텍스트가 잘리는 문제를 발견해 `erd-wrap` 세로 비율(46%→58%)을 수정하고, ERD 원본 PDF 링크를 상대경로 → GitHub 절대경로로 변경(iframe 안에서도 열리도록). `CHG_20260711_005`로 변경 이력 등록, `CFG_WEB_022`의 `CHANGE_REF` 갱신 | Claude |
