from __future__ import annotations

import re
from typing import Mapping

from .exceptions import OkwConfigError


# $MEM{KEY}
_MEM_RE = re.compile(r"\$MEM\{([A-Za-z0-9_\-\.]+)\}")


def expand_mem(text: str, store: Mapping[str, object]) -> str:
    """
    Expands $MEM{KEY} placeholders in the given text using the provided store.

    Rules:
    - Unknown key -> raises OkwConfigError (fail-fast, prevents silent noise)
    - None value -> treated as empty string
    - All occurrences are expanded
    """
    if text is None:
        return ""

    def repl(match: re.Match) -> str:
        key = match.group(1)
        if key not in store:
            raise OkwConfigError(f"Memorized key not found: {key}")
        val = store[key]
        return "" if val is None else str(val)

    return _MEM_RE.sub(repl, text)
