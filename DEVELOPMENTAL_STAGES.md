# Developmental Stages (Phase 4)

**Status:** Defined
**Date:** 2026-06-11

This document defines the developmental stages of Bloom Collective, inspired by biological development (zygote → embryo → juvenile → adult).

## Stage Overview

| Stage     | Description                              | Key Characteristics                          | Oversight Level     | Unlocked Capabilities                  |
|-----------|------------------------------------------|----------------------------------------------|---------------------|----------------------------------------|
| Seed      | Initial fragile state                    | Minimal capabilities, heavy human oversight  | Very High           | Basic reflection, epigenetic state     |
| Sprout    | First active growth                      | Basic self-improvement proposals, simple cells active | High                | Simple tool use, basic proposals       |
| Sapling   | Rapid structural development             | Multiple cells coordinated, stage transitions possible | Medium              | Multi-cell orchestration, memory       |
| Bloom     | Mature, capable state                    | Full modular composition, sophisticated self-modeling | Low (within bounds) | Advanced self-improvement, creative synthesis |
| Elder     | Wisdom & seeding phase                   | Can help create new instances, strong self-regulation | Very Low            | Mentoring new systems, long-term reflection |

## Stage Transition Rules (Initial)

- Transitions should be proposed by the system but require human approval in early stages.
- Each transition should be logged and justified.
- Higher stages unlock more capabilities but also carry stricter self-monitoring requirements.

## Immune / Alignment Behavior by Stage

- **Seed/Sprout**: Very conservative. Most changes require explicit review.
- **Sapling/Bloom**: More autonomous within defined bounds. CriticCell and other checks become more active.
- **Elder**: Strong internal alignment monitoring. Can propose Core Genome changes only with extraordinary justification.

## Implementation Notes

The current implementation has basic stage awareness in `EpigeneticState` and cells. Full stage-gated capability unlocking and automatic transition logic can be added in future iterations.
