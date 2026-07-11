import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
REQUEST_CSV = WIKI_ROOT / "8_요청관리" / "REQUEST.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["서비스요청", "정보요청", "접근권한요청", "기타"]
STATUS_OPTIONS = ["접수", "처리중", "완료", "반려"]

LIST_COLUMNS = ["REQ_ID", "REQ_TITLE", "REQ_TYPE", "STATUS", "REQUESTED_DT", "COMPLETED_DT", "ASSIGNED_TEAM"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("요청관리")

st.subheader("요청 등록/조회")

request_df = load_df(REQUEST_CSV)
status_values = request_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = request_df if selected_status == "전체" else request_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 요청 등록"):
        with st.form("add_request_form", clear_on_submit=True):
            req_title = st.text_input("REQ_TITLE *")
            req_type = st.selectbox("REQ_TYPE", TYPE_OPTIONS)
            requester_id = st.text_input("REQUESTER_ID", value="USR_001")
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            assigned_team = st.text_input("ASSIGNED_TEAM")
            with st.expander("추가 항목(선택)"):
                requested_dt = st.text_input("REQUESTED_DT (YYYY-MM-DD)")
                completed_dt = st.text_input("COMPLETED_DT (YYYY-MM-DD)")
                desc = st.text_area("DESC")
            submitted = st.form_submit_button("등록")
            if submitted:
                if not req_title.strip():
                    st.error("REQ_TITLE은 필수입니다.")
                else:
                    new_id = next_id(request_df, "REQ_ID", "REQ")
                    new_row = {
                        "REQ_ID": new_id, "REQ_TITLE": req_title, "REQ_TYPE": req_type,
                        "REQUESTER_ID": requester_id, "STATUS": status, "REQUESTED_DT": requested_dt,
                        "COMPLETED_DT": completed_dt, "ASSIGNED_TEAM": assigned_team, "DESC": desc,
                    }
                    updated = pd.concat([request_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, REQUEST_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 요청 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 요청이 없습니다.")
        else:
            del_options = {f"{r.REQ_ID} — {r.REQ_TITLE}": r.REQ_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 요청 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = request_df[request_df["REQ_ID"] != selected_del_id]
                save_df(updated, REQUEST_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("요청 등록/조회는 8_요청관리/REQUEST.csv를 직접 수정합니다.")
