"""
Sanctions data loader for payment vector testing.
"""
import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

from ..ai_integration import AIProcessor, DataNormalizer

logger = logging.getLogger(__name__)


class SanctionsLoader:
    """Loads and processes sanctions data from ai-service."""
    
    def __init__(self, data_path: Optional[str] = None, ai_processor: Optional[AIProcessor] = None):
        """
        Initialize sanctions loader.
        
        Args:
            data_path: Path to sanctions data directory
            ai_processor: AI processor for text processing
        """
        if data_path is None:
            # Default path to ai-service data
            current_dir = Path(__file__).parent
            data_path = current_dir / ".." / ".." / "ai-service" / "src" / "ai_service" / "data"
        
        self.data_path = Path(data_path)
        self.ai_processor = ai_processor or AIProcessor()
        self.data_normalizer = DataNormalizer(self.ai_processor)
        self.sanctions_persons = []
        self.sanctions_companies = []
        self.terrorism_list = []
        
        self._load_all_data()
    
    def _load_all_data(self) -> None:
        """Load all sanctions data."""
        try:
            self._load_sanctions_persons()
            self._load_sanctions_companies()
            self._load_terrorism_list()
            logger.info(f"Loaded {len(self.sanctions_persons)} persons, "
                       f"{len(self.sanctions_companies)} companies, "
                       f"{len(self.terrorism_list)} terrorism entities")
        except Exception as e:
            logger.error(f"Failed to load sanctions data: {e}")
            raise
    
    def _load_sanctions_persons(self) -> None:
        """Load sanctioned persons data."""
        try:
            file_path = self.data_path / "sanctioned_persons.json"
            if not file_path.exists():
                logger.warning(f"Sanctions persons file not found: {file_path}")
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.sanctions_persons = json.load(f)
            
            logger.info(f"Loaded {len(self.sanctions_persons)} sanctioned persons")
        except Exception as e:
            logger.error(f"Failed to load sanctions persons: {e}")
            raise
    
    def _load_sanctions_companies(self) -> None:
        """Load sanctioned companies data."""
        try:
            file_path = self.data_path / "sanctioned_companies.json"
            if not file_path.exists():
                logger.warning(f"Sanctions companies file not found: {file_path}")
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.sanctions_companies = json.load(f)
            
            logger.info(f"Loaded {len(self.sanctions_companies)} sanctioned companies")
        except Exception as e:
            logger.error(f"Failed to load sanctions companies: {e}")
            raise
    
    def _load_terrorism_list(self) -> None:
        """Load terrorism blacklist data."""
        try:
            file_path = self.data_path / "terrorism_black_list.json"
            if not file_path.exists():
                logger.warning(f"Terrorism blacklist file not found: {file_path}")
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.terrorism_list = json.load(f)
            
            logger.info(f"Loaded {len(self.terrorism_list)} terrorism entities")
        except Exception as e:
            logger.error(f"Failed to load terrorism list: {e}")
            raise
    
    def get_sanctions_persons(self) -> List[Dict[str, Any]]:
        """Get list of sanctioned persons."""
        return self.sanctions_persons.copy()
    
    def get_sanctions_companies(self) -> List[Dict[str, Any]]:
        """Get list of sanctioned companies."""
        return self.sanctions_companies.copy()
    
    def get_terrorism_list(self) -> List[Dict[str, Any]]:
        """Get terrorism blacklist."""
        return self.terrorism_list.copy()
    
    def get_all_sanctions_entities(self) -> List[Dict[str, Any]]:
        """Get all sanctions entities combined."""
        all_entities = []
        
        # Add persons
        for person in self.sanctions_persons:
            entity = {
                "id": f"person_{person.get('id', '')}",
                "name": person.get('name', ''),
                "name_en": person.get('name_en', ''),
                "name_ru": person.get('name_ru', ''),
                "entity_type": "person",
                "birthdate": person.get('birthdate', ''),
                "itn": person.get('itn', ''),
                "status": person.get('status', 1),
                "source": "sanctions_persons"
            }
            all_entities.append(entity)
        
        # Add companies
        for company in self.sanctions_companies:
            entity = {
                "id": f"company_{company.get('id', '')}",
                "name": company.get('name', ''),
                "entity_type": "company",
                "tax_number": company.get('tax_number', ''),
                "reg_number": company.get('reg_number', ''),
                "address": company.get('address', ''),
                "status": company.get('status', 1),
                "source": "sanctions_companies"
            }
            all_entities.append(entity)
        
        # Add terrorism entities
        for terror in self.terrorism_list:
            entity = {
                "id": f"terror_{terror.get('id', '')}",
                "name": terror.get('name', ''),
                "entity_type": "terrorism",
                "description": terror.get('description', ''),
                "status": terror.get('status', 1),
                "source": "terrorism_list"
            }
            all_entities.append(entity)
        
        return all_entities
    
    def search_entity_by_name(self, name: str, entity_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for entity by name.
        
        Args:
            name: Name to search for
            entity_type: Optional entity type filter
            
        Returns:
            List of matching entities
        """
        results = []
        name_lower = name.lower()
        
        for entity in self.get_all_sanctions_entities():
            if entity_type and entity.get('entity_type') != entity_type:
                continue
            
            # Check main name
            if name_lower in entity.get('name', '').lower():
                results.append(entity)
                continue
            
            # Check English name
            if name_lower in entity.get('name_en', '').lower():
                results.append(entity)
                continue
            
            # Check Russian name
            if name_lower in entity.get('name_ru', '').lower():
                results.append(entity)
                continue
        
        return results
    
    def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """
        Get entity by ID.
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Entity data or None if not found
        """
        for entity in self.get_all_sanctions_entities():
            if entity.get('id') == entity_id:
                return entity
        return None
    
    def get_processed_sanctions_entities(self) -> List[Dict[str, Any]]:
        """
        Get all sanctions entities processed with AI.
        
        Returns:
            List of processed sanctions entities with vectors
        """
        try:
            # Get all entities
            entities = self.get_all_sanctions_entities()
            
            # Process each entity with AI
            processed_entities = []
            for entity in entities:
                try:
                    # Process entity with AI
                    result = self.ai_processor.process_sanctions_entity(entity)
                    if result['success']:
                        processed_entities.append(result['entity_data'])
                    else:
                        logger.warning(f"Failed to process entity {entity.get('id', 'unknown')}: {result.get('error', 'Unknown error')}")
                        # Add entity without AI processing
                        entity['vector'] = []
                        processed_entities.append(entity)
                except Exception as e:
                    logger.error(f"Error processing entity {entity.get('id', 'unknown')}: {e}")
                    # Add entity without AI processing
                    entity['vector'] = []
                    processed_entities.append(entity)
            
            logger.info(f"Processed {len(processed_entities)} sanctions entities with AI")
            return processed_entities
            
        except Exception as e:
            logger.error(f"Failed to get processed sanctions entities: {e}")
            return self.get_all_sanctions_entities()
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded sanctions data."""
        return {
            "total_persons": len(self.sanctions_persons),
            "total_companies": len(self.sanctions_companies),
            "total_terrorism": len(self.terrorism_list),
            "total_entities": len(self.get_all_sanctions_entities()),
            "data_path": str(self.data_path),
            "ai_processor_available": self.ai_processor is not None
        }
