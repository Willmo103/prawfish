from pydantic import BaseSettings
from pydantic import BaseModel
from typing import Any
import os


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
        local_env: bool = False,
        form_data: dict | None = None
    ):
        if local_env:
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

        if form_data:
            self.db_host = form_data.db_host
            self.db_port = form_data.db_port
            self.db_pass = form_data.db_pass
            self.db_name = form_data.db_name
            self.db_usr_name = form_data.db_usr_name
            self.client_id = form_data.client_id
            self.client_secret = form_data.client_secret
            self.usr_agent = form_data.usr_agent
            self.output = None

config = Config()
