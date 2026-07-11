import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "배포관리",
    "7_배포관리/README.md",
    [
        ("DEPLOY (배포 마스터)", "7_배포관리/DEPLOY.csv"),
        ("DEPLOY_CHG_MAP (변경 연결)", "7_배포관리/배포이력/DEPLOY_CHG_MAP.csv"),
    ],
)
