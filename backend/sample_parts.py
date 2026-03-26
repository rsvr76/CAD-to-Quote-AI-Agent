"""Three sample parts for demo — pre-filled geometry + user inputs."""

from __future__ import annotations

SAMPLE_PARTS: dict = {
    "steel_bracket": {
        "geometry": {
            "part_name": "Steel Bracket",
            "volume_cm3": 120.0,
            "surface_area_cm2": 210.0,
            "bbox_x_mm": 160.0,
            "bbox_y_mm": 45.0,
            "bbox_z_mm": 35.0,
            "aspect_ratio": 4.57,
            "num_faces": 842,
            "num_edges": 1260,
        },
        "inputs": {
            "num_holes": 6,
            "num_pockets": 2,
            "max_depth_mm": 25.0,
            "material": "Steel",
            "quantity": 50,
            "tolerance_class": "Fine",
        },
    },
    "aluminum_housing": {
        "geometry": {
            "part_name": "Aluminum Housing",
            "volume_cm3": 180.0,
            "surface_area_cm2": 300.0,
            "bbox_x_mm": 120.0,
            "bbox_y_mm": 110.0,
            "bbox_z_mm": 70.0,
            "aspect_ratio": 1.71,
            "num_faces": 1190,
            "num_edges": 1785,
        },
        "inputs": {
            "num_holes": 4,
            "num_pockets": 3,
            "max_depth_mm": 12.0,
            "material": "Aluminium",
            "quantity": 20,
            "tolerance_class": "Standard",
        },
    },
    "titanium_shaft": {
        "geometry": {
            "part_name": "Titanium Shaft",
            "volume_cm3": 95.0,
            "surface_area_cm2": 175.0,
            "bbox_x_mm": 280.0,
            "bbox_y_mm": 32.0,
            "bbox_z_mm": 30.0,
            "aspect_ratio": 9.33,
            "num_faces": 520,
            "num_edges": 780,
        },
        "inputs": {
            "num_holes": 1,
            "num_pockets": 0,
            "max_depth_mm": 18.0,
            "material": "Titanium",
            "quantity": 2,
            "tolerance_class": "Ultra-Fine",
        },
    },
}


def get_sample(name: str) -> dict:
    """Return sample data or raise KeyError."""
    if name not in SAMPLE_PARTS:
        raise KeyError(f"Unknown sample: {name}. Available: {list(SAMPLE_PARTS.keys())}")
    return SAMPLE_PARTS[name]
