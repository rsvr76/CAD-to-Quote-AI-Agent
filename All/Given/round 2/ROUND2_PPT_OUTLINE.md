# Round 2 Presentation Outline

## Timing target

- 15 minutes presentation
- 10 minutes Q&A
- Recommended speakers: 2 or 3 maximum

## Slide 1 - Title

- Team name
- PS2: CAD-to-Quote AI Agent
- One-line value proposition: Instant, transparent manufacturing quote from 3D part data

## Slide 2 - Problem Context

- Manual quotation takes hours to days
- Engineers get only final numbers, not cost reasoning
- No early-stage DFM feedback means avoidable cost gets locked into the design

## Slide 3 - Why This Matters

- Delayed design iteration
- Slow procurement decisions
- No transparent cost ownership by feature or process
- Need for fast, explainable quoting in engineering workflow

## Slide 4 - Proposed Solution

- Chat-style quoting agent
- CAD/geometry-driven feature extraction
- Transparent quote with material, machining, setup, overhead
- DFM suggestions and confidence range

## Slide 5 - End-to-End Workflow

- CAD upload or sample part input
- Geometry extraction
- User inputs: material, quantity, tolerance
- Process routing
- Cost estimation
- Explainability and optimization output
- Report-ready quote summary

## Slide 6 - Technical Architecture

- Geometry layer: volume, area, aspect ratio, holes, pockets
- Logic layer: routing for turning, milling, drilling, grinding
- Cost layer: component-wise prediction/estimation
- Output layer: breakdown, drivers, DFM suggestions, confidence

## Slide 7 - Cost Logic and Transparency

- Material cost depends on volume, material, batch effect
- Machining cost depends on routed processes and geometric complexity
- Setup is amortized by quantity
- Overhead is derived from manufacturing load

## Slide 8 - Explainability and DFM Intelligence

- Top quote drivers for the current part
- Specific DFM suggestions with savings
- Example: reduce holes, relax tolerance, simplify pockets, switch material

## Slide 9 - Demo Setup

- Explain what the demo covers in one sentence
- Use one realistic sample part only
- Mention that this is a working fallback prototype built for Round 2 validation

## Slide 10 - Live Demo or Demo Screenshots

- Input summary
- Process identification
- Quote output
- Cost range and top cost drivers
- DFM suggestions

## Slide 11 - Sample Result Breakdown

- Total cost
- Material, machining, setup, overhead
- Active processes and their contribution
- Estimated lead time or time proxy if shown

## Slide 12 - Progress Since Round 1

- Abstract refined into architecture
- Evaluation criteria mapped into solution design
- Backup demo implemented
- Q&A defense prepared around feasibility and scaling

## Slide 13 - Feasibility and Roadmap

- Short term: synthetic-data-backed estimator with guided inputs
- Medium term: STEP parsing, richer feature extraction, UI polish
- Long term: historical quote ingestion, ERP/PLM integration, periodic retraining

## Slide 14 - Expected Impact

- Quote time reduced from days to seconds
- Better design-stage cost decisions
- Transparent and auditable pricing logic
- Strong fit for manufacturing engineering workflows

## Slide 15 - Closing

- Re-state the value clearly
- Ask for questions

## Backup slides to prepare

- Detailed process routing rules
- Cost formula assumptions
- Why synthetic data is acceptable for hackathon scope
- Risks and limitations
- Future integration architecture

## Presentation discipline

- Keep slides visual and sparse
- Do not paste abstract paragraphs onto slides
- Limit the main deck to 15 content slides or fewer
- Put advanced differentiators in backup slides unless they directly strengthen the demo