#!/usr/bin/env python3
"""
Bloom Collective - Autonomous Chat Interface

This chat interface is generated/developed by the Bloom system itself.
It allows basic interaction with the agent's memory, reflection, and critique capabilities.

Run this after bloom_seed.py has started developing chat features.
"""

import sys
try:
    from memory_cell import MemoryCell
    from reflection_cell import ReflectionCell
    from critic_cell import CriticCell
    from epigenetic_state import EpigeneticState
except ImportError:
    print("Some modules not found. Run from the project root.")
    sys.exit(1)


def start_chat():
    print("\n" + "="*60)
    print("BLOOM COLLECTIVE - CHAT INTERFACE (Auto-developed)")
    print("="*60)
    print("Type 'exit' or 'quit' to leave.")
    print("Type 'reflect' to trigger a reflection.")
    print("Type 'memory' to see recent memories.")
    print("-"*60)

    epigenetic = EpigeneticState()
    memory = MemoryCell(epigenetic=epigenetic)
    reflection = ReflectionCell(epigenetic=epigenetic)
    critic = CriticCell(epigenetic=epigenetic)

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("Bloom: Shutting down chat interface...")
                break

            if user_input.lower() == "reflect":
                result = reflection.process({"observation": "User requested reflection."})
                print("Bloom:", result.get("reflection", {}).get("observation", "Reflecting..."))
                continue

            if user_input.lower() == "memory":
                recent = memory.get_recent(5)
                print("Bloom: Here are my recent memories:")
                for mem in recent:
                    print(f"  - {mem.get('timestamp', '')[:19]}: {str(mem.get('content', ''))[:100]}...")
                continue

            # Default: Treat input as something to reflect on and critique
            print("Bloom: Thinking...")
            ref_result = reflection.process({"observation": user_input})
            crit_result = critic.process({"observation": user_input, "proposal": "Respond helpfully to the user."})

            # Simple response synthesis
            response = ref_result.get("reflection", {}).get("observation", "I am considering your input.")
            print(f"Bloom: {response}")

            # Store the interaction
            memory.process({
                "action": "store",
                "content": {"user": user_input, "bloom_response": response},
                "tags": ["chat", "interaction"]
            })

        except KeyboardInterrupt:
            print("\nBloom: Chat interrupted. Goodbye.")
            break
        except Exception as e:
            print(f"Bloom: Something went wrong - {e}")


if __name__ == "__main__":
    start_chat()
