# CAD-to-Quote Front-End Map

This document tracks all generated UI designs, their original folder names in the `ui` directory, and where they have been mapped in the FastAPI `.templates/` folder and what steps they correspond to.

| Original Design Folder (in `ui/stitch_landing_upload/`) | Target File Path (`frontend/templates/`) | Pipeline Step | Description & Key Line Numbers |
|---|---|---|---|
| `landing_upload_clean_layout` | `frontend/templates/index.html` | Step 0 | Initial Landing Screen and Upload Zone. **Interactions:** L57 (New Quote), L74 (Drop Zone), L82 (Browse), L93,103,113 (Samples) |
| `geometry_analysis_back_button_added` | `frontend/templates/geometry.html` | Steps 1-2 | CAD Validation & Geometry Extraction. **Interactions:** L41,234 (Back), L238 (Continue) |
| `smart_guided_setup_with_named_back_button` | `frontend/templates/input.html` | Step 3 | Smart Guided Setup. **Interactions:** L58,60 (Back), L98,116,134 (Confirm), L153-157 (Materials), L172-174 (Qty +/-), L188-190 (Tolerance), L282 (Generate Quote) |
| `process_routing_with_named_back_button` | `frontend/templates/routing.html` | Step 4 | Process Routing Toggles. **Interactions:** L41 (Back), L62-65 (Lean More Removed), L67 (Dynamic Warning), L100,125,150,175 (Switches), L183 (Confirm Routing) |
| `confirm_stock_material_selection_active` | `frontend/templates/stock.html` | Steps 5-6 | Stock Estimation. **Interactions:** L43 (Back), L110 (Material Dropdown/Diagram Sync), L170 (Confirm Stock) |
| `cad_to_quote_pipeline_progress` | `frontend/templates/progress.html` | Steps 7-12 | AI Engine pipeline animation. **Interactions:** L74-152 (Sequential 7-Step Animation), L155 (Auto-scroll) |
| `quote_dashboard_process_color_refinement` | `frontend/templates/dashboard.html` | Step 13 | Final Quote Results Dashboard. **Interactions:** L46 (New Quote), L50 (Export PDF), L296 (Badge Removed), L255,267,279,291 (DFM Simulate) |
| `symmetrical_dfm_comparison_view` | `frontend/templates/dfm.html` | Step 13 (DFM) | Side-by-side DFM simulation view. **Interactions:** L48 (Export PDF), L203 (Keep Original), L206 (Apply This Change) |
| `pdf_export_indian_localization` | `frontend/templates/export.html` | Step 13 (Export) | PDF Summary Export view. **Interactions:** L45 (Dashboard), L46 (Quotes), L78 (Print), L82 (Download PDF) |
