"""Very small Tkinter GUI to trigger scheduling.

This GUI loads `config.json` and prints the generated schedule in a
scrollable text widget. It is intentionally simple and can be extended
as needed.
"""

import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext

from models import Parent
from scheduler import schedule
from excel_import import load_parents_from_excel

CONFIG_FILE = Path("config.json")


def load_config():
    with CONFIG_FILE.open() as fh:
        return json.load(fh)


def load_parents(data):
    return [Parent(name=p["name"], quota=p.get("quota", 0), preferences=p.get("preferences", {})) for p in data]


def run_schedule(text: scrolledtext.ScrolledText) -> None:
    conf = load_config()
    start = datetime.strptime(conf["start_date"], "%Y-%m-%d").date()
    end = datetime.strptime(conf["end_date"], "%Y-%m-%d").date()
    closed = [datetime.strptime(d, "%Y-%m-%d").date() for d in conf.get("closed_days", [])]

    if "excel_file" in conf:
        parents = load_parents_from_excel(conf["excel_file"])
    else:
        parents = load_parents(conf.get("parents", []))

    sched = schedule(parents, start, end, closed_days=closed)
    text.delete("1.0", tk.END)
    for day, names in sorted(sched.items()):
        printable = ", ".join(names) if names else "--"
        text.insert(tk.END, f"{day} -> {printable}\n")


def main() -> None:
    root = tk.Tk()
    root.title("Schema Visan")

    text = scrolledtext.ScrolledText(root, width=40, height=15)
    text.pack(padx=10, pady=10)

    btn = tk.Button(root, text="Generate Schedule", command=lambda: run_schedule(text))
    btn.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
