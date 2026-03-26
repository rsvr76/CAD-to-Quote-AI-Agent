"""Cost drivers — Step 11 (Explainability).

Ranks cost components by impact and returns human-readable reasons.
TODO: Add SHAP TreeExplainer waterfall when ML model is ready.
"""

from __future__ import annotations

from .models import CostBreakdown, CostDriver, MachiningBreakdown, UserInputs


def build_cost_drivers(
    inputs: UserInputs,
    cost: CostBreakdown,
    machining_breakdown: MachiningBreakdown,
) -> list[CostDriver]:
    """Return top cost drivers ranked by ₹ impact."""
    drivers: list[CostDriver] = []

    # Material driver
    drivers.append(CostDriver(
        feature=f"{inputs.material} raw material",
        impact_value=cost.material_cost_inr,
        reason="Material choice affects both raw cost and machinability.",
    ))

    # Per-process drivers from machining breakdown
    for detail in machining_breakdown.details:
        process = detail.process
        if process == "Drilling" and inputs.num_holes > 0:
            drivers.append(CostDriver(
                feature=f"{inputs.num_holes} holes at {inputs.max_depth_mm:.0f}mm depth",
                impact_value=detail.cost_inr,
                reason="Drilling time rises with hole count and depth.",
            ))
        elif process == "Milling" and inputs.num_pockets > 0:
            drivers.append(CostDriver(
                feature=f"{inputs.num_pockets} pocket features",
                impact_value=detail.cost_inr,
                reason="Pocket machining adds milling passes and toolpath complexity.",
            ))
        elif process == "Turning":
            drivers.append(CostDriver(
                feature="Elongated geometry (turning required)",
                impact_value=detail.cost_inr,
                reason="Longer cylindrical geometry increases turning effort.",
            ))
        elif process == "Grinding":
            drivers.append(CostDriver(
                feature=f"{inputs.tolerance_class} tolerance requirement",
                impact_value=detail.cost_inr,
                reason="Tighter tolerance adds finishing effort.",
            ))

    # Setup driver
    drivers.append(CostDriver(
        feature=f"Setup for qty {inputs.quantity}",
        impact_value=cost.setup_cost_inr,
        reason="Setup cost is amortized across batch size.",
    ))

    # Sort by impact descending, return top 4
    drivers.sort(key=lambda d: d.impact_value, reverse=True)
    return drivers[:4]
