'''
Test suite for the morph command line tool.
'''

from pathlib import Path
import os
from unittest.mock import patch

import python_morph.morph as morph

def test_get_config_filename_from_env():
    '''test that config file can be set with environment variable CONFIG_FILE'''
    # setup environment variable
    configfile = '/my/test/dir/myconfig.yaml'
    os.environ["CONFIG_FILE"] = configfile
    # check configfile can be configured through the environment variable
    envfile = morph.get_config_filename()
    assert envfile == configfile
    # clean up environment variable
    del os.environ['CONFIG_FILE']


def test_get_config_filename_from_home():
    '''test that config file can be set in home directory'''
    with patch.object(Path, 'home', return_value='/home/user') as mock_home:
        with patch.object(Path, 'is_file', return_value=True) as mock_is_file:
            config = morph.get_config_filename()
            mock_home.assert_called()
            mock_is_file.assert_called()
            assert config == '/home/user/.morph.yaml'

def test_get_config_from_global():
    '''test that config file has its global location set'''
    config = morph.get_config_filename()
    assert config == '/usr/local/etc/morph.yaml'
