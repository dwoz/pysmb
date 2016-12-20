# -*- coding: utf-8 -*-

from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from smb import smb_structs
import pytest

conn = None
info = {}

@pytest.fixture
def setup_func_SMB1():
    global conn, info
    smb_structs.SUPPORT_SMB2 = False
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True)
    assert conn.connect(info['server_ip'], info['server_port'])

@pytest.fixture
def setup_func_SMB2():
    global conn, info
    smb_structs.SUPPORT_SMB2 = True
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True)
    assert conn.connect(info['server_ip'], info['server_port'])

@pytest.yield_fixture
def teardown_func():
    global conn, info
    yield
    conn.close()

def test_getAttributes_SMB2(setup_func_SMB2, teardown_func):
    global conn
    file_info = conn.getAttributes(info['share'], '/Test Folder with Long Name/')
    assert file_info.isDirectory

    file_info = conn.getAttributes(info['share'], '/rfc1001.txt')
    assert not file_info.isDirectory
    assert file_info.file_size == 158437
    assert file_info.alloc_size == 159744

    file_info = conn.getAttributes(info['share'], u'/\u6d4b\u8bd5\u6587\u4ef6\u5939')
    assert file_info.isDirectory

def test_getAttributes_SMB1(setup_func_SMB1, teardown_func):
    global conn
    file_info = conn.getAttributes(info['share'], '/Test Folder with Long Name/')
    assert file_info.isDirectory

    file_info = conn.getAttributes(info['share'], '/rfc1001.txt')
    assert not file_info.isDirectory
    assert file_info.file_size == 158437
    assert file_info.alloc_size == 159744

    file_info = conn.getAttributes(info['share'], u'/\u6d4b\u8bd5\u6587\u4ef6\u5939')
    assert file_info.isDirectory
