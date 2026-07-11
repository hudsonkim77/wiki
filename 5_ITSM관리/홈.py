import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "5_ITSM관리"))
from labels import CATEGORY_LABELS_KO  # noqa: E402

CI_CSV = ROOT / "3_구성관리" / "CI.csv"
CHANGE_CSV = ROOT / "1_변경관리" / "CHANGE.csv"
INCIDENT_CSV = ROOT / "2_장애관리" / "INCIDENT.csv"
CI_HISTORY_CSV = ROOT / "3_구성관리" / "구성이력" / "CI_HISTORY.csv"
PRIVACY_POLICY_MD = ROOT / "5_ITSM관리" / "개인정보처리방침.md"
ASSETS = ROOT / "5_ITSM관리" / "assets"


# 정적 HTML 버전의 policy-modal.js와 동일한 역할. 원문(개인정보처리방침.md)을 그대로
# st.markdown으로 렌더링하므로 본문 수정 시 이 코드는 그대로 두고 .md 파일만 고치면 됨.
@st.dialog("개인정보 처리방침")
def show_privacy_policy():
    st.markdown(PRIVACY_POLICY_MD.read_text(encoding="utf-8"))


# 경영진 관제형(Control-room) 디자인 기조 — 단일 앰버 액센트(카테고리별 무지개색 대신
# 정적 HTML(style.css --accent)과 통일된 그라데이션 사용).
ACCENT_START = "#ff9f45"
ACCENT_END = "#ffc27a"

st.set_page_config(page_title="ITSM 통합관리대시보드", layout="wide")


def render_home():
    st.logo(str(ASSETS / "logo-full-flat.png"), icon_image=str(ASSETS / "logo-mark-flat.png"))
    # st.logo()는 크기를 small/medium/large로만 조절 가능해 400px 이상으로 키울 수 없다.
    # 가독성 요구사항(폭 400px 이상)을 맞추기 위해 본문 상단에 별도로 큰 로고를 노출한다.
    st.image(str(ASSETS / "logo-nav-flat.png"), width=420)

    ci_df = pd.read_csv(CI_CSV)
    change_df = pd.read_csv(CHANGE_CSV)
    incident_df = pd.read_csv(INCIDENT_CSV)

    st.title("ITSM 통합관리대시보드")

    col_total, col_chart = st.columns([1, 2])

    with col_total:
        with st.container(border=True):
            st.metric("총 자산수", f"{len(ci_df):,}")
            st.caption("3_구성관리/CI.csv 기준")

    with col_chart:
        with st.container(border=True):
            st.markdown("**카테고리별 자산 현황**")
            cat_counts = (
                ci_df["CI_CATEGORY"]
                .value_counts()
                .rename_axis("category")
                .reset_index(name="count")
                .sort_values("count", ascending=True)
            )
            cat_counts["category_ko"] = cat_counts["category"].map(CATEGORY_LABELS_KO).fillna(cat_counts["category"])
            categories_ko = cat_counts["category_ko"].tolist()
            n = max(len(categories_ko) - 1, 1)
            start_rgb = tuple(int(ACCENT_START[i : i + 2], 16) for i in (1, 3, 5))
            end_rgb = tuple(int(ACCENT_END[i : i + 2], 16) for i in (1, 3, 5))
            colors = [
                "#{:02x}{:02x}{:02x}".format(
                    *(int(s + (e - s) * i / n) for s, e in zip(start_rgb, end_rgb))
                )
                for i in range(len(categories_ko))
            ]

            fig = go.Figure(
                go.Bar(
                    y=categories_ko,
                    x=cat_counts["count"],
                    orientation="h",
                    marker=dict(color=colors, line=dict(width=0)),
                    text=cat_counts["count"],
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>자산수: %{x}건<extra></extra>",
                )
            )
            fig.update_traces(marker_cornerradius=6)
            fig.update_layout(
                height=28 * len(categories_ko) + 40,
                margin=dict(l=0, r=24, t=8, b=0),
                xaxis=dict(visible=False),
                yaxis=dict(title=None, color="#a7acb3"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(size=12, color="#a7acb3"),
                showlegend=False,
                bargap=0.35,
                transition=dict(duration=400, easing="cubic-in-out"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.subheader("현황")
    history_df = pd.read_csv(CI_HISTORY_CSV) if CI_HISTORY_CSV.exists() else pd.DataFrame(columns=["ACTION"])
    ci_added = int((history_df["ACTION"] == "ADDED").sum())
    ci_removed = int((history_df["ACTION"] == "REMOVED").sum())

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        with st.container(border=True):
            st.metric("변경건수", len(change_df))
    with c2:
        with st.container(border=True):
            st.metric("장애건수", len(incident_df))
    with c3:
        with st.container(border=True):
            st.metric("구성관리(추가)", ci_added)
            st.caption("3_구성관리/구성이력/CI_HISTORY.csv 기준")
    with c4:
        with st.container(border=True):
            st.metric("구성관리(삭제)", ci_removed)
            st.caption("3_구성관리/구성이력/CI_HISTORY.csv 기준")

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

    st.divider()
    _, footer_logo_col, _ = st.columns([2, 1, 2])
    with footer_logo_col:
        st.image(str(ASSETS / "logo-full-flat.png"))

    footer_col1, footer_col2 = st.columns([1, 1])
    with footer_col1:
        if st.button("개인정보처리방침"):
            show_privacy_policy()
    with footer_col2:
        st.caption("이용약관 (원고 준비 후 연결 예정)")


PAGES_DIR = ROOT / "5_ITSM관리" / "pages"
# st.navigation()으로 사이드바 라벨을 파일명("홈")과 무관하게 직접 지정한다.
# 이 함수를 쓰기 전에는 메인 스크립트가 항상 "홈"으로만 표시되어 "ITSM관리"로
# 바꿔달라는 요청을 파일명 변경 없이 처리할 수 없었다(Main file path 설정 유지 필요).
nav = st.navigation([
    st.Page(render_home, title="ITSM관리", icon="🏠", default=True),
    st.Page(str(PAGES_DIR / "1_변경관리.py"), title="변경관리"),
    st.Page(str(PAGES_DIR / "2_장애관리.py"), title="장애관리"),
    st.Page(str(PAGES_DIR / "3_구성관리.py"), title="구성관리"),
    st.Page(str(PAGES_DIR / "4_경영관리.py"), title="경영관리"),
])
nav.run()
