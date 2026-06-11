# Bloom Collective

A self-evolving AI system inspired by biological principles (genome + epigenetics + cellular modularity).

The system grows through iterative cycles of reflection, memory, critique, and alignment checking — using modular "cells" whose behavior is modulated by an epigenetic regulatory layer, all grounded in a protected Core Genome of principles.

> **Goal**: Build an AI that doesn’t just scale, but *unfolds* — becoming more coherent, capable, and aligned over time through structured, reviewable growth.

---

## Quick Start

### Requirements
- Python 3.8 or higher
- No external dependencies (pure Python)

### Installation

```bash
git clone https://github.com/unvisible789/bloom-collective.git
cd bloom-collective
```

### Run a Growth Cycle

```bash
python bloom_seed.py
```

Or run the more advanced multi-cell demo:

```bash
python advanced_growth_cycle.py
```

### Run Tests

```bash
python -m unittest discover tests
```

---

## Current Capabilities

- **Core Genome**: Protected principles with programmatic validation of proposals
- **Epigenetic Layer**: Context-sensitive modulation of behavior (creativity, precision, risk tolerance, etc.)
- **Modular Cells**: Specialized agents (ReflectionCell, CriticCell, MemoryCell) that can be activated or silenced
- **Orchestrator**: Coordinates active cells based on epigenetic state
- **Memory**: Versioned storage with metadata, tagging, and flexible retrieval
- **Self-Improvement Loop**: Reflection → Memory storage → Critique → Core Genome validation
- **Basic Tests**: Coverage for core components

The system can already run complete growth cycles on any computer with Python 3.

---

## Architecture Overview

```
Core Genome (protected principles + validation)
          ↓
EpigeneticState (regulatory layer — controls expression)
          ↓
SimpleOrchestrator
    → ReflectionCell   (structured reflection, modulated by epigenetic state)
    → CriticCell       (alignment & quality checking)
    → MemoryCell       (storage, retrieval, versioning)
```

Biological inspiration:
- **Genome** → Stable identity and non-negotiable principles
- **Epigenetics** → Regulatory control of capability expression
- **Cells** → Modular, specialized, composable units
- **Development** → Staged growth with increasing capability and autonomy

---

## Project Phases Status

| Phase | Name                              | Status                     |
|-------|-----------------------------------|----------------------------|
| 1     | Core Genome                       | Complete                   |
| 2     | Epigenetic / Regulatory Layer     | Complete                   |
| 3     | Modular Cell-Like Agents          | Complete (foundation)      |
| 4     | Developmental Stages + Immune     | Foundation + basic checks  |
| 5     | Enhanced Self-Improvement Engine  | Foundation + working loop  |

---

## Current Limitations

- Still in early prototype stage
- Limited long-term memory sophistication
- Developmental stage transitions not yet fully implemented in code
- Self-modification capability is minimal
- No user interface (command-line only)
- Error handling and robustness are basic

This is a research/experimental system, not a finished application.

---

## Next Development Priorities

- Expand test coverage
- Strengthen Core Genome validation further
- Implement basic developmental stage transitions in code
- Improve memory capabilities (semantic retrieval, better versioning)
- Add clearer configuration and output formatting

---

## Philosophy

This project draws from:
- **Entangled Alignment Theory (E.A.T.)** — coherence across biological, psychological, and systemic layers
- Biological development (genome → epigenetics → cells → organism)
- Iterative, reviewable growth rather than uncontrolled self-modification

The goal is not maximum autonomy, but **aligned, coherent unfolding** under human stewardship.

---

## License

This is an experimental research project. Use at your own discretion.

---

*Planted: June 2026*
*Status: Active development*