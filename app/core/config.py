from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    # Indicamos a Pydantic que lea desde el archivo .env en la raíz
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variables del sistema que no usemos aquí
    )

# Instanciamos la configuración para importarla en cualquier parte del proyecto
settings = Settings()