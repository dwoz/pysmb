# -*- coding: utf-8 -*-

from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from smb import smb_structs

import pytest

conn = None

@pytest.fixture
def setup_func_SMB1():
    global conn, info
    smb_structs.SUPPORT_SMB2 = False
    info = getConnectionInfo()
    conn = SMBConnection(info['user'], info['password'], info['client_name'], info['server_name'], use_ntlm_v2 = True, is_direct_tcp=True)
    assert conn.connect(info['server_ip'], info['server_port'])

@pytest.fixture
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

def test_listPath_SMB1(setup_func_SMB1, teardown_func):
    global conn
    results = conn.listPath(info['share'], '/')
    filenames = [( r.filename, r.isDirectory ) for r in results]
    assert ( u'测试文件夹', True) in filenames                      # Test non-English folder names
    assert ( 'Test Folder with Long Name', True ) in filenames      # Test long English folder names
    assert ( 'TestDir1', True ) in filenames                        # Test short English folder names
    assert ( 'Implementing CIFS - SMB.html', False ) in filenames   # Test long English file names
    assert ( 'rfc1001.txt', False ) in filenames                    # Test short English file names

def test_listSubPath_SMB1(setup_func_SMB1, teardown_func):
    global conn
    results = conn.listPath(info['share'], '/Test Folder with Long Name/')
    filenames = [( r.filename, r.isDirectory ) for r in results]
    assert ( 'Test File.txt', False ) in filenames
    assert ( 'Test Folder', True ) in filenames
    assert ( u'子文件夹', True ) in filenames

def test_listPath_SMB2(setup_func_SMB1, teardown_func):
    global conn
    results = conn.listPath(info['share'], '/')
    filenames = [( r.filename, r.isDirectory ) for r in results]
    assert ( u'测试文件夹', True) in filenames                      # Test non-English folder names
    assert ( 'Test Folder with Long Name', True ) in filenames      # Test long English folder names
    assert ( 'TestDir1', True ) in filenames                        # Test short English folder names
    assert ( 'Implementing CIFS - SMB.html', False ) in filenames   # Test long English file names
    assert ( 'rfc1001.txt', False ) in filenames                    # Test short English file names

def test_listSubPath_SMB2(setup_func_SMB1, teardown_func):
    global conn
    results = conn.listPath(info['share'], '/Test Folder with Long Name/')
    filenames = [( r.filename, r.isDirectory ) for r in results]
    assert ( 'Test File.txt', False ) in filenames
    assert ( 'Test Folder', True ) in filenames
    assert ( u'子文件夹', True ) in filenames
