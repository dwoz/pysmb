
from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from smb import smb_structs

import pytest

conn = None
info = {}

def setup_func_SMB1():
    global conn, info
    smb_structs.SUPPORT_SMB2 = False
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True, is_direct_tcp=True)
    assert conn.connect(info['server_ip'], info['server_port'])

def setup_func_SMB2():
    global conn, info
    smb_structs.SUPPORT_SMB2 = True
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True, is_direct_tcp=True)
    assert conn.connect(info['server_ip'], info['server_port'])

@pytest.yield_fixture
def teardown_func():
    yield
    global conn, info
    conn.close()
    info = {}

@pytest.mark.xfail(True, reason='TODO')
def test_listsnapshots_SMB1(setup_func_SMB1, teardown_func):
    global conn
    results = conn.listSnapshots(info['share'], '/rfc1001.txt')
    assert len(results) > 0

@pytest.mark.xfail(True, reason='TODO')
def test_listsnapshots_SMB2(setup_func_SMB2, teardown_func):
    global conn
    results = conn.listSnapshots(info['share'], '/rfc1001.txt')
    assert len(results) > 0
