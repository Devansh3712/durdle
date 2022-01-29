from pydantic import BaseSettings

class Settings(BaseSettings):
    token: str
    password: str
    mongodb_uri: str

    class Config:
        env_file = ".env"

settings = Settings()
