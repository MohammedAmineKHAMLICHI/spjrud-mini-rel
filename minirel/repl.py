# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""REPL simple pour expérimenter le moteur d’algèbre relationnelle SPJRUD.

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict

from .examples import university_examples
from .parser import eval_expression
from .relation import Relation
from .sqf_loader import load_sqf

PROMPT = "rel> "


def _print_help() -> None:
    print(
        "Commandes:\n"
        "  LIST                      lister les relations chargées\n"
        "  SHOW <Nom>                afficher une relation\n"
        "  EVAL <expr>               évaluer une expression (SELECT, PROJECT, JOIN, ...)\n"
        "  LOAD <chemin>             charger des relations depuis un fichier .sqf\n"
        "  HELP                      afficher l’aide\n"
        "  QUIT / EXIT               quitter le REPL\n"
    )


def _show_relation(rel: Relation) -> None:
    print(rel.format_table())


def _handle_command(line: str, env: Dict[str, Relation]) -> bool:
    stripped = line.strip()
    if not stripped:
        return True
    upper = stripped.upper()

    if upper == "HELP":
        _print_help()
        return True
    if upper == "LIST":
        print("Relations:", ", ".join(sorted(env.keys())) if env else "(none)")
        return True
    if upper.startswith("SHOW "):
        name = stripped.split(maxsplit=1)[1]
        rel = env.get(name)
        if rel is None:
            print(f"Unknown relation: {name}")
        else:
            _show_relation(rel)
        return True
    if upper.startswith("EVAL "):
        expr = stripped.split(maxsplit=1)[1]
        try:
            result = eval_expression(expr, env)
        except Exception as exc:  # noqa: BLE001 - surface parsing errors directly
            print(f"Error: {exc}")
            return True
        _show_relation(result)
        return True
    if upper.startswith("LOAD "):
        path_text = stripped.split(maxsplit=1)[1]
        path = Path(path_text)
        if not path.exists():
            print(f"File not found: {path}")
            return True
        try:
            loaded = load_sqf(str(path))
        except Exception as exc:  # noqa: BLE001 - user facing tool
            print(f"Error while loading {path}: {exc}")
            return True
        env.update(loaded)
        print(f"Loaded {len(loaded)} relation(s) from {path}")
        return True
    if upper in {"QUIT", "EXIT"}:
        return False

    print("Unrecognized command. Type HELP for usage.")
    return True


def main() -> None:
    env = university_examples()
    print("Mini relational algebra REPL. Type HELP to list commands.")
    try:
        while True:
            try:
                line = input(PROMPT)
            except EOFError:
                break
            if not _handle_command(line, env):
                break
    except KeyboardInterrupt:
        print()
        return


if __name__ == "__main__":
    # Allow loading an initial .sqf file passed as an argument for convenience.
    if len(sys.argv) > 1:
        initial_env = university_examples()
        try:
            loaded = load_sqf(sys.argv[1])
            initial_env.update(loaded)
        except Exception as exc:  # noqa: BLE001 - REPL should remain friendly
            print(f"Failed to load {sys.argv[1]}: {exc}")
            sys.exit(1)
        env = initial_env
        print(f"Loaded initial data set from {sys.argv[1]}")
        print("Starting REPL...")
        try:
            while True:
                line = input(PROMPT)
                if not _handle_command(line, env):
                    break
        except KeyboardInterrupt:
            print()
    else:
        main()
