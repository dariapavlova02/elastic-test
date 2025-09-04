"""
Configuration module for Elasticsearch payment vector testing project.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ElasticsearchConfig(BaseSettings):
    """Elasticsearch configuration."""
    host: str = Field(default="localhost", env="ELASTICSEARCH_HOST")
    port: int = Field(default=9200, env="ELASTICSEARCH_PORT")
    username: Optional[str] = Field(default=None, env="ELASTICSEARCH_USERNAME")
    password: Optional[str] = Field(default=None, env="ELASTICSEARCH_PASSWORD")
    use_ssl: bool = Field(default=False, env="ELASTICSEARCH_USE_SSL")
    verify_certs: bool = Field(default=False, env="ELASTICSEARCH_VERIFY_CERTS")
    
    @property
    def url(self) -> str:
        """Get Elasticsearch URL."""
        protocol = "https" if self.use_ssl else "http"
        return f"{protocol}://{self.host}:{self.port}"


class VectorConfig(BaseSettings):
    """Vector model configuration."""
    model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        env="VECTOR_MODEL_NAME"
    )
    dimension: int = Field(default=384, env="VECTOR_DIMENSION")
    index_name: str = Field(default="payment_vectors", env="VECTOR_INDEX_NAME")


class DataConfig(BaseSettings):
    """Data paths configuration."""
    payment_data_path: str = Field(
        default="./data/raw/payments.csv",
        env="PAYMENT_DATA_PATH"
    )
    sanctions_data_path: str = Field(
        default="./data/raw/sanctions.csv",
        env="SANCTIONS_DATA_PATH"
    )


class LoggingConfig(BaseSettings):
    """Logging configuration."""
    level: str = Field(default="INFO", env="LOG_LEVEL")
    file_path: str = Field(default="./logs/app.log", env="LOG_FILE")


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.elasticsearch = ElasticsearchConfig()
        self.vector = VectorConfig()
        self.data = DataConfig()
        self.logging = LoggingConfig()
    
    def get_elasticsearch_config(self) -> dict:
        """Get Elasticsearch client configuration."""
        config = {
            "hosts": [self.elasticsearch.url],
            "verify_certs": self.elasticsearch.verify_certs,
        }
        
        if self.elasticsearch.username and self.elasticsearch.password:
            config["basic_auth"] = (
                self.elasticsearch.username,
                self.elasticsearch.password
            )
        
        return config


# Global config instance
config = Config()
