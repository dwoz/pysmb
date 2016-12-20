
from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from smb import smb_structs

import pytest

conn = None

@pytest.yield_fixture
def teardown_func():
    yield
    global conn
    conn.close()


def test_NTLMv1_auth_SMB1(teardown_func):
    global conn
    smb_structs.SUPPORT_SMB2 = False
    info = getConnectionInfo()
    conn = SMBConnection(
        info['user'],
        info['password'],
        info['client_name'],
        info['server_name'],
        domain=info['domain'],
        is_direct_tcp=True,
        use_ntlm_v2=False,
    )
    assert conn.connect(info['server_ip'], info['server_port'])

def test_NTLMv2_auth_SMB1(teardown_func):
    global conn
    smb_structs.SUPPORT_SMB2 = False
    info = getConnectionInfo()
    conn = SMBConnection(
        info['user'], info['password'], info['client_name'],
        info['server_name'], use_ntlm_v2 = True, is_direct_tcp=True
    )
    assert conn.connect(info['server_ip'], info['server_port'])

def test_NTLMv1_auth_SMB2(teardown_func):
    global conn
    smb_structs.SUPPORT_SMB2 = True
    info = getConnectionInfo()
    conn = SMBConnection(
        info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = False,
        is_direct_tcp=True
    )
    assert conn.connect(info['server_ip'], info['server_port'])

def test_NTLMv2_auth_SMB2(teardown_func):
    global conn
    smb_structs.SUPPORT_SMB2 = True
    info = getConnectionInfo()
    conn = SMBConnection(
        info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True,
        is_direct_tcp=True
    )
    assert conn.connect(info['server_ip'], info['server_port'])
