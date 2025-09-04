"""
Sanctions matching service for payment vector testing.
"""
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

from .sanctions_loader import SanctionsLoader
from ..ai_integration import AIProcessor

logger = logging.getLogger(__name__)


class SanctionsMatcher:
    """Matches payment metadata against sanctions lists using vector similarity."""
    
    def __init__(self, sanctions_loader: Optional[SanctionsLoader] = None, 
                 ai_processor: Optional[AIProcessor] = None):
        """
        Initialize sanctions matcher.
        
        Args:
            sanctions_loader: Sanctions data loader
            ai_processor: AI processor for text processing
        """
        self.sanctions_loader = sanctions_loader or SanctionsLoader()
        self.ai_processor = ai_processor or AIProcessor()
        self.similarity_threshold = 0.7
        
        # Pre-compute embeddings for sanctions entities
        self._precompute_sanctions_embeddings()
    
    def _precompute_sanctions_embeddings(self) -> None:
        """Pre-compute embeddings for all sanctions entities."""
        try:
            logger.info("Pre-computing embeddings for sanctions entities...")
            
            # Get processed entities with AI
            processed_entities = self.sanctions_loader.get_processed_sanctions_entities()
            
            # Extract embeddings and entities
            self.sanctions_embeddings = []
            self.sanctions_entities = []
            
            for entity in processed_entities:
                if 'vector' in entity and entity['vector']:
                    self.sanctions_embeddings.append(entity['vector'])
                    self.sanctions_entities.append(entity)
                else:
                    logger.warning(f"Entity {entity.get('id', 'unknown')} has no vector, skipping")
            
            logger.info(f"Pre-computed embeddings for {len(self.sanctions_entities)} sanctions entities")
        except Exception as e:
            logger.error(f"Failed to pre-compute sanctions embeddings: {e}")
            self.sanctions_embeddings = []
            self.sanctions_entities = []
    
    def match_payment_against_sanctions(self, payment_data: Dict[str, Any], 
                                      threshold: Optional[float] = None) -> Dict[str, Any]:
        """
        Match payment metadata against sanctions lists.
        
        Args:
            payment_data: Payment metadata dictionary
            threshold: Similarity threshold (optional)
            
        Returns:
            Matching results
        """
        try:
            threshold = threshold or self.similarity_threshold
            
            # Process payment with AI to get embedding
            result = self.ai_processor.process_payment_metadata(payment_data)
            if not result['success']:
                return {
                    "success": False,
                    "error": f"Failed to process payment: {result.get('error', 'Unknown error')}",
                    "matches": []
                }
            
            payment_embedding = result['embeddings']
            
            if not payment_embedding or all(x == 0.0 for x in payment_embedding):
                return {
                    "success": False,
                    "error": "Failed to generate payment embedding",
                    "matches": []
                }
            
            # Calculate similarities
            matches = []
            for i, (entity, entity_embedding) in enumerate(zip(self.sanctions_entities, self.sanctions_embeddings)):
                similarity = self._calculate_cosine_similarity(payment_embedding, entity_embedding)
                
                if similarity >= threshold:
                    match = {
                        "entity": entity,
                        "similarity_score": similarity,
                        "match_rank": len(matches) + 1
                    }
                    matches.append(match)
            
            # Sort by similarity score
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return {
                "success": True,
                "payment_id": payment_data.get('payment_id', 'unknown'),
                "total_matches": len(matches),
                "threshold": threshold,
                "matches": matches
            }
            
        except Exception as e:
            logger.error(f"Failed to match payment against sanctions: {e}")
            return {
                "success": False,
                "error": str(e),
                "matches": []
            }
    
    def match_text_against_sanctions(self, text: str, threshold: Optional[float] = None) -> Dict[str, Any]:
        """
        Match text against sanctions lists.
        
        Args:
            text: Text to match
            threshold: Similarity threshold (optional)
            
        Returns:
            Matching results
        """
        try:
            threshold = threshold or self.similarity_threshold
            
            # Process text with AI to get embedding
            result = self.ai_processor.process_text(text, include_embeddings=True)
            if not result['success']:
                return {
                    "success": False,
                    "error": f"Failed to process text: {result.get('error', 'Unknown error')}",
                    "matches": []
                }
            
            text_embedding = result['embeddings']
            
            if not text_embedding or all(x == 0.0 for x in text_embedding):
                return {
                    "success": False,
                    "error": "Failed to generate text embedding",
                    "matches": []
                }
            
            # Calculate similarities
            matches = []
            for i, (entity, entity_embedding) in enumerate(zip(self.sanctions_entities, self.sanctions_embeddings)):
                similarity = self._calculate_cosine_similarity(text_embedding, entity_embedding)
                
                if similarity >= threshold:
                    match = {
                        "entity": entity,
                        "similarity_score": similarity,
                        "match_rank": len(matches) + 1
                    }
                    matches.append(match)
            
            # Sort by similarity score
            matches.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return {
                "success": True,
                "query_text": text,
                "total_matches": len(matches),
                "threshold": threshold,
                "matches": matches
            }
            
        except Exception as e:
            logger.error(f"Failed to match text against sanctions: {e}")
            return {
                "success": False,
                "error": str(e),
                "matches": []
            }
    
    def _calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        try:
            # Convert to numpy arrays
            v1 = np.array(vec1)
            v2 = np.array(vec2)
            
            # Calculate cosine similarity
            dot_product = np.dot(v1, v2)
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except Exception as e:
            logger.error(f"Failed to calculate cosine similarity: {e}")
            return 0.0
    
    def get_sanctions_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded sanctions data."""
        return self.sanctions_loader.get_statistics()
    
    def update_threshold(self, threshold: float) -> None:
        """Update similarity threshold."""
        self.similarity_threshold = threshold
        logger.info(f"Updated similarity threshold to {threshold}")
    
    def get_top_matches(self, payment_data: Dict[str, Any], top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Get top K matches for payment data.
        
        Args:
            payment_data: Payment metadata
            top_k: Number of top matches to return
            
        Returns:
            List of top matches
        """
        result = self.match_payment_against_sanctions(payment_data, threshold=0.0)
        if result['success']:
            return result['matches'][:top_k]
        return []
