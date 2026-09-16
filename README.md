# okw-contract-utils

[![PyPI](https://img.shields.io/pypi/v/okw-contract-utils)](https://pypi.org/project/okw-contract-utils/)
[![Python](https://img.shields.io/pypi/pyversions/okw-contract-utils)](https://pypi.org/project/okw-contract-utils/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

Shared contracts for the [OKW4Robot](https://github.com/Hrabovszki1023/robotframework-okw4robot) ecosystem — matchers, tokens, and value expansion used by all OKW libraries.

> **Deutsche Version:** [README_de.md](README_de.md)

## Signal vs. NOISE

| Signal (your test) | NOISE (hidden in contract-utils) |
|---|---|
| `VerifyValue Status Logged in` | Match mode selection (EXACT/WCM/REGX) |
| `${IGNORE}` → skip step | Token parsing, case normalization |
| `$MEM{TOKEN}` → stored value | Dictionary lookup, missing-key error handling |

## Install

```bash
pip install okw-contract-utils
```

## Features

- **Match modes**: EXACT (equality), WCM (wildcard via fnmatch: `*` = any chars, `?` = one char), REGX (regex via `re.search`)
- **Value expansion**: `$MEM{KEY}` placeholder expansion via `expand_mem(text, store)`
- **Global tokens**: `$IGNORE`, `$EMPTY`, `$DELETE`
- **YES/NO existence model**: `parse_yes_no()`, `assert_exists()`
- **Timeout helper**: `wait_until(predicate, timeout_s, interval_s)`
- **Exceptions**: `OkwAssertionError`, `OkwTimeoutError`, `OkwConfigError`

## Non-goals

- No Robot Framework keywords
- No SSH/Selenium/GUI dependencies
- No environment/provider logic

## Match Modes

All match modes normalize newlines (`\r\n` to `\n`) before comparing.

| Mode | Function | Description |
|------|----------|-------------|
| EXACT | `a == e` | Exact string equality |
| WCM | `fnmatch(a, e)` | Wildcard pattern match (`*` = any chars, `?` = one char) |
| REGX | `re.search(e, a)` | Regular expression search (multiline) |

Usage:

```python
from okw_contract_utils import assert_match, MatchMode

assert_match("Hello World", "Hello World", MatchMode.EXACT)
assert_match("Hello World", "Hello*", MatchMode.WCM)
assert_match("Hello World", r"Hello\s+\w+", MatchMode.REGX)
```

## Global Token Model

OKW defines a small set of global tokens. Tokens are **case-insensitive** and evaluated after
trimming surrounding whitespace.

Tokens are **defined here** (contract) and may be **implemented selectively** by concrete keyword
libraries. Not every library must implement every token.

### Tokens

- `$IGNORE` (control token)
  - Meaning: the keyword becomes a **no-op** (PASS).
  - Use case: disable single steps inside reusable sequences without control structures.

- `$EMPTY` (value-intent token)
  - Meaning: expected/target value is **empty**.
  - Use case: explicitly verify that a value is empty (e.g. stdout/stderr is empty), even if the
    underlying system does not represent emptiness strictly as `""`.

- `$DELETE` (action-intent token)
  - Meaning: perform an explicit **delete/clear** action.
  - Typically used in GUI libraries (e.g. clear text fields).
  - Libraries that cannot implement delete semantics simply do not support `$DELETE`.

### Robot Framework variables

Robot variables like `${IGNORE}` are expanded by Robot **before** the keyword is executed.
If `${IGNORE}` is not defined, Robot fails before the library can handle it.

Recommended suite variables:

```robot
*** Variables ***
${IGNORE}    $IGNORE
${EMPTY}     $EMPTY
${DELETE}    $DELETE
```

### Evaluation order (contract)

For keyword parameters of type Value/Expected/Command:

* Robot Framework variable expansion (e.g. ${IGNORE} -> $IGNORE)
* OKW value expansion (e.g. $MEM{KEY})
* Token parsing ($IGNORE, $EMPTY, $DELETE)
* Keyword semantics / adapter execution

## YES/NO Existence Model

For keywords that verify whether a resource exists (files, directories, UI elements, etc.),
OKW defines a standard YES/NO model.

### Accepted values

| Input | Parsed as |
|-------|-----------|
| `YES`, `TRUE`, `1` | YES (must exist) |
| `NO`, `FALSE`, `0` | NO (must not exist) |

All values are **case-insensitive** and trimmed. Invalid values raise `ValueError`.

### Usage

```python
from okw_contract_utils.tokens import parse_yes_no, assert_exists, OkwYesNo

# Parse user input
yn = parse_yes_no("YES")       # -> OkwYesNo.YES
yn = parse_yes_no("false")     # -> OkwYesNo.NO
yn = parse_yes_no("1")         # -> OkwYesNo.YES

# Assert existence
assert_exists(True, OkwYesNo.YES)   # PASS
assert_exists(False, OkwYesNo.NO)   # PASS
assert_exists(False, OkwYesNo.YES)  # raises OkwAssertionError
```

### Robot Framework integration

Keywords typically expose the expected parameter with a default of `YES`:

```robot
Verify Remote File Exists    session1    /tmp/data.txt           # default: YES
Verify Remote File Exists    session1    /tmp/data.txt    YES
Verify Remote File Exists    session1    /tmp/old.txt     NO     # must NOT exist
```

## Value Expansion

`expand_mem(text, store)` replaces `$MEM{KEY}` placeholders with values from a dictionary.
Missing keys cause an immediate error (no silent fallback).

```python
from okw_contract_utils import expand_mem

store = {"USER": "admin", "HOST": "10.0.0.1"}
result = expand_mem("ssh $MEM{USER}@$MEM{HOST}", store)
# -> "ssh admin@10.0.0.1"
```

## Runnable Examples

[okw-examples](https://github.com/Hrabovszki1023/okw-examples) — working Robot Framework tests for all OKW libraries.

## Handbuch

[OKW4Robot Handbuch](https://hrabovszki1023.github.io/okw-examples/) — step-by-step guide (German).
