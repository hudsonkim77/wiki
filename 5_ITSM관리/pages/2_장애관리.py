import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
INCIDENT_CSV = WIKI_ROOT / "2_장애관리" / "INCIDENT.csv"
CHANGE_CSV = WIKI_ROOT / "1_변경관리" / "CHANGE.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

SEVERITY_OPTIONS = ["SEV1", "SEV2", "SEV3", "SEV4"]
STATUS_OPTIONS = ["등록", "조사중", "처리중", "종료"]

LIST_COLUMNS = ["INCIDENT_ID", "INCIDENT_TITLE", "SEVERITY", "INCIDENT_STATUS", "DETECTED_DT", "RESOLVED_DT", "CAUSED_BY_CHG_TICKET_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("장애관리")

st.subheader("장애 등록/조회")

incident_df = load_df(INCIDENT_CSV)
status_values = incident_df["INCIDENT_STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = incident_df if selected_status == "전체" else incident_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 장애 등록"):
        with st.form("add_incident_form", clear_on_submit=True):
            incident_title = st.text_input("INCIDENT_TITLE *")
            severity = st.selectbox("SEVERITY", SEVERITY_OPTIONS)
            incident_status = st.selectbox("INCIDENT_STATUS", STATUS_OPTIONS)
            handler_id = st.text_input("HANDLER_ID", value="USR_001")
            with st.expander("추가 항목(선택)"):
                detected_dt = st.text_input("DETECTED_DT (YYYY-MM-DD HH:MM)")
                resolved_dt = st.text_input("RESOLVED_DT (YYYY-MM-DD HH:MM)")
                root_cause = st.text_area("ROOT_CAUSE")
                action_taken = st.text_area("ACTION_TAKEN")
                caused_by_chg = st.selectbox(
                    "CAUSED_BY_CHG_TICKET_ID (원인이 된 변경)",
                    fk_options(CHANGE_CSV, "CHG_TICKET_ID"),
                )
            submitted = st.form_submit_button("등록")
            if submitted:
                if not incident_title.strip():
                    st.error("INCIDENT_TITLE은 필수입니다.")
                else:
                    new_id = next_id(incident_df, "INCIDENT_ID", "INC")
                    new_row = {
                        "INCIDENT_ID": new_id, "INCIDENT_TITLE": incident_title, "SEVERITY": severity,
                        "DETECTED_DT": detected_dt, "RESOLVED_DT": resolved_dt, "ROOT_CAUSE": root_cause,
                        "ACTION_TAKEN": action_taken, "HANDLER_ID": handler_id,
                        "INCIDENT_STATUS": incident_status,
                        "CAUSED_BY_CHG_TICKET_ID": "" if caused_by_chg == "(없음)" else caused_by_chg,
                    }
                    updated = pd.concat([incident_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, INCIDENT_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 장애 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 장애가 없습니다.")
        else:
            del_options = {f"{r.INCIDENT_ID} — {r.INCIDENT_TITLE}": r.INCIDENT_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 장애 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = incident_df[incident_df["INCIDENT_ID"] != selected_del_id]
                save_df(updated, INCIDENT_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("장애 등록/조회는 2_장애관리/INCIDENT.csv를 직접 수정합니다(별도 장애보고서 문서 대신 이 CRUD 화면으로 갈음).")
