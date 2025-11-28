# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Parseur pour un mini-langage textuel proche de SPJRUD.

Auteur : Mohammed Amine KHAMLICHI

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

from __future__ import annotations

import re
from typing import Dict, List

from .operations import (
    difference,
    natural_join,
    project,
    rename_attribute,
    rename_relation,
    select,
    union,
)
from .relation import Relation

_SELECT_RE = re.compile(r"^SELECT\s+(?P<cond>.+?)\s+FROM\s+(?P<rel>\w+)$", re.IGNORECASE)
_PROJECT_RE = re.compile(r"^PROJECT\s+(?P<attrs>[\w,\s]+)\s+FROM\s+(?P<rel>\w+)$", re.IGNORECASE)
_JOIN_RE = re.compile(r"^JOIN\s+(?P<left>\w+)\s*,\s*(?P<right>\w+)$", re.IGNORECASE)
_UNION_RE = re.compile(r"^UNION\s+(?P<left>\w+)\s*,\s*(?P<right>\w+)$", re.IGNORECASE)
_DIFF_RE = re.compile(r"^DIFF\s+(?P<left>\w+)\s*,\s*(?P<right>\w+)$", re.IGNORECASE)
_REN_ATTR_RE = re.compile(
    r"^RENAME\s+ATTR\s+(?P<old>[\w#]+)\s+TO\s+(?P<new>[\w#]+)\s+IN\s+(?P<rel>\w+)$",
    re.IGNORECASE,
)
_REN_REL_RE = re.compile(r"^RENAME\s+REL\s+(?P<old>\w+)\s+TO\s+(?P<new>\w+)$", re.IGNORECASE)


def _parse_literal(token: str):
    """Convertit un jeton texte en valeur Python (int, float, bool ou str)."""
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        inner = token[1:-1]
        inner = (
            inner.replace(r"\'", "'")
            .replace(r"\"", '"')
            .replace(r"\,", ",")
            .replace(r"\>", ">")
            .replace(r"\\", "\\")
        )
        return inner
    lowered = token.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if re.fullmatch(r"-?\d+", token):
        return int(token)
    if re.fullmatch(r"-?\d+\.\d+", token):
        return float(token)
    return token


def _parse_condition(condition: str):
    """
    Parse a simple condition of the form "attr op value".

    The right-hand side can be a literal or another attribute name. Supported
    operators: =, !=, <>, <, <=, >, >=.
    """
    m = re.match(
        r"^\s*(?P<left>[A-Za-z_#][\w#]*)\s*(?P<op>>=|<=|<>|!=|=|<|>)\s*(?P<right>.+?)\s*$",
        condition,
    )
    if not m:
        raise ValueError(f"invalid selection condition: {condition}")
    left = m.group("left")
    op = m.group("op")
    right_raw = m.group("right").strip()

    is_attr_ref = False
    if (right_raw.startswith("'") and right_raw.endswith("'")) or (
        right_raw.startswith('"') and right_raw.endswith('"')
    ):
        right_value = _parse_literal(right_raw)
    else:
        if re.fullmatch(r"[A-Za-z_#][\w#]*", right_raw):
            is_attr_ref = True
            right_value = right_raw
        else:
            right_value = _parse_literal(right_raw)

    op = "!=" if op == "<>" else op

    def predicate(row: dict) -> bool:
        if left not in row:
            raise ValueError(f"attribute {left} not found in relation")
        left_val = row[left]
        if is_attr_ref:
            if right_value not in row:
                raise ValueError(f"attribute {right_value} not found in relation")
            right_val = row[right_value]
        else:
            right_val = right_value
        if op == "=":
            return left_val == right_val
        if op == "!=":
            return left_val != right_val
        if op == "<":
            return left_val < right_val
        if op == "<=":
            return left_val <= right_val
        if op == ">":
            return left_val > right_val
        if op == ">=":
            return left_val >= right_val
        raise ValueError(f"unsupported operator {op}")

    return predicate


def _split_attributes(attr_text: str) -> List[str]:
    return [part.strip() for part in attr_text.split(",") if part.strip()]


def _get_relation(env: Dict[str, Relation], name: str) -> Relation:
    if name not in env:
        raise ValueError(f"relation {name} is not defined")
    return env[name]


# --- SQF-like parser (prefix @select/@project/@rename, infix @join/@union/@minus) ---

PREFIX_OPS = {"select", "project", "rename", "s", "p", "r"}
INFIX_OPS = {"join", "union", "minus", "diff"}


def _tokenize_sqf(expr: str):
    """
    Tokenize SQF-style expressions.

    Tokens are tuples (kind, value) where kind is among: ATWORD, IDENT, BRACES,
    LPAREN, RPAREN.
    """
    tokens = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isspace():
            i += 1
            continue
        if ch == "(":
            tokens.append(("LPAREN", ch))
            i += 1
            continue
        if ch == ")":
            tokens.append(("RPAREN", ch))
            i += 1
            continue
        if ch == "@":
            j = i + 1
            while j < len(expr) and expr[j].isalpha():
                j += 1
            tokens.append(("ATWORD", expr[i + 1 : j].lower()))
            i = j
            continue
        if ch == "*":
            tokens.append(("ATWORD", "join"))
            i += 1
            continue
        if ch == "-":
            tokens.append(("ATWORD", "minus"))
            i += 1
            continue
        if ch == "{":
            depth = 1
            j = i + 1
            buf = []
            while j < len(expr) and depth > 0:
                c = expr[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                if depth > 0:
                    buf.append(c)
                j += 1
            tokens.append(("BRACES", "".join(buf)))
            i = j
            continue
        if ch.isalnum() or ch in "_#.":
            j = i + 1
            while j < len(expr) and (expr[j].isalnum() or expr[j] in "_#."):
                j += 1
            tokens.append(("IDENT", expr[i:j]))
            i = j
            continue
        # ignore stray characters such as commas
        i += 1
    return tokens


class _SqfParser:
    def __init__(self, tokens, env: Dict[str, Relation]):
        self.tokens = tokens
        self.pos = 0
        self.env = env

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        tok = self._peek()
        if tok is not None:
            self.pos += 1
        return tok

    def _expect(self, kind: str) -> str:
        tok = self._advance()
        if tok is None or tok[0] != kind:
            raise ValueError(f"expected {kind}")
        return tok[1]

    def parse_expression(self) -> Relation:
        """
        expression := term (infix_op term)*
        All infix operators are treated left-associatively with equal precedence.
        """
        node = self.parse_term()
        while True:
            tok = self._peek()
            if tok and tok[0] == "ATWORD" and tok[1] in INFIX_OPS:
                op = self._advance()[1]
                right = self.parse_term()
                node = self._apply_infix(op, node, right)
            else:
                break
        return node

    def parse_term(self) -> Relation:
        """
        term := prefix_chain factor
        prefix_chain := (prefix_op BRACES)*
        factor := IDENT | '(' expression ')'
        Prefix operators bind tightly to the immediate factor to their right.
        """
        prefixes = []
        while True:
            tok = self._peek()
            if tok and tok[0] == "ATWORD" and tok[1] in PREFIX_OPS:
                op = self._advance()[1]
                content = self._expect("BRACES")
                prefixes.append((op, content))
            else:
                break

        node = self.parse_factor()
        # Apply collected prefixes from right to left (closest to factor first).
        for op, content in reversed(prefixes):
            node = self._apply_prefix(op, content, node)
        return node

    def parse_factor(self) -> Relation:
        tok = self._peek()
        if tok is None:
            raise ValueError("unexpected end of expression")
        if tok[0] == "LPAREN":
            self._advance()
            node = self.parse_expression()
            self._expect("RPAREN")
            return node
        if tok[0] == "IDENT":
            name = self._advance()[1]
            return _get_relation(self.env, name)
        raise ValueError(f"unexpected token {tok}")

    def _apply_prefix(self, op: str, content: str, rel: Relation) -> Relation:
        if op in {"select", "s"}:
            predicate = _parse_condition(content)
            return select(rel, predicate)
        if op in {"project", "p"}:
            attrs = _split_attributes(content)
            return project(rel, attrs)
        if op in {"rename", "r"}:
            pairs = [p.strip() for p in content.split(",") if p.strip()]
            if not pairs:
                return rel

            mapping = {}
            for pair in pairs:
                if ":" not in pair:
                    raise ValueError(f"invalid rename clause: {pair}")
                old, new = [x.strip() for x in pair.split(":", 1)]
                mapping[old] = new

            # Apply all renames simultaneously to support swaps (e.g., A->B, B->A).
            new_attributes = [mapping.get(attr, attr) for attr in rel.attributes]
            if len(new_attributes) != len(set(new_attributes)):
                raise ValueError(f"rename would create duplicate attributes in relation {rel.name}")
            new_rows = []
            for row in rel.rows:
                updated = {}
                for attr in rel.attributes:
                    updated[mapping.get(attr, attr)] = row[attr]
                new_rows.append(updated)
            return Relation.from_rows(rel.name, new_attributes, new_rows)
        raise ValueError(f"unsupported prefix operator @{op}")

    def _apply_infix(self, op: str, left: Relation, right: Relation) -> Relation:
        if op == "join":
            return natural_join(left, right)
        if op == "union":
            return union(left, right)
        if op in {"minus", "diff"}:
            return difference(left, right)
        raise ValueError(f"unsupported infix operator @{op}")


def _eval_sqf_expression(expr: str, env: Dict[str, Relation]) -> Relation:
    tokens = _tokenize_sqf(expr)
    parser = _SqfParser(tokens, env)
    result = parser.parse_expression()
    return result


def eval_expression(expr: str, env: Dict[str, Relation]) -> Relation:
    """
    Évalue une expression textuelle de type SPJRUD.

    L’environnement est un mapping nom -> Relation. Les expressions restent
    volontairement simples pour garder un parseur lisible, avec mots-clés
    insensibles à la casse.
    """
    expr = expr.strip()

    if m := _SELECT_RE.match(expr):
        condition = m.group("cond")
        rel_name = m.group("rel")
        relation = _get_relation(env, rel_name)
        predicate = _parse_condition(condition)
        return select(relation, predicate)

    if m := _PROJECT_RE.match(expr):
        attrs = _split_attributes(m.group("attrs"))
        rel_name = m.group("rel")
        relation = _get_relation(env, rel_name)
        return project(relation, attrs)

    if m := _JOIN_RE.match(expr):
        left = _get_relation(env, m.group("left"))
        right = _get_relation(env, m.group("right"))
        return natural_join(left, right)

    if m := _UNION_RE.match(expr):
        left = _get_relation(env, m.group("left"))
        right = _get_relation(env, m.group("right"))
        return union(left, right)

    if m := _DIFF_RE.match(expr):
        left = _get_relation(env, m.group("left"))
        right = _get_relation(env, m.group("right"))
        return difference(left, right)

    if m := _REN_ATTR_RE.match(expr):
        old = m.group("old")
        new = m.group("new")
        relation = _get_relation(env, m.group("rel"))
        return rename_attribute(relation, old, new)

    if m := _REN_REL_RE.match(expr):
        old_name = m.group("old")
        new_name = m.group("new")
        relation = _get_relation(env, old_name)
        return rename_relation(relation, new_name)

    # Fallback to the SQF-style parser (@select/@project/@rename with infix @join/@union/@minus)
    return _eval_sqf_expression(expr, env)
