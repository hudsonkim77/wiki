import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
OPS_CSV = WIKI_ROOT / "11_운영상태관리" / "OPS_STATUS.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import load_df, next_id, save_df  # noqa: E402

STATUS_OPTIONS = ["정상", "경고", "장애"]

LIST_COLUMNS = ["OPS_ID", "CHECK_DT", "STATUS", "METRIC_SUMMARY", "NOTE"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("운영상태관리")

st.subheader("운영상태 등록/조회")

ops_df = load_df(OPS_CSV)
status_values = ops_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = ops_df if selected_status == "전체" else ops_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 운영상태 등록"):
        with st.form("add_ops_form", clear_on_submit=True):
            check_dt = st.text_input("CHECK_DT (YYYY-MM-DD HH:MM) *")
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            metric_summary = st.text_input("METRIC_SUMMARY (예: CPU 42%, 메모리 58%)")
            note = st.text_area("NOTE")
            submitted = st.form_submit_button("등록")
            if submitted:
                if not check_dt.strip():
                    st.error("CHECK_DT는 필수입니다.")
                else:
                    new_id = next_id(ops_df, "OPS_ID", "OPS")
                    new_row = {
                        "OPS_ID": new_id, "CHECK_DT": check_dt, "STATUS": status,
                        "METRIC_SUMMARY": metric_summary, "NOTE": note,
                    }
                    updated = pd.concat([ops_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, OPS_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 운영상태 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 운영상태 기록이 없습니다.")
        else:
            del_options = {f"{r.OPS_ID} — {r.CHECK_DT}": r.OPS_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 기록 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = ops_df[ops_df["OPS_ID"] != selected_del_id]
                save_df(updated, OPS_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("운영상태 등록/조회는 11_운영상태관리/OPS_STATUS.csv를 직접 수정합니다.")
