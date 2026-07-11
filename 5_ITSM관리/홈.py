from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
CI_CSV = ROOT / "3_구성관리" / "CI.csv"
CHANGE_CSV = ROOT / "1_변경관리" / "CHANGE.csv"
INCIDENT_CSV = ROOT / "2_장애관리" / "INCIDENT.csv"

CAT_COLORS = [
    "#2a78d6", "#1baf7a", "#eda100", "#008300",
    "#4a3aa7", "#e34948", "#e87ba4", "#eb6834",
]

st.set_page_config(page_title="ITSM 통합관리대시보드", layout="wide")

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
    categories = cat_counts["category"].tolist()
    colors = [CAT_COLORS[i % len(CAT_COLORS)] for i in range(len(categories))]

    bars = (
        alt.Chart(cat_counts)
        .mark_bar(cornerRadiusTopRight=4, cornerRadiusBottomRight=4, size=16)
        .encode(
            y=alt.Y("category:N", sort="-x", title=None),
            x=alt.X("count:Q", title=None),
            color=alt.Color(
                "category:N",
                scale=alt.Scale(domain=categories, range=colors),
                legend=None,
            ),
            tooltip=["category", "count"],
        )
    )
    labels = bars.mark_text(align="left", dx=4).encode(text="count:Q")
    st.altair_chart(
        (bars + labels).properties(height=28 * len(categories)),
        use_container_width=True,
    )

st.subheader("현황")
c1, c2, c3, c4 = st.columns(4)
c1.metric("변경건수", len(change_df))
c2.metric("장애건수", len(incident_df))
c3.metric("구성관리(추가)", 4)
c3.caption("이력 미설계 - 이번 CI 등록분만 반영")
c4.metric("구성관리(삭제)", 0)
c4.caption("이력 미설계 - 0 고정")

st.divider()
st.caption("개인정보처리방침 · 이용약관 (원고 준비 후 연결 예정)")
