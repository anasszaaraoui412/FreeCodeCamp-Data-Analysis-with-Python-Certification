from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/unoya"
    PROJECT_NAME: str = "UNOYA AI Workplace Concierge"
    API_V1_STR: str = "/api/v1"

    # Auth
    MOCK_AUTH_ENABLED: bool = True
    CLERK_API_URL: str = "https://api.clerk.dev/v1"
    CLERK_SECRET_KEY: str = ""

    class Config:
        case_sensitive = True

settings = Settings()
