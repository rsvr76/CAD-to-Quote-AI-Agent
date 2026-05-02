# QuoteAI - Instant Cost Estimation

A FastAPI backend + simple HTML UI for an end-to-end CAD-to-quote workflow

STEP geometry extraction → guided inputs → process routing → stock estimation → ML machining-time prediction → cost breakdown → confidence → explainability → DFM suggestions.

## Project Details

### What is this project?

QuoteAI is a small web app + API that turns a CAD part (STEP upload) and a few user inputs into an explainable manufacturing quote.

### Problem

Manufacturing quotes for machined parts are often slow because they require:

- Extracting geometry and features from CAD
- Deciding which processes/machines are needed (routing)
- Estimating material stock and machining time
- Producing a cost breakdown, confidence range, and actionable DFM suggestions

### Our solution

This project implements a guided pipeline that:

1. Extracts geometry metrics from STEP using `gmsh` (volume, area, bbox, faces/edges + a lightweight preview image)
2. Collects user inputs (holes/pockets/depth/material/quantity/tolerance)
3. Computes routing flags (turning/milling/drilling/grinding) and default machine assignment
4. Estimates raw stock shape/weight
5. Predicts machining time using a trained RandomForest model (auto-trains on first run if missing)
6. Calculates total cost (material + machining + setup + overhead)
7. Produces a confidence interval + top cost drivers (SHAP when available, otherwise heuristic)
8. Generates DFM suggestions and scores savings by simulating each variant through the same pipeline

## Prerequisites

- Python **3.11+**

## Run Locally

### Quickstart (Windows PowerShell)

```powershell
cd <path-to-this-repo>

# Create & activate a virtualenv (recommended)
py -3.11 -m venv .venv  # or: python -m venv .venv

# If activation is blocked on your machine:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run the web app
python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000 --reload
```


### Quickstart (macOS / Linux)

```bash
cd <path-to-this-repo>

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000 --reload
```

## Notes

- **First run may take longer**: the ML module (`backend/ml_engine.py`) auto-trains a RandomForest model if artifacts are missing and writes them under `backend/models_ml/`.
- STEP upload parsing uses `gmsh` via `backend/step_extract.py`.

## Useful Commands

### Run the CLI backup demo

```bash
python Final.py
```

### Pre-generate training data and train the model (Optional)

```bash
python scripts/generate_dataset.py
python scripts/train_model.py
```

### Smoke-test STEP extraction  (Optional)

```bash
python backend/smoke_step_extract.py
```
