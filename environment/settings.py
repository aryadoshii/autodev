"""
Configuration Management for AutoDev
Updated for CrewAI + LiteLLM Standard
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class QubridConfig(BaseModel):
    """Qubrid AI Platform configuration"""
    # UPDATED: Now maps to the OPENAI_ keys we set in .env
    api_key: str = Field(..., description="OpenAI/Qubrid API key")
    base_url: str = Field(default="https://platform.qubrid.com/api/v1/qubridai")
    model: str = Field(default="openai/Qwen/Qwen3-Coder-30B-A3B-Instruct")
    timeout: int = Field(default=120, description="API timeout in seconds")
    max_retries: int = Field(default=3)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4000, gt=0)


class ProjectConfig(BaseModel):
    """Project generation configuration"""
    output_dir: Path = Field(default=Path("./generated_projects"))
    enable_git: bool = Field(default=True)
    enable_testing: bool = Field(default=True)
    enable_linting: bool = Field(default=True)


class StreamlitConfig(BaseModel):
    """Streamlit UI configuration"""
    server_port: int = Field(default=8501)
    server_address: str = Field(default="localhost")
    theme: str = Field(default="dark")


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field(default="INFO")
    log_file: Optional[Path] = Field(default=Path("logs/autodev.log"))
    format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )


class GitHubConfig(BaseModel):
    """GitHub integration configuration"""
    token: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    enabled: bool = Field(default=False)


class DeploymentConfig(BaseModel):
    """Deployment platform configuration"""
    vercel_token: Optional[str] = Field(default=None)
    railway_token: Optional[str] = Field(default=None)
    enabled: bool = Field(default=False)


class AppConfig(BaseModel):
    """Main application configuration"""
    qubrid: QubridConfig
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    streamlit: StreamlitConfig = Field(default_factory=StreamlitConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    github: GitHubConfig = Field(default_factory=GitHubConfig)
    deployment: DeploymentConfig = Field(default_factory=DeploymentConfig)


def load_config() -> AppConfig:
    """Load configuration from environment variables"""
    
    # UPDATED: Use the new variable names
    qubrid_config = QubridConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        base_url=os.getenv("OPENAI_API_BASE", "https://platform.qubrid.com/api/v1/qubridai"),
        model=os.getenv("OPENAI_MODEL_NAME", "openai/Qwen/Qwen3-Coder-30B-A3B-Instruct"),
        timeout=int(os.getenv("API_TIMEOUT", "120")),
        max_retries=int(os.getenv("MAX_RETRIES", "3")),
        temperature=float(os.getenv("TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("MAX_TOKENS", "4000"))
    )
    
    # Project configuration
    project_config = ProjectConfig(
        output_dir=Path(os.getenv("OUTPUT_DIR", "./generated_projects")),
        enable_git=os.getenv("ENABLE_GIT", "true").lower() == "true",
        enable_testing=os.getenv("ENABLE_TESTING", "true").lower() == "true"
    )
    
    # Streamlit configuration
    streamlit_config = StreamlitConfig(
        server_port=int(os.getenv("STREAMLIT_SERVER_PORT", "8501")),
        server_address=os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    )
    
    # Logging configuration
    logging_config = LoggingConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=Path(os.getenv("LOG_FILE", "logs/autodev.log"))
    )
    
    # GitHub configuration
    github_token = os.getenv("GITHUB_TOKEN")
    github_config = GitHubConfig(
        token=github_token,
        username=os.getenv("GITHUB_USERNAME"),
        enabled=github_token is not None
    )
    
    # Deployment configuration
    vercel_token = os.getenv("VERCEL_TOKEN")
    railway_token = os.getenv("RAILWAY_TOKEN")
    deployment_config = DeploymentConfig(
        vercel_token=vercel_token,
        railway_token=railway_token,
        enabled=vercel_token is not None or railway_token is not None
    )
    
    return AppConfig(
        qubrid=qubrid_config,
        project=project_config,
        streamlit=streamlit_config,
        logging=logging_config,
        github=github_config,
        deployment=deployment_config
    )


# Global config instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get or create global config instance"""
    global _config
    if _config is None:
        _config = load_config()
    return _config


if __name__ == "__main__":
    config = get_config()
    print("Configuration loaded:")
    print(f"  Model: {config.qubrid.model}")
    print(f"  Base URL: {config.qubrid.base_url}")
    print(f"  Output Directory: {config.project.output_dir}")