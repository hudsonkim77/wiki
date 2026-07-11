import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "5_ITSM관리"))
from labels import CATEGORY_LABELS_KO  # noqa: E402

CI_CSV = ROOT / "3_구성관리" / "CI.csv"
CHANGE_CSV = ROOT / "1_변경관리" / "CHANGE.csv"
INCIDENT_CSV = ROOT / "2_장애관리" / "INCIDENT.csv"
CI_HISTORY_CSV = ROOT / "3_구성관리" / "구성이력" / "CI_HISTORY.csv"
PRIVACY_POLICY_MD = ROOT / "5_ITSM관리" / "개인정보처리방침.md"


# 정적 HTML 버전의 policy-modal.js와 동일한 역할. 원문(개인정보처리방침.md)을 그대로
# st.markdown으로 렌더링하므로 본문 수정 시 이 코드는 그대로 두고 .md 파일만 고치면 됨.
@st.dialog("개인정보 처리방침")
def show_privacy_policy():
    st.markdown(PRIVACY_POLICY_MD.read_text(encoding="utf-8"))

CAT_COLORS = [
    "#2a78d6", "#1baf7a", "#eda100", "#008300",
    "#4a3aa7", "#e34948", "#e87ba4", "#eb6834",
]

st.set_page_config(page_title="ITSM 통합관리대시보드", layout="wide")
st.logo(str(ROOT / "5_ITSM관리" / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "5_ITSM관리" / "assets" / "logo-mark-flat.png"))

ci_df = pd.read_csv(CI_CSV)
change_df = pd.read_csv(CHANGE_CSV)
incident_df = pd.read_csv(INCIDENT_CSV)

st.title("ITSM 통합관리대시보드")

col_total, col_chart = st.columns([1, 2])

with col_total:
    st.metric("총 자산수", f"{len(ci_df):,}")
    st.caption("3_구성관리/CI.csv 기준")

with col_chart:
    st.markdown("**카테고리별 자산 현황**")
    cat_counts = (
        ci_df["CI_CATEGORY"]
        .value_counts()
        .rename_axis("category")
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    cat_counts["category_ko"] = cat_counts["category"].map(CATEGORY_LABELS_KO).fillna(cat_counts["category"])
    categories_ko = cat_counts["category_ko"].tolist()
    colors = [CAT_COLORS[i % len(CAT_COLORS)] for i in range(len(categories_ko))]

    bars = (
        alt.Chart(cat_counts)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, size=16)
        .encode(
            y=alt.Y("category_ko:N", sort=categories_ko, title=None),
            x=alt.X("count:Q", title=None),
            color=alt.Color(
                "category_ko:N",
                scale=alt.Scale(domain=categories_ko, range=colors),
                legend=None,
            ),
            tooltip=[alt.Tooltip("category_ko:N", title="카테고리"), alt.Tooltip("count:Q", title="자산수")],
        )
    )
    labels = bars.mark_text(align="left", dx=4).encode(text="count:Q")
    st.altair_chart(
        (bars + labels).properties(height=28 * len(categories_ko)),
        width="stretch",
    )

st.subheader("현황")
c1, c2, c3, c4 = st.columns(4)
history_df = pd.read_csv(CI_HISTORY_CSV) if CI_HISTORY_CSV.exists() else pd.DataFrame(columns=["ACTION"])
ci_added = int((history_df["ACTION"] == "ADDED").sum())
ci_removed = int((history_df["ACTION"] == "REMOVED").sum())

c1.metric("변경건수", len(change_df))
c2.metric("장애건수", len(incident_df))
c3.metric("구성관리(추가)", ci_added)
c3.caption("3_구성관리/구성이력/CI_HISTORY.csv 기준")
c4.metric("구성관리(삭제)", ci_removed)
c4.caption("3_구성관리/구성이력/CI_HISTORY.csv 기준")

st.subheader("최근 사항 3건")

latest_change = change_df.iloc[-1]
with st.expander(f"🔵 변경 · {latest_change['CHG_TICKET_ID']} — {latest_change['CHG_TITLE']}"):
    st.write(latest_change["RELATED_DESC"])
    st.caption(f"적용일 {latest_change['APPLIED_DT']}")

if len(history_df):
    latest_hist = history_df.iloc[-1]
    action_ko = "등록" if latest_hist["ACTION"] == "ADDED" else "삭제"
    with st.expander(f"🟡 자산등록 · {latest_hist['CI_NAME']} {action_ko}"):
        st.write(f"CI_ID: {latest_hist['CI_ID']} · 카테고리: {latest_hist['CI_CATEGORY']}")
        st.caption(f"{latest_hist['ACTION_DT']} · {latest_hist['ACTION_BY']} · {latest_hist['NOTE']}")
else:
    st.caption("🟡 자산등록 · 이력 없음")

if len(incident_df):
    latest_incident = incident_df.iloc[-1]
    with st.expander(f"🔴 장애 · {latest_incident['INCIDENT_ID']} — {latest_incident['INCIDENT_TITLE']}"):
        st.write(f"**원인**: {latest_incident['ROOT_CAUSE']}")
        st.write(f"**조치**: {latest_incident['ACTION_TAKEN']}")
        st.caption(f"감지 {latest_incident['DETECTED_DT']} · 복구 {latest_incident['RESOLVED_DT']} ({latest_incident['SEVERITY']})")
else:
    st.caption("🔴 장애 · 이력 없음")

st.subheader("경영관리 업무보고")
st.markdown(
    "- [IT 자산 현황 브리핑](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_IT자산_현황_브리핑.pdf)\n"
    "- [데이터 모델 ERD 보고](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_2주차_데이터모델ERD보고.pdf)\n"
    "- [장애관리대장](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_장애관리대장.pdf)\n"
    "- [경위서 — ITSM 통합관리대시보드 서비스 장애](https://github.com/hudsonkim77/wiki/blob/main/4_경영관리/_업무보고/20260711_경위서_ITSM대시보드장애.pdf)"
)

st.divider()
_, footer_logo_col, _ = st.columns([2, 1, 2])
with footer_logo_col:
    st.image(str(ROOT / "5_ITSM관리" / "assets" / "logo-full-flat.png"))

footer_col1, footer_col2 = st.columns([1, 1])
with footer_col1:
    if st.button("개인정보처리방침"):
        show_privacy_policy()
with footer_col2:
    st.caption("이용약관 (원고 준비 후 연결 예정)")
