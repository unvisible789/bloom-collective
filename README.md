# Bloom Collective (Blossom)

A self-evolving, biologically-inspired AI system built with modular cells, epigenetic regulation, and a protected Core Genome.

## Vision

Build an efficient, aligned, and gradually capable AI agent that can improve itself over time while maintaining strong human oversight and safety boundaries.

## Current Status (June 2026)

- **Architecture**: Strong foundation (Core Genome, EpigeneticState, modular cells, developmental stages)
- **Test Coverage**: Significantly improved (28+ tests)
- **Local Agent**: Basic `local_agent.py` now exists with goal planning
- **Stability**: Active refactoring and testing in progress
- **Usability**: Still early / prototype stage

## Project Structure

- `base_cell.py` — Base class for all modular cells
- `orchestrator.py` — Routes tasks to appropriate cells
- `epigenetic_state.py` — Controls which capabilities are active
- `memory_cell.py`, `reflection_cell.py`, `critic_cell.py` — Core cognitive cells
- `file_system_cell.py`, `browser_cell.py` — Computer interaction cells
- `planning_cell.py`, `verification_cell.py` — Planning and self-verification
- `system_ai_cell.py` — Interface for external AIs (Grok, Copilot, etc.)
- `bloom_seed.py` — Main entry point / growth loop
- `local_agent.py` — Emerging local goal-planning agent

## How to Run

```bash
python bloom_seed.py
```

Or for the local agent:

```bash
python local_agent.py
```

Run tests:

```bash
python -m unittest discover tests -v
```

## Roadmap

### Phase 1: Stabilization (Mostly Complete)
- [x] Fix MemoryCell activation
- [x] Fix orchestrator routing
- [x] Add FileSystemCell path safety
- [x] Improve test isolation
- [x] Expand core test coverage to 28+ tests

### Phase 2: Core Agent Capabilities (In Progress)
- [ ] Strengthen PlanningCell with dependencies and prioritization
- [ ] Improve VerificationCell with real outcome checking
- [ ] Make SystemAICell capable of actual delegation to Grok/Copilot
- [ ] Add basic self-verification after actions
- [ ] Improve `local_agent.py` goal execution reliability

### Phase 3: Tool Use & External Integration
- [ ] Full integration with GitHub Copilot CLI
- [ ] Reliable delegation to Grok
- [ ] BrowserCell with real web capabilities (with safety)
- [ ] Safe command execution cell

### Phase 4: Planning & Autonomy
- [ ] Long-horizon planning with dependency tracking
- [ ] Task decomposition engine
- [ ] Self-correction loops
- [ ] Goal persistence across sessions

### Phase 5: Polish & Usability
- [ ] Clean CLI or simple interface
- [ ] Better logging and observability
- [ ] Documentation and examples
- [ ] Packaging and easy installation

## Contribution Guidelines

### For Other Workers / Contributors

1. **Stay in scope** — Focus on the current phase before jumping ahead.
2. **Test everything** — All changes must pass `python -m unittest discover tests -v`.
3. **Respect the architecture**:
   - Use `supported_tasks` in cells
   - Respect `is_active` from EpigeneticState
   - Keep changes small and targeted
4. **No breaking changes** without discussion.
5. **Use temporary files** in tests (never rely on real `memory/epigenetic_state.json`).

### Development Principles
- Prefer small, correct fixes over large refactors.
- Maintain separation between Core Genome (protected) and Epigenetic layer (flexible).
- Build capabilities gradually through developmental stages.
- Prioritize alignment and human oversight.

## Getting Help

- Check existing issues and discussions
- Follow the roadmap above
- When in doubt, stabilize first, then expand

## License

TBD
