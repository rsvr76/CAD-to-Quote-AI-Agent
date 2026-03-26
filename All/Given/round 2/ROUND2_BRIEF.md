# Round 2 Brief

## What the files say collectively

Your Round 1 direction is strong and consistent: the core idea is a CAD-to-Quote AI agent that converts part geometry plus a few manufacturing inputs into a transparent cost quote with explainability and DFM guidance.

The official Round 2 material shifts the burden from idea quality to judge confidence. The panel will score you on:

- Problem-solution alignment: 15%
- Idea clarity and innovation: 20%
- Technical depth and robustness: 25%
- Demo quality and visible progress: 20%
- Feasibility and roadmap: 10%
- Presentation quality and Q&A handling: 10%

This means Round 2 is not won by adding the most features. It is won by presenting a coherent system, proving technical reasoning, and showing credible implementation progress.

## Must-haves for Round 2

- Explain the real manufacturing pain clearly: manual quoting is slow, opaque, and not useful during design.
- Show a concrete pipeline: CAD input, feature extraction, chat agent, process routing, quote prediction, explainability, DFM suggestions, report output.
- Keep the quote transparent: material, machining, setup, and overhead must be visible.
- Show process-wise contribution: drilling, milling, turning, grinding should feel engineered, not decorative.
- Demonstrate visible progress: working script, mock UI, diagrams, charts, sample outputs, or recorded flow.
- Stay consistent with the Round 1 abstract. Refinements are welcome, but the core direction cannot drift.

## What to emphasize to judges

- The system is not a black box. It uses explicit geometry features and rule-based process routing.
- The quote is actionable, not just predictive. It explains cost drivers and suggests cost-reducing design changes.
- The approach is feasible in hackathon scope because it can start with synthetic data and lightweight Python tooling.
- The design is extensible to real industrial deployment through historical quote ingestion and periodic retraining.

## What to avoid

- Claiming full automatic manufacturing feature extraction from STL alone.
- Presenting too many differentiators without proving the core flow works.
- Generic AI wording without cost logic, routing logic, or demo evidence.
- Overshooting the 15-minute limit with too much technical detail on slides.

## Recommended story for Round 2

1. Problem: Manual quoting delays design decisions and hides cost drivers.
2. Solution: A CAD-to-Quote agent gives a quote in seconds with transparent breakdown.
3. Architecture: Geometry extraction plus input collection plus routing plus cost engine plus explainability.
4. Demo: One part goes through the full quote flow.
5. Impact: Faster quoting, better DFM decisions, scalable to real industrial data.

## Core differentiators to keep

Keep these three in the live story because they are strong and defensible:

- Transparent multi-component quote breakdown
- DFM suggestions with quantified savings
- Confidence range with explanation of uncertainty

Keep other differentiators as backup slides, not main-flow dependencies.

## Gaps found while analyzing the workspace

- [Final.py](Final.py) was empty, so there was no runnable backup demo.
- The strategy is richer than the presentation rules require; it needs pruning for judge-facing delivery.
- The abstracts are strong, but Round 2 needs more implementation evidence and crisper demo sequencing.

## Immediate execution priority

1. Use [Final.py](Final.py) as a fallback demo during practice and presentation day.
2. Build slides from [ROUND2_PPT_OUTLINE.md](ROUND2_PPT_OUTLINE.md), not directly from the long strategy file.
3. Rehearse answers from [ROUND2_QA.md](ROUND2_QA.md) until the team can defend data, feasibility, and assumptions quickly.