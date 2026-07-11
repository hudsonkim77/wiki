import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "이벤트관리",
    "12_이벤트관리/README.md",
    [
        ("EVENT (이벤트 마스터)", "12_이벤트관리/EVENT.csv"),
    ],
)
