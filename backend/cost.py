"""Cost calculation engine — Step 10.

Computes material, machining, setup, and overhead costs using deterministic formulas.
Only machining cost depends on the ML prediction.
"""

from __future__ import annotations

import math

from .models import (
    CostBreakdown,
    MachineSelection,
    MachiningBreakdown,
    ProcessDetail,
    RoutingFlags,
)


# ──────────────────────────────────
# Lookup tables (from Steps/10.md)
# ──────────────────────────────────

PRICE_PER_KG: dict[str, float] = {
    "Aluminium": 220.0,
    "Steel": 85.0,
    "Brass": 450.0,
    "Titanium": 3200.0,
    "ABS": 150.0,
}

BATCH_DISCOUNT_TIERS: list[tuple[int, int, float]] = [
    (1, 9, 1.00),
    (10, 50, 0.90),
    (51, 200, 0.80),
    (201, 999999, 0.70),
]

RATE_PER_MACHINE_PER_HOUR: dict[str, float] = {
    "3-Axis VMC": 1000.0,
    "4-Axis": 1300.0,
    "5-Axis": 1800.0,
    "CNC Lathe": 1200.0,
    "Manual Lathe": 700.0,
    "Surface Grinder": 900.0,
    "VMC Drill": 900.0,
}

PROCESS_TIME_WEIGHTS: dict[str, float] = {
    "turning": 0.35,
    "milling": 0.45,
    "drilling": 0.15,
    "grinding": 0.05,
}

OVERHEAD_RATE: dict[str, float] = {
    "Aluminium": 0.12,
    "Steel": 0.15,
    "Brass": 0.18,
    "Titanium": 0.22,
    "ABS": 0.10,
}


# ──────────────────────────────────
# Individual cost functions
# ──────────────────────────────────

def get_batch_discount(quantity: int) -> float:
    for low, high, disc in BATCH_DISCOUNT_TIERS:
        if low <= quantity <= high:
            return disc
    return 1.0


def calc_material_cost(stock_weight_kg: float, material: str, quantity: int) -> float:
    price = PRICE_PER_KG.get(material, 85.0)
    discount = get_batch_discount(quantity)
    return round(stock_weight_kg * price * discount, 2)


def allocate_time(machining_time_min: float, routing: RoutingFlags) -> dict[str, float]:
    """Split total machining time across active processes using heuristic weights."""
    active = {
        "turning": routing.is_turning,
        "milling": routing.is_milling,
        "drilling": routing.is_drilling,
        "grinding": routing.is_grinding,
    }
    total_weight = sum(PROCESS_TIME_WEIGHTS[p] for p, on in active.items() if on)
    if total_weight <= 0:
        return {p: 0.0 for p in active}
    return {
        p: round(machining_time_min * (PROCESS_TIME_WEIGHTS[p] / total_weight), 2) if on else 0.0
        for p, on in active.items()
    }


def calc_machining_cost(
    machining_time_min: float,
    routing: RoutingFlags,
    machines: MachineSelection,
) -> tuple[float, MachiningBreakdown]:
    """Calculate machining cost and per-process breakdown."""
    time_split = allocate_time(machining_time_min, routing)
    machine_map = {
        "turning": machines.turning,
        "milling": machines.milling,
        "drilling": machines.drilling,
        "grinding": machines.grinding,
    }

    details: list[ProcessDetail] = []
    total_cost = 0.0
    total_time = 0.0

    for process, minutes in time_split.items():
        if minutes <= 0:
            continue
        machine = machine_map.get(process) or "3-Axis VMC"
        rate = RATE_PER_MACHINE_PER_HOUR.get(machine, 1000.0)
        cost = round(minutes * (rate / 60.0), 2)
        total_cost += cost
        total_time += minutes
        details.append(ProcessDetail(
            process=process.capitalize(),
            machine=machine,
            time_min=minutes,
            rate_per_hr_inr=rate,
            cost_inr=cost,
        ))

    breakdown = MachiningBreakdown(
        details=details,
        total_time_min=round(total_time, 2),
        total_cost_inr=round(total_cost, 2),
    )
    return round(total_cost, 2), breakdown


def calc_setup_cost(quantity: int) -> float:
    return round(max(2000.0 / math.sqrt(max(quantity, 1)), 200.0), 2)


def calc_overhead_cost(material_cost: float, machining_cost: float, setup_cost: float, material: str) -> float:
    subtotal = material_cost + machining_cost + setup_cost
    rate = OVERHEAD_RATE.get(material, 0.15)
    return round(subtotal * rate, 2)


# ──────────────────────────────────
# Full quote calculation
# ──────────────────────────────────

def calculate_full_cost(
    stock_weight_kg: float,
    machining_time_min: float,
    material: str,
    quantity: int,
    routing: RoutingFlags,
    machines: MachineSelection,
) -> tuple[CostBreakdown, MachiningBreakdown]:
    """Calculate complete cost breakdown per Step 10."""
    mat = calc_material_cost(stock_weight_kg, material, quantity)
    mach, mach_breakdown = calc_machining_cost(machining_time_min, routing, machines)
    stp = calc_setup_cost(quantity)
    ovhd = calc_overhead_cost(mat, mach, stp, material)
    total = round(mat + mach + stp + ovhd, 2)

    breakdown = CostBreakdown(
        material_cost_inr=mat,
        machining_cost_inr=mach,
        setup_cost_inr=stp,
        overhead_cost_inr=ovhd,
        total_cost_inr=total,
    )
    return breakdown, mach_breakdown
