"""ML Engine -- trained model inference + SHAP drivers.

This module is imported by the FastAPI app. To keep server startup fast and
robust across environments, model artefacts are *lazy-loaded* on first use.

If the model (or its dependencies) are not available, we fall back to the
deterministic formula from `ml_placeholder.py`.
"""

from __future__ import annotations

import json
import os
from typing import Optional

import numpy as np

from .models import CostDriver, GeometryData, RoutingFlags, UserInputs

# ── Paths ────────────────────────────────────────────────────────────────────
_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_DIR = os.path.join(_DIR, "models_ml")

_MODEL_PATH = os.path.join(_MODEL_DIR, "rf_machining_model.joblib")
_SHAP_PATH  = os.path.join(_MODEL_DIR, "shap_explainer.joblib")
_COLS_PATH  = os.path.join(_MODEL_DIR, "feature_columns.json")

# ── Machinability / density / tolerance maps (same as generate_dataset.py) ──
MACHINABILITY: dict[str, float] = {
    "Aluminium": 1.0, "Steel": 1.8, "Titanium": 5.0, "Brass": 1.2, "ABS": 0.5,
}
MATERIAL_DENSITY: dict[str, float] = {
    "Aluminium": 2.7, "Steel": 7.85, "Titanium": 4.5, "Brass": 8.5, "ABS": 1.05,
}
TOLERANCE_FACTOR: dict[str, float] = {
    "Standard": 1.0, "Fine": 1.25, "Ultra-Fine": 1.6,
}

# ── Lazy-loaded artefacts ───────────────────────────────────────────────────
_model = None
_explainer = None
_feature_cols: list[str] = []
_load_attempted = False


def _ensure_loaded() -> None:
    """Load model artefacts once, on-demand.

    Never raises: on any failure we keep `_model`/`_explainer` as None.
    """
    global _model, _explainer, _feature_cols, _load_attempted
    if _load_attempted:
        return
    _load_attempted = True

    if not (os.path.exists(_MODEL_PATH) and os.path.exists(_COLS_PATH)):
        return

    try:
        import joblib  # local import to avoid heavy deps at server startup

        with open(_COLS_PATH) as f:
            _feature_cols = json.load(f)

        _model = joblib.load(_MODEL_PATH)
        if os.path.exists(_SHAP_PATH):
            _explainer = joblib.load(_SHAP_PATH)
    except Exception:
        _model = None
        _explainer = None
        _feature_cols = []


def _build_feature_vector(
    geo: GeometryData,
    inp: UserInputs,
    flags: RoutingFlags,
) -> np.ndarray:
    """Build a 1-D feature array matching the training column order."""
    machinability = MACHINABILITY.get(inp.material, 1.8)
    density = MATERIAL_DENSITY.get(inp.material, 7.85)
    tol_factor = TOLERANCE_FACTOR.get(inp.tolerance_class, 1.0)

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
    mac = MACHINABILITY.get(inp.material, 1.8)
    tol = TOLERANCE_FACTOR.get(inp.tolerance_class, 1.0)
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
    """Predict machining time in minutes using the trained RF model.

    Falls back to the deterministic formula if the model file is missing.
    """
    _ensure_loaded()
    if _model is None or not _feature_cols:
        return _formula_fallback(geometry, inputs, routing_flags)

    X = _build_feature_vector(geometry, inputs, routing_flags)
    prediction = float(_model.predict(X)[0])
    return round(max(prediction, 0.5), 2)


def get_shap_drivers(
    geometry: GeometryData,
    inputs: UserInputs,
    routing_flags: RoutingFlags,
    top_n: int = 5,
) -> Optional[list[CostDriver]]:
    """Return SHAP-based feature impact drivers for the waterfall chart.

    Returns None if SHAP explainer is not available.
    """
    _ensure_loaded()
    if _explainer is None or _model is None or not _feature_cols:
        return None

    X = _build_feature_vector(geometry, inputs, routing_flags)
    shap_values = _explainer.shap_values(X)[0]  # shape: (n_features,)

    # Build ranked list of drivers
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
