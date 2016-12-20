# -*- coding: utf-8 -*-

import os, time, random
from io import BytesIO
from smb.SMBConnection import SMBConnection
from .util import getConnectionInfo
from smb import smb_structs
import pytest

conn = None
info = {}

@pytest.yield_fixture
def teardown_func():
    global conn, info
    yield
    conn.close()

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

@pytest.mark.xfail(True, reason='TODO')
def test_delete_SMB1(setup_func_SMB1, teardown_func):
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile(info['share'], path+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath(info['share'], path)
    print(results)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles(info['share'], path+'/aa*.txt')

    results = conn.listPath(info['share'], path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles(info['share'], path+'/aaTest.*')

    results = conn.listPath(info['share'], path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles(info['share'], path+'/*')
    conn.deleteDirectory(info['share'], path)

@pytest.mark.xfail(True, reason='TODO')
def test_delete_SMB2(setup_func_SMB2, teardown_func):
    global conn

    path = os.sep + u'testDelete %d-%d' % ( time.time(), random.randint(0, 1000) )
    conn.createDirectory(info['share'], path)

    for filename in [ 'aaTest.txt', 'aaBest.txt', 'aaTest.bin', 'aaBest.bin', 'random.txt' ]:
        conn.storeFile(info['share'], path+"/"+filename, BytesIO(b"0123456789"))

    results = conn.listPath(info['share'], path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.txt' in filenames
    assert 'aaBest.txt' in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles(info['share'], path+'/aa*.txt')

    results = conn.listPath(info['share'], path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.txt' not in filenames
    assert 'aaBest.txt' not in filenames
    assert 'aaTest.bin' in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames

    conn.deleteFiles(info['share'], path+'/aaTest.*')

    results = conn.listPath(info['share'], path)
    filenames = list(map(lambda r: r.filename, results))
    assert 'aaTest.bin' not in filenames
    assert 'aaBest.bin' in filenames
    assert 'random.txt' in filenames
