#!/usr/bin/env python3
"""
Load sanctions data via API instead of direct Elasticsearch connection.
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

class APISanctionsLoader:
    """Load sanctions data via API."""
    
    def __init__(self, api_url: str = "http://95.217.84.234", data_path: str = "ai-service/src/ai_service/data"):
        """Initialize the loader."""
        self.api_url = api_url.rstrip('/')
        self.data_path = data_path
        self.ai_processor = AIProcessor()
        self.sanctions_loader = SanctionsLoader(data_path=data_path, ai_processor=self.ai_processor)
        
    def load_sanctions_data(self) -> List[Dict[str, Any]]:
        """Load sanctions data from files."""
        logger.info("Loading sanctions data from files...")
        return self.sanctions_loader.get_all_sanctions_entities()
    
    async def process_and_send_entity(self, entity: Dict[str, Any]) -> bool:
        """Process entity with AI and send to API."""
        try:
            # Process with AI
            result = await self.ai_processor.process_sanctions_entity(entity)
            
            if not result['success']:
                logger.error(f"❌ AI processing failed for entity: {result.get('error', 'Unknown error')}")
                return False
            
            processed = result['entity_data']
            
            # Debug: print the processed data structure
            logger.info(f"Processed data keys: {list(processed.keys())}")
            if 'vector' in processed:
                logger.info(f"Vector type: {type(processed['vector'])}, length: {len(processed['vector']) if isinstance(processed['vector'], list) else 'not a list'}")
                
                # Fix vector format - flatten if it's nested
                if isinstance(processed['vector'], list) and len(processed['vector']) == 1 and isinstance(processed['vector'][0], list):
                    processed['vector'] = processed['vector'][0]
                    logger.info(f"Flattened vector, new length: {len(processed['vector'])}")
            
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
                'source': processed.get('source'),
                'vector': processed.get('vector'),
                'variants': processed.get('variants', [])
            }
            
            # Remove None values
            simplified = {k: v for k, v in simplified.items() if v is not None}
            
            # Send parent entity to API
            response = requests.post(
                f"{self.api_url}/index",
                json={
                    "index": "sanctions",
                    "document": simplified
                },
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Successfully loaded entity: {entity.get('name', 'Unknown')}")
                # Also send variants to companion index
                parent_id = simplified.get('id')
                variants = processed.get('variants', [])
                ok_variants = True
                for v in variants:
                    try:
                        vdoc = {
                            'parent_id': parent_id,
                            'text': v.get('text'),
                            'lang': v.get('lang'),
                            'weight': v.get('weight'),
                            'vector': v.get('vector')
                        }
                        vdoc = {k: v for k, v in vdoc.items() if v is not None}
                        vresp = requests.post(
                            f"{self.api_url}/index",
                            json={"index": "sanctions_variants", "document": vdoc},
                            timeout=30
                        )
                        if vresp.status_code != 200:
                            ok_variants = False
                            logger.warning(f"Variant index failed: {vresp.status_code} {vresp.text}")
                    except Exception as ve:
                        ok_variants = False
                        logger.warning(f"Variant index error: {ve}")
                # Also index into parent-child sanctions_pc
                try:
                    # Parent entity with join field
                    parent_pc = {
                        'name': processed.get('name'),
                        'name_en': processed.get('name_en'),
                        'name_ru': processed.get('name_ru'),
                        'entity_type': processed.get('entity_type'),
                        'source': processed.get('source'),
                        'vector': processed.get('vector'),
                        'doc_rel': { 'name': 'entity' }
                    }
                    pc_parent_resp = requests.post(
                        f"{self.api_url}/index",
                        json={
                            "index": "sanctions_pc",
                            "document": parent_pc,
                            "doc_id": parent_id,
                            "routing": parent_id
                        },
                        timeout=30
                    )
                    if pc_parent_resp.status_code != 200:
                        logger.warning(f"PC parent index failed: {pc_parent_resp.status_code} {pc_parent_resp.text}")
                    # Child variants
                    for v in variants:
                        vdoc = {
                            'text': v.get('text'),
                            'lang': v.get('lang'),
                            'weight': v.get('weight'),
                            'vector': v.get('vector'),
                            'doc_rel': { 'name': 'variant', 'parent': parent_id }
                        }
                        pc_child_resp = requests.post(
                            f"{self.api_url}/index",
                            json={
                                "index": "sanctions_pc",
                                "document": vdoc,
                                "routing": parent_id
                            },
                            timeout=30
                        )
                        if pc_child_resp.status_code != 200:
                            logger.warning(f"PC child index failed: {pc_child_resp.status_code} {pc_child_resp.text}")
                except Exception as pce:
                    logger.warning(f"PC indexing error: {pce}")

                return ok_variants
            else:
                logger.error(f"❌ Failed to load entity: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error processing entity {entity.get('name', 'Unknown')}: {e}")
            return False
    
    async def load_sanctions_via_api(self, limit: int = None) -> bool:
        """Load sanctions data via API."""
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
    
    parser = argparse.ArgumentParser(description="Load sanctions data via API")
    parser.add_argument("--api-url", default="http://95.217.84.234", help="API URL")
    parser.add_argument("--data-path", default="ai-service/src/ai_service/data", help="Path to data files")
    parser.add_argument("--limit", type=int, help="Limit number of entities to load (for testing)")
    
    args = parser.parse_args()
    
    print("Payment Vector Testing - API Sanctions Loader")
    print("=" * 50)
    print(f"API URL: {args.api_url}")
    print(f"Data path: {args.data_path}")
    if args.limit:
        print(f"Limit: {args.limit} entities")
    print()
    
    # Initialize loader
    loader = APISanctionsLoader(args.api_url, args.data_path)
    
    try:
        # Load sanctions data via API
        success = await loader.load_sanctions_via_api(args.limit)
        
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
