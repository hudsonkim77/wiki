import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
BACKUP_CSV = WIKI_ROOT / "15_백업관리" / "BACKUP.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["백업", "복원"]
STATUS_OPTIONS = ["성공", "실패", "진행중"]

LIST_COLUMNS = ["BACKUP_ID", "ACTION_TYPE", "BACKUP_DT", "STATUS", "RETENTION_UNTIL_DT", "RESTORED_FROM_BACKUP_ID", "OWNER_TEAM"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("백업관리")

st.subheader("백업 등록/조회")

backup_df = load_df(BACKUP_CSV)
status_values = backup_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = backup_df if selected_status == "전체" else backup_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 백업 등록"):
        with st.form("add_backup_form", clear_on_submit=True):
            action_type = st.selectbox("ACTION_TYPE", TYPE_OPTIONS)
            backup_dt = st.text_input("BACKUP_DT (YYYY-MM-DD) *")
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                retention_until_dt = st.text_input("RETENTION_UNTIL_DT (YYYY-MM-DD)")
                restore_options = ["(없음)"] + backup_df["BACKUP_ID"].tolist()
                restored_from_backup_id = st.selectbox("RESTORED_FROM_BACKUP_ID (복원 원본)", restore_options)
            submitted = st.form_submit_button("등록")
            if submitted:
                if not backup_dt.strip():
                    st.error("BACKUP_DT는 필수입니다.")
                else:
                    new_id = next_id(backup_df, "BACKUP_ID", "BAK")
                    new_row = {
                        "BACKUP_ID": new_id, "ACTION_TYPE": action_type, "BACKUP_DT": backup_dt,
                        "STATUS": status, "RETENTION_UNTIL_DT": retention_until_dt,
                        "RESTORED_FROM_BACKUP_ID": "" if restored_from_backup_id == "(없음)" else restored_from_backup_id,
                        "OWNER_TEAM": owner_team,
                    }
                    updated = pd.concat([backup_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, BACKUP_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 백업 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 백업이 없습니다.")
        else:
            del_options = {f"{r.BACKUP_ID} — {r.ACTION_TYPE} ({r.BACKUP_DT})": r.BACKUP_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 백업 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = backup_df[backup_df["BACKUP_ID"] != selected_del_id]
                save_df(updated, BACKUP_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("백업 등록/조회는 15_백업관리/BACKUP.csv를 직접 수정합니다.")
