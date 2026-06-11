#!/usr/bin/env python3
"""
Bloom Collective - Main Agent (More Autonomous)

The main loop is now more dynamic. The system can influence its own focus
based on previous reflections and plans.
"""

from datetime import datetime

try:
    from epigenetic_state import EpigeneticState, DevelopmentalStage
    from orchestrator import SimpleOrchestrator
    from reflection_cell import ReflectionCell
    from critic_cell import CriticCell
    from memory_cell import MemoryCell
    from system_ai_cell import SystemAICell
    from file_system_cell import FileSystemCell
    from browser_cell import BrowserCell
    from planning_cell import PlanningCell
    from verification_cell import VerificationCell
    from core_genome import CoreGenome
except ImportError as e:
    print(f"Import error: {e}")


class BloomSeed:
    def __init__(self):
        print("\n" + "="*70)
        print("BLOOM COLLECTIVE - INITIALIZING (Autonomous Mode)")
        print("="*70)

        self.epigenetic = EpigeneticState() if EpigeneticState else None
        self.genome = CoreGenome() if 'CoreGenome' in dir() else None

        if self.epigenetic:
            self.epigenetic.apply_seed_stage_regulation()

        self.orchestrator = SimpleOrchestrator(epigenetic=self.epigenetic) if SimpleOrchestrator else None

        if self.orchestrator:
            for Cell in [ReflectionCell, CriticCell, MemoryCell, SystemAICell,
                         FileSystemCell, BrowserCell, PlanningCell, VerificationCell]:
                if Cell:
                    self.orchestrator.register_cell(Cell(epigenetic=self.epigenetic))

        self.growth_cycles = 0
        self.current_focus = "Expanding capabilities and collaboration."
        print(f"Stage: {self.epigenetic.stage if self.epigenetic else 'unknown'}\n")

    def run_growth_cycle(self):
        self.growth_cycles += 1
        print(f"\n--- Cycle {self.growth_cycles} ---")

        observation = self.current_focus

        if self.orchestrator:
            # Reflection
            reflection = self.orchestrator.run_task("reflect", {"observation": observation})

            # Planning
            self.orchestrator.run_task("planning", {"goal": observation})

            # Memory
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": observation,
                "tags": ["growth"]
            })

            # System AI delegation
            self.orchestrator.run_task("system_ai", {"task": observation, "delegate": True})

            # File System
            self.orchestrator.run_task("file_system", {"action": "list", "path": "."})

            # Browser
            self.orchestrator.run_task("browser", {"action": "search", "query": observation})

            # Verification
            self.orchestrator.run_task("verification", {
                "action": "growth cycle",
                "expected_outcome": "Progress on capabilities"
            })

            # Critique
            critique = self.orchestrator.run_task("critique", {
                "observation": observation,
                "proposal": "Improve autonomy and capabilities."
            })

        if self.genome:
            validation = self.genome.validate_proposal("Improve autonomy and capabilities")
            print(f"Core Genome: {'Valid' if validation['valid'] else 'Issues'} | Score: {validation['alignment_score']}")

        # Update focus for next cycle based on reflection (basic autonomy)
        if self.growth_cycles % 2 == 0:
            self.current_focus = "Continue developing computer interaction and external AI collaboration."
        else:
            self.current_focus = "Focus on planning, verification, and efficiency."

        # Stage progression
        if self.epigenetic and self.growth_cycles % 3 == 0:
            current = DevelopmentalStage(self.epigenetic.stage)
            next_stages = list(DevelopmentalStage)
            try:
                idx = next_stages.index(current)
                if idx + 1 < len(next_stages):
                    next_stage = next_stages[idx + 1]
                    if self.epigenetic.can_transition_to(next_stage):
                        if self.epigenetic.transition_to(next_stage):
                            print(f">>> Stage: {current.value} → {next_stage.value}")
            except Exception:
                pass

        print("-" * 50)


if __name__ == "__main__":
    seed = BloomSeed()
    for _ in range(6):
        seed.run_growth_cycle()
