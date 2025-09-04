#!/usr/bin/env python3
"""
Create sanctions index with correct vector dimensions.
"""
import requests
import json

def create_sanctions_index():
    """Create sanctions index with proper mapping."""
    
    # Index mapping with correct vector dimensions (384)
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "name": {"type": "text", "analyzer": "standard"},
                "name_en": {"type": "text", "analyzer": "standard"},
                "name_ru": {"type": "text", "analyzer": "standard"},
                "entity_type": {"type": "keyword"},
                "birthdate": {"type": "date"},
                "itn": {"type": "keyword"},
                "status": {"type": "keyword"},
                "source": {"type": "keyword"},
                "vector": {
                    "type": "dense_vector",
                    "dims": 384
                }
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    # Create index via Elasticsearch API
    url = "http://95.217.84.234:9200/sanctions"
    
    response = requests.put(url, json=mapping)
    
    if response.status_code == 200:
        print("✅ Sanctions index created successfully!")
        print(f"Response: {response.json()}")
        return True
    else:
        print(f"❌ Failed to create index: {response.status_code}")
        print(f"Error: {response.text}")
        return False

if __name__ == "__main__":
    create_sanctions_index()
