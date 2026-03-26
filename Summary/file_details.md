# File Details

Auto-generated per-file notes (purpose + key symbols where available).
Source: `Summary/_repo_scan.json`.

## /All/

### /All/Given/Abstract_Submission_Guidelines.pdf

- Purpose: Binary asset
- Type: binary.pdf

### /All/Given/Guidelines.md

- Purpose: Markdown document
- Type: text.md
- Lines: 5

### /All/Given/PS.md

- Purpose: **I**n**n**o**v**a**t**e **t**o**B**u**i**l**d** **t**h**e** **F**u**t**u**r**e
- Type: text.md
- Lines: 47

### /All/Given/Strategy.md

- Purpose: PS2 — CAD-to-Quote AI Agent: Full Strategy
- Type: text.md
- Lines: 1560

### /All/Given/abstract/ABSTRACT FINAL.md

- Purpose: Abstract
- Type: text.md
- Lines: 26

### /All/Given/abstract/Abstract.md

- Purpose: Abstract — PS2: CAD-to-Quote AI Agent
- Type: text.md
- Lines: 114

### /All/Given/round 2/2nd round rules.md

- Purpose: Markdown document
- Type: text.md
- Lines: 188

### /All/Given/round 2/ROUND2_BRIEF.md

- Purpose: Round 2 Brief
- Type: text.md
- Lines: 69

### /All/Given/round 2/ROUND2_PPT_OUTLINE.md

- Purpose: Round 2 Presentation Outline
- Type: text.md
- Lines: 124

### /All/Given/round 2/ROUND2_QA.md

- Purpose: Round 2 Q&A Preparation
- Type: text.md
- Lines: 63

### /All/PS2-CAD-to-Quote-AI-Agent.pdf

- Purpose: Binary asset
- Type: binary.pdf

### /All/Presentation_Round_Guidelines.pdf

- Purpose: Binary asset
- Type: binary.pdf

### /All/Steps/0.md

- Purpose: Step 0 - AI Agent Receives User Request
- Type: text.md
- Lines: 159

### /All/Steps/1.md

- Purpose: Step 1 — STEP CAD Upload
- Type: text.md
- Lines: 137

### /All/Steps/10.md

- Purpose: Step 10 — Cost Calculation
- Type: text.md
- Lines: 243

### /All/Steps/11.md

- Purpose: Step 11 - Explainability
- Type: text.md
- Lines: 137

### /All/Steps/12.md

- Purpose: Step 12 - DFM Suggestions
- Type: text.md
- Lines: 222

### /All/Steps/13.md

- Purpose: Step 13 - Final Output
- Type: text.md
- Lines: 236

### /All/Steps/2.md

- Purpose: Step 2 — Geometry Extraction (STEP)
- Type: text.md
- Lines: 171

### /All/Steps/3.md

- Purpose: Step 3 — Agent Inputs via Chat (Confirm + Fill Gaps)
- Type: text.md
- Lines: 145

### /All/Steps/4.md

- Purpose: Step 4 — Process Routing
- Type: text.md
- Lines: 138

### /All/Steps/5.md

- Purpose: Step 5 — Stock Estimation
- Type: text.md
- Lines: 137

### /All/Steps/6.md

- Purpose: Step 6 — User Stock Confirmation
- Type: text.md
- Lines: 120

### /All/Steps/7.md

- Purpose: Step 7 - Feature Vector Assembly
- Type: text.md
- Lines: 154

### /All/Steps/8.md

- Purpose: Step 8 — ML Prediction
- Type: text.md
- Lines: 112

### /All/Steps/9.md

- Purpose: Step 9 — Prediction Interval
- Type: text.md
- Lines: 135

### /All/The-Problem.pdf

- Purpose: Binary asset
- Type: binary.pdf

### /All/gamma_prompt.md

- Purpose: Gamma Prompt — CAD-to-Quote AI Agent (PIVOT Round 2)
- Type: text.md
- Lines: 363

### /All/gl/0.md

- Purpose: Step 0 - The Brain of the System (Grandma Version)
- Type: text.md
- Lines: 56

### /All/gl/1.md

- Purpose: Step 1 - Uploading the Design (Grandma Version)
- Type: text.md
- Lines: 51

### /All/gl/10.md

- Purpose: Step 10 - Adding Up All the Costs (Grandma Version)
- Type: text.md
- Lines: 107

### /All/gl/11.md

- Purpose: Step 11 - Explaining the Quote (Grandma Version)
- Type: text.md
- Lines: 82

### /All/gl/12.md

- Purpose: Step 12 - Design Improvement Suggestions (Grandma Version)
- Type: text.md
- Lines: 99

### /All/gl/13.md

- Purpose: Step 13 - The Final Quote (Grandma Version)
- Type: text.md
- Lines: 120

### /All/gl/2.md

- Purpose: Step 2 - Measuring the Shape (Grandma Version)
- Type: text.md
- Lines: 55

### /All/gl/3.md

- Purpose: Step 3 - Asking the Engineer (Grandma Version)
- Type: text.md
- Lines: 53

### /All/gl/4.md

- Purpose: Step 4 - Deciding the Processes (and Choosing Machines) (Grandma Version)
- Type: text.md
- Lines: 82

### /All/gl/5.md

- Purpose: Step 5 - Figuring Out the Raw Material Needed (Grandma Version)
- Type: text.md
- Lines: 71

### /All/gl/6.md

- Purpose: Step 6 - Confirming the Material Weight (Grandma Version)
- Type: text.md
- Lines: 56

### /All/gl/7.md

- Purpose: Step 7 - Putting All the Puzzle Pieces Together (Grandma Version)
- Type: text.md
- Lines: 59

### /All/gl/8.md

- Purpose: Step 8 - The AI Makes Its Prediction (Grandma Version)
- Type: text.md
- Lines: 51

### /All/gl/9.md

- Purpose: Step 9 - How Confident is the AI? (Grandma Version)
- Type: text.md
- Lines: 54

## /Final.py/

### /Final.py

- Purpose: Python module
- Type: text.py
- Lines: 434
- Top-level symbols:
- ClassDef: QuoteInput (lines 91-110)
- ClassDef: QuoteResult (lines 114-129)
- FunctionDef: route_processes (lines 132-142)
- FunctionDef: estimate_cost (lines 145-193)
- FunctionDef: estimate_confidence (lines 196-220)
- FunctionDef: build_cost_drivers (lines 223-241)
- FunctionDef: build_dfm_suggestions (lines 244-269)
- FunctionDef: prompt_float (lines 272-274)
- FunctionDef: prompt_int (lines 277-279)
- FunctionDef: prompt_choice (lines 282-288)
- FunctionDef: collect_interactive_input (lines 291-323)
- FunctionDef: format_currency (lines 326-327)
- FunctionDef: build_cost_contribution (lines 330-342)
- FunctionDef: print_quote (lines 345-386)
- FunctionDef: build_part_from_sample (lines 389-405)
- FunctionDef: parse_args (lines 408-412)
- FunctionDef: main (lines 415-430)

## /Summary/

### /Summary/_repo_scan.json

- Purpose: JSON data/config
- Type: text.json
- Lines: 1357

### /Summary/api_summary.md

- Purpose: API Summary
- Type: text.md
- Lines: 183

### /Summary/backend_summary.md

- Purpose: Backend Summary
- Type: text.md
- Lines: 198

### /Summary/docs_summary.md

- Purpose: Docs Summary (Hackathon Materials)
- Type: text.md
- Lines: 64

### /Summary/file_details.md

- Purpose: File Details
- Type: text.md
- Lines: 782

### /Summary/file_index.md

- Purpose: File Index
- Type: text.md
- Lines: 158

### /Summary/findings.md

- Purpose: Findings / Issues
- Type: text.md
- Lines: 55

### /Summary/frontend_summary.md

- Purpose: Frontend Summary
- Type: text.md
- Lines: 112

### /Summary/ml_data_summary.md

- Purpose: ML + Data Summary
- Type: text.md
- Lines: 90

### /Summary/system_overview.md

- Purpose: System Overview
- Type: text.md
- Lines: 74

## /backend/

### /backend/__init__.py

- Purpose: Python module
- Type: text.py
- Lines: 1

### /backend/confidence.py

- Purpose: Prediction interval / risk estimation -- Step 9. Uses the RandomForest's individual tree predictions to compute percentile-based confidence intervals. Falls back to heuristic margins if the model is not available.
- Type: text.py
- Lines: 168
- Top-level symbols:
- FunctionDef: _ensure_model_loaded (lines 22-42)
- FunctionDef: _tree_based_confidence (lines 45-106)
- FunctionDef: _heuristic_confidence (lines 109-153)
- FunctionDef: estimate_confidence (lines 156-168)

### /backend/cost.py

- Purpose: Python module
- Type: text.py
- Lines: 177
- Top-level symbols:
- FunctionDef: get_batch_discount (lines 69-73)
- FunctionDef: calc_material_cost (lines 76-79)
- FunctionDef: allocate_time (lines 82-96)
- FunctionDef: calc_machining_cost (lines 99-138)
- FunctionDef: calc_setup_cost (lines 141-142)
- FunctionDef: calc_overhead_cost (lines 145-148)
- FunctionDef: calculate_full_cost (lines 155-177)

### /backend/dfm.py

- Purpose: DFM suggestion engine — Step 12. Generates design-for-manufacturing suggestion *candidates* (variant_inputs + text). Savings are computed server-side by simulating each variant through the actual pipeline (routing → stock → time → cost) to keep numbers consistent with `/api/dfm/simulate`.
- Type: text.py
- Lines: 98
- Top-level symbols:
- FunctionDef: generate_dfm_suggestions (lines 26-98)

### /backend/explainability.py

- Purpose: Cost drivers — Step 11 (Explainability). Ranks cost components by impact and returns human-readable reasons. TODO: Add SHAP TreeExplainer waterfall when ML model is ready.
- Type: text.py
- Lines: 64
- Top-level symbols:
- FunctionDef: build_cost_drivers (lines 12-64)

### /backend/main.py

- Purpose: Python module
- Type: text.py
- Lines: 411
- Top-level symbols:
- FunctionDef: _simulate_total_cost_inr (lines 42-66)
- AsyncFunctionDef: landing (lines 94-95)
- AsyncFunctionDef: geometry (lines 99-100)
- AsyncFunctionDef: input_setup (lines 104-105)
- AsyncFunctionDef: process_routing (lines 109-110)
- AsyncFunctionDef: stock_estimation (lines 114-115)
- AsyncFunctionDef: progress_overlay (lines 119-120)
- AsyncFunctionDef: quote_dashboard (lines 124-125)
- AsyncFunctionDef: dfm_comparison (lines 129-130)
- AsyncFunctionDef: export_pdf (lines 134-135)
- AsyncFunctionDef: list_samples (lines 143-145)
- AsyncFunctionDef: get_sample_part (lines 149-155)
- AsyncFunctionDef: api_routing (lines 159-168)
- AsyncFunctionDef: api_stock (lines 172-183)
- AsyncFunctionDef: api_quote (lines 187-272)
- AsyncFunctionDef: api_dfm_simulate (lines 276-365)
- AsyncFunctionDef: api_step_extract (lines 369-407)

### /backend/ml_engine.py

- Purpose: Python module
- Type: text.py
- Lines: 190
- Top-level symbols:
- FunctionDef: _ensure_loaded (lines 46-71)
- FunctionDef: _build_feature_vector (lines 74-101)
- FunctionDef: _formula_fallback (lines 105-115)
- FunctionDef: predict_machining_time (lines 122-137)
- FunctionDef: get_shap_drivers (lines 140-190)

### /backend/ml_placeholder.py

- Purpose: ML placeholder — formula-based machining time estimation. TODO: Replace with trained RandomForest model via joblib.load(). Currently uses deterministic formulas ported from Final.py to simulate ML output.
- Type: text.py
- Lines: 70
- Top-level symbols:
- FunctionDef: predict_machining_time (lines 29-70)

### /backend/models.py

- Purpose: Python module
- Type: text.py
- Lines: 139
- Top-level symbols:
- ClassDef: GeometryData (lines 8-17)
- ClassDef: UserInputs (lines 20-26)
- ClassDef: RoutingFlags (lines 29-33)
- ClassDef: MachineSelection (lines 36-40)
- ClassDef: OverrideInfo (lines 43-46)
- ClassDef: RoutingDecisionLayer (lines 49-51)
- ClassDef: MachineAssignment (lines 54-55)
- ClassDef: RoutingDecision (lines 58-61)
- ClassDef: StockEstimate (lines 64-68)
- ClassDef: CostBreakdown (lines 71-76)
- ClassDef: ProcessDetail (lines 79-84)
- ClassDef: MachiningBreakdown (lines 87-90)
- ClassDef: ConfidenceRange (lines 93-98)
- ClassDef: CostDriver (lines 101-104)
- ClassDef: DFMSuggestion (lines 107-113)
- ClassDef: QuoteRequest (lines 116-120)
- ClassDef: FullQuoteResponse (lines 123-132)
- ClassDef: DFMComparison (lines 135-139)

### /backend/models_ml/feature_columns.json

- Purpose: JSON data/config
- Type: text.json
- Lines: 17

### /backend/models_ml/rf_machining_model.joblib

- Purpose: Binary asset
- Type: binary.joblib

### /backend/models_ml/shap_explainer.joblib

- Purpose: Binary asset
- Type: binary.joblib

### /backend/routing.py

- Purpose: Process routing engine — Step 4. Determines which machining processes are needed based on geometry + user inputs. Entirely rule-based — no ML involved.
- Type: text.py
- Lines: 103
- Top-level symbols:
- FunctionDef: compute_routing_flags (lines 38-45)
- FunctionDef: build_default_machine_selection (lines 48-55)
- FunctionDef: route_processes (lines 58-72)
- FunctionDef: get_routing_reason (lines 75-103)

### /backend/sample_parts.py

- Purpose: Python module
- Type: text.py
- Lines: 76
- Top-level symbols:
- FunctionDef: get_sample (lines 72-76)

### /backend/smoke_step_extract.py

- Purpose: Python module
- Type: text.py
- Lines: 69
- Top-level symbols:
- FunctionDef: _make_box_step (lines 15-27)
- FunctionDef: main (lines 30-65)

### /backend/step_extract.py

- Purpose: Python module
- Type: text.py
- Lines: 293
- Top-level symbols:
- ClassDef: StepExtractResult (lines 33-41)
- FunctionDef: _safe_float (lines 44-47)
- FunctionDef: extract_step_geometry (lines 50-171)
- FunctionDef: _iter_gmsh_triangles (lines 174-222)
- FunctionDef: _render_triangles_png (lines 225-293)

### /backend/stock.py

- Purpose: Stock estimation — Steps 5-6. Estimates raw material stock (cylindrical bar or rectangular block) based on geometry + routing flags + material.
- Type: text.py
- Lines: 86
- Top-level symbols:
- FunctionDef: cylindrical_stock_volume (lines 28-35)
- FunctionDef: block_stock_volume (lines 38-42)
- FunctionDef: estimate_stock_weight (lines 45-49)
- FunctionDef: estimate_stock (lines 52-86)

## /data/

### /data/training_data.csv

- Purpose: CSV dataset
- Type: text.csv
- Lines: 2993
- Note: content truncated in scan (large file).

## /frontend/

### /frontend/templates/dashboard.html

- Purpose: Manufacturing Quote Dashboard
- Type: text.html
- Lines: 532

### /frontend/templates/dfm.html

- Purpose: DFM Comparison View
- Type: text.html
- Lines: 398

### /frontend/templates/export.html

- Purpose: Quote Summary Preview - QuoteAI
- Type: text.html
- Lines: 552

### /frontend/templates/geometry.html

- Purpose: CAD Analysis Pro - Validation
- Type: text.html
- Lines: 379

### /frontend/templates/index.html

- Purpose: QuoteAI - Industrial CAD-to-Quote
- Type: text.html
- Lines: 368

### /frontend/templates/input.html

- Purpose: Smart Guided Setup Form - Manufacturing OS
- Type: text.html
- Lines: 427

### /frontend/templates/progress.html

- Purpose: HTML template
- Type: text.html
- Lines: 219

### /frontend/templates/routing.html

- Purpose: Process Routing &amp; Machine Assignment
- Type: text.html
- Lines: 404

### /frontend/templates/stock.html

- Purpose: Stock Estimation &amp; Confirmation
- Type: text.html
- Lines: 389

## /implementation_plan.md.resolved/

### /implementation_plan.md.resolved

- Purpose: Resolved spec/notes
- Type: text.resolved
- Lines: 356

## /openapi_tmp.json/

### /openapi_tmp.json

- Purpose: JSON data/config
- Type: text.json
- Lines: 1

## /plan.md/

### /plan.md

- Purpose: CAD-to-Quote AI Agent — Overall Strategy
- Type: text.md
- Lines: 336

## /scripts/

### /scripts/generate_dataset.py

- Purpose: Python module
- Type: text.py
- Lines: 137
- Top-level symbols:
- FunctionDef: _formula_time (lines 31-57)
- FunctionDef: generate (lines 60-123)

### /scripts/train_model.py

- Purpose: Train a RandomForest regressor on the synthetic machining-time dataset. Outputs: backend/models_ml/rf_machining_model.joblib — trained model backend/models_ml/shap_explainer.joblib — SHAP TreeExplainer backend/models_ml/feature_columns.json — ordered feature list Usage: python scripts/train_model.py
- Type: text.py
- Lines: 133
- Top-level symbols:
- FunctionDef: main (lines 50-129)

## /task.md.resolved/

### /task.md.resolved

- Purpose: Resolved spec/notes
- Type: text.resolved
- Lines: 56

## /tmp/

### /tmp/analyze_wl_range.py

- Purpose: Analyze water level ranges and find the 12 orphan nodes.
- Type: text.py
- Lines: 85

### /tmp/audit_backend.py

- Purpose: Comprehensive backend audit -- tests all modules, ML consistency, edge cases.
- Type: text.py
- Lines: 224
- Top-level symbols:
- FunctionDef: check (lines 9-13)

### /tmp/check_dfm_simulate.py

- Purpose: Python module
- Type: text.py
- Lines: 31
- Top-level symbols:
- AsyncFunctionDef: _run (lines 12-27)

### /tmp/gen_file_details.py

- Purpose: Python module
- Type: text.py
- Lines: 115

### /tmp/scan_repo.py

- Purpose: Python module
- Type: text.py
- Lines: 104

## /ui/

### /ui/stitch_landing_upload/cad_to_quote_pipeline_progress/code.html

- Purpose: HTML template
- Type: text.html
- Lines: 193

### /ui/stitch_landing_upload/cad_to_quote_pipeline_progress/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/confirm_stock_material_selection_active/code.html

- Purpose: Stock Estimation &amp; Confirmation
- Type: text.html
- Lines: 181

### /ui/stitch_landing_upload/confirm_stock_material_selection_active/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/geometry_analysis_back_button_added/code.html

- Purpose: CAD Analysis Pro - Validation
- Type: text.html
- Lines: 245

### /ui/stitch_landing_upload/geometry_analysis_back_button_added/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/landing_upload_clean_layout/code.html

- Purpose: QuoteAI - Industrial CAD-to-Quote
- Type: text.html
- Lines: 126

### /ui/stitch_landing_upload/landing_upload_clean_layout/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/pdf_export_indian_localization/code.html

- Purpose: Quote Summary Preview - QuoteAI
- Type: text.html
- Lines: 317

### /ui/stitch_landing_upload/pdf_export_indian_localization/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/process_routing_with_named_back_button/code.html

- Purpose: Process Routing &amp; Machine Assignment
- Type: text.html
- Lines: 194

### /ui/stitch_landing_upload/process_routing_with_named_back_button/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/quote_dashboard_process_color_refinement/code.html

- Purpose: Manufacturing Quote Dashboard
- Type: text.html
- Lines: 308

### /ui/stitch_landing_upload/quote_dashboard_process_color_refinement/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/smart_guided_setup_with_named_back_button/code.html

- Purpose: Smart Guided Setup Form - Manufacturing OS
- Type: text.html
- Lines: 291

### /ui/stitch_landing_upload/smart_guided_setup_with_named_back_button/screen.png

- Purpose: Binary asset
- Type: binary.png

### /ui/stitch_landing_upload/symmetrical_dfm_comparison_view/code.html

- Purpose: DFM Comparison View
- Type: text.html
- Lines: 214

### /ui/stitch_landing_upload/symmetrical_dfm_comparison_view/screen.png

- Purpose: Binary asset
- Type: binary.png

## /ui.md/

### /ui.md

- Purpose: CAD-to-Quote Front-End Map
- Type: text.md
- Lines: 15
