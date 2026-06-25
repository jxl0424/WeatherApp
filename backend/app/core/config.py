from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=[".env", "../.env"], env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str
    ALLOWED_ORIGINS: str = "http://localhost:3000"

    NVIDIA_API_KEY: str = ""
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL: str = "minimaxai/minimax-m3"

    APP_ENV: str = "development"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()
