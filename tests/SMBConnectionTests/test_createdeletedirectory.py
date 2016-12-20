# -*- coding: utf-8 -*-

import os, time, random
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

def test_english_directory_SMB1(setup_func_SMB1, teardown_func):
    global conn

    path = os.sep + 'TestDir %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) in names

    conn.deleteDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) not in names

def test_english_directory_SMB2(setup_func_SMB2, teardown_func):
    global conn

    path = os.sep + 'TestDir %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) in names

    conn.deleteDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) not in names

def test_unicode_directory_SMB1(setup_func_SMB1, teardown_func):
    global conn

    path = os.sep + u'文件夹创建 %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) in names

    conn.deleteDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) not in names

def test_unicode_directory_SMB2(setup_func_SMB2, teardown_func):
    global conn

    path = os.sep + u'文件夹创建 %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) in names

    conn.deleteDirectory(info['share'], path)

    entries = conn.listPath(info['share'], os.path.dirname(path.replace('/', os.sep)))
    names = [e.filename for e in entries]
    assert os.path.basename(path.replace('/', os.sep)) not in names
