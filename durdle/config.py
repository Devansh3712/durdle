__author__ = "Devansh Singh"
__license__ = "GNU AGPLv3"
__version__ = "0.1.0"
__status__ = "Development"

from pydantic import BaseSettings

class Settings(BaseSettings):
    token: str
    password: str
    mongodb_uri: str

    class Config:
        env_file = ".env"

settings = Settings()
