"""
Helper utilities for payment vector testing.
"""
import logging
import os
from typing import Dict, Any
from elasticsearch import Elasticsearch
from elasticsearch import TransportError

from config.config import config


def setup_logging(log_level: str = None, log_file: str = None) -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Path to log file
    """
    level = log_level or config.logging.level
    file_path = log_file or config.logging.file_path
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(file_path),
            logging.StreamHandler()
        ]
    )


def validate_elasticsearch_connection() -> Dict[str, Any]:
    """
    Validate Elasticsearch connection.
    
    Returns:
        Validation result
    """
    try:
        es_config = config.get_elasticsearch_config()
        client = Elasticsearch(**es_config)
        
        # Test connection
        info = client.info()
        
        return {
            "success": True,
            "version": info['version']['number'],
            "cluster_name": info['cluster_name'],
            "url": config.elasticsearch.url
        }
    except TransportError as e:
        return {
            "success": False,
            "error": str(e),
            "url": config.elasticsearch.url
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "url": config.elasticsearch.url
        }


def ensure_directories() -> None:
    """Ensure required directories exist."""
    directories = [
        "logs",
        "data/raw",
        "data/processed"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
