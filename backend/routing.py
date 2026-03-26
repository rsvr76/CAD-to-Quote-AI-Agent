"""Process routing engine — Step 4.

Determines which machining processes are needed based on geometry + user inputs.
Entirely rule-based — no ML involved.
"""

from __future__ import annotations

from .models import (
    GeometryData,
    MachineAssignment,
    MachineSelection,
    OverrideInfo,
    RoutingDecision,
    RoutingDecisionLayer,
    RoutingFlags,
    UserInputs,
)


# Default machine for each process
DEFAULT_MACHINES: dict[str, str] = {
    "turning": "CNC Lathe",
    "milling": "3-Axis VMC",
    "drilling": "VMC Drill",
    "grinding": "Surface Grinder",
}

# Available machine options per process (for UI dropdown)
MACHINE_OPTIONS: dict[str, list[str]] = {
    "turning": ["CNC Lathe", "Manual Lathe"],
    "milling": ["3-Axis VMC", "4-Axis", "5-Axis"],
    "drilling": ["VMC Drill"],
    "grinding": ["Surface Grinder"],
}


def compute_routing_flags(geometry: GeometryData, inputs: UserInputs) -> RoutingFlags:
    """Apply routing rules from Steps/4.md."""
    return RoutingFlags(
        is_turning=int(geometry.aspect_ratio > 2.0),
        is_milling=int(inputs.num_pockets > 0 or geometry.surface_area_cm2 > 200),
        is_drilling=int(inputs.num_holes > 0),
        is_grinding=int(inputs.tolerance_class in ("Fine", "Ultra-Fine")),
    )


def build_default_machine_selection(flags: RoutingFlags) -> MachineSelection:
    """Assign default machines for each active process."""
    return MachineSelection(
        turning=DEFAULT_MACHINES["turning"] if flags.is_turning else None,
        milling=DEFAULT_MACHINES["milling"] if flags.is_milling else None,
        drilling=DEFAULT_MACHINES["drilling"] if flags.is_drilling else None,
        grinding=DEFAULT_MACHINES["grinding"] if flags.is_grinding else None,
    )


def route_processes(geometry: GeometryData, inputs: UserInputs) -> RoutingDecision:
    """Full routing decision: auto flags + default machines + no overrides."""
    auto_flags = compute_routing_flags(geometry, inputs)
    machines = build_default_machine_selection(auto_flags)

    return RoutingDecision(
        routing_decision=RoutingDecisionLayer(
            routing_auto=auto_flags,
            routing_final=auto_flags.model_copy(),  # start with auto = final
        ),
        machine_assignment=MachineAssignment(
            machine_selection_final=machines,
        ),
        overrides=OverrideInfo(),
    )


def get_routing_reason(process: str, geometry: GeometryData, inputs: UserInputs) -> str:
    """Return human-readable reason for why a process is ON/OFF."""
    reasons = {
        "turning": (
            f"Aspect ratio {geometry.aspect_ratio:.1f}:1 (> 2.0 threshold)"
            if geometry.aspect_ratio > 2.0
            else f"Aspect ratio {geometry.aspect_ratio:.1f}:1 (below 2.0 threshold)"
        ),
        "milling": (
            f"{inputs.num_pockets} pockets detected"
            if inputs.num_pockets > 0
            else (
                f"Surface area {geometry.surface_area_cm2:.0f} cm² (> 200 threshold)"
                if geometry.surface_area_cm2 > 200
                else "No pockets and surface area below threshold"
            )
        ),
        "drilling": (
            f"{inputs.num_holes} holes detected"
            if inputs.num_holes > 0
            else "No holes detected"
        ),
        "grinding": (
            f"Tolerance class = {inputs.tolerance_class}"
            if inputs.tolerance_class in ("Fine", "Ultra-Fine")
            else f"Tolerance = {inputs.tolerance_class} (no grinding needed)"
        ),
    }
    return reasons.get(process, "Unknown process")
