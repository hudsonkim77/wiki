import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
INTERFACE_CSV = WIKI_ROOT / "14_연계관리" / "INTERFACE.csv"
TEST_CSV = WIKI_ROOT / "13_테스트관리" / "TEST_CASE.csv"
BASELINE_CSV = WIKI_ROOT / "10_형상관리" / "BASELINE.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

STATUS_OPTIONS = ["정상", "점검중", "중단"]

LIST_COLUMNS = ["INTERFACE_ID", "INTERFACE_NAME", "EXTERNAL_SYSTEM_NAME", "STATUS", "LAST_CHECK_DT", "VALIDATED_BY_TEST_ID", "BASELINE_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("연계관리")

st.subheader("연계 등록/조회")

interface_df = load_df(INTERFACE_CSV)
status_values = interface_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = interface_df if selected_status == "전체" else interface_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 연계 등록"):
        with st.form("add_interface_form", clear_on_submit=True):
            interface_name = st.text_input("INTERFACE_NAME *")
            external_system_name = st.text_input("EXTERNAL_SYSTEM_NAME")
            protocol = st.text_input("PROTOCOL (예: REST API, SFTP, DB Link)")
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                last_check_dt = st.text_input("LAST_CHECK_DT (YYYY-MM-DD)")
                validated_by_test_id = st.selectbox(
                    "VALIDATED_BY_TEST_ID (검증 테스트)", fk_options(TEST_CSV, "TEST_ID")
                )
                baseline_id = st.selectbox("BASELINE_ID (연동 버전)", fk_options(BASELINE_CSV, "BASELINE_ID"))
            submitted = st.form_submit_button("등록")
            if submitted:
                if not interface_name.strip():
                    st.error("INTERFACE_NAME은 필수입니다.")
                else:
                    new_id = next_id(interface_df, "INTERFACE_ID", "INTF")
                    new_row = {
                        "INTERFACE_ID": new_id, "INTERFACE_NAME": interface_name,
                        "EXTERNAL_SYSTEM_NAME": external_system_name, "PROTOCOL": protocol,
                        "STATUS": status, "LAST_CHECK_DT": last_check_dt, "OWNER_TEAM": owner_team,
                        "VALIDATED_BY_TEST_ID": "" if validated_by_test_id == "(없음)" else validated_by_test_id,
                        "BASELINE_ID": "" if baseline_id == "(없음)" else baseline_id,
                    }
                    updated = pd.concat([interface_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, INTERFACE_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 연계 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 연계가 없습니다.")
        else:
            del_options = {f"{r.INTERFACE_ID} — {r.INTERFACE_NAME}": r.INTERFACE_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 연계 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = interface_df[interface_df["INTERFACE_ID"] != selected_del_id]
                save_df(updated, INTERFACE_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("연계 등록/조회는 14_연계관리/INTERFACE.csv를 직접 수정합니다.")
