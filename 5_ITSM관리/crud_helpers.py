"""전체 관리 페이지가 공유하는 CRUD 보일러플레이트(CHG_20260712_004).
변경관리(pages/1_변경관리.py)에서 처음 만든 패턴 — 상태 선택 → 조회, 추가/삭제 —
을 다른 도메인에도 반복하면서 CSV 로드/저장, ID 채번, FK 선택지 조회 부분만 공통화했다.
폼 위젯 구성 자체(어떤 필드에 selectbox를 쓸지 등)는 도메인마다 달라 각 페이지 파일에 그대로 둔다.
"""

from datetime import datetime

import pandas as pd


def load_df(csv_path):
    return pd.read_csv(csv_path, dtype=str, keep_default_na=False)


def save_df(df, csv_path):
    df.to_csv(csv_path, index=False)


def next_id(df, id_field, prefix):
    """{PREFIX}_{YYYYMMDD}_{순번:03d} 형식 ID 채번(변경관리 next_chg_id와 동일 규칙)."""
    today = datetime.now().strftime("%Y%m%d")
    pattern = rf"^{prefix}_{today}_(\d+)$"
    existing = df[id_field].str.extract(pattern)[0].dropna().astype(int)
    n = (existing.max() + 1) if len(existing) else 1
    return f"{prefix}_{today}_{n:03d}"


def fk_options(csv_path, id_field, none_label="(없음)"):
    """다른 도메인 CSV의 ID 목록을 FK 선택지로 불러온다(옵션 FK만 지원, 없으면 빈 목록)."""
    if not csv_path.exists():
        return [none_label]
    df = load_df(csv_path)
    return [none_label] + df[id_field].tolist()
