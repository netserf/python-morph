'''
Test suite for the sarlac command line tool.
'''

# pylint: disable=protected-access

from pathlib import Path
import os
import re
from unittest.mock import patch
from click.testing import CliRunner
import pytest
import python_sarlac.sarlac as sarlac

def test_get_config_filename_from_env():
    '''test that config file can be set with environment variable SARLAC_CONFIG'''
    # setup environment variable
    configfile = '/my/test/dir/myconfig.yaml'
    os.environ["SARLAC_CONFIG"] = configfile
    # check configfile can be configured through the environment variable
    envfile = sarlac._get_config_filename()
    assert envfile == configfile
    # clean up environment variable
    del os.environ['SARLAC_CONFIG']


def test_get_config_filename_from_home():
    '''test that config file can be set in home directory'''
    with patch.object(Path, 'home', return_value='/home/user') as mock_home:
        with patch.object(Path, 'is_file', return_value=True) as mock_is_file:
            config = sarlac._get_config_filename()
            mock_home.assert_called()
            mock_is_file.assert_called()
            assert config == '/home/user/.sarlac.yaml'


def test_get_config_from_global():
    '''test that config file has its global location set'''
    config = sarlac._get_config_filename()
    assert config == '/usr/local/etc/sarlac.yaml'


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
    sub_rules = {'substitutions': [
        {'match': re.compile(r'match rule 0'), 'replace': r'test 0'},
        {'match': re.compile(r'match rule 1 (.*) done'), 'replace': r'\1'},
        {'match': re.compile(r'match rule 2 (.*) more\s+complex (.*) done'), 'replace': r'\1 \2'},
    ]}
    assert sarlac._run_subs(sub_rules, instr) == expected


def test_parse_config_file_collects_file_contents():
    '''test that config file can be parsed'''
    sub_rules = sarlac._parse_config('tests/sarlac.yaml')
    assert 'substitutions' in sub_rules


def test_parse_config_file_no_file():
    '''test that missing config file wil raise an exception'''
    with pytest.raises(FileNotFoundError):
        sarlac._parse_config('not_a_file.yaml')


RULE_LIST = [
    (['testmatch', 'replaced', 'testmatch'], \
        {'substitutions': [{'match': re.compile('testmatch'), 'replace': 'replaced'}]}),
    ([r'test(.*)', r'\1', 'testreplaced2'], \
        {'substitutions': [{'match': re.compile('test(.*)'), 'replace': '\\1'}]}),
    ([r'test(.*)', r'\1', 'testreplaced3', 'testreplaced4'], \
        {'substitutions': [{'match': re.compile('test(.*)'), 'replace': '\\1'}]})
]
RULE_IDS = [f'rule test {n}' for n, _ in enumerate(RULE_LIST)]

@pytest.mark.parametrize('rule_input,expected', RULE_LIST, ids=RULE_IDS)
def test_generate_cli_adhoc_rules(rule_input, expected):
    '''test substitution rules generation for ad-hoc match/replace on the cli'''
    sub_rules = sarlac._generate_cli_adhoc_rules(rule_input[0], rule_input[1])
    print(sub_rules)
    print(expected)
    assert sub_rules == expected


CLI_LIST = [
    (['--match', 'testmatch', '--replace', 'replaced', 'testmatch'], \
        'replaced\n'),
    (['--match', r'test(.*)', '--replace', r'\1', 'testreplaced2'], \
        'replaced2\n'), \
    (['--match', r'test(.*)', '--replace', r'\1', 'testreplaced3', 'testreplaced4'], \
        'replaced3\nreplaced4\n')
]
CLI_IDS = [f'cli test {n}' for n, _ in enumerate(CLI_LIST)]

@pytest.mark.parametrize('cli_input,expected', CLI_LIST, ids=CLI_IDS)
def test_main_cli_thru_cli_args(cli_input, expected):
    '''test that sarlac cli can run ad-hoc match/replace'''
    runner = CliRunner()
    result = runner.invoke(sarlac.main, cli_input)
    assert result.exit_code == 0
    assert result.output == expected


def test_main_cli_thru_stdin():
    '''test that sarlac cli can run ad-hoc match/replace on piped stdin'''
    runner = CliRunner()
    cli_input = ['--match', 'testmatch', '--replace', 'replaced', '-']
    result = runner.invoke(sarlac.main, cli_input, input="testmatch")
    assert result.exit_code == 0
    assert result.output == "replaced\n"


@pytest.mark.parametrize('cli_input', [(), ('--help'), ('-h')])
def test_main_cli_no_input_invokes_help(cli_input):
    '''test scenarios where help is called'''
    runner = CliRunner()
    result = runner.invoke(sarlac.main, cli_input)
    assert result.exit_code == 0
    assert result.output.startswith('Usage:')
