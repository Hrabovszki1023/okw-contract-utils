import pytest
from okw_contract_utils import MatchMode, assert_match, OkwAssertionError

def test_exact_ok():
    assert_match("abc", "abc", MatchMode.EXACT)

def test_exact_fail():
    with pytest.raises(OkwAssertionError):
        assert_match("abc", "ab", MatchMode.EXACT)

# --- WCM (Wildcard Match) ---

def test_wcm_star_contains():
    """* matches any number of characters."""
    assert_match("hello world", "*world", MatchMode.WCM)

def test_wcm_star_both_sides():
    """*pattern* matches substring anywhere."""
    assert_match("hello world foo", "*world*", MatchMode.WCM)

def test_wcm_question_mark():
    """? matches exactly one character."""
    assert_match("Date:  23.10.1963", "Date:  ??.??.????", MatchMode.WCM)

def test_wcm_combined():
    """Combined * and ? in one pattern."""
    assert_match(
        "Geburtsdatum von Hans Mueller ist 23.10.1963 in Graz",
        "*Hans Mueller* ??.??.???? *",
        MatchMode.WCM,
    )

def test_wcm_exact_match():
    """Pattern without wildcards matches exact string."""
    assert_match("hello", "hello", MatchMode.WCM)

def test_wcm_no_implicit_contains():
    """Without * a plain pattern does NOT match a longer string."""
    with pytest.raises(OkwAssertionError):
        assert_match("hello world", "hello", MatchMode.WCM)

def test_wcm_fail():
    """Non-matching wildcard pattern fails."""
    with pytest.raises(OkwAssertionError):
        assert_match("abc", "x?z", MatchMode.WCM)

# --- REGX ---

def test_regx_ok():
    assert_match("nginx active (running)", r"active\s+\(running\)", MatchMode.REGX)
