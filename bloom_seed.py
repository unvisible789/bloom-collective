#!/usr/bin/env python3
"""
Bloom Collective - Main Seed Agent (with Active Memory Usage)

Demonstrates the improved MemoryCell in a real growth cycle:
- Stores reflections with metadata
- Retrieves recent memories
- Uses memory context in reflection
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

    def run_growth_cycle(self, observation: str = None):
        print("=" * 65)
        print("BLOOM SEED GROWTH CYCLE (with Active Memory)")
        print("=" * 65)
        print()

        if observation is None:
            observation = "System continuing to evolve with improved memory capabilities."

        # 1. Get recent memories for context
        print("[1] Retrieving recent memories for context...")
        recent_memories = []
        if self.orchestrator:
            mem_cell = self.orchestrator.cells.get("MemoryCell")
            if mem_cell:
                recent = mem_cell.get_recent(3)
                recent_memories = recent
                print(f"   Found {len(recent)} recent memories.")
        print()

        # 2. Reflection (include memory context)
        print("[2] Performing reflection...")
        reflection_input = {
            "observation": observation,
            "recent_memories_count": len(recent_memories)
        }
        reflection_result = self.orchestrator.run_task("reflect", reflection_input) if self.orchestrator else {}
        print(reflection_result)
        print()

        # 3. Store reflection with rich metadata
        print("[3] Storing reflection with metadata...")
        if self.orchestrator:
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": reflection_result,
                "tags": ["reflection", "growth", f"cycle-{self.growth_cycles + 1}"],
                "metadata": {
                    "cycle": self.growth_cycles + 1,
                    "stage": self.epigenetic.stage if self.epigenetic else "unknown",
                    "has_recent_memories": len(recent_memories) > 0
                }
            })
        print()

        # 4. Critique a proposal
        print("[4] Critiquing improvement proposal...")
        proposal = "Enhance memory retrieval with simple semantic search."
        critique_result = self.orchestrator.run_task("critique", {
            "observation": observation,
            "proposal": proposal
        }) if self.orchestrator else {}
        print(critique_result)
        print()

        # 5. Core Genome validation
        if self.genome:
            print("[5] Validating against Core Genome...")
            validation = self.genome.validate_proposal(proposal)
            print(f"   Valid: {validation['valid']}, Score: {validation['alignment_score']}")
            if validation['issues']:
                print(f"   Issues: {validation['issues']}")
            print()

        self.growth_cycles += 1
        print("=" * 65)
        print(f"Cycle {self.growth_cycles} Complete")
        print("=" * 65)
        print()


if __name__ == "__main__":
    seed = BloomSeed()
    seed.run_growth_cycle()
