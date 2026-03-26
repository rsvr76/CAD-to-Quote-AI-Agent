"""ML placeholder — formula-based machining time estimation.

TODO: Replace with trained RandomForest model via joblib.load().
Currently uses deterministic formulas ported from Final.py to simulate ML output.
"""

from __future__ import annotations

from .models import GeometryData, RoutingFlags, UserInputs


# Machinability index (higher = harder to machine = more time)
MACHINABILITY: dict[str, float] = {
    "Aluminium": 1.0,
    "Steel": 1.8,
    "Titanium": 5.0,
    "Brass": 1.2,
    "ABS": 0.5,
}

# Tolerance time multiplier
TOLERANCE_MULTIPLIER: dict[str, float] = {
    "Standard": 1.0,
    "Fine": 1.25,
    "Ultra-Fine": 1.6,
}


def predict_machining_time(
    geometry: GeometryData,
    inputs: UserInputs,
    routing_flags: RoutingFlags,
) -> float:
    """Placeholder: formula-based machining time in minutes.

    When the trained ML model is ready, replace this function body with:
        model = joblib.load("model.pkl")
        features = build_feature_vector(geometry, inputs, routing_flags)
        return model.predict([features])[0]
    """
    machinability = MACHINABILITY.get(inputs.material, 1.8)
    tol_factor = TOLERANCE_MULTIPLIER.get(inputs.tolerance_class, 1.0)

    # Base cutting time from volume and surface area
    base_time = (geometry.volume_cm3 * 0.03 + geometry.surface_area_cm2 * 0.01) * machinability

    # Drilling contribution
    drill_time = 0.0
    if routing_flags.is_drilling and inputs.num_holes > 0:
        drill_time = inputs.num_holes * 0.3 * max(inputs.max_depth_mm / 10.0, 1.0) * machinability

    # Milling contribution
    mill_time = 0.0
    if routing_flags.is_milling and inputs.num_pockets > 0:
        mill_time = inputs.num_pockets * 1.2 * (geometry.surface_area_cm2 / 150.0) * machinability

    # Turning contribution
    turn_time = 0.0
    if routing_flags.is_turning:
        turn_time = 0.8 * geometry.volume_cm3 * 0.02 * machinability * min(geometry.aspect_ratio / 2.0, 3.0)

    # Grinding contribution
    grind_time = 0.0
    if routing_flags.is_grinding:
        grind_time = 0.5 * geometry.surface_area_cm2 * 0.005 * (tol_factor - 0.85)

    total_time = (base_time + drill_time + mill_time + turn_time + grind_time) * tol_factor

    # Ensure minimum meaningful time
    return round(max(total_time, 0.5), 2)
