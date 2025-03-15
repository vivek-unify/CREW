# config.py
import os
import logging
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# Configure logger
logger = logging.getLogger(__name__)

class Config:
    """Configuration manager for the CrewAI system."""
    
    def __init__(self, env_file: str = ".env"):
        """Initialize configuration from environment variables."""
        # Load environment variables
        load_dotenv(env_file)
        
        # API keys and providers
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_openai_api_base = os.getenv("AZURE_OPENAI_API_BASE")
        self.azure_openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        
        # Default LLM settings
        self.default_llm_provider = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
        self.default_llm_model = os.getenv("DEFAULT_LLM_MODEL", "gpt-4-turbo")
        
        # System settings
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.output_base_dir = os.getenv("OUTPUT_BASE_DIR", "./generated_projects")
        self.max_rpm = int(os.getenv("MAX_RPM", "10"))
        self.test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Validate the configuration and provide warnings/errors as needed."""
        # Check for required API keys
        if not self.openai_api_key and not self.anthropic_api_key and not self.azure_openai_api_key:
            logger.error("No API keys found. Please set at least one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or AZURE_OPENAI_API_KEY")
        
        # Check for specific provider configurations
        if self.default_llm_provider == "openai" and not self.openai_api_key:
            logger.warning("OpenAI selected as provider but no OPENAI_API_KEY found")
        
        if self.default_llm_provider == "anthropic" and not self.anthropic_api_key:
            logger.warning("Anthropic selected as provider but no ANTHROPIC_API_KEY found")
        
        if self.default_llm_provider == "azure":
            if not self.azure_openai_api_key:
                logger.warning("Azure OpenAI selected as provider but no AZURE_OPENAI_API_KEY found")
            if not self.azure_openai_api_base:
                logger.warning("Azure OpenAI selected as provider but no AZURE_OPENAI_API_BASE found")
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get the appropriate LLM configuration based on the selected provider."""
        if self.default_llm_provider == "anthropic" and self.anthropic_api_key:
            return {
                "provider": "anthropic",
                "api_key": self.anthropic_api_key,
                "model": self.default_llm_model if "claude" in self.default_llm_model else "claude-3-opus-20240229"
            }
        elif self.default_llm_provider == "azure" and self.azure_openai_api_key:
            return {
                "provider": "azure",
                "api_key": self.azure_openai_api_key,
                "api_base": self.azure_openai_api_base,
                "api_version": self.azure_openai_api_version,
                "model": self.default_llm_model
            }
        else:
            # Default to OpenAI
            return {
                "provider": "openai",
                "api_key": self.openai_api_key,
                "model": self.default_llm_model
            }
    
    def configure_logging(self) -> None:
        """Configure the logging system based on settings."""
        numeric_level = getattr(logging, self.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = logging.INFO
        
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("crewai_execution.log"),
                logging.StreamHandler()
            ]
        )

# Create a global config instance
config = Config()