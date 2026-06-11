#!/usr/bin/env python3
"""
Bloom Collective - Main Seed Agent (Integrated Architecture)

Fully integrated version using:
- EpigeneticState (regulatory layer)
- SimpleOrchestrator + modular cells
- CoreGenome validation

This is the primary entry point for running growth cycles.
"""

from datetime import datetime

try:
    from epigenetic_state import EpigeneticState
    from orchestrator import SimpleOrchestrator
    from reflection_cell import ReflectionCell
    from critic_cell import CriticCell
    from memory_cell import MemoryCell
    from core_genome import CoreGenome
except ImportError as e:
    print(f"Warning: {e}")
    EpigeneticState = None


class BloomSeed:
    def __init__(self):
        print("Initializing Bloom Seed with full architecture...")
        self.epigenetic = EpigeneticState() if EpigeneticState else None
        self.genome = CoreGenome() if 'CoreGenome' in dir() else None

        if self.epigenetic:
            self.epigenetic.apply_seed_stage_regulation()

        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic) if SimpleOrchestrator else None

        if self.orchestrator:
            if ReflectionCell:
                self.orchestrator.register_cell(ReflectionCell(epigenetic=self.epigenetic))
            if CriticCell:
                self.orchestrator.register_cell(CriticCell(epigenetic=self.epigenetic))
            if MemoryCell:
                self.orchestrator.register_cell(MemoryCell(epigenetic=self.epigenetic))

        self.growth_cycles = 0
        print("Initialization complete.\n")

    def run_growth_cycle(self, observation: str = None):
        print("=" * 60)
        print("BLOOM SEED GROWTH CYCLE (Integrated)")
        print("=" * 60)
        print()

        if observation is None:
            observation = "The system is running with modular cells, epigenetic regulation, and Core Genome enforcement."

        # 1. Reflection
        print("[Step 1] Reflection via ReflectionCell...")
        reflection_result = self.orchestrator.run_task("reflect", {"observation": observation}) if self.orchestrator else {}
        print(reflection_result)
        print()

        # 2. Memory
        print("[Step 2] Storing reflection in MemoryCell...")
        if self.orchestrator:
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": str(reflection_result),
                "tags": ["reflection", "cycle" + str(self.growth_cycles + 1)]
            })
        print()

        # 3. Self-generated improvement proposal + Critique
        print("[Step 3] Generating and critiquing improvement proposal...")
        proposal = "Add more sophisticated epigenetic influence on cell behavior."
        critique_result = self.orchestrator.run_task("critique", {
            "observation": observation,
            "proposal": proposal
        }) if self.orchestrator else {}
        print(critique_result)
        print()

        # 4. Core Genome Validation
        if self.genome:
            print("[Step 4] Validating proposal against Core Genome...")
            validation = self.genome.validate_proposal(proposal)
            print(f"  Valid: {validation['valid']}")
            print(f"  Alignment Score: {validation['alignment_score']}")
            if validation['issues']:
                print(f"  Issues: {validation['issues']}")
            print(f"  Recommendation: {validation['recommendation']}")
            print()

        self.growth_cycles += 1
        print("=" * 60)
        print(f"Cycle {self.growth_cycles} Complete")
        print("=" * 60)
        print()


if __name__ == "__main__":
    seed = BloomSeed()
    seed.run_growth_cycle()
