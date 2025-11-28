# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Opérateurs algébriques pour le sous-ensemble SPJRUD.

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

from typing import Callable, List

from .relation import Relation

Predicate = Callable[[dict], bool]


def select(relation: Relation, predicate: Predicate) -> Relation:
    """
    Sélection (sigma) des lignes satisfaisant le prédicat.

    Le prédicat reçoit chaque ligne sous forme de dict. Le schéma est conservé et
    les doublons sont éliminés par le constructeur Relation.
    """
    filtered = [row for row in relation.rows if predicate(row)]
    return Relation.from_rows(relation.name, relation.attributes, filtered)


def project(relation: Relation, attributes: List[str]) -> Relation:
    """
    Projection (pi) de `relation` sur les attributs fournis.

    L’ordre des attributs est préservé. Provoque ValueError si un attribut manque.
    """
    missing = [attr for attr in attributes if attr not in relation.attributes]
    if missing:
        raise ValueError(f"projection attributes not in relation {relation.name}: {missing}")
    projected_rows = [{attr: row[attr] for attr in attributes} for row in relation.rows]
    return Relation.from_rows(relation.name, attributes, projected_rows)


def natural_join(left: Relation, right: Relation) -> Relation:
    """
    Jointure naturelle de deux relations.

    Les attributs communs servent de clés ; en l’absence d’attribut commun, le
    résultat équivaut à un produit cartésien.
    """
    common = [attr for attr in left.attributes if attr in right.attributes]
    right_only = [attr for attr in right.attributes if attr not in common]
    new_attributes = left.attributes + right_only

    result_rows = []
    for lrow in left.rows:
        for rrow in right.rows:
            if common:
                if any(lrow[attr] != rrow[attr] for attr in common):
                    continue
            merged = {**lrow}
            merged.update({attr: rrow[attr] for attr in right_only})
            result_rows.append(merged)
    return Relation.from_rows(f"{left.name}_JOIN_{right.name}", new_attributes, result_rows)


def rename_relation(relation: Relation, new_name: str) -> Relation:
    """Copie de `relation` avec un nom différent."""
    return Relation.from_rows(new_name, relation.attributes, relation.rows)


def rename_attribute(relation: Relation, old: str, new: str) -> Relation:
    """
    Renomme un attribut dans la relation.

    Provoque ValueError si l’attribut n’existe pas ou si le nouveau nom crée un doublon.
    """
    if old not in relation.attributes:
        raise ValueError(f"attribute {old} not found in relation {relation.name}")
    if new != old and new in relation.attributes:
        raise ValueError(f"attribute {new} already exists in relation {relation.name}")

    new_attributes = [new if attr == old else attr for attr in relation.attributes]
    new_rows = []
    for row in relation.rows:
        updated = {}
        for attr, value in row.items():
            key = new if attr == old else attr
            updated[key] = value
        new_rows.append(updated)
    return Relation.from_rows(relation.name, new_attributes, new_rows)


def union(left: Relation, right: Relation) -> Relation:
    """
    Union de deux relations de schéma identique.

    Les schémas doivent correspondre. Si l’ordre diffère, la droite est réordonnée
    avant l’union.
    """
    if set(left.attributes) != set(right.attributes):
        raise ValueError("cannot union relations with different schemas")
    if left.attributes == right.attributes:
        combined = list(left.rows) + list(right.rows)
        return Relation.from_rows(f"{left.name}_UNION_{right.name}", left.attributes, combined)

    # Reorder right rows to match the left attribute order.
    reordered_right = [{attr: row[attr] for attr in left.attributes} for row in right.rows]
    combined = list(left.rows) + reordered_right
    return Relation.from_rows(f"{left.name}_UNION_{right.name}", left.attributes, combined)


def difference(left: Relation, right: Relation) -> Relation:
    """
    Différence ensembliste `left - right`.

    Les schémas doivent correspondre. Si l’ordre diffère, la droite est réordonnée
    avant soustraction.
    """
    if set(left.attributes) != set(right.attributes):
        raise ValueError("cannot diff relations with different schemas")
    if left.attributes != right.attributes:
        right_rows = [{attr: row[attr] for attr in left.attributes} for row in right.rows]
    else:
        right_rows = right.rows
    right_keys = {tuple(row[attr] for attr in left.attributes) for row in right_rows}
    remaining = [row for row in left.rows if tuple(row[attr] for attr in left.attributes) not in right_keys]
    return Relation.from_rows(f"{left.name}_DIFF_{right.name}", left.attributes, remaining)
