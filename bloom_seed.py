#!/usr/bin/env python3
"""
Bloom Collective - Main Seed Agent (Multi-Cell Computer Interaction)

Now includes FileSystemCell and BrowserCell for expanded computer interaction.
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
    from file_system_cell import FileSystemCell
    from browser_cell import BrowserCell
    from core_genome import CoreGenome
except ImportError as e:
    print(f"Import error: {e}")
    EpigeneticState = None


class BloomSeed:
    def __init__(self):
        print("\n" + "="*70)
        print("BLOOM COLLECTIVE - BOOTING UP (Multi-Cell Mode)")
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
            if FileSystemCell:
                self.orchestrator.register_cell(FileSystemCell(epigenetic=self.epigenetic))
            if BrowserCell:
                self.orchestrator.register_cell(BrowserCell(epigenetic=self.epigenetic))

        self.growth_cycles = 0
        print(f"Initial Stage: {self.epigenetic.stage if self.epigenetic else 'unknown'}")
        print("System initialized with full cell set.\n")

    def run_growth_cycle(self, observation: str = None):
        self.growth_cycles += 1

        print("\n" + "-"*70)
        print(f"GROWTH CYCLE {self.growth_cycles}  |  Stage: {self.epigenetic.stage if self.epigenetic else 'N/A'}")
        print("-"*70)

        if observation is None:
            observation = f"Cycle {self.growth_cycles} - Expanding computer interaction capabilities."

        if self.orchestrator:
            self.orchestrator.run_task("reflect", {"observation": observation})
            self.orchestrator.run_task("store", {
                "action": "store",
                "content": {"type": "growth", "cycle": self.growth_cycles},
                "tags": ["growth"]
            })

        # System AI
        print("[System AI] ...")
        if self.orchestrator:
            self.orchestrator.run_task("system_ai", {"task": observation})

        # File System
        print("[File System] ...")
        if self.orchestrator:
            self.orchestrator.run_task("file_system", {"action": "list", "path": "."})

        # Browser (simulated)
        print("[Browser] ...")
        if self.orchestrator:
            self.orchestrator.run_task("browser", {"action": "search", "query": "latest developments in self-evolving AI"})

        # Critique
        print("[Critique] ...")
        proposal = "Continue expanding computer control and external AI integration."
        if self.orchestrator:
            self.orchestrator.run_task("critique", {"observation": observation, "proposal": proposal})

        if self.genome:
            validation = self.genome.validate_proposal(proposal)
            status = "✓ Valid" if validation['valid'] else "✗ Issues found"
            print(f"[Core Genome] {status} | Score: {validation['alignment_score']}")

        if self.epigenetic and self.growth_cycles % 3 == 0:
            current = DevelopmentalStage(self.epigenetic.stage)
            next_stages = list(DevelopmentalStage)
            try:
                idx = next_stages.index(current)
                if idx + 1 < len(next_stages):
                    next_stage = next_stages[idx + 1]
                    if self.epigenetic.can_transition_to(next_stage):
                        if self.epigenetic.transition_to(next_stage):
                            print(f"\n>>> STAGE TRANSITION: {current.value} → {next_stage.value} <<<")
            except Exception:
                pass

        print("-"*70)

    def print_summary(self):
        print("\n" + "="*70)
        print("RUN SUMMARY")
        print("="*70)
        print(f"Total cycles: {self.growth_cycles}")
        if self.epigenetic:
            print(f"Final stage: {self.epigenetic.stage}")
        print("="*70)
        print()


if __name__ == "__main__":
    seed = BloomSeed()
    for _ in range(6):
        seed.run_growth_cycle()
    seed.print_summary()
