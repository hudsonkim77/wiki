import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "테스트관리",
    "13_테스트관리/README.md",
    [
        ("TEST_CASE (테스트 마스터)", "13_테스트관리/TEST_CASE.csv"),
    ],
)
