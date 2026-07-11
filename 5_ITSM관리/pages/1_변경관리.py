import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
CHANGE_CSV = WIKI_ROOT / "1_변경관리" / "CHANGE.csv"
INCIDENT_CSV = WIKI_ROOT / "2_장애관리" / "INCIDENT.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

STATUS_OPTIONS = ["등록", "검토중", "승인", "적용완료", "보류", "롤백"]
TYPE_OPTIONS = ["표준", "긴급", "비상"]
IMPACT_OPTIONS = ["낮음", "중간", "높음"]

LIST_COLUMNS = ["CHG_TICKET_ID", "CHG_TITLE", "CHG_TYPE", "CHG_STATUS", "IMPACT_LEVEL", "APPLIED_DT", "TRIGGERED_BY_INCIDENT_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("변경관리")

st.subheader("변경요청 등록/조회")

change_df = load_df(CHANGE_CSV)
status_values = change_df["CHG_STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = change_df if selected_status == "전체" else change_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 변경요청 등록"):
        with st.form("add_change_form", clear_on_submit=True):
            chg_title = st.text_input("CHG_TITLE *")
            chg_type = st.selectbox("CHG_TYPE", TYPE_OPTIONS)
            request_team = st.text_input("REQUEST_TEAM")
            requester_id = st.text_input("REQUESTER_ID", value="USR_001")
            approver_id = st.text_input("APPROVER_ID", value="USR_001")
            chg_status = st.selectbox("CHG_STATUS", STATUS_OPTIONS)
            impact_level = st.selectbox("IMPACT_LEVEL", IMPACT_OPTIONS)
            with st.expander("추가 항목(선택)"):
                planned_dt = st.text_input("PLANNED_DT (YYYY-MM-DD)")
                applied_dt = st.text_input("APPLIED_DT (YYYY-MM-DD)")
                rollback_yn = st.selectbox("ROLLBACK_YN", ["N", "Y"])
                related_desc = st.text_area("RELATED_DESC")
                triggered_by = st.selectbox(
                    "TRIGGERED_BY_INCIDENT_ID (이 변경을 촉발한 장애)",
                    fk_options(INCIDENT_CSV, "INCIDENT_ID"),
                )
            submitted = st.form_submit_button("등록")
            if submitted:
                if not chg_title.strip():
                    st.error("CHG_TITLE은 필수입니다.")
                else:
                    new_ticket_id = next_id(change_df, "CHG_TICKET_ID", "CHG")
                    new_row = {
                        "CHG_TICKET_ID": new_ticket_id, "CHG_TITLE": chg_title, "CHG_TYPE": chg_type,
                        "REQUEST_TEAM": request_team, "REQUESTER_ID": requester_id,
                        "APPROVER_ID": approver_id, "CHG_STATUS": chg_status,
                        "PLANNED_DT": planned_dt, "APPLIED_DT": applied_dt,
                        "ROLLBACK_YN": rollback_yn, "IMPACT_LEVEL": impact_level,
                        "RELATED_DESC": related_desc,
                        "TRIGGERED_BY_INCIDENT_ID": "" if triggered_by == "(없음)" else triggered_by,
                    }
                    updated = pd.concat([change_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, CHANGE_CSV)
                    st.success(f"{new_ticket_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 변경요청 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 변경요청이 없습니다.")
        else:
            del_options = {f"{r.CHG_TICKET_ID} — {r.CHG_TITLE}": r.CHG_TICKET_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 변경요청 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = change_df[change_df["CHG_TICKET_ID"] != selected_del_id]
                save_df(updated, CHANGE_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("변경요청 등록/조회는 1_변경관리/CHANGE.csv를 직접 수정합니다(별도 변경요청서 문서 대신 이 CRUD 화면으로 갈음).")
