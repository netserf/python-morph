'''
Test suite for the morph command line tool.
'''

from pathlib import Path
import os
import re
from unittest.mock import patch
import pytest
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


INSTR_LIST = [
    ('match rule 0', 'test 0'),
    ('match rule 1 YES2 done', 'YES2'),
    ('match rule 2 YES4.1 more    complex YES4.2 done', 'YES4.1 YES4.2'),
    ('match rule 3 NO MATCHES FOUND', None)
]
INSTR_IDS = [f'match rule {n}' for n, _ in enumerate(INSTR_LIST)]
@pytest.mark.parametrize('instr,expected', INSTR_LIST, ids=INSTR_IDS)
def test_run_subs_with_small_sub_rules_list(instr, expected):
    '''test that batch substitution rules run as expected'''
    sub_rules = [
        {'match': re.compile(r'match rule 0'), 'replace': r'test 0'},
        {'match': re.compile(r'match rule 1 (.*) done'), 'replace': r'\1'},
        {'match': re.compile(r'match rule 2 (.*) more\s+complex (.*) done'), 'replace': r'\1 \2'},
    ]
    assert morph.run_subs(sub_rules, instr) == expected


def test_parse_config_file_collects_file_contents():
    '''test that config file can be parsed'''
    sub_rules = morph.parse_config('tests/morph.yaml')
    assert 'substitutions' in sub_rules


def test_parse_config_file_no_file():
    '''test that missing config file wil raise an exception'''
    with pytest.raises(FileNotFoundError):
        morph.parse_config('not_a_file.yaml')
