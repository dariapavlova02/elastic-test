#!/usr/bin/env python3
"""
Script for loading sanctions data into Elasticsearch.
This script runs locally and loads vectorized sanctions data.
"""
import sys
import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.es_client import ElasticsearchClient, IndexManager
from src.ai_integration import AIProcessor, DataNormalizer
from src.sanctions import SanctionsLoader
from config.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SanctionsLoader:
    """Load sanctions data into Elasticsearch."""
    
    def __init__(self, elasticsearch_url: str = "http://localhost:9200"):
        """Initialize the loader."""
        self.es_client = ElasticsearchClient(elasticsearch_url)
        self.index_manager = IndexManager(self.es_client)
        self.ai_processor = AIProcessor()
        self.data_normalizer = DataNormalizer(self.ai_processor)
        self.sanctions_loader = SanctionsLoader(ai_processor=self.ai_processor)
        
    def create_indices(self):
        """Create Elasticsearch indices."""
        try:
            logger.info("Creating Elasticsearch indices...")
            
            # Create sanctions index
            self.index_manager.create_sanctions_index("sanctions")
            logger.info("Created sanctions index")
            
            return True
        except Exception as e:
            logger.error(f"Failed to create indices: {e}")
            return False
    
    async def load_sanctions_from_files(self, data_path: str) -> Dict[str, Any]:
        """Load sanctions data from files."""
        data_path = Path(data_path)
        results = {
            "persons": {"loaded": 0, "failed": 0},
            "companies": {"loaded": 0, "failed": 0},
            "terrorism": {"loaded": 0, "failed": 0}
        }
        
        # Load persons
        persons_file = data_path / "sanctioned_persons.json"
        if persons_file.exists():
            logger.info(f"Loading persons from {persons_file}")
            result = await self._load_sanctions_file(persons_file, "person")
            results["persons"] = result
            logger.info(f"Persons: {result['loaded']} loaded, {result['failed']} failed")
        
        # Load companies
        companies_file = data_path / "sanctioned_companies.json"
        if companies_file.exists():
            logger.info(f"Loading companies from {companies_file}")
            result = await self._load_sanctions_file(companies_file, "company")
            results["companies"] = result
            logger.info(f"Companies: {result['loaded']} loaded, {result['failed']} failed")
        
        # Load terrorism
        terrorism_file = data_path / "terrorism_black_list.json"
        if terrorism_file.exists():
            logger.info(f"Loading terrorism from {terrorism_file}")
            result = await self._load_sanctions_file(terrorism_file, "terrorism")
            results["terrorism"] = result
            logger.info(f"Terrorism: {result['loaded']} loaded, {result['failed']} failed")
        
        return results
    
    async def _load_sanctions_file(self, file_path: Path, entity_type: str) -> Dict[str, int]:
        """Load sanctions from a single file."""
        loaded = 0
        failed = 0
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                entities = json.load(f)
            
            logger.info(f"Processing {len(entities)} {entity_type} entities...")
            
            for i, entity in enumerate(entities):
                try:
                    # Process entity with AI
                    result = await self.ai_processor.process_sanctions_entity(entity)
                    
                    if result["success"]:
                        # Create document for Elasticsearch
                        doc = {
                            "entity_id": entity.get("id", f"{entity_type}_{i}"),
                            "name": entity.get("name", ""),
                            "name_en": entity.get("name_en", ""),
                            "name_ru": entity.get("name_ru", ""),
                            "aliases": f"{entity.get('name_en', '')} {entity.get('name_ru', '')}",
                            "entity_type": entity_type,
                            "country": entity.get("country", ""),
                            "sanctions_list": entity.get("source", ""),
                            "description": entity.get("description", ""),
                            "address": entity.get("address", ""),
                            "vector": result["embeddings"],
                            "normalized_text": result.get("normalized_text", ""),
                            "language": result.get("language", ""),
                            "variants": result.get("variants", []),
                            "created_at": datetime.now().isoformat(),
                            "updated_at": datetime.now().isoformat()
                        }
                        
                        # Index to Elasticsearch
                        self.es_client.index_document("sanctions", doc)
                        loaded += 1
                        
                        if loaded % 100 == 0:
                            logger.info(f"Loaded {loaded} {entity_type} entities...")
                    else:
                        failed += 1
                        logger.warning(f"Failed to process {entity_type} entity {i}: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    failed += 1
                    logger.warning(f"Failed to process {entity_type} entity {i}: {e}")
                    continue
            
            logger.info(f"Completed loading {entity_type}: {loaded} loaded, {failed} failed")
            
        except Exception as e:
            logger.error(f"Failed to load {entity_type} from {file_path}: {e}")
            return {"loaded": 0, "failed": 1}
        
        return {"loaded": loaded, "failed": failed}
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get loading statistics."""
        try:
            # Get index stats
            stats = self.es_client.client.indices.stats(index="sanctions")
            
            return {
                "total_documents": stats["indices"]["sanctions"]["total"]["docs"]["count"],
                "index_size": stats["indices"]["sanctions"]["total"]["store"]["size_in_bytes"],
                "index_exists": self.es_client.index_exists("sanctions")
            }
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {"error": str(e)}

async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load sanctions data into Elasticsearch")
    parser.add_argument("--elasticsearch-url", default="http://localhost:9200", help="Elasticsearch URL")
    parser.add_argument("--data-path", default="ai-service/src/ai_service/data", help="Path to data files")
    parser.add_argument("--create-indices", action="store_true", help="Create indices before loading")
    
    args = parser.parse_args()
    
    print("Payment Vector Testing - Sanctions Loader")
    print("=" * 50)
    print(f"Elasticsearch URL: {args.elasticsearch_url}")
    print(f"Data path: {args.data_path}")
    print()
    
    # Initialize loader
    loader = SanctionsLoader(args.elasticsearch_url)
    
    try:
        # Create indices if requested
        if args.create_indices:
            if not loader.create_indices():
                print("❌ Failed to create indices")
                return 1
            print("✅ Indices created successfully")
        
        # Load sanctions data
        print("\nLoading sanctions data...")
        results = await loader.load_sanctions_from_files(args.data_path)
        
        # Print summary
        print("\n" + "=" * 50)
        print("Loading Summary:")
        print("=" * 50)
        
        total_loaded = 0
        total_failed = 0
        
        for category, stats in results.items():
            print(f"{category.capitalize()}: {stats['loaded']} loaded, {stats['failed']} failed")
            total_loaded += stats['loaded']
            total_failed += stats['failed']
        
        print(f"\nTotal: {total_loaded} loaded, {total_failed} failed")
        
        # Get final statistics
        print("\nFinal Statistics:")
        stats = loader.get_statistics()
        if "error" not in stats:
            print(f"  Total documents: {stats['total_documents']}")
            print(f"  Index size: {stats['index_size']} bytes")
            print(f"  Index exists: {stats['index_exists']}")
        else:
            print(f"  Error getting stats: {stats['error']}")
        
        print("\n🎉 Sanctions loading completed successfully!")
        print(f"Data is now available in Elasticsearch at {args.elasticsearch_url}")
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
