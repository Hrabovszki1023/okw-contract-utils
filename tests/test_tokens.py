import pytest
from okw_contract_utils.tokens import (
    parse_token, OkwToken, parse_yes_no, OkwYesNo, assert_exists,
)
from okw_contract_utils import OkwAssertionError

def test_parse_ignore():
    assert parse_token("$IGNORE") == OkwToken.IGNORE
    assert parse_token("  $ignore  ") == OkwToken.IGNORE

def test_parse_empty():
    assert parse_token("$EMPTY") == OkwToken.EMPTY
    assert parse_token(" $empty ") == OkwToken.EMPTY

def test_parse_delete():
    assert parse_token("$DELETE") == OkwToken.DELETE
    assert parse_token(" $delete ") == OkwToken.DELETE

def test_parse_none():
    assert parse_token("x") is None
    assert parse_token("") is None
    assert parse_token(None) is None


# --- YES/NO ---

def test_parse_yes_no_yes_variants():
    """YES, TRUE, 1 all parse to OkwYesNo.YES (case-insensitive)."""
    assert parse_yes_no("YES") == OkwYesNo.YES
    assert parse_yes_no("yes") == OkwYesNo.YES
    assert parse_yes_no("  Yes  ") == OkwYesNo.YES
    assert parse_yes_no("TRUE") == OkwYesNo.YES
    assert parse_yes_no("true") == OkwYesNo.YES
    assert parse_yes_no("1") == OkwYesNo.YES

def test_parse_yes_no_no_variants():
    """NO, FALSE, 0 all parse to OkwYesNo.NO (case-insensitive)."""
    assert parse_yes_no("NO") == OkwYesNo.NO
    assert parse_yes_no("no") == OkwYesNo.NO
    assert parse_yes_no("  No  ") == OkwYesNo.NO
    assert parse_yes_no("FALSE") == OkwYesNo.NO
    assert parse_yes_no("false") == OkwYesNo.NO
    assert parse_yes_no("0") == OkwYesNo.NO

def test_parse_yes_no_invalid():
    """Invalid values raise ValueError."""
    with pytest.raises(ValueError):
        parse_yes_no("MAYBE")
    with pytest.raises(ValueError):
        parse_yes_no("")
    with pytest.raises(ValueError):
        parse_yes_no("2")

def test_assert_exists_yes_pass():
    """actual=True, expected=YES -> PASS."""
    assert_exists(True, OkwYesNo.YES)

def test_assert_exists_yes_fail():
    """actual=False, expected=YES -> FAIL."""
    with pytest.raises(OkwAssertionError, match="Expected to exist"):
        assert_exists(False, OkwYesNo.YES)

def test_assert_exists_no_pass():
    """actual=False, expected=NO -> PASS."""
    assert_exists(False, OkwYesNo.NO)

def test_assert_exists_no_fail():
    """actual=True, expected=NO -> FAIL."""
    with pytest.raises(OkwAssertionError, match="Expected to NOT exist"):
        assert_exists(True, OkwYesNo.NO)

def test_assert_exists_with_context():
    """Context is included in error message."""
    with pytest.raises(OkwAssertionError, match=r"\[r1\] /tmp/file"):
        assert_exists(False, OkwYesNo.YES, context="[r1] /tmp/file")
