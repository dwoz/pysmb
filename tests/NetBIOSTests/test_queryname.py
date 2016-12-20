
from nmb.NetBIOS import NetBIOS
import pytest
conn = None

@pytest.yield_fixture
def teardown_func():
    yield
    global conn
    conn.close()

@pytest.mark.xfail(True, reason='TODO')
def test_broadcast(teardown_func):
    global conn
    conn = NetBIOS()
    assert conn.queryName('FXB04FS0301', timeout = 10)

