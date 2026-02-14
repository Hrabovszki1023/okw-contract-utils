import pytest
from okw_contract_utils import expand_mem, OkwConfigError


def test_expand_mem_single():
    store = {"NGINX_STATUS": "abc"}
    assert expand_mem("X $MEM{NGINX_STATUS} Y", store) == "X abc Y"


def test_expand_mem_multiple_occurrences():
    store = {"A": "1", "B": "2"}
    assert expand_mem("$MEM{A}+$MEM{B}=$MEM{A}$MEM{B}", store) == "1+2=12"


def test_expand_mem_missing_key_fails():
    store = {"A": "1"}
    with pytest.raises(OkwConfigError):
        expand_mem("X $MEM{B} Y", store)


def test_expand_mem_none_becomes_empty_string():
    store = {"A": None}
    assert expand_mem("X$MEM{A}Y", store) == "XY"
