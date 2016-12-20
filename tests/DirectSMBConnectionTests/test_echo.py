
import random
from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo

import pytest

conn = None

@pytest.fixture
def setup_func():
    global conn
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True, is_direct_tcp=True)
    assert conn.connect(info['server_ip'], info['server_port'])

@pytest.yield_fixture
def teardown_func():
    yield
    global conn
    conn.close()

def test_echo(setup_func, teardown_func):
    global conn
    data = bytearray('%d' % random.randint(1000, 9999), 'ascii')
    assert conn.echo(data) == data
