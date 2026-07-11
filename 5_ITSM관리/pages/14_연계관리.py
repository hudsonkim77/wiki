import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "연계관리",
    "14_연계관리/README.md",
    [
        ("INTERFACE (연계 마스터)", "14_연계관리/INTERFACE.csv"),
        ("INTERFACE_CI_MAP (CI 연결)", "14_연계관리/연계이력/INTERFACE_CI_MAP.csv"),
    ],
)
