from pydantic import BaseSettings
from pydantic import BaseModel
from praw import Reddit
from typing import Any, Optional
from sqlalchemy.orm import Session
from .models import Config as ConfigDB
import os
import json


class _ConfFormData(BaseModel):
    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_usr_name: str
    client_id: str
    client_secret: str
    usr_agent: str


class _Settings(BaseSettings):
    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_usr_name: str
    client_id: str
    client_secret: str
    usr_agent: str

    class Config:
        env_file = os.path.abspath(__file__).replace(os.path.basename(__file__), ".env")


# initialize an instance of this class to import elsewhere
try:
    _settings = _Settings()
except FileNotFoundError:
    pass


class Config:
    def __init__(self):
        self._db_host = None
        self._db_port = None
        self._db_pass = None
        self._db_name = None
        self._db_usr_name = None
        self._client_id = None
        self._client_secret = None
        self._usr_agent = None

    @classmethod
    def from_env(cls):
        self = cls()
        self._db_host = os.environ["db_host"]
        self._db_port = os.environ["db_port"]
        self._db_pass = os.environ["db_pass"]
        self._db_name = os.environ["db_name"]
        self._db_usr_name = os.environ["db_usr_name"]
        self._client_id = os.environ["client_id"]
        self._client_secret = os.environ["client_secret"]
        self._usr_agent = os.environ["usr_agent"]
        return self

    @classmethod
    def from_json_file(cls, path: str):
        if os.path.exists(path):
            with open(path, "r") as f:
                self = cls()
                data = json.load(f)
                self._db_host = data["db_host"]
                self._db_port = data["db_port"]
                self._db_pass = data["db_pass"]
                self._db_name = data["db_name"]
                self._db_usr_name = data["db_usr_name"]
                self._client_id = data["client_id"]
                self._client_secret = data["client_secret"]
                self._usr_agent = data["usr_agent"]
        return self

    @classmethod
    def from_dict(cls, data: dict):
        self = cls()
        self._db_host = data["db_host"]
        self._db_port = data["db_port"]
        self._db_pass = data["db_pass"]
        self._db_name = data["db_name"]
        self._db_usr_name = data["db_usr_name"]
        self._client_id = data["client_id"]
        self._client_secret = data["client_secret"]
        self._usr_agent = data["usr_agent"]
        return self

    @classmethod
    def from_database(cls, db: Session):
        conf: ConfigDB = db.query(ConfigDB).first()
        if conf:
            self = cls()
            self._db_host = conf.db_host
            self._db_port = conf.db_port
            self._db_pass = conf.db_pass
            self._db_name = conf.db_name
            self._db_usr_name = conf.db_usr_name
            self._client_id = conf.client_id
            self._client_secret = conf.client_secret
            self._usr_agent = conf.usr_agent
        return self

    @classmethod
    def from_local(cls):
        self = cls()
        self._db_host = _settings.db_host
        self._db_port = _settings.db_port
        self._db_pass = _settings.db_pass
        self._db_name = _settings.db_name
        self._db_usr_name = _settings.db_usr_name
        self._client_id = _settings.client_id
        self._client_secret = _settings.client_secret
        self._usr_agent = _settings.usr_agent
        return self

    def is_empty(self) -> bool:
        """return True if all attributes are None"""
        return all([getattr(self, attr) is None for attr in self.__dict__])

    def _to_json(self):
        return {
            "db_host": self._db_host,
            "db_port": self._db_port,
            "db_pass": self._db_pass,
            "db_name": self._db_name,
            "db_usr_name": self._db_usr_name,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "usr_agent": self._usr_agent,
        }

    def database_url(self) -> str:
        return f"postgresql://{self._db_usr_name}:{self._db_pass}@{self._db_host}:{self._db_port}/{self._db_name}"

    def build_reddit_instance(self) -> Reddit:
        """return the reddit instance for the praw api"""
        reddit = Reddit(
            client_id=self._client_id,
            client_secret=self._client_secret,
            user_agent=self._usr_agent,
        )
        return reddit

    # a method to try all the methods to get the config starting from the from_env, then from_locals, then from_json_file
    @classmethod
    def try_build_config(cls, path: str = None):
        try:
            return cls.from_env()
        except KeyError:
            try:
                return cls.from_local()
            except NameError:
                if path:
                    try:
                        return cls.from_json_file(path)
                    except FileNotFoundError:
                        return cls()
                else:
                    return cls()

    def write_to_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self._to_json(), f)

    def __dict__(self):
        return self._to_json()

    @property
    def db_host(self):
        return self._db_host

    @property
    def db_port(self):
        return self._db_port

    @property
    def db_pass(self):
        return self._db_pass

    @property
    def db_name(self):
        return self._db_name

    @property
    def db_usr_name(self):
        return self._db_usr_name

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret

    @property
    def usr_agent(self):
        return self._usr_agent
