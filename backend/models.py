from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class GeometryData(BaseModel):
    part_name: str | None = None
    volume_cm3: float = Field(..., ge=0, description="Part volume in cm^3")
    surface_area_cm2: float = Field(..., ge=0, description="Part surface area in cm^2")
    bbox_x_mm: float = Field(..., ge=0, description="Bounding box X in mm")
    bbox_y_mm: float = Field(..., ge=0, description="Bounding box Y in mm")
    bbox_z_mm: float = Field(..., ge=0, description="Bounding box Z in mm")
    aspect_ratio: float = Field(..., ge=0, description="max(bbox)/min(nonzero bbox)")
    num_faces: int = Field(..., ge=0, description="Topology faces count")
    num_edges: int = Field(..., ge=0, description="Topology edges count")


class UserInputs(BaseModel):
    num_holes: int = Field(0, ge=0)
    num_pockets: int = Field(0, ge=0)
    max_depth_mm: float = Field(0, ge=0)
    material: str
    quantity: int = Field(1, ge=1)
    tolerance_class: Literal["Standard", "Fine", "Ultra-Fine"] = "Standard"


class RoutingFlags(BaseModel):
    is_turning: int = Field(0, ge=0, le=1)
    is_milling: int = Field(0, ge=0, le=1)
    is_drilling: int = Field(0, ge=0, le=1)
    is_grinding: int = Field(0, ge=0, le=1)


class MachineSelection(BaseModel):
    turning: str | None = None
    milling: str | None = None
    drilling: str | None = None
    grinding: str | None = None


class OverrideInfo(BaseModel):
    engineer_override: bool = False
    override_note: str | None = None
    contradictions_acknowledged: bool = False


class RoutingDecisionLayer(BaseModel):
    routing_auto: RoutingFlags
    routing_final: RoutingFlags


class MachineAssignment(BaseModel):
    machine_selection_final: MachineSelection


class RoutingDecision(BaseModel):
    routing_decision: RoutingDecisionLayer
    machine_assignment: MachineAssignment
    overrides: OverrideInfo = Field(default_factory=OverrideInfo)


class StockEstimate(BaseModel):
    stock_shape: Literal["block", "cylinder"]
    stock_volume_cm3: float = Field(..., ge=0)
    stock_weight_kg: float = Field(..., ge=0)
    material: str


class CostBreakdown(BaseModel):
    material_cost_inr: float = Field(..., ge=0)
    machining_cost_inr: float = Field(..., ge=0)
    setup_cost_inr: float = Field(..., ge=0)
    overhead_cost_inr: float = Field(..., ge=0)
    total_cost_inr: float = Field(..., ge=0)


class ProcessDetail(BaseModel):
    process: Literal["Turning", "Milling", "Drilling", "Grinding"]
    machine: str
    time_min: float = Field(..., ge=0)
    rate_per_hr_inr: float = Field(..., ge=0)
    cost_inr: float = Field(..., ge=0)


class MachiningBreakdown(BaseModel):
    details: list[ProcessDetail]
    total_time_min: float = Field(..., ge=0)
    total_cost_inr: float = Field(..., ge=0)


class ConfidenceRange(BaseModel):
    low: float = Field(..., ge=0)
    nominal: float = Field(..., ge=0)
    high: float = Field(..., ge=0)
    risk_level: Literal["Low", "Medium", "High"]
    margin_pct: float = Field(..., ge=0)


class CostDriver(BaseModel):
    feature: str
    impact_value: float
    reason: str


class DFMSuggestion(BaseModel):
    suggestion_id: str
    change: str
    savings_inr: float
    reason: str
    icon: str | None = None
    variant_inputs: dict[str, Any] | None = None


class QuoteRequest(BaseModel):
    geometry: GeometryData
    inputs: UserInputs
    routing: RoutingDecision | None = None
    stock_override_kg: float | None = Field(default=None, ge=0)


class FullQuoteResponse(BaseModel):
    geometry: GeometryData
    inputs: UserInputs
    routing: RoutingDecision
    stock: StockEstimate
    cost: CostBreakdown
    confidence: ConfidenceRange
    machining_breakdown: MachiningBreakdown
    drivers: list[CostDriver]
    dfm_suggestions: list[DFMSuggestion]


class DFMComparison(BaseModel):
    quote_original: FullQuoteResponse
    quote_modified: FullQuoteResponse
    deltas: dict[str, Any] = Field(default_factory=dict)
    applied_suggestion_id: str | None = None
