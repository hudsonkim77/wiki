import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from domain_view import render_domain_page  # noqa: E402

render_domain_page(
    "서비스수준관리",
    "9_서비스수준관리/README.md",
    [
        ("SLA (SLA 마스터)", "9_서비스수준관리/SLA.csv"),
        ("SLA_INCIDENT_MAP (장애 연결)", "9_서비스수준관리/SLA이력/SLA_INCIDENT_MAP.csv"),
        ("SLA_OPS_MAP (운영상태 연결)", "9_서비스수준관리/SLA이력/SLA_OPS_MAP.csv"),
    ],
)
