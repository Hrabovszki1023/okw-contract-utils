# okw-contract-utils

[![PyPI](https://img.shields.io/pypi/v/okw-contract-utils)](https://pypi.org/project/okw-contract-utils/)
[![Python](https://img.shields.io/pypi/pyversions/okw-contract-utils)](https://pypi.org/project/okw-contract-utils/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

Gemeinsame Verträge für das [OKW4Robot](https://github.com/Hrabovszki1023/robotframework-okw4robot)-Ökosystem — Matcher, Tokens und Wertersetzung, die von allen OKW-Bibliotheken genutzt werden.

> **English version:** [README.md](README.md)

## Signal vs. NOISE

| Signal (dein Test) | NOISE (versteckt in contract-utils) |
|---|---|
| `VerifyValue Status Logged in` | Match-Modus-Auswahl (EXACT/WCM/REGX) |
| `${IGNORE}` → Schritt überspringen | Token-Parsing, Groß-/Kleinschreibung |
| `$MEM{TOKEN}` → gespeicherter Wert | Dictionary-Lookup, Fehlerbehandlung |

## Installation

```bash
pip install okw-contract-utils
```

## Features

- **Match-Modi**: EXACT (Gleichheit), WCM (Wildcard via fnmatch: `*` = beliebige Zeichen, `?` = ein Zeichen), REGX (Regex via `re.search`)
- **Wertersetzung**: `$MEM{KEY}` Platzhalter-Expansion via `expand_mem(text, store)`
- **Globale Tokens**: `$IGNORE`, `$EMPTY`, `$DELETE`
- **YES/NO-Existenzmodell**: `parse_yes_no()`, `assert_exists()`
- **Timeout-Helfer**: `wait_until(predicate, timeout_s, interval_s)`
- **Exceptions**: `OkwAssertionError`, `OkwTimeoutError`, `OkwConfigError`

## Keine Ziele

- Keine Robot Framework Keywords
- Keine SSH/Selenium/GUI-Abhängigkeiten
- Keine Umgebungs-/Provider-Logik

## Match-Modi

Alle Match-Modi normalisieren Zeilenumbrüche (`\r\n` zu `\n`) vor dem Vergleich.

| Modus | Funktion | Beschreibung |
|-------|----------|--------------|
| EXACT | `a == e` | Exakte Zeichenkettengleichheit |
| WCM | `fnmatch(a, e)` | Wildcard-Pattern-Match (`*` = beliebige Zeichen, `?` = ein Zeichen) |
| REGX | `re.search(e, a)` | Regulärer Ausdruck (mehrzeilig) |

Verwendung:

```python
from okw_contract_utils import assert_match, MatchMode

assert_match("Hello World", "Hello World", MatchMode.EXACT)
assert_match("Hello World", "Hello*", MatchMode.WCM)
assert_match("Hello World", r"Hello\s+\w+", MatchMode.REGX)
```

## Globales Token-Modell

OKW definiert einen kleinen Satz globaler Tokens. Tokens sind **groß-/kleinschreibungsunabhängig**
und werden nach dem Trimmen von Whitespace ausgewertet.

Tokens werden **hier definiert** (Vertrag) und können **selektiv implementiert** werden
von konkreten Keyword-Bibliotheken. Nicht jede Bibliothek muss jedes Token implementieren.

### Tokens

- `$IGNORE` (Steuer-Token)
  - Bedeutung: das Keyword wird zum **No-Op** (PASS).
  - Anwendungsfall: Einzelne Schritte in wiederverwendbaren Sequenzen deaktivieren ohne Kontrollstrukturen.

- `$EMPTY` (Wert-Token)
  - Bedeutung: Erwarteter/Zielwert ist **leer**.
  - Anwendungsfall: Explizit verifizieren, dass ein Wert leer ist (z.B. stdout/stderr ist leer).

- `$DELETE` (Aktions-Token)
  - Bedeutung: Explizite **Lösch-/Clear-Aktion** ausführen.
  - Typischerweise in GUI-Bibliotheken verwendet (z.B. Textfelder leeren).
  - Bibliotheken, die keine Lösch-Semantik implementieren können, unterstützen `$DELETE` einfach nicht.

### Robot Framework Variablen

Robot-Variablen wie `${IGNORE}` werden von Robot **vor** der Keyword-Ausführung expandiert.
Wenn `${IGNORE}` nicht definiert ist, schlägt Robot fehl bevor die Bibliothek handeln kann.

Empfohlene Suite-Variablen:

```robot
*** Variables ***
${IGNORE}    $IGNORE
${EMPTY}     $EMPTY
${DELETE}    $DELETE
```

### Auswertungsreihenfolge (Vertrag)

Für Keyword-Parameter vom Typ Value/Expected/Command:

* Robot Framework Variablen-Expansion (z.B. ${IGNORE} -> $IGNORE)
* OKW Wertersetzung (z.B. $MEM{KEY})
* Token-Parsing ($IGNORE, $EMPTY, $DELETE)
* Keyword-Semantik / Adapter-Ausführung

## YES/NO-Existenzmodell

Für Keywords, die prüfen ob eine Ressource existiert (Dateien, Verzeichnisse, UI-Elemente, etc.),
definiert OKW ein standardisiertes YES/NO-Modell.

### Akzeptierte Werte

| Eingabe | Interpretiert als |
|---------|-------------------|
| `YES`, `TRUE`, `1` | YES (muss existieren) |
| `NO`, `FALSE`, `0` | NO (darf nicht existieren) |

Alle Werte sind **groß-/kleinschreibungsunabhängig** und getrimmt. Ungültige Werte lösen `ValueError` aus.

### Verwendung

```python
from okw_contract_utils.tokens import parse_yes_no, assert_exists, OkwYesNo

# Benutzereingabe parsen
yn = parse_yes_no("YES")       # -> OkwYesNo.YES
yn = parse_yes_no("false")     # -> OkwYesNo.NO
yn = parse_yes_no("1")         # -> OkwYesNo.YES

# Existenz prüfen
assert_exists(True, OkwYesNo.YES)   # PASS
assert_exists(False, OkwYesNo.NO)   # PASS
assert_exists(False, OkwYesNo.YES)  # löst OkwAssertionError aus
```

### Robot Framework Integration

Keywords stellen den Expected-Parameter typischerweise mit Default `YES` bereit:

```robot
Verify Remote File Exists    session1    /tmp/data.txt           # Standard: YES
Verify Remote File Exists    session1    /tmp/data.txt    YES
Verify Remote File Exists    session1    /tmp/old.txt     NO     # darf NICHT existieren
```

## Wertersetzung

`expand_mem(text, store)` ersetzt `$MEM{KEY}`-Platzhalter mit Werten aus einem Dictionary.
Fehlende Schlüssel führen zu einem sofortigen Fehler (kein stilles Fallback).

```python
from okw_contract_utils import expand_mem

store = {"USER": "admin", "HOST": "10.0.0.1"}
result = expand_mem("ssh $MEM{USER}@$MEM{HOST}", store)
# -> "ssh admin@10.0.0.1"
```

## Lauffähige Beispiele

[okw-examples](https://github.com/Hrabovszki1023/okw-examples) — lauffähige Robot Framework Tests für alle OKW-Bibliotheken.

## Handbuch

[OKW4Robot Handbuch](https://hrabovszki1023.github.io/okw-examples/) — Schritt-für-Schritt-Anleitung.
