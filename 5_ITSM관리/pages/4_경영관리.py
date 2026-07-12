from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("경영관리")


def _expected_password():
    # secrets.toml이 아예 없으면(로컬 초기 설정 전 등) st.secrets 접근 자체가 예외를 던진다.
    try:
        return st.secrets.get("MGMT_PASSWORD")
    except Exception:
        return None


def check_password():
    if st.session_state.get("mgmt_authed"):
        return True

    expected = _expected_password()
    if not expected:
        st.warning(
            "관리자가 아직 비밀번호(MGMT_PASSWORD)를 설정하지 않아 이 페이지를 열 수 없습니다. "
            ".streamlit/secrets.toml(로컬) 또는 Streamlit Cloud의 앱 설정 > Secrets(배포판)에 설정하세요."
        )
        return False

    st.subheader("🔒 접근 제한")
    st.caption("경영관리 업무보고는 비밀번호 확인 후 열람할 수 있습니다.")
    pw = st.text_input("비밀번호", type="password", key="mgmt_pw_input")
    if st.button("확인"):
        if pw == expected:
            st.session_state["mgmt_authed"] = True
            st.rerun()
        else:
            st.error("비밀번호가 올바르지 않습니다.")
    return False


if not check_password():
    st.stop()

st.caption("업무보고 열람 — 원본 카탈로그: ../4_경영관리/업무보고목록.md")

# 아래 목록은 4_경영관리/업무보고목록.md와 동일 내용을 유지해야 한다(자동 연동 아님).
# 원본 PDF가 저장소 파일이라 Streamlit Cloud에 별도 공개 URL이 없어 GitHub 절대경로로 연결한다.
st.markdown(
    "- [IT 자산 현황 브리핑](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_IT자산_현황_브리핑.pdf)\n"
    "- [데이터 모델 ERD 보고](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_2주차_데이터모델ERD보고.pdf)\n"
    "- [장애관리대장](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_장애관리대장.pdf)\n"
    "- [경위서 — ITSM 통합관리대시보드 서비스 장애](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_경위서_ITSM대시보드장애.pdf)\n"
    "- [경위서 — Streamlit 배포판 상단 로고 크기 미반영 반복](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_경위서_로고크기미반영.pdf)"
)
# 마크다운 링크는 Streamlit에서 같은 탭에 열려, 새 창(new window)으로 열어달라는 요청에 맞춰
# 이 링크만 raw HTML(target="_blank")로 별도 추가한다.
st.markdown(
    '- WBS: <a href="https://claude.ai/code/artifact/d32f4d77-b56e-4a11-8192-85a1c7e51c65" target="_blank" rel="noopener">'
    'ITIL v4 기반 IT서비스운영관리 WBS 및 진척현황</a>',
    unsafe_allow_html=True,
)
# ERD는 claude.ai 외부 링크가 아니라 앱 내부 페이지(pages/16_ERD.py)라 st.page_link로 연결한다
# (내부 페이지 이동은 Streamlit 라우팅을 타야 하므로 WBS처럼 raw <a href>를 쓰지 않음).
st.page_link("pages/16_ERD.py", label="ERD: 통합 데이터 모델 ERD(논리/물리)", icon="🗺️")

st.divider()
st.subheader("구축산출물")
st.caption("15페이지 CRUD 기능테스트 결과 기반 — 원본 카탈로그: ../4_경영관리/구축산출물목록.md")
# 아래 목록은 4_경영관리/구축산출물목록.md와 동일 내용을 유지해야 한다(자동 연동 아님).
st.markdown(
    "- [테스트결과서 - 기능테스트](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_테스트결과서-기능테스트.pdf)\n"
    "- [프로그램명세서](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_프로그램명세서.pdf)\n"
    "- [데이터베이스명세서](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_데이터베이스명세서.pdf)\n"
    "- [아키텍처결과서](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_아키텍처결과서.pdf)\n"
    "- [표준정의서(용어, 도메인)](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_표준정의서(용어_도메인).pdf)\n"
    "- [초기 베이스라인 정의서 v1.0](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/구축산출물/20260712_초기베이스라인정의서.pdf)"
)
