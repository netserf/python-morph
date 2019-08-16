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


def get_config_filename():
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
