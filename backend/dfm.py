"""DFM suggestion engine — Step 12.

Generates design-for-manufacturing suggestion *candidates* (variant_inputs + text).

Savings are computed server-side by simulating each variant through the actual
pipeline (routing → stock → time → cost) to keep numbers consistent with
`/api/dfm/simulate`.
"""

from __future__ import annotations

from .models import DFMSuggestion, GeometryData, RoutingFlags, UserInputs
from .cost import calc_setup_cost


# Machinability for DFM material-switch estimation
MACHINABILITY: dict[str, float] = {
    "Aluminium": 1.0,
    "Steel": 1.8,
    "Titanium": 5.0,
    "Brass": 1.2,
    "ABS": 0.5,
}


def generate_dfm_suggestions(
    geometry: GeometryData,
    inputs: UserInputs,
    routing: RoutingFlags,
    total_cost: float,
) -> list[DFMSuggestion]:
    """Generate DFM suggestion candidates.

    Note: `savings_inr` values are placeholders here and should be overwritten
    by the caller after simulating each variant.
    """
    suggestions: list[DFMSuggestion] = []

    # 1. Reduce holes (if > 4)
    if inputs.num_holes > 4:
        reduced = inputs.num_holes - 2
        suggestions.append(DFMSuggestion(
            suggestion_id="reduce_holes",
            change=f"Reduce holes from {inputs.num_holes} to {reduced}",
            savings_inr=0.0,
            reason="Fewer holes reduce drilling cycle time and tool changes.",
            icon="build",
            variant_inputs={"num_holes": reduced},
        ))

    # 2. Simplify pockets (if > 1)
    if inputs.num_pockets > 1:
        suggestions.append(DFMSuggestion(
            suggestion_id="simplify_pockets",
            change=f"Simplify pockets from {inputs.num_pockets} to {inputs.num_pockets - 1}",
            savings_inr=0.0,
            reason="Reducing pockets cuts milling passes.",
            icon="construction",
            variant_inputs={"num_pockets": inputs.num_pockets - 1},
        ))

    # 3. Switch material (Steel/Titanium → Aluminium)
    if inputs.material in ("Steel", "Titanium"):
        alt = "Aluminium"
        suggestions.append(DFMSuggestion(
            suggestion_id="switch_material",
            change=f"Switch material from {inputs.material} to {alt} (if function allows)",
            savings_inr=0.0,
            reason="Softer materials reduce both raw material and machining cost.",
            icon="swap_horiz",
            variant_inputs={"material": alt},
        ))

    # 4. Relax tolerance
    if inputs.tolerance_class in ("Fine", "Ultra-Fine"):
        next_tol = "Standard" if inputs.tolerance_class == "Fine" else "Fine"
        suggestions.append(DFMSuggestion(
            suggestion_id="relax_tolerance",
            change=f"Relax tolerance from {inputs.tolerance_class} to {next_tol}",
            savings_inr=0.0,
            reason="Relaxed tolerance can remove or reduce grinding effort.",
            icon="tune",
            variant_inputs={"tolerance_class": next_tol},
        ))

    # 5. Increase quantity (if qty == 1)
    if inputs.quantity == 1:
        suggestions.append(DFMSuggestion(
            suggestion_id="increase_qty",
            change="Increase order quantity from 1 to 5",
            savings_inr=0.0,
            reason="Setup cost is amortized across multiple units.",
            icon="add_shopping_cart",
            variant_inputs={"quantity": 5},
        ))

    # Caller will compute savings and rank.
    return suggestions
