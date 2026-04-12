from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_secret_key: str = "default_secret_key"
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ivr_adherence"
    
    # Africa's Talking
    at_username: str = "sandbox"
    at_api_key: str = "your_sandbox_api_key_here"
    at_virtual_number: str = "+254711082000"
    
    # Base Application URL (for webhooks/MP3s)
    base_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
