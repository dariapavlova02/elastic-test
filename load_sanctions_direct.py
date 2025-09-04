#!/usr/bin/env python3
"""
Load sanctions data directly to Elasticsearch.
"""
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import requests

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

class DirectSanctionsLoader:
    """Load sanctions data directly to Elasticsearch."""
    
    def __init__(self, elasticsearch_url: str = "http://95.217.84.234:9200", data_path: str = "ai-service/src/ai_service/data"):
        """Initialize the loader."""
        self.elasticsearch_url = elasticsearch_url.rstrip('/')
        self.data_path = data_path
        self.ai_processor = AIProcessor()
        self.sanctions_loader = SanctionsLoader(data_path=data_path, ai_processor=self.ai_processor)
        
    def load_sanctions_data(self) -> List[Dict[str, Any]]:
        """Load sanctions data from files."""
        logger.info("Loading sanctions data from files...")
        return self.sanctions_loader.get_all_sanctions_entities()
    
    async def process_and_send_entity(self, entity: Dict[str, Any]) -> bool:
        """Process entity with AI and send to Elasticsearch."""
        try:
            # Process with AI
            result = await self.ai_processor.process_sanctions_entity(entity)
            
            if not result['success']:
                logger.error(f"❌ AI processing failed for entity: {result.get('error', 'Unknown error')}")
                return False
            
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
            
            # Send to Elasticsearch
            response = requests.post(
                f"{self.elasticsearch_url}/sanctions/_doc",
                json=simplified,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Successfully loaded entity: {entity.get('name', 'Unknown')}")
                return True
            else:
                logger.error(f"❌ Failed to load entity: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error processing entity {entity.get('name', 'Unknown')}: {e}")
            return False
    
    async def load_sanctions_direct(self, limit: int = None) -> bool:
        """Load sanctions data directly to Elasticsearch."""
        try:
            # Load data from files
            entities = self.load_sanctions_data()
            
            if limit:
                entities = entities[:limit]
                logger.info(f"Limited to {limit} entities for testing")
            
            logger.info(f"Processing {len(entities)} entities...")
            
            success_count = 0
            for i, entity in enumerate(entities, 1):
                logger.info(f"Processing entity {i}/{len(entities)}: {entity.get('name', 'Unknown')}")
                
                if await self.process_and_send_entity(entity):
                    success_count += 1
                
                # Small delay to avoid overwhelming the server
                await asyncio.sleep(0.1)
            
            logger.info(f"✅ Successfully loaded {success_count}/{len(entities)} entities")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"❌ Error loading sanctions data: {e}")
            return False

async def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load sanctions data directly to Elasticsearch")
    parser.add_argument("--elasticsearch-url", default="http://95.217.84.234:9200", help="Elasticsearch URL")
    parser.add_argument("--data-path", default="ai-service/src/ai_service/data", help="Path to data files")
    parser.add_argument("--limit", type=int, help="Limit number of entities to load (for testing)")
    
    args = parser.parse_args()
    
    print("Payment Vector Testing - Direct Sanctions Loader")
    print("=" * 50)
    print(f"Elasticsearch URL: {args.elasticsearch_url}")
    print(f"Data path: {args.data_path}")
    if args.limit:
        print(f"Limit: {args.limit} entities")
    print()
    
    # Initialize loader
    loader = DirectSanctionsLoader(args.elasticsearch_url, args.data_path)
    
    try:
        # Load sanctions data directly
        success = await loader.load_sanctions_direct(args.limit)
        
        if success:
            print("✅ Sanctions data loaded successfully!")
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
