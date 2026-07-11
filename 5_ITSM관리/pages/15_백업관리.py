import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "백업관리",
    "15_백업관리/README.md",
    [
        ("BACKUP (백업 마스터)", "15_백업관리/BACKUP.csv"),
        ("BACKUP_CI_MAP (CI 연결)", "15_백업관리/백업이력/BACKUP_CI_MAP.csv"),
    ],
)
