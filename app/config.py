from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    host: str = Field(validation_alias='DB_HOST')
    password: str = Field(validation_alias='DB_PASS')
    username: str = Field(validation_alias='DB_USER')
    database: str = Field(validation_alias='DB_NAME')
    port: int = Field(validation_alias='DB_PORT')

    model_config = SettingsConfigDict(env_file='.env', populate_by_name=True)
