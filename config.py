from pydantic import BaseSettings
from pydantic import BaseModel
from praw import Reddit
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
_settings = _Settings()


class Config:
    """class to hold configuration data for the app.
    __init__ params: local_env: bool
    __init__ params: form_data: ConfFormData
    """

    def __init__(
        self,
        **kwargs,
    ):
        self._json_path = None
        if kwargs:
            if kwargs.get("file_path"):
                file_path = kwargs.get("file_path")
                try:
                    self.read_from_json(file_path)
                    return
                except FileNotFoundError:
                    raise FileNotFoundError(
                        "File not found. Please check the file path and try again."
                    )

            if kwargs.get("local_env") == True:
                settings: _settings = _Settings

            elif kwargs.get("form_data"):
                settings: ConfFormData = kwargs.get("form_data")

            if settings:
                self.db_host = settings.db_host
                self.db_port = settings.db_port
                self.db_pass = settings.db_pass
                self.db_name = settings.db_name
                self.db_usr_name = settings.db_usr_name
                self.client_id = settings.client_id
                self.client_secret = settings.client_secret
                self.usr_agent = settings.usr_agent
                self.output = None

        elif not kwargs:
            try:
                self.db_host = os.environ["db_host"]
                self.db_port = os.environ["db_port"]
                self.db_pass = os.environ["db_pass"]
                self.db_name = os.environ["db_name"]
                self.db_usr_name = os.environ["db_usr_name"]
                self.client_id = os.environ["client_id"]
                self.client_secret = os.environ["client_secret"]
                self.usr_agent = os.environ["usr_agent"]
                self.output = None
                self._json_path = None
                return
            except KeyError:
                ...
            try:
                self.read_from_json()
                return
            except FileNotFoundError:
                raise FileNotFoundError(
                    "File not found. Please check the file path and try again."
                )
        else:
            raise ValueError(
                "Must provide either local_env, form_data, or file_path keyword argument"
            )

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
            "db_host": self.db_host,
            "db_port": self.db_port,
            "db_pass": self.db_pass,
            "db_name": self.db_name,
            "db_usr_name": self.db_usr_name,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "usr_agent": self.usr_agent,
            "output": self.output,
        }

    def write_to_json(
        self,
        path: str = os.path.abspath(__file__).replace(
            os.path.basename(__file__), "config.json"
        ),
    ):
        self._json_path = path
        with open(path, "w") as f:
            json.dump(self.to_json(), f)

    def read_from_json(
        self,
        path: str = os.path.abspath(__file__).replace(
            os.path.basename(__file__), "config.json"
        ),
    ):
        self._json_path = path
        try:
            with open(path, "r") as f:
                data = json.load(f)
                self.db_host = data["db_host"]
                self.db_port = data["db_port"]
                self.db_pass = data["db_pass"]
                self.db_name = data["db_name"]
                self.db_usr_name = data["db_usr_name"]
                self.client_id = data["client_id"]
                self.client_secret = data["client_secret"]
                self.usr_agent = data["usr_agent"]
                self.output = None
        except FileNotFoundError:
            raise FileNotFoundError(
                "File not found. Please check the file path and try again."
            )

    def database_url(self) -> str:
        return f"postgresql://{self.db_usr_name}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    def build_reddit_instance(self) -> Reddit:
        return Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.usr_agent,
        )


# config = Config()
