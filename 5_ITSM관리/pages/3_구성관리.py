import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
WIKI_ROOT = ROOT.parent
STYLE_CSS = ROOT / "style.css"
CI_HTML = ROOT / "구성관리.html"
CI_CSV = WIKI_ROOT / "3_구성관리" / "CI.csv"
CI_HISTORY_CSV = WIKI_ROOT / "3_구성관리" / "구성이력" / "CI_HISTORY.csv"

sys.path.insert(0, str(ROOT))
from labels import CATEGORY_LABELS_KO  # noqa: E402

HISTORY_COLUMNS = ["HISTORY_ID", "CI_ID", "CI_NAME", "CI_CATEGORY", "ACTION", "ACTION_DT", "ACTION_BY", "NOTE"]

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))

st.title("구성관리")


def _extract_section(html, index):
    parts = html.split('<section class="panel">')
    body = parts[index]
    return body[: body.rfind("</section>") + len("</section>")]


# 정적 HTML 버전(구성관리.html)의 "자산 배치도(3D)" + "데이터 모델 ERD" 두 패널을 그대로
# 잘라내 iframe에 임베딩한다. 마크업/CSS를 이 파일에 다시 옮겨 적지 않는 이유는, 두 버전이
# 어긋나지 않도록 구성관리.html + style.css를 유일한 원본으로 유지하기 위함이다.
html = CI_HTML.read_text(encoding="utf-8")
building_section = _extract_section(html, 1)
erd_section = _extract_section(html, 2)
css = STYLE_CSS.read_text(encoding="utf-8")

embed = f"""
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<style>{css}</style>
</head>
<body>
<main>
{building_section}
{erd_section}
</main>
</body>
</html>
"""

components.html(embed, height=1450, scrolling=True)


# ---------------------------------------------------------------------------
# CI 등록/조회 — 카테고리 선택 → 목록 조회, 추가/삭제(CI.csv를 직접 수정, CI_HISTORY.csv에 이력 기록)
# ---------------------------------------------------------------------------

def load_ci():
    return pd.read_csv(CI_CSV, dtype=str, keep_default_na=False)


def save_ci(df):
    df.to_csv(CI_CSV, index=False)


def load_history():
    if CI_HISTORY_CSV.exists():
        return pd.read_csv(CI_HISTORY_CSV, dtype=str, keep_default_na=False)
    return pd.DataFrame(columns=HISTORY_COLUMNS)


def append_history(ci_id, ci_name, category, action, note):
    hist = load_history()
    n = len(hist) + 1
    new_row = {
        "HISTORY_ID": f"HIST_{n:04d}",
        "CI_ID": ci_id,
        "CI_NAME": ci_name,
        "CI_CATEGORY": category,
        "ACTION": action,
        "ACTION_DT": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ACTION_BY": "USR_001",
        "NOTE": note,
    }
    hist = pd.concat([hist, pd.DataFrame([new_row])], ignore_index=True)
    hist.to_csv(CI_HISTORY_CSV, index=False)


def next_ci_id(df):
    existing = df["CI_ID"].str.extract(r"^CI_NEW_(\d+)$")[0].dropna().astype(int)
    n = (existing.max() + 1) if len(existing) else 1
    return f"CI_NEW_{n:04d}"


st.subheader("CI 등록/조회")

ci_df = load_ci()
categories = sorted(ci_df["CI_CATEGORY"].dropna().unique().tolist())
category_options = {f"{CATEGORY_LABELS_KO.get(c, c)} ({c})": c for c in categories}
selected_label = st.selectbox("카테고리 선택", options=list(category_options.keys()))
selected_category = category_options[selected_label]

filtered = ci_df[ci_df["CI_CATEGORY"] == selected_category]
st.caption(f"{selected_label} — {len(filtered)}건")
st.dataframe(
    filtered[["CI_ID", "CI_NAME", "OWNER_TEAM", "ADMIN_USER_ID", "STATUS", "INST_DT"]],
    width="stretch",
    hide_index=True,
)

col_add, col_del = st.columns(2)

with col_add:
    with st.expander("➕ CI 추가"):
        with st.form("add_ci_form", clear_on_submit=True):
            ci_name = st.text_input("CI_NAME *")
            ci_type = st.text_input("CI_TYPE", value=selected_category)
            owner_team = st.text_input("OWNER_TEAM")
            admin_user = st.text_input("ADMIN_USER_ID")
            status = st.selectbox("STATUS", ["OPERATIONAL", "Active", "STANDBY"])
            with st.expander("추가 항목(선택)"):
                host_name = st.text_input("HOST_NAME")
                location = st.text_input("LOCATION_OR_URL")
                ip_addr = st.text_input("IP_ADDRESS")
                os_version = st.text_input("OS_VERSION")
                serial_num = st.text_input("SERIAL_NUM")
                parent_ci = st.text_input("PARENT_CI_ID")
                depth_level = st.text_input("DEPTH_LEVEL", value="1")
                chg_ticket = st.text_input("CHG_TICKET_ID")
            submitted = st.form_submit_button("등록")
            if submitted:
                if not ci_name.strip():
                    st.error("CI_NAME은 필수입니다.")
                else:
                    new_id = next_ci_id(ci_df)
                    new_row = {
                        "CI_ID": new_id, "CI_NAME": ci_name, "HOST_NAME": host_name,
                        "CI_TYPE": ci_type, "CI_CATEGORY": selected_category,
                        "DEPTH_LEVEL": depth_level, "PARENT_CI_ID": parent_ci,
                        "LOCATION_OR_URL": location, "IP_ADDRESS": ip_addr,
                        "OS_VERSION": os_version, "SERIAL_NUM": serial_num,
                        "OWNER_TEAM": owner_team, "ADMIN_USER_ID": admin_user,
                        "STATUS": status, "INST_DT": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "CHG_TICKET_ID": chg_ticket,
                    }
                    updated = pd.concat([ci_df, pd.DataFrame([new_row])], ignore_index=True)
                    save_ci(updated)
                    append_history(new_id, ci_name, selected_category, "ADDED", "Streamlit CI 등록화면을 통해 추가")
                    st.success(f"{new_id} 등록 완료")
                    st.rerun()

with col_del:
    with st.expander("🗑️ CI 삭제"):
        if len(filtered) == 0:
            st.caption("삭제할 CI가 없습니다.")
        else:
            del_options = {f"{r.CI_ID} — {r.CI_NAME}": r.CI_ID for r in filtered.itertuples()}
            selected_del_label = st.selectbox("삭제할 CI 선택", options=list(del_options.keys()), key="del_select")
            selected_del_id = del_options[selected_del_label]
            confirm = st.checkbox("정말 삭제하시겠습니까? (되돌릴 수 없습니다)", key="del_confirm")
            if st.button("삭제 실행", disabled=not confirm):
                row_to_delete = ci_df[ci_df["CI_ID"] == selected_del_id].iloc[0]
                updated = ci_df[ci_df["CI_ID"] != selected_del_id]
                save_ci(updated)
                append_history(
                    selected_del_id, row_to_delete["CI_NAME"], row_to_delete["CI_CATEGORY"],
                    "REMOVED", "Streamlit CI 삭제화면을 통해 삭제",
                )
                st.success(f"{selected_del_id} 삭제 완료")
                st.rerun()

st.caption("CI 추가/삭제는 3_구성관리/CI.csv를 직접 수정하고, 3_구성관리/구성이력/CI_HISTORY.csv에 이력을 남깁니다(홈 화면 '구성관리(추가)/(삭제)' 지표에 반영).")
