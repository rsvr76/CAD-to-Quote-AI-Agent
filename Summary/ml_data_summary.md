# ML + Data Summary

## Training Data

**Description**

- The project uses a synthetic dataset (physics-inspired formula + noise) to train a machining-time predictor.

**Source Files**

- /scripts/generate_dataset.py (dataset generator; lines 1–170)
- /data/training_data.csv (generated dataset)

**Inputs/Outputs**

- Output file: `data/training_data.csv`
- Features include geometry, inputs, routing flags, and material/tolerance factors.
- Target: `machining_time_min`

**Dependencies**

- External: numpy, pandas

## Model Training

**Description**

- Trains a `RandomForestRegressor` on the synthetic dataset.
- Optionally creates a SHAP `TreeExplainer` if `shap` is installed.

**Source Files**

- /scripts/train_model.py
  - `FEATURE_COLS` list (lines 30–46)
  - RandomForest training + metrics + artifact saves (lines 49–170)

**Outputs**

- /backend/models_ml/rf_machining_model.joblib
- /backend/models_ml/feature_columns.json
- /backend/models_ml/shap_explainer.joblib (optional)

**Dependencies**

- External:
  - scikit-learn, joblib
  - shap (optional)

## Inference (Runtime)

**Description**

- Backend lazy-loads model artifacts on first use.
- If artifacts are missing (or SHAP explainer is missing), the app falls back gracefully.

**Source Files**

- /backend/ml_engine.py
  - Lazy-loading: `_ensure_loaded` (lines 46–71)
  - Feature vector: `_build_feature_vector` (lines 74–101)
  - Prediction: `predict_machining_time` (lines 122–137)
  - Explainability: `get_shap_drivers` (lines 140–190)
- /backend/ml_placeholder.py
  - Formula baseline: `predict_machining_time` (lines 30–93)

## Uncertainty / Confidence

**Description**

- If RF model is available: uses per-tree prediction variance to produce cost interval.
- Otherwise: heuristic uncertainty.

**Source Files**

- /backend/confidence.py
  - `_tree_based_confidence` (lines 45–106)
  - `_heuristic_confidence` (lines 109–153)
  - `estimate_confidence` (lines 156–168)

## Explainability (Drivers)

**Description**

- Preferred path: SHAP drivers from /backend/ml_engine.py.
- Fallback: heuristic “cost drivers” built from cost + machining breakdown.

**Source Files**

- /backend/ml_engine.py: `get_shap_drivers` (lines 140–190)
- /backend/explainability.py: `build_cost_drivers` (lines 12–64)
