import pastools
import pytest
import os

def test_parse_url():
    url = r'pbscp://host1/home/user1/test1.sh'
    host, path = pastools.parse_url(url)
    assert host == 'host1'
    assert path == '/home/user1/test1.sh'


def test_parse_export_env():
    env = r'HOME=/home/user1,MYVAR=1,PAS_PRIMARY_FILE=pbscp://host1/home/user1/test1.sh'
    env_vars = pastools.parse_export_env(env)
    assert env_vars == {
        "HOME": "/home/user1",
        "MYVAR": "1",
        "PAS_PRIMARY_FILE": "pbscp://host1/home/user1/test1.sh"}

def test_create_access_env_vars():
    host = 'host1'
    path = '/home/user1/test1.sh'
    vars = pastools.create_access_env_vars(host, path)
    assert vars == {
        'ACCESS_INPUT_FILES': 'test1.sh@host1:/home/user1/test1.sh',
        'ACCESS_OUTPUT_FILES': '*@host1:/home/user1',
        'ACCESS_RUNNING_FILES': '/home/user1'}

def test_create_logs():
    dirname = os.path.abspath('.')
    basename = 'test'
    o, e = pastools.create_logs(dirname, basename)
    assert os.path.exists(o)
    assert os.path.exists(e)
    assert o == os.path.join(os.path.abspath('.'), 'test.o.log')
    assert e == os.path.join(os.path.abspath('.'), 'test.e.log')
    os.remove(o)
    os.remove(e)