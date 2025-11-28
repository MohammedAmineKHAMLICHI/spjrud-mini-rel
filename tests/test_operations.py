import pytest

from minirel.operations import (
    difference,
    natural_join,
    project,
    rename_attribute,
    rename_relation,
    select,
    union,
)
from minirel.relation import Relation


def make_relation():
    return Relation("R", ["id", "value"], [{"id": 1, "value": "a"}, {"id": 2, "value": "b"}])


def test_select_filters_rows():
    rel = make_relation()
    result = select(rel, lambda row: row["id"] == 1)
    assert result.rows == [{"id": 1, "value": "a"}]


def test_project_reduces_schema():
    rel = make_relation()
    projected = project(rel, ["value"])
    assert projected.attributes == ["value"]
    assert projected.rows == [{"value": "a"}, {"value": "b"}]
    with pytest.raises(ValueError):
        project(rel, ["missing"])


def test_natural_join_on_common_attribute():
    left = Relation("L", ["id", "name"], [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}])
    right = Relation("R", ["id", "course"], [{"id": 1, "course": "BD"}, {"id": 3, "course": "ALG"}])
    joined = natural_join(left, right)
    assert joined.attributes == ["id", "name", "course"]
    assert joined.rows == [{"id": 1, "name": "Alice", "course": "BD"}]


def test_natural_join_cartesian_when_no_common_attributes():
    left = Relation("L", ["a"], [{"a": 1}, {"a": 2}])
    right = Relation("R", ["b"], [{"b": 3}, {"b": 4}])
    joined = natural_join(left, right)
    assert joined.attributes == ["a", "b"]
    assert len(joined.rows) == 4


def test_union_and_difference_require_same_schema():
    left = make_relation()
    right = Relation("R2", ["id", "value"], [{"id": 3, "value": "c"}])
    united = union(left, right)
    assert len(united.rows) == 3

    diffed = difference(united, right)
    assert {"id": 3, "value": "c"} not in diffed.rows

    incompatible = Relation("X", ["other"], [{"other": 1}])
    with pytest.raises(ValueError):
        union(left, incompatible)
    with pytest.raises(ValueError):
        difference(left, incompatible)


def test_rename_operations():
    rel = make_relation()
    renamed_rel = rename_relation(rel, "R2")
    assert renamed_rel.name == "R2"

    renamed_attr = rename_attribute(rel, "value", "val")
    assert "val" in renamed_attr.attributes
    assert all("val" in row for row in renamed_attr.rows)

    with pytest.raises(ValueError):
        rename_attribute(rel, "missing", "x")
    with pytest.raises(ValueError):
        rename_attribute(rel, "id", "value")
