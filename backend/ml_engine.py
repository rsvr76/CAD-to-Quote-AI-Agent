"""ML Engine -- trained model inference + SHAP drivers.

This module is imported by the FastAPI app. On first import, it checks for
pre-trained model artefacts. If they are missing, it auto-generates a synthetic
dataset and trains the model, then saves the artefacts to disk for subsequent
runs.

This ensures the ML model is always available without manual pre-training.
"""

from __future__ import annotations

import json
import os
import random
import time
from typing import Optional

import numpy as np
import pandas as pd


def _log(msg: str) -> None:
    """Print timestamped progress message."""
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

from .models import CostDriver, GeometryData, RoutingFlags, UserInputs

# ── Paths ────────────────────────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_DIR = os.path.join(_DIR, "models_ml")
_BASE_DIR = os.path.dirname(_DIR)
_DATA_DIR = os.path.join(_BASE_DIR, "data")

_MODEL_PATH = os.path.join(_MODEL_DIR, "rf_machining_model.joblib")
_SHAP_PATH = os.path.join(_MODEL_DIR, "shap_explainer.joblib")
_COLS_PATH = os.path.join(_MODEL_DIR, "feature_columns.json")
_DATA_PATH = os.path.join(_DATA_DIR, "training_data.csv")

# ── Constants for dataset generation (same as scripts/generate_dataset.py) ──
MATERIALS = ["Aluminium", "Steel", "Titanium", "Brass", "ABS"]
MACHINABILITY_MAP: dict[str, float] = {
    "Aluminium": 1.0, "Steel": 1.8, "Titanium": 5.0, "Brass": 1.2, "ABS": 0.5,
}
MATERIAL_DENSITY_MAP: dict[str, float] = {
    "Aluminium": 2.7, "Steel": 7.85, "Titanium": 4.5, "Brass": 8.5, "ABS": 1.05,
}
TOLERANCE_MULTIPLIER: dict[str, float] = {
    "Standard": 1.0, "Fine": 1.25, "Ultra-Fine": 1.6,
}
N_SAMPLES = 8_000
NOISE_STD_FRACTION = 0.08
SEED = 42

FEATURE_COLS = [
    "volume_cm3", "surface_area_cm2", "aspect_ratio", "num_faces", "num_edges",
    "num_holes", "num_pockets", "max_depth_mm", "machinability", "density",
    "tolerance_factor", "is_turning", "is_milling", "is_drilling", "is_grinding",
]
TARGET_COL = "machining_time_min"

# ── Lazy-loaded artefacts ───────────────────────────────────────────────────
_model = None
_explainer = None
_feature_cols: list[str] = []
_load_attempted = False


def _generate_dataset() -> pd.DataFrame:
    """Generate synthetic manufacturing dataset inline."""
    _log("[1/4] Generating synthetic dataset (8000 rows)...")
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    rows: list[dict] = []
    for _ in range(N_SAMPLES):
        volume = rng.uniform(10, 500)
        surface_area = rng.uniform(50, 800)
        bbox_x = rng.uniform(20, 400)
        bbox_y = rng.uniform(10, 200)
        bbox_z = rng.uniform(5, 150)
        dims = sorted([bbox_x, bbox_y, bbox_z])
        aspect_ratio = dims[2] / max(dims[0], 0.1)
        num_faces = int(rng.integers(50, 2500))
        num_edges = int(rng.integers(80, 3000))

        num_holes = int(rng.integers(0, 15))
        num_pockets = int(rng.integers(0, 8))
        max_depth = rng.uniform(0, 60)
        material = random.choice(MATERIALS)
        tol_class = random.choice(list(TOLERANCE_MULTIPLIER.keys()))

        machinability = MACHINABILITY_MAP[material]
        density = MATERIAL_DENSITY_MAP[material]
        tol_factor = TOLERANCE_MULTIPLIER[tol_class]

        is_turning = int(aspect_ratio > 3.0 and rng.random() > 0.3)
        is_milling = int(num_pockets > 0 or rng.random() > 0.2)
        is_drilling = int(num_holes > 0)
        is_grinding = int(tol_class != "Standard" and rng.random() > 0.4)

        base = (volume * 0.03 + surface_area * 0.01) * machinability
        drill = 0.0
        if is_drilling and num_holes > 0:
            drill = num_holes * 0.3 * max(max_depth / 10.0, 1.0) * machinability
        mill = 0.0
        if is_milling and num_pockets > 0:
            mill = num_pockets * 1.2 * (surface_area / 150.0) * machinability
        turn = 0.0
        if is_turning:
            turn = 0.8 * volume * 0.02 * machinability * min(aspect_ratio / 2.0, 3.0)
        grind = 0.0
        if is_grinding:
            grind = 0.5 * surface_area * 0.005 * (tol_factor - 0.85)

        time_clean = (base + drill + mill + turn + grind) * tol_factor
        noise = rng.normal(0, NOISE_STD_FRACTION * time_clean)
        time_noisy = max(round(time_clean + noise, 2), 0.5)

        rows.append({
            "volume_cm3": round(volume, 2),
            "surface_area_cm2": round(surface_area, 2),
            "aspect_ratio": round(aspect_ratio, 3),
            "num_faces": num_faces,
            "num_edges": num_edges,
            "num_holes": num_holes,
            "num_pockets": num_pockets,
            "max_depth_mm": round(max_depth, 2),
            "machinability": machinability,
            "density": density,
            "tolerance_factor": tol_factor,
            "is_turning": is_turning,
            "is_milling": is_milling,
            "is_drilling": is_drilling,
            "is_grinding": is_grinding,
            "machining_time_min": time_noisy,
        })

    df = pd.DataFrame(rows)
    _log(f"[1/4] Dataset generated: {len(df)} rows")
    return df


def _train_model(df: pd.DataFrame) -> tuple:
    """Train RandomForest model and return (model, explainer, mae, r2)."""
    import joblib
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error, r2_score
    from sklearn.model_selection import train_test_split

    _log("[2/4] Training RandomForest (200 trees, depth 18)...")

    X = df[FEATURE_COLS].values
    y = df[TARGET_COL].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED,
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=18,
        min_samples_leaf=4,
        n_jobs=-1,
        random_state=SEED,
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    _log(f"[2/4] Model trained. MAE: {mae:.4f} min, R²: {r2:.4f}")

    _log("[3/4] Building SHAP TreeExplainer...")
    import shap
    explainer = shap.TreeExplainer(model)
    _ = explainer.shap_values(X_test[:1])
    _log("[3/4] SHAP TreeExplainer ready")

    return model, explainer, mae, r2


def _ensure_loaded() -> None:
    """Check for model artefacts, auto-generate and train if missing."""
    global _model, _explainer, _feature_cols, _load_attempted

    if _load_attempted:
        return
    _load_attempted = True

    if os.path.exists(_MODEL_PATH) and os.path.exists(_COLS_PATH):
        _log("[LOAD] Loading cached ML model...")
        import joblib

        with open(_COLS_PATH) as f:
            _feature_cols = json.load(f)

        _model = joblib.load(_MODEL_PATH)
        if os.path.exists(_SHAP_PATH):
            _explainer = joblib.load(_SHAP_PATH)

        _log("[LOAD] ML model ready from cache")
        return

    _log("[INIT] ML model not found. Starting auto-training...")
    os.makedirs(_MODEL_DIR, exist_ok=True)
    os.makedirs(_DATA_DIR, exist_ok=True)

    df = _generate_dataset()
    df.to_csv(_DATA_PATH, index=False)
    _log(f"[1/4] Dataset saved to data/training_data.csv")

    _model, _explainer, mae, r2 = _train_model(df)

    _log("[4/4] Saving model artefacts...")
    import joblib
    joblib.dump(_model, _MODEL_PATH)
    joblib.dump(_explainer, _SHAP_PATH)
    with open(_COLS_PATH, "w") as f:
        json.dump(FEATURE_COLS, f)

    _feature_cols = FEATURE_COLS

    _log(f"[4/4] Model saved to backend/models_ml/")
    _log(f"[INIT] ML model ready (MAE: {mae:.4f} min, R²: {r2:.4f})")


def _build_feature_vector(
    geo: GeometryData,
    inp: UserInputs,
    flags: RoutingFlags,
) -> np.ndarray:
    """Build a 1-D feature array matching the training column order."""
    machinability = MACHINABILITY_MAP.get(inp.material, 1.8)
    density = MATERIAL_DENSITY_MAP.get(inp.material, 7.85)
    tol_factor = TOLERANCE_MULTIPLIER.get(inp.tolerance_class, 1.0)

    feature_map = {
        "volume_cm3":       geo.volume_cm3,
        "surface_area_cm2": geo.surface_area_cm2,
        "aspect_ratio":     geo.aspect_ratio,
        "num_faces":        geo.num_faces,
        "num_edges":        geo.num_edges,
        "num_holes":        inp.num_holes,
        "num_pockets":      inp.num_pockets,
        "max_depth_mm":     inp.max_depth_mm,
        "machinability":    machinability,
        "density":          density,
        "tolerance_factor": tol_factor,
        "is_turning":       flags.is_turning,
        "is_milling":       flags.is_milling,
        "is_drilling":      flags.is_drilling,
        "is_grinding":      flags.is_grinding,
    }
    return np.array([[feature_map[c] for c in _feature_cols]])


# ── Fallback formula (same as ml_placeholder.py) ────────────────────────────
def _formula_fallback(
    geo: GeometryData, inp: UserInputs, flags: RoutingFlags,
) -> float:
    mac = MACHINABILITY_MAP.get(inp.material, 1.8)
    tol = TOLERANCE_MULTIPLIER.get(inp.tolerance_class, 1.0)
    base = (geo.volume_cm3 * 0.03 + geo.surface_area_cm2 * 0.01) * mac
    drill = (inp.num_holes * 0.3 * max(inp.max_depth_mm / 10.0, 1.0) * mac) if flags.is_drilling and inp.num_holes > 0 else 0
    mill = (inp.num_pockets * 1.2 * (geo.surface_area_cm2 / 150.0) * mac) if flags.is_milling and inp.num_pockets > 0 else 0
    turn = (0.8 * geo.volume_cm3 * 0.02 * mac * min(geo.aspect_ratio / 2.0, 3.0)) if flags.is_turning else 0
    grind = (0.5 * geo.surface_area_cm2 * 0.005 * (tol - 0.85)) if flags.is_grinding else 0
    return round(max((base + drill + mill + turn + grind) * tol, 0.5), 2)


# ═══════════════════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════════════════

def predict_machining_time(
    geometry: GeometryData,
    inputs: UserInputs,
    routing_flags: RoutingFlags,
) -> float:
    """Predict machining time in minutes using the trained RF model."""
    _ensure_loaded()
    X = _build_feature_vector(geometry, inputs, routing_flags)
    prediction = float(_model.predict(X)[0])
    return round(max(prediction, 0.5), 2)


def get_shap_drivers(
    geometry: GeometryData,
    inputs: UserInputs,
    routing_flags: RoutingFlags,
    top_n: int = 5,
) -> Optional[list[CostDriver]]:
    """Return SHAP-based feature impact drivers for the waterfall chart."""
    _ensure_loaded()
    if _explainer is None:
        return None

    X = _build_feature_vector(geometry, inputs, routing_flags)
    shap_values = _explainer.shap_values(X)[0]

    abs_impacts = np.abs(shap_values)
    sorted_idx = np.argsort(abs_impacts)[::-1][:top_n]

    HUMAN_NAMES = {
        "volume_cm3":       "Part volume",
        "surface_area_cm2": "Surface area",
        "aspect_ratio":     "Aspect ratio",
        "num_faces":        "Face count",
        "num_edges":        "Edge count",
        "num_holes":        "Number of holes",
        "num_pockets":      "Number of pockets",
        "max_depth_mm":     "Max hole depth",
        "machinability":    "Material hardness",
        "density":          "Material density",
        "tolerance_factor": "Tolerance class",
        "is_turning":       "Turning process",
        "is_milling":       "Milling process",
        "is_drilling":      "Drilling process",
        "is_grinding":      "Grinding process",
    }

    drivers: list[CostDriver] = []
    for idx in sorted_idx:
        col = _feature_cols[idx]
        sv = float(shap_values[idx])
        direction = "increases" if sv > 0 else "decreases"
        drivers.append(CostDriver(
            feature=HUMAN_NAMES.get(col, col),
            impact_value=round(abs(sv), 3),
            reason=f"{HUMAN_NAMES.get(col, col)} {direction} machining time by {abs(sv):.2f} min.",
        ))

    return drivers
