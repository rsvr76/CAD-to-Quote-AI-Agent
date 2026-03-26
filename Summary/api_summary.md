# API Summary

## Base

**Description**

- APIs are hosted by the FastAPI app in /backend/main.py.
- Most endpoints accept a JSON body shaped like `{ geometry: ..., inputs: ... }`.

**Source Files**

- /backend/main.py (API routes; lines 143–395)
- /backend/models.py (schema definitions; lines 8–139)
- /openapi_tmp.json (captured OpenAPI snapshot)

## Endpoints

### `GET /api/samples`

**Description**

- Lists available pre-filled sample part names.

**Source Files**

- /backend/main.py: `list_samples` (lines 143–145)
- /backend/sample_parts.py (sample definitions)

**Response**

- `{ "samples": string[] }`

### `GET /api/samples/{name}`

**Description**

- Returns sample geometry + inputs by name.

**Source Files**

- /backend/main.py: `get_sample_part` (lines 149–155)
- /backend/sample_parts.py: `get_sample` (lines 72–76)

**Response**

- `{ geometry: GeometryData, inputs: UserInputs, ... }` (shape defined in /backend/sample_parts.py)

### `POST /api/routing`

**Description**

- Computes routing flags and machine selections from geometry + inputs.

**Source Files**

- /backend/main.py: `api_routing` (lines 159–168)
- /backend/routing.py: `route_processes` (lines 58–72)

**Request**

- JSON body:
  - `geometry`: /backend/models.py `GeometryData` (lines 8–17)
  - `inputs`: /backend/models.py `UserInputs` (lines 20–26)

**Response**

- /backend/models.py `RoutingDecision` (lines 58–61) serialized via `model_dump()`.

### `POST /api/stock`

**Description**

- Estimates stock volume/weight and shape.

**Source Files**

- /backend/main.py: `api_stock` (lines 172–183)
- /backend/stock.py: `estimate_stock` (lines 52–86)

**Request**

- JSON body:
  - `geometry`: `GeometryData`
  - `routing_flags`: /backend/models.py `RoutingFlags` (lines 29–33)
  - `material`: string
  - optional `stock_shape_override`: "block" | "cylinder" (string in request)

**Response**

- /backend/models.py `StockEstimate` (lines 64–68)

### `POST /api/quote`

**Description**

- Runs the full pipeline and returns the complete quote result.

**Source Files**

- /backend/main.py: `api_quote` (lines 187–272)
- Pipeline modules:
  - /backend/routing.py (Step 4)
  - /backend/stock.py (Steps 5–6)
  - /backend/ml_engine.py (Step 8)
  - /backend/cost.py (Step 10)
  - /backend/confidence.py (Step 9)
  - /backend/explainability.py (Step 11 fallback)
  - /backend/dfm.py (Step 12 candidates)

**Request**

- JSON body:
  - `geometry`: `GeometryData`
  - `inputs`: `UserInputs`
  - optional `routing`: `RoutingDecision` (to override)
  - optional `stock_override_kg`: number
  - optional `stock_shape_override`: string

**Response**

- /backend/models.py `FullQuoteResponse` (lines 123–132)

### `POST /api/dfm/simulate`

**Description**

- Intended to apply a selected DFM suggestion to the original quote and re-run the pipeline to show savings.

**Source Files**

- /backend/main.py: `api_dfm_simulate` (lines 276–304)

**Request**

- JSON body:
  - `suggestion_id`: string
  - `quote`: original `FullQuoteResponse`-like object

**Response**

- Intended: /backend/models.py `DFMComparison` (lines 135–139) plus savings fields.

**Notes**

- The handler currently does not return a response; see /Summary/findings.md.

### `POST /api/step/extract`

**Description**

- Upload a STEP file and receive extracted geometry metrics + preview image URL.

**Source Files**

- /backend/main.py: `api_step_extract` (lines 308–395)
- /backend/step_extract.py: `extract_step_geometry` (lines 50–171)

**Request**

- `multipart/form-data` with field `file`.

**Response**

- `{ geometry: GeometryData, preview_image_url: string | null }`

## HTML Page Routes

**Description**

- These serve the frontend templates.

**Source Files**

- /backend/main.py
  - `GET /` → index.html (lines 94–95)
  - `GET /geometry` → geometry.html (lines 99–100)
  - `GET /input` → input.html (lines 104–105)
  - `GET /routing` → routing.html (lines 109–110)
  - `GET /stock` → stock.html (lines 114–115)
  - `GET /progress` → progress.html (lines 119–120)
  - `GET /dashboard` → dashboard.html (lines 124–125)
  - `GET /dfm` → dfm.html (lines 129–130)
  - `GET /export` → export.html (lines 134–135)
