import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
SLA_CSV = WIKI_ROOT / "9_서비스수준관리" / "SLA.csv"
DEPLOY_CSV = WIKI_ROOT / "7_배포관리" / "DEPLOY.csv"

sys.path.insert(0, str(ROOT))
from column_labels import ko_labels  # noqa: E402
from crud_helpers import fk_options, load_df, next_id, save_df  # noqa: E402

METRIC_OPTIONS = ["가용성", "응답시간", "처리량", "오류율"]
STATUS_OPTIONS = ["정상", "주의", "위반"]

LIST_COLUMNS = ["SLA_ID", "SERVICE_NAME", "METRIC_TYPE", "TARGET_VALUE", "MEASURED_VALUE", "STATUS", "DEPLOY_ID"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("서비스수준관리")

st.subheader("SLA 등록/조회")

sla_df = load_df(SLA_CSV)
status_values = sla_df["STATUS"].replace("", "미정")
status_options = ["전체"] + sorted(status_values.unique().tolist())
selected_status = st.selectbox("상태 선택", options=status_options)

filtered = sla_df if selected_status == "전체" else sla_df[status_values == selected_status]
st.caption(f"{selected_status} — {len(filtered)}건")
st.dataframe(
    filtered[LIST_COLUMNS].rename(columns=ko_labels(LIST_COLUMNS)),
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ SLA 등록"):
        with st.form("add_sla_form", clear_on_submit=True):
            service_name = st.text_input("SERVICE_NAME *")
            metric_type = st.selectbox("METRIC_TYPE", METRIC_OPTIONS)
            target_value = st.text_input("TARGET_VALUE")
            status = st.selectbox("STATUS", STATUS_OPTIONS)
            owner_team = st.text_input("OWNER_TEAM")
            with st.expander("추가 항목(선택)"):
                period = st.text_input("PERIOD (예: 월간)")
                measured_value = st.text_input("MEASURED_VALUE")
                deploy_id = st.selectbox("DEPLOY_ID (모니터링 대상 배포)", fk_options(DEPLOY_CSV, "DEPLOY_ID"))
            submitted = st.form_submit_button("등록")
            if submitted:
                if not service_name.strip():
                    st.error("SERVICE_NAME은 필수입니다.")
                else:
                    new_id = next_id(sla_df, "SLA_ID", "SLA")
                    new_row = {
                        "SLA_ID": new_id, "SERVICE_NAME": service_name, "METRIC_TYPE": metric_type,
                        "TARGET_VALUE": target_value, "PERIOD": period, "MEASURED_VALUE": measured_value,
                        "STATUS": status, "OWNER_TEAM": owner_team,
                        "DEPLOY_ID": "" if deploy_id == "(없음)" else deploy_id,
                    }
                    updated = pd.concat([sla_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_df(updated, SLA_CSV)
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ SLA 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 SLA가 없습니다.")
        else:
            del_options = {f"{r.SLA_ID} — {r.SERVICE_NAME}": r.SLA_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 SLA 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                updated = sla_df[sla_df["SLA_ID"] != selected_del_id]
                save_df(updated, SLA_CSV)
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("SLA 등록/조회는 9_서비스수준관리/SLA.csv를 직접 수정합니다.")
