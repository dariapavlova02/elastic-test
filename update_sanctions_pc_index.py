#!/usr/bin/env python3
"""
Create or recreate a parent-child index with join field for sanctions and variants.
Index: sanctions_pc
Parent type: entity
Child type: variant
"""
import requests


def update_sanctions_pc_index(base_url: str = "http://95.217.84.234:9200") -> bool:
    idx = f"{base_url.rstrip('/')}/sanctions_pc"
    try:
        # Delete existing index
        try:
            del_resp = requests.delete(idx)
            print(f"Delete sanctions_pc: {del_resp.status_code}")
        except Exception as e:
            print(f"Delete sanctions_pc skipped: {e}")

        mapping = {
            "mappings": {
                "properties": {
                    "doc_rel": {"type": "join", "relations": {"entity": "variant"}},
                    "name": {"type": "text", "analyzer": "standard"},
                    "name_en": {"type": "text", "analyzer": "standard"},
                    "name_ru": {"type": "text", "analyzer": "standard"},
                    "entity_type": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
                    "text": {"type": "text", "analyzer": "standard"},
                    "lang": {"type": "keyword"},
                    "weight": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        put_resp = requests.put(idx, json=mapping)
        print(f"Create sanctions_pc: {put_resp.status_code}")
        print(put_resp.text)
        return put_resp.status_code == 200
    except Exception as e:
        print(f"Failed to create sanctions_pc: {e}")
        return False


if __name__ == "__main__":
    update_sanctions_pc_index()

