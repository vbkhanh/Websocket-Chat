from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_HOST : str
    POSTGRES_PORT : str
    POSTGRES_DB : str

    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_MAX: int = 20
    DATABASE_POOL_TIMEOUT: int = 30

    REDIS_HOST : str
    REDIS_PORT : int
    REDIS_DB: int = 0

    ALLOW_ORIGINS: list[str] = ["*"]

    @property
    def DB_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

settings = Settings()
