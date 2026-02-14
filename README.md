# okw-contract-utils

# okw-contract-utils

Small utility library for OKW-style contract matching and timeout handling.

## Features

- Match modes: EXACT, WCM (contains), REGX (regex)
- wait_until(predicate, timeout_s, interval_s)
- `$MEM{KEY}` placeholder expansion via `expand_mem(text, store)`

## Non-goals

- No Robot Framework keywords
- No SSH/Selenium/GUI dependencies
- No environment/provider logic