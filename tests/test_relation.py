import pytest

from minirel.relation import Relation


def test_relation_validation_removes_duplicates():
    rel = Relation(
        "R",
        ["a", "b"],
        [
            {"a": 1, "b": 2},
            {"a": 1, "b": 2},  # duplicate should be removed
            {"a": 2, "b": 3},
        ],
    )
    assert len(rel.rows) == 2
    assert rel.attributes == ["a", "b"]


def test_relation_rejects_duplicate_attributes():
    with pytest.raises(ValueError):
        Relation("R", ["a", "a"], [])


def test_relation_row_schema_mismatch():
    with pytest.raises(ValueError):
        Relation("R", ["a", "b"], [{"a": 1}])
