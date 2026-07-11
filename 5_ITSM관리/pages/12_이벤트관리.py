import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
EVENT_CSV = WIKI_ROOT / "12_이벤트관리" / "EVENT.csv"
CI_CSV = WIKI_ROOT / "3_구성관리" / "CI.csv"
OPS_CSV = WIKI_ROOT / "11_운영상태관리" / "OPS_STATUS.csv"
INCIDENT_CSV = WIKI_ROOT / "2_장애관리" / "INCIDENT.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["정보", "경고", "심각"]
STATUS_OPTIONS = ["발생", "확인중", "종료"]

LIST_COLUMNS = ["EVENT_ID", "EVENT_TITLE", "EVENT_TYPE", "EVENT_STATUS", "CI_ID", "DETECTED_DT", "ESCALATED_INCIDENT_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("이벤트관리")

st.subheader("이벤트 등록/조회")

event_df = load_df(EVENT_CSV)
status_values = event_df["EVENT_STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = event_df if selected_status == "전체" else event_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 이벤트 등록"):
        with st.form("add_event_form", clear_on_submit=True):
            event_title = st.text_input("EVENT_TITLE *")
            event_type = st.selectbox("EVENT_TYPE", TYPE_OPTIONS)
            event_status = st.selectbox("EVENT_STATUS", STATUS_OPTIONS)
            ci_id = st.selectbox("CI_ID (발생 자산)", fk_options(CI_CSV, "CI_ID"))
            with st.expander("추가 항목(선택)"):
                detected_dt = st.text_input("DETECTED_DT (YYYY-MM-DD HH:MM)")
                source_ops_id = st.selectbox("SOURCE_OPS_ID (감지 운영상태)", fk_options(OPS_CSV, "OPS_ID"))
                escalated_incident_id = st.selectbox(
                    "ESCALATED_INCIDENT_ID (확대된 장애)", fk_options(INCIDENT_CSV, "INCIDENT_ID")
                )
            submitted = st.form_submit_button("등록")
            if submitted:
                if not event_title.strip():
                    st.error("EVENT_TITLE은 필수입니다.")
                else:
                    new_id = next_id(event_df, "EVENT_ID", "EVT")
                    new_row = {
                        "EVENT_ID": new_id, "EVENT_TITLE": event_title, "EVENT_TYPE": event_type,
                        "CI_ID": "" if ci_id == "(없음)" else ci_id,
                        "SOURCE_OPS_ID": "" if source_ops_id == "(없음)" else source_ops_id,
                        "DETECTED_DT": detected_dt, "EVENT_STATUS": event_status,
                        "ESCALATED_INCIDENT_ID": "" if escalated_incident_id == "(없음)" else escalated_incident_id,
                    }
                    updated = pd.concat([event_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, EVENT_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 이벤트 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 이벤트가 없습니다.")
        else:
            del_options = {f"{r.EVENT_ID} — {r.EVENT_TITLE}": r.EVENT_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 이벤트 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = event_df[event_df["EVENT_ID"] != selected_del_id]
                save_df(updated, EVENT_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("이벤트 등록/조회는 12_이벤트관리/EVENT.csv를 직접 수정합니다.")
