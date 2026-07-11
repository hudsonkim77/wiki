import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "문제관리",
    "6_문제관리/README.md",
    [
        ("PROBLEM (문제 마스터)", "6_문제관리/PROBLEM.csv"),
        ("PROBLEM_INCIDENT_MAP (장애 연결)", "6_문제관리/문제이력/PROBLEM_INCIDENT_MAP.csv"),
    ],
)
