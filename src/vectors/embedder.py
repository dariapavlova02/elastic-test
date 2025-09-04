"""
Vector embedding generation for payment metadata and sanctions data.
Uses the existing EmbeddingService from ai-service.
"""
import logging
import sys
import os
from typing import List, Dict, Any, Optional
import numpy as np

# Add ai-service to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'ai-service', 'src'))

from ai_service.services.embedding_service import EmbeddingService
from config.config import config

logger = logging.getLogger(__name__)


class VectorEmbedder:
    """Generates vector embeddings for text data using ai-service EmbeddingService."""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        Initialize vector embedder.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name or config.vector.model_name
        self.embedding_service = EmbeddingService(default_model=self.model_name)
        self.dimension = config.vector.dimension
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Vector embedding as list of floats
        """
        try:
            if not text or not text.strip():
                logger.warning("Empty text provided for embedding")
                return [0.0] * self.dimension
            
            result = self.embedding_service.get_embeddings(text)
            if result['success'] and result['embeddings']:
                return result['embeddings'][0]
            else:
                logger.error(f"Failed to embed text: {result.get('error', 'Unknown error')}")
                return [0.0] * self.dimension
        except Exception as e:
            logger.error(f"Failed to embed text: {e}")
            raise
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of vector embeddings
        """
        try:
            if not texts:
                logger.warning("Empty list of texts provided")
                return []
            
            # Filter out empty texts
            valid_texts = [text for text in texts if text and text.strip()]
            if not valid_texts:
                logger.warning("No valid texts to embed")
                return []
            
            result = self.embedding_service.get_embeddings(valid_texts)
            if result['success'] and result['embeddings']:
                return result['embeddings']
            else:
                logger.error(f"Failed to embed texts: {result.get('error', 'Unknown error')}")
                return []
        except Exception as e:
            logger.error(f"Failed to embed texts: {e}")
            raise
    
    def embed_payment_metadata(self, payment_data: Dict[str, Any]) -> List[float]:
        """
        Generate embedding for payment metadata.
        
        Args:
            payment_data: Dictionary containing payment information
            
        Returns:
            Vector embedding for payment metadata
        """
        try:
            # Combine relevant text fields for embedding
            text_parts = []
            
            # Add sender information
            if 'sender' in payment_data and payment_data['sender']:
                text_parts.append(f"sender: {payment_data['sender']}")
            
            # Add receiver information
            if 'receiver' in payment_data and payment_data['receiver']:
                text_parts.append(f"receiver: {payment_data['receiver']}")
            
            # Add description
            if 'description' in payment_data and payment_data['description']:
                text_parts.append(f"description: {payment_data['description']}")
            
            # Add metadata fields
            if 'metadata' in payment_data and isinstance(payment_data['metadata'], dict):
                metadata = payment_data['metadata']
                if 'bank_code' in metadata and metadata['bank_code']:
                    text_parts.append(f"bank_code: {metadata['bank_code']}")
                if 'transaction_type' in metadata and metadata['transaction_type']:
                    text_parts.append(f"transaction_type: {metadata['transaction_type']}")
                if 'country' in metadata and metadata['country']:
                    text_parts.append(f"country: {metadata['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)
            
            if not combined_text.strip():
                logger.warning("No text data found in payment metadata")
                return [0.0] * self.dimension
            
            return self.embed_text(combined_text)
        except Exception as e:
            logger.error(f"Failed to embed payment metadata: {e}")
            raise
    
    def embed_sanctions_entity(self, entity_data: Dict[str, Any]) -> List[float]:
        """
        Generate embedding for sanctions entity.
        
        Args:
            entity_data: Dictionary containing sanctions entity information
            
        Returns:
            Vector embedding for sanctions entity
        """
        try:
            # Combine relevant text fields for embedding
            text_parts = []
            
            # Add entity name
            if 'name' in entity_data and entity_data['name']:
                text_parts.append(f"name: {entity_data['name']}")
            
            # Add aliases
            if 'aliases' in entity_data and entity_data['aliases']:
                if isinstance(entity_data['aliases'], list):
                    aliases_text = " ".join(entity_data['aliases'])
                else:
                    aliases_text = str(entity_data['aliases'])
                text_parts.append(f"aliases: {aliases_text}")
            
            # Add description
            if 'description' in entity_data and entity_data['description']:
                text_parts.append(f"description: {entity_data['description']}")
            
            # Add entity type
            if 'entity_type' in entity_data and entity_data['entity_type']:
                text_parts.append(f"type: {entity_data['entity_type']}")
            
            # Add country
            if 'country' in entity_data and entity_data['country']:
                text_parts.append(f"country: {entity_data['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)
            
            if not combined_text.strip():
                logger.warning("No text data found in sanctions entity")
                return [0.0] * self.dimension
            
            return self.embed_text(combined_text)
        except Exception as e:
            logger.error(f"Failed to embed sanctions entity: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        try:
            return self.embedding_service.get_model_info(self.model_name)
        except Exception as e:
            logger.error(f"Failed to get model info: {e}")
            return {"error": str(e)}
