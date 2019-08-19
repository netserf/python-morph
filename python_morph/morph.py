"""
This module provides a command line tool to help manage string transformations
through a yaml config file and some understanding of regular expressions.

There are 2 ways the string transformations will be handled:

1. YAML configuration with an order of precedence:

    1. environment variable (MORPH_CONFIG) set to configuration file location
    2. home directory with a .morph.yaml file
    3. /usr/local/etc/morph.yaml

2. CLI args for single ad-hoc transformations

Argument lists and stdin are both acceptable ways to input the string(s) to be
transformed.
"""

from pathlib import Path
import os
import re
import yaml
import click
import fileinput

@click.command()
@click.option('-m', '--match', 'match_pattern')
@click.option('-r', '--replace', 'replace_pattern')
@click.argument('cli_args', nargs=-1)
def main(match_pattern, replace_pattern, cli_args):
    '''A tool to help manage string transformations through a yaml config file
    and some understanding of regular expressions.'''
    config = get_config_filename()
    sub_rules = _get_cli_adhoc_rules(match_pattern, replace_pattern)
    if not sub_rules:
        sub_rules = _parse_config(config)
    _process_input(sub_rules, cli_args)     

#    if match_pattern and replace_pattern:
#        _cli_adhoc(match_pattern, replace_pattern, cli_args)

def _generate_cli_adhoc_rules(match_pattern, replace_pattern):
    '''helper method for processing ad-hoc cli match/replace requests'''
    sub_rules = None
    if match_pattern and replace_pattern:
        sub_rules = {
            'substitutions': [
                {'match': re.compile(match_pattern), 'replace': replace_pattern}
            ]
        }
    return sub_rules
'''
'''
def _get_config_filename():
    ''' config file order of precedence is:
    1. environment variable CONFIG_FILE
    2. $HOME/.morph.yaml
    3. /usr/local/etc/morph.yaml
    '''
    envfile = os.getenv('CONFIG_FILE')
    homefile = Path(str(Path.home()) + "/.morph.yaml")
    globalfile = '/usr/local/etc/morph.yaml'
    configfile = globalfile
    if homefile.is_file():
        configfile = str(homefile)
    if envfile:
        configfile = envfile
    return configfile

def _process_input(sub_rules, cli_args):
    # process piped stdin input
    if cli_args[-1] == "-":
        with click.open_file('-', mode='r') as infile:
            for instr in infile:
                out = _run_subs(sub_rules, instr.rstrip())
                click.echo(out)
    else:
        for instr in cli_args:
            out = _run_subs(sub_rules, instr)
            click.echo(out)


def _run_subs(sub_rules, instr):
    '''take substitution rules tuple {match, replace}, and see if input matches.
    If match, then replace.
    '''
    for rule in sub_rules['substitutions']:
        if rule['match'].match(instr):
            return re.sub(rule['match'], rule['replace'], instr)
    return None

def _parse_config(configfile):
    '''parse config file and return it as a set of rules that will be used in
    the match/replace logic'''
    with open(configfile, 'r') as infile:
        config = yaml.safe_load(infile)
    for rule in config['substitutions']:
        rule['match'] = re.compile(rule['match'])
    return config


if __name__ == '__main__':
    main()
