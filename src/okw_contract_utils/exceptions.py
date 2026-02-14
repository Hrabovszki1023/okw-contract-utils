class OkwAssertionError(AssertionError):
    """Raised when a contract/matcher assertion fails."""


class OkwTimeoutError(TimeoutError):
    """Raised when a wait/timeout condition is not met in time."""


class OkwAssertionError(AssertionError):
    """Raised when a contract/matcher assertion fails."""


class OkwTimeoutError(TimeoutError):
    """Raised when a wait/timeout condition is not met in time."""


class OkwConfigError(RuntimeError):
    """Raised for configuration/value-resolution errors (e.g., missing $MEM keys)."""
