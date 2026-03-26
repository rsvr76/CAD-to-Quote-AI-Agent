# Backend Summary

## FastAPI App + Endpoints

**Description**

- Main server module defines:
  - HTML page routes (multi-page flow)
  - JSON endpoints for routing/stock/quote/DFM simulate/STEP extract
  - A helper `_simulate_total_cost_inr` used to score DFM variants by re-running the same pipeline.

**Source Files**

- /backend/main.py
  - `app = FastAPI(...)` (line ~33)
  - `_simulate_total_cost_inr` (lines 42–66)
  - Page routes `landing` → `export_pdf` (lines 94–135)
  - API endpoints:
    - `api_routing` (lines 159–168)
    - `api_stock` (lines 172–183)
    - `api_quote` (lines 187–272)
    - `api_dfm_simulate` (lines 276–304)
    - `api_step_extract` (lines 308–395)

**Key Functions / Classes**

- `_simulate_total_cost_inr` → simulates routing→stock→time→cost and returns total ₹ → /backend/main.py:42
- `api_quote` → full pipeline → /backend/main.py:187
- `api_step_extract` → STEP upload → geometry extraction + preview URL → /backend/main.py:308

**Dependencies**

- Internal:
  - /backend/models.py schemas
  - /backend/routing.py, /backend/stock.py, /backend/ml_engine.py, /backend/cost.py, /backend/confidence.py, /backend/explainability.py, /backend/dfm.py, /backend/step_extract.py
- External:
  - fastapi, uvicorn

## Data Models (Schemas)

**Description**

- Pydantic models define the request/response shapes shared by backend endpoints and frontend JS.

**Source Files**

- /backend/models.py
  - `GeometryData` (lines 8–17)
  - `UserInputs` (lines 20–26)
  - `RoutingFlags` (lines 29–33)
  - `RoutingDecision` + nested models (lines 43–61)
  - `StockEstimate` (lines 64–68)
  - `CostBreakdown` + machining breakdown models (lines 71–90)
  - `ConfidenceRange` (lines 93–98)
  - `CostDriver` (lines 101–104)
  - `DFMSuggestion` (lines 107–113)
  - `FullQuoteResponse` (lines 123–132)

**Dependencies**

- External: pydantic

## Routing Engine (Step 4)

**Description**

- Rule-based routing flags:
  - turning if `aspect_ratio > 2`
  - milling if pockets exist OR large surface area
  - drilling if holes exist
  - grinding if tolerance is Fine/Ultra-Fine
- Provides default machine selections and a human-readable reason helper.

**Source Files**

- /backend/routing.py
  - `compute_routing_flags` (lines 38–45)
  - `build_default_machine_selection` (lines 48–55)
  - `route_processes` (lines 58–72)
  - `get_routing_reason` (lines 75–103)

## Stock Estimation (Steps 5–6)

**Description**

- Chooses stock shape:
  - cylinder if turning, else block (unless override)
- Computes stock volume and weight using density table.

**Source Files**

- /backend/stock.py
  - `estimate_stock` (lines 52–86)

## ML Inference + Explainability (Steps 8 + 11)

**Description**

- Lazy-loads RF model + feature columns; uses formula fallback when artifacts are missing.
- Optional SHAP drivers when `shap_explainer.joblib` is present.

**Source Files**

- /backend/ml_engine.py
  - `_ensure_loaded` (lines 46–71)
  - `predict_machining_time` (lines 122–137)
  - `get_shap_drivers` (lines 140–190)
- /backend/ml_placeholder.py
  - `predict_machining_time` formula baseline (lines 30–93)

## Cost Engine (Step 10)

**Description**

- Deterministic cost breakdown:
  - material cost from weight × ₹/kg × batch discount
  - machining cost by allocating ML time across active processes and applying machine rates
  - setup cost amortized by quantity
  - overhead as a material-specific percentage of subtotal

**Source Files**

- /backend/cost.py
  - `calculate_full_cost` (lines 155–177)

## Confidence / Uncertainty (Step 9)

**Description**

- If RF model is available: uses per-tree prediction spread to compute a percentile-based cost interval.
- Otherwise: heuristic uncertainty based on material/tolerance/quantity/features.

**Source Files**

- /backend/confidence.py
  - `_tree_based_confidence` (lines 45–106)
  - `_heuristic_confidence` (lines 109–153)
  - `estimate_confidence` (lines 156–168)

## DFM Suggestions (Step 12)

**Description**

- Generates candidate design/input changes with `variant_inputs`.
- Savings are intended to be computed by simulating each variant through the actual pipeline.

**Source Files**

- /backend/dfm.py
  - `generate_dfm_suggestions` (lines 26–98)
- /backend/main.py
  - Variant scoring uses `_simulate_total_cost_inr` inside `api_quote` (lines 187–272)

## STEP Extraction (Upload → Geometry)

**Description**

- Parses uploaded STEP via `gmsh` OpenCascade kernel.
- Extracts volume/surface area/bbox + face/edge counts.
- Generates a best-effort preview PNG (matplotlib) and returns as a data URL.

**Source Files**

- /backend/step_extract.py
  - `extract_step_geometry` (lines 50–171)
  - `_render_triangles_png` (lines 225–293)
- /backend/main.py
  - `api_step_extract` builds `GeometryData` and returns `{geometry, preview_image_url}` (lines 308–395)

## Audit / Smoke Tests

**Description**

- `tmp/audit_backend.py` is a self-check script that imports modules and runs sample pipelines (not wired into CI).
- `backend/smoke_step_extract.py` generates a simple STEP box via gmsh and validates extraction.

**Source Files**

- /tmp/audit_backend.py (ad-hoc audit script)
- /backend/smoke_step_extract.py
  - `_make_box_step` (lines 15–27)
  - `main` (lines 30–65)

## Known Issue (Important)

**Description**

- The DFM simulation endpoint appears incomplete: `api_dfm_simulate` exits after parsing inputs but never runs the modified pipeline nor returns a response. Additionally, a large block of “DFM simulate” logic is currently placed *after* the `return` in `api_step_extract`, making it unreachable.

**Source Files**

- /backend/main.py
  - `api_dfm_simulate` has no return after line 304 (lines 276–304)
  - `api_step_extract` returns at lines 392–395, but additional pipeline code follows that `return` (lines 308–402)

**Notes**

- See /Summary/findings.md for details and recommended fix approach.
