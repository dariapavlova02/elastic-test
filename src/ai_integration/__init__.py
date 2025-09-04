"""
AI service integration module for payment vector testing.
"""
import logging

logger = logging.getLogger(__name__)

try:
    # Try to import full AI services
    from .ai_processor import AIProcessor
    from .data_normalizer import DataNormalizer
    logger.info("Full AI services imported successfully")
except ImportError as e:
    logger.warning(f"Full AI services not available: {e}")
    logger.info("Using AI service stubs for basic functionality")
    
    # Fallback to stub implementations
    from .ai_stub import AIProcessor, DataNormalizer

__all__ = ["AIProcessor", "DataNormalizer"]
