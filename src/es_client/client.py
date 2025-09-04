"""
Elasticsearch client wrapper for payment vector testing.
"""
import logging
from typing import Dict, List, Optional, Any
from elasticsearch import Elasticsearch
from elasticsearch import TransportError

from config.config import config

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Elasticsearch client wrapper with error handling."""
    
    def __init__(self):
        """Initialize Elasticsearch client."""
        self.client = self._create_client()
        self._test_connection()
    
    def _create_client(self) -> Elasticsearch:
        """Create Elasticsearch client with configuration."""
        try:
            es_config = config.get_elasticsearch_config()
            client = Elasticsearch(**es_config)
            logger.info(f"Created Elasticsearch client for {config.elasticsearch.url}")
            return client
        except Exception as e:
            logger.error(f"Failed to create Elasticsearch client: {e}")
            raise
    
    def _test_connection(self) -> None:
        """Test connection to Elasticsearch."""
        try:
            info = self.client.info()
            logger.info(f"Connected to Elasticsearch: {info['version']['number']}")
        except TransportError as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            raise
    
    def index_document(self, index_name: str, document: Dict[str, Any], 
                      doc_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Index a document in Elasticsearch.
        
        Args:
            index_name: Name of the index
            document: Document to index
            doc_id: Optional document ID
            
        Returns:
            Response from Elasticsearch
        """
        try:
            response = self.client.index(
                index=index_name,
                body=document,
                id=doc_id
            )
            logger.debug(f"Indexed document in {index_name}: {response['_id']}")
            return response
        except TransportError as e:
            logger.error(f"Failed to index document: {e}")
            raise
    
    def bulk_index(self, index_name: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Bulk index multiple documents.
        
        Args:
            index_name: Name of the index
            documents: List of documents to index
            
        Returns:
            Response from Elasticsearch
        """
        try:
            actions = []
            for doc in documents:
                action = {
                    "_index": index_name,
                    "_source": doc
                }
                actions.append(action)
            
            response = self.client.bulk(body=actions)
            logger.info(f"Bulk indexed {len(documents)} documents to {index_name}")
            return response
        except TransportError as e:
            logger.error(f"Failed to bulk index documents: {e}")
            raise
    
    def search(self, index_name: str, query: Dict[str, Any], 
              size: int = 10) -> Dict[str, Any]:
        """
        Search documents in Elasticsearch.
        
        Args:
            index_name: Name of the index
            query: Search query
            size: Number of results to return
            
        Returns:
            Search results
        """
        try:
            response = self.client.search(
                index=index_name,
                body=query,
                size=size
            )
            logger.debug(f"Search completed in {index_name}: {response['hits']['total']['value']} hits")
            return response
        except TransportError as e:
            logger.error(f"Failed to search documents: {e}")
            raise
    
    def vector_search(self, index_name: str, vector: List[float], 
                     size: int = 10, similarity_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Perform vector similarity search.
        
        Args:
            index_name: Name of the index
            vector: Query vector
            size: Number of results to return
            similarity_threshold: Minimum similarity score
            
        Returns:
            Search results
        """
        query = {
            "knn": {
                "field": "vector",
                "query_vector": vector,
                "k": size,
                "num_candidates": size * 2
            },
            "min_score": similarity_threshold
        }
        
        return self.search(index_name, query, size)
    
    def delete_index(self, index_name: str) -> Dict[str, Any]:
        """
        Delete an index.
        
        Args:
            index_name: Name of the index to delete
            
        Returns:
            Response from Elasticsearch
        """
        try:
            response = self.client.indices.delete(index=index_name)
            logger.info(f"Deleted index: {index_name}")
            return response
        except TransportError as e:
            logger.error(f"Failed to delete index {index_name}: {e}")
            raise
    
    def index_exists(self, index_name: str) -> bool:
        """
        Check if index exists.
        
        Args:
            index_name: Name of the index
            
        Returns:
            True if index exists, False otherwise
        """
        try:
            return self.client.indices.exists(index=index_name)
        except TransportError as e:
            logger.error(f"Failed to check if index exists: {e}")
            return False
