from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile

try:
    from backend.step_extract import extract_step_geometry
except ModuleNotFoundError:  # running as a direct file: `python backend/...`
    from step_extract import extract_step_geometry


def _make_box_step(path: str) -> None:
    code = (
        "import sys; import gmsh; p=sys.argv[1]; "
        "gmsh.initialize([]); "
        "gmsh.option.setNumber('General.Terminal', 0); "
        "gmsh.option.setNumber('General.Verbosity', 0); "
        "gmsh.model.add('m'); "
        "gmsh.model.occ.addBox(0,0,0,50,30,20); "
        "gmsh.model.occ.synchronize(); "
        "gmsh.write(p); "
        "gmsh.finalize()"
    )
    subprocess.run([sys.executable, "-c", code, path], check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-preview", action="store_true")
    args = ap.parse_args()

    fd, step_path = tempfile.mkstemp(suffix=".step")
    os.close(fd)
    try:
        print("phase1: generate step")
        sys.stdout.flush()
        _make_box_step(step_path)

        print("phase2: read bytes")
        sys.stdout.flush()
        step_bytes = open(step_path, "rb").read()

        print("phase3: extract")
        sys.stdout.flush()
        res = extract_step_geometry(step_bytes, generate_preview=not args.no_preview)

        print("phase4: done")
        sys.stdout.flush()
        print(
            "volume_cm3=", res.volume_cm3,
            "area_cm2=", res.surface_area_cm2,
            "bbox=", (res.bbox_x_mm, res.bbox_y_mm, res.bbox_z_mm),
            "faces=", res.num_faces,
            "edges=", res.num_edges,
            "preview=", bool(res.preview_image_url),
        )
        return 0
    finally:
        try:
            os.unlink(step_path)
        except OSError:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
