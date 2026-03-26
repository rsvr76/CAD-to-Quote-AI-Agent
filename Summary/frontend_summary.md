# Frontend Summary

## UI Approach

**Description**

- Multi-page HTML flow served by FastAPI (Jinja templates).
- Styling via Tailwind CDN and Google fonts/icons.
- State is persisted across pages in `localStorage` under a `quoteSession` object.

**Source Files**

- /backend/main.py (page routes; lines 94–135)
- /frontend/templates/*.html

## State Model (`localStorage.quoteSession`)

**Description**

Across pages, the UI stores a session object with (commonly) keys like:

- `geometry` → geometry metrics used by routing/stock/quote
- `inputs` → user-entered manufacturing inputs (holes, pockets, depth, material, quantity, tolerance)
- `routing` → routing decision returned by `/api/routing`
- `stock`/`stock_override_*` → stock estimation inputs and results
- `quoteResult` → full quote response from `/api/quote`

**Source Files**

- /frontend/templates/index.html (clears `quoteSession`, sets upload/sample; lines ~240+)
- /frontend/templates/geometry.html (reads session and displays extracted features)
- /frontend/templates/input.html (collects/updates `inputs`)
- /frontend/templates/routing.html (calls `/api/routing`, writes routing into session)
- /frontend/templates/dashboard.html (reads `quoteResult` to populate cost/confidence/drivers/DFM cards)

## Page-by-Page Flow

### Landing / Upload / Samples

**Description**

- Lets the user upload a STEP (`.step`/`.stp`) or select a sample.
- Upload path posts the file to `/api/step/extract`, then stores returned geometry (+ preview URL) into session.

**Source Files**

- /frontend/templates/index.html
  - Uses `fetch(base + '/api/step/extract', { method: 'POST', body: FormData })` (script section)
  - Uses `/api/samples` + `/api/samples/{name}` for sample loading

### Geometry Validation

**Description**

- Displays geometry values and preview.
- Warns if there is no session.

**Source Files**

- /frontend/templates/geometry.html

### Input Collection

**Description**

- Collects manufacturing parameters (holes, pockets, depth, material, quantity, tolerance).
- Updates `quoteSession.inputs`.

**Source Files**

- /frontend/templates/input.html

### Routing

**Description**

- Calls `/api/routing` with `geometry` + `inputs`.
- Renders process flags + machine dropdowns.

**Source Files**

- /frontend/templates/routing.html

### Quote Dashboard

**Description**

- Reads `quoteResult` from session and displays:
  - total cost and confidence interval
  - cost breakdown
  - process details table
  - explainability drivers (SHAP if present, else heuristic)
  - DFM suggestion cards

**Source Files**

- /frontend/templates/dashboard.html

## UI Mockups (Design Iterations)

**Description**

- Additional standalone HTML mockups exist under `/ui/stitch_landing_upload/...`.
- These appear to be design snapshots (not wired into the running FastAPI templates).

**Source Files**

- /ui/stitch_landing_upload/*/code.html

**Notes**

- For API details, see /Summary/api_summary.md.
