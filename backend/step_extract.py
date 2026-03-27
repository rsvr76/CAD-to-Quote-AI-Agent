"""STEP geometry extraction utilities.

This project is a CAD-to-quote demo. To make uploaded STEP files reflect the
real design (measurements + a visible preview), we parse STEP using the `gmsh`
Python package.

`gmsh` bundles an OpenCascade kernel and is pip-installable on Windows, making it
the most reliable option here.

We extract:
- Volume (cm^3)
- Surface area (cm^2)
- Bounding box (mm)
- Face (surface) count and edge (curve) count

We also generate a lightweight preview PNG from a surface triangulation so the
existing UI (which expects an image URL) can show a design preview without
adding a full 3D viewer.
"""

from __future__ import annotations

import base64
import io
import math
import os
import tempfile
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StepExtractResult:
    volume_cm3: float
    surface_area_cm2: float
    bbox_x_mm: float
    bbox_y_mm: float
    bbox_z_mm: float
    num_faces: int
    num_edges: int
    preview_image_url: str | None
    hole_count_est: int
    hole_diam_min_mm: float | None
    hole_diam_max_mm: float | None
    max_drilling_depth_est_mm: float
    feature_confidence: str


def _safe_float(v: float) -> float:
    if not (isinstance(v, (int, float)) and math.isfinite(v)):
        return 0.0
    return float(v)


def extract_step_geometry(
    step_bytes: bytes,
    *,
    deflection: float = 0.6,
    generate_preview: bool = True,
) -> StepExtractResult:
    """Parse STEP bytes and extract metrics + optional preview.

    Units:
    - We assume the STEP file units are millimeters (typical for mechanical CAD).
    - Volume returned by gmsh is in mm^3, surface area in mm^2.
    - We convert to cm^3 and cm^2 to match the rest of the app.
    """

    try:
        import gmsh
    except Exception as exc:  # pragma: no cover
        raise RuntimeError("STEP parsing dependency missing. Install `gmsh`.") from exc

    with tempfile.NamedTemporaryFile(delete=False, suffix=".step") as tmp:
        tmp.write(step_bytes)
        tmp_path = tmp.name

    try:
        gmsh.initialize([])
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.model.add("step")

        try:
            gmsh.model.occ.importShapes(tmp_path)
            gmsh.model.occ.synchronize()

            # Entities
            volumes = gmsh.model.getEntities(3)
            surfaces = gmsh.model.getEntities(2)
            curves = gmsh.model.getEntities(1)

            num_faces = len(surfaces)
            num_edges = len(curves)

            # Bounding box across all volumes (preferred) or surfaces.
            bbox_entities = volumes or surfaces
            if not bbox_entities:
                raise RuntimeError("No valid solids/surfaces found in STEP")

            xmin = ymin = zmin = float("inf")
            xmax = ymax = zmax = float("-inf")
            for dim, tag in bbox_entities:
                bxmin, bymin, bzmin, bxmax, bymax, bzmax = gmsh.model.getBoundingBox(dim, tag)
                xmin = min(xmin, bxmin)
                ymin = min(ymin, bymin)
                zmin = min(zmin, bzmin)
                xmax = max(xmax, bxmax)
                ymax = max(ymax, bymax)
                zmax = max(zmax, bzmax)

            bbox_x_mm = max(0.0, _safe_float(xmax - xmin))
            bbox_y_mm = max(0.0, _safe_float(ymax - ymin))
            bbox_z_mm = max(0.0, _safe_float(zmax - zmin))

            hole_count_est, hole_dmin, hole_dmax, feat_conf = _estimate_holes_from_curves(gmsh)
            max_drill_est = _estimate_max_drilling_depth(bbox_x_mm, bbox_y_mm, bbox_z_mm)

            # Mass properties
            volume_mm3 = 0.0
            for _dim, vtag in volumes:
                try:
                    volume_mm3 += float(gmsh.model.occ.getMass(3, vtag))
                except Exception:
                    pass

            area_mm2 = 0.0
            for _dim, stag in surfaces:
                try:
                    area_mm2 += float(gmsh.model.occ.getMass(2, stag))
                except Exception:
                    pass

            volume_cm3 = round(max(volume_mm3 / 1000.0, 0.0), 4)
            surface_area_cm2 = round(max(area_mm2 / 100.0, 0.0), 4)

            # Preview render (best-effort): surface mesh triangles
            preview_url: str | None = None
            if generate_preview:
                try:
                    # Keep meshing coarse and scale-aware; previews don't need high fidelity.
                    # This avoids pathological runtimes for large parts.
                    size_mm = max(bbox_x_mm, bbox_y_mm, bbox_z_mm)
                    if size_mm <= 0:
                        size_mm = 100.0

                    target = max(float(deflection), size_mm / 60.0)
                    char_min = max(target * 0.6, 0.8)
                    char_max = max(target * 2.2, 3.0)

                    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", char_min)
                    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", char_max)
                    gmsh.option.setNumber("Mesh.MeshSizeMin", char_min)
                    gmsh.option.setNumber("Mesh.MeshSizeMax", char_max)
                    gmsh.option.setNumber("Mesh.Algorithm", 6)  # Frontal-Delaunay
                    gmsh.model.mesh.generate(2)
                    tris = list(_iter_gmsh_triangles(gmsh, max_tris=12000))
                    if tris:
                        preview_url = _render_triangles_png(tris)
                except Exception:
                    preview_url = None

        finally:
            gmsh.finalize()

        return StepExtractResult(
            volume_cm3=volume_cm3,
            surface_area_cm2=surface_area_cm2,
            bbox_x_mm=round(bbox_x_mm, 3),
            bbox_y_mm=round(bbox_y_mm, 3),
            bbox_z_mm=round(bbox_z_mm, 3),
            num_faces=int(num_faces),
            num_edges=int(num_edges),
            preview_image_url=preview_url,
            hole_count_est=int(hole_count_est),
            hole_diam_min_mm=(round(float(hole_dmin), 2) if hole_dmin is not None else None),
            hole_diam_max_mm=(round(float(hole_dmax), 2) if hole_dmax is not None else None),
            max_drilling_depth_est_mm=float(max_drill_est),
            feature_confidence=str(feat_conf),
        )
    finally:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass


def _estimate_holes_from_curves(
    gmsh_mod,
    *,
    min_diam_mm: float = 5.0,
    max_diam_mm: float = 12.0,
) -> tuple[int, float | None, float | None, str]:
    """Heuristic hole recognition.

    We look for OCC curves of type "Circle" whose bounding-box diameter falls
    inside the UI's displayed range (Ø5–12mm). Many CAD parts represent hole
    openings as circular edges; through-holes often produce two circular edges.

    Returns: (hole_count_est, hole_dmin_mm, hole_dmax_mm, confidence_label)
    """

    import math

    try:
        curves = gmsh_mod.model.getEntities(1)
    except Exception:
        return 0, None, None, "Low"

    unique: dict[tuple[float, float, float, float], float] = {}
    for dim, tag in curves:
        try:
            t = gmsh_mod.model.getType(dim, tag)
        except Exception:
            continue
        if not isinstance(t, str) or t.lower() != "circle":
            continue
        try:
            bxmin, bymin, bzmin, bxmax, bymax, bzmax = gmsh_mod.model.getBoundingBox(dim, tag)
            dx, dy, dz = float(bxmax - bxmin), float(bymax - bymin), float(bzmax - bzmin)
            diam = max(dx, dy, dz)
            if not (min_diam_mm - 1e-3 <= diam <= max_diam_mm + 1e-3):
                continue

            # Center of mass for a circle curve should be at its center
            cx, cy, cz = gmsh_mod.model.occ.getCenterOfMass(dim, tag)
            key = (round(float(cx), 1), round(float(cy), 1), round(float(cz), 1), round(float(diam), 1))
            unique[key] = float(diam)
        except Exception:
            continue

    edge_count = len(unique)
    if edge_count <= 0:
        return 0, None, None, "Low"

    # Through-holes often yield two circular edges. Use ceil to avoid undercounting.
    hole_count = int(math.ceil(edge_count / 2.0))

    ds = list(unique.values())
    dmin = min(ds) if ds else None
    dmax = max(ds) if ds else None

    # If the number of edges is even, we're a bit more confident.
    confidence = "Medium" if (edge_count % 2 == 0 and hole_count > 0) else "Low"
    return hole_count, dmin, dmax, confidence


def _estimate_max_drilling_depth(bx: float, by: float, bz: float) -> float:
    """Estimate a plausible drilling depth from part bounding box.

    Very rough: use ~60% of the smallest dimension, clamped.
    """
    dims = [d for d in (float(bx), float(by), float(bz)) if d and d > 1e-6]
    if not dims:
        return 0.0
    m = min(dims)
    return round(max(0.0, min(m * 0.6, m)), 1)


def _iter_gmsh_triangles(
    gmsh_mod,
    *,
    max_tris: int = 12000,
) -> Iterable[list[tuple[float, float, float]]]:
    """Yield surface mesh triangles (3 points) from gmsh.

    Important: Avoid pulling every node/triangle for large assemblies; we only
    need a bounded number of triangles for a preview image.
    """

    try:
        conn = gmsh_mod.model.mesh.getElementsByType(2)[1]
    except Exception:
        return

    total_tris = len(conn) // 3
    if total_tris <= 0:
        return

    stride = 1
    if total_tris > max_tris:
        stride = max(1, total_tris // max_tris)

    node_cache: dict[int, tuple[float, float, float]] = {}

    def get_pt(node_tag: int) -> tuple[float, float, float] | None:
        cached = node_cache.get(node_tag)
        if cached is not None:
            return cached
        try:
            ret = gmsh_mod.model.mesh.getNode(node_tag)
            xyz = ret[0]
            pt = (float(xyz[0]), float(xyz[1]), float(xyz[2]))
            node_cache[node_tag] = pt
            return pt
        except Exception:
            return None

    for tri_index in range(0, total_tris, stride):
        i = tri_index * 3
        n1 = int(conn[i])
        n2 = int(conn[i + 1])
        n3 = int(conn[i + 2])
        p1 = get_pt(n1)
        p2 = get_pt(n2)
        p3 = get_pt(n3)
        if p1 and p2 and p3:
            yield [p1, p2, p3]


def _render_triangles_png(triangles: list[list[tuple[float, float, float]]]) -> str:
    """Render triangles to a PNG data URL using matplotlib (Agg backend).

    Uses a simple projected 2D render (painter's algorithm) to stay fast and
    robust in headless environments.
    """

    # Avoid pathological sizes for huge assemblies.
    max_tris = 6000
    if len(triangles) > max_tris:
        stride = max(1, len(triangles) // max_tris)
        triangles = triangles[::stride]

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    # Rotation for an isometric-ish view
    elev = math.radians(18.0)
    azim = math.radians(38.0)
    ce, se = math.cos(elev), math.sin(elev)
    ca, sa = math.cos(azim), math.sin(azim)

    def rot(p: tuple[float, float, float]) -> tuple[float, float, float]:
        x, y, z = p
        # azimuth around Z
        x2 = ca * x - sa * y
        y2 = sa * x + ca * y
        z2 = z
        # elevation around X
        y3 = ce * y2 - se * z2
        z3 = se * y2 + ce * z2
        return (x2, y3, z3)

    # Center model
    xs = [p[0] for tri in triangles for p in tri]
    ys = [p[1] for tri in triangles for p in tri]
    zs = [p[2] for tri in triangles for p in tri]
    cx = (min(xs) + max(xs)) / 2.0 if xs else 0.0
    cy = (min(ys) + max(ys)) / 2.0 if ys else 0.0
    cz = (min(zs) + max(zs)) / 2.0 if zs else 0.0

    projected: list[tuple[float, list[tuple[float, float]]]] = []
    for tri in triangles:
        rp = [rot((p[0] - cx, p[1] - cy, p[2] - cz)) for p in tri]
        depth = (rp[0][2] + rp[1][2] + rp[2][2]) / 3.0
        poly2d = [(rp[0][0], rp[0][1]), (rp[1][0], rp[1][1]), (rp[2][0], rp[2][1])]
        projected.append((depth, poly2d))

    projected.sort(key=lambda t: t[0])
    polys = [p for _d, p in projected]

    fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=140)
    coll = PolyCollection(polys, linewidths=0.1, alpha=0.95)
    coll.set_facecolor((0.23, 0.51, 0.96, 0.85))
    coll.set_edgecolor((0.12, 0.18, 0.29, 0.10))
    ax.add_collection(coll)
    ax.autoscale_view()
    ax.set_aspect("equal", adjustable="box")
    ax.set_axis_off()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.02, transparent=True)
    plt.close(fig)

    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"
