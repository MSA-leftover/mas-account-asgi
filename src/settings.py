from pydantic import BaseSettings


class Settings(BaseSettings):
    db_protocol: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    class Config:
        env_file = ".env"


settings = Settings()
