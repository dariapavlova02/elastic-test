"""
AI service processor for payment vector testing.
Uses the existing AI service for text processing and vectorization.
"""
import logging
import sys
import os
from typing import Dict, List, Any, Optional
import re
try:
    from unidecode import unidecode as _unidecode
except Exception:
    _unidecode = None
from pathlib import Path

# Add ai-service to path
ai_service_path = Path(__file__).parent.parent.parent / "ai-service" / "src"
if ai_service_path.exists():
    sys.path.insert(0, str(ai_service_path))
else:
    # Fallback for container environment
    ai_service_path = Path("/app/ai-service/src")
    if ai_service_path.exists():
        sys.path.insert(0, str(ai_service_path))

try:
    from ai_service.services.orchestrator_service import OrchestratorService
    from ai_service.services.embedding_service import EmbeddingService
    from ai_service.services.normalization_service import NormalizationService
    from ai_service.services.language_detection_service import LanguageDetectionService
    from ai_service.exceptions import ProcessingError
except ImportError as e:
    logging.error(f"Failed to import AI service modules: {e}")
    raise

logger = logging.getLogger(__name__)


class AIProcessor:
    """AI service processor for text processing and vectorization."""
    
    def __init__(self):
        """Initialize AI processor."""
        try:
            # Initialize AI services
            logger.info("Initializing OrchestratorService...")
            self.orchestrator = OrchestratorService()
            logger.info("OrchestratorService initialized successfully")
            
            logger.info("Initializing EmbeddingService...")
            self.embedding_service = EmbeddingService()
            logger.info("EmbeddingService initialized successfully")
            
            logger.info("Initializing NormalizationService...")
            self.normalization_service = NormalizationService()
            logger.info("NormalizationService initialized successfully")
            
            logger.info("Initializing LanguageDetectionService...")
            self.language_detection = LanguageDetectionService()
            logger.info("LanguageDetectionService initialized successfully")
            
            logger.info("AI services initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI services: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception details: {str(e)}")
            raise
        # Arabic transliteration (optional)
        try:
            from camel_tools.transliteration.transliterator import Transliterator
            self._ar_translit = Transliterator.factory('ar2lat')
            logger.info("CAMeL Tools Arabic transliterator initialized")
        except Exception:
            self._ar_translit = None
    
    async def process_text(self, text: str, generate_embeddings: bool = True, generate_variants: bool = True) -> Dict[str, Any]:
        """
        Process text using AI service.
        
        Args:
            text: Text to process
            generate_embeddings: Whether to generate vector embeddings
            generate_variants: Whether to generate text variants
            
        Returns:
            Processing result
        """
        try:
            if not text or not text.strip():
                return {
                    "success": False,
                    "error": "Empty text provided",
                    "original_text": text,
                    "normalized_text": "",
                    "language": "unknown",
                    "embeddings": []
                }
            
            # Process text through orchestrator
            result = await self.orchestrator.process_text(
                text=text,
                generate_embeddings=generate_embeddings,
                generate_variants=generate_variants
            )
            
            return {
                "success": result.success,
                "original_text": result.original_text,
                "normalized_text": result.normalized_text,
                "language": result.language,
                "language_confidence": result.language_confidence,
                "variants": result.variants,
                "embeddings": result.embeddings if generate_embeddings else [],
                "processing_time": result.processing_time,
                "errors": result.errors or []
            }
            
        except ProcessingError as e:
            logger.error(f"AI processing error: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "normalized_text": "",
                "language": "unknown",
                "embeddings": []
            }
        except Exception as e:
            logger.error(f"Unexpected error in AI processing: {e}")
            return {
                "success": False,
                "error": str(e),
                "original_text": text,
                "normalized_text": "",
                "language": "unknown",
                "embeddings": []
            }
    
    async def process_payment_metadata(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process payment metadata for vectorization.
        
        Args:
            payment_data: Payment metadata dictionary
            
        Returns:
            Processed payment data with embeddings
        """
        try:
            # Combine relevant text fields
            text_parts = []
            
            # Add sender information
            if payment_data.get('sender'):
                text_parts.append(f"sender: {payment_data['sender']}")
            
            # Add receiver information
            if payment_data.get('receiver'):
                text_parts.append(f"receiver: {payment_data['receiver']}")
            
            # Add description
            if payment_data.get('description'):
                text_parts.append(f"description: {payment_data['description']}")
            
            # Add metadata fields
            if payment_data.get('metadata') and isinstance(payment_data['metadata'], dict):
                metadata = payment_data['metadata']
                if metadata.get('bank_code'):
                    text_parts.append(f"bank_code: {metadata['bank_code']}")
                if metadata.get('transaction_type'):
                    text_parts.append(f"transaction_type: {metadata['transaction_type']}")
                if metadata.get('country'):
                    text_parts.append(f"country: {metadata['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)
            
            if not combined_text.strip():
                return {
                    "success": False,
                    "error": "No text data found in payment metadata",
                    "payment_data": payment_data,
                    "embeddings": []
                }
            
            # Process text
            result = await self.process_text(combined_text, generate_embeddings=True)
            
            # Add processing result to payment data
            payment_data['ai_processing'] = result
            payment_data['vector'] = result.get('embeddings', [])
            
            return {
                "success": result['success'],
                "payment_data": payment_data,
                "embeddings": result.get('embeddings', []),
                "normalized_text": result.get('normalized_text', ''),
                "language": result.get('language', 'unknown')
            }
            
        except Exception as e:
            logger.error(f"Failed to process payment metadata: {e}")
            return {
                "success": False,
                "error": str(e),
                "payment_data": payment_data,
                "embeddings": []
            }
    
    async def process_sanctions_entity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process sanctions entity for vectorization.
        
        Args:
            entity_data: Sanctions entity data
            
        Returns:
            Processed entity data with embeddings
        """
        try:
            # Combine relevant text fields
            text_parts = []
            
            # Add entity name
            if entity_data.get('name'):
                text_parts.append(f"name: {entity_data['name']}")
            
            # Add English name
            if entity_data.get('name_en'):
                text_parts.append(f"name_en: {entity_data['name_en']}")
            
            # Add Russian name
            if entity_data.get('name_ru'):
                text_parts.append(f"name_ru: {entity_data['name_ru']}")
            
            # Add description
            if entity_data.get('description'):
                text_parts.append(f"description: {entity_data['description']}")
            
            # Add address for companies
            if entity_data.get('address'):
                text_parts.append(f"address: {entity_data['address']}")
            
            # Add entity type
            if entity_data.get('entity_type'):
                text_parts.append(f"type: {entity_data['entity_type']}")
            
            # Add country
            if entity_data.get('country'):
                text_parts.append(f"country: {entity_data['country']}")
            
            # Combine all text parts
            combined_text = " ".join(text_parts)

            if not combined_text.strip():
                return {
                    "success": False,
                    "error": "No text data found in sanctions entity",
                    "entity_data": entity_data,
                    "embeddings": []
                }
            
            # Base names to expand
            base_names: List[str] = []
            for key in ('name', 'name_en', 'name_ru'):
                val = entity_data.get(key)
                if val and isinstance(val, str) and val.strip():
                    base_names.append(val.strip())

            # Collect variants and compute embeddings
            variant_texts: List[str] = []
            variants_payload: List[Dict[str, Any]] = []
            primary_vector: List[float] = []
            primary_done = False

            def contains_arabic(s: str) -> bool:
                return any('\u0600' <= ch <= '\u06FF' for ch in s)

            def arabic_to_latin(s: str) -> str:
                # Prefer CAMeL Tools if available, fallback to simple map
                if getattr(self, '_ar_translit', None) is not None:
                    try:
                        return self._ar_translit.transliterate(s)
                    except Exception:
                        pass
                table = {
                    'ا': 'a', 'أ': 'a', 'إ': 'i', 'آ': 'aa', 'ب': 'b', 'ت': 't', 'ث': 'th', 'ج': 'j', 'ح': 'h',
                    'خ': 'kh', 'د': 'd', 'ذ': 'dh', 'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
                    'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q', 'ك': 'k', 'ل': 'l', 'م': 'm',
                    'ن': 'n', 'ه': 'h', 'و': 'w', 'ؤ': 'u', 'ي': 'y', 'ئ': 'i', 'ى': 'a', 'ة': 'a'
                }
                return ''.join(table.get(ch, ch) for ch in s)

            # Pull more aliases if provided by data
            alias_keys = ('aliases', 'aka', 'alt_names', 'other_names')
            for k in alias_keys:
                val = entity_data.get(k)
                if isinstance(val, list):
                    for s in val:
                        if isinstance(s, str) and s.strip():
                            base_names.append(s.strip())
                elif isinstance(val, str) and val.strip():
                    # Split by comma/semicolon
                    for s in re.split(r'[;,]', val):
                        if s.strip():
                            base_names.append(s.strip())

            for nm in base_names:
                try:
                    res = await self.process_text(nm, generate_embeddings=False, generate_variants=True)
                    if not res.get('success'):
                        continue
                    norm = res.get('normalized_text') or nm
                    lang = res.get('language', 'unknown')
                    # Keep normalized first
                    if norm not in variant_texts:
                        variant_texts.append(norm)
                        variants_payload.append({'text': norm, 'lang': lang, 'weight': 1.0})
                    # Add limited variants (top K)
                    for v in (res.get('variants') or [])[:10]:
                        if v and v not in variant_texts:
                            variant_texts.append(v)
                            variants_payload.append({'text': v, 'lang': lang, 'weight': 0.8})
                    # Arabic transliteration (index-time), if applicable
                    if contains_arabic(nm):
                        ar_lat = arabic_to_latin(nm)
                        if ar_lat and ar_lat not in variant_texts:
                            variant_texts.append(ar_lat)
                            variants_payload.append({'text': ar_lat, 'lang': 'ar-Latn', 'weight': 0.7})
                    # Cyrillic -> Latin transliteration for RU/UK variants to help cross-script matching
                    if _unidecode is not None and (re.search(r"[\u0400-\u04FF]", norm) or re.search(r"[\u0400-\u04FF]", nm)):
                        lat = _unidecode(norm)
                        if lat and lat not in variant_texts:
                            variant_texts.append(lat)
                            variants_payload.append({'text': lat, 'lang': f'{lang}-Latn', 'weight': 0.6})
                except Exception as _:
                    continue

            # Deduplicate hard
            variant_texts = list(dict.fromkeys([t for t in variant_texts if isinstance(t, str)]))
            if not variant_texts:
                # Fallback to combined text
                variant_texts = [combined_text]
                variants_payload = [{'text': combined_text, 'lang': 'unknown', 'weight': 1.0}]

            # Compute embeddings for all collected variants
            try:
                emb_res = self.embedding_service.get_embeddings(variant_texts)
                if emb_res.get('success'):
                    embs = emb_res.get('embeddings', [])
                else:
                    embs = []
            except Exception:
                embs = []

            # Attach vectors back to payload
            if embs and len(embs) == len(variants_payload):
                for i, emb in enumerate(embs):
                    variants_payload[i]['vector'] = emb
                    if not primary_done:
                        primary_vector = emb
                        primary_done = True
            else:
                # No vectors, leave empty
                for vp in variants_payload:
                    vp['vector'] = []

            # Detect dominant language for the entity (best-effort)
            try:
                lang_det = self.language_detection.detect_language(entity_data.get('name') or combined_text)
                lang_guess = lang_det.get('language', 'unknown')
            except Exception:
                lang_guess = 'unknown'

            # Add processing result to entity data
            entity_data['ai_processing'] = {
                'normalized_texts': variant_texts[:1],
                'total_variants': len(variants_payload),
                'language': lang_guess
            }
            entity_data['variants'] = variants_payload
            entity_data['vector'] = primary_vector
            
            return {
                "success": True,
                "entity_data": entity_data,
                "embeddings": entity_data.get('vector', []),
                "normalized_text": (variant_texts[0] if variant_texts else (entity_data.get('name') or combined_text)),
                "language": lang_guess
            }
            
        except Exception as e:
            logger.error(f"Failed to process sanctions entity: {e}")
            return {
                "success": False,
                "error": str(e),
                "entity_data": entity_data,
                "embeddings": []
            }
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of vector embeddings
        """
        try:
            result = self.embedding_service.get_embeddings(texts)
            if result['success']:
                return result['embeddings']
            else:
                logger.error(f"Failed to get embeddings: {result.get('error', 'Unknown error')}")
                return []
        except Exception as e:
            logger.error(f"Failed to get embeddings: {e}")
            return []
    
    def get_service_info(self) -> Dict[str, Any]:
        """Get information about AI services."""
        try:
            return {
                "orchestrator_available": self.orchestrator is not None,
                "embedding_service_available": self.embedding_service is not None,
                "normalization_service_available": self.normalization_service is not None,
                "language_detection_available": self.language_detection is not None,
                "supported_models": self.embedding_service.get_supported_models() if self.embedding_service else {}
            }
        except Exception as e:
            logger.error(f"Failed to get service info: {e}")
            return {"error": str(e)}
