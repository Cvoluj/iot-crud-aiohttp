from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    DB_PORT: int
    DB_HOST: str
    POSTGRES_PASSWORD: int
    POSTGRES_USER: str
    POSTGRES_DATABASE:str

    @property
    def DB_URL(self):
        return f'mysql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DATABASE}'        

    model_config = SettingsConfigDict(env_file='.env')


server_setting = ServerSettings()