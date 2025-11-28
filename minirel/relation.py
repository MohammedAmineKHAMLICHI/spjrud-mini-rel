# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Modèle de relation utilisé par le moteur d’algèbre relationnelle.

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


class Relation:
    """
    Représente une relation (table) du modèle relationnel.

    Contenu :
    - un nom (informatif),
    - une liste ordonnée d’attributs,
    - des lignes (dict attribut -> valeur).

    Le constructeur valide le schéma et supprime les doublons en se basant
    sur l’ordre des attributs pour construire une clé hashable.
    """

    def __init__(self, name: str, attributes: List[str], rows: List[Dict[str, Any]]) -> None:
        self.name = name
        self.attributes = self._validate_attributes(attributes)
        self.rows = self._validate_rows(rows)

    @classmethod
    def from_rows(cls, name: str, attributes: List[str], rows: Iterable[Dict[str, Any]]) -> "Relation":
        """Constructeur pratique acceptant tout itérable de lignes."""
        return cls(name, list(attributes), list(rows))

    def _validate_attributes(self, attributes: List[str]) -> List[str]:
        if attributes is None:
            raise ValueError("attributes cannot be None")
        cleaned = [attr.strip() for attr in attributes]
        if len(cleaned) != len(set(cleaned)):
            raise ValueError("attributes must not contain duplicates")
        # Empty attribute lists are rare but possible in relational algebra;
        # the code tolerates them for completeness.
        return cleaned

    def _validate_rows(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        validated: List[Dict[str, Any]] = []
        seen: set[Tuple[Any, ...]] = set()
        for row in rows:
            if not isinstance(row, dict):
                raise ValueError("each row must be a dict mapping attribute -> value")
            keys = set(row.keys())
            if keys != set(self.attributes):
                raise ValueError(
                    f"row schema mismatch for relation {self.name}: expected {self.attributes}, got {sorted(keys)}"
                )
            key = tuple(row[attr] for attr in self.attributes)
            if key in seen:
                # silently drop duplicates to keep the relation set-like
                continue
            seen.add(key)
            validated.append({attr: row[attr] for attr in self.attributes})
        return validated

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self.rows)

    def __iter__(self):  # pragma: no cover - trivial
        return iter(self.rows)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Relation):
            return False
        if self.attributes != other.attributes:
            return False
        return self._row_set() == other._row_set()

    def _row_set(self) -> set[Tuple[Any, ...]]:
        """Représentation en ensemble des lignes pour comparer deux relations."""
        return {tuple(row[attr] for attr in self.attributes) for row in self.rows}

    def format_table(self) -> str:
        """
        Retourne une représentation tabulaire lisible en ASCII.

        Les relations sans attribut sont gérées explicitement.
        """
        title = f"Relation {self.name} ({len(self.attributes)} attrs, {len(self.rows)} rows)"
        if not self.attributes:
            if not self.rows:
                return f"{title}\n(no tuples)"
            tuples = "\n".join("<>" for _ in self.rows)
            return f"{title}\n{tuples}"

        widths = {attr: len(attr) for attr in self.attributes}
        for row in self.rows:
            for attr in self.attributes:
                widths[attr] = max(widths[attr], len(str(row[attr])))

        header = " | ".join(attr.ljust(widths[attr]) for attr in self.attributes)
        separator = "-+-".join("-" * widths[attr] for attr in self.attributes)
        body_lines = [
            " | ".join(str(row[attr]).ljust(widths[attr]) for attr in self.attributes)
            for row in self.rows
        ]
        body = "\n".join(body_lines)
        return f"{title}\n{header}\n{separator}\n{body}" if body_lines else f"{title}\n{header}\n{separator}\n(no rows)"

    def __str__(self) -> str:  # pragma: no cover - thin wrapper
        return self.format_table()
