"""
Data normalizer for payment and sanctions data using AI service.
"""
import logging
from typing import Dict, List, Any, Optional
import json
from pathlib import Path

from .ai_processor import AIProcessor

logger = logging.getLogger(__name__)


class DataNormalizer:
    """Normalizes data using AI service for better vectorization."""
    
    def __init__(self, ai_processor: Optional[AIProcessor] = None):
        """
        Initialize data normalizer.
        
        Args:
            ai_processor: AI processor instance
        """
        self.ai_processor = ai_processor or AIProcessor()
    
    def normalize_payment_data(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize payment data for better processing.
        
        Args:
            payment_data: Raw payment data
            
        Returns:
            Normalized payment data
        """
        try:
            normalized = payment_data.copy()
            
            # Normalize text fields
            text_fields = ['sender', 'receiver', 'description']
            for field in text_fields:
                if field in normalized and normalized[field]:
                    result = self.ai_processor.process_text(str(normalized[field]), include_embeddings=False)
                    if result['success']:
                        normalized[f"{field}_normalized"] = result['normalized_text']
                        normalized[f"{field}_language"] = result['language']
                    else:
                        normalized[f"{field}_normalized"] = str(normalized[field])
                        normalized[f"{field}_language"] = "unknown"
            
            # Normalize metadata fields
            if 'metadata' in normalized and isinstance(normalized['metadata'], dict):
                metadata = normalized['metadata'].copy()
                
                # Normalize transaction type
                if 'transaction_type' in metadata and metadata['transaction_type']:
                    result = self.ai_processor.process_text(str(metadata['transaction_type']), include_embeddings=False)
                    if result['success']:
                        metadata['transaction_type_normalized'] = result['normalized_text']
                        metadata['transaction_type_language'] = result['language']
                
                # Normalize country
                if 'country' in metadata and metadata['country']:
                    result = self.ai_processor.process_text(str(metadata['country']), include_embeddings=False)
                    if result['success']:
                        metadata['country_normalized'] = result['normalized_text']
                        metadata['country_language'] = result['language']
                
                normalized['metadata'] = metadata
            
            return normalized
            
        except Exception as e:
            logger.error(f"Failed to normalize payment data: {e}")
            return payment_data
    
    def normalize_sanctions_entity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize sanctions entity data.
        
        Args:
            entity_data: Raw sanctions entity data
            
        Returns:
            Normalized entity data
        """
        try:
            normalized = entity_data.copy()
            
            # Normalize name fields
            name_fields = ['name', 'name_en', 'name_ru']
            for field in name_fields:
                if field in normalized and normalized[field]:
                    result = self.ai_processor.process_text(str(normalized[field]), include_embeddings=False)
                    if result['success']:
                        normalized[f"{field}_normalized"] = result['normalized_text']
                        normalized[f"{field}_language"] = result['language']
                    else:
                        normalized[f"{field}_normalized"] = str(normalized[field])
                        normalized[f"{field}_language"] = "unknown"
            
            # Normalize description
            if 'description' in normalized and normalized['description']:
                result = self.ai_processor.process_text(str(normalized['description']), include_embeddings=False)
                if result['success']:
                    normalized['description_normalized'] = result['normalized_text']
                    normalized['description_language'] = result['language']
            
            # Normalize address
            if 'address' in normalized and normalized['address']:
                result = self.ai_processor.process_text(str(normalized['address']), include_embeddings=False)
                if result['success']:
                    normalized['address_normalized'] = result['normalized_text']
                    normalized['address_language'] = result['language']
            
            return normalized
            
        except Exception as e:
            logger.error(f"Failed to normalize sanctions entity: {e}")
            return entity_data
    
    def batch_normalize_payments(self, payments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a batch of payments.
        
        Args:
            payments: List of payment data
            
        Returns:
            List of normalized payment data
        """
        try:
            normalized_payments = []
            for i, payment in enumerate(payments):
                try:
                    normalized = self.normalize_payment_data(payment)
                    normalized_payments.append(normalized)
                except Exception as e:
                    logger.error(f"Failed to normalize payment {i}: {e}")
                    normalized_payments.append(payment)  # Keep original if normalization fails
            
            logger.info(f"Normalized {len(normalized_payments)} out of {len(payments)} payments")
            return normalized_payments
            
        except Exception as e:
            logger.error(f"Failed to batch normalize payments: {e}")
            return payments
    
    def batch_normalize_sanctions(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a batch of sanctions entities.
        
        Args:
            entities: List of sanctions entity data
            
        Returns:
            List of normalized entity data
        """
        try:
            normalized_entities = []
            for i, entity in enumerate(entities):
                try:
                    normalized = self.normalize_sanctions_entity(entity)
                    normalized_entities.append(normalized)
                except Exception as e:
                    logger.error(f"Failed to normalize entity {i}: {e}")
                    normalized_entities.append(entity)  # Keep original if normalization fails
            
            logger.info(f"Normalized {len(normalized_entities)} out of {len(entities)} entities")
            return normalized_entities
            
        except Exception as e:
            logger.error(f"Failed to batch normalize sanctions: {e}")
            return entities
