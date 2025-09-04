"""
AI service processor for payment vector testing.
Uses the existing AI service for text processing and vectorization.
"""
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add ai-service to path
ai_service_path = Path(__file__).parent.parent.parent / "ai-service" / "src"
sys.path.insert(0, str(ai_service_path))

try:
    from ai_service.services.orchestrator_service import OrchestratorService
    from ai_service.services.embedding_service import EmbeddingService
    from ai_service.services.normalization_service import NormalizationService
    from ai_service.services.language_detection_service import LanguageDetectionService
    from ai_service.exceptions import ProcessingError
except ImportError as e:
    logging.error(f"Failed to import AI service modules: {e}")
    raise

logger = logging.getLogger(__name__)


class AIProcessor:
    """AI service processor for text processing and vectorization."""
    
    def __init__(self):
        """Initialize AI processor."""
        try:
            # Initialize AI services
            self.orchestrator = OrchestratorService()
            self.embedding_service = EmbeddingService()
            self.normalization_service = NormalizationService()
            self.language_detection = LanguageDetectionService()
            
            logger.info("AI services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {e}")
            raise
    
    async def process_text(self, text: str, include_embeddings: bool = True) -> Dict[str, Any]:
        """
        Process text using AI service.
        
        Args:
            text: Text to process
            include_embeddings: Whether to include vector embeddings
            
        Returns:
            Processing result
        """
        try:
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty text provided",
                    "original_text": text,
                    "normalized_text": "",
                    "language": "unknown",
                    "embeddings": []
                }
            
            # Process text through orchestrator
            result = await self.orchestrator.process_text(
                text=text,
                generate_embeddings=include_embeddings,
                generate_variants=True
            )
            
            return {
                "success": result.success,
                "original_text": result.original_text,
                "normalized_text": result.normalized_text,
                "language": result.language,
                "language_confidence": result.language_confidence,
                "variants": result.variants,
                "embeddings": result.embeddings if include_embeddings else [],
                "processing_time": result.processing_time,
                "errors": result.errors or []
            }
            
        except ProcessingError as e:
            logger.error(f"AI processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "normalized_text": "",
                "language": "unknown",
                "embeddings": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in AI processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "normalized_text": "",
                "language": "unknown",
                "embeddings": []
            }
    
    async def process_payment_metadata(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process payment metadata for vectorization.
        
        Args:
            payment_data: Payment metadata dictionary
            
        Returns:
            Processed payment data with embeddings
        """
        try:
            # Combine relevant text fields
            text_parts = []
            
            # Add sender information
            if payment_data.get('sender'):
                text_parts.append(f"sender: {payment_data['sender']}")
            
            # Add receiver information
            if payment_data.get('receiver'):
                text_parts.append(f"receiver: {payment_data['receiver']}")
            
            # Add description
            if payment_data.get('description'):
                text_parts.append(f"description: {payment_data['description']}")
            
            # Add metadata fields
            if payment_data.get('metadata') and isinstance(payment_data['metadata'], dict):
                metadata = payment_data['metadata']
                if metadata.get('bank_code'):
                    text_parts.append(f"bank_code: {metadata['bank_code']}")
                if metadata.get('transaction_type'):
                    text_parts.append(f"transaction_type: {metadata['transaction_type']}")
                if metadata.get('country'):
                    text_parts.append(f"country: {metadata['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)
            
            if not combined_text.strip():
                return {
                    "success": False,
                    "error": "No text data found in payment metadata",
                    "payment_data": payment_data,
                    "embeddings": []
                }
            
            # Process text
            result = await self.process_text(combined_text, include_embeddings=True)
            
            # Add processing result to payment data
            payment_data['ai_processing'] = result
            payment_data['vector'] = result.get('embeddings', [])
            
            return {
                "success": result['success'],
                "payment_data": payment_data,
                "embeddings": result.get('embeddings', []),
                "normalized_text": result.get('normalized_text', ''),
                "language": result.get('language', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Failed to process payment metadata: {e}")
            return {
                "success": False,
                "error": str(e),
                "payment_data": payment_data,
                "embeddings": []
            }
    
    async def process_sanctions_entity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process sanctions entity for vectorization.
        
        Args:
            entity_data: Sanctions entity data
            
        Returns:
            Processed entity data with embeddings
        """
        try:
            # Combine relevant text fields
            text_parts = []
            
            # Add entity name
            if entity_data.get('name'):
                text_parts.append(f"name: {entity_data['name']}")
            
            # Add English name
            if entity_data.get('name_en'):
                text_parts.append(f"name_en: {entity_data['name_en']}")
            
            # Add Russian name
            if entity_data.get('name_ru'):
                text_parts.append(f"name_ru: {entity_data['name_ru']}")
            
            # Add description
            if entity_data.get('description'):
                text_parts.append(f"description: {entity_data['description']}")
            
            # Add address for companies
            if entity_data.get('address'):
                text_parts.append(f"address: {entity_data['address']}")
            
            # Add entity type
            if entity_data.get('entity_type'):
                text_parts.append(f"type: {entity_data['entity_type']}")
            
            # Add country
            if entity_data.get('country'):
                text_parts.append(f"country: {entity_data['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)
            
            if not combined_text.strip():
                return {
                    "success": False,
                    "error": "No text data found in sanctions entity",
                    "entity_data": entity_data,
                    "embeddings": []
                }
            
            # Process text
            result = await self.process_text(combined_text, include_embeddings=True)
            
            # Add processing result to entity data
            entity_data['ai_processing'] = result
            entity_data['vector'] = result.get('embeddings', [])
            
            return {
                "success": result['success'],
                "entity_data": entity_data,
                "embeddings": result.get('embeddings', []),
                "normalized_text": result.get('normalized_text', ''),
                "language": result.get('language', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Failed to process sanctions entity: {e}")
            return {
                "success": False,
                "error": str(e),
                "entity_data": entity_data,
                "embeddings": []
            }
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of vector embeddings
        """
        try:
            result = self.embedding_service.get_embeddings(texts)
            if result['success']:
                return result['embeddings']
            else:
                logger.error(f"Failed to get embeddings: {result.get('error', 'Unknown error')}")
                return []
        except Exception as e:
            logger.error(f"Failed to get embeddings: {e}")
            return []
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about AI services."""
        try:
            return {
                "orchestrator_available": self.orchestrator is not None,
                "embedding_service_available": self.embedding_service is not None,
                "normalization_service_available": self.normalization_service is not None,
                "language_detection_available": self.language_detection is not None,
                "supported_models": self.embedding_service.get_supported_models() if self.embedding_service else {}
            }
        except Exception as e:
            logger.error(f"Failed to get service info: {e}")
            return {"error": str(e)}
