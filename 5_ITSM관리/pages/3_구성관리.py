from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent.parent
STYLE_CSS = ROOT / "style.css"
CI_HTML = ROOT / "구성관리.html"

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

st.info("CI 등록/조회 입력 화면은 아직 설계 전입니다. 설계가 끝나면 이 페이지에 CI 등록/조회 화면이 들어갑니다.")
