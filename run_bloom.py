#!/usr/bin/env python3
"""
Run Bloom Collective as a local goal-oriented program.
"""

import argparse
import json

from local_agent import LocalBloomAgent


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Bloom Collective locally.")
    parser.add_argument("--goal", help="Goal for Bloom to execute.")
    parser.add_argument("--json", action="store_true", help="Print full JSON result.")
    args = parser.parse_args()

    agent = LocalBloomAgent()

    if args.goal:
        result = agent.execute_goal(args.goal)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(result["summary"])
        return 0 if result["status"] == "success" else 1

    print("Bloom Collective local agent. Type 'exit' to quit.")
    while True:
        try:
            goal = input("Goal> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0

        if goal.lower() in {"exit", "quit"}:
            return 0
        if not goal:
            continue

        result = agent.execute_goal(goal)
        print(result["summary"])


if __name__ == "__main__":
    raise SystemExit(main())
