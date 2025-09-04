"""
AI service stub for basic functionality when full AI service is not available.
"""
import logging
from typing import Dict, List, Any, Optional
import asyncio

logger = logging.getLogger(__name__)


class AIProcessorStub:
    """Stub AI processor with basic text processing."""
    
    def __init__(self):
        """Initialize stub AI processor."""
        logger.info("Initializing AI processor stub (limited functionality)")
        
    async def process_text(self, text: str, include_embeddings: bool = True, include_variants: bool = False) -> Dict[str, Any]:
        """
        Process text with basic normalization.
        
        Args:
            text: Text to process
            include_embeddings: Whether to include embeddings (stub returns empty)
            include_variants: Whether to include variants (stub returns empty)
            
        Returns:
            Dict with processing results
        """
        try:
            # Basic text normalization
            normalized = text.strip().lower()
            
            # Simple language detection based on character patterns
            language = "unknown"
            if any(ord(char) >= 0x0400 and ord(char) <= 0x04FF for char in text):
                language = "ru"  # Cyrillic
            elif all(ord(char) < 128 for char in text):
                language = "en"  # ASCII
                
            result = {
                "success": True,
                "normalized_text": normalized,
                "language": language,
                "processing_info": {
                    "method": "stub",
                    "original_length": len(text),
                    "normalized_length": len(normalized)
                }
            }
            
            if include_embeddings:
                # Return dummy embedding vector
                result["embeddings"] = [0.0] * 384  # Standard sentence-transformer size
                
            if include_variants:
                # Return basic variants
                result["variants"] = [normalized, text.strip()]
                
            return result
            
        except Exception as e:
            logger.error(f"Stub AI processing failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "normalized_text": text,
                "language": "unknown",
                "embeddings": [0.0] * 384 if include_embeddings else None,
                "variants": [text] if include_variants else None
            }


class DataNormalizerStub:
    """Stub data normalizer."""
    
    def __init__(self, ai_processor):
        """Initialize stub data normalizer."""
        self.ai_processor = ai_processor
        logger.info("Initializing data normalizer stub")
        
    async def normalize(self, text: str) -> Dict[str, Any]:
        """Normalize text using AI processor."""
        return await self.ai_processor.process_text(text, include_embeddings=False)


# Export stub classes
AIProcessor = AIProcessorStub
DataNormalizer = DataNormalizerStub