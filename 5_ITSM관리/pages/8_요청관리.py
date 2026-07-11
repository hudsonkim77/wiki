import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "요청관리",
    "8_요청관리/README.md",
    [
        ("REQUEST (요청 마스터)", "8_요청관리/REQUEST.csv"),
        ("REQUEST_INCIDENT_MAP (장애 연결)", "8_요청관리/요청이력/REQUEST_INCIDENT_MAP.csv"),
        ("REQUEST_CI_MAP (CI 연결)", "8_요청관리/요청이력/REQUEST_CI_MAP.csv"),
    ],
)
