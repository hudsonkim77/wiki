from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("경영관리")
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
