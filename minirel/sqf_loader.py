# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Chargeur de fichiers .sqf simplifiés (relations et expressions SPJRUD).

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

import re
from typing import Dict, List

from .parser import eval_expression
from .relation import Relation


def _strip_comments(text: str) -> str:
    """Supprime les segments de commentaires (%) avant parsing."""
    cleaned_lines = []
    for line in text.splitlines():
        if "%" in line:
            line = line.split("%", 1)[0]
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def _parse_literal(token: str):
    """Convertit un jeton texte en entier, flottant, booléen ou chaîne."""
    token = token.strip()
    if token == "":
        return ""
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    if re.fullmatch(r"-?\d+\.\d+", token):
        return float(token)
    lowered = token.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return token


def _parse_tuple_values(text: str) -> List[str]:
    """
    Découpe le contenu brut "<...>" en valeurs individuelles non citées.

    Gère les virgules dans des valeurs entre guillemets et quelques échappements
    (virgule, chevron, guillemets).
    """
    values: List[str] = []
    buf: List[str] = []
    in_quote = False
    quote_char = ""
    escape = False
    for ch in text:
        if escape:
            buf.append(ch)
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if in_quote:
            if ch == quote_char:
                in_quote = False
                continue
            buf.append(ch)
            continue
        if ch in ("'", '"'):
            # Treat as quote delimiter only when starting a value (buffer empty or whitespace-only).
            if not buf or all(c.isspace() for c in buf):
                in_quote = True
                quote_char = ch
                continue
            # Otherwise the character is part of the value (e.g., l'humour).
            buf.append(ch)
            continue
        if ch == ",":
            values.append("".join(buf).strip())
            buf = []
            continue
        buf.append(ch)
    trailing = "".join(buf).strip()
    if trailing or text.strip():
        values.append(trailing)
    return values


def _parse_relation_block(name: str, body: str) -> Relation:
    """Parse un bloc @relation [attrs] { <...> } et construit la Relation associée."""
    match = re.match(r"@relation\s*\[(?P<attrs>.*?)\]\s*\{(?P<data>.*)\}\s*$", body, re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError(f"invalid relation definition for {name}")
    attr_text = match.group("attrs")
    data_text = match.group("data")

    attributes = [attr.strip() for attr in attr_text.split(",") if attr.strip() != ""]
    tuple_texts = re.findall(r"<(.*?)>", data_text, re.DOTALL)

    rows = []
    for tup in tuple_texts:
        raw_values = _parse_tuple_values(tup)
        if len(raw_values) != len(attributes):
            raise ValueError(
                f"tuple arity mismatch in relation {name}: expected {len(attributes)}, got {len(raw_values)}"
            )
        row = {attr: _parse_literal(val) for attr, val in zip(attributes, raw_values)}
        rows.append(row)
    return Relation(name, attributes, rows)


def load_sqf(path: str) -> Dict[str, Relation]:
    """
    Charge un fichier .sqf simplifié et retourne un dictionnaire nom -> Relation.

    Construit à partir de :
      - @let NAME = @relation [a, b] { <1,2> <3,4> }
      - @let NAME = <expression SPJRUD simplifiée>

    Les lignes débutant par % sont ignorées. Les directives comme @print sont filtrées.
    """
    with open(path, "r", encoding="utf-8") as fh:
        raw_text = fh.read()
    stripped = _strip_comments(raw_text)
    # Remove helper directives that are not part of @let blocks.
    filtered_lines = []
    for line in stripped.splitlines():
        stripped_line = line.strip()
        if not stripped_line:
            continue
        if stripped_line.lower().startswith("@print") or stripped_line.lower().startswith("@allow"):
            continue
        filtered_lines.append(stripped_line)
    text = "\n".join(filtered_lines)

    env: Dict[str, Relation] = {}
    let_pattern = re.compile(r"@let\s+(?P<name>\w+)\s*=\s*", re.IGNORECASE)
    matches = list(let_pattern.finditer(text))
    for idx, match in enumerate(matches):
        name = match.group("name")
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        if body.lower().startswith("@relation"):
            relation = _parse_relation_block(name, body)
            env[name] = relation
        else:
            expr = body.strip().strip(";")
            relation = eval_expression(expr, env)
            env[name] = relation
    return env
