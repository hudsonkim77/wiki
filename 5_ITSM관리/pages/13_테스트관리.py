import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
TEST_CSV = WIKI_ROOT / "13_테스트관리" / "TEST_CASE.csv"
DEPLOY_CSV = WIKI_ROOT / "7_배포관리" / "DEPLOY.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

TYPE_OPTIONS = ["기능테스트", "회귀테스트", "성능테스트"]
RESULT_OPTIONS = ["PASS", "FAIL", "보류"]

LIST_COLUMNS = ["TEST_ID", "DEPLOY_ID", "TEST_TYPE", "TEST_RESULT", "TESTED_DT", "TESTER_TEAM", "NOTE"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("테스트관리")

st.subheader("테스트 등록/조회")

test_df = load_df(TEST_CSV)
result_values = test_df["TEST_RESULT"].replace("", "미정")
result_options = ["전체"] + sorted(result_values.unique().tolist())
selected_result = st.selectbox("결과 선택", options=result_options)

filtered = test_df if selected_result == "전체" else test_df[result_values == selected_result]
st.caption(f"{selected_result} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ 테스트 등록"):
        with st.form("add_test_form", clear_on_submit=True):
            deploy_id = st.selectbox("DEPLOY_ID (검증 대상 배포) *", fk_options(DEPLOY_CSV, "DEPLOY_ID"))
            test_type = st.selectbox("TEST_TYPE", TYPE_OPTIONS)
            test_result = st.selectbox("TEST_RESULT", RESULT_OPTIONS)
            tester_team = st.text_input("TESTER_TEAM")
            with st.expander("추가 항목(선택)"):
                tested_dt = st.text_input("TESTED_DT (YYYY-MM-DD)")
                note = st.text_area("NOTE")
            submitted = st.form_submit_button("등록")
            if submitted:
                if deploy_id == "(없음)":
                    st.error("DEPLOY_ID는 필수입니다.")
                else:
                    new_id = next_id(test_df, "TEST_ID", "TST")
                    new_row = {
                        "TEST_ID": new_id, "DEPLOY_ID": deploy_id, "TEST_TYPE": test_type,
                        "TEST_RESULT": test_result, "TESTED_DT": tested_dt, "TESTER_TEAM": tester_team,
                        "NOTE": note,
                    }
                    updated = pd.concat([test_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, TEST_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ 테스트 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 테스트가 없습니다.")
        else:
            del_options = {f"{r.TEST_ID} — {r.DEPLOY_ID}": r.TEST_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 테스트 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = test_df[test_df["TEST_ID"] != selected_del_id]
                save_df(updated, TEST_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("테스트 등록/조회는 13_테스트관리/TEST_CASE.csv를 직접 수정합니다.")
