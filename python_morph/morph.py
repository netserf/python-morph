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
    configfile = ''
    if envfile:
        return envfile
    elif homefile.is_file():
        return str(homefile)
    else:
        return globalfile