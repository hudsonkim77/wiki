import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
BASELINE_CSV = WIKI_ROOT / "10_형상관리" / "BASELINE.csv"
PROBLEM_CSV = WIKI_ROOT / "6_문제관리" / "PROBLEM.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["코드", "문서", "구성"]
STATUS_OPTIONS = ["초안", "검토중", "승인", "폐기"]

LIST_COLUMNS = ["BASELINE_ID", "BASELINE_NAME", "VERSION", "BASELINE_TYPE", "STATUS", "CREATED_DT", "RESOLVED_PROBLEM_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("형상관리")

st.subheader("베이스라인 등록/조회")

baseline_df = load_df(BASELINE_CSV)
status_values = baseline_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = baseline_df if selected_status == "전체" else baseline_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 베이스라인 등록"):
        with st.form("add_baseline_form", clear_on_submit=True):
            baseline_name = st.text_input("BASELINE_NAME *")
            version = st.text_input("VERSION")
            baseline_type = st.selectbox("BASELINE_TYPE", TYPE_OPTIONS)
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                created_dt = st.text_input("CREATED_DT (YYYY-MM-DD)")
                approved_dt = st.text_input("APPROVED_DT (YYYY-MM-DD)")
                resolved_problem_id = st.selectbox(
                    "RESOLVED_PROBLEM_ID (이 베이스라인으로 조치된 문제)",
                    fk_options(PROBLEM_CSV, "PROBLEM_ID"),
                )
            submitted = st.form_submit_button("등록")
            if submitted:
                if not baseline_name.strip():
                    st.error("BASELINE_NAME은 필수입니다.")
                else:
                    new_id = next_id(baseline_df, "BASELINE_ID", "BSL")
                    new_row = {
                        "BASELINE_ID": new_id, "BASELINE_NAME": baseline_name, "VERSION": version,
                        "BASELINE_TYPE": baseline_type, "STATUS": status, "CREATED_DT": created_dt,
                        "APPROVED_DT": approved_dt, "OWNER_TEAM": owner_team,
                        "RESOLVED_PROBLEM_ID": "" if resolved_problem_id == "(없음)" else resolved_problem_id,
                    }
                    updated = pd.concat([baseline_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, BASELINE_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 베이스라인 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 베이스라인이 없습니다.")
        else:
            del_options = {f"{r.BASELINE_ID} — {r.BASELINE_NAME}": r.BASELINE_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 베이스라인 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = baseline_df[baseline_df["BASELINE_ID"] != selected_del_id]
                save_df(updated, BASELINE_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("베이스라인 등록/조회는 10_형상관리/BASELINE.csv를 직접 수정합니다.")
