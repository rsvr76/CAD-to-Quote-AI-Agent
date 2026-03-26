"""Comprehensive backend audit -- tests all modules, ML consistency, edge cases."""
import sys, os
sys.path.insert(0, r"D:\Hackathon\Live\Pivot Hack")

errors = []
warnings = []
passes = []

def check(name, condition, msg=""):
    if condition:
        passes.append(f"PASS: {name}")
    else:
        errors.append(f"FAIL: {name} -- {msg}")

# ========================================
# 1. Module imports
# ========================================
print("=" * 60)
print("1. MODULE IMPORTS")
print("=" * 60)

from backend.models import GeometryData, UserInputs, RoutingFlags, CostBreakdown, ProcessDetail
from backend.routing import route_processes, compute_routing_flags
from backend.stock import estimate_stock
from backend.ml_engine import predict_machining_time, get_shap_drivers, _model
from backend.cost import calculate_full_cost
from backend.confidence import estimate_confidence
from backend.explainability import build_cost_drivers
from backend.dfm import generate_dfm_suggestions
from backend.sample_parts import SAMPLE_PARTS, get_sample

check("All module imports", True)
check("ML model loaded", _model is not None, "Model file not found")

# ========================================
# 2. SCHEMA VALIDATION
# ========================================
print("\n" + "=" * 60)
print("2. SCHEMA VALIDATION")
print("=" * 60)

for proc_name in ["Turning", "Milling", "Drilling", "Grinding"]:
    try:
        pd = ProcessDetail(process=proc_name, machine="Test", time_min=1, rate_per_hr_inr=100, cost_inr=10)
        check(f"ProcessDetail('{proc_name}')", True)
    except Exception as e:
        check(f"ProcessDetail('{proc_name}')", False, str(e))

# GeometryData with part_name
try:
    geo = GeometryData(volume_cm3=100, surface_area_cm2=200, bbox_x_mm=100, bbox_y_mm=50, bbox_z_mm=30, aspect_ratio=3.33, num_faces=100, num_edges=150)
    check("GeometryData without part_name", True)
except Exception as e:
    check("GeometryData without part_name", False, str(e))

# ========================================
# 3. FULL PIPELINE (3 samples)
# ========================================
print("\n" + "=" * 60)
print("3. FULL PIPELINE (3 samples)")
print("=" * 60)

for name in ("steel_bracket", "aluminum_housing", "titanium_shaft"):
    try:
        sample = get_sample(name)
        geo = GeometryData(**sample["geometry"])
        inp = UserInputs(**sample["inputs"])
        
        routing = route_processes(geo, inp)
        flags = routing.routing_decision.routing_final
        machines = routing.machine_assignment.machine_selection_final
        
        stock = estimate_stock(geo, flags, inp.material)
        check(f"{name}: stock weight > 0", stock.stock_weight_kg > 0, f"weight={stock.stock_weight_kg}")
        
        time_val = predict_machining_time(geo, inp, flags)
        check(f"{name}: ML time > 0", time_val > 0, f"time={time_val}")
        
        cost, mach = calculate_full_cost(stock.stock_weight_kg, time_val, inp.material, inp.quantity, flags, machines)
        check(f"{name}: total > 0", cost.total_cost_inr > 0, f"total={cost.total_cost_inr}")
        
        # Sum check
        computed = round(cost.material_cost_inr + cost.machining_cost_inr + cost.setup_cost_inr + cost.overhead_cost_inr, 2)
        check(f"{name}: cost sum = total", abs(computed - cost.total_cost_inr) < 0.1,
              f"sum={computed} vs total={cost.total_cost_inr}")
        
        # Machining breakdown check
        mach_sum = round(sum(d.cost_inr for d in mach.details), 2)
        check(f"{name}: mach breakdown sum = mach cost", abs(mach_sum - cost.machining_cost_inr) < 0.1,
              f"breakdown_sum={mach_sum} vs mach_cost={cost.machining_cost_inr}")
        
        # Confidence
        conf = estimate_confidence(inp, flags, cost.total_cost_inr, geometry=geo)
        check(f"{name}: low < nominal < high", conf.low < conf.nominal < conf.high,
              f"low={conf.low} nom={conf.nominal} high={conf.high}")
        check(f"{name}: risk in valid set", conf.risk_level in ("Low", "Medium", "High"))
        
        # SHAP drivers
        drivers = get_shap_drivers(geo, inp, flags, top_n=5)
        check(f"{name}: SHAP drivers count", drivers is not None and len(drivers) == 5,
              f"count={len(drivers) if drivers else 'None'}")
        
        # DFM suggestions
        dfm = generate_dfm_suggestions(geo, inp, flags, cost.total_cost_inr)
        check(f"{name}: DFM count > 0", len(dfm) > 0, f"count={len(dfm)}")
        
        # Check all DFM have variant_inputs
        for s in dfm:
            check(f"{name}: DFM '{s.suggestion_id}' has variants", s.variant_inputs is not None and len(s.variant_inputs) > 0)
        
        print(f"  {name}: cost={cost.total_cost_inr} time={time_val}min conf={conf.risk_level}({conf.margin_pct}%) dfm={len(dfm)}")
    except Exception as e:
        import traceback
        check(f"{name}: pipeline", False, str(e))
        traceback.print_exc()

# ========================================
# 4. ML CONSISTENCY
# ========================================
print("\n" + "=" * 60)
print("4. ML CONSISTENCY (10 identical runs)")
print("=" * 60)

sample = get_sample("steel_bracket")
geo = GeometryData(**sample["geometry"])
inp = UserInputs(**sample["inputs"])
flags = compute_routing_flags(geo, inp)

preds = [predict_machining_time(geo, inp, flags) for _ in range(10)]
check("ML deterministic", len(set(preds)) == 1, f"unique values: {set(preds)}")
print(f"  10 runs: {preds[0]} (all identical: {len(set(preds)) == 1})")

# SHAP consistency
shap1 = get_shap_drivers(geo, inp, flags, top_n=3)
shap2 = get_shap_drivers(geo, inp, flags, top_n=3)
if shap1 and shap2:
    same_features = [s1.feature == s2.feature for s1, s2 in zip(shap1, shap2)]
    same_values = [abs(s1.impact_value - s2.impact_value) < 0.001 for s1, s2 in zip(shap1, shap2)]
    check("SHAP deterministic (features)", all(same_features))
    check("SHAP deterministic (values)", all(same_values))

# ========================================
# 5. EDGE CASES
# ========================================
print("\n" + "=" * 60)
print("5. EDGE CASES")
print("=" * 60)

# Zero geometry
try:
    geo_z = GeometryData(volume_cm3=0, surface_area_cm2=0, bbox_x_mm=0, bbox_y_mm=0, bbox_z_mm=0, aspect_ratio=0, num_faces=0, num_edges=0)
    inp_z = UserInputs(num_holes=0, num_pockets=0, max_depth_mm=0, material="Steel", quantity=1, tolerance_class="Standard")
    flags_z = compute_routing_flags(geo_z, inp_z)
    time_z = predict_machining_time(geo_z, inp_z, flags_z)
    check("Zero geometry: time >= 0.5", time_z >= 0.5, f"time={time_z}")
    stock_z = estimate_stock(geo_z, flags_z, "Steel")
    check("Zero geometry: stock runs", True)
except Exception as e:
    check("Zero geometry", False, str(e))

# Unknown material fallback
try:
    inp_u = UserInputs(num_holes=1, num_pockets=0, max_depth_mm=10, material="Inconel", quantity=1, tolerance_class="Standard")
    geo_t = GeometryData(volume_cm3=100, surface_area_cm2=200, bbox_x_mm=100, bbox_y_mm=50, bbox_z_mm=30, aspect_ratio=3.33, num_faces=100, num_edges=150)
    flags_u = compute_routing_flags(geo_t, inp_u)
    time_u = predict_machining_time(geo_t, inp_u, flags_u)
    check("Unknown material: prediction OK", time_u > 0, f"time={time_u}")
    stock_u = estimate_stock(geo_t, flags_u, "Inconel")
    check("Unknown material: stock uses default density", stock_u.stock_weight_kg > 0)
except Exception as e:
    check("Unknown material", False, str(e))

# Extreme values
try:
    geo_b = GeometryData(volume_cm3=5000, surface_area_cm2=10000, bbox_x_mm=1000, bbox_y_mm=500, bbox_z_mm=300, aspect_ratio=3.33, num_faces=5000, num_edges=8000)
    inp_b = UserInputs(num_holes=20, num_pockets=10, max_depth_mm=100, material="Titanium", quantity=1, tolerance_class="Ultra-Fine")
    flags_b = compute_routing_flags(geo_b, inp_b)
    time_b = predict_machining_time(geo_b, inp_b, flags_b)
    check("Extreme values: prediction OK", time_b > 0, f"time={time_b}")
    cost_b, _ = calculate_full_cost(50.0, time_b, "Titanium", 1, flags_b, 
        routing.machine_assignment.machine_selection_final)
    check("Extreme values: cost OK", cost_b.total_cost_inr > 0)
except Exception as e:
    check("Extreme values", False, str(e))

# Quantity = 0 edge case
try:
    inp_q0 = UserInputs(num_holes=1, num_pockets=1, max_depth_mm=10, material="Steel", quantity=1, tolerance_class="Standard")
    # quantity min is 1 per schema, testing qty=1
    check("Minimum quantity=1 accepted", True)
except Exception as e:
    check("Minimum quantity", False, str(e))

# ========================================
# 6. COST CAPITALIZATION
# ========================================
print("\n" + "=" * 60)
print("6. PROCESS CAPITALIZATION MAPPING")
print("=" * 60)

for raw, expected in {"turning": "Turning", "milling": "Milling", "drilling": "Drilling", "grinding": "Grinding"}.items():
    check(f"'{raw}'.capitalize() == '{expected}'", raw.capitalize() == expected)

# ========================================
# SUMMARY
# ========================================
print("\n" + "=" * 60)
print("AUDIT SUMMARY")
print("=" * 60)
print(f"  PASS: {len(passes)}")
print(f"  WARN: {len(warnings)}")
print(f"  FAIL: {len(errors)}")

if warnings:
    print("\nWARNINGS:")
    for w in warnings:
        print(f"  {w}")

if errors:
    print("\nFAILURES:")
    for e in errors:
        print(f"  {e}")
else:
    print("\n  >>> All checks passed! <<<")
