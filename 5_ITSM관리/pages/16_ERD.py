from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).resolve().parent.parent  # 5_ITSM관리/
ERD_HTML = ROOT / "ERD.html"
STYLE_CSS = ROOT / "style.css"

st.logo(str(ROOT / "assets" / "logo-full-flat.png"), icon_image=str(ROOT / "assets" / "logo-mark-flat.png"))
st.image(str(ROOT / "assets" / "logo-nav-flat.png"), width=420)

st.title("통합 데이터 모델 ERD")


def _extract_section(html, index):
    parts = html.split('<section class="panel">')
    body = parts[index]
    return body[: body.rfind("</section>") + len("</section>")]


# 정적 HTML 버전(ERD.html)의 패널을 그대로 잘라내 임베딩한다. 마크업이나 Mermaid 다이어그램
# 정의를 이 파일에 다시 옮겨 적지 않는 이유는, 두 버전이 어긋나지 않도록 ERD.html+style.css를
# 유일한 원본으로 유지하기 위함이다(구성관리와 동일한 방식, CHG_20260711_005 참고).
html = ERD_HTML.read_text(encoding="utf-8")
panel_section = _extract_section(html, 1)
css = STYLE_CSS.read_text(encoding="utf-8")

embed = f"""
<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<style>{css}</style>
</head>
<body>
<main class="erd-wide-main">
{panel_section}
</main>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'base',
    themeVariables: {{
      primaryColor: '#21252b',
      primaryTextColor: '#edeef0',
      primaryBorderColor: '#ff9f45',
      lineColor: '#767c85',
      tertiaryColor: '#1b1e23',
      attributeBackgroundColorOdd: '#1b1e23',
      attributeBackgroundColorEven: '#21252b'
    }}
  }});

  function fixSvgNativeSize() {{
    document.querySelectorAll('.erd-mermaid-scroll svg').forEach((svg) => {{
      const vb = svg.viewBox && svg.viewBox.baseVal;
      if (vb && vb.width) {{
        svg.style.width = vb.width + 'px';
        svg.style.height = vb.height + 'px';
      }}
    }});
  }}
  setTimeout(fixSvgNativeSize, 300);

  function showErdModel(which) {{
    document.getElementById('erd-diagram-logical').classList.toggle('erd-mermaid-hidden', which !== 'logical');
    document.getElementById('erd-diagram-physical').classList.toggle('erd-mermaid-hidden', which !== 'physical');
    document.getElementById('erd-btn-logical').classList.toggle('active', which === 'logical');
    document.getElementById('erd-btn-physical').classList.toggle('active', which === 'physical');
    document.getElementById('erd-caption').textContent = which === 'logical'
      ? '논리 모델: 13개 ITIL practice 도메인의 핵심 엔티티와 관계만 표시(구현 세부는 생략). 컬럼은 한글명(영문 컬럼명)으로 표시됩니다.'
      : '물리 모델: 실제 CSV 스키마 기준 전체 26개 테이블 · 전체 컬럼(한글명(영문 컬럼명)) · PK/FK를 표시.';
    erdZoomReset();
  }}

  // ---- 확대/축소 + 드래그 이동 --------------------------------------------------
  let erdScale = 1;
  let erdPanX = 0;
  let erdPanY = 0;

  function applyErdTransform() {{
    const content = document.getElementById('erd-zoom-content');
    content.style.transform = `translate(${{erdPanX}}px, ${{erdPanY}}px) scale(${{erdScale}})`;
    document.getElementById('erd-zoom-label').textContent = Math.round(erdScale * 100) + '%';
  }}

  function erdZoom(factor) {{
    erdScale = Math.min(3, Math.max(0.2, erdScale * factor));
    applyErdTransform();
  }}

  function erdZoomReset() {{
    erdScale = 1;
    erdPanX = 0;
    erdPanY = 0;
    applyErdTransform();
  }}

  (function setupErdPanZoom() {{
    const viewport = document.getElementById('erd-viewport');
    let dragging = false;
    let startX = 0;
    let startY = 0;
    let startPanX = 0;
    let startPanY = 0;

    viewport.addEventListener('mousedown', (e) => {{
      dragging = true;
      viewport.classList.add('erd-dragging');
      startX = e.clientX;
      startY = e.clientY;
      startPanX = erdPanX;
      startPanY = erdPanY;
      e.preventDefault();
    }});
    window.addEventListener('mousemove', (e) => {{
      if (!dragging) return;
      erdPanX = startPanX + (e.clientX - startX);
      erdPanY = startPanY + (e.clientY - startY);
      applyErdTransform();
    }});
    window.addEventListener('mouseup', () => {{
      dragging = false;
      viewport.classList.remove('erd-dragging');
    }});
    viewport.addEventListener('wheel', (e) => {{
      e.preventDefault();
      erdZoom(e.deltaY < 0 ? 1.08 : 1 / 1.08);
    }}, {{ passive: false }});
  }})();
</script>
</body>
</html>
"""

components.html(embed, height=1050, scrolling=True)
