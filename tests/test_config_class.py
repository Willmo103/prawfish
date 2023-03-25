import os
import pytest
from pydantic import ValidationError
from ..config import Config, _ConfFormData, _settings
from praw.models import Redditor
from praw import Reddit


def test_config_init_local_env():
    """checking that .env files are loaded properly is local_env arg is passed"""
    conf = Config.from_local()
    assert conf.db_host == _settings.db_host
    assert conf.db_port == _settings.db_port
    assert conf.db_pass == _settings.db_pass
    assert conf.db_name == _settings.db_name
    assert conf.db_usr_name == _settings.db_usr_name
    assert conf.client_id == _settings.client_id
    assert conf.client_secret == _settings.client_secret
    assert conf.usr_agent == _settings.usr_agent


def test_config_from_dict():
    """testing constructor handles dict data from pydantic model"""
    form_data = _ConfFormData(
        db_host="localhost",
        db_port=5432,
        db_pass="password",
        db_name="mydb",
        db_usr_name="myuser",
        client_id="myclientid",
        client_secret="myclientsecret",
        usr_agent="myuseragent",
    )

    conf = Config.from_dict(form_data.dict())

    assert conf.db_host == "localhost"
    assert conf.db_port == 5432
    assert conf.db_pass == "password"
    assert conf.db_name == "mydb"
    assert conf.db_usr_name == "myuser"
    assert conf.client_id == "myclientid"
    assert conf.client_secret == "myclientsecret"
    assert conf.usr_agent == "myuseragent"


def test_config_init_invalid_args():
    """checking that constructor raises error when invalid args are passed"""
    with pytest.raises(TypeError):
        Config(invalid_arg=True)


def test_to_json_method():
    """checking all keys and values in the object json"""
    conf = Config.from_local()
    conf_json = conf._to_json()
    assert conf_json["db_host"] == _settings.db_host
    assert conf_json["db_port"] == _settings.db_port
    assert conf_json["db_pass"] == _settings.db_pass
    assert conf_json["db_name"] == _settings.db_name
    assert conf_json["db_usr_name"] == _settings.db_usr_name
    assert conf_json["client_id"] == _settings.client_id
    assert conf_json["client_secret"] == _settings.client_secret
    assert conf_json["usr_agent"] == _settings.usr_agent


def test_config_init_invalid_args():
    """checking that constructor raises error when invalid args are passed"""
    with pytest.raises(TypeError):
        Config(invalid_arg=True)


def test_write_to_json_method():
    """checking that write_json_file method works properly"""
    conf = Config.from_local()
    conf.write_to_json("test.json")
    conf2 = Config.from_json_file("test.json")
    assert conf.db_host == conf2.db_host
    assert conf.db_port == conf2.db_port
    assert conf.db_pass == conf2.db_pass
    assert conf.db_name == conf2.db_name
    assert conf.db_usr_name == conf2.db_usr_name
    assert conf.client_id == conf2.client_id
    assert conf.client_secret == conf2.client_secret
    assert conf.usr_agent == conf2.usr_agent
    os.remove("test.json")


def test_database_url_method():
    """checking that database_url method works properly"""
    conf = Config.from_local()
    assert (
        conf.database_url()
        == f"postgresql://{conf.db_usr_name}:{conf.db_pass}@{conf.db_host}:{conf.db_port}/{conf.db_name}"
    )


def test_build_reddit_instance_method():
    """checking that build_reddit_instance method works properly"""
    conf = Config.from_local()
    reddit = conf.build_reddit_instance()
    assert isinstance(reddit, Reddit)
