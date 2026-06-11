#!/usr/bin/env python3
"""
Bloom Collective - Main Seed Agent (with SystemAICell Integration)

Now includes the new SystemAICell for proposing use of onboard AIs.
"""

from datetime import datetime
import time

try:
    from epigenetic_state import EpigeneticState, DevelopmentalStage
    from orchestrator import SimpleOrchestrator
    from reflection_cell import ReflectionCell
    from critic_cell import CriticCell
    from memory_cell import MemoryCell
    from system_ai_cell import SystemAICell
    from core_genome import CoreGenome
except ImportError as e:
    print(f"Import error: {e}")
    EpigeneticState = None


class BloomSeed:
    def __init__(self):
        print("\n" + "="*70)
        print("BLOOM COLLECTIVE - BOOTING UP (with System AI Integration)")
        print("="*70)

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
            if SystemAICell:
                self.orchestrator.register_cell(SystemAICell(epigenetic=self.epigenetic))

        self.growth_cycles = 0
        print(f"Initial Stage: {self.epigenetic.stage if self.epigenetic else 'unknown'}")
        print("System initialized with SystemAICell.\n")

    def run_growth_cycle(self, observation: str = None):
        self.growth_cycles += 1

        print("\n" + "-"*70)
        print(f"GROWTH CYCLE {self.growth_cycles}  |  Stage: {self.epigenetic.stage if self.epigenetic else 'N/A'}")
        print("-"*70)

        if observation is None:
            observation = f"Cycle {self.growth_cycles} - Continuing coherent growth and capability development."

        # Reflection
        print("[Reflection] ...")
        if self.orchestrator:
            self.orchestrator.run_task("reflect", {"observation": observation})

        # Memory
        if self.orchestrator:
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": {"type": "growth", "cycle": self.growth_cycles},
                "tags": ["growth", f"cycle-{self.growth_cycles}"]
            })

        # System AI consideration (new)
        print("[System AI Check] ...")
        if self.orchestrator:
            ai_result = self.orchestrator.run_task("system_ai", {
                "task": "Improve efficiency on current growth focus"
            })
            if ai_result.get("results"):
                for cell_name, result in ai_result["results"].items():
                    if "SystemAICell" in cell_name:
                        print(f"  {result.get('recommendation', 'No recommendation')}")

        # Critique
        print("[Critique] ...")
        proposal = "Continue developing tool use and external AI integration capabilities."
        if self.orchestrator:
            self.orchestrator.run_task("critique", {
                "observation": observation,
                "proposal": proposal
            })

        # Core Genome validation
        if self.genome:
            validation = self.genome.validate_proposal(proposal)
            status = "✓ Valid" if validation['valid'] else "✗ Issues found"
            print(f"[Core Genome] {status} | Score: {validation['alignment_score']}")

        # Stage transition demo
        if self.epigenetic and self.growth_cycles % 3 == 0:
            current = DevelopmentalStage(self.epigenetic.stage)
            next_stages = list(DevelopmentalStage)
            try:
                idx = next_stages.index(current)
                if idx + 1 < len(next_stages):
                    next_stage = next_stages[idx + 1]
                    if self.epigenetic.can_transition_to(next_stage):
                        success = self.epigenetic.transition_to(next_stage)
                        if success:
                            print(f"\n>>> STAGE TRANSITION: {current.value} → {next_stage.value} <<<")
            except Exception:
                pass

        print("-"*70)

    def print_summary(self):
        print("\n" + "="*70)
        print("RUN SUMMARY")
        print("="*70)
        print(f"Total cycles completed: {self.growth_cycles}")
        if self.epigenetic:
            print(f"Final stage reached: {self.epigenetic.stage}")
        print("="*70)
        print()


if __name__ == "__main__":
    seed = BloomSeed()
    for _ in range(6):
        seed.run_growth_cycle()
    seed.print_summary()
