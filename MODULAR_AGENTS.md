# Modular Cell-Like Agents - Bloom Collective (Phase 3)

**Status:** Initial Design Draft
**Date:** 2026-06-11
**Purpose:** Define the modular, semi-autonomous "cell-like" agents that will form the building blocks of the system. These are the reusable, composable units whose activation is controlled by the epigenetic layer.

---

## Biological Analogy

In biology:
- Every cell contains the full genome but only expresses a subset of it (regulated by epigenetics)
- Cells are semi-autonomous: they maintain local state, make local decisions, and communicate with other cells
- Different cell types specialize while sharing the same underlying DNA
- Tissues and organs emerge from coordinated populations of cells
- Redundancy and robustness exist at the cellular level

We translate this into software agents:

- Each "Cell" carries awareness of the Core Genome and current Epigenetic State
- Cells are specialized but follow common interfaces
- The epigenetic layer controls which cells are active vs silenced
- Higher-level behavior emerges from cell interactions rather than being centrally scripted

## Core Principles for Cell-Like Agents

1. **Genome + Epigenetic Awareness**
   Every cell should be able to query the current Core Genome principles and the active epigenetic expression profile.

2. **Local Autonomy + Global Coherence**
   Cells make local decisions but operate within bounds set by the Core Genome and current epigenetic state.

3. **Clear Interfaces**
   All cells should implement a minimal common interface (e.g., `process(input)`, `get_state()`, `communicate(message)`).

4. **Composability**
   Cells can be combined into small "tissues" (coordinated groups) for more complex tasks.

5. **Observability**
   Every significant action or decision by a cell should be loggable and reviewable.

## Proposed Cell Interface (Initial)

```python
class BaseCell:
    def __init__(self, genome_ref, epigenetic_ref):
        self.genome = genome_ref      # Reference to Core Genome
        self.epigenetic = epigenetic_ref  # Reference to current EpigeneticState

    def process(self, input_data: dict) -> dict:
        """Main work method."""
        raise NotImplementedError

    def get_state(self) -> dict:
        """Return current internal state for observation."""
        raise NotImplementedError

    def communicate(self, message: dict) -> dict:
        """Send/receive messages to/from other cells or the orchestrator."""
        raise NotImplementedError

    def is_active(self) -> bool:
        """Should this cell be running given current epigenetic state?"""
        return self.epigenetic.is_module_active(self.__class__.__name__.lower().replace("cell", ""))
```

## First Proposed Cell Types (Phase 3 Seed)

### 1. ReflectionCell
- Responsible for structured self-reflection
- Uses current epigenetic expression (especially `reflection_depth` and `precision`)
- Outputs observations, strengths, and improvement areas
- Can be more or less verbose depending on epigenetic settings

### 2. MemoryCell
- Handles storage, retrieval, and versioning of experiences and states
- Supports semantic-like access (initially simple tagging + later vector search)
- Maintains both short-term working memory and longer-term episodic/semantic stores
- Works closely with EpigeneticState to weight what gets remembered strongly

### 3. CriticCell (Pruner)
- Evaluates proposals, changes, or outputs against Core Genome and current epigenetic goals
- Flags misalignment, bloat, or low coherence
- Can be more or less strict depending on `precision` and `risk_tolerance` settings
- Produces review-style feedback

### 4. ProposalCell (future)
- Generates concrete improvement proposals
- Modulated by creativity and risk tolerance
- Can operate in "safe/minimal change" mode or "exploratory" mode

## Orchestration Pattern (Initial)

For early phases we will use a simple central orchestrator (the BloomSeed or a new `OrchestratorCell`):

```
Orchestrator
  → Loads Core Genome + EpigeneticState
  → Determines which cells are currently active
  → Routes tasks to active cells
  → Collects outputs and logs results
  → Persists state
```

Later this can evolve into more decentralized, message-passing, or tissue-like coordination.

## Implementation Priorities for Phase 3

1. Define a clean `BaseCell` abstract/interface class
2. Implement `ReflectionCell` as the first concrete cell (refactor existing reflection logic)
3. Implement `MemoryCell` with basic versioning
4. Create a simple `Orchestrator` that loads genome + epigenetic state and routes to active cells
5. Demonstrate one full cycle using multiple cells

## Open Questions

- How much local state should individual cells maintain vs. delegating to a shared memory system?
- Should cells be able to propose their own activation/silencing (meta-regulation)?
- What is the minimal viable "tissue" (small group of cooperating cells) we should build first?
- How do we handle cell-to-cell communication in the early implementation?

---

*This document will evolve as we implement and learn.*
*Strongly inspired by cellular modularity and specialization in biology.*