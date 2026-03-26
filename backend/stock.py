"""Stock estimation — Steps 5-6.

Estimates raw material stock (cylindrical bar or rectangular block)
based on geometry + routing flags + material.
"""

from __future__ import annotations

import math

from .models import GeometryData, RoutingFlags, StockEstimate


# Material densities in g/cm³
DENSITY: dict[str, float] = {
    "Aluminium": 2.70,
    "Steel": 7.85,
    "Brass": 8.50,
    "Titanium": 4.50,
    "ABS": 1.05,
}

# Margins
TURNING_DIAMETER_MARGIN = 0.10  # 10% bar diameter margin
MILLING_MARGIN_MM = 5  # mm per side for clamping/clearance


def cylindrical_stock_volume(bbox_x: float, bbox_y: float, bbox_z: float) -> float:
    """Estimate cylindrical bar stock volume in cm³."""
    dims = sorted([bbox_x, bbox_y, bbox_z], reverse=True)
    length = dims[0]
    cross = dims[1:]
    diameter = max(cross) * (1.0 + TURNING_DIAMETER_MARGIN)
    volume_mm3 = math.pi * (diameter / 2) ** 2 * length
    return round(volume_mm3 / 1000.0, 2)


def block_stock_volume(bbox_x: float, bbox_y: float, bbox_z: float) -> float:
    """Estimate rectangular block stock volume in cm³."""
    m = MILLING_MARGIN_MM
    volume_mm3 = (bbox_x + 2 * m) * (bbox_y + 2 * m) * (bbox_z + 2 * m)
    return round(volume_mm3 / 1000.0, 2)


def estimate_stock_weight(stock_volume_cm3: float, material: str) -> float:
    """Convert stock volume to weight in kg."""
    density = DENSITY.get(material, 7.85)  # default to Steel
    weight_grams = stock_volume_cm3 * density
    return round(weight_grams / 1000.0, 2)


def estimate_stock(
    geometry: GeometryData,
    routing_flags: RoutingFlags,
    material: str,
    override_kg: float | None = None,
    stock_shape_override: str | None = None,
) -> StockEstimate:
    """Complete stock estimation per Steps 5-6."""
    chosen_shape = None
    if stock_shape_override in ("block", "cylinder"):
        chosen_shape = stock_shape_override
    else:
        chosen_shape = "cylinder" if bool(routing_flags.is_turning) else "block"

    if chosen_shape == "cylinder":
        stock_shape = "cylinder"
        vol = cylindrical_stock_volume(geometry.bbox_x_mm, geometry.bbox_y_mm, geometry.bbox_z_mm)
    else:
        stock_shape = "block"
        vol = block_stock_volume(geometry.bbox_x_mm, geometry.bbox_y_mm, geometry.bbox_z_mm)

    weight = estimate_stock_weight(vol, material)
    final_weight = override_kg if override_kg is not None else weight

    # Waste percentage
    waste = 0.0
    if vol > 0 and geometry.volume_cm3 > 0:
        waste = round((1.0 - geometry.volume_cm3 / vol) * 100, 1)

    return StockEstimate(
        stock_shape=stock_shape,
        stock_volume_cm3=vol,
        stock_weight_kg=final_weight,
        material=material,
    )
