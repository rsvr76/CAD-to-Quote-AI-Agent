# Abstract — PS2: CAD-to-Quote AI Agent

**Event:** PIVOT Innovation Challenge
**Problem Statement:** PS2 — Costing Automation: CAD-to-Quote AI Agent

---

Manufacturing cost estimation is a critical bottleneck in product development. Engineers rely on manual, vendor-dependent quotation processes that take hours to days, producing opaque cost figures with no breakdown, no design feedback, and no basis for cost-informed decision-making at the design stage.

We propose a **CAD-to-Quote AI Agent** — a chat-driven web application that converts a 3D CAD model into a complete, transparent manufacturing cost quote in under 30 seconds. The engineer uploads a CAD file, answers three guided inputs (material, quantity, tolerance), and receives an itemized quote instantly.

The system extracts geometric features from the CAD file automatically, routes the part to applicable manufacturing processes (turning, milling, drilling, grinding) using rule-based logic, and predicts cost using four independent Random Forest Regression models — one each for material, machining, setup, and overhead. Machining cost is further split by process, delivering both feature-wise and process-wise cost transparency. A feedback loop appends confirmed quotes to the training data, enabling continuous accuracy improvement over time.

Two key differentiators distinguish this system: a **Design Optimization Engine** that recommends specific design changes with projected cost savings (e.g., "Reduce holes from 6 → 4: saves ₹420"), and a **Quote Confidence Range** derived from model variance (e.g., ₹5,420 – ₹6,180 at 79% confidence) — communicating quote reliability the way real industrial systems do.

This solution reduces quote turnaround from days to seconds, equips engineers with actionable cost intelligence at the design stage, and delivers a transparent, explainable, and continuously improving manufacturing quotation platform.

---

*Word count: ~246 words*

---

## 1. Problem Understanding

In modern manufacturing environments, cost estimation remains one of the most critical and time-consuming steps in the product development cycle. When a design engineer completes a 3D CAD model, determining its manufacturing cost requires routing the design through vendors or internal costing teams, waiting for manual quotations, and receiving a final number — often without a transparent breakdown or justification. This process typically spans several hours to multiple days, introducing significant delays in design decisions, procurement planning, and project timelines.

The deeper problem is not merely the time taken, but the opacity of the result. Engineers receive a cost figure with no visibility into which design attributes are responsible — whether it is the choice of material, the number and depth of drilled holes, the complexity introduced by tight tolerances, or the number of manufacturing setups required. Without this visibility, engineers have no basis to make cost-informed design decisions at the stage when changes are cheapest and most impactful. Cost optimization is left as an afterthought rather than a design input.

Additionally, there is no feedback mechanism for engineers to understand how alternative design choices would affect cost. A quote arrives as a static number, not as an actionable decision-support tool. This limits the application of Design for Manufacturability (DFM) principles and results in higher manufacturing costs that could have been avoided at the design stage.

The goal of PS2 is to eliminate this gap by building an AI-powered agent that converts a 3D CAD model directly into an instant, transparent, and explainable manufacturing cost quote — one that not only tells the engineer what the cost is, but why, and what to do about it.

---

## 2. Proposed Solution

We propose the **CAD-to-Quote AI Agent** — an intelligent, chat-driven web application that enables an engineer to upload a 3D CAD file, respond to a concise set of guided inputs, and receive a complete, itemized manufacturing cost quote within 30 seconds.

The system is built around three core principles:

- **Transparency** — every rupee in the quote is accounted for, broken down by cost component and by manufacturing process
- **Actionability** — the engineer receives specific, quantified design recommendations to reduce cost before manufacturing begins
- **Reliability** — the quote is accompanied by a statistical confidence range, not just a single number, so the engineer knows how much to trust it

### System Workflow

The end-to-end workflow of the system proceeds as follows:

**Step 1 — CAD Upload and Geometry Extraction:**
The engineer uploads a 3D part file in STL or STEP format. The system automatically extracts quantitative geometric properties — volume, surface area, bounding box dimensions, face count, aspect ratio, and geometry validity. For STEP files, manufacturing-specific features such as hole count, pocket identification, and fillet geometry are extracted directly from the part topology. For STL files, the chat agent supplements the automatic extraction with a small number of targeted user inputs.

**Step 2 — Conversational Input Collection:**
The AI agent engages the engineer in a guided conversational interface, collecting three essential manufacturing parameters: intended material (e.g., Aluminum, Steel, Titanium), required production quantity, and precision tolerance grade (Standard, High, or Ultra-High). These inputs, combined with the extracted geometry, form the complete feature vector used for cost prediction.

**Step 3 — Process Routing:**
A rule-based process routing engine evaluates the feature vector and identifies the applicable manufacturing processes for the part. Cylindrical geometry routes to CNC Turning; pocket features route to Milling; hole features route to Drilling; high-tolerance requirements trigger Grinding. This mirrors the decision logic applied by an experienced process engineer reviewing a drawing, and requires no machine learning.

**Step 4 — Multi-Model Cost Prediction:**
Four independent Random Forest Regression models — one for each cost component — predict the cost of Material, Machining, Setup, and Overhead independently. The machining cost is further distributed across the identified processes (drilling, milling, turning, grinding) based on their respective computational weights. The total quote is the sum of four genuinely predicted components, not a single black-box output with post-hoc ratio splits.

**Step 5 — Cost Breakdown and Process-wise Contribution:**
The output presents a structured breakdown showing each cost component in both absolute and percentage terms, with machining further split by process. This delivers both the feature-wise and process-wise cost contribution explicitly required by the PS.

**Step 6 — Explainability Engine:**
The system surfaces the top cost-driving design features in ranked order, quantifying each driver in rupee terms and explaining the engineering reason behind it (e.g., "6 deep holes contribute ₹810, accounting for 22% of total cost due to extended drilling cycle time"). This allows engineers to immediately identify what is making the part expensive.

**Step 7 — Design Optimization (Differentiator 1):**
Rather than only reporting the current cost, the system simulates targeted design modifications — reducing hole count, simplifying pocket geometry, switching material, or relaxing tolerance — and presents a ranked list of recommendations each with its projected savings and a revised total cost estimate. This converts the system from a passive cost calculator into an active design advisory platform, enabling engineers to make cost-informed design decisions before committing to manufacturing.

**Step 8 — Quote Confidence Range (Differentiator 2):**
The system computes the statistical variance across the predictions of all individual decision trees within each Random Forest model and derives a confidence range around the central estimate (e.g., ₹5,800 estimated cost, ₹5,420–₹6,180 range at 79% confidence). This provides a quantified measure of quote reliability — a capability explicitly absent from conventional manual quotation processes and representative of how mature industrial quoting systems communicate risk.

**Step 9 — PDF Export:**
The complete output — cost breakdown, process-wise contribution, cost drivers, optimization suggestions, and confidence range — is packaged into a structured PDF quotation summary, ready for records or vendor communication.

**Step 10 — Feedback Loop:**
After each quote, the system prompts the engineer to confirm or correct the actual manufacturing cost. Verified entries are appended to the training dataset and used to periodically retrain the models, enabling continuous accuracy improvement as real-world quotation data accumulates over time.

---

## 3. Approach and Technical Framework

The system is implemented entirely in Python using the following technology stack:

| Layer                 | Technology                                               |
| --------------------- | -------------------------------------------------------- |
| CAD Parsing (STL)     | `trimesh`                                              |
| CAD Parsing (STEP)    | `cadquery`                                             |
| Machine Learning      | `scikit-learn` — RandomForestRegressor                |
| Explainability        | Feature importances + SHAP values                        |
| User Interface + Chat | `Streamlit`                                            |
| PDF Generation        | `fpdf2`                                                |
| Training Data         | Synthetic dataset generated from machining cost formulas |

The training dataset is generated programmatically using standard machining cost formulas, with ±5% noise added per record to simulate real-world cost variability. Each record stores four independent cost labels, enabling each sub-model to learn the cost dynamics of its specific component. The dataset is designed to be replaced or augmented with real historical quotation data as the system is deployed in a production environment.

The architecture is modular — each layer operates independently and can be upgraded without affecting the others. The process routing engine can be extended to include additional manufacturing processes. The ML models can be swapped for more sophisticated algorithms as data volume grows.

---

## 4. Expected Outcome and Practical Usefulness

The proposed system delivers a complete manufacturing cost quote — with structured cost breakdown, process-wise contribution, ranked cost drivers, design optimization recommendations, statistical confidence range, and PDF export — in under 30 seconds from CAD upload.

For **design engineers**, the system provides immediate cost feedback at the design stage, enabling DFM decisions before designs are committed — reducing unnecessary rework and revision cycles.

For **procurement engineers**, it provides a structured, verifiable, and fast first estimate that can accelerate vendor selection and negotiation.

For **manufacturing organizations**, it delivers a consistent, auditable, and data-driven quotation baseline that improves continuously with accumulated data.

The two differentiators — **Design Optimization** (telling the engineer how to reduce the cost) and **Quote Confidence Range** (telling the engineer how much to trust the cost) — together elevate this system beyond a conventional cost estimator into a manufacturing intelligence platform. Both are directly grounded in the PS requirements and aligned with real industrial quoting workflows.

In a production deployment, the system is designed to integrate with PLM and ERP infrastructure, ingest historical quotation records, and scale across diverse component categories and manufacturing processes. This solution provides fast, transparent, and actionable cost intelligence at the earliest and most impactful stage of the engineering workflow.
