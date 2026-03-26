"""Generate a synthetic manufacturing dataset for training the machining-time ML model.

Uses the same physics-inspired formulas from ml_placeholder.py as the ground truth,
then adds controlled Gaussian noise so the trained model can generalise beyond the
deterministic formula.

Output: data/training_data.csv  (~8 000 rows, 13 features + 1 target)
"""

from __future__ import annotations

import os
import random

import numpy as np
import pandas as pd

# ── constants (mirrored from ml_placeholder.py) ──────────────────────────────
MATERIALS = ["Aluminium", "Steel", "Titanium", "Brass", "ABS"]
MACHINABILITY = {"Aluminium": 1.0, "Steel": 1.8, "Titanium": 5.0, "Brass": 1.2, "ABS": 0.5}
MATERIAL_DENSITY = {"Aluminium": 2.7, "Steel": 7.85, "Titanium": 4.5, "Brass": 8.5, "ABS": 1.05}

TOLERANCE_CLASSES = ["Standard", "Fine", "Ultra-Fine"]
TOLERANCE_MULTIPLIER = {"Standard": 1.0, "Fine": 1.25, "Ultra-Fine": 1.6}

N_SAMPLES = 8_000
NOISE_STD_FRACTION = 0.08  # ±8 % Gaussian noise on the target
SEED = 42


def _formula_time(
    volume: float, surface_area: float, aspect_ratio: float,
    num_holes: int, num_pockets: int, max_depth: float,
    machinability: float, tol_factor: float,
    is_turning: int, is_milling: int, is_drilling: int, is_grinding: int,
) -> float:
    """Deterministic formula identical to ml_placeholder.predict_machining_time."""
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

    total = (base + drill + mill + turn + grind) * tol_factor
    return max(total, 0.5)


def generate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    random.seed(SEED)

    rows: list[dict] = []
    for _ in range(N_SAMPLES):
        # ── sample geometry ──
        volume = rng.uniform(10, 500)
        surface_area = rng.uniform(50, 800)
        bbox_x = rng.uniform(20, 400)
        bbox_y = rng.uniform(10, 200)
        bbox_z = rng.uniform(5, 150)
        dims = sorted([bbox_x, bbox_y, bbox_z])
        aspect_ratio = dims[2] / max(dims[0], 0.1)
        num_faces = int(rng.integers(50, 2500))
        num_edges = int(rng.integers(80, 3000))

        # ── sample inputs ──
        num_holes = int(rng.integers(0, 15))
        num_pockets = int(rng.integers(0, 8))
        max_depth = rng.uniform(0, 60)
        material = random.choice(MATERIALS)
        tol_class = random.choice(TOLERANCE_CLASSES)

        machinability = MACHINABILITY[material]
        density = MATERIAL_DENSITY[material]
        tol_factor = TOLERANCE_MULTIPLIER[tol_class]

        # ── sample routing flags (realistic combinations) ──
        is_turning = int(aspect_ratio > 3.0 and rng.random() > 0.3)
        is_milling = int(num_pockets > 0 or rng.random() > 0.2)
        is_drilling = int(num_holes > 0)
        is_grinding = int(tol_class != "Standard" and rng.random() > 0.4)

        # ── compute target ──
        time_clean = _formula_time(
            volume, surface_area, aspect_ratio,
            num_holes, num_pockets, max_depth,
            machinability, tol_factor,
            is_turning, is_milling, is_drilling, is_grinding,
        )
        noise = rng.normal(0, NOISE_STD_FRACTION * time_clean)
        time_noisy = max(round(time_clean + noise, 3), 0.5)

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

    return pd.DataFrame(rows)


if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "training_data.csv")

    df = generate()
    df.to_csv(out_path, index=False)
    print(f"[OK] Generated {len(df)} rows -> {out_path}")
    print(f"  Features : {list(df.columns[:-1])}")
    print(f"  Target   : machining_time_min")
    print(f"  Stats    :")
    print(df['machining_time_min'].describe())
