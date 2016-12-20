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

def test_rename_english_file_SMB1(setup_func_SMB1, teardown_func):
    global conn

    old_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.storeFile('smbtest', old_path, BytesIO(b'Rename file test'))

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteFiles('smbtest', new_path)

def test_rename_english_file_SMB2(setup_func_SMB2, teardown_func):
    global conn

    old_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.storeFile('smbtest', old_path, BytesIO(b'Rename file test'))

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteFiles('smbtest', new_path)

def test_rename_unicode_file_SMB1(setup_func_SMB1, teardown_func):
    global conn

    old_path = u'/改名测试 %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = u'/改名测试 %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.storeFile('smbtest', old_path, BytesIO(b'Rename file test'))

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteFiles('smbtest', new_path)

def test_rename_unicode_file_SMB2(setup_func_SMB2, teardown_func):
    global conn

    old_path = u'/改名测试 %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = u'/改名测试 %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.storeFile('smbtest', old_path, BytesIO(b'Rename file test'))

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteFiles('smbtest', new_path)

def test_rename_english_directory_SMB1(setup_func_SMB1, teardown_func):
    global conn

    old_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.createDirectory('smbtest', old_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteDirectory('smbtest', new_path)

def test_rename_english_directory_SMB2(setup_func_SMB2, teardown_func):
    global conn

    old_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )
    new_path = '/RenameTest %d-%d.txt' % ( time.time(), random.randint(1000, 9999) )

    conn.createDirectory('smbtest', old_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteDirectory('smbtest', new_path)

def test_rename_unicode_directory_SMB1(setup_func_SMB1, teardown_func):
    global conn

    old_path = u'/改名测试 %d-%d' % ( time.time(), random.randint(1000, 9999) )
    new_path = u'/改名测试 %d-%d' % ( time.time(), random.randint(1000, 9999) )

    conn.createDirectory('smbtest', old_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteDirectory('smbtest', new_path)

def test_rename_unicode_directory_SMB2(setup_func_SMB2, teardown_func):
    global conn

    old_path = u'/改名测试 %d-%d' % ( time.time(), random.randint(1000, 9999) )
    new_path = u'/改名测试 %d-%d' % ( time.time(), random.randint(1000, 9999) )

    conn.createDirectory('smbtest', old_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) not in filenames

    conn.rename('smbtest', old_path, new_path)

    entries = conn.listPath('smbtest', os.path.dirname(old_path.replace('/', os.sep)))
    filenames = [e.filename for e in entries]
    assert os.path.basename(old_path.replace('/', os.sep)) not in filenames
    assert os.path.basename(new_path.replace('/', os.sep)) in filenames

    conn.deleteDirectory('smbtest', new_path)
