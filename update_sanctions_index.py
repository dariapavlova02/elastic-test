#!/usr/bin/env python3
"""
Update sanctions index to make vector optional.
"""
import requests
import json

def update_sanctions_index():
    """Update sanctions index mapping."""
    
    # Delete existing index
    delete_response = requests.delete("http://95.217.84.234:9200/sanctions")
    print(f"Delete response: {delete_response.status_code}")
    
    # New mapping with optional vector
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
                    "dims": 384,
                    "index": True,
                    "similarity": "cosine"
                },
                "variants": {
                    "type": "nested",
                    "properties": {
                        "text": {"type": "text", "analyzer": "standard"},
                        "lang": {"type": "keyword"},
                        "weight": {"type": "float"},
                        "vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"}
                    }
                }
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    # Create index
    create_response = requests.put("http://95.217.84.234:9200/sanctions", json=mapping)
    
    if create_response.status_code == 200:
        print("✅ Sanctions index updated successfully!")
        print(f"Response: {create_response.json()}")
        return True
    else:
        print(f"❌ Failed to update index: {create_response.status_code}")
        print(f"Error: {create_response.text}")
        return False

if __name__ == "__main__":
    update_sanctions_index()
