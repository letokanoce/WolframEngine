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
    COSUMER_KEY: str = Field(..., env="COSUMER_KEY")
    COSUMER_PASSWORD: str = Field(..., env="COSUMER_PASSWORD")


class Settings(CommonSettings, ServerSettings, WLSettings):
    pass
