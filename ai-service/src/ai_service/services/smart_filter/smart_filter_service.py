"""
Smart Filter Service

Main service for intelligent pre-filtering.
Determines whether to run full Aho-Corasick search
based on signal analysis in text.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from ...config import SERVICE_CONFIG
from ...exceptions import SmartFilterError, LanguageDetectionError
from ...utils.logging_config import get_logger
from ...data.dicts.smart_filter_patterns import (
    EXCLUSION_PATTERNS, SERVICE_WORDS, CONFIDENCE_THRESHOLDS, DATE_TIME_PATTERNS
)
from .company_detector import CompanyDetector
from .name_detector import NameDetector
from .document_detector import DocumentDetector
from .terrorism_detector import TerrorismDetector
from .confidence_scorer import ConfidenceScorer
from .decision_logic import DecisionLogic, DecisionType, RiskLevel
from ..signal_service import SignalService


@dataclass
class FilterResult:
    """Result of smart filter operation"""
    should_process: bool
    confidence: float
    detected_signals: List[str]
    signal_details: Dict[str, Any]
    processing_recommendation: str
    estimated_complexity: str


class SmartFilterService:
    """Smart pre-filter for determining text relevance"""
    
    def __init__(
        self, 
        language_service: Optional[Any] = None, 
        signal_service: Optional[Any] = None, 
        enable_terrorism_detection: bool = True
    ):
        """
        Initialize smart filter service
        
        Args:
            language_service: Language detection service instance
            signal_service: Signal detection service instance
            enable_terrorism_detection: Enable terrorism detection
            
        Raises:
            SmartFilterError: If service initialization fails
        """
        self.logger = get_logger(__name__)
        
        try:
            # Use existing services
            self.language_service = language_service
            self.signal_service = signal_service
            
            # Initialize base signal service
            self.signal_service = signal_service or SignalService()
            
            # Initialize main decision module
            self.decision_logic = DecisionLogic(enable_terrorism_detection=enable_terrorism_detection)
            
            # Initialize detectors (for backward compatibility)
            self.company_detector = CompanyDetector()
            self.name_detector = NameDetector()
            self.document_detector = DocumentDetector()
            if enable_terrorism_detection:
                self.terrorism_detector = TerrorismDetector()
            else:
                self.terrorism_detector = None
            self.confidence_scorer = ConfidenceScorer()
            
            # Decision thresholds (from dictionary)
            self.thresholds = CONFIDENCE_THRESHOLDS.copy()
            
            # Patterns for quick exclusion (from dictionary)
            self.exclusion_patterns = EXCLUSION_PATTERNS.copy()
            
            # Service word dictionaries for cleaning
            self.service_words = SERVICE_WORDS.copy()
            
            # Date and time patterns
            self.date_time_patterns = DATE_TIME_PATTERNS.copy()
            
            self.logger.info(f"SmartFilterService initialized (terrorism detection: {enable_terrorism_detection})")
        except Exception as e:
            self.logger.error(f"Failed to initialize SmartFilterService: {e}")
            raise SmartFilterError(f"Service initialization failed: {str(e)}")
    
    def should_process_text(self, text: str) -> FilterResult:
        """
        Determines whether to process text with full search
        
        Args:
            text: Text to analyze
            
        Returns:
            FilterResult with recommendation
            
        Raises:
            SmartFilterError: If text processing fails
        """
        if not text or not text.strip():
            return self._create_empty_result()
        
        try:
            # Pre-cleanup of service words
            cleaned_text = self._clean_service_words(text)
            
            # Text normalization
            normalized_text = self._normalize_text(cleaned_text)
            
            # Quick exclusion check
            if self._is_excluded_text(normalized_text):
                return FilterResult(
                    should_process=False,
                    confidence=0.0,
                    detected_signals=[],
                    signal_details={},
                    processing_recommendation="Text excluded from processing (service information only)",
                    estimated_complexity="very_low"
                )
            
            # Date and time check
            if self._is_date_only_text(normalized_text):
                return FilterResult(
                    should_process=False,
                    confidence=0.0,
                    detected_signals=[],
                    signal_details={},
                    processing_recommendation="Text excluded from processing (date/time only)",
                    estimated_complexity="very_low"
                )
            
            # Signal analysis
            company_signals = self.company_detector.detect_company_signals(normalized_text)
            name_signals = self.name_detector.detect_name_signals(normalized_text)
            
            # Combine results
            all_signals = {
                'companies': company_signals,
                'names': name_signals
            }
            
            # Calculate total confidence
            total_confidence = self.confidence_scorer.calculate_confidence(all_signals)
            
            # Determine recommendation
            should_process, recommendation, complexity = self._make_processing_decision(
                total_confidence, all_signals, normalized_text
            )
            
            # Form list of detected signals
            detected_signals = []
            if company_signals['confidence'] > 0:
                detected_signals.append('company')
            if name_signals['confidence'] > 0:
                detected_signals.append('name')
            
            return FilterResult(
                should_process=should_process,
                confidence=total_confidence,
                detected_signals=detected_signals,
                signal_details=all_signals,
                processing_recommendation=recommendation,
                estimated_complexity=complexity
            )
        except Exception as e:
            self.logger.error(f"Error in should_process_text: {e}")
            raise SmartFilterError(f"Text processing failed: {str(e)}")
    
    def analyze_payment_description(self, text: str) -> Dict[str, Any]:
        """
        Analyzes payment description and returns detailed information
        
        Args:
            text: Payment description text
            
        Returns:
            Detailed text analysis
            
        Raises:
            SmartFilterError: If analysis fails
        """
        try:
            result = self.should_process_text(text)
            
            # Additional statistics
            word_count = len(text.split())
            char_count = len(text)
            
            # Language composition analysis
            language_analysis = self._analyze_language_composition(text)
            
            return {
                'filter_result': result,
                'text_statistics': {
                    'word_count': word_count,
                    'char_count': char_count,
                    'average_word_length': char_count / word_count if word_count > 0 else 0
                },
                'language_analysis': language_analysis,
                'processing_time': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error in analyze_payment_description: {e}")
            raise SmartFilterError(f"Payment description analysis failed: {str(e)}")
    
    def _clean_service_words(self, text: str) -> str:
        """Pre-cleanup of service words"""
        if not text or not text.strip():
            return text
        
        # Detect text language
        detected_language = self._detect_language(text)
        
        # Get service words for the language
        service_words = self.service_words.get(detected_language, [])
        
        # Create pattern for removing service words
        if service_words:
            # Pattern for removing service words at beginning and end
            service_pattern = r'^(?:' + '|'.join(re.escape(word) for word in service_words) + r')\s*'
            text = re.sub(service_pattern, '', text, flags=re.IGNORECASE)
            
            service_pattern = r'\s*(?:' + '|'.join(re.escape(word) for word in service_words) + r')$'
            text = re.sub(service_pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def _detect_language(self, text: str) -> str:
        """Detect text language"""
        if self.language_service:
            try:
                result = self.language_service.detect_language(text)
                return result.get('language', 'ukrainian')
            except Exception as e:
                self.logger.warning(f"Language detection error: {e}")
        
        # Fallback - simple character-based detection
        cyrillic_count = len(re.findall(r'[а-яёіїєґ]', text, re.IGNORECASE))
        latin_count = len(re.findall(r'[a-z]', text, re.IGNORECASE))
        
        if cyrillic_count > latin_count:
            return 'ukrainian'  # Default Ukrainian for Cyrillic
        elif latin_count > 0:
            return 'english'
        else:
            return 'ukrainian'
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for analysis"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for some checks
        # (but preserve original for name analysis)
        return text
    
    def make_smart_decision(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make smart decision using all detectors
        
        Args:
            text: Text to analyze
            context: Additional context
            
        Returns:
            Decision result
            
        Raises:
            SmartFilterError: If decision making fails
        """
        try:
            decision_result = self.decision_logic.make_decision(text, context)
            
            # Convert result for API compatibility
            return {
                'should_process': decision_result.decision in [DecisionType.FULL_SEARCH, DecisionType.MANUAL_REVIEW],
                'decision_type': decision_result.decision.value,
                'confidence': decision_result.confidence,
                'risk_level': decision_result.risk_level.value,
                'reasoning': decision_result.reasoning,
                'recommendations': decision_result.recommendations,
                'requires_escalation': decision_result.requires_escalation,
                'processing_time': decision_result.processing_time,
                'detected_signals': decision_result.detected_signals,
                'metadata': decision_result.metadata,
                'blocked': decision_result.decision == DecisionType.BLOCK
            }
        except Exception as e:
            self.logger.error(f"Error in make_smart_decision: {e}")
            raise SmartFilterError(f"Smart decision making failed: {str(e)}")
    
    def get_comprehensive_analysis(self, text: str) -> Dict[str, Any]:
        """
        Получение комплексного анализа текста со всеми детекторами
        
        Args:
            text: Текст для анализа
            
        Returns:
            Комплексный анализ с детальной информацией
        """
        # Базовый анализ через старую систему
        legacy_result = self.should_process_text(text)
        
        # Новый анализ через систему принятия решений
        decision_analysis = self.decision_logic.get_detailed_analysis(text)
        
        # Дополнительные детальные анализы
        name_analysis = self.name_detector.get_detailed_name_analysis(text) if hasattr(self.name_detector, 'get_detailed_name_analysis') else {}
        company_analysis = self.company_detector.get_enhanced_company_analysis(text) if hasattr(self.company_detector, 'get_enhanced_company_analysis') else {}
        
        # Анализ терроризма (если включен)
        terrorism_analysis = {}
        if self.terrorism_detector:
            terrorism_signals = self.terrorism_detector.detect_terrorism_signals(text)
            terrorism_analysis = self.terrorism_detector.get_risk_assessment(terrorism_signals)
        
        return {
            'input_text': text,
            'legacy_analysis': {
                'should_process': legacy_result.should_process,
                'confidence': legacy_result.confidence,
                'detected_signals': legacy_result.detected_signals,
                'processing_recommendation': legacy_result.processing_recommendation,
                'estimated_complexity': legacy_result.estimated_complexity
            },
            'decision_analysis': decision_analysis,
            'detailed_breakdowns': {
                'names': name_analysis,
                'companies': company_analysis,
                'terrorism': terrorism_analysis
            },
            'summary': {
                'final_decision': decision_analysis['decision_result']['decision'],
                'final_confidence': decision_analysis['decision_result']['confidence'],
                'risk_level': decision_analysis['decision_result']['risk_level'],
                'requires_action': decision_analysis['decision_result']['requires_escalation'],
                'processing_recommendation': decision_analysis['decision_result']['reasoning']
            }
        }
    
    def _is_excluded_text(self, text: str) -> bool:
        """Проверка на исключение из обработки"""
        text_lower = text.lower().strip()
        
        for pattern in self.exclusion_patterns:
            if re.match(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _is_date_only_text(self, text: str) -> bool:
        """Проверка, содержит ли текст только даты и время"""
        text_stripped = text.strip()
        
        # Проверка всех паттернов дат и времени
        all_date_patterns = []
        for pattern_group in self.date_time_patterns.values():
            all_date_patterns.extend(pattern_group)
        
        # Проверяем, состоит ли текст только из дат/времени
        for pattern in all_date_patterns:
            if re.fullmatch(pattern, text_stripped, re.IGNORECASE):
                return True
        
        # Дополнительная проверка на относительные даты
        relative_dates = ['сьогодні', 'вчора', 'позавчора', 'завтра', 'післязавтра',
                         'сегодня', 'вчера', 'позавчера', 'завтра', 'послезавтра',
                         'today', 'yesterday', 'tomorrow']
        
        if text_stripped.lower() in relative_dates:
            return True
        
        return False
    
    def _make_processing_decision(
        self, 
        confidence: float, 
        signals: Dict[str, Any], 
        text: str
    ) -> Tuple[bool, str, str]:
        """Принятие решения о необходимости обработки"""
        
        if confidence >= self.thresholds['high']:
            return True, "Высокая уверенность в наличии релевантных сигналов", "high"
        
        elif confidence >= self.thresholds['medium']:
            return True, "Средняя уверенность в наличии релевантных сигналов", "medium"
        
        elif confidence >= self.thresholds['min_processing_threshold']:
            return True, "Низкая уверенность, но есть потенциальные сигналы", "low"
        
        else:
            return False, "Недостаточно сигналов для обработки", "very_low"
    
    def _analyze_language_composition(self, text: str) -> Dict[str, Any]:
        """Анализ языкового состава текста"""
        # Подсчет кириллических символов
        cyrillic_count = len(re.findall(r'[а-яёіїєґ]', text, re.IGNORECASE))
        
        # Подсчет латинских символов
        latin_count = len(re.findall(r'[a-z]', text, re.IGNORECASE))
        
        # Подсчет цифр
        digit_count = len(re.findall(r'\d', text))
        
        # Подсчет спецсимволов
        special_count = len(re.findall(r'[^\w\s]', text))
        
        total_chars = len(text)
        
        return {
            'cyrillic_ratio': cyrillic_count / total_chars if total_chars > 0 else 0,
            'latin_ratio': latin_count / total_chars if total_chars > 0 else 0,
            'digit_ratio': digit_count / total_chars if total_chars > 0 else 0,
            'special_ratio': special_count / total_chars if total_chars > 0 else 0,
            'is_mixed_language': cyrillic_count > 0 and latin_count > 0
        }
    
    def _create_empty_result(self) -> FilterResult:
        """Create empty result"""
        return FilterResult(
            should_process=False,
            confidence=0.0,
            detected_signals=[],
            signal_details={},
            processing_recommendation="Empty text",
            estimated_complexity="none"
        )
