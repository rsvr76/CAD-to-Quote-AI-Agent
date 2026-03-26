"""Train a RandomForest regressor on the synthetic machining-time dataset.

Outputs:
    backend/models_ml/rf_machining_model.joblib   — trained model
    backend/models_ml/shap_explainer.joblib        — SHAP TreeExplainer
    backend/models_ml/feature_columns.json         — ordered feature list

Usage:
    python scripts/train_model.py
"""

from __future__ import annotations

import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "training_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models_ml")

FEATURE_COLS = [
    "volume_cm3",
    "surface_area_cm2",
    "aspect_ratio",
    "num_faces",
    "num_edges",
    "num_holes",
    "num_pockets",
    "max_depth_mm",
    "machinability",
    "density",
    "tolerance_factor",
    "is_turning",
    "is_milling",
    "is_drilling",
    "is_grinding",
]
TARGET_COL = "machining_time_min"


def main() -> None:
    # ── 1. Load data ─────────────────────────────────────────────────────────
    if not os.path.exists(DATA_PATH):
        print("[ERR] Dataset not found. Run  python scripts/generate_dataset.py  first.")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    print(f"[OK] Loaded {len(df)} rows from {DATA_PATH}")

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    # ── 2. Train / test split ────────────────────────────────────────────────
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42,
    )
    print(f"  Train: {len(X_train)}  |  Test: {len(X_test)}")

    # ── 3. Train RandomForest ────────────────────────────────────────────────
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=18,
        min_samples_leaf=4,
        n_jobs=-1,
        random_state=42,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n-- Test Metrics --")
    print(f"  MAE  : {mae:.4f} min")
    print(f"  R2   : {r2:.4f}")

    # ── 4. Feature Importances ───────────────────────────────────────────────
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    print(f"\n-- Feature Importances --")
    for i in sorted_idx:
        print(f"  {FEATURE_COLS[i]:25s} {importances[i]:.4f}")

    # ── 5. SHAP Explainer ────────────────────────────────────────────────────
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        # Smoke-test on a single sample
        _ = explainer.shap_values(X_test[:1])
        print(f"\n[OK] SHAP TreeExplainer created and validated")
        has_shap = True
    except ImportError:
        print("\n[WARN] shap not installed -- skipping explainer. Install with: pip install shap")
        explainer = None
        has_shap = False

    # ── 6. Save artefacts ────────────────────────────────────────────────────
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, "rf_machining_model.joblib")
    joblib.dump(model, model_path)
    print(f"\n[OK] Model saved -> {model_path}")

    cols_path = os.path.join(MODEL_DIR, "feature_columns.json")
    with open(cols_path, "w") as f:
        json.dump(FEATURE_COLS, f, indent=2)
    print(f"[OK] Feature columns saved -> {cols_path}")

    if has_shap:
        shap_path = os.path.join(MODEL_DIR, "shap_explainer.joblib")
        joblib.dump(explainer, shap_path)
        print(f"[OK] SHAP explainer saved -> {shap_path}")

    # ── 7. Summary ───────────────────────────────────────────────────────────
    print(f"\n{'=' * 50}")
    print(f"  Model   : RandomForest (200 trees, depth 18)")
    print(f"  MAE     : {mae:.4f} min")
    print(f"  R2      : {r2:.4f}")
    print(f"  SHAP    : {'Yes' if has_shap else 'No (install shap)'}")
    print(f"  Output  : {MODEL_DIR}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
