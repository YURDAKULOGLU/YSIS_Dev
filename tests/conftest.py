import os


def pytest_configure() -> None:
    """
    Enable optional smoke tests automatically when dependencies are available.
    """
    if os.getenv("PLAYWRIGHT_E2E") is None:
        try:
            import playwright  # noqa: F401
        except Exception:
            pass
        else:
            os.environ["PLAYWRIGHT_E2E"] = "1"

    if os.getenv("TESTCONTAINERS_SMOKE") is None:
        try:
            import testcontainers  # noqa: F401
        except Exception:
            pass
        else:
            os.environ["TESTCONTAINERS_SMOKE"] = "1"
