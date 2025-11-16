"""
Configuration settings for the PR Review Agent
"""
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Groq API Configuration (for Llama3)
    GROQ_API_KEY: Optional[str] = ""
    LLM_MODEL: str = "llama-3.1-70b-versatile"  # Groq Llama3 models
    LLM_TEMPERATURE: float = 0.3
    
    # OpenAI Configuration (optional, for backward compatibility)
    OPENAI_API_KEY: Optional[str] = ""
    
    # GitHub Configuration
    GITHUB_TOKEN: Optional[str] = ""
    GITHUB_API_URL: str = "https://api.github.com"
    
    # Agent Configuration
    MAX_TOKENS: int = 2000
    ENABLE_ALL_AGENTS: bool = True
    
    # FastAPI Configuration
    API_TITLE: str = "PR Review Agent API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Automated GitHub Pull Request Review Agent"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

