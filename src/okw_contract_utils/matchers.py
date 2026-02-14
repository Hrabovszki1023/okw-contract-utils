from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import re

from .exceptions import OkwAssertionError
from .text import normalize_newlines


class MatchMode(str, Enum):
    EXACT = "EXACT"
    WCM = "WCM"
    REGX = "REGX"


@dataclass(frozen=True)
class MatchResult:
    ok: bool
    message: str = ""


def is_match(actual: str, expected: str, mode: MatchMode) -> MatchResult:
    a = normalize_newlines(actual or "")
    e = normalize_newlines(expected or "")

    if mode == MatchMode.EXACT:
        if a == e:
            return MatchResult(True)
        return MatchResult(False, _msg(mode, e, a))

    if mode == MatchMode.WCM:
        if e in a:
            return MatchResult(True)
        return MatchResult(False, _msg(mode, e, a))

    if mode == MatchMode.REGX:
        try:
            if re.search(e, a, flags=re.MULTILINE):
                return MatchResult(True)
            return MatchResult(False, _msg(mode, e, a))
        except re.error as ex:
            return MatchResult(False, f"Invalid REGX pattern: {e!r}. Regex error: {ex}")

    return MatchResult(False, f"Unsupported match mode: {mode}")


def assert_match(actual: str, expected: str, mode: MatchMode, *, context: str | None = None) -> None:
    res = is_match(actual, expected, mode)
    if not res.ok:
        prefix = f"{context}\n" if context else ""
        raise OkwAssertionError(prefix + res.message)


def _msg(mode: MatchMode, expected: str, actual: str) -> str:
    return (
        f"Match failed (mode={mode}).\n"
        f"Expected: {expected!r}\n"
        f"Actual:   {actual!r}"
    )
