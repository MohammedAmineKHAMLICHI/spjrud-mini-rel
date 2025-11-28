from pathlib import Path

import pytest

from minirel.sqf_loader import load_sqf


def test_load_basic_sqf(tmp_path: Path):
    content = """
    % sample file
    @let STUDENT = @relation [id, name] {
      <1, "Alice">
      <2, "Bob">
    }

    @let SENIORS = SELECT id >= 2 FROM STUDENT
    """
    path = tmp_path / "sample.sqf"
    path.write_text(content, encoding="utf-8")

    env = load_sqf(str(path))
    assert set(env.keys()) == {"STUDENT", "SENIORS"}
    assert len(env["STUDENT"].rows) == 2
    assert env["SENIORS"].rows == [{"id": 2, "name": "Bob"}]


def test_tuple_arity_mismatch_raises(tmp_path: Path):
    bad = "@let R = @relation [a, b] { <1> }"
    path = tmp_path / "bad.sqf"
    path.write_text(bad, encoding="utf-8")
    with pytest.raises(ValueError):
        load_sqf(str(path))
