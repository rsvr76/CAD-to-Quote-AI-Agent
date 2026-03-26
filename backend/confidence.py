"""Prediction interval / risk estimation -- Step 9.

Uses the RandomForest's individual tree predictions to compute
percentile-based confidence intervals. Falls back to heuristic
margins if the model is not available.
"""

from __future__ import annotations

import os
from typing import Optional

import numpy as np

from .models import ConfidenceRange, GeometryData, RoutingFlags, UserInputs

# ── Lazy-loaded model for tree-based percentiles ────────────────────────────
_model = None
_load_attempted = False


def _ensure_model_loaded() -> None:
    """Load the trained RF model on-demand.

    Never raises: on any failure we keep `_model` as None.
    """
    global _model, _load_attempted
    if _load_attempted:
        return
    _load_attempted = True

    try:
        _DIR = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(_DIR, "models_ml", "rf_machining_model.joblib")
        if not os.path.exists(model_path):
            return

        import joblib  # local import to avoid heavy deps at server startup

        _model = joblib.load(model_path)
    except Exception:
        _model = None


def _tree_based_confidence(
    geometry: GeometryData,
    inputs: UserInputs,
    routing: RoutingFlags,
    total_cost: float,
) -> Optional[ConfidenceRange]:
    """Use individual tree predictions to build percentile intervals.

    Each tree in the RandomForest gives a slightly different prediction.
    We use the spread of these predictions to estimate uncertainty,
    then scale from machining-time variance to cost variance.
    """
    _ensure_model_loaded()
    if _model is None:
        return None

    try:
        from .ml_engine import _build_feature_vector, MACHINABILITY, TOLERANCE_FACTOR

        X = _build_feature_vector(geometry, inputs, routing)

        # Get predictions from each individual tree
        tree_predictions = np.array([
            tree.predict(X)[0] for tree in _model.estimators_
        ])

        # Percentiles on machining time predictions
        p10 = float(np.percentile(tree_predictions, 10))
        p50 = float(np.percentile(tree_predictions, 50))
        p90 = float(np.percentile(tree_predictions, 90))

        # Relative spread: how much the trees disagree
        if p50 > 0:
            spread_low = (p50 - p10) / p50    # fractional spread below median
            spread_high = (p90 - p50) / p50   # fractional spread above median
        else:
            spread_low = 0.08
            spread_high = 0.08

        # Scale to cost
        low_cost = round(total_cost * (1 - spread_low), 2)
        high_cost = round(total_cost * (1 + spread_high), 2)
        margin = round(max(spread_low, spread_high) * 100, 1)

        # Risk level based on tree agreement
        cv = float(np.std(tree_predictions) / max(np.mean(tree_predictions), 0.01))
        if cv < 0.08:
            risk = "Low"
        elif cv < 0.15:
            risk = "Medium"
        else:
            risk = "High"

        return ConfidenceRange(
            low=max(low_cost, 0),
            nominal=total_cost,
            high=high_cost,
            risk_level=risk,
            margin_pct=margin,
        )
    except Exception:
        return None


def _heuristic_confidence(
    inputs: UserInputs,
    routing: RoutingFlags,
    total_cost: float,
) -> ConfidenceRange:
    """Fallback heuristic-based confidence intervals."""
    uncertainty = 0.08  # base 8%

    if inputs.material == "Titanium":
        uncertainty += 0.05
    if inputs.tolerance_class == "Ultra-Fine":
        uncertainty += 0.05
    if inputs.quantity <= 1:
        uncertainty += 0.03
    if inputs.num_holes >= 6:
        uncertainty += 0.03

    active_count = sum([
        routing.is_turning,
        routing.is_milling,
        routing.is_drilling,
        routing.is_grinding,
    ])
    if active_count >= 3:
        uncertainty += 0.03

    confidence_pct = max(55, min(92, int((1 - uncertainty) * 100)))
    low = round(total_cost * (1 - uncertainty), 2)
    high = round(total_cost * (1 + uncertainty), 2)
    margin = round(uncertainty * 100, 1)

    if confidence_pct >= 85:
        risk = "Low"
    elif confidence_pct >= 70:
        risk = "Medium"
    else:
        risk = "High"

    return ConfidenceRange(
        low=low,
        nominal=total_cost,
        high=high,
        risk_level=risk,
        margin_pct=margin,
    )


def estimate_confidence(
    inputs: UserInputs,
    routing: RoutingFlags,
    total_cost: float,
    geometry: GeometryData | None = None,
) -> ConfidenceRange:
    """Compute confidence range -- tree-based if model available, else heuristic."""
    if geometry is not None:
        tree_result = _tree_based_confidence(geometry, inputs, routing, total_cost)
        if tree_result is not None:
            return tree_result

    return _heuristic_confidence(inputs, routing, total_cost)
