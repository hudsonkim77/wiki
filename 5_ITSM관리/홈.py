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

# CI_CATEGORY(원본 코드) -> 화면 표시용 한글 라벨. CI.csv의 CI_CATEGORY 값 자체는
# 그대로 두고, 대시보드 표시 문구만 한글로 바꾼다.
CATEGORY_LABELS_KO = {
    "Storage": "스토리지",
    "VM": "가상머신(VM)",
    "Staff": "인력",
    "PC": "PC",
    "Server": "서버",
    "Internal_Security_Sol": "내부보안솔루션",
    "DMZ_Compute": "DMZ 서버",
    "Switch": "스위치",
    "Network_Security": "네트워크 보안",
    "Network_Equipment": "네트워크 장비",
    "L3_PAGE": "웹페이지(3단계)",
    "L2_PAGE": "웹페이지(2단계)",
    "L1_PAGE": "웹페이지(1단계)",
    "Peripheral": "주변기기",
    "Security_Management": "보안관제",
}

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

st.subheader("최근 사항 3건")

latest_change = change_df.iloc[-1]
with st.expander(f"🔵 변경 · {latest_change['CHG_TICKET_ID']} — {latest_change['CHG_TITLE']}"):
    st.write(latest_change["RELATED_DESC"])
    st.caption(f"적용일 {latest_change['APPLIED_DT']}")

# 자산등록 이력 로그가 아직 없어(README 참고) 최초 등록 건을 고정 표기. 향후 이력 로그가
# 생기면 CI.csv에서 최신 등록분을 직접 계산하도록 바꿔야 함.
with st.expander("🟡 자산등록 · ITSM 통합관리대시보드 신규 자산 등록(4건)"):
    st.write(
        "구성관리 CI 마스터에 신규 자산 4건(CFG_WEB_019~022: ITSM 통합관리대시보드 메인 및 "
        "변경·장애·구성관리 하위 메뉴 페이지)을 등록했습니다."
    )
    st.caption("등록일시 2026-07-11 12:00 · 근거 변경티켓 CHG_20260711_001")

if len(incident_df):
    latest_incident = incident_df.iloc[-1]
    with st.expander(f"🔴 장애 · {latest_incident['INCIDENT_ID']} — {latest_incident['INCIDENT_TITLE']}"):
        st.write(f"**원인**: {latest_incident['ROOT_CAUSE']}")
        st.write(f"**조치**: {latest_incident['ACTION_TAKEN']}")
        st.caption(f"감지 {latest_incident['DETECTED_DT']} · 복구 {latest_incident['RESOLVED_DT']} ({latest_incident['SEVERITY']})")
else:
    st.caption("🔴 장애 · 이력 없음")

st.divider()
st.caption("개인정보처리방침 · 이용약관 (원고 준비 후 연결 예정)")
