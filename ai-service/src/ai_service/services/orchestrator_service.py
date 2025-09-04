"""
Orchestrator for coordinating all AI system services
"""

import asyncio
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

from ..config import PERFORMANCE_CONFIG
from ..exceptions import (
    ServiceInitializationError,
    ProcessingError,
    CacheError,
    LanguageDetectionError,
    NormalizationError,
    VariantGenerationError,
    EmbeddingError
)
from ..utils import get_logger
from .unicode_service import UnicodeService
from .language_detection_service import LanguageDetectionService
from .normalization_service import NormalizationService
from .variant_generation_service import VariantGenerationService
from .pattern_service import PatternService
from .template_builder import TemplateBuilder
from .embedding_service import EmbeddingService
from .cache_service import CacheService
from .signal_service import SignalService
# DISABLED: Smart filter temporarily disabled
# from .smart_filter.smart_filter_service import SmartFilterService


@dataclass
class ProcessingResult:
    """Text processing result"""
    original_text: str
    normalized_text: str
    language: str
    language_confidence: float
    variants: List[str]
    embeddings: Optional[List] = None
    processing_time: float = 0.0
    success: bool = True
    errors: List[str] = None
    
    def to_dict(self) -> dict:
        """
        Converts the ProcessingResult to a dictionary for JSON serialization.

        This method creates a dictionary representation of the processing
        result that can be easily serialized to JSON format. Useful for
        API responses, logging, or data storage.

        Returns:
            dict: A dictionary containing all the processing result fields
                  in a serializable format.
        """
        return {
            'original_text': self.original_text,
            'normalized_text': self.normalized_text,
            'language': self.language,
            'language_confidence': self.language_confidence,
            'variants': self.variants,
            'embeddings': self.embeddings,
            'processing_time': self.processing_time,
            'success': self.success,
            'errors': self.errors
        }


class OrchestratorService:
    """Orchestrator for coordinating all services"""
    
    def __init__(self, cache_size: Optional[int] = None, default_ttl: Optional[int] = None):
        """
        Initialize orchestrator service
        
        Args:
            cache_size: Cache size (uses config default if None)
            default_ttl: Default TTL in seconds (uses config default if None)
            
        Raises:
            ServiceInitializationError: If service initialization fails
        """
        self.logger = get_logger(__name__)
        
        try:
            # Use configuration defaults if not provided
            cache_size = cache_size or PERFORMANCE_CONFIG.cache_size
            default_ttl = default_ttl or PERFORMANCE_CONFIG.cache_ttl
            
            # Initialize all services
            self.unicode_service = UnicodeService()
            self.language_service = LanguageDetectionService()
            self.normalization_service = NormalizationService()
            self.variant_service = VariantGenerationService()
            self.pattern_service = PatternService()
            self.template_builder = TemplateBuilder()
            self.embedding_service = EmbeddingService()
            self.cache_service = CacheService(max_size=cache_size, default_ttl=default_ttl)
            self.signal_service = SignalService()
            
            # Initialize smart filter with existing services
            # DISABLED: Smart filter temporarily disabled
            # self.smart_filter = SmartFilterService(
            #     language_service=self.language_service,
            #     signal_service=self.signal_service
            # )
            self.smart_filter = None
        except Exception as e:
            self.logger.error(f"Failed to initialize orchestrator services: {e}")
            raise ServiceInitializationError(f"Service initialization failed: {str(e)}")
        
        # Processing statistics
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0,
            'average_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0,
            'smart_filter_skipped': 0,
            'smart_filter_processed': 0
        }
        
        self.logger.info("OrchestratorService initialized with all services")
    
    async def process_text(
        self,
        text: str,
        generate_variants: bool = True,
        generate_embeddings: bool = False,
        cache_result: bool = True,
        force_reprocess: bool = False
    ) -> ProcessingResult:
        """
        Complete text processing through all services
        
        Args:
            text: Input text
            generate_variants: Generate variants
            generate_embeddings: Generate embeddings
            cache_result: Cache result
            force_reprocess: Force reprocessing
            
        Returns:
            ProcessingResult with processing results
        """
        start_time = datetime.now()
        
        try:
            # Check cache
            cache_key = self._generate_cache_key(text, generate_variants, generate_embeddings)
            
            if not force_reprocess and cache_result:
                cached_result = self.cache_service.get(cache_key)
                if cached_result:
                    self.processing_stats['cache_hits'] += 1
                    self.logger.debug(f"Cache hit for text: {text[:50]}...")
                    return cached_result
            
            self.processing_stats['cache_misses'] += 1
            
            # 1. CRITICAL: Language detection BEFORE Unicode normalization!
            # This prevents loss of Cyrillic characters through unidecode
            language_result = self.language_service.detect_language(text)
            language = language_result['language']
            language_confidence = language_result['confidence']
            
            self.logger.info(f"Language detected before normalization: {language} (confidence: {language_confidence:.2f})")
                                                        
            
            # 2. Unicode normalization AFTER language detection
            unicode_result = self.unicode_service.normalize_text(text, aggressive=False)
            normalized_text = unicode_result['normalized']
            
            # 3. Text normalization - EXPLICITLY pass detected language
            norm_result = await self.normalization_service.normalize(
                normalized_text,
                language=language,  # Explicitly pass detected language instead of 'auto'
                preserve_names=True,
                apply_lemmatization=True,
                apply_stemming=False,
                remove_stop_words=False
            )
            
            # Defensive coding: check normalization result
            if norm_result is None:
                self.logger.error(f"Normalization service returned None for text: {normalized_text[:50]}...")
                                                        
                return ProcessingResult(
                    original_text=text,
                    normalized_text=normalized_text,
                    language=language,
                    language_confidence=language_confidence,
                    variants=[],
                    processing_time=(datetime.now() - start_time).total_seconds(),
                    success=False,
                    errors=["Normalization service returned None"]
                )
            
            final_normalized = getattr(norm_result, 'normalized', normalized_text)
            
            # 4. Variant generation (optimized logic)
            variants = []
            if generate_variants:
                if len(final_normalized.strip()) > 2:
                    # Get variants for the entire normalized text ONCE
                    variant_result = self.variant_service.generate_variants(
                        text=final_normalized,
                        language=language,
                        max_variants=50  # Limit total number of variants
                    )
                    if variant_result and 'variants' in variant_result:
                        variants = variant_result['variants']
                    
                    # Remove duplicates and empty strings
                    variants = list(set(v for v in variants if v and len(v.strip()) > 0))
                
                # Fallback if no variants
                if not variants:
                    variants = [final_normalized]
            
            # 6. Generate embeddings (if needed)
            embeddings = None
            if generate_embeddings:
                embedding_result = self.embedding_service.get_embeddings(
                    [final_normalized],
                    normalize=True
                )
                if embedding_result.get('success'):
                    embeddings = embedding_result['embeddings']
            
            # Form result
            processing_time = (datetime.now() - start_time).total_seconds()
            
            result = ProcessingResult(
                original_text=text,
                normalized_text=final_normalized,
                language=language,
                language_confidence=language_confidence,
                variants=variants,
                embeddings=embeddings,
                processing_time=processing_time,
                success=True
            )
            
            # Cache result
            if cache_result:
                self.cache_service.set(cache_key, result, ttl=3600)
            
            # Update statistics
            self._update_stats(processing_time, True)
            
            return result
            
        except Exception as e:
            processing_time = (datetime.now() - start_time).total_seconds()
            self.logger.error(f"Error processing text: {e}")
            
            # Update statistics
            self._update_stats(processing_time, False)
            
            return ProcessingResult(
                original_text=text,
                normalized_text="",
                language="unknown",
                language_confidence=0.0,
                variants=[],
                processing_time=processing_time,
                success=False,
                errors=[str(e)]
            )
    
    async def process_batch(
        self,
        texts: List[str],
        generate_variants: bool = True,
        generate_embeddings: bool = False,
        max_concurrent: int = 10
    ) -> List[ProcessingResult]:
        """
        Batch text processing
        
        Args:
            texts: List of texts
            generate_variants: Generate variants
            generate_embeddings: Generate embeddings
            max_concurrent: Maximum number of concurrent tasks
            
        Returns:
            List of processing results
        """
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_single(text: str) -> ProcessingResult:
            async with semaphore:
                return await self.process_text(
                    text=text,
                    generate_variants=generate_variants,
                    generate_embeddings=generate_embeddings
                )
        
        # Create tasks for all texts
        tasks = [process_single(text) for text in texts]
        
        # Execute tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process errors
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                self.logger.error(f"Error processing text {i}: {result}")
                processed_results.append(ProcessingResult(
                    original_text=texts[i],
                    normalized_text="",
                    language="unknown",
                    language_confidence=0.0,
                    variants=[],
                    processing_time=0.0,
                    success=False,
                    errors=[str(result)]
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def search_similar_names(
        self,
        query: str,
        candidates: List[str],
        threshold: float = 0.7,
        top_k: int = 10,
        use_embeddings: bool = True
    ) -> Dict:
        """
        Search for similar names among candidates
        
        Args:
            query: Search query
            candidates: List of candidates
            threshold: Similarity threshold
            top_k: Number of best results
            use_embeddings: Use embeddings for search
            
        Returns:
            Search results
        """
        try:
            if use_embeddings:
                # Use embeddings for search
                search_result = self.embedding_service.find_similar_texts(
                    query=query,
                    candidates=candidates,
                    threshold=threshold,
                    top_k=top_k
                )
                
                if search_result.get('success'):
                    return {
                        'method': 'embeddings',
                        'query': query,
                        'results': search_result['results'],
                        'total_candidates': search_result['total_candidates'],
                        'threshold': threshold
                    }
            
            # Fallback to simpler search
            variant_result = self.variant_service.find_best_matches(
                query=query,
                candidates=candidates,
                threshold=threshold,
                max_results=top_k
            )
            
            return {
                'method': 'variants',
                'query': query,
                'results': variant_result,
                'total_candidates': len(candidates),
                'threshold': threshold
            }
            
        except Exception as e:
            self.logger.error(f"Error in name search: {e}")
            return {
                'method': 'error',
                'query': query,
                'results': [],
                'error': str(e)
            }
    
    async def analyze_text_complexity(
        self,
        text: str
    ) -> Dict:
        """
        Analyze text complexity
        
        Args:
            text: Input text
            
        Returns:
            Complexity analysis
        """
        try:
            # Unicode complexity
            unicode_result = self.unicode_service.normalize_text(text, aggressive=False)
            unicode_complexity = {
                'confidence': unicode_result['confidence'],
                'changes': unicode_result['changes'],
                'issues': unicode_result.get('issues', [])
            }
            
            # Language complexity
            language_result = self.language_service.detect_language(text)
            language_complexity = {
                'detected_language': language_result['language'],
                'confidence': language_result['confidence'],
                'method': language_result.get('method', 'unknown')
            }
            
            # Name signals
            signal_result = self.signal_service.get_name_signals(text)
            name_complexity = {
                'signal_type': 'name_signal',
                'total_score': signal_result['count'],
                'confidence': signal_result['confidence']
            }
            
            # Overall complexity score
            complexity_score = self._calculate_complexity_score(
                unicode_complexity,
                language_complexity,
                name_complexity
            )
            
            return {
                'text': text,
                'complexity_score': complexity_score,
                'unicode': unicode_complexity,
                'language': language_complexity,
                'names': name_complexity,
                'recommendations': self._generate_complexity_recommendations(complexity_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing text complexity: {e}")
            return {
                'text': text,
                'error': str(e),
                'complexity_score': 0.0
            }
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """
        Retrieves the current processing statistics for the service.

        This includes metrics like total requests, success/failure rates,
        average processing time, and detailed cache statistics.

        Returns:
            Dict[str, Any]: A dictionary containing comprehensive statistics
                            about the service's operation.
        """
        stats = self.processing_stats.copy()
        
        # Add cache statistics
        cache_stats = self.cache_service.get_stats()
        stats['cache'] = cache_stats
        
        # Add service statistics
        stats['services'] = {
            'unicode': 'active',
            'language': 'active',
            'normalization': 'active',
            'variants': 'active',
            'patterns': 'active',
            'templates': 'active',
            'embeddings': 'active'
        }
        
        return stats
    
    def clear_cache(self):
        """
        Clears all cached data from the cache service.

        This method removes all stored processing results and resets
        the cache to its initial state. Useful for freeing memory
        or when cache consistency is required.

        Note:
            This operation is irreversible and will affect all cached data.
        """
        self.cache_service.clear()
        self.logger.info("Cache cleared")
    
    def reset_stats(self):
        """
        Resets all processing statistics to their initial values.

        This method clears all accumulated metrics including total processed
        requests, success/failure counts, timing information, and cache
        performance data. Useful for starting fresh measurements or
        troubleshooting performance issues.

        Note:
            This operation is irreversible and will reset all historical data.
        """
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0.0,
            'average_time': 0.0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.logger.info("Statistics reset")
    
    def _generate_cache_key(
        self,
        text: str,
        generate_variants: bool,
        generate_embeddings: bool
    ) -> str:
        """
        Generates a unique cache key for text processing requests.

        Creates a deterministic hash-based key that uniquely identifies
        a processing request based on the input text and processing options.
        This ensures that identical requests with the same parameters
        will use the same cache entry.

        Args:
            text (str): The input text to be processed.
            generate_variants (bool): Whether to generate text variants.
            generate_embeddings (bool): Whether to generate embeddings.

        Returns:
            str: A unique MD5 hash-based cache key prefixed with 'orchestrator_'.
        """
        import hashlib
        
        key_data = f"{text}_{generate_variants}_{generate_embeddings}"
        return f"orchestrator_{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def _update_stats(self, processing_time: float, success: bool):
        """
        Updates internal processing statistics with new request data.

        This method maintains running totals and calculates averages for
        processing performance metrics. It updates both request counts
        and timing information to provide real-time service performance
        insights.

        Args:
            processing_time (float): The time taken to process the request in seconds.
            success (bool): Whether the request was processed successfully.
        """
        self.processing_stats['total_processed'] += 1
        self.processing_stats['total_time'] += processing_time
        
        if success:
            self.processing_stats['successful'] += 1
        else:
            self.processing_stats['failed'] += 1
        
        # Update average time
        if self.processing_stats['total_processed'] > 0:
            self.processing_stats['average_time'] = (
                self.processing_stats['total_time'] / 
                self.processing_stats['total_processed']
            )
    
    def _calculate_complexity_score(
        self,
        unicode_complexity: Dict,
        language_complexity: Dict,
        name_complexity: Dict
    ) -> float:
        """
        Calculates an overall complexity score for text processing.

        Combines multiple complexity factors into a single normalized score
        that indicates how challenging a text will be to process. The score
        ranges from 0.0 (simple) to 1.0 (very complex).

        Args:
            unicode_complexity (Dict): Unicode normalization complexity metrics.
            language_complexity (Dict): Language detection complexity metrics.
            name_complexity (Dict): Name signal detection complexity metrics.

        Returns:
            float: A normalized complexity score between 0.0 and 1.0,
                   where higher values indicate more complex processing requirements.
        """
        score = 0.0
        
        # Unicode complexity (0-1)
        unicode_score = 1.0 - unicode_complexity['confidence']
        score += unicode_score * 0.3
        
        # Language complexity (0-1)
        language_score = 1.0 - language_complexity['confidence']
        score += language_score * 0.3
        
        # Name complexity (0-1)
        name_score = 1.0 - name_complexity['confidence']
        score += name_score * 0.4
        
        return min(score, 1.0)
    
    def _generate_complexity_recommendations(self, complexity_score: float) -> List[str]:
        """
        Generates processing recommendations based on complexity score.

        Provides actionable advice for handling texts of different complexity
        levels. Recommendations help users understand what to expect and
        suggest appropriate processing strategies.

        Args:
            complexity_score (float): The calculated complexity score (0.0 to 1.0).

        Returns:
            List[str]: A list of recommendation strings providing guidance
                       for processing the text based on its complexity level.
        """
        recommendations = []
        
        if complexity_score < 0.3:
            recommendations.append("Text has low complexity for processing")
        elif complexity_score < 0.6:
            recommendations.append("Text has medium complexity for processing")
            recommendations.append("It is recommended to check Unicode normalization")
        else:
            recommendations.append("Text has high complexity for processing")
            recommendations.append("It is recommended to perform a detailed analysis and manual verification")
            recommendations.append("Possible issues with encoding or language")
        
        return recommendations
    
    async def process_text_with_smart_filter(
        self,
        text: str,
        generate_variants: bool = True,
        use_embeddings: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Process text with smart filter optimization
        
        Args:
            text: Text to process
            generate_variants: Whether to generate variants
            use_embeddings: Whether to generate embeddings
            use_cache: Whether to use cache
            
        Returns:
            Processing result with smart filter information
        """
        start_time = datetime.now()
        
        try:
            # DISABLED: Smart filter is temporarily disabled
            # Just process text normally without smart filter
            self.processing_stats['smart_filter_processed'] += 1
            
            # Use existing process_text method
            result = await self.process_text(
                text=text,
                generate_variants=generate_variants,
                generate_embeddings=use_embeddings,
                cache_result=use_cache
            )
            
            # Add smart filter information to result (disabled)
            if isinstance(result, dict):
                result['smart_filter'] = {
                    'should_process': True,
                    'confidence': 1.0,
                    'reason': "Smart filter disabled - processing all texts",
                    'detected_signals': [],
                    'complexity': 'unknown'
                }
            else:
                # If result is ProcessingResult object
                result.smart_filter = {
                    'should_process': True,
                    'confidence': 1.0,
                    'reason': "Smart filter disabled - processing all texts",
                    'detected_signals': [],
                    'complexity': 'unknown'
                }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in process_text_with_smart_filter: {e}")
            self.processing_stats['failed'] += 1
            
            return {
                'original_text': text,
                'normalized_text': text,
                'language': 'unknown',
                'language_confidence': 0.0,
                'variants': [],
                'embeddings': None,
                'processing_time': (datetime.now() - start_time).total_seconds(),
                'success': False,
                'errors': [str(e)],
                'smart_filter': {
                    'should_process': False,
                    'confidence': 0.0,
                    'reason': f"Error in processing: {str(e)}",
                    'detected_signals': [],
                    'complexity': 'unknown'
                }
            }
    
    def get_smart_filter_stats(self) -> Dict[str, Any]:
        """
        Get smart filter statistics
        DISABLED: Smart filter is temporarily disabled
        
        Returns:
            Dictionary with smart filter statistics (disabled status)
        """
        total_processed = self.processing_stats['total_processed']
        processed = self.processing_stats['smart_filter_processed']
        
        return {
            'total_texts_analyzed': total_processed,
            'skipped_by_filter': 0,  # No texts skipped since filter is disabled
            'processed_fully': processed,
            'efficiency_percentage': 0.0,  # No efficiency since filter is disabled
            'status': 'disabled',
            'message': 'Smart filter is temporarily disabled - all texts are processed',
            'filter_effectiveness': {
                'skipped_ratio': 0.0,
                'processed_ratio': 1.0 if total_processed > 0 else 0.0
            }
        }
