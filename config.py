from pydantic import BaseSettings
from pydantic import BaseModel
from typing import Any
import os


class ConfigForm(BaseModel):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    client_id: str
    client_secret: str
    user_agent: str


class _Settings(BaseSettings, ConfigForm):
    class Config:
        env_file = os.path.abspath(__file__).replace(os.path.basename(__file__), ".env")


# initialize an instance of this class to import elsewhere
_settings = _Settings()


class Config:
    def __init__(
        self,
        db_host: str | int | None = None,
        db_port: int | None = None,
        db_passwd: Any | None = None,
        db_name: str | None = None,
        db_usr_name: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
        usr_agent: str | None = None,
        form_data: ConfigForm | None = None,
        env_file: Any | None = None,
        output_type: str | None = None,
    ):
        self.output
        if settings is None:
            settings = _settings
        self.db_host = settings.database_hostname
        self.db_port = settings.database_port
        self.db_pass = settings.database_password
        self.db_name = settings.database_name
        self.db_usr_name = settings.database_username
        self.client_id = settings.client_id
        self.client_secret = settings.client_secret
        self.usr_agent = settings.user_agent
        self.output = None

        if form_data:
            self.db_host = form_data.db_hostname
            self.db_port = form_data.db_port
            self.db_pass = form_data.db_pass
            self.db_name = form_data.db_name
            self.db_usr_name = form_data.db_usr_name
            self.client_id = form_data.client_id
            self.client_secret = form_data.client_secret
            self.usr_agent = form_data.usr_agent
            self.output = None


# conf = Config()
# print(conf.db_host)
_ = _Settings()
print(_.database_hostname)
