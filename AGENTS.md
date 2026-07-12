# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Streamlit multipage app** (Korean ITSM 통합관리대시보드). Data lives in CSV files across the numbered domain folders (e.g. `3_구성관리/CI.csv`, `1_변경관리/CHANGE.csv`); there is no database.

- **Dependencies** (`streamlit`, `pandas`) are installed by the startup update script (`pip install -r requirements.txt`). The `streamlit` console script lands in `~/.local/bin`, which may not be on `PATH` — always run it as `python3 -m streamlit ...`.
- **Run the app** (dev mode) from the repo root; the entry point is `5_ITSM관리/홈.py`:
  `python3 -m streamlit run "5_ITSM관리/홈.py" --server.port 8501 --server.address 0.0.0.0 --server.headless true`
  Health check: `curl http://localhost:8501/_stcore/health` → `ok`.
- **No test suite or linter config** exists. For a fast sanity check, byte-compile the sources:
  `python3 -m py_compile 5_ITSM관리/홈.py 5_ITSM관리/*.py 5_ITSM관리/pages/*.py`.
- **CRUD writes to tracked CSVs.** The management pages (e.g. `pages/1_변경관리.py`) read/write the domain CSVs directly. Exercising the "등록/삭제" forms mutates files like `1_변경관리/CHANGE.csv` — revert test data with `git checkout -- <path>` if you don't intend to commit it.
- **경영관리 page is password-gated** via `st.secrets["MGMT_PASSWORD"]`. To open it, create `.streamlit/secrets.toml` (gitignored) with `MGMT_PASSWORD = "..."`; without it the page shows a warning and blocks its body. See `.streamlit/secrets.toml.example`.
