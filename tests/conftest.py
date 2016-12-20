import pytest
collect_ignore = []

def pytest_configure(config):
    collect_ignore.extend([
        'DirectSMBTwistedTests/test_auth.py',
        'DirectSMBTwistedTests/test_createdeletedirectory.py',
        'DirectSMBTwistedTests/test_echo.py',
        'DirectSMBTwistedTests/test_listpath.py',
        'DirectSMBTwistedTests/test_listshares.py',
        'DirectSMBTwistedTests/test_listsnapshots.py',
        'DirectSMBTwistedTests/test_rename.py',
        'DirectSMBTwistedTests/test_retrievefile.py',
        'DirectSMBTwistedTests/test_storefile.py',
        'SMBTwistedTests/test_auth.py',
        'SMBTwistedTests/test_createdeletedirectory.py',
        'SMBTwistedTests/test_echo.py',
        'SMBTwistedTests/test_getattributes.py',
        'SMBTwistedTests/test_listpath.py',
        'SMBTwistedTests/test_listshares.py',
        'SMBTwistedTests/test_listsnapshots.py',
        'SMBTwistedTests/test_rename.py',
        'SMBTwistedTests/test_retrievefile.py',
        'SMBTwistedTests/test_storefile.py',
    ])
