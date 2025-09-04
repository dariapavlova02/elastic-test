"""
Index management for payment vector testing.
"""
import logging
from typing import Dict, Any, Optional
from elasticsearch import TransportError

from .client import ElasticsearchClient
from config.config import config

logger = logging.getLogger(__name__)


class IndexManager:
    """Manages Elasticsearch indices for payment vector testing."""
    
    def __init__(self, es_client: ElasticsearchClient):
        """Initialize index manager."""
        self.client = es_client
        self.vector_config = config.vector
    
    def create_payment_vector_index(self, index_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Create index for payment vectors with proper mapping.
        
        Args:
            index_name: Optional custom index name
            
        Returns:
            Response from Elasticsearch
        """
        index_name = index_name or self.vector_config.index_name
        
        mapping = {
            "mappings": {
                "properties": {
                    "payment_id": {
                        "type": "keyword"
                    },
                    "amount": {
                        "type": "float"
                    },
                    "currency": {
                        "type": "keyword"
                    },
                    "sender": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "receiver": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "description": {
                        "type": "text"
                    },
                    "timestamp": {
                        "type": "date"
                    },
                    "metadata": {
                        "type": "object",
                        "properties": {
                            "bank_code": {"type": "keyword"},
                            "transaction_type": {"type": "keyword"},
                            "country": {"type": "keyword"},
                            "risk_score": {"type": "float"}
                        }
                    },
                    "vector": {
                        "type": "dense_vector",
                        "dims": self.vector_config.dimension,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "sanctions_match": {
                        "type": "boolean"
                    },
                    "sanctions_entities": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        try:
            if self.client.index_exists(index_name):
                logger.warning(f"Index {index_name} already exists")
                return {"message": f"Index {index_name} already exists"}
            
            response = self.client.client.indices.create(
                index=index_name,
                body=mapping
            )
            logger.info(f"Created index {index_name} with vector mapping")
            return response
        except TransportError as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            raise
    
    def create_sanctions_index(self, index_name: str = "sanctions") -> Dict[str, Any]:
        """
        Create index for sanctions data.
        
        Args:
            index_name: Name of the sanctions index
            
        Returns:
            Response from Elasticsearch
        """
        mapping = {
            "mappings": {
                "properties": {
                    "entity_id": {
                        "type": "keyword"
                    },
                    "name": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "aliases": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword"
                            }
                        }
                    },
                    "entity_type": {
                        "type": "keyword"
                    },
                    "country": {
                        "type": "keyword"
                    },
                    "sanctions_list": {
                        "type": "keyword"
                    },
                    "description": {
                        "type": "text"
                    },
                    "vector": {
                        "type": "dense_vector",
                        "dims": self.vector_config.dimension,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "created_at": {
                        "type": "date"
                    },
                    "updated_at": {
                        "type": "date"
                    }
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        try:
            if self.client.index_exists(index_name):
                logger.warning(f"Index {index_name} already exists")
                return {"message": f"Index {index_name} already exists"}
            
            response = self.client.client.indices.create(
                index=index_name,
                body=mapping
            )
            logger.info(f"Created sanctions index {index_name}")
            return response
        except TransportError as e:
            logger.error(f"Failed to create sanctions index {index_name}: {e}")
            raise
    
    def get_index_mapping(self, index_name: str) -> Dict[str, Any]:
        """
        Get mapping for an index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Index mapping
        """
        try:
            response = self.client.client.indices.get_mapping(index=index_name)
            return response
        except TransportError as e:
            logger.error(f"Failed to get mapping for {index_name}: {e}")
            raise
    
    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """
        Get statistics for an index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Index statistics
        """
        try:
            response = self.client.client.indices.stats(index=index_name)
            return response
        except TransportError as e:
            logger.error(f"Failed to get stats for {index_name}: {e}")
            raise
