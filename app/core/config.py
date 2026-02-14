from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """
    Application configuration settings.
    """

    app_name: str = "FastAPI"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = ""
    jwt_key: str = ""
    algorithm: str = "HS256"
    token_expire_minutes: int = 30
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}@localhost/{self.db_name}"
        )


config = Config()

