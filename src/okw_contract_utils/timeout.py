from __future__ import annotations

import time
from typing import Callable, TypeVar, Optional

from .exceptions import OkwTimeoutError

T = TypeVar("T")


def wait_until(
    predicate: Callable[[], T],
    *,
    timeout_s: float,
    interval_s: float = 0.2,
    timeout_message: str = "Condition not met within timeout.",
) -> T:
    if timeout_s <= 0:
        raise ValueError("timeout_s must be > 0")
    if interval_s <= 0:
        raise ValueError("interval_s must be > 0")

    deadline = time.monotonic() + timeout_s
    last: Optional[T] = None

    while True:
        last = predicate()
        if last:
            return last
        if time.monotonic() >= deadline:
            raise OkwTimeoutError(timeout_message)
        time.sleep(interval_s)
