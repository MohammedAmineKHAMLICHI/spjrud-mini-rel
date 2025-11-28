# Auteur : Mohammed Amine KHAMLICHI
# LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/
"""Mini relational algebra engine (SPJRUD) package.

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/"""

__all__ = [
    "Relation",
    "select",
    "project",
    "natural_join",
    "rename_relation",
    "rename_attribute",
    "union",
    "difference",
    "eval_expression",
    "load_sqf",
]

__author__ = "Mohammed Amine KHAMLICHI"

from .relation import Relation
from .operations import (
    select,
    project,
    natural_join,
    rename_relation,
    rename_attribute,
    union,
    difference,
)
from .parser import eval_expression
from .sqf_loader import load_sqf
