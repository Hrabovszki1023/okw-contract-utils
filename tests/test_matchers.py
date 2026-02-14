import pytest
from okw_contract_utils import MatchMode, assert_match, OkwAssertionError

def test_exact_ok():
    assert_match("abc", "abc", MatchMode.EXACT)

def test_exact_fail():
    with pytest.raises(OkwAssertionError):
        assert_match("abc", "ab", MatchMode.EXACT)

def test_wcm_ok():
    assert_match("hello world", "world", MatchMode.WCM)

def test_regx_ok():
    assert_match("nginx active (running)", r"active\s+\(running\)", MatchMode.REGX)
