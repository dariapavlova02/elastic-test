#!/usr/bin/env python3
"""
Load all sanctions data to Elasticsearch.
"""
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import requests
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.sanctions.sanctions_loader import SanctionsLoader
from src.ai_integration import AIProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BulkSanctionsLoader:
    """Load all sanctions data to Elasticsearch."""
    
    def __init__(self, elasticsearch_url: str = "http://95.217.84.234:9200", data_path: str = "ai-service/src/ai_service/data"):
        """Initialize the loader."""
        self.elasticsearch_url = elasticsearch_url.rstrip('/')
        self.data_path = data_path
        self.ai_processor = AIProcessor()
        self.sanctions_loader = SanctionsLoader(data_path=data_path, ai_processor=self.ai_processor)
        self.batch_size = 100  # Process in batches
        self.delay_between_batches = 1  # seconds
        
    def load_sanctions_data(self) -> List[Dict[str, Any]]:
        """Load sanctions data from files."""
        logger.info("Loading sanctions data from files...")
        return self.sanctions_loader.get_all_sanctions_entities()
    
    async def process_entity(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Process entity with AI."""
        try:
            result = await self.ai_processor.process_sanctions_entity(entity)
            
            if not result['success']:
                logger.warning(f"AI processing failed for entity: {entity.get('name', 'Unknown')}")
                return None
            
            processed = result['entity_data']
            
            # Simplify the document for Elasticsearch
            simplified = {
                'id': processed.get('id'),
                'name': processed.get('name'),
                'name_en': processed.get('name_en'),
                'name_ru': processed.get('name_ru'),
                'entity_type': processed.get('entity_type'),
                'birthdate': processed.get('birthdate'),
                'itn': processed.get('itn'),
                'status': processed.get('status'),
                'source': processed.get('source')
            }
            
            # Add vector if available
            if 'vector' in processed and processed['vector']:
                vector = processed['vector']
                # Fix vector format - flatten if it's nested
                if isinstance(vector, list) and len(vector) == 1 and isinstance(vector[0], list):
                    vector = vector[0]
                simplified['vector'] = vector
            
            # Remove None values
            simplified = {k: v for k, v in simplified.items() if v is not None}
            
            return simplified
            
        except Exception as e:
            logger.error(f"Error processing entity {entity.get('name', 'Unknown')}: {e}")
            return None
    
    def bulk_index_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Bulk index documents to Elasticsearch."""
        if not documents:
            return True
            
        try:
            # Prepare bulk request
            bulk_data = []
            for doc in documents:
                # Add index action
                bulk_data.append({
                    "index": {
                        "_index": "sanctions"
                    }
                })
                # Add document
                bulk_data.append(doc)
            
            # Send bulk request
            response = requests.post(
                f"{self.elasticsearch_url}/_bulk",
                data='\n'.join(json.dumps(item) for item in bulk_data) + '\n',
                headers={'Content-Type': 'application/x-ndjson'},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('errors'):
                    logger.error(f"Bulk indexing had errors: {result}")
                    return False
                else:
                    logger.info(f"Successfully indexed {len(documents)} documents")
                    return True
            else:
                logger.error(f"Bulk indexing failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error in bulk indexing: {e}")
            return False
    
    async def load_all_sanctions(self) -> bool:
        """Load all sanctions data to Elasticsearch."""
        try:
            # Load data from files
            entities = self.load_sanctions_data()
            total_entities = len(entities)
            
            logger.info(f"Processing {total_entities} entities in batches of {self.batch_size}...")
            
            success_count = 0
            processed_count = 0
            
            for i in range(0, total_entities, self.batch_size):
                batch_entities = entities[i:i + self.batch_size]
                batch_num = i // self.batch_size + 1
                total_batches = (total_entities + self.batch_size - 1) // self.batch_size
                
                logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch_entities)} entities)")
                
                # Process batch
                batch_documents = []
                for j, entity in enumerate(batch_entities, 1):
                    logger.info(f"  Processing entity {i + j}/{total_entities}: {entity.get('name', 'Unknown')}")
                    
                    processed = await self.process_entity(entity)
                    if processed:
                        batch_documents.append(processed)
                        success_count += 1
                    
                    processed_count += 1
                
                # Index batch
                if batch_documents:
                    if self.bulk_index_documents(batch_documents):
                        logger.info(f"✅ Batch {batch_num} indexed successfully")
                    else:
                        logger.error(f"❌ Batch {batch_num} indexing failed")
                
                # Delay between batches
                if i + self.batch_size < total_entities:
                    logger.info(f"Waiting {self.delay_between_batches}s before next batch...")
                    await asyncio.sleep(self.delay_between_batches)
            
            logger.info(f"✅ Processing complete: {success_count}/{processed_count} entities processed successfully")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error loading sanctions data: {e}")
            return False

async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load all sanctions data to Elasticsearch")
    parser.add_argument("--elasticsearch-url", default="http://95.217.84.234:9200", help="Elasticsearch URL")
    parser.add_argument("--data-path", default="ai-service/src/ai_service/data", help="Path to data files")
    parser.add_argument("--batch-size", type=int, default=100, help="Batch size for processing")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between batches in seconds")
    
    args = parser.parse_args()
    
    print("Payment Vector Testing - Bulk Sanctions Loader")
    print("=" * 50)
    print(f"Elasticsearch URL: {args.elasticsearch_url}")
    print(f"Data path: {args.data_path}")
    print(f"Batch size: {args.batch_size}")
    print(f"Delay between batches: {args.delay}s")
    print()
    
    # Initialize loader
    loader = BulkSanctionsLoader(args.elasticsearch_url, args.data_path)
    loader.batch_size = args.batch_size
    loader.delay_between_batches = args.delay
    
    try:
        # Load all sanctions data
        success = await loader.load_all_sanctions()
        
        if success:
            print("✅ All sanctions data loaded successfully!")
        else:
            print("❌ Failed to load sanctions data")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️  Loading interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
