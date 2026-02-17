# okw-contract-utils

Shared utilities for the OKW ecosystem. This package defines cross-library contracts such as
matchers (EXACT/WCM/REGX), value expansion ($MEM{KEY}) and global OKW tokens.

## Features

- Match modes: EXACT, WCM (contains), REGX (regex)
- wait_until(predicate, timeout_s, interval_s)
- `$MEM{KEY}` placeholder expansion via `expand_mem(text, store)`

## Non-goals

- No Robot Framework keywords
- No SSH/Selenium/GUI dependencies
- No environment/provider logic

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

* Robot Framework variable expansion (e.g. ${IGNORE} → $IGNORE)
* OKW value expansion (e.g. $MEM{KEY})
* Token parsing ($IGNORE, $EMPTY, $DELETE)
* Keyword semantics / adapter execution

