# CAD-to-Quote AI Agent — Overall Strategy

---

## AI Agent Orchestration Layer

The system includes an AI-assisted orchestration layer (“AI Quote Agent”) that coordinates the quoting workflow.

### Architecture

```
User
  │
  ▼
┌──────────────────────┐
│   AI QUOTE AGENT      │
│   (Orchestrator)      │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   CAD Analyzer        │
│   (STEP/OpenCascade)  │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   Process Routing     │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   ML Machining Model  │
│   (Random Forest)     │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   Cost Engine         │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   Explainability      │
│   (SHAP + formulas)   │
└──────────────────────┘
          │
          ▼
┌──────────────────────┐
│   DFM Advisor         │
└──────────────────────┘
```

### Agent Workflow

The AI Quote Agent acts as a manufacturing assistant by orchestrating a predefined tool chain (with conditional pauses for missing human inputs and validation/error handling):

1. **Understand the task** — User uploads CAD, agent goal: generate manufacturing quote
2. **Collect missing information** — Agent asks: holes? material? tolerance?
3. **Call the correct tools** — geometry extractor, routing engine, ML model, cost calculator
4. **Combine results** — assemble full cost breakdown with uncertainty range
5. **Explain the quote** — SHAP waterfall, formula transparency, routing explanation
6. **Recommend improvements** — DFM suggestions with quantified savings

### Tool Chain

| Tool | Module | Purpose |
|---|---|---|
| CAD Analyzer | OpenCascade (pythonocc-core) | Parse STEP (.step/.stp) B-Rep and extract exact geometry + topology features |
| Process Routing Engine | Rules | Determine required machining processes |
| ML Machining Predictor | RandomForestRegressor | Predict machining time |
| Cost Engine | Formulas | Calculate material, setup, overhead costs |
| Explainability Module | SHAP + formulas | Explain cost drivers |
| DFM Advisor | Model re-prediction | Suggest design improvements with ₹ savings |

### One-Line Definition (for slides/judges)

> The CAD-to-Quote AI Agent orchestrates CAD analysis, machine-learning prediction, rule-based process planning, and cost modelling to generate transparent manufacturing quotes with design improvement suggestions.

### Why This Is an AI Agent (Not a Calculator)

The system performs a full decision workflow:

```
User request → Collect inputs → Analyze CAD → Predict machining (ML)
→ Calculate cost → Explain results → Recommend improvements
```

Three strong AI elements:
1. **Machine learning prediction** — RF predicts machining time
2. **Explainable AI** — SHAP per-quote waterfall
3. **Design recommendation engine** — DFM re-prediction with savings

Manufacturing quoting requires coordinating multiple specialized modules (CAD analysis, process planning, machining prediction, and cost modeling). The agent provides a unified orchestration layer that manages this workflow and interacts with the engineer when additional information is required.

### Updated Workflow (14 steps)

| Step | Title |
|---|---|
| 0 | AI Agent receives user request |
| 1 | CAD Upload |
| 2 | Geometry Extraction |
| 3 | Agent collects missing inputs |
| 4 | Process Routing |
| 5 | Stock Estimation |
| 6 | Stock Confirmation |
| 7 | Feature Vector Assembly |
| 8 | ML Machining Prediction |
| 9 | Prediction Interval |
| 10 | Cost Calculation |
| 11 | Explainability |
| 12 | DFM Suggestions |
| 13 | Final Quote |

---

## 1.1 Goal of the System

The system converts a CAD design into a transparent manufacturing cost quote in under 30 seconds (with a PDF-ready quote summary).

Instead of returning a black-box price, it provides:

- Material cost
- Machining cost
- Setup cost
- Overhead cost
- Machining uncertainty range
- Feature-level explanation (SHAP)
- Design-for-Manufacturing suggestions

It also provides:
- A PDF-ready quotation summary for sharing
- Process-wise machining contribution (shown as a clearly-labeled approximation derived from active routing flags)

The system acts as a **design feedback assistant**, not just a quoting tool.

---

## 1.2 Core Design Principles

The architecture follows three engineering principles:

### 1️⃣ Use ML only where necessary

Machine learning is used **only** for machining time prediction.
Other components follow deterministic formulas.

| Component | Method |
|---|---|
| Material cost | Formula |
| Machining time | Random Forest |
| Setup cost | Formula |
| Overhead | Rule |
| Process routing | Rules |
| DFM suggestions | Model re-prediction |

This avoids unnecessary ML complexity.

---

### 2️⃣ Separate explainability layers

The system separates three different explanations:

| Layer | Explains |
|---|---|
| ML (SHAP) | Why machining time changed |
| Formula transparency | How costs were calculated |
| Routing rules | Why processes were selected |

Mixing these explanations leads to incorrect interpretation.

---

### 3️⃣ Human-in-the-loop verification

Some manufacturing information still cannot be guaranteed from CAD alone.

Therefore the engineer confirms (human-in-the-loop):

- detected hole / pocket counts (and max depth if needed)
- material, quantity, tolerance
- raw stock weight (because real stock sizes and supplier constraints vary)

This improves reliability while keeping automation high.

---

## 1.3 Machine Learning Model

### Model Type

**RandomForestRegressor**

Chosen because:

- handles non-linear interactions
- robust on small datasets
- explainable using SHAP TreeExplainer
- minimal hyperparameter tuning

### ML Prediction Target

**machining_time** (minutes)

ML predicts time, not cost.
Cost is derived later using machine rate.

### Feature Categories

| Feature Type | Examples |
|---|---|
| Geometry | surface area, volume, aspect ratio |
| User inputs | holes, pockets, depth |
| Material | machinability |
| Routing flags | milling, drilling, turning |
| Derived | complexity_score, drilling_work |

**Total ML input features: 17**

### Why Quantity Is Not an ML Feature

Quantity does not affect machining time per part.
A single part takes the same machining time regardless of batch size.
Quantity only affects setup cost amortisation, which is handled by formula.

---

## 1.4 Synthetic Training Data

Real vendor quotes are unavailable during the hackathon.
A synthetic dataset is generated using machining relationships.

**Example generation formula:**

```
machining_time =
    base_cutting_time
  + hole_drilling_time
  + pocket_milling_time
  + tolerance_multiplier
  + Gaussian noise
```

**Dataset characteristics:**

| Parameter | Value |
|---|---|
| Rows | 5000 |
| Features | 17 |
| Train/Test | 80/20 |
| Target | machining_time |

**Expected performance:**

| Metric | Target |
|---|---|
| R² | ≥ 0.95 |
| MAPE | ≤ 8% |

The model pipeline is built so real vendor invoice data can replace synthetic data later without redesign.

---

## 1.5 Cost Model

The final quote contains four components.

### Material Cost

```
material_cost = stock_weight × price_per_kg × batch_discount
```

Material prices are stored in lookup tables.

### Machining Cost

```
machining_cost = machining_time × machine_rate
```

Machine rate used: **per-machine hourly rates** based on the final selected machine(s) (so changing the machine updates the machining cost).

### Setup Cost

```
setup_cost = max(2000 / √quantity, 200)
```

Large batches distribute setup cost.

### Overhead

```
overhead = (material + machining + setup) × overhead_rate
```

Rates vary by material.

---

## 1.6 Prediction Uncertainty

Random Forest contains many decision trees.
Each tree produces a prediction.

Prediction interval is computed using:

- **10th percentile**
- **90th percentile**

This creates a machining time uncertainty range.

> **Important:** The uncertainty applies only to machining cost, because other costs are deterministic.

---

## 1.7 DFM Suggestions

The system evaluates design improvements by:

1. Modifying one feature
2. Re-running the model
3. Measuring cost difference

**Example suggestions:**

| Suggestion | Reason |
|---|---|
| Reduce hole count | reduces drilling time |
| Relax tolerance | removes grinding |
| Reduce pocket complexity | reduces milling |
| Use aluminium instead of titanium | reduces machining + material |

Savings are ranked and shown to the engineer.
