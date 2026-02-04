from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    log_level: str = "INFO"
    api_prefix: str = "/v1"

    # NVIDIA NIM
    nim_base_url: str
    nim_api_key: str
    nim_model: str
    nim_timeout_s: int = 20
    nim_max_retries: int = 2

    # Supabase
    supabase_url: str | None = None
    supabase_service_key: str | None = None
    supabase_table_runs: str = "runs"


settings = Settings()
