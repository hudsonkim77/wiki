# AGENTS.md

## Domain context

The numbered domain folders (`1_변경관리`, `2_장애관리`, `3_구성관리`, `6_문제관리` … `15_백업관리`, plus `5_ITSM관리` as the app) are **not arbitrary** — they model how a **Korean public institution (대한민국 공공기관) structures its standard operational management (표준운영관리)**. The design references the **ITIL v4** standard but adapts it to this public-sector operating structure, so the set and grouping of domains reflects that adaptation rather than a strict 1:1 ITIL mapping. Keep this intent in mind when adding or reorganizing domains/pages.

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

### `ITSM_CURSOR/` — new React + FastAPI app (redesign)

`ITSM_CURSOR/` is a **separate, modern reimplementation** of the ITSM dashboard: same data/domain structure and CSVs (copied from the wiki root, so data stays consistent), but a fully custom **React (Vite + TS + Tailwind)** frontend backed by a **FastAPI** service. It is independent of the root Streamlit app. See `ITSM_CURSOR/README.md`.

- **Two dev processes** (run both):
  - Backend `:8000` — `cd "ITSM_CURSOR/5_ITSM관리/backend" && MGMT_PASSWORD=7587 python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload`
  - Frontend `:5173` — `cd "ITSM_CURSOR/5_ITSM관리/frontend" && npm run dev` (Vite proxies `/api` → `:8000`, so **the backend must be running** or the UI shows load errors).
- **경영관리 password here is an env var** (`MGMT_PASSWORD`), NOT `secrets.toml` — this app does not use Streamlit. If unset, `/api/management/unlock` returns 503.
- **CRUD writes to CSV + folder history.** Every create/delete via the API updates the domain's master CSV **and appends a row to that folder's `_HISTORY.csv`** (`backend/domains.py` lists the domain→folder/CSV mapping).
- **Data layer is config-driven**: columns come from the CSV header; Korean labels live in `backend/domains.py` (`COLUMN_LABELS_KO`). To add/adjust a domain, edit `DOMAINS` there — the frontend renders generically.
- **ERD** is reused from the wiki: `backend` extracts the mermaid `erDiagram` blocks from `ITSM_CURSOR/5_ITSM관리/ERD.html`; the React page renders them with `mermaid`.
- `node_modules`/`dist` under `frontend/` are gitignored (see `frontend/.gitignore`).
