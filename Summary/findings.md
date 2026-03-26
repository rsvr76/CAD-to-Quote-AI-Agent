# Findings / Issues

## 1) `POST /api/dfm/simulate` was incomplete (now fixed)

**Description**

- This issue is resolved: the handler now applies the selected suggestion’s `variant_inputs`, re-runs the full pipeline, and returns a comparison response including `savings_inr` and `savings_pct`.
- The unreachable “simulate pipeline” code that was previously located after the `return` in `api_step_extract` has been removed.

**Source Files**

- /backend/main.py
  - `api_dfm_simulate` (starts around line 276)
  - `api_step_extract` (starts around line 369)
- /tmp/check_dfm_simulate.py (in-process sanity check covering the simulate flow)

**Impact**

- Frontend “Simulate” flow for DFM comparisons should now work (the endpoint returns JSON).

**Notes**

- If you want a quick regression check without starting the server, run `/tmp/check_dfm_simulate.py`.

## 2) STEP extraction requires optional heavy dependencies

**Description**

- STEP parsing uses `gmsh` and preview rendering uses `matplotlib`. If these are not installed, `/api/step/extract` will fail (by design).

**Source Files**

- /backend/step_extract.py
  - Imports `gmsh` inside `extract_step_geometry` and raises if missing (lines 50–71)
  - Uses matplotlib in `_render_triangles_png` (lines 225–293)

**Impact**

- Deploy/run environments need these dependencies installed for upload-based geometry extraction.

## 3) Audit script expectations may not match runtime fallback behavior

**Description**

- `tmp/audit_backend.py` appears to expect `_model is not None` and SHAP drivers to be present.
- In runtime, the app intentionally falls back to formula estimation when model artifacts are missing.

**Source Files**

- /tmp/audit_backend.py (module import checks + SHAP checks; see early sections)
- /backend/ml_engine.py (fallback behavior; lines 46–137)

**Impact**

- Running the audit without trained artifacts (or without `shap`) may produce failures even if the app’s fallback path is working as intended.
