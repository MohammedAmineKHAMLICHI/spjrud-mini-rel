# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Jeu minimal de relations d'exemple intégrées (domaine étudiant/cours).

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

from typing import Dict

from .relation import Relation


def university_examples() -> Dict[str, Relation]:
    """Renvoie quelques relations dans le domaine étudiant/cours classique."""
    student = Relation(
        "STUDENT",
        ["sid", "name", "year"],
        [
            {"sid": 1, "name": "Alice", "year": 1},
            {"sid": 2, "name": "Bob", "year": 2},
            {"sid": 3, "name": "Chloe", "year": 2},
            {"sid": 4, "name": "David", "year": 3},
        ],
    )

    course = Relation(
        "COURSE",
        ["cid", "title"],
        [
            {"cid": "BD1", "title": "Bases de donnees I"},
            {"cid": "ALG", "title": "Algorithmique"},
            {"cid": "IA", "title": "Intelligence artificielle"},
        ],
    )

    enrolled = Relation(
        "ENROLLED",
        ["sid", "cid"],
        [
            {"sid": 1, "cid": "BD1"},
            {"sid": 2, "cid": "BD1"},
            {"sid": 2, "cid": "ALG"},
            {"sid": 3, "cid": "IA"},
            {"sid": 4, "cid": "ALG"},
        ],
    )
    return {"STUDENT": student, "COURSE": course, "ENROLLED": enrolled}
