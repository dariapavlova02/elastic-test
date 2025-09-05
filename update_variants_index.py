#!/usr/bin/env python3
"""
Create or recreate a companion index for per-variant documents with vectors.
Index name: sanctions_variants
"""
import requests


def update_variants_index(base_url: str = "http://95.217.84.234:9200") -> bool:
    idx = f"{base_url.rstrip('/')}/sanctions_variants"
    try:
        # Delete existing index (best-effort)
        try:
            del_resp = requests.delete(idx)
            print(f"Delete sanctions_variants: {del_resp.status_code}")
        except Exception as e:
            print(f"Delete sanctions_variants skipped: {e}")

        mapping = {
            "mappings": {
                "properties": {
                    "parent_id": {"type": "keyword"},
                    "text": {"type": "text", "analyzer": "standard"},
                    "lang": {"type": "keyword"},
                    "weight": {"type": "float"},
                    "vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        put_resp = requests.put(idx, json=mapping)
        print(f"Create sanctions_variants: {put_resp.status_code}")
        print(put_resp.text)
        return put_resp.status_code == 200
    except Exception as e:
        print(f"Failed to create sanctions_variants: {e}")
        return False


if __name__ == "__main__":
    update_variants_index()

