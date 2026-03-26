"""QuoteAI Backend — FastAPI server with page routes + API endpoints."""

from __future__ import annotations

import os

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from .models import (
    DFMComparison,
    FullQuoteResponse,
    GeometryData,
    QuoteRequest,
    RoutingDecision,
    RoutingDecisionLayer,
    MachineAssignment,
    MachineSelection,
    OverrideInfo,
    RoutingFlags,
    StockEstimate,
    UserInputs,
)
from .sample_parts import get_sample, SAMPLE_PARTS
from .routing import route_processes, compute_routing_flags, build_default_machine_selection
from .stock import estimate_stock
from .ml_engine import predict_machining_time, get_shap_drivers
from .cost import calculate_full_cost
from .confidence import estimate_confidence
from .explainability import build_cost_drivers
from .dfm import generate_dfm_suggestions
from .step_extract import extract_step_geometry


app = FastAPI(title="QuoteAI - CAD-to-Quote")


def _simulate_total_cost_inr(
    geo: GeometryData,
    inp: UserInputs,
    routing_override: RoutingDecision | None = None,
    stock_override_kg: float | None = None,
) -> float:
    """Simulate routing→stock→time→cost and return total_cost_inr.

    Used to ensure DFM suggestion savings match the actual pipeline.
    """
    routing_decision = routing_override or route_processes(geo, inp)
    final_flags = routing_decision.routing_decision.routing_final
    machines = routing_decision.machine_assignment.machine_selection_final

    stock = estimate_stock(geo, final_flags, inp.material, stock_override_kg)
    machining_time = predict_machining_time(geo, inp, final_flags)
    cost_breakdown, _mach_breakdown = calculate_full_cost(
        stock_weight_kg=stock.stock_weight_kg,
        machining_time_min=machining_time,
        material=inp.material,
        quantity=inp.quantity,
        routing=final_flags,
        machines=machines,
    )
    return float(cost_breakdown.total_cost_inr)

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, "templates")
STATIC_DIR = os.path.join(FRONTEND_DIR, "static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Mount static files if directory exists
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ══════════════════════════════════════════
# PAGE ROUTES (GET — serve HTML templates)
# ══════════════════════════════════════════

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/geometry", response_class=HTMLResponse)
async def geometry(request: Request):
    return templates.TemplateResponse("geometry.html", {"request": request})


@app.get("/input", response_class=HTMLResponse)
async def input_setup(request: Request):
    return templates.TemplateResponse("input.html", {"request": request})


@app.get("/routing", response_class=HTMLResponse)
async def process_routing(request: Request):
    return templates.TemplateResponse("routing.html", {"request": request})


@app.get("/stock", response_class=HTMLResponse)
async def stock_estimation(request: Request):
    return templates.TemplateResponse("stock.html", {"request": request})


@app.get("/progress", response_class=HTMLResponse)
async def progress_overlay(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def quote_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/dfm", response_class=HTMLResponse)
async def dfm_comparison(request: Request):
    return templates.TemplateResponse("dfm.html", {"request": request})


@app.get("/export", response_class=HTMLResponse)
async def export_pdf(request: Request):
    return templates.TemplateResponse("export.html", {"request": request})


# ══════════════════════════════════════════
# API ROUTES (POST/GET — data processing)
# ══════════════════════════════════════════

@app.get("/api/samples")
async def list_samples():
    """List available sample part names."""
    return {"samples": list(SAMPLE_PARTS.keys())}


@app.get("/api/samples/{name}")
async def get_sample_part(name: str):
    """Load a pre-filled sample part (geometry + inputs)."""
    try:
        data = get_sample(name)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Sample '{name}' not found")
    return data


@app.post("/api/routing")
async def api_routing(request_data: dict):
    """Compute routing from geometry + inputs. Returns RoutingDecision."""
    try:
        geo = GeometryData(**request_data.get("geometry", {}))
        inp = UserInputs(**request_data.get("inputs", {}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    decision = route_processes(geo, inp)
    return decision.model_dump()


@app.post("/api/stock")
async def api_stock(request_data: dict):
    """Compute stock estimation from geometry + routing + material."""
    try:
        geo = GeometryData(**request_data.get("geometry", {}))
        flags = RoutingFlags(**request_data.get("routing_flags", {}))
        material = request_data.get("material", "Steel")
        stock_shape_override = request_data.get("stock_shape_override")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    stock = estimate_stock(geo, flags, material, stock_shape_override=stock_shape_override)
    return stock.model_dump()


@app.post("/api/quote")
async def api_quote(request_data: dict):
    """Full pipeline: routing → stock → ML → cost → confidence → explain → DFM."""
    try:
        geo = GeometryData(**request_data.get("geometry", {}))
        inp = UserInputs(**request_data.get("inputs", {}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 4: Routing
    routing_override = request_data.get("routing")
    if routing_override:
        routing_decision = RoutingDecision(**routing_override)
    else:
        routing_decision = route_processes(geo, inp)

    final_flags = routing_decision.routing_decision.routing_final
    machines = routing_decision.machine_assignment.machine_selection_final

    # Step 5-6: Stock
    stock_override = request_data.get("stock_override_kg")
    stock_shape_override = request_data.get("stock_shape_override")
    stock = estimate_stock(
        geo,
        final_flags,
        inp.material,
        stock_override,
        stock_shape_override=stock_shape_override,
    )

    # Step 8: ML Prediction (trained RandomForest)
    machining_time = predict_machining_time(geo, inp, final_flags)

    # Step 10: Cost
    cost_breakdown, mach_breakdown = calculate_full_cost(
        stock_weight_kg=stock.stock_weight_kg,
        machining_time_min=machining_time,
        material=inp.material,
        quantity=inp.quantity,
        routing=final_flags,
        machines=machines,
    )

    # Step 9: Confidence
    confidence = estimate_confidence(inp, final_flags, cost_breakdown.total_cost_inr, geometry=geo)

    # Step 11: Cost Drivers (SHAP-based if available, else heuristic)
    shap_drivers = get_shap_drivers(geo, inp, final_flags, top_n=5)
    if shap_drivers:
        drivers = shap_drivers
    else:
        drivers = build_cost_drivers(inp, cost_breakdown, mach_breakdown)

    # Step 12: DFM Suggestions
    dfm_candidates = generate_dfm_suggestions(geo, inp, final_flags, cost_breakdown.total_cost_inr)
    base_total = float(cost_breakdown.total_cost_inr)
    dfm_scored = []
    for s in dfm_candidates:
        variant = s.variant_inputs or {}
        if not variant:
            continue
        try:
            inp_variant_data = inp.model_dump()
            inp_variant_data.update(variant)
            inp_variant = UserInputs(**inp_variant_data)
            new_total = _simulate_total_cost_inr(geo, inp_variant)
            savings = round(max(base_total - float(new_total), 0.0), 2)
        except Exception:
            savings = 0.0
        dfm_scored.append(s.model_copy(update={"savings_inr": savings}))

    dfm_scored.sort(key=lambda x: x.savings_inr, reverse=True)
    dfm = dfm_scored[:4]

    # Step 13: Full response
    response = FullQuoteResponse(
        geometry=geo,
        inputs=inp,
        routing=routing_decision,
        stock=stock,
        cost=cost_breakdown,
        confidence=confidence,
        machining_breakdown=mach_breakdown,
        drivers=drivers,
        dfm_suggestions=dfm,
    )
    return response.model_dump()


@app.post("/api/dfm/simulate")
async def api_dfm_simulate(request_data: dict):
    """Re-run pipeline with a modified DFM suggestion applied."""
    try:
        suggestion_id = request_data.get("suggestion_id", "")
        original_quote = request_data.get("quote", {})

        # Get original inputs
        geo = GeometryData(**original_quote.get("geometry", {}))
        inp_data = dict(original_quote.get("inputs", {}))

        # Find the suggestion and apply its variant inputs
        suggestions = original_quote.get("dfm_suggestions", [])
        variant_inputs = None
        for s in suggestions:
            if s.get("suggestion_id") == suggestion_id:
                variant_inputs = s.get("variant_inputs", {})
                break

        if not variant_inputs:
            raise HTTPException(status_code=404, detail=f"Suggestion '{suggestion_id}' not found")

        # Apply modifications
        inp_data.update(variant_inputs)
        inp_modified = UserInputs(**inp_data)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Re-run full pipeline with modified inputs
    routing_decision = route_processes(geo, inp_modified)
    final_flags = routing_decision.routing_decision.routing_final
    machines = routing_decision.machine_assignment.machine_selection_final

    stock = estimate_stock(geo, final_flags, inp_modified.material)
    machining_time = predict_machining_time(geo, inp_modified, final_flags)
    cost_breakdown, mach_breakdown = calculate_full_cost(
        stock_weight_kg=stock.stock_weight_kg,
        machining_time_min=machining_time,
        material=inp_modified.material,
        quantity=inp_modified.quantity,
        routing=final_flags,
        machines=machines,
    )

    confidence = estimate_confidence(
        inp_modified,
        final_flags,
        cost_breakdown.total_cost_inr,
        geometry=geo,
    )

    shap_drivers = get_shap_drivers(geo, inp_modified, final_flags, top_n=5)
    if shap_drivers:
        drivers = shap_drivers
    else:
        drivers = build_cost_drivers(inp_modified, cost_breakdown, mach_breakdown)

    dfm = generate_dfm_suggestions(geo, inp_modified, final_flags, cost_breakdown.total_cost_inr)

    modified_quote = FullQuoteResponse(
        geometry=geo,
        inputs=inp_modified,
        routing=routing_decision,
        stock=stock,
        cost=cost_breakdown,
        confidence=confidence,
        machining_breakdown=mach_breakdown,
        drivers=drivers,
        dfm_suggestions=dfm,
    )

    # Build comparison + savings summary
    original_total = float(original_quote.get("cost", {}).get("total_cost_inr", 0) or 0)
    modified_total = float(cost_breakdown.total_cost_inr)
    savings = round(max(original_total - modified_total, 0.0), 2)
    savings_pct = round((savings / original_total * 100) if original_total > 0 else 0.0, 1)

    comparison = DFMComparison(
        quote_original=FullQuoteResponse(**original_quote),
        quote_modified=modified_quote,
        deltas=variant_inputs,
        applied_suggestion_id=suggestion_id,
    )

    result = comparison.model_dump()
    result["savings_inr"] = savings
    result["savings_pct"] = savings_pct
    return result


@app.post("/api/step/extract")
async def api_step_extract(file: UploadFile = File(...)):
    """Extract real geometry metrics from an uploaded STEP file."""

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty upload")

    filename = file.filename or "uploaded.step"
    part_name = filename
    if part_name.lower().endswith(".step"):
        part_name = part_name[:-5]
    elif part_name.lower().endswith(".stp"):
        part_name = part_name[:-4]

    try:
        res = extract_step_geometry(data)
    except Exception as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    dims = [float(res.bbox_x_mm), float(res.bbox_y_mm), float(res.bbox_z_mm)]
    nonzero = [d for d in dims if d > 1e-6]
    aspect = (max(dims) / min(nonzero)) if nonzero else 0.0

    geo = GeometryData(
        part_name=part_name,
        volume_cm3=res.volume_cm3,
        surface_area_cm2=res.surface_area_cm2,
        bbox_x_mm=res.bbox_x_mm,
        bbox_y_mm=res.bbox_y_mm,
        bbox_z_mm=res.bbox_z_mm,
        aspect_ratio=round(float(aspect), 4),
        num_faces=int(res.num_faces),
        num_edges=int(res.num_edges),
    )

    return {
        "geometry": geo.model_dump(),
        "preview_image_url": res.preview_image_url,
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=5000, reload=True)
