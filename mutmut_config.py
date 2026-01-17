"""
mutmut configuration for mutation testing.

Mutation testing measures test quality by introducing bugs (mutations)
and checking if tests catch them.
"""


def pre_mutation(context):
    """Skip certain files from mutation testing."""
    # Skip test files themselves
    if "test_" in context.filename or "_test.py" in context.filename:
        return False

    # Skip migration files
    if "migrations" in context.filename:
        return False

    # Skip vendor code
    if "vendors" in context.filename:
        return False

    return True


