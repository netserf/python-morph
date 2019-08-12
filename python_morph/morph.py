import os

def get_config_file():
    configfile = os.getenv('CONFIG_FILE')
    return configfile