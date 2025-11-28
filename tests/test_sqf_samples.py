from pathlib import Path

import pytest

from minirel.sqf_loader import load_sqf

SAMPLES_DIR = Path("sqf_exemples/sqf_exemples_20160912/sqf_exemples")


@pytest.mark.skipif(not SAMPLES_DIR.exists(), reason="sample SQF folder not present")
def test_load_all_course_examples():
    errors = []
    for path in sorted(SAMPLES_DIR.glob("*.sqf")):
        try:
            env = load_sqf(str(path))
        except Exception as exc:  # noqa: BLE001 - fail with collected errors
            errors.append(f"{path.name}: {exc}")
            continue
        assert env, f"{path.name} produced an empty environment"
    if errors:
        pytest.fail("Errors while loading SQF samples:\n" + "\n".join(errors))
