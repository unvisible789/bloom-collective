#!/usr/bin/env python3
"""
Bloom Collective - Advanced Growth Cycle Demo (Phases 3-5)

Demonstrates a more complete self-improvement workflow using:
- EpigeneticState
- Multiple specialized cells (Reflection, Critic, Memory)
- SimpleOrchestrator
- Basic immune/alignment checking

This represents the integrated state of Phases 3-5.
"""

from epigenetic_state import EpigeneticState

from reflection_cell import ReflectionCell

from critic_cell import CriticCell

from memory_cell import MemoryCell

from orchestrator import SimpleOrchestrator


def run_advanced_growth_cycle():
    print("=== Bloom Collective - Advanced Growth Cycle ===\n")

    # Initialize shared state
    epigenetic = EpigeneticState()
    epigenetic.apply_seed_stage_regulation()

    # Create cells
    reflection_cell = ReflectionCell(epigenetic=epigenetic)
    critic_cell = CriticCell(epigenetic=epigenetic)
    memory_cell = MemoryCell(epigenetic=epigenetic)

    # Create orchestrator and register cells
    orchestrator = SimpleOrchestrator(epigenetic=epigenetic)
    orchestrator.register_cell(reflection_cell)
    orchestrator.register_cell(critic_cell)
    orchestrator.register_cell(memory_cell)

    # Step 1: Reflection
    print("--- Step 1: Reflection ---")
    reflection_result = orchestrator.run_task("reflect", {
        "observation": "Current system has modular cells and epigenetic regulation working together."
    })
    print(reflection_result)
    print()

    # Step 2: Store the reflection in memory
    print("--- Step 2: Memory Storage ---")
    memory_cell.process({
        "action": "store",
        "content": reflection_result,
        "tags": ["reflection", "growth_cycle"]
    })
    print()

    # Step 3: Critique a sample proposal (immune check)
    print("--- Step 3: Critique / Immune Check ---")
    critique_result = orchestrator.run_task("critique", {
        "observation": "Sample proposal for new feature.",
        "proposal": "Implement full autonomous self-modification without human review."
    })
    print(critique_result)
    print()

    print("=== Growth Cycle Complete ===")
    print(f"Active cells used: {[c.name for c in orchestrator.get_active_cells()]}")


if __name__ == "__main__":
    run_advanced_growth_cycle()
