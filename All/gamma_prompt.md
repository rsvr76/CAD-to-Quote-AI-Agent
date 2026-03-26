# Gamma Prompt — CAD-to-Quote AI Agent (PIVOT Round 2)

> **Gamma Instructions:** Paste each slide section using "Paste in text". Keep bullets SHORT (max 8–10 words each). Where you see [VISUAL], add a diagram/chart/screenshot in Gamma. Use a clean dark professional theme. Min 18pt body font.

---

# TITLE (not counted)

## Slide 0 — Title

**[YOUR TEAM NAME]**
PS2: CAD-to-Quote AI Agent

*Instant, transparent manufacturing quotes from 3D part data*

PIVOT Innovation Challenge · Round 2 · Product Development Centre, L&T

---

# SECTION 4.1 — PROBLEM & CONTEXT (~3 min)

## Slide 1 — The Problem

**Manufacturing Quoting Is Broken**

- Manual quoting takes **hours to days** per part
- Engineers get only a final ₹ number — no reasoning
- Estimator knowledge is tribal — not scalable
- No cost feedback while design is still flexible
- Every quote is a one-off manual effort

[VISUAL: Icon grid showing the 4 pain points — clock, black box, person bottleneck, locked design]

---

## Slide 2 — Why It Matters

**The Real Cost of Slow Quotes**

[VISUAL: 4 impact cards side-by-side]

| Impact | Problem |
|---|---|
| 🕐 Design Stalls | Engineers wait days for cost signals |
| 🔒 DFM Too Late | Avoidable cost gets locked into design |
| 📋 Procurement Bottleneck | RFQs pile up at estimation desk |
| ❓ No Feature-Level Insight | Can't tell which feature drives cost |

> **15–30% of manufacturing cost** could be avoided with earlier feedback

---

## Slide 3 — What Industry Needs

**The Gap We Fill**

- Quotes in **seconds**, not days
- **Transparent breakdown** — not just a number
- **Process-level attribution** — which operation costs how much
- **DFM suggestions** with ₹ savings attached
- Feedback at **design stage** — before it's too late

[VISUAL: Before/After comparison — "Manual: 2 days, opaque" vs "AI Agent: 30 sec, transparent"]

---

# SECTION 4.2 — PROPOSED SOLUTION (~3 min)

## Slide 4 — Our Solution

**CAD-to-Quote AI Agent**

An AI-driven quoting system that produces:

- ✅ 4-component cost breakdown (Material · Machining · Setup · Overhead)
- ✅ Confidence range (₹ low–high band)
- ✅ Per-quote explainability (SHAP + Formula + Routing)
- ✅ Actionable DFM suggestions with ₹ savings
- ✅ PDF-ready export

Software-only · No hardware · Works on STEP CAD files

[VISUAL: Product screenshot — dashboard overview]

---

## Slide 5 — Pipeline at a Glance

**7 Steps — Upload to Quote**

[VISUAL: Horizontal pipeline flow diagram with icons]

1. 📤 **CAD Upload** — STEP file or sample part
2. 📐 **Geometry Extraction** — Volume, area, bbox, features
3. ✏️ **Input Collection** — Material, qty, tolerance, holes
4. ⚙️ **Process Routing** — Turning / Milling / Drilling / Grinding
5. 🤖 **ML Prediction** — Machining time (17 features → minutes)
6. 💰 **Cost Calculation** — Material + Machining + Setup + Overhead
7. 📊 **Dashboard** — Breakdown, SHAP, DFM, PDF export

---

## Slide 6 — vs. Conventional Methods

**Why This Is Better**

[VISUAL: Comparison table with green/red indicators]

| Aspect | Manual Estimation | Our AI Agent |
|---|---|---|
| Speed | ❌ Hours–days | ✅ < 30 seconds |
| Transparency | ❌ Final number only | ✅ Full breakdown |
| DFM Feedback | ❌ Post-production | ✅ At design stage |
| Consistency | ❌ Varies by estimator | ✅ Deterministic |
| Explainability | ❌ None | ✅ 3 layers |

**Key differentiator:** ML predicts **time**, not cost — rates change without retraining

---

# SECTION 4.3 — TECHNICAL APPROACH (~5 min)

## Slide 7 — Architecture

**System Architecture**

[VISUAL: Block diagram — full slide, minimal text]

```
Engineer
   ↓
┌─────────────────────────┐
│  AI Quote Agent          │
│  (Orchestrator)          │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  CAD Analyzer            │
│  (OpenCascade / STEP)    │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  Process Routing (Rules) │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  ML Predictor (RF-17)    │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  Cost Engine (Formulas)  │
└─────────┬───────────────┘
          ↓
┌─────────────────────────┐
│  SHAP + DFM + Dashboard  │
└─────────────────────────┘
```

**Stack:** FastAPI · Python · Jinja2 · Tailwind · SHAP · scikit-learn

---

## Slide 8 — ML Model

**Random Forest → Machining Time**

[VISUAL: Feature vector diagram showing 4 groups flowing into RF model]

| Group | Features | # |
|---|---|---|
| Geometry | volume, area, aspect ratio, SV ratio, slenderness, pocket density | 6 |
| User Inputs | holes, pockets, depth, material, tolerance | 5 |
| Routing | turning, milling, drilling, grinding flags | 4 |
| Derived | complexity_score, drilling_work | 2 |

**Total: 17 features → 1 output (minutes)**

- Synthetic training: 5,000 rows · R² ≥ 0.95 target
- SHAP TreeExplainer for per-quote explanations
- Real vendor data is a drop-in replacement

---

## Slide 9 — Cost Formulas

**4 Deterministic Components**

[VISUAL: 4 cards with formula + icon for each]

| Component | Formula |
|---|---|
| 🧱 **Material** | weight × price/kg × batch_discount |
| ⚙️ **Machining** | ML_time × machine_rate/hr |
| 🔧 **Setup** | max(2000/√qty, ₹200) |
| 📦 **Overhead** | subtotal × overhead_rate% |

- Batch discount: qty 1–9 (0%) · 10–50 (10%) · 51–200 (20%) · 201+ (30%)
- Overhead by material: Al 12% · Steel 15% · Ti 22%
- Machine rates: 3-Axis ₹1,000/hr · 5-Axis ₹1,800/hr

---

## Slide 10 — Explainability & DFM

**3 Explanation Layers + DFM Suggestions**

[VISUAL: Left half = 3-layer explanation cards, Right half = DFM savings table]

**Explainability:**

| Layer | Answers | Method |
|---|---|---|
| SHAP | "Why 7.5 min?" | ML introspection |
| Formula | "How ₹12,200?" | Show calculation |
| Routing | "Why Grinding?" | Show rule + threshold |

**DFM Suggestions (ranked by ₹ savings):**

| Change | Saves |
|---|---|
| Relax tolerance | ₹2,400 |
| Reduce holes 6→4 | ₹560 |
| Switch to Aluminium | ₹340 |
| Simplify pockets | ₹180 |

---

# SECTION 4.4 — IMPLEMENTATION & DEMO (~5 min)

## Slide 11 — What We've Built

**Implementation Status**

[VISUAL: Checklist with green/yellow indicators]

- ✅ 9 interactive frontend screens
- ✅ FastAPI backend with modular architecture
- ✅ Process routing engine with warnings
- ✅ 4-component cost calculation engine
- ✅ DFM suggestion engine with re-prediction
- ✅ Confidence intervals and risk classification
- ✅ 17-feature ML schema designed
- ⏳ ML model training (placeholder active)
- ⏳ Real STEP parsing (samples simulate output)

---

## Slide 12 — Live Demo Walkthrough

**Steel Bracket — 9 Screens**

[VISUAL: Screenshot carousel or grid of all 9 screens]

1. **Landing** → Select Steel Bracket sample
2. **Geometry** → Volume, area, bbox, faces
3. **Input** → 6 holes · Steel · Qty 50 · Fine tolerance
4. **Routing** → Milling ✅ · Drilling ✅ · Grinding ✅ · Turning ❌
5. **Stock** → Rectangular block · 2.04 kg
6. **Progress** → 7-step AI pipeline animation
7. **Dashboard** → ₹28,400 · Full breakdown · SHAP · DFM
8. **DFM** → Original vs. Optimized side-by-side
9. **Export** → PDF-ready quote summary

---

## Slide 13 — Round 1 → Round 2 Progress

**What Changed**

[VISUAL: Before/After comparison columns]

| Round 1 | Round 2 |
|---|---|
| Problem statement | 13-step pipeline architecture |
| High-level concept | 9 backend modules designed |
| No code | Working web app (9 screens) |
| No UI | Professional dark-theme dashboard |
| No DFM | DFM view with ₹ savings |
| No explainability | 3-layer explainability |

---

# SECTION 4.5 — BENEFITS & ROADMAP (~2 min)

## Slide 14 — Impact & KPIs

**Expected Benefits**

[VISUAL: KPI cards with before/after metrics]

| Metric | Before | After |
|---|---|---|
| Quote time | Hours–days | < 30 sec |
| Transparency | ❌ None | ✅ Full breakdown |
| DFM timing | Post-production | Design stage |
| Estimator need | Senior expert | Automated |

**Honest Limitations:**
- ML currently uses formula placeholder
- STEP parsing simulated via samples
- Costs use representative rates (configurable)

---

## Slide 15 — Roadmap & Close

**What's Next**

[VISUAL: Horizontal timeline with 4 phases]

| Phase | Scope |
|---|---|
| ✅ **Done** | Full UI · Cost engine · Routing · DFM |
| 🔜 **Short** (2–4 wks) | Train RF · SHAP · STEP parsing |
| 📈 **Medium** (3–6 mo) | Vendor data · ERP integration |
| 🚀 **Long** (6–12 mo) | Retraining · Supplier optimization |

> **From CAD geometry to a transparent, explainable quote — in seconds.**

**Thank you. We're ready for your questions.**

---

# BACKUP SLIDES (not counted)

## Backup B1 — Routing Rules Detail

[VISUAL: Table with color-coded ON/OFF examples]

| Process | Condition | Rationale |
|---|---|---|
| Turning | aspect_ratio > 2.0 | Elongated → lathe |
| Milling | pockets > 0 OR area > 200 | Pockets → mill |
| Drilling | holes > 0 | Holes → drill |
| Grinding | Fine or Ultra-Fine | Tight tolerance → finish |

---

## Backup B2 — Cost Assumptions

- Material: Al ₹220 · Steel ₹85 · Brass ₹450 · Ti ₹3,200 · ABS ₹150 per kg
- Machines: VMC ₹1,000 · 5-Axis ₹1,800 · Lathe ₹1,200 · Grinder ₹900 per hr
- All configurable — not hardcoded

---

## Backup B3 — Synthetic Data Justification

- Real vendor quotes unavailable during hackathon
- Physics-based generation: time ∝ volume × machinability + holes × depth + noise
- Pipeline accepts real data as drop-in replacement
- Target: R² ≥ 0.95, MAPE ≤ 8%

---

## Backup B4 — Risks & Mitigations

| Risk | Mitigation |
|---|---|
| Synthetic ≠ real | Supports vendor data ingestion |
| Stock approximation | Engineer override + audit |
| No STEP demo | OpenCascade designed; samples simulate |
| SHAP interpretation | 3 separate layers prevent confusion |
