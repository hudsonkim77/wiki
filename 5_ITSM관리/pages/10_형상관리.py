import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "형상관리",
    "10_형상관리/README.md",
    [
        ("BASELINE (베이스라인 마스터)", "10_형상관리/BASELINE.csv"),
        ("BASELINE_CI_MAP (CI 연결)", "10_형상관리/형상이력/BASELINE_CI_MAP.csv"),
    ],
)
