import pytest
import os
import python_morph.morph as morph

def test_set_config_file_check_env():
    # setup environment
    config_name = '/my/test/dir/myconfig.yaml'
    os.environ["CONFIG_FILE"] = config_name
    env_config = morph.get_config_file()
    assert env_config == config_name

