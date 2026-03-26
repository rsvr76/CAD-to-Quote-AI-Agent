"""Backup round-2 demo for PS2: CAD-to-Quote AI Agent.

This is a dependency-free CLI prototype intended for presentation backup.
It demonstrates the core logic expected by the problem statement:

- guided input collection
- process routing
- transparent cost breakdown
- confidence range
- cost-driver explanation
- DFM suggestions
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, List, Tuple


MATERIAL_RATES = {
	"Aluminum": 7.0,
	"Steel": 10.0,
	"Titanium": 35.0,
	"Brass": 12.0,
}

MACHINABILITY = {
	"Aluminum": 1.0,
	"Steel": 1.8,
	"Titanium": 5.0,
	"Brass": 1.2,
}

TOLERANCE_MULTIPLIER = {
	"Standard": 1.0,
	"High": 1.25,
	"Ultra-High": 1.6,
}

SAMPLE_PARTS = {
	"steel_bracket": {
		"part_name": "Steel Bracket",
		"volume": 120.0,
		"surface_area": 210.0,
		"length": 160.0,
		"width": 45.0,
		"height": 35.0,
		"face_count": 842,
		"num_holes": 6,
		"avg_hole_depth": 25.0,
		"num_pockets": 2,
		"material": "Steel",
		"quantity": 5,
		"tolerance": "High",
	},
	"aluminum_housing": {
		"part_name": "Aluminum Housing",
		"volume": 180.0,
		"surface_area": 300.0,
		"length": 120.0,
		"width": 110.0,
		"height": 70.0,
		"face_count": 1190,
		"num_holes": 4,
		"avg_hole_depth": 12.0,
		"num_pockets": 3,
		"material": "Aluminum",
		"quantity": 20,
		"tolerance": "Standard",
	},
	"titanium_shaft": {
		"part_name": "Titanium Shaft",
		"volume": 95.0,
		"surface_area": 175.0,
		"length": 280.0,
		"width": 32.0,
		"height": 30.0,
		"face_count": 520,
		"num_holes": 1,
		"avg_hole_depth": 18.0,
		"num_pockets": 0,
		"material": "Titanium",
		"quantity": 2,
		"tolerance": "Ultra-High",
	},
}


@dataclass
class QuoteInput:
	part_name: str
	volume: float
	surface_area: float
	length: float
	width: float
	height: float
	face_count: int
	num_holes: int
	avg_hole_depth: float
	num_pockets: int
	material: str
	quantity: int
	tolerance: str

	@property
	def aspect_ratio(self) -> float:
		dimensions = sorted([self.length, self.width, self.height], reverse=True)
		smallest = max(dimensions[-1], 1.0)
		return dimensions[0] / smallest


@dataclass
class QuoteResult:
	processes: List[str]
	material_cost: float
	drill_cost: float
	mill_cost: float
	turn_cost: float
	grind_cost: float
	setup_cost: float
	overhead_cost: float
	total_cost: float
	confidence: int
	low_range: float
	high_range: float
	risk: str
	cost_drivers: List[Tuple[str, float, str]]
	dfm_suggestions: List[Tuple[str, float, str]]


def route_processes(part: QuoteInput) -> List[str]:
	processes: List[str] = []
	if part.aspect_ratio > 3.0:
		processes.append("Turning")
	if part.num_pockets > 0:
		processes.append("Milling")
	if part.num_holes > 0:
		processes.append("Drilling")
	if part.tolerance in {"High", "Ultra-High"}:
		processes.append("Grinding")
	return processes


def estimate_cost(part: QuoteInput) -> QuoteResult:
	processes = route_processes(part)
	machinability = MACHINABILITY[part.material]
	tolerance_factor = TOLERANCE_MULTIPLIER[part.tolerance]

	batch_factor = max(0.70, 1 - 0.03 * part.quantity)
	material_cost = part.volume * MATERIAL_RATES[part.material] * batch_factor

	drill_cost = 0.0
	if "Drilling" in processes:
		drill_cost = part.num_holes * 24.0 * (max(part.avg_hole_depth, 1.0) ** 1.12) * machinability

	mill_cost = 0.0
	if "Milling" in processes:
		mill_cost = part.num_pockets * 150.0 * (part.surface_area / 100.0) * machinability

	turn_cost = 0.0
	if "Turning" in processes:
		turn_cost = 5.0 * part.volume * machinability * min(part.aspect_ratio / 3.0, 2.2)

	grind_cost = 0.0
	if "Grinding" in processes:
		grind_cost = 1.4 * part.surface_area * (tolerance_factor - 0.85)

	setup_cost = (260.0 + len(processes) * 90.0) / max(part.quantity, 1)
	overhead_cost = 0.12 * (material_cost + drill_cost + mill_cost + turn_cost + grind_cost)
	total_cost = material_cost + drill_cost + mill_cost + turn_cost + grind_cost + setup_cost + overhead_cost

	confidence, low_range, high_range, risk = estimate_confidence(part, total_cost, processes)
	cost_drivers = build_cost_drivers(part, drill_cost, mill_cost, turn_cost, grind_cost, material_cost)
	dfm_suggestions = build_dfm_suggestions(part, total_cost)

	return QuoteResult(
		processes=processes,
		material_cost=material_cost,
		drill_cost=drill_cost,
		mill_cost=mill_cost,
		turn_cost=turn_cost,
		grind_cost=grind_cost,
		setup_cost=setup_cost,
		overhead_cost=overhead_cost,
		total_cost=total_cost,
		confidence=confidence,
		low_range=low_range,
		high_range=high_range,
		risk=risk,
		cost_drivers=cost_drivers,
		dfm_suggestions=dfm_suggestions,
	)


def estimate_confidence(part: QuoteInput, total_cost: float, processes: List[str]) -> Tuple[int, float, float, str]:
	uncertainty = 0.08
	if part.material == "Titanium":
		uncertainty += 0.05
	if part.tolerance == "Ultra-High":
		uncertainty += 0.05
	if part.quantity == 1:
		uncertainty += 0.03
	if part.num_holes >= 6:
		uncertainty += 0.03
	if len(processes) >= 3:
		uncertainty += 0.03

	confidence = max(55, min(92, int((1 - uncertainty) * 100)))
	low_range = total_cost * (1 - uncertainty)
	high_range = total_cost * (1 + uncertainty)

	if confidence >= 85:
		risk = "Low Risk"
	elif confidence >= 70:
		risk = "Medium Risk"
	else:
		risk = "High Risk"

	return confidence, low_range, high_range, risk


def build_cost_drivers(
	part: QuoteInput,
	drill_cost: float,
	mill_cost: float,
	turn_cost: float,
	grind_cost: float,
	material_cost: float,
) -> List[Tuple[str, float, str]]:
	drivers: List[Tuple[str, float, str]] = []
	if drill_cost > 0:
		drivers.append((f"{part.num_holes} holes at {part.avg_hole_depth:.0f} mm depth", drill_cost, "Drilling time rises with hole count and depth."))
	if mill_cost > 0:
		drivers.append((f"{part.num_pockets} pocket features", mill_cost, "Pocket machining adds milling passes and toolpath complexity."))
	if turn_cost > 0:
		drivers.append((f"Aspect ratio {part.aspect_ratio:.1f}:1", turn_cost, "Longer cylindrical geometry increases turning effort."))
	if grind_cost > 0:
		drivers.append((f"{part.tolerance} tolerance requirement", grind_cost, "Tighter tolerance adds finishing effort."))
	drivers.append((f"{part.material} raw material", material_cost, "Material choice affects both raw cost and machinability."))
	return sorted(drivers, key=lambda item: item[1], reverse=True)[:4]


def build_dfm_suggestions(part: QuoteInput, total_cost: float) -> List[Tuple[str, float, str]]:
	suggestions: List[Tuple[str, float, str]] = []

	if part.num_holes > 4:
		reduced_holes = part.num_holes - 2
		savings = 2 * 24.0 * (max(part.avg_hole_depth, 1.0) ** 1.12) * MACHINABILITY[part.material]
		suggestions.append((f"Reduce holes from {part.num_holes} to {reduced_holes}", savings, "Fewer holes reduce drilling cycle time and tool changes."))

	if part.num_pockets > 1:
		savings = 150.0 * (part.surface_area / 100.0) * MACHINABILITY[part.material]
		suggestions.append((f"Simplify pockets from {part.num_pockets} to {part.num_pockets - 1}", savings, "Reducing pockets cuts milling passes."))

	if part.material in {"Steel", "Titanium"}:
		alt_material = "Aluminum"
		alt_cost = total_cost * (MACHINABILITY[alt_material] / MACHINABILITY[part.material]) * 0.82
		suggestions.append((f"Switch material from {part.material} to {alt_material} if function allows", max(total_cost - alt_cost, 0.0), "Softer materials reduce both raw material and machining cost."))

	if part.tolerance in {"High", "Ultra-High"}:
		next_tol = "Standard" if part.tolerance == "High" else "High"
		savings = 1.4 * part.surface_area * (TOLERANCE_MULTIPLIER[part.tolerance] - TOLERANCE_MULTIPLIER[next_tol])
		suggestions.append((f"Relax tolerance from {part.tolerance} to {next_tol}", max(savings, 0.0), "Relaxed tolerance can remove or reduce grinding effort."))

	if part.quantity == 1:
		suggestions.append(("Increase order quantity from 1 to 5", 220.0, "Setup cost is amortized across multiple units."))

	return sorted(suggestions, key=lambda item: item[1], reverse=True)[:4]


def prompt_float(label: str, default: float) -> float:
	raw = input(f"{label} [{default}]: ").strip()
	return float(raw) if raw else default


def prompt_int(label: str, default: int) -> int:
	raw = input(f"{label} [{default}]: ").strip()
	return int(raw) if raw else default


def prompt_choice(label: str, options: List[str], default: str) -> str:
	option_text = "/".join(options)
	raw = input(f"{label} ({option_text}) [{default}]: ").strip()
	value = raw or default
	if value not in options:
		raise ValueError(f"Invalid value for {label}: {value}")
	return value


def collect_interactive_input() -> QuoteInput:
	print("QuoteAI Backup Demo")
	print("Enter part information. Press Enter to accept the sample default.")

	part_name = input("Part name [Demo Part]: ").strip() or "Demo Part"
	volume = prompt_float("Volume in cm^3", 120.0)
	surface_area = prompt_float("Surface area in cm^2", 210.0)
	length = prompt_float("Length in mm", 160.0)
	width = prompt_float("Width in mm", 45.0)
	height = prompt_float("Height in mm", 35.0)
	face_count = prompt_int("Face count", 842)
	num_holes = prompt_int("Number of holes", 6)
	avg_hole_depth = prompt_float("Average hole depth in mm", 25.0)
	num_pockets = prompt_int("Number of pockets", 2)
	material = prompt_choice("Material", list(MATERIAL_RATES.keys()), "Steel")
	quantity = prompt_int("Quantity", 5)
	tolerance = prompt_choice("Tolerance", list(TOLERANCE_MULTIPLIER.keys()), "High")

	return QuoteInput(
		part_name=part_name,
		volume=volume,
		surface_area=surface_area,
		length=length,
		width=width,
		height=height,
		face_count=face_count,
		num_holes=num_holes,
		avg_hole_depth=avg_hole_depth,
		num_pockets=num_pockets,
		material=material,
		quantity=quantity,
		tolerance=tolerance,
	)


def format_currency(value: float) -> str:
	return f"₹{value:,.0f}"


def build_cost_contribution(result: QuoteResult) -> List[Tuple[str, float, float]]:
	"""Return [(component, cost, percent_of_total), ...] for the main 4 buckets."""
	machining_total = result.drill_cost + result.mill_cost + result.turn_cost + result.grind_cost
	components = [
		("Material", result.material_cost),
		("Machining", machining_total),
		("Setup", result.setup_cost),
		("Overhead", result.overhead_cost),
	]
	denom = result.total_cost if result.total_cost > 0 else sum(cost for _, cost, in components)
	if denom <= 0:
		return [(name, cost, 0.0) for name, cost in components]
	return [(name, cost, (cost / denom) * 100.0) for name, cost in components]


def print_quote(part: QuoteInput, result: QuoteResult) -> None:
	print("\n" + "=" * 68)
	print(f"Quote Summary: {part.part_name}")
	print("=" * 68)
	print(f"Geometry: volume={part.volume:.1f} cm^3 | area={part.surface_area:.1f} cm^2 | aspect ratio={part.aspect_ratio:.1f}:1 | faces={part.face_count}")
	print(f"Inputs: material={part.material} | quantity={part.quantity} | tolerance={part.tolerance} | holes={part.num_holes} | pockets={part.num_pockets}")
	print(f"Processes identified: {', '.join(result.processes) if result.processes else 'None'}")

	print("\nTransparent cost breakdown")
	print(f"  Material  : {format_currency(result.material_cost)}")
	print(f"  Drilling  : {format_currency(result.drill_cost)}")
	print(f"  Milling   : {format_currency(result.mill_cost)}")
	print(f"  Turning   : {format_currency(result.turn_cost)}")
	print(f"  Grinding  : {format_currency(result.grind_cost)}")
	print(f"  Setup     : {format_currency(result.setup_cost)}")
	print(f"  Overhead  : {format_currency(result.overhead_cost)}")
	print(f"  Total     : {format_currency(result.total_cost)}")

	print("\nCost contribution (share of total)")
	contribution = build_cost_contribution(result)
	for name, cost, pct in contribution:
		print(f"  {name:<9}: {format_currency(cost)}  ({pct:>5.1f}%)")
	if contribution:
		largest = max(contribution, key=lambda item: item[1])
		print(f"  Largest cost driver: {largest[0]} ({largest[2]:.1f}%)")

	print("\nConfidence")
	print(f"  Estimated range: {format_currency(result.low_range)} to {format_currency(result.high_range)}")
	print(f"  Confidence : {result.confidence}% ({result.risk})")

	print("\nTop cost drivers")
	for title, value, reason in result.cost_drivers:
		print(f"  - {title}: {format_currency(value)}")
		print(f"    Reason: {reason}")

	print("\nDFM suggestions")
	if result.dfm_suggestions:
		for change, savings, reason in result.dfm_suggestions:
			print(f"  - {change}: save about {format_currency(savings)}")
			print(f"    Reason: {reason}")
	else:
		print("  - No high-impact suggestions for this input set.")


def build_part_from_sample(sample_name: str) -> QuoteInput:
	sample = SAMPLE_PARTS[sample_name]
	return QuoteInput(
		part_name=sample["part_name"],
		volume=sample["volume"],
		surface_area=sample["surface_area"],
		length=sample["length"],
		width=sample["width"],
		height=sample["height"],
		face_count=sample["face_count"],
		num_holes=sample["num_holes"],
		avg_hole_depth=sample["avg_hole_depth"],
		num_pockets=sample["num_pockets"],
		material=sample["material"],
		quantity=sample["quantity"],
		tolerance=sample["tolerance"],
	)


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(description="Backup PS2 quote demo")
	parser.add_argument("--sample", choices=sorted(SAMPLE_PARTS.keys()), help="Run a built-in sample part")
	parser.add_argument("--list-samples", action="store_true", help="List available sample parts")
	return parser.parse_args()


def main() -> None:
	args = parse_args()

	if args.list_samples:
		print("Available samples:")
		for name in sorted(SAMPLE_PARTS):
			print(f"  - {name}")
		return

	if args.sample:
		part = build_part_from_sample(args.sample)
	else:
		part = collect_interactive_input()

	result = estimate_cost(part)
	print_quote(part, result)


if __name__ == "__main__":
	main()
