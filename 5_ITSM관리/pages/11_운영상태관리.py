import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "운영상태관리",
    "11_운영상태관리/README.md",
    [
        ("OPS_STATUS (운영상태 마스터)", "11_운영상태관리/OPS_STATUS.csv"),
        ("OPS_CI_MAP (CI 연결)", "11_운영상태관리/운영이력/OPS_CI_MAP.csv"),
    ],
)
