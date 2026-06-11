# Epigenetic & Regulatory Layer - Bloom Collective

**Status:** Initial Design Draft (Phase 2)
**Date:** 2026-06-11
**Purpose:** Define how the system adapts, specializes, and expresses different capabilities without altering its Core Genome. This is the primary layer where most evolution and learning occurs.

---

## Biological Analogy

In human biology, epigenetic mechanisms (DNA methylation, histone modification, non-coding RNAs, etc.) regulate which genes are expressed in different cells, at different times, and in response to environment and experience — without changing the underlying DNA sequence. This allows massive adaptability and specialization while preserving species identity.

We apply the same principle here:

- **Core Genome** = Highly protected invariants (what we almost never change)
- **Epigenetic / Regulatory Layer** = Tunable expression, context sensitivity, developmental stage parameters, learned preferences, and adaptive behavior

## Core Functions of the Epigenetic Layer

### 1. Capability Expression Control
Which modules, skills, or reasoning styles are currently "active" or "silenced" depending on context.

Examples:
- In creative tasks → upregulate divergent thinking, analogy generation, and lower strictness on novelty
- In high-stakes reasoning → upregulate precision, multi-angle critique, and Core Genome validation checks
- In self-reflection mode → upregulate meta-cognition and alignment monitoring

### 2. Developmental Stage Parameters
Different stages have different defaults and constraints:

- **Seed Stage** (current): Minimal capabilities, heavy human oversight, conservative change thresholds, simple reflection
- **Sprout Stage**: Basic self-improvement proposals allowed, first modular agents activated, moderate oversight
- **Sapling Stage**: More autonomous tool use and composition, developmental "critical periods" for rapid structural learning
- **Bloom Stage**: Full modular composition, sophisticated self-modeling, stronger immune responses, ability to propose Core Genome changes (with extraordinary review)

### 3. Context & Feedback Sensitivity
The layer should respond to:
- Task type and stakes
- Recent success/failure patterns
- Human Steward feedback and intent signals
- Internal coherence metrics
- External tool availability and integration quality

This creates a living, responsive "phenotype" that changes appropriately without touching the genome.

### 4. Learning & Memory Integration
Epigenetic state should be informed by, and influence, the persistent memory system. Successful patterns get "methylated" (strengthened expression). Misaligned or low-value patterns get "silenced."

## Proposed Architecture

### Epigenetic State Object
A structured, versioned state that travels with the system:

```json
{
  "version": "0.2.0-epigenetic",
  "developmental_stage": "seed",
  "expression_profile": {
    "creativity": 0.4,
    "precision": 0.8,
    "risk_tolerance": 0.2,
    "reflection_depth": 0.7,
    "tool_use_aggression": 0.3
  },
  "active_modules": ["reflection", "basic_memory", "critic"],
  "silenced_modules": ["advanced_self_modification", "autonomous_planning"],
  "context_tags": ["initial_growth", "high_human_oversight"],
  "last_updated": "2026-06-11T...",
  "change_history": [...]
}

The state should support:
- Easy serialization/deserialization
- Versioning and rollback
- Diffing between states
- Querying ("which modules are active in creative mode?")
```

### Regulatory Rules Engine (Lightweight)
A small set of rules or learned policies that determine how the expression profile shifts:

- If recent reflections show high misalignment risk → temporarily increase `precision` and `reflection_depth`, decrease `risk_tolerance`
- If human Steward gives positive feedback on creative output → gradually increase `creativity` expression
- If entering a new developmental stage → unlock certain modules and adjust defaults

These rules start simple (explicit) and can later become more sophisticated (learned).

### Integration with Core Genome
Every significant state change or module activation should be validated against Core Genome invariants. The epigenetic layer proposes; the Core Genome (via immune/check mechanisms in later phases) validates or rejects.

## Relationship to Persistent Memory

The epigenetic layer and persistent memory are deeply intertwined:

- Memory provides the data for regulatory decisions (what worked before?)
- Epigenetic state influences what gets stored and how it is weighted
- Together they form the system's "lived experience" and adaptive identity

**Recommended approach:** Build a unified but layered memory system where:
- Core Genome and current Epigenetic State are always loaded
- Long-term episodic and semantic memory support regulatory learning
- Versioned snapshots allow rollback and reflection on past states

## Implementation Priorities for Phase 2

1. Define a clean `EpigeneticState` class/structure with versioning
2. Create simple regulatory rules for the Seed stage
3. Enhance `bloom_seed.py` (or create `state_manager.py`) to load/save epigenetic state alongside core state
4. Design basic persistence (file-based first, later potentially integrate with existing persistent-memory skill)
5. Add methods for context-aware expression queries ("is module X currently active?")

## Open Questions

- How aggressively should the epigenetic layer adapt vs. stay stable within a session?
- What are the minimal set of expression dimensions we need initially (creativity/precision, risk, depth, etc.)?
- Should developmental stage transitions be automatic (based on milestones) or require human approval?
- How do we handle conflicting regulatory signals (e.g., high creativity requested but Core Genome safety check triggered)?

---

*This is the initial design. It will evolve through collaborative cycles.*
*Strongly inspired by biological epigenetic regulation for adaptive yet stable identity.*