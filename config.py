from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    client_id: str
    client_secret: str
    user_agent: str

    class Config:
        env_file = os.path.abspath(__file__).replace(os.path.basename(__file__), ".env")


# initialize an instance of this class to import elsewhere
settings = Settings()
