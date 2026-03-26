# PS2 — CAD-to-Quote AI Agent: Full Strategy

## Event Context

- **Event:** PIVOT Innovation Challenge (SRCAS × L&T Product Development Centre)
- **Date:** 14th March 2026
- **Problem Statement:** PS2 — Costing Automation: CAD-to-Quote AI Agent
- **Round 1:** Abstract Submission → Shortlisting
- **Round 2:** Concept Presentation (PPT + Live Demo)

---

## Problem Statement Summary

Build an AI system that:

- Extracts manufacturing features from CAD models
- Estimates material, machining, setup, and overhead costs
- Provides a transparent cost breakdown
- Includes a chat-style quoting agent
- Shows explainable AI (top cost drivers + what-if impact)
- Suggests DFM changes that reduce cost

---

## What They Are Asking vs What They Expect (Deep Breakdown)

This section maps directly to PS2 wording + the official evaluation guidelines.

### What PS2 is *explicitly asking you to build* (Must-Haves)

- **Manufacturing feature extraction from CAD**
  - Input is a CAD model; output must be measurable features (geometry + manufacturing proxies).
- **Cost calculation algorithms**
  - You must have a clear costing logic (even if ML is used). The system should not feel like a "black box".
- **Estimate costs with a transparent split**
  - Expected outcome explicitly mentions: **material + machining + setup + overhead**.
- **Chat-style quoting agent (not optional)**
  - The agent must collect at least: **material, quantity, tolerance** and then generate the quote.
- **Explainable AI + what-if impact**
  - Show top cost drivers and demonstrate how changing a feature changes the quote.
- **DFM suggestions**
  - Provide student-friendly design recommendations that reduce cost and machining time.

### What PS2 expects as a *demo experience*

- **Quote in seconds** (fast end-to-end flow)
- **Auto quotation summary (report/PDF-ready)**
- **Improves over time** using **historical or synthetic data** (synthetic is acceptable for hackathon; design pipeline to later plug real data)

---

## How the Event Evaluates You (Round 1 vs Round 2)

This section is based on the Event Guidelines.

### Round 1 — Abstract (Shortlisting)

Your abstract is evaluated on:

- **Relevance** to PS2
- **Understanding** of the problem
- **Core idea** and why it solves the problem
- **Approach/framework** (system flow, modules, what you will build)
- **Feasibility** within the timeline
- **Originality + practical value** (clear differentiation without unnecessary complexity)

Round 1 rewards clarity and feasibility over a fully built product.

### Round 2 — Concept Presentation (Final Evaluation)

Your presentation/demo is evaluated on:

- **Depth of understanding** (manufacturing + quoting workflow)
- **Practicality and clarity** (usable quoting flow, transparent pricing)
- **Alignment with real engineering/operational needs** (breakdown, risk, reasoning)
- **Technical reasoning and execution approach** (why these features/models)
- **Innovation, scalability, and future potential** (how it becomes a real tool)

Note: supporting materials (diagrams, wireframes, mockups, simulations) are a value-add; a working prototype helps but a strong concept is still acceptable.

---

## Judge-Ready Deliverables Checklist (What We Will Show)

**Core Pipeline:**

- CAD upload → auto-extracted geometry table (volume, surface area, bounding box, face count)
- Chat agent collects: part type, material, quantity, tolerance — guided, step-by-step, with contextual engineering insights at each step
- Process routing: system identifies turning / milling / drilling / grinding from geometry + inputs
- Manufacturability risk assessment shown before quote (Differentiator 7)
- Quote generated in seconds with genuine multi-component breakdown
- Transparent breakdown: material / machining (per-process, genuinely predicted) / setup / overhead
- Process-wise cost contribution: each active process predicted by its own sub-model
- Manufacturing time estimation alongside cost — per-process (Differentiator 6)

**Explainability & Visualization:**

- Global feature importances + per-quote SHAP waterfall (dual-layer: global AND local)
- Cost Sankey diagram: interactive flow from inputs → processes → total cost (Differentiator 3)
- Cost heatmap on 3D model: color-coded regions showing high-cost areas (Differentiator 11)
- AI-generated quote narrative: plain-English paragraph summary (Differentiator 9)
- Similar parts finder: top 3 closest parts from dataset with costs (Differentiator 10)

**Design Intelligence:**

- Interactive what-if simulator: sliders for each modifiable feature → live cost recalculation + sensitivity chart
- Tolerance–cost tradeoff curve: full spectrum view across all tolerance levels (Differentiator 4)
- Break-even quantity analysis: per-unit cost curve with stabilization point (Differentiator 5)
- DFM suggestions: concrete rule-based engine with quantified ₹ AND hours saved per suggestion
- Quote version comparison: side-by-side diff of old vs new quote (Differentiator 8)

**Trust & Improvement:**

- Confidence + cost range with visual gauge, risk classification, and uncertainty explanation
- Feedback loop: user confirms/corrects actual cost → row added, accuracy impact shown
- Model validation dashboard: per-model RMSE/MAE/R², actual-vs-predicted plots, cross-validation

**Output:**

- Professional PDF quote summary with embedded charts, SHAP waterfall, Sankey, and 3D model thumbnail
- Real-time cost ticker: cost updates live as each input is entered

---

## High-Level System Flow

```
CAD File (.STL / .STEP / .IGES)
           ↓
  Geometry Extractor  (auto: volume, surface area, bounding box, face count)
           ↓
  Chat Agent  ──────→  part type, material, quantity, tolerance
           ↓              ↓ contextual engineering advice at each step
           ↓              ↓ real-time cost ticker (narrows as inputs arrive)
  Process Router  (turning / milling / drilling / grinding / combined)
           ↓
  Manufacturability Risk Assessment (pre-quote risk flags)  [Diff 7]
           ↓
  Feature Vector  [geometry + process + user inputs]
           ↓
  7 Cost Sub-Models + 4 Time Sub-Models (Random Forest)
    ├── Material Cost Model
    ├── Machining: Drilling (Cost + Time)
    ├── Machining: Milling  (Cost + Time)
    ├── Machining: Turning  (Cost + Time)
    ├── Machining: Grinding (Cost + Time)
    ├── Setup Cost Model
    └── Overhead Cost Model
           ↓
  Total Quote = sum of active components  |  Total Time = sum of active processes
           ↓
  Output Engine
    → Cost breakdown + Cost Sankey diagram                         [Diff 3]
    → Manufacturing time breakdown (per-process)                   [Diff 6]
    → Cost heatmap on 3D model                                     [Diff 11]
    → Explainability (global importances + SHAP waterfall)
    → AI-generated quote narrative (plain English)                  [Diff 9]
    → Similar parts finder (k-NN benchmarking)                     [Diff 10]
    → Interactive what-if simulator + tolerance-cost curve          [Diff 4]
    → Break-even quantity analysis                                  [Diff 5]
    → DFM rules engine (₹ + hours saved per suggestion)
    → Quote version comparison (side-by-side diff)                  [Diff 8]
    → Confidence range + visual gauge + uncertainty explanation
           ↓
  Feedback Loop  (user confirms/corrects → accuracy impact tracked)
           ↓
  Professional PDF Export (charts + Sankey + SHAP + 3D heatmap)
```

---

## Step-by-Step Pipeline

### STEP 1 — CAD Input

**Accepted formats:** `.STL`, `.STEP`, `.IGES`

User uploads via the Streamlit UI. The system reads the file and passes it to the geometry extractor.

> Do NOT train ML on raw CAD. Always extract numeric geometry statistics first.

---

### STEP 2 — Geometry Extraction

**What trimesh CAN extract automatically (from STL):**

| Feature            | Meaning                   | Source |
| ------------------ | ------------------------- | ------ |
| Volume             | Material used             | Auto   |
| Surface area       | Machining effort          | Auto   |
| Bounding box (XYZ) | Part size / machine size  | Auto   |
| Face count         | Mesh complexity proxy     | Auto   |
| Watertight check   | Is geometry valid/closed? | Auto   |
| Aspect ratio       | Cylindrical vs prismatic  | Auto   |

**What requires STEP files or user input (NOT auto from STL mesh):**

| Feature        | How to Get It                                            |
| -------------- | -------------------------------------------------------- |
| num_holes      | `cadquery` on STEP — or user provides count           |
| avg_hole_depth | `cadquery` on STEP — or user provides                 |
| num_pockets    | `cadquery` on STEP — or user provides                 |
| fillet_count   | `cadquery` on STEP — or estimated from face curvature |

> **Hackathon approach:** Auto-extract geometry stats from any file. For STL, supplement with 2–3 user inputs via the chat agent (hole count, pocket count). For STEP, use `cadquery` to extract topology directly. Never claim full automatic detection from STL alone.

---

### STEP 3 — Feature Engineering ⭐

Combine auto-extracted geometry with user-provided inputs into one feature vector:

| Feature         | Source          | Why Important         |
| --------------- | --------------- | --------------------- |
| volume          | Auto (trimesh)  | Material used         |
| surface_area    | Auto (trimesh)  | Machining effort      |
| aspect_ratio    | Auto (trimesh)  | Process type hint     |
| face_count      | Auto (trimesh)  | Complexity proxy      |
| num_holes       | User / cadquery | Drilling time         |
| avg_hole_depth  | User / cadquery | Machining difficulty  |
| num_pockets     | User / cadquery | Milling effort        |
| material_type   | User (chat)     | Cutting speed, cost   |
| quantity        | User (chat)     | Batch economics       |
| tolerance_grade | User (chat)     | Precision effort      |
| process_type    | Auto (Step 3.5) | Drives machining cost |

Final feature vector:

```
X = [volume, surface_area, aspect_ratio, face_count, holes, hole_depth, pockets, material, qty, tolerance, process_type]
```

---

### STEP 3.5 — Process Routing ⭐ (New)

Before training or predicting, classify the **manufacturing process** from geometry + user inputs.
This is a rule-based classifier — no extra ML needed.

```python
def route_process(aspect_ratio, num_holes, num_pockets, tolerance):
    processes = []
    if aspect_ratio > 3:            # long, cylindrical
        processes.append("Turning")
    if num_pockets > 0:             # has cavities
        processes.append("Milling")
    if num_holes > 0:               # has holes
        processes.append("Drilling")
    if tolerance == "High" or tolerance == "Ultra-High":
        processes.append("Grinding")  # finishing required
    return processes
```

**Output example:**

```
Processes identified: [Turning, Drilling, Grinding]
```

This feeds directly into the cost breakdown — each identified process gets its own genuinely predicted cost estimate.

---

### STEP 4 — Dataset Creation ⭐ (Enhanced)

Generate a synthetic dataset of **1,000–2,000 rows** with realistic non-linear cost relationships. Each row stores **7 genuine cost components** — material, 4 per-process machining costs, setup, and overhead — computed from formulas with engineering-grounded non-linearities.

**Example schema:**

| volume | holes | hole_depth | pockets | material | qty | tolerance | drill_cost | mill_cost | turn_cost | grind_cost | mat_cost | setup | overhead | total |
| ------ | ----- | ---------- | ------- | -------- | --- | --------- | ---------- | --------- | --------- | ---------- | -------- | ----- | -------- | ----- |
| 120    | 4     | 15         | 1       | Aluminum | 10  | Standard  | 480        | 630       | 0         | 0          | 840      | 320   | 320      | 2590  |
| 210    | 6     | 25         | 3       | Steel    | 5   | High      | 980        | 1120      | 0         | 700        | 2100     | 420   | 480      | 5800  |

**Cost formulas per row (non-linear, engineering-grounded):**

```python
# Material rates vary by type (kg/cm³ × ₹/kg)
material_rates = {"Aluminum": 7.0, "Steel": 10.0, "Titanium": 35.0, "Brass": 12.0}
machinability  = {"Aluminum": 1.0, "Steel": 1.8, "Titanium": 5.0, "Brass": 1.2}

# Material cost — batch discount (diminishing returns, not linear)
mat_cost = volume * material_rates[material] * qty * max(0.70, 1 - 0.03 * qty)

# Per-process machining costs (each stored independently)
drill_cost = holes * drill_rate * (hole_depth ** 1.3) * machinability[material]  # deep holes cost exponentially more
mill_cost  = pockets * mill_rate * surface_area_factor * machinability[material]
turn_cost  = turn_rate * volume_factor * machinability[material]                 # only if turning is routed
grind_cost = grind_rate * surface_area * tolerance_multiplier                    # only if grinding is routed

# Setup — amortized per unit (hyperbolic, not flat)
setup_cost = (base_setup + num_processes * process_setup_fee) / qty

# Overhead — scaled with noise
overhead = (mat_cost + drill_cost + mill_cost + turn_cost + grind_cost) * overhead_pct

total = mat_cost + drill_cost + mill_cost + turn_cost + grind_cost + setup_cost + overhead
```

**Why non-linear formulas matter:**

- **Deep holes** cost disproportionately more (exponential, not linear) — justifies ML over formula lookup
- **Batch discounts** follow diminishing returns — quantity 100 isn't 10× cheaper than quantity 10
- **Material-speed interaction** — Titanium drilling is 5× slower than Aluminum, creating cross-feature dependencies
- **Setup amortization** — hyperbolic per-unit relationship; single-unit parts carry full setup cost

**Dataset best practices:**

- Add ±3–8% varied noise per cost component (overhead noisier than material)
- Include edge case rows: extreme aspect ratios, qty=1, ultra-high tolerance + soft material
- Ensure balanced coverage across material types and tolerance grades (stratified sampling)
- Set non-routed process costs to 0 (e.g., no turning cost if aspect_ratio ≤ 3)

> This dataset structure defends against judges asking *"why not just use the formula?"* — the answer is: real costs have cross-feature interactions and non-linear scaling that formulas can't capture cleanly, and ML generalizes better across the full feature space.

---

### STEP 5 — ML Model Training ⭐ (Enhanced)

**Model:** `RandomForestRegressor` (scikit-learn) — trained as **7 separate sub-models**:

- 1 × Material cost model
- 4 × Per-process machining models (Drilling, Milling, Turning, Grinding)
- 1 × Setup cost model
- 1 × Overhead cost model

**Why 7 sub-models (not 4):**

The original strategy trained one machining model and then split by fixed ratio weights — this is still ratio-based and contradicts the "genuine, not ratios" principle. By training one model per manufacturing process, every rupee in the process-wise breakdown is genuinely predicted by its own model with its own feature importances.

```python
model_material  = RandomForestRegressor(n_estimators=200).fit(X, y_material)
model_drilling  = RandomForestRegressor(n_estimators=200).fit(X, y_drilling)
model_milling   = RandomForestRegressor(n_estimators=200).fit(X, y_milling)
model_turning   = RandomForestRegressor(n_estimators=200).fit(X, y_turning)
model_grinding  = RandomForestRegressor(n_estimators=200).fit(X, y_grinding)
model_setup     = RandomForestRegressor(n_estimators=200).fit(X, y_setup)
model_overhead  = RandomForestRegressor(n_estimators=200).fit(X, y_overhead)

# Only sum predictions from routed processes
active_models = [model_material, model_setup, model_overhead]
for process in identified_processes:
    active_models.append(process_model_map[process])

total_cost = sum([m.predict(X_new) for m in active_models])
```

**Model Validation Dashboard ⭐ (New — shown as a Streamlit tab):**

Instead of only tracking metrics internally, expose a **Model Performance** tab in the UI:

- Per-model metrics displayed as cards: **RMSE, MAE, R²**
- **Actual vs Predicted scatter plot** for each sub-model (proves predictions are accurate)
- **Residual distribution plot** (shows errors are random, not systematic)
- **5-fold cross-validation results** (not just one 80/20 split — more credible to judges)
- Metric summary table:

```
Model Performance (5-Fold Cross-Validation):
  Material Cost  → R²: 0.97  |  MAE: ₹42   |  RMSE: ₹58
  Drilling Cost  → R²: 0.95  |  MAE: ₹31   |  RMSE: ₹45
  Milling Cost   → R²: 0.94  |  MAE: ₹38   |  RMSE: ₹52
  Turning Cost   → R²: 0.96  |  MAE: ₹28   |  RMSE: ₹40
  Grinding Cost  → R²: 0.93  |  MAE: ₹22   |  RMSE: ₹35
  Setup Cost     → R²: 0.98  |  MAE: ₹15   |  RMSE: ₹22
  Overhead       → R²: 0.96  |  MAE: ₹35   |  RMSE: ₹48
```

> This directly supports PS2's "improved accuracy over time" — you show judges the system *knows* how accurate it is and can prove it.

---

### STEP 6 — Cost Breakdown ⭐ (Genuinely Predicted, Not Ratios)

Each component is predicted independently by its own sub-model. The process-wise machining breakdown is **genuinely predicted** — not a single machining total split by fixed weights.

```
Estimated Total Cost: ₹4,200
  ├── Material Cost      : ₹1,050  (predicted by model_material)
  ├── Machining Cost     : ₹2,310  (sum of active process models)
  │     ├── Turning      :   ₹600  (predicted by model_turning)
  │     ├── Drilling     :   ₹810  (predicted by model_drilling)
  │     ├── Milling      :   ₹630  (predicted by model_milling)
  │     └── Grinding     :   ₹270  (predicted by model_grinding)
  ├── Setup Cost         :   ₹420  (predicted by model_setup)
  └── Overhead           :   ₹420  (predicted by model_overhead)
```

**Key difference from original strategy:** Each process cost line now comes from its own trained model with its own learned feature relationships — not `machining_total * process_weight[process]`. This means:

- Each process model has its own `.feature_importances_` → process-level explainability is real
- Each process model can be independently validated with RMSE/R²
- If a process is not routed (e.g., no Turning for a prismatic part), its model is simply not called — no need to zero out a ratio

This is what L&T means by **"feature-wise AND process-wise cost contribution"** — both are genuinely predicted and independently explainable.

---

### STEP 7 — Explainability Engine ⭐ (Enhanced — Dual Layer)

Show **three layers** of explainability — global feature importances, per-quote SHAP waterfall, and process-wise:

**Layer 1 — Global Feature Importances (from `.feature_importances_`):**

```
Global Cost Drivers (across all predictions):
  + volume            (31%)  → more material consumed
  + avg_hole_depth    (22%)  → longer drilling cycle time
  + num_pockets       (14%)  → additional milling passes
  + material_type     (11%)  → raw material price + cutting speed
```

**Layer 2 — Per-Quote SHAP Waterfall ⭐ (New):**

Use `shap.TreeExplainer` to show what drove *this specific part's* cost up or down from the dataset average:

```python
import shap
explainer = shap.TreeExplainer(model_material)
shap_values = explainer.shap_values(X_new)
shap.waterfall_plot(shap_values[0])
```

**Example output for a specific quote:**

```
Part-Specific Cost Drivers (this quote):
  Base (average cost)           : ₹3,200
  + 6 deep holes                : +₹810   (above average drilling complexity)
  + Steel material              : +₹420   (above average material cost)
  + 3 pockets                   : +₹310   (above average milling effort)
  − Low volume (120 cm³)        : −₹340   (below average material consumption)
  − Standard tolerance          : −₹200   (no grinding required)
  ─────────────────────────────────────────
  = This part's predicted cost  : ₹4,200
```

> This tells the engineer *exactly* why *their specific part* costs what it does — not just general averages.

**Layer 3 — Process-wise (from Step 6 per-process models):**

```
Machining Cost by Process (genuinely predicted):
  + Drilling  : ₹810  (35% of machining)  ← driven by 6 holes × 25mm depth
  + Milling   : ₹630  (27% of machining)  ← driven by 3 pockets
  + Turning   : ₹600  (26% of machining)  ← driven by cylindrical geometry
  + Grinding  : ₹270  (12% of machining)  ← driven by High tolerance
```

Each process cost is explained by its own model's SHAP values — genuine process-level explainability.

**Make this interactive in the UI:**

- User clicks any feature driver → sees ₹ contribution + engineering reason
- User clicks any process → sees what drives that process cost via its own SHAP values
- User adjusts a feature value → cost recalculates live (connects to What-If Simulator in Differentiator 1)

---

### STEP 8 — Chat Agent ⭐ (Centerpiece UX — Enhanced)

The chat agent is the headline feature of PS2 — not a side component. Design a complete, professional guided flow with **contextual engineering intelligence** at every step:

```
Agent: "Welcome to QuoteAI! Upload your CAD file to get started."
User:  [uploads part.stl]
Agent: "Got it. I extracted the following geometry:
         Volume: 120 cm³ | Surface Area: 210 cm² | Faces: 842
         What is the part material? (Aluminum / Steel / Titanium / Other)"
User:  "Steel"
Agent: "📋 Steel selected.
         ℹ️ Note: Steel has a machinability index of 1.8× — machining costs
         will be higher than Aluminum but significantly lower than Titanium.
         Density: 7.85 g/cm³ | Hardness: ~200 HB
         How many units are you ordering?"
User:  "5"
Agent: "What tolerance grade does this part require?"
        [Standard] [High] [Ultra-High]
User:  "High"
Agent: "⚙️ High tolerance requires a Grinding finishing pass, which will
         add approximately ₹200–₹400 to the machining cost.
         How many holes does the part have? (Approximate is fine)"
User:  "6"
Agent: "Any pockets or cavities? (Yes/No)"
User:  "Yes, 2 pockets"
Agent: "Analyzing... Processes identified: Drilling + Milling + Grinding
         ─────────────────────────────────────────
         💰 Estimated Cost    : ₹5,800
         📊 Cost Range        : ₹5,420 – ₹6,180
         🎯 Confidence        : 79% (Medium Risk)
         ─────────────────────────────────────────
         Material          : ₹2,100
         Machining         : ₹2,800 (Drill ₹980 | Mill ₹1,120 | Grind ₹700)
         Setup             : ₹480
         Overhead          : ₹420
         ─────────────────────────────────────────
         📈 This part costs 18% more than average for similar-volume Steel parts.
         Would you like to: [See Cost Drivers] [What-If Simulator] [DFM Suggestions] [Download PDF]"
```

**Contextual intelligence responses ⭐ (New):**

| When User Selects...            | Agent Provides...                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| **Titanium**                    | "Titanium is 3–5× harder to machine than Aluminum. Expect significantly higher machining cost. Consider Aluminum if strength allows." |
| **Quantity = 1**                | "Single-unit orders carry full setup cost. Would you like to see a comparison quote at qty=5?"                            |
| **Quantity > 10,000**           | "At this volume, tooling amortization significantly reduces per-unit cost. Setup cost per unit drops below ₹5."           |
| **Ultra-High tolerance**        | "Ultra-High tolerance requires Grinding as a finishing pass. This adds ₹X to the estimate."                              |
| **Extreme aspect ratio** (auto) | "Your part has a 7:1 aspect ratio — CNC Turning will dominate machining cost."                                           |

**Edge case handling (mandatory):**

| Situation                           | Agent Response                                                                                             |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Corrupted / unreadable CAD file     | "I couldn't read this file. Please upload a valid STL or STEP file."                                       |
| Quantity = 1 (one-off part)         | Adds high setup cost weighting; flags: "One-off parts carry higher setup cost per unit."                   |
| Quantity > 10,000 (mass production) | Flags: "At this volume, tooling amortization significantly reduces per-unit cost."                         |
| Missing input (user skips)          | Agent re-asks: "I need the material type to continue — please select one."                                |
| Non-manufacturable geometry         | Flags thin walls or extreme aspect ratios: "Warning: wall thickness may be below machinability threshold." |

**Real-time cost ticker ⭐ (New):**

As each input is provided, a sidebar cost estimate updates progressively:

```
Inputs collected so far: Material=Steel, Qty=5
├── Estimated range (partial): ₹3,800 – ₹6,200
└── Waiting for: tolerance, holes, pockets
```

This makes the speed of quoting *visible* — the cost narrows in front of the engineer's eyes.

Build with Streamlit `st.chat_message` and `st.chat_input` components.

---

### STEP 9 — PDF Export ⭐ (Enhanced — Professional Quotation)

Auto-generate a **professional-grade quote summary PDF** that looks like a real industrial quotation:

**Layout and content:**

- **Header:** Company branding area (QuoteAI logo, date, quote reference number)
- **Part Summary:** Part name, geometry properties table, 3D model thumbnail (rendered via `trimesh.scene.Scene` → PNG export)
- **Cost Breakdown:** Visualized as a stacked bar chart or pie chart, not just text
- **Process-wise Machining Split:** Horizontal bar chart with ₹ labels
- **SHAP Waterfall Chart:** Embedded per-quote explainability visualization
- **DFM Suggestions:** Numbered list with ₹ savings per suggestion
- **Confidence Range:** Visual gauge graphic with risk classification
- **Quote Validity:** "This estimate is valid for 30 days from generation date"
- **Disclaimer:** "Estimate based on geometric analysis and ML prediction. Actual cost may vary."

**Tools:** `fpdf2` for layout + `matplotlib` for charts rendered as embedded PNGs.

> A polished PDF signals **production readiness** — a key Round 2 evaluation criterion. Judges associate visual quality with engineering maturity.

---

### STEP 10 — Feedback Loop ⭐ (Enhanced — Visible Impact)

After showing the quote, the agent asks:

```
Agent: "Was this quote accurate? If you know the actual cost, enter it below
        so the system can learn and improve."
User:  ₹5,600
Agent: "✅ Feedback recorded. Here's what your feedback means:

        📊 Training Data: 1,500 synthetic + 12 real-world entries
        📈 Model Accuracy: Improved from 91.2% → 91.5% (after last retrain)
        💰 Your feedback has reduced average quote error by ₹340

        Real-world data is 3× more valuable than synthetic data for model
        improvement. Thank you for contributing to accuracy improvement."
```

**Implementation:**

- The confirmed row (features + actual cost) is appended to `training_data.csv`
- A **data growth tracker** displays: synthetic count + real-world count
- A **before/after accuracy comparison** shows the tangible impact of feedback
- A retraining trigger flag is set (can be manual for demo; automatic in production)
- Admin view includes a **"Retrain Models" button** (even if just a demo trigger)

This directly satisfies PS2's "improved accuracy over time using historical data" requirement — and makes it **demonstrable** rather than just claimed.

**Scalability note for judges:** *In production, this connects to an L&T PLM/ERP system, ingests real historical quotes, and retrains weekly. The synthetic dataset used here is the seed data — the system is designed to outgrow it.*

---

## ⭐ Differentiator 1 — Design Optimization + Interactive What-If (Enhanced)

### Part A — DFM Rules Engine ⭐ (New — Concrete Implementation)

A rule-based engine that generates **specific, quantified DFM suggestions** automatically after every quote:

```python
def generate_dfm_suggestions(features, models, identified_processes):
    suggestions = []

    # Rule 1: Hole consolidation
    if features["num_holes"] > 4:
        modified = features.copy()
        modified["num_holes"] = 4
        savings = predict_total(features, models) - predict_total(modified, models)
        suggestions.append({
            "change": f"Reduce holes from {features['num_holes']} → 4",
            "savings": savings,
            "reason": "Fewer holes reduce drilling cycle time and tool changes"
        })

    # Rule 2: Pocket simplification
    if features["num_pockets"] > 2:
        modified = features.copy()
        modified["num_pockets"] = max(1, features["num_pockets"] - 1)
        savings = predict_total(features, models) - predict_total(modified, models)
        suggestions.append({
            "change": f"Simplify from {features['num_pockets']} → {modified['num_pockets']} pockets",
            "savings": savings,
            "reason": "Fewer pockets reduce milling passes and setup complexity"
        })

    # Rule 3: Material substitution
    if features["material_type"] in ["Titanium", "Steel"]:
        modified = features.copy()
        modified["material_type"] = "Aluminum"
        savings = predict_total(features, models) - predict_total(modified, models)
        suggestions.append({
            "change": f"Switch from {features['material_type']} → Aluminum (if strength allows)",
            "savings": savings,
            "reason": "Aluminum is cheaper and 2–5× faster to machine"
        })

    # Rule 4: Tolerance relaxation
    if features["tolerance_grade"] in ["Ultra-High", "High"]:
        lower = "Standard" if features["tolerance_grade"] == "High" else "High"
        modified = features.copy()
        modified["tolerance_grade"] = lower
        savings = predict_total(features, models) - predict_total(modified, models)
        suggestions.append({
            "change": f"Relax tolerance from {features['tolerance_grade']} → {lower}",
            "savings": savings,
            "reason": "Lower tolerance removes or reduces grinding finishing pass"
        })

    # Rule 5: Batch size optimization
    if features["quantity"] == 1:
        modified = features.copy()
        modified["quantity"] = 5
        original_per_unit = predict_total(features, models)
        batch_per_unit = predict_total(modified, models)
        savings = original_per_unit - batch_per_unit
        suggestions.append({
            "change": "Order batch of 5 instead of 1",
            "savings": savings,
            "reason": "Setup cost is amortized across units — per-unit cost drops significantly"
        })

    # Rule 6: Reduce hole depth
    if features["avg_hole_depth"] > 20:
        modified = features.copy()
        modified["avg_hole_depth"] = 15
        savings = predict_total(features, models) - predict_total(modified, models)
        suggestions.append({
            "change": f"Reduce avg hole depth from {features['avg_hole_depth']}mm → 15mm",
            "savings": savings,
            "reason": "Deep holes increase drilling time exponentially due to chip evacuation"
        })

    # Rule 7: Aspect ratio reduction
    if features["aspect_ratio"] > 5:
        suggestions.append({
            "change": "Consider redesigning for lower aspect ratio (< 5:1)",
            "savings": "Varies",
            "reason": "High aspect ratio increases turning passes and may require tailstock support"
        })

    # Rule 8: Multi-setup warning
    if len(identified_processes) >= 3:
        suggestions.append({
            "change": "Redesign for fewer manufacturing processes (currently: " + str(len(identified_processes)) + ")",
            "savings": "Varies",
            "reason": "Each additional process adds setup time, tool changes, and handling cost"
        })

    # Sort by savings (highest first)
    return sorted(suggestions, key=lambda s: s.get("savings", 0) if isinstance(s.get("savings"), (int, float)) else 0, reverse=True)
```

**Output:**

```
🔧 DFM Suggestions (ranked by savings):

  1. Switch from Steel → Aluminum         saves ₹620
     └ Aluminum is cheaper and 2–5× faster to machine

  2. Reduce holes from 6 → 4              saves ₹420
     └ Fewer holes reduce drilling cycle time and tool changes

  3. Simplify from 3 → 2 pockets          saves ₹380
     └ Fewer pockets reduce milling passes and setup complexity

  4. Relax tolerance High → Standard       saves ₹270
     └ Lower tolerance removes grinding finishing pass

  ─────────────────────────────────────────
  Total Potential Savings: ₹1,690 (29% of original cost)
  Optimized Cost: ₹4,110
```

### Part B — Interactive What-If Simulator ⭐ (New)

A dedicated Streamlit panel where the user can **explore design changes live**:

```python
st.subheader("🔬 What-If Simulator")

# Sliders for each modifiable feature
mod_holes = st.slider("Number of holes", 0, 20, current_holes)
mod_pockets = st.slider("Number of pockets", 0, 10, current_pockets)
mod_hole_depth = st.slider("Avg hole depth (mm)", 5, 50, current_hole_depth)
mod_material = st.selectbox("Material", ["Aluminum", "Steel", "Titanium", "Brass"], index=current_idx)
mod_tolerance = st.selectbox("Tolerance", ["Standard", "High", "Ultra-High"], index=current_tol_idx)
mod_quantity = st.number_input("Quantity", 1, 100000, current_qty)

# Live cost recalculation
modified_cost = predict_with_modified_features(...)

# Display
col1, col2, col3 = st.columns(3)
col1.metric("Original Cost", f"₹{original_cost:,.0f}")
col2.metric("Modified Cost", f"₹{modified_cost:,.0f}", delta=f"₹{modified_cost - original_cost:,.0f}")
col3.metric("Savings", f"₹{original_cost - modified_cost:,.0f}", delta=f"{(original_cost - modified_cost)/original_cost*100:.1f}%")

# Sensitivity bar chart: which feature has the steepest cost gradient
st.bar_chart(sensitivity_data)
```

**Sensitivity analysis (shows which feature to change first):**

```
Feature Sensitivity (₹ change per unit adjustment):
  avg_hole_depth   : ₹52 / mm       ← Most cost-sensitive
  num_holes        : ₹105 / hole
  num_pockets      : ₹380 / pocket
  material_type    : ₹620 / switch
  tolerance_grade  : ₹270 / grade
```

This directly satisfies PS2's *"what-if design change impact"* as an interactive, live experience.

### Why Differentiator 1 Wins

Converts a predictor into a **manufacturing intelligence tool**. Every other team shows a cost. You show how to reduce it — with quantified suggestions AND a live exploration tool.

---

## ⭐ Differentiator 2 — Confidence + Cost Range ⭐ (Enhanced — Actionable Reliability)

### What It Does

Shows **how reliable** the predicted cost is — with a visual gauge, risk classification, and an explanation of **what's causing uncertainty**.

### How It Works

Use the individual tree predictions from each Random Forest sub-model:

```python
def compute_confidence(models, X_new):
    all_tree_preds = []
    for model in models.values():
        tree_preds = np.array([tree.predict(X_new) for tree in model.estimators_])
        all_tree_preds.append(tree_preds.sum(axis=0))  # sum across models per tree

    combined = np.array(all_tree_preds).sum(axis=0)
    cost_mean = np.mean(combined)
    cost_std = np.std(combined)
    cost_min = np.percentile(combined, 10)
    cost_max = np.percentile(combined, 90)

    # Confidence as inverse of coefficient of variation
    cv = cost_std / cost_mean
    confidence = max(0, min(100, int((1 - cv * 5) * 100)))

    # Risk classification
    if confidence >= 85:
        risk = "Low Risk 🟢"
    elif confidence >= 60:
        risk = "Medium Risk 🟡"
    else:
        risk = "High Risk 🔴"

    return cost_mean, cost_min, cost_max, confidence, risk
```

### Output

```
💰 Estimated Cost : ₹4,200
📊 Cost Range     : ₹3,950 – ₹4,480
🎯 Confidence     : 82% (Medium Risk 🟡)

⚠️ Uncertainty Drivers:
  → This combination of Steel + 6 deep holes has limited training coverage
  → Recommendation: Provide actual cost feedback to improve future estimates
```

### Visual Confidence Gauge ⭐ (New)

Display a speedometer-style gauge in the Streamlit UI:

- **Green zone (85–100%):** High confidence — quote is reliable
- **Yellow zone (60–84%):** Medium confidence — quote is indicative
- **Red zone (0–59%):** Low confidence — treat as rough estimate

### Uncertainty Explanation ⭐ (New)

The system explains **why** confidence is low when it is:

```python
def explain_uncertainty(X_new, X_train, feature_names):
    """Identify which features have sparse training data coverage"""
    explanations = []
    for i, feat in enumerate(feature_names):
        # Check how many training examples are similar to this input
        similar_count = np.sum(np.abs(X_train[:, i] - X_new[0, i]) < threshold[i])
        if similar_count < min_coverage:
            explanations.append(f"Limited training data for {feat}={X_new[0, i]}")
    return explanations
```

### Why Differentiator 2 Wins

No other team will show this. It adds **trust** to the quote and demonstrates real understanding of how ML uncertainty works in engineering decisions. The explanation turns it from a passive indicator into **actionable intelligence**.

---

## ⭐ Differentiator 3 — Cost Sankey Diagram (Visual Cost Flow)

**PS2 mapping:** *"Clear feature-wise and process-wise cost contribution (transparent pricing)"*

### What It Does

Visualizes the **complete cost genealogy** as an interactive Sankey flow diagram — every rupee is traceable from input feature through manufacturing process to final cost.

### How It Works

```python
import plotly.graph_objects as go

def render_cost_sankey(breakdown, features):
    """Render interactive Sankey diagram from cost breakdown"""
    labels = [
        # Sources (left)
        f"Raw Material ({features['material_type']})",
        f"Holes ({features['num_holes']})",
        f"Pockets ({features['num_pockets']})",
        f"Tolerance ({features['tolerance_grade']})",
        "Batch Setup",
        # Processes (middle)
        "Material Cost", "Drilling", "Milling", "Turning", "Grinding",
        "Setup Cost", "Overhead",
        # Destination (right)
        f"TOTAL: ₹{breakdown['total']:,.0f}"
    ]

    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels, color=color_palette),
        link=dict(
            source=[0,1,1,2,3,4, 5,6,7,8,9,10,11],
            target=[5,6,8,7,9,10, 12,12,12,12,12,12,12],
            value=[
                breakdown['material'], breakdown['drilling'],
                breakdown['turning'], breakdown['milling'],
                breakdown['grinding'], breakdown['setup'],
                breakdown['material'], breakdown['drilling'],
                breakdown['milling'], breakdown['turning'],
                breakdown['grinding'], breakdown['setup'],
                breakdown['overhead']
            ]
        )
    )])
    return fig
```

### Output

```
[Interactive Sankey Flow in Streamlit]

  Raw Material ──→ Material Cost (₹2,100) ──┐
                                              │
  Holes (6) ─────→ Drilling (₹980) ──┐       │
  Pockets (2) ───→ Milling (₹1,120) ─┤       ├──→ TOTAL: ₹5,800
  Tolerance ─────→ Grinding (₹700) ──┘       │
                                  ↓           │
                     Machining (₹2,800) ──────┤
                                              │
  Batch Setup ───→ Setup (₹480) ─────────────┤
  Overhead ──────→ Overhead (₹420) ──────────┘
```

### Why It Wins

Judges can **trace every rupee** from input to output in one glance. The most visual and intuitive way to present "transparent pricing." Uses `plotly` — 1 chart call, ~30 lines of code.

---

## ⭐ Differentiator 4 — Tolerance–Cost Tradeoff Curve

**PS2 mapping:** *"What-if design change impact"* — tolerance is one of the 3 inputs PS2 explicitly names.

### What It Does

Shows a **graph** of how cost changes across all tolerance levels for the current part, so the engineer can visually pick the optimal precision level.

### How It Works

```python
def tolerance_cost_curve(features, models):
    """Run prediction at each tolerance level, plot the cost curve"""
    tolerances = ["Standard", "High", "Ultra-High"]
    costs = []
    for tol in tolerances:
        modified = features.copy()
        modified["tolerance_grade"] = tol
        costs.append(predict_total(modified, models))

    fig, ax = plt.subplots()
    ax.bar(tolerances, costs, color=["#4CAF50", "#FFC107", "#F44336"])
    ax.set_ylabel("Estimated Cost (₹)")
    ax.set_title("Tolerance vs Cost — This Part")

    for i, (tol, cost) in enumerate(zip(tolerances, costs)):
        ax.text(i, cost + 50, f"₹{cost:,.0f}", ha="center", fontweight="bold")

    return fig, tolerances, costs
```

### Output

```
Tolerance vs Cost (this part):

  Ultra-High  ████████████████████  ₹6,800  (+₹1,000 vs High)
  High        ██████████████████    ₹5,800  ← Your selection
  Standard    █████████████         ₹4,200  (−₹1,600 vs High)

  "Relaxing from High → Standard saves ₹1,600 (27%).
   Tightening to Ultra-High adds ₹1,000 (17%).
   Standard removes the Grinding finishing pass entirely."
```

### Why It Wins

Takes "what-if" from a single comparison to a **full spectrum view**. The engineer sees the entire cost landscape and can make an informed precision choice. ~15 lines of code.

---

## ⭐ Differentiator 5 — Break-Even Quantity Analysis

**PS2 mapping:** *"DFM suggestions that reduce cost"* — batch ordering is a concrete cost reduction strategy.

### What It Does

Shows the engineer **at what batch size per-unit cost stabilizes** — directly answers "how many should I order?"

### How It Works

```python
def break_even_analysis(features, models):
    """Run prediction at multiple quantities, plot per-unit cost curve"""
    quantities = [1, 2, 5, 10, 25, 50, 100, 500]
    per_unit_costs = []
    setup_per_unit = []

    for qty in quantities:
        modified = features.copy()
        modified["quantity"] = qty
        total = predict_total(modified, models)
        setup = models["setup"].predict(build_vector(modified))[0]
        per_unit_costs.append(total)
        setup_per_unit.append(setup)

    # Find stabilization point (where marginal savings < 2%)
    for i in range(1, len(per_unit_costs)):
        delta = (per_unit_costs[i-1] - per_unit_costs[i]) / per_unit_costs[i-1]
        if delta < 0.02:
            stabilization_qty = quantities[i]
            break

    return quantities, per_unit_costs, setup_per_unit, stabilization_qty
```

### Output

```
📦 Break-Even Quantity Analysis:

  Qty   | Per-Unit Cost | Setup/Unit  | Savings vs Qty=1
  ──────┼───────────────┼─────────────┼──────────────────
   1    |    ₹8,200     |   ₹2,400    |       —
   5    |    ₹5,800     |     ₹480    |     −29%
  10    |    ₹4,900     |     ₹240    |     −40%
  50    |    ₹4,350     |      ₹48    |     −47%
 100    |    ₹4,280     |      ₹24    |     −48%  ← Cost stabilizes
 500    |    ₹4,260     |       ₹5    |     −48%

  📈 [Diminishing returns curve plotted]

  "Ordering ≥50 units reduces per-unit cost by 47% vs single unit.
   Beyond 100 units, further savings are marginal (<2%).
   Recommended minimum batch: 10 units for best cost/flexibility tradeoff."
```

### Why It Wins

Every real procurement engineer asks this question. Answering it automatically transforms the system from a single-quote tool into a **production planning advisor**.

---

## ⭐ Differentiator 6 — Manufacturing Time Estimation

**PS2 mapping:** *"DFM suggestions that reduce cost **and machining time**"* — PS2 explicitly says "machining time" but the system currently only estimates cost.

### What It Does

Alongside cost, predicts **manufacturing time per process** — directly answers "how long will this take?"

### How It Works

Add time columns to the synthetic dataset using the same formulas with time-based rates:

```python
# Time formulas (parallel to cost formulas)
drill_time = holes * (hole_depth / drill_feed_rate) * machinability[material]   # minutes
mill_time  = pockets * pocket_volume / mill_removal_rate * machinability[material]
turn_time  = turning_length / (rpm * feed_per_rev) * machinability[material]
grind_time = surface_area / grind_rate * tolerance_multiplier
setup_time = base_setup_time + num_processes * process_changeover_time          # fixed per batch

# Train parallel time sub-models
model_drill_time  = RandomForestRegressor(n_estimators=200).fit(X, y_drill_time)
model_mill_time   = RandomForestRegressor(n_estimators=200).fit(X, y_mill_time)
model_turn_time   = RandomForestRegressor(n_estimators=200).fit(X, y_turn_time)
model_grind_time  = RandomForestRegressor(n_estimators=200).fit(X, y_grind_time)
```

### Output

```
⏱️ Estimated Manufacturing Time: 4.2 hours (per unit)
  ├── Turning     : 1.5 hrs   (36%)
  ├── Drilling    : 1.2 hrs   (29%)  — 6 holes × 25mm deep
  ├── Milling     : 0.8 hrs   (19%)  — 2 pockets
  ├── Grinding    : 0.4 hrs   (10%)  — High tolerance finish
  └── Setup/Load  : 0.3 hrs   ( 7%)

  At qty=5, total batch time: ~18 hours (setup amortized)

  ⏱️ Time Savings from DFM:
    → Reduce holes 6→4:        saves 0.4 hrs/unit (−10%)
    → Relax tolerance High→Std: saves 0.4 hrs/unit (−10%, removes grinding)
    → Switch Steel→Aluminum:    saves 0.8 hrs/unit (−19%, faster cutting)
```

### Why It Wins

**This fills a literal gap in PS2 compliance.** PS2 says "reduce cost AND machining time" but the current strategy only predicts cost. Adding time estimation means every DFM suggestion now shows **both ₹ saved AND hours saved** — exactly what PS2 asks for.

---

## ⭐ Differentiator 7 — Manufacturability Risk Score

**PS2 mapping:** *"DFM suggestions that reduce cost and machining time (student-friendly insights)"*

### What It Does

Before showing the quote, runs a **pre-quote risk assessment** that flags potential manufacturing difficulties.

### How It Works

```python
def assess_manufacturability(features, identified_processes):
    """Rule-based risk assessment on feature ratios"""
    risks = []
    total_score = 0

    # Check 1: Hole depth-to-diameter ratio
    if features.get("avg_hole_depth", 0) > 30:
        risks.append({
            "severity": "HIGH",
            "icon": "🔴",
            "issue": f"Deep holes ({features['avg_hole_depth']}mm) — may require peck drilling or specialized tooling",
            "impact": "Adds ₹200–₹400 and 15–30 min per unit",
            "suggestion": "Reduce hole depth to ≤20mm if functionally acceptable"
        })
        total_score += 3

    # Check 2: Multi-process complexity
    if len(identified_processes) >= 3:
        risks.append({
            "severity": "MEDIUM",
            "icon": "🟡",
            "issue": f"{len(identified_processes)} manufacturing processes required — part needs re-fixturing between operations",
            "impact": "Each re-fixturing adds 10–20 min setup time",
            "suggestion": "Redesign features to reduce process count"
        })
        total_score += 2

    # Check 3: Extreme aspect ratio
    if features.get("aspect_ratio", 1) > 8:
        risks.append({
            "severity": "HIGH",
            "icon": "🔴",
            "issue": f"Extreme aspect ratio ({features['aspect_ratio']}:1) — risk of part deflection during turning",
            "impact": "May require tailstock support or reduced feed rate",
            "suggestion": "Redesign for aspect ratio < 5:1"
        })
        total_score += 3

    # Check 4: Titanium + tight tolerance
    if features.get("material_type") == "Titanium" and features.get("tolerance_grade") in ["High", "Ultra-High"]:
        risks.append({
            "severity": "HIGH",
            "icon": "🔴",
            "issue": "Titanium + tight tolerance — extremely slow machining with high tool wear",
            "impact": "5–10× slower than Aluminum at same tolerance",
            "suggestion": "Consider alternative material or relaxed tolerance"
        })
        total_score += 3

    # Check 5: Very low quantity with complex setup
    if features.get("quantity", 1) == 1 and len(identified_processes) >= 2:
        risks.append({
            "severity": "MEDIUM",
            "icon": "🟡",
            "issue": "Single-unit order with multi-process setup — setup cost dominates total",
            "impact": f"Setup accounts for ~{int(features.get('setup_pct', 30))}% of total cost",
            "suggestion": "Consider ordering qty ≥ 5 to amortize setup"
        })
        total_score += 2

    # Risk classification
    if total_score >= 6:
        overall = "High Risk 🔴"
    elif total_score >= 3:
        overall = "Moderate Risk 🟡"
    else:
        overall = "Low Risk 🟢"

    return risks, total_score, overall
```

### Output

```
⚠️ Manufacturability Assessment:

  Overall Risk Score: 6.2 / 10 (Moderate 🟡)

  🔴 HIGH:  Deep holes (25mm) — may require peck drilling
            └ Suggestion: Reduce hole depth to ≤20mm

  🟡 MEDIUM: 3 manufacturing processes — part needs re-fixturing
             └ Suggestion: Redesign to reduce process count

  🟢 LOW:   Steel is widely available and well-understood
  🟢 LOW:   Volume within standard CNC envelope

  "This part is manufacturable but has elevated drilling complexity.
   Address the HIGH risk items to improve reliability and reduce cost."
```

### Why It Wins

Goes beyond cost and time — shows **manufacturing feasibility**. This is real DFM intelligence. The risk score runs before the quote, so the engineer sees warnings upfront.

---

## ⭐ Differentiator 8 — Quote Version Comparison

**PS2 mapping:** *"What-if design change impact"* — showing a before/after diff is the most direct way to demonstrate impact.

### What It Does

When the user modifies inputs (via what-if or new quote), shows a **side-by-side diff** of the old vs new quote.

### How It Works

```python
# Store every quote in session state
if "quote_history" not in st.session_state:
    st.session_state.quote_history = []

# After each quote prediction
st.session_state.quote_history.append({
    "version": len(st.session_state.quote_history) + 1,
    "features": features.copy(),
    "breakdown": breakdown.copy(),
    "total": total_cost,
    "timestamp": datetime.now()
})

# Render comparison if multiple versions exist
if len(st.session_state.quote_history) >= 2:
    v1 = st.session_state.quote_history[-2]
    v2 = st.session_state.quote_history[-1]
    render_quote_diff(v1, v2)
```

### Output

```
📊 Quote Comparison: v1 vs v2

                    v1 (Original)     v2 (After DFM)     Change
  ─────────────────────────────────────────────────────────────
  Material        :    ₹2,100            ₹1,480          −₹620 ↓
  Drilling        :      ₹980              ₹520          −₹460 ↓
  Milling         :    ₹1,120            ₹1,120              —
  Grinding        :      ₹700                ₹0          −₹700 ↓ (removed)
  Setup           :      ₹480              ₹380          −₹100 ↓
  Overhead        :      ₹420              ₹350           −₹70 ↓
  ─────────────────────────────────────────────────────────────
  TOTAL           :    ₹5,800            ₹3,850        −₹1,950 ↓ (34% savings)

  Changes Made: Steel→Aluminum, Holes 6→4, Tolerance High→Standard
```

### Why It Wins

Makes the impact of every design decision **quantifiable and visual**. The engineer can see exactly which component changed and by how much. Low effort — just session state + a diff table.

---

## ⭐ Differentiator 9 — AI-Generated Quote Narrative

**PS2 mapping:** *"Explainable AI showing top cost drivers"* — a plain-English paragraph is the most accessible form of explanation.

### What It Does

Generates a **plain-English paragraph** explaining the entire quote — readable by a non-technical stakeholder (project manager, procurement lead).

### How It Works

```python
def generate_quote_narrative(features, breakdown, confidence, dfm_suggestions, time_estimate):
    """Template-based narrative generation — no LLM needed"""

    # Identify top cost driver
    cost_components = {
        "material": breakdown["material"],
        "machining": breakdown["machining_total"],
        "setup": breakdown["setup"],
        "overhead": breakdown["overhead"]
    }
    top_driver = max(cost_components, key=cost_components.get)
    top_pct = cost_components[top_driver] / breakdown["total"] * 100

    # Identify top machining process
    process_costs = {p: breakdown[p] for p in breakdown.get("processes", {})}
    top_process = max(process_costs, key=process_costs.get) if process_costs else None

    # Build narrative
    narrative = (
        f"This {features['material_type']} part with {features['num_holes']} drilled holes "
        f"and {features['num_pockets']} milled pockets is estimated at "
        f"₹{breakdown['total']:,.0f} per unit for a batch of {features['quantity']}. "
        f"The largest cost contributor is {top_driver} ({top_pct:.0f}%)"
    )

    if top_process:
        narrative += (
            f", driven primarily by {top_process} "
            f"(₹{process_costs[top_process]:,.0f})."
        )

    if dfm_suggestions:
        top_dfm = dfm_suggestions[0]
        narrative += (
            f" To reduce cost, the most effective change would be: "
            f"{top_dfm['change']} (saves ₹{top_dfm['savings']:,.0f})."
        )

    narrative += (
        f" The quote confidence is {confidence}% — "
        f"{'high reliability' if confidence >= 85 else 'moderate coverage' if confidence >= 60 else 'limited coverage'} "
        f"for this feature combination."
    )

    if time_estimate:
        narrative += f" Estimated manufacturing time is {time_estimate:.1f} hours per unit."

    return narrative
```

### Output

```
📝 Quote Summary (Plain English):

  "This Steel part with 6 drilled holes and 2 milled pockets is estimated
   at ₹5,800 per unit for a batch of 5. The largest cost contributor is
   machining (48%), driven primarily by Drilling (₹980). To reduce cost,
   the most effective change would be: Switch from Steel → Aluminum
   (saves ₹620). The quote confidence is 79% — moderate coverage for
   this feature combination. Estimated manufacturing time is 4.2 hours
   per unit."
```

### Why It Wins

Makes the quote **accessible to everyone** — not just engineers. A project manager or procurement lead can read it without understanding SHAP plots or cost trees. Template-based, no LLM dependency.

---

## ⭐ Differentiator 10 — Similar Parts Finder

**PS2 mapping:** *"Clear feature-wise and process-wise cost contribution (transparent pricing)"* — adds benchmarking context.

### What It Does

After quoting, shows the **3 most similar parts** from the training dataset and their costs — gives the engineer contextual benchmarking.

### How It Works

```python
from sklearn.neighbors import NearestNeighbors

def find_similar_parts(X_new, X_train, y_train_total, feature_names, k=3):
    """Find k most similar parts from training data using k-NN"""
    # Normalize features for fair distance calculation
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_new_scaled = scaler.transform(X_new)

    nn = NearestNeighbors(n_neighbors=k, metric="euclidean")
    nn.fit(X_train_scaled)
    distances, indices = nn.kneighbors(X_new_scaled)

    similar_parts = []
    for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
        similarity = max(0, int((1 - dist / 10) * 100))  # normalize to percentage
        similar_parts.append({
            "rank": i + 1,
            "index": idx,
            "cost": y_train_total[idx],
            "similarity": similarity,
            "features": {fn: X_train[idx, j] for j, fn in enumerate(feature_names)}
        })

    return similar_parts
```

### Output

```
📋 Similar Parts in Database:

  #1  Part #0047  (Steel, 4 holes, 1 pocket, Standard tol.)
      Cost: ₹3,900  |  Similarity: 87%

  #2  Part #0123  (Steel, 8 holes, 2 pockets, High tol.)
      Cost: ₹6,400  |  Similarity: 79%

  #3  Part #0291  (Aluminum, 6 holes, 2 pockets, High tol.)
      Cost: ₹4,100  |  Similarity: 74%

  "Your part (₹5,800) falls between Part #0047 and #0123.
   The estimate aligns with the expected range for this geometry class."
```

### Why It Wins

Adds **trust and context**. The engineer sees the estimate isn't arbitrary — it's consistent with similar parts. Also strengthens the confidence range (if similar parts exist, confidence is higher). Uses `sklearn.neighbors` — ~15 lines.

---

## ⭐ Differentiator 11 — Cost Heatmap on 3D Model

**PS2 mapping:** *"Clear feature-wise and process-wise cost contribution (transparent pricing)"* — visualized directly on the part geometry.

### What It Does

Renders the uploaded 3D model with **color-coded regions** showing which areas of the part contribute most to manufacturing cost.

### How It Works

```python
import trimesh
import numpy as np

def render_cost_heatmap(mesh, features, breakdown):
    """Color mesh faces by estimated cost contribution region"""
    face_colors = np.ones((len(mesh.faces), 4)) * [0.5, 0.8, 0.5, 1.0]  # default green (low cost)

    # Identify high-cost regions heuristically
    face_normals = mesh.face_normals
    face_centers = mesh.triangles_center

    # Hole regions: faces with normals pointing inward near cylindrical features
    # (approximate: faces with high curvature near hole-sized geometry)
    for i, (center, normal) in enumerate(zip(face_centers, face_normals)):
        # Near bottom/top of part → setup/fixturing cost
        z_range = mesh.bounds[1][2] - mesh.bounds[0][2]
        z_normalized = (center[2] - mesh.bounds[0][2]) / z_range

        # High curvature regions → machining cost
        if is_high_curvature_region(mesh, i):
            cost_intensity = breakdown["machining_total"] / breakdown["total"]
            face_colors[i] = [0.9, 0.2, 0.2, 1.0]  # red = expensive

        # Interior surfaces → drilling/milling cost
        elif is_interior_surface(mesh, i):
            face_colors[i] = [0.9, 0.6, 0.1, 1.0]  # orange = moderate

    mesh.visual.face_colors = (face_colors * 255).astype(np.uint8)

    # Render to PNG for embedding in Streamlit
    scene = trimesh.Scene(mesh)
    png_data = scene.save_image(resolution=(800, 600))
    return png_data
```

### Output

```
[3D Model Rendered in Streamlit with cost coloring]

  🔴 Red regions:    High-cost areas (holes, pockets) — ₹2,800 machining
  🟡 Yellow regions: Moderate-cost areas (surfaces requiring finishing)
  🟢 Green regions:  Low-cost areas (flat surfaces, minimal machining)

  Legend:
    ← Cheap                                    Expensive →
    🟢─────────🟡─────────🟠─────────🔴

  "62% of machining cost is concentrated in the red zones.
   Simplifying these features would yield the highest savings."
```

### Why It Wins

The **most visual differentiator** in the entire system. Judges see cost mapped directly onto the 3D part — no abstraction needed. No other team will render a cost-colored 3D model. Uses `trimesh` which is already in the stack.

> **Note:** The face-to-cost mapping is heuristic (based on curvature and geometry analysis), not exact. This is acceptable for a hackathon demonstration and honest to acknowledge.

---

## Tech Stack

| Layer              | Tool                                 |
| ------------------ | ------------------------------------ |
| CAD parsing (STL)  | `trimesh`                          |
| CAD parsing (STEP) | `cadquery` / `ifcopenshell`      |
| ML Model           | `scikit-learn` RandomForest        |
| Explainability     | `shap` (per-quote) + `.feature_importances_` (global) |
| Similar Parts      | `sklearn.neighbors` NearestNeighbors |
| UI + Chat          | `Streamlit`                        |
| PDF Export         | `fpdf2` + `matplotlib` (charts)  |
| Visualization      | `matplotlib` / `plotly` (Sankey, heatmap, curves) |
| 3D Rendering       | `trimesh` (cost heatmap + thumbnail) |
| Dataset            | Synthetic (Python formulas — non-linear, cost + time) |
| Language           | Python 3.x                           |

---

## Execution Timeline

| Days  | Focus                                                                                               |
| ----- | --------------------------------------------------------------------------------------------------- |
| 1–2  | Geometry extraction (trimesh auto-features), process routing, manufacturability risk rules          |
| 3–4  | Synthetic dataset (1,000+ rows, non-linear formulas, 7 cost + 4 time columns per-process)          |
| 5–6  | 7 cost + 4 time sub-models trained, 5-fold CV validation, model validation dashboard               |
| 7–8  | Streamlit UI + full chat agent flow (contextual intelligence + edge cases + real-time cost ticker)  |
| 9     | Cost + time breakdown, Sankey diagram, cost heatmap on 3D model, similar parts finder              |
| 10    | Explainability (SHAP waterfall + global importances), AI quote narrative                            |
| 11    | Diff 1: DFM rules engine + what-if simulator + tolerance-cost curve + break-even quantity          |
| 12    | Diff 2: confidence range + visual gauge + uncertainty explanation + quote version comparison        |
| 13    | Feedback loop (accuracy impact), professional PDF (charts + Sankey + heatmap), polish all panels   |
| 14    | Full demo dry run, finalize Round 2 PPT, scalability narrative                                     |

---

## Minimum Viable Version (if time is short)

Protect this order strictly:

1. Geometry extraction working on a sample STL (auto-features only)
2. Synthetic dataset with 7 cost + 4 time columns (per-process, non-linear formulas)
3. 7 cost sub-models + 4 time sub-models trained (each process genuinely predicted)
4. Chat agent collecting material / quantity / tolerance with contextual responses
5. Quote displayed with genuine process-wise cost + time breakdown
6. DFM suggestions (at least top 4 rules with ₹ savings + hours saved)
7. Cost Sankey diagram (transparent cost flow visualization)

**Layer 2 (high impact, low effort):**
8. Tolerance-cost curve + Break-even quantity analysis
9. Quote narrative (plain-English summary)
10. Similar parts finder
11. Quote version comparison

**Layer 3 (wow factor):**
12. Cost heatmap on 3D model
13. Manufacturability risk score
14. SHAP waterfall + confidence gauge

Everything else stacks on top of this core.

---

## What the Judges See

| Module                               | Skill Demonstrated                          |
| ------------------------------------ | ------------------------------------------- |
| Geometry extraction (honest)         | CAD understanding + intellectual honesty    |
| Process routing + risk assessment    | Real manufacturing workflow + feasibility   |
| 7 cost + 4 time sub-models           | AI capability + engineering rigor           |
| Process-wise cost + time breakdown   | L&T-level quoting transparency             |
| Cost Sankey diagram                  | Best-in-class cost flow visualization       |
| Cost heatmap on 3D model             | Unprecedented visual transparency           |
| SHAP waterfall + global importances  | Dual-layer AI explainability                |
| AI quote narrative                   | Accessible to non-technical stakeholders    |
| Similar parts benchmarking           | Trust through contextual comparison         |
| What-if simulator + tolerance curve  | PS2 "what-if" fully realized, interactive   |
| Break-even quantity analysis         | Production planning intelligence            |
| DFM rules engine (₹ + hours saved)  | Actionable design + time intelligence       |
| Quote version comparison             | Design iteration impact tracking            |
| Manufacturability risk score         | Pre-quote feasibility assessment            |
| Chat agent with domain knowledge     | Production-ready UX + manufacturing advisor |
| Confidence gauge + uncertainty why   | Industrial maturity + ML risk communication |
| Feedback loop with impact tracking   | Scalability + continuous improvement proof  |
| Model validation dashboard           | ML rigor + credibility                      |
| Professional PDF with charts         | Real-world deployment thinking              |

---

## One-Line Summary of Each Differentiator

| # | Differentiator | One-Line Summary | PS2 Requirement |
|---|---|---|---|
| 1 | **DFM + What-If** | *How to reduce the cost* | What-if impact + DFM suggestions |
| 2 | **Confidence Range** | *How much to trust the cost* | Explainable AI |
| 3 | **Cost Sankey** | *Trace every rupee from input to output* | Transparent pricing |
| 4 | **Tolerance–Cost Curve** | *See the full cost landscape for precision choices* | What-if impact |
| 5 | **Break-Even Quantity** | *Know how many to order* | DFM suggestions |
| 6 | **Manufacturing Time** | *Not just cost — also how long* | Reduce machining time |
| 7 | **Manufacturability Risk** | *Flag problems before they become expensive* | DFM insights |
| 8 | **Quote Comparison** | *See exactly what changed and by how much* | What-if impact |
| 9 | **Quote Narrative** | *Anyone can understand the quote* | Explainable AI |
| 10 | **Similar Parts** | *This price makes sense because...* | Transparent pricing |
| 11 | **Cost Heatmap** | *See where the money goes on the actual part* | Transparent pricing |

All 11 differentiators map directly to PS2 objectives. None stray outside scope. Together they make judges say **"this team actually thought about every angle."**

---
