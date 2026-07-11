from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))

st.title("장애관리")
st.info("입력 화면은 아직 설계 전입니다. 설계가 끝나면 이 페이지에 장애 등록/조회 화면이 들어갑니다.")
