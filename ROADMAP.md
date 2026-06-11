# Bloom Collective Roadmap

This document outlines the phased plan to turn Bloom Collective into a reliable, useful self-evolving AI agent.

## Guiding Principles
- Build capabilities gradually (developmental stages)
- Maintain strong alignment and human oversight
- Prefer modular, testable components
- Stabilize before expanding

## Phase 1: Foundation & Stabilization (Complete)

**Goal**: Make the core system reliable and testable.

- Core Genome + EpigeneticState
- Modular cell system with `supported_tasks`
- Orchestrator with proper routing
- Basic Memory, Reflection, and Critic cells
- FileSystemCell with path safety
- Comprehensive test coverage (28+ tests)
- GitHub Actions CI

## Phase 2: Core Agent Loop (Current Focus)

**Goal**: Create a reliable agent that can plan and execute simple multi-step goals.

### Priorities
- [ ] Improve PlanningCell (dependencies, priorities, alternatives)
- [ ] Strengthen VerificationCell with real outcome checking
- [ ] Make SystemAICell functional (real delegation to Grok / Copilot)
- [ ] Improve `local_agent.py` execution reliability
- [ ] Add basic self-correction after failed actions

### Success Criteria
- Agent can reliably complete simple multi-step goals
- Actions are verified after execution
- External AI delegation works for at least one assistant

## Phase 3: Tool Use & External Integration

**Goal**: Give the agent real capabilities through tools and other AIs.

- [ ] Safe command execution cell
- [ ] BrowserCell with real (sandboxed) web access
- [ ] Robust integration with GitHub Copilot and Grok
- [ ] Memory of past tool results

## Phase 4: Planning & Long-term Autonomy

**Goal**: Enable more complex, long-horizon behavior.

- [ ] Advanced planning with dependency graphs
- [ ] Task decomposition
- [ ] Goal persistence and memory across sessions
- [ ] Self-reflection on past performance

## Phase 5: Usability & Distribution

**Goal**: Make the system easy to use and contribute to.

- [ ] Clean CLI or web interface
- [ ] Good documentation and examples
- [ ] Easy installation (`pip install` or similar)
- [ ] Contributor-friendly onboarding

## How to Contribute

See `README.md` for contribution guidelines.

When working on the project:
1. Check the current phase
2. Write tests for new behavior
3. Keep changes small and focused
4. Run the full test suite before pushing
