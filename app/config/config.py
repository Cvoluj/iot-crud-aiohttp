from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    SECRET_KEY: str
    
    DB_PORT: int
    DB_HOST: str
    POSTGRES_PASSWORD: int
    POSTGRES_USER: str
    POSTGRES_DATABASE:str
    
    LOG_LEVEL: str   

    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_DATABASE: str

    model_config = SettingsConfigDict(env_file='.env')


server_setting = ServerSettings()