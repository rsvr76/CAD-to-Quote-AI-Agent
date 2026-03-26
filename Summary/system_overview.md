# System Overview

## Project Type

**Description**

- Demo “CAD-to-Quote” web app: upload/select a part → compute geometry/routing/stock/ML time/cost/confidence/explainability/DFM → render quote UI.

**Source Files**

- /backend/main.py (FastAPI app + HTML + API endpoints; lines 1–402)
- /frontend/templates/*.html (UI pages)
- /backend/*.py (pipeline modules)
- /All/Steps/*.md (intended pipeline spec)
- /All/gl/*.md (simplified “Grandma language” spec)

**Dependencies**

- External:
  - fastapi, uvicorn (web server)
  - pydantic (request/response models)
  - numpy, joblib (ML inference + optional uncertainty)
  - gmsh, matplotlib (STEP parsing + preview rendering)
- Internal:
  - backend routing/stock/ml/cost/confidence/dfm/explainability modules

## High-Level Architecture

**Description**

- Backend serves both:
  - HTML pages (Jinja2 templates) for the multi-step UI flow.
  - JSON APIs to run the pipeline.
- Frontend is server-rendered HTML + Tailwind CDN + vanilla JS; state is carried between pages using `localStorage`.

**Source Files**

- /backend/main.py (page routes: lines 94–135; API routes: lines 143–395)
- /frontend/templates/index.html (landing + upload + samples; uses `localStorage` and APIs)

## Core Workflow (“CAD-to-Quote” pipeline)

**Description**

A typical quote run follows:

1) **Geometry**: either sample geometry or uploaded STEP extraction.
2) **Routing**: decide which processes are needed (turning/milling/drilling/grinding).
3) **Stock**: estimate raw material stock shape + weight.
4) **Machining time**: RandomForest model if present; formula fallback otherwise.
5) **Cost**: deterministic breakdown from stock + time + machine rates + setup + overhead.
6) **Confidence**: tree-spread percentile interval if RF available; heuristic otherwise.
7) **Drivers**: SHAP-based drivers if explainer available; heuristic drivers otherwise.
8) **DFM**: generate candidate changes; server simulates variants to score savings.

**Source Files**

- /backend/main.py
  - Full pipeline endpoint: /api/quote (lines 187–272)
  - STEP extraction: /api/step/extract (lines 308–395)
- /backend/routing.py (Step 4 rules; lines 1–103)
- /backend/stock.py (Steps 5–6; lines 1–86)
- /backend/ml_engine.py (Step 8 + Step 11 SHAP drivers; lines 1–190)
- /backend/cost.py (Step 10 deterministic costing; lines 1–177)
- /backend/confidence.py (Step 9 uncertainty; lines 1–168)
- /backend/explainability.py (Step 11 heuristic drivers; lines 1–64)
- /backend/dfm.py (Step 12 candidate generation; lines 1–98)
- /backend/step_extract.py (STEP parsing + preview; lines 1–293)

## Repo Maps

- Full file inventory: /Summary/file_index.md
- Auto-generated per-file notes: /Summary/file_details.md
- Machine-readable scan used to generate these docs: /Summary/_repo_scan.json
