from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent


def render_domain_page(title, readme_rel, tables):
    """신규 도메인(6~15번 폴더)용 최소 조회 화면. README 요약 + CSV 테이블만 보여주는
    읽기 전용 화면이며, 등록/조회 CRUD는 각 도메인이 목표 진척률에 도달한 뒤 추가한다."""
    st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
    st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)
    st.title(title)

    readme_path = WIKI_ROOT / readme_rel
    if readme_path.exists():
        with st.expander("도메인 설명 (README)", expanded=False):
            st.markdown(readme_path.read_text(encoding="utf-8"))

    for label, rel_path in tables:
        csv_path = WIKI_ROOT / rel_path
        st.subheader(label)
        if csv_path.exists():
            df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
            st.caption(f"{csv_path.relative_to(WIKI_ROOT)} — {len(df)}건")
            if len(df):
                st.dataframe(df, width="stretch", hide_index=True)
            else:
                st.caption("스키마만 반영되어 있고 실데이터는 아직 없습니다.")
        else:
            st.caption("파일 없음")
