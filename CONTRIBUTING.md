# Contributing to Bloom Collective

Thank you for your interest in contributing to Bloom Collective (Blossom)! This document explains how to contribute effectively.

## Code of Conduct

- Be respectful and constructive.
- Focus on the current phase of the roadmap.
- Prioritize stability and test coverage.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch from `main`
4. Make your changes
5. Run tests: `python -m unittest discover tests -v`
6. Submit a pull request

## Development Guidelines

### Core Principles

- **Stabilize first, expand later**
- **Small, targeted changes** are preferred over large refactors
- **All changes must pass tests**
- Respect the modular architecture (`supported_tasks`, `is_active`, EpigeneticState)

### Testing Requirements

- Use `tempfile` for any state or file operations in tests
- Never depend on real `memory/epigenetic_state.json`
- Add tests for any new behavior
- Run the full test suite before pushing

### Architecture Rules

- New cells must implement `supported_tasks`
- Respect `is_active` from `BaseCell`
- Keep logic in the appropriate cell (don’t put everything in `bloom_seed.py`)
- Use the Orchestrator for task routing

## Roadmap Alignment

Please check `ROADMAP.md` before starting work.

Current focus: **Phase 2 – Core Agent Capabilities**

Priority items:
- Improve PlanningCell
- Strengthen VerificationCell
- Make SystemAICell functional
- Improve local agent reliability

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Keep PRs focused (one feature/fix per PR)
4. Reference any related issues

## Questions?

Open an issue with the `question` label or start a discussion.

Thank you for helping build Bloom Collective!