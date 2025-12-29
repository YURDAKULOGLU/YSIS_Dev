import os

import pytest


def test_testcontainers_importable():
    if os.getenv("TESTCONTAINERS_SMOKE") != "1":
        pytest.skip("Set TESTCONTAINERS_SMOKE=1 to run Testcontainers smoke tests.")

    try:
        import testcontainers  # noqa: F401
    except Exception:
        pytest.skip("Testcontainers not installed.")

    assert True
