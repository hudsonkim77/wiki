import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
PROBLEM_CSV = WIKI_ROOT / "6_문제관리" / "PROBLEM.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["REACTIVE", "PROACTIVE"]
STATUS_OPTIONS = ["등록", "조사중", "근본원인식별", "영구조치", "종료"]

LIST_COLUMNS = ["PROBLEM_ID", "PROBLEM_TITLE", "PROBLEM_TYPE", "STATUS", "DETECTED_DT", "RESOLVED_DT", "OWNER_TEAM"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("문제관리")

st.subheader("문제 등록/조회")

problem_df = load_df(PROBLEM_CSV)
status_values = problem_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = problem_df if selected_status == "전체" else problem_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 문제 등록"):
        with st.form("add_problem_form", clear_on_submit=True):
            problem_title = st.text_input("PROBLEM_TITLE *")
            problem_type = st.selectbox("PROBLEM_TYPE", TYPE_OPTIONS)
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                detected_dt = st.text_input("DETECTED_DT (YYYY-MM-DD)")
                resolved_dt = st.text_input("RESOLVED_DT (YYYY-MM-DD)")
                root_cause = st.text_area("ROOT_CAUSE")
                workaround = st.text_area("WORKAROUND")
                permanent_fix = st.text_area("PERMANENT_FIX")
            submitted = st.form_submit_button("등록")
            if submitted:
                if not problem_title.strip():
                    st.error("PROBLEM_TITLE은 필수입니다.")
                else:
                    new_id = next_id(problem_df, "PROBLEM_ID", "PRB")
                    new_row = {
                        "PROBLEM_ID": new_id, "PROBLEM_TITLE": problem_title, "PROBLEM_TYPE": problem_type,
                        "ROOT_CAUSE": root_cause, "WORKAROUND": workaround, "PERMANENT_FIX": permanent_fix,
                        "STATUS": status, "DETECTED_DT": detected_dt, "RESOLVED_DT": resolved_dt,
                        "OWNER_TEAM": owner_team,
                    }
                    updated = pd.concat([problem_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, PROBLEM_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 문제 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 문제가 없습니다.")
        else:
            del_options = {f"{r.PROBLEM_ID} — {r.PROBLEM_TITLE}": r.PROBLEM_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 문제 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = problem_df[problem_df["PROBLEM_ID"] != selected_del_id]
                save_df(updated, PROBLEM_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("문제 등록/조회는 6_문제관리/PROBLEM.csv를 직접 수정합니다.")
