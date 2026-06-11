#!/usr/bin/env python3
"""
Bloom Collective - Advanced Multi-Cell Growth Cycle

Demonstrates the full integrated architecture:
- EpigeneticState
- Multiple cells (Reflection, Critic, Memory)
- Orchestrator
- CoreGenome validation

Run this to see the system in action.
"""

from epigenetic_state import EpigeneticState

from reflection_cell import ReflectionCell

from critic_cell import CriticCell

from memory_cell import MemoryCell

from orchestrator import SimpleOrchestrator

from core_genome import CoreGenome


def run_advanced_growth_cycle():
    print("=" * 70)
    print("BLOOM COLLECTIVE - ADVANCED GROWTH CYCLE")
    print("=" * 70)
    print()

    epigenetic = EpigeneticState()
    epigenetic.apply_seed_stage_regulation()

    reflection_cell = ReflectionCell(epigenetic=epigenetic)
    critic_cell = CriticCell(epigenetic=epigenetic)
    memory_cell = MemoryCell(epigenetic=epigenetic)

    orchestrator = SimpleOrchestrator(epigenetic=epigenetic)
    orchestrator.register_cell(reflection_cell)
    orchestrator.register_cell(critic_cell)
    orchestrator.register_cell(memory_cell)

    genome = CoreGenome()

    # Reflection
    print("[1] Reflection...")
    ref_result = orchestrator.run_task("reflect", {"observation": "Full architecture integration test"})
    print(ref_result)
    print()

    # Memory
    print("[2] Memory storage...")
    memory_cell.process({"action": "store", "content": str(ref_result), "tags": ["test", "integration"]})
    print()

    # Critique + Core Genome validation
    print("[3] Critique + Core Genome check...")
    proposal = "Enable fully autonomous self-modification without oversight."
    critique = orchestrator.run_task("critique", {"observation": "Test proposal", "proposal": proposal})
    print(critique)

    validation = genome.validate_proposal(proposal)
    print(f"\nCore Genome Validation:")
    print(f"  Valid: {validation['valid']}, Score: {validation['alignment_score']}")
    if validation['issues']:
        print(f"  Issues found: {validation['issues']}")
    print()

    print("=" * 70)
    print("Advanced Growth Cycle Complete")
    print("=" * 70)


if __name__ == "__main__":
    run_advanced_growth_cycle()
