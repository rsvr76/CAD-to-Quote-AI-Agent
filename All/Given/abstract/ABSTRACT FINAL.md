# Abstract

## PS2 — CAD-to-Quote AI Agent: Instant Manufacturing Cost from 3D Models

**PIVOT Innovation Challenge**

---

**🔴 Problem**
Manufacturing cost estimation relies on slow, manual vendor quotation processes that take hours to days, produce opaque cost figures with no breakdown, and offer no design-stage feedback on cost or machining time — delaying engineering decisions and increasing avoidable costs.

**🟢 Solution**
We propose the **CAD-to-Quote AI Agent** — a chat-driven web application where an engineer uploads a 3D CAD model, provides three inputs (material, quantity, tolerance), and receives a complete, itemized manufacturing cost and time quote in under 30 seconds.

**🔵 Approach**
The system extracts geometric properties from the CAD file, identifies applicable processes (turning, milling, drilling, grinding) via rule-based routing, and predicts cost and machining time through seven independent Random Forest models — one each for material, four per-process machining costs, setup, and overhead. The output is a transparent, process-wise breakdown with per-quote explainability (SHAP), interactive cost flow visualization, a plain-English quote narrative, and a PDF-ready quotation summary.

**🟡 Innovation**
Beyond cost estimation, the system acts as a **design advisor**: a DFM rules engine recommends specific design changes with quantified savings in both rupees and machining hours, an interactive what-if simulator lets engineers explore tradeoffs live, and a confidence range with uncertainty explanation communicates quote reliability — capabilities absent from conventional quoting tools.

**⚪ Feasibility & Impact**
The entire system uses proven, lightweight Python libraries (scikit-learn, Streamlit, trimesh) with a synthetic training dataset — requiring no external dependencies, vendor data, or cloud infrastructure. This makes it fully implementable within the given timeline. The solution reduces quote turnaround from days to seconds, empowers engineers to make cost-informed design decisions before manufacturing commitment, and improves continuously through a built-in feedback loop.

---

**Word Count: ~247 words**
