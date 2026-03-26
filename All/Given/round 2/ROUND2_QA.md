# Round 2 Q&A Preparation

## Likely panel questions and strong answers

### 1. Why is this better than a normal formula-based costing sheet?

Because the system combines explicit engineering logic with a scalable prediction layer. Formula sheets are rigid and hard to maintain when multiple variables interact, especially material, quantity, tolerance, and geometry together. Our system preserves transparency while handling non-linear interactions more naturally.

### 2. Why use AI at all if you already know costing formulas?

The initial system uses engineering-grounded costing logic and synthetic data to establish a reliable baseline. AI becomes useful when cross-feature effects grow and when the system starts learning from real historical quotations over time. We are not replacing engineering rules; we are augmenting them.

### 3. How do you extract manufacturing features from CAD?

At minimum, geometry statistics such as volume, surface area, and aspect ratio can be extracted automatically. Richer features like pockets and holes are straightforward from STEP topology, while STL-only workflows may need a few guided user inputs. We avoid overstating STL capability.

### 4. How do you ensure the quote is transparent?

We do not output only a final number. The quote is split into material, machining, setup, and overhead, and machining is further tied to active processes such as drilling, milling, turning, and grinding. We also expose the main cost drivers and DFM suggestions.

### 5. What data did you train on?

For hackathon scope, the baseline can be built using a synthetic dataset generated from engineering cost relationships with controlled variability. The architecture is intentionally designed so real quotation history can replace or augment that seed data later.

### 6. How will the model improve over time?

Each confirmed real-world quote becomes a labeled data point. Those records can be appended to the dataset and used in scheduled retraining. The key point is that the system is designed with a feedback loop, not as a one-time estimator.

### 7. What happens if the CAD file is incomplete or unreadable?

The system falls back gracefully. It asks for essential missing inputs rather than failing silently. For Round 2, we also maintain a backup sample-part demo so the quoting pipeline can still be shown even if file parsing fails.

### 8. How is this feasible within a hackathon timeline?

We intentionally chose a modular build: geometry inputs, routing logic, cost engine, explainability, and report output can each be demonstrated independently. That gives us a credible prototype without requiring enterprise integrations or large proprietary datasets.

### 9. What are the main limitations today?

- Synthetic data is only a starting point, not a substitute for full industrial history
- STL-only feature extraction is limited compared with STEP topology
- The current prototype is a decision-support estimator, not a final vendor quote replacement

### 10. What is the business value?

The biggest gain is earlier and faster decision-making. Engineers can identify expensive design choices before manufacturing commitment, procurement gets faster first-pass estimates, and teams gain a transparent costing baseline instead of opaque vendor-dependent turnaround.

## Questions you should ask yourselves before presenting

- Can every team member explain why setup cost changes with quantity?
- Can you defend why grinding is triggered by high tolerance?
- Can you explain the difference between feature-wise and process-wise cost contribution?
- Can you clearly say what is already built versus what is roadmap?
- Can you describe one realistic failure mode and how the system handles it?

## Short answer style for the panel

- Start with the conclusion first
- Give one technical reason
- End with one practical implication

Example:

"Yes. We keep the quote transparent by predicting or estimating each major cost component separately, so the engineer sees not just the total but what is driving it. That makes the system useful for design decisions, not just quoting."