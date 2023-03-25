from pydantic import BaseSettings
from pydantic import BaseModel
from typing import Any
import os
import json


class ConfFormData(BaseModel):
    db_host: str
    db_port: int
    db_pass: str
    db_name: str
    db_usr_name: str
    client_id: str
    client_secret: str
    usr_agent: str


class _settings(BaseSettings):
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
_settings = _settings()


class Config:
    def __init__(
        self,
        # local_env: bool = False,
        # form_data: dict | None = None,
        **kwargs
    ):
        if kwargs and kwargs.get('local_env') == True:
            settings = _settings
            self.db_host = settings.db_host
            self.db_port = settings.db_port
            self.db_pass = settings.db_pass
            self.db_name = settings.db_name
            self.db_usr_name = settings.db_usr_name
            self.client_id = settings.client_id
            self.client_secret = settings.client_secret
            self.usr_agent = settings.usr_agent
            self.output = None

        if kwargs and kwargs.get('form_data'):
            form_data = kwargs.get('form_data')
            self.db_host = form_data.db_host
            self.db_port = form_data.db_port
            self.db_pass = form_data.db_pass
            self.db_name = form_data.db_name
            self.db_usr_name = form_data.db_usr_name
            self.client_id = form_data.client_id
            self.client_secret = form_data.client_secret
            self.usr_agent = form_data.usr_agent
            self.output = None


    def set_output(self, output: str):
        self.output = output

    def __dict__(self):
        return self.to_json()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self) -> dict[str, Any]:
        return {
            'db_host': self.db_host,
            'db_port': self.db_port,
            'db_pass': self.db_pass,
            'db_name': self.db_name,
            'db_usr_name': self.db_usr_name,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'usr_agent': self.usr_agent,
            'output': self.output
        }


config = Config()
