from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv(verbose=True)


class CommonSettings(BaseSettings):
    APP_NAME: str = Field(..., env="APP_NAME")
    DEBUG_MODE: bool = Field(True, env="DEBUG_MODE")


class ServerSettings(BaseSettings):
    HOST: str = Field("localhost", env="HOST")
    PORT: int = Field(8000, env="PORT")


class WLSettings(BaseSettings):
    CONSUMER_KEY: str = Field(..., env="CONSUMER_KEY")
    CONSUMER_PASSWORD: str = Field(..., env="CONSUMER_PASSWORD")


class Settings(CommonSettings, ServerSettings, WLSettings):
    pass
