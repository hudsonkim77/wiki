import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
DEPLOY_CSV = WIKI_ROOT / "7_배포관리" / "DEPLOY.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["정기", "긴급", "롤백"]
STATUS_OPTIONS = ["계획", "빌드", "테스트", "배포완료", "롤백"]

LIST_COLUMNS = ["DEPLOY_ID", "DEPLOY_NAME", "DEPLOY_TYPE", "DEPLOY_STATUS", "PLANNED_DT", "DEPLOYED_DT", "OWNER_TEAM"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("배포관리")

st.subheader("배포 등록/조회")

deploy_df = load_df(DEPLOY_CSV)
status_values = deploy_df["DEPLOY_STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = deploy_df if selected_status == "전체" else deploy_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 배포 등록"):
        with st.form("add_deploy_form", clear_on_submit=True):
            deploy_name = st.text_input("DEPLOY_NAME *")
            deploy_type = st.selectbox("DEPLOY_TYPE", TYPE_OPTIONS)
            deploy_status = st.selectbox("DEPLOY_STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                planned_dt = st.text_input("PLANNED_DT (YYYY-MM-DD)")
                deployed_dt = st.text_input("DEPLOYED_DT (YYYY-MM-DD)")
                desc = st.text_area("DESC")
            submitted = st.form_submit_button("등록")
            if submitted:
                if not deploy_name.strip():
                    st.error("DEPLOY_NAME은 필수입니다.")
                else:
                    new_id = next_id(deploy_df, "DEPLOY_ID", "DEP")
                    new_row = {
                        "DEPLOY_ID": new_id, "DEPLOY_NAME": deploy_name, "DEPLOY_TYPE": deploy_type,
                        "DEPLOY_STATUS": deploy_status, "PLANNED_DT": planned_dt, "DEPLOYED_DT": deployed_dt,
                        "OWNER_TEAM": owner_team, "DESC": desc,
                    }
                    updated = pd.concat([deploy_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, DEPLOY_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 배포 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 배포가 없습니다.")
        else:
            del_options = {f"{r.DEPLOY_ID} — {r.DEPLOY_NAME}": r.DEPLOY_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 배포 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = deploy_df[deploy_df["DEPLOY_ID"] != selected_del_id]
                save_df(updated, DEPLOY_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("배포 등록/조회는 7_배포관리/DEPLOY.csv를 직접 수정합니다.")
