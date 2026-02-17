from __future__ import annotations
from enum import Enum
from typing import Optional

from .exceptions import OkwAssertionError


class OkwToken(str, Enum):
    IGNORE = "$IGNORE"
    EMPTY = "$EMPTY"
    DELETE = "$DELETE"


class OkwYesNo(str, Enum):
    """OKW existence expectation: YES means 'must exist', NO means 'must not exist'."""
    YES = "YES"
    NO = "NO"


def normalize_token_candidate(value: object) -> str:
    return str(value).strip()


def parse_token(value: object | None) -> Optional[OkwToken]:
    if value is None:
        return None
    s = normalize_token_candidate(value).upper()
    if s == OkwToken.IGNORE.value:
        return OkwToken.IGNORE
    if s == OkwToken.EMPTY.value:
        return OkwToken.EMPTY
    if s == OkwToken.DELETE.value:
        return OkwToken.DELETE
    return None


def parse_yes_no(value: object) -> OkwYesNo:
    """Parses a YES/NO value. Accepts YES/NO, TRUE/FALSE, 1/0 (case-insensitive).

    Returns OkwYesNo.YES or OkwYesNo.NO.
    Raises ValueError if the value is not a recognized YES/NO variant.
    """
    s = str(value).strip().upper()
    if s in ("YES", "TRUE", "1"):
        return OkwYesNo.YES
    if s in ("NO", "FALSE", "0"):
        return OkwYesNo.NO
    raise ValueError(f"Expected YES or NO, got '{value}'")


def assert_exists(actual: bool, expected: OkwYesNo, *, context: str | None = None) -> None:
    """Asserts that an existence check matches the expected YES/NO value.

    Arguments:
    - actual: True if the element exists, False if not.
    - expected: OkwYesNo.YES (must exist) or OkwYesNo.NO (must not exist).
    - context: Optional context string for error messages.

    Raises OkwAssertionError if actual does not match expected.
    """
    if expected == OkwYesNo.YES and not actual:
        prefix = f"{context}\n" if context else ""
        raise OkwAssertionError(f"{prefix}Expected to exist (YES), but does not exist.")
    if expected == OkwYesNo.NO and actual:
        prefix = f"{context}\n" if context else ""
        raise OkwAssertionError(f"{prefix}Expected to NOT exist (NO), but exists.")


def is_ignore(value: object | None) -> bool:
    return parse_token(value) == OkwToken.IGNORE


def is_empty_token(value: object | None) -> bool:
    return parse_token(value) == OkwToken.EMPTY


def is_delete_token(value: object | None) -> bool:
    return parse_token(value) == OkwToken.DELETE
