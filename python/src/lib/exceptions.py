class UnreachableCodeError(AssertionError):
    """
    Mark a branch as unreachable.

    This is to aid static analysers.
    """
