import pytest

from minirel.examples import university_examples
from minirel.parser import eval_expression
from minirel.relation import Relation


def test_select_expression():
    env = university_examples()
    result = eval_expression("SELECT year >= 2 FROM STUDENT", env)
    assert all(row["year"] >= 2 for row in result.rows)
    assert len(result.rows) == 3


def test_project_expression():
    env = university_examples()
    projected = eval_expression("PROJECT name FROM STUDENT", env)
    assert projected.attributes == ["name"]
    assert {"name": "Alice"} in projected.rows


def test_join_expression():
    env = university_examples()
    joined = eval_expression("JOIN STUDENT, ENROLLED", env)
    assert "cid" in joined.attributes
    # ensure join happened on sid
    assert all(row["sid"] in [1, 2, 3, 4] for row in joined.rows)


def test_union_and_diff_expressions():
    env = {
        "R1": Relation("R1", ["a"], [{"a": 1}, {"a": 2}]),
        "R2": Relation("R2", ["a"], [{"a": 2}, {"a": 3}]),
    }
    united = eval_expression("UNION R1, R2", env)
    assert len(united.rows) == 3

    diffed = eval_expression("DIFF R1, R2", env)
    assert diffed.rows == [{"a": 1}]


def test_rename_expressions():
    env = {"R": Relation("R", ["x"], [{"x": 1}])}
    renamed_attr = eval_expression("RENAME ATTR x TO y IN R", env)
    assert renamed_attr.attributes == ["y"]

    renamed_rel = eval_expression("RENAME REL R TO S", env)
    assert renamed_rel.name == "S"


def test_unknown_relation():
    with pytest.raises(ValueError):
        eval_expression("SELECT a = 1 FROM UNKNOWN", {})


def test_sqf_style_macros():
    env = university_examples()
    # @s / @p are accepted shortcuts.
    seniors = eval_expression("@s{year>=2} STUDENT", env)
    assert all(row["year"] >= 2 for row in seniors.rows)

    joined = eval_expression("STUDENT @join ENROLLED", env)
    assert "cid" in joined.attributes

    diffed = eval_expression("@p{name} STUDENT - @p{name} STUDENT", env)
    assert diffed.rows == []

    swapped = eval_expression("@r{name:student, sid:id} STUDENT", env)
    assert swapped.attributes == ["id", "student", "year"]
