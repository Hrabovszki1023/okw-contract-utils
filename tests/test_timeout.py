import pytest
import time
from okw_contract_utils import wait_until, OkwTimeoutError

def test_wait_until_passes():
    start = time.monotonic()
    def pred():
        return (time.monotonic() - start) > 0.2
    assert wait_until(pred, timeout_s=2.0, interval_s=0.05) is True

def test_wait_until_times_out():
    with pytest.raises(OkwTimeoutError):
        wait_until(lambda: False, timeout_s=0.2, interval_s=0.05)
