import pytest
from pydantic import ValidationError
from ..config import Config, ConfFormData, _settings


def test_config_init_local_env():
    conf = Config(local_env=True)
    assert conf.db_host == _settings.db_host
    assert conf.db_port == _settings.db_port
    assert conf.db_pass == _settings.db_pass
    assert conf.db_name == _settings.db_name
    assert conf.db_usr_name == _settings.db_usr_name
    assert conf.client_id == _settings.client_id
    assert conf.client_secret == _settings.client_secret
    assert conf.usr_agent == _settings.usr_agent

def test_config_init_form_data():
    form_data = ConfFormData(
        db_host='localhost',
        db_port=5432,
        db_pass='password',
        db_name='mydb',
        db_usr_name='myuser',
        client_id='myclientid',
        client_secret='myclientsecret',
        usr_agent='myuseragent'
    )

    conf = Config(form_data=form_data)

    assert conf.db_host == 'localhost'
    assert conf.db_port == 5432
    assert conf.db_pass == 'password'
    assert conf.db_name == 'mydb'
    assert conf.db_usr_name == 'myuser'
    assert conf.client_id == 'myclientid'
    assert conf.client_secret == 'myclientsecret'
    assert conf.usr_agent == 'myuseragent'

def test_config_init_invalid_form_data():
    with pytest.raises(ValidationError):
        form_data = ConfFormData(
            db_host='localhost',
            db_port='invalid_port',
            db_pass='password',
            db_name='mydb',
            db_usr_name='myuser',
            client_id='myclientid',
            client_secret='myclientsecret',
            usr_agent='myuseragent'
        )


