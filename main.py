"""Simple CLI interface for generating a schedule."""

import json
from datetime import datetime
from pathlib import Path
from typing import List

from models import Parent
from scheduler import schedule
from excel_import import load_parents_from_excel


CONFIG_FILE = Path("config.json")


def load_parents(data: List[dict]) -> List[Parent]:
    parents = []
    for p in data:
        parents.append(
            Parent(
                name=p["name"],
                quota=p.get("quota", 0),
                preferences=p.get("preferences", {}),
            )
        )
    return parents


def main() -> None:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file {CONFIG_FILE} not found")

    with CONFIG_FILE.open() as fh:
        config = json.load(fh)

    start = datetime.strptime(config["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(config["end_date"], "%Y-%m-%d").date()
    closed = [datetime.strptime(d, "%Y-%m-%d").date() for d in config.get("closed_days", [])]

    if "excel_file" in config:
        parents = load_parents_from_excel(config["excel_file"])
    else:
        parents = load_parents(config.get("parents", []))

    sched = schedule(parents, start, end, closed_days=closed)

    for day, names in sorted(sched.items()):
        printable = ", ".join(names) if names else "--"
        print(f"{day} -> {printable}")


if __name__ == "__main__":
    main()
