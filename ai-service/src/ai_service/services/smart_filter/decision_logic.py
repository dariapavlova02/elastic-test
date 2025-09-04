"""
Decision Logic Module

Модуль логики принятия решений для умного фильтра.
Объединяет результаты всех детекторов сигналов и принимает решение
о необходимости полного поиска по Ахо-Корасику.

Реализует блок "Логика принятия решений" из диаграммы системы.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

from ...utils.logging_config import get_logger
from .name_detector import NameDetector
from .company_detector import CompanyDetector
from .document_detector import DocumentDetector
from .terrorism_detector import TerrorismDetector
from .confidence_scorer import ConfidenceScorer


class DecisionType(Enum):
    """Типы решений"""
    ALLOW = "allow"
    BLOCK = "block"
    FULL_SEARCH = "full_search"
    MANUAL_REVIEW = "manual_review"
    PRIORITY_REVIEW = "priority_review"


class RiskLevel(Enum):
    """Уровни риска"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class DecisionResult:
    """Результат принятия решения"""
    decision: DecisionType
    confidence: float
    risk_level: RiskLevel
    reasoning: str
    detected_signals: Dict[str, Any]
    recommendations: List[str]
    processing_time: float
    requires_escalation: bool
    metadata: Dict[str, Any]


class DecisionLogic:
    """
    Модуль логики принятия решений
    
    Анализирует сигналы от всех детекторов и принимает решение:
    - Разрешить без дополнительной проверки
    - Запустить полный поиск по Ахо-Корасику  
    - Заблокировать (для опасных сигналов)
    - Отправить на ручную проверку
    """
    
    def __init__(self, enable_terrorism_detection: bool = True):
        """
        Инициализация модуля принятия решений
        
        Args:
            enable_terrorism_detection: Включить детектор терроризма
        """
        self.logger = get_logger(__name__)
        
        # Инициализация детекторов
        self.name_detector = NameDetector()
        self.company_detector = CompanyDetector()
        self.document_detector = DocumentDetector()
        self.terrorism_detector = TerrorismDetector() if enable_terrorism_detection else None
        self.confidence_scorer = ConfidenceScorer()
        
        # Простые языковые паттерны для оптимизации (украинский, русский, английский)
        self.language_patterns = {
            'ukrainian': {
                'chars': r'[іїєґІЇЄҐ]',  # Уникальные украинские буквы
                'words': ['тов', 'інн', 'єдрпоу', 'київ', 'вул', 'буд'],
                'weight': 1.2  # Приоритет для украинского
            },
            'russian': {
                'chars': r'[ыэъёЫЭЪЁ]',  # Уникальные русские буквы  
                'words': ['ооо', 'зао', 'инн', 'огрн', 'москва', 'ул', 'дом'],
                'weight': 1.1  # Приоритет для русского
            },
            'english': {
                'chars': r'[a-zA-Z]',  # Латиница
                'words': ['llc', 'inc', 'corp', 'bank', 'street', 'avenue'],
                'weight': 1.0  # Стандартный приоритет
            }
        }
        
        # Пороги для принятия решений
        self.decision_thresholds = {
            'terrorism_block': 0.8,      # Блокировать при подозрении на терроризм
            'terrorism_review': 0.5,     # Отправить на проверку
            'full_search_high': 0.7,     # Запустить полный поиск (высокая уверенность)
            'full_search_medium': 0.5,   # Запустить полный поиск (средняя уверенность)
            'manual_review': 0.3,        # Отправить на ручную проверку
            'allow_threshold': 0.2       # Разрешить без проверки (очень низкая уверенность)
        }
        
        # Веса для различных типов сигналов в принятии решений
        self.signal_weights = {
            'terrorism': 1.0,      # Максимальный приоритет
            'documents': 0.8,      # Высокий приоритет (ИНН, документы)
            'names': 0.7,          # Высокий приоритет (имена людей)
            'companies': 0.6,      # Средний приоритет (компании)
        }
        
        # Паттерны исключений (не требуют проверки)
        self.exclusion_patterns = [
            r'^\d+$',  # Только цифры
            r'^[^\w\s]+$',  # Только спецсимволы
            r'^(оплата|платеж|перевод)$',  # Общие термины
        ]
        
        self.logger.info(f"DecisionLogic initialized (terrorism detection: {enable_terrorism_detection})")
    
    def make_decision(self, text: str, context: Optional[Dict[str, Any]] = None) -> DecisionResult:
        """
        Принятие решения на основе анализа всех сигналов
        
        Args:
            text: Текст для анализа
            context: Дополнительный контекст (источник, тип операции и т.д.)
            
        Returns:
            Результат принятия решения
        """
        import time
        start_time = time.time()
        
        if not text or not text.strip():
            return self._create_allow_decision("Пустой текст", start_time)
        
        # Предварительная проверка на исключения
        if self._is_excluded_text(text):
            return self._create_allow_decision("Текст исключен по паттернам", start_time)
        
        # Простое определение языка
        detected_language, language_weight = self._detect_language_simple(text)
        self.logger.debug(f"Определен язык: {detected_language} (вес: {language_weight:.2f})")
        
        # Сбор сигналов от всех детекторов с языковой оптимизацией
        all_signals = self._collect_all_signals_optimized(text, detected_language, language_weight)
        
        # Анализ терроризма (высший приоритет)
        if self.terrorism_detector:
            terrorism_decision = self._analyze_terrorism_signals(all_signals, text, start_time)
            if terrorism_decision:
                return terrorism_decision
        
        # Анализ остальных сигналов
        decision_result = self._analyze_regular_signals(all_signals, text, context, start_time)
        
        self.logger.debug(f"Decision made: {decision_result.decision.value} with confidence {decision_result.confidence}")
        
        return decision_result
    
    def _collect_all_signals(self, text: str) -> Dict[str, Any]:
        """Сбор сигналов от всех детекторов"""
        signals = {}
        
        try:
            # Сигналы имен
            signals['names'] = self.name_detector.detect_name_signals(text)
        except Exception as e:
            self.logger.error(f"Error in name detection: {e}")
            signals['names'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы компаний
            signals['companies'] = self.company_detector.detect_company_signals(text)
        except Exception as e:
            self.logger.error(f"Error in company detection: {e}")
            signals['companies'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы документов
            signals['documents'] = self.document_detector.detect_document_signals(text)
        except Exception as e:
            self.logger.error(f"Error in document detection: {e}")
            signals['documents'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы терроризма
            if self.terrorism_detector:
                signals['terrorism'] = self.terrorism_detector.detect_terrorism_signals(text)
            else:
                signals['terrorism'] = {'confidence': 0.0, 'risk_level': 'very_low', 'signals': []}
        except Exception as e:
            self.logger.error(f"Error in terrorism detection: {e}")
            signals['terrorism'] = {'confidence': 0.0, 'risk_level': 'very_low', 'signals': []}
        
        return signals
    
    def _detect_language_simple(self, text: str) -> Tuple[str, float]:
        """Простое определение основного языка текста"""
        text_lower = text.lower()
        scores = {}
        
        for lang_name, lang_data in self.language_patterns.items():
            score = 0.0
            
            # Проверка уникальных символов
            if re.search(lang_data['chars'], text):
                score += 0.5
            
            # Проверка характерных слов
            word_matches = sum(1 for word in lang_data['words'] if word in text_lower)
            if word_matches > 0:
                score += min(word_matches * 0.2, 0.5)
            
            scores[lang_name] = score * lang_data['weight']
        
        if scores:
            detected_lang = max(scores.keys(), key=lambda k: scores[k])
            weight = self.language_patterns[detected_lang]['weight']
            return detected_lang, weight
        
        return 'english', 1.0  # По умолчанию
    
    def _collect_all_signals_optimized(self, text: str, detected_language: str, language_weight: float) -> Dict[str, Any]:
        """Сбор сигналов от всех детекторов с языковой оптимизацией"""
        signals = {}
        
        self.logger.debug(f"Оптимизация для языка: {detected_language}, вес: {language_weight:.2f}")
        
        try:
            # Сигналы имен (с языковой оптимизацией)
            signals['names'] = self.name_detector.detect_name_signals(text)
            if signals['names']['confidence'] > 0:
                # Бонус для славянских языков
                if detected_language in ['ukrainian', 'russian']:
                    slavic_patterns = ['-енко', '-ко', '-ов', '-ев', '-ич', '-ович', '-овна', '-евна']
                    if any(pattern in text.lower() for pattern in slavic_patterns):
                        signals['names']['confidence'] = min(signals['names']['confidence'] * language_weight, 1.0)
                        self.logger.debug(f"Применен бонус {language_weight:.1f} для {detected_language} имен")
                        
        except Exception as e:
            self.logger.error(f"Error in optimized name detection: {e}")
            signals['names'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы компаний (с языковой оптимизацией)
            signals['companies'] = self.company_detector.detect_company_signals(text)
            if signals['companies']['confidence'] > 0:
                # Языковые бонусы для организационно-правовых форм
                if detected_language == 'ukrainian' and any(form in text.lower() for form in ['тов', 'прат', 'товариство']):
                    signals['companies']['confidence'] = min(signals['companies']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен украинский бонус для компаний")
                elif detected_language == 'russian' and any(form in text.lower() for form in ['ооо', 'зао', 'оао', 'общество']):
                    signals['companies']['confidence'] = min(signals['companies']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен русский бонус для компаний")
                elif detected_language == 'english' and any(form in text.lower() for form in ['llc', 'inc', 'corp', 'company']):
                    signals['companies']['confidence'] = min(signals['companies']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен английский бонус для компаний")
                        
        except Exception as e:
            self.logger.error(f"Error in optimized company detection: {e}")
            signals['companies'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы документов (с языковой оптимизацией)
            signals['documents'] = self.document_detector.detect_document_signals(text)
            if signals['documents']['confidence'] > 0:
                # Языковые бонусы для документов
                if detected_language == 'ukrainian' and any(doc in text for doc in ['інн', 'єдрпоу', 'мфо']):
                    signals['documents']['confidence'] = min(signals['documents']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен украинский бонус для документов")
                elif detected_language == 'russian' and any(doc in text.lower() for doc in ['инн', 'огрн', 'кпп', 'бик']):
                    signals['documents']['confidence'] = min(signals['documents']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен русский бонус для документов")
                elif detected_language == 'english' and any(doc in text.upper() for doc in ['TIN', 'EIN', 'SWIFT']):
                    signals['documents']['confidence'] = min(signals['documents']['confidence'] * language_weight, 1.0)
                    self.logger.debug(f"Применен английский бонус для документов")
                        
        except Exception as e:
            self.logger.error(f"Error in optimized document detection: {e}")
            signals['documents'] = {'confidence': 0.0, 'signals': []}
        
        try:
            # Сигналы терроризма (без языковой корректировки - универсальные)
            if self.terrorism_detector:
                signals['terrorism'] = self.terrorism_detector.detect_terrorism_signals(text)
            else:
                signals['terrorism'] = {'confidence': 0.0, 'risk_level': 'very_low', 'signals': []}
        except Exception as e:
            self.logger.error(f"Error in terrorism detection: {e}")
            signals['terrorism'] = {'confidence': 0.0, 'risk_level': 'very_low', 'signals': []}
        
        # Добавляем информацию о языке в результат
        for signal_type in signals:
            if isinstance(signals[signal_type], dict):
                signals[signal_type]['language_info'] = {
                    'detected_language': detected_language,
                    'weight': language_weight
                }
        
        return signals
    
    def _analyze_terrorism_signals(self, signals: Dict[str, Any], text: str, start_time: float) -> Optional[DecisionResult]:
        """Анализ сигналов терроризма (высший приоритет)"""
        terrorism_signals = signals.get('terrorism', {})
        terrorism_confidence = terrorism_signals.get('confidence', 0.0)
        terrorism_risk = terrorism_signals.get('risk_level', 'very_low')
        
        if terrorism_confidence >= self.decision_thresholds['terrorism_block']:
            return DecisionResult(
                decision=DecisionType.BLOCK,
                confidence=terrorism_confidence,
                risk_level=RiskLevel.CRITICAL,
                reasoning=f"Обнаружены критические индикаторы терроризма (confidence: {terrorism_confidence:.2f})",
                detected_signals=signals,
                recommendations=[
                    "Немедленно заблокировать транзакцию",
                    "Уведомить службы безопасности",
                    "Провести расследование",
                    "Зафиксировать все детали для отчета"
                ],
                processing_time=time.time() - start_time,
                requires_escalation=True,
                metadata={'terrorism_risk': terrorism_risk, 'blocked_reason': 'terrorism_indicators'}
            )
        
        elif terrorism_confidence >= self.decision_thresholds['terrorism_review']:
            return DecisionResult(
                decision=DecisionType.PRIORITY_REVIEW,
                confidence=terrorism_confidence,
                risk_level=RiskLevel.HIGH,
                reasoning=f"Обнаружены подозрительные индикаторы терроризма (confidence: {terrorism_confidence:.2f})",
                detected_signals=signals,
                recommendations=[
                    "Приостановить обработку",
                    "Срочная ручная проверка",
                    "Уведомить службу безопасности",
                    "Провести дополнительный анализ"
                ],
                processing_time=time.time() - start_time,
                requires_escalation=True,
                metadata={'terrorism_risk': terrorism_risk, 'review_priority': 'high'}
            )
        
        return None  # Продолжить обычный анализ
    
    def _analyze_regular_signals(self, signals: Dict[str, Any], text: str, 
                                context: Optional[Dict[str, Any]], start_time: float) -> DecisionResult:
        """Анализ обычных сигналов (имена, компании, документы)"""
        
        # Вычисление общей уверенности с весами
        weighted_confidence = 0.0
        total_weight = 0.0
        signal_details = {}
        
        for signal_type, signal_data in signals.items():
            if signal_type == 'terrorism':
                continue  # Уже обработано
            
            confidence = signal_data.get('confidence', 0.0)
            weight = self.signal_weights.get(signal_type, 0.5)
            
            weighted_confidence += confidence * weight
            total_weight += weight
            
            signal_details[signal_type] = {
                'confidence': confidence,
                'weight': weight,
                'signal_count': signal_data.get('signal_count', 0),
                'high_confidence_signals': len(signal_data.get('high_confidence_signals', []))
            }
        
        # Нормализация общей уверенности
        if total_weight > 0:
            normalized_confidence = weighted_confidence / total_weight
        else:
            normalized_confidence = 0.0
        
        # Определение уровня риска
        risk_level = self._determine_risk_level(normalized_confidence, signals)
        
        # Принятие решения на основе уверенности и контекста
        decision, reasoning, recommendations = self._make_regular_decision(
            normalized_confidence, signals, text, context
        )
        
        return DecisionResult(
            decision=decision,
            confidence=normalized_confidence,
            risk_level=risk_level,
            reasoning=reasoning,
            detected_signals=signals,
            recommendations=recommendations,
            processing_time=time.time() - start_time,
            requires_escalation=decision in [DecisionType.MANUAL_REVIEW, DecisionType.PRIORITY_REVIEW],
            metadata={'signal_details': signal_details, 'context': context or {}}
        )
    
    def _make_regular_decision(self, confidence: float, signals: Dict[str, Any], 
                             text: str, context: Optional[Dict[str, Any]]) -> Tuple[DecisionType, str, List[str]]:
        """Принятие обычного решения на основе уверенности"""
        
        # Проверка на высокую уверенность - запуск полного поиска
        if confidence >= self.decision_thresholds['full_search_high']:
            return (
                DecisionType.FULL_SEARCH,
                f"Высокая уверенность в наличии релевантных сигналов (confidence: {confidence:.2f})",
                [
                    "Запустить полный поиск по Ахо-Корасику",
                    "Проанализировать все найденные совпадения",
                    "Применить дополнительные фильтры"
                ]
            )
        
        # Проверка на среднюю уверенность - запуск полного поиска
        elif confidence >= self.decision_thresholds['full_search_medium']:
            return (
                DecisionType.FULL_SEARCH,
                f"Средняя уверенность в наличии релевантных сигналов (confidence: {confidence:.2f})",
                [
                    "Запустить полный поиск по Ахо-Корасику",
                    "Проанализировать найденные совпадения",
                    "Рассмотреть возможность дополнительной проверки"
                ]
            )
        
        # Проверка на низкую уверенность - ручная проверка
        elif confidence >= self.decision_thresholds['manual_review']:
            return (
                DecisionType.MANUAL_REVIEW,
                f"Низкая уверенность, но есть потенциальные сигналы (confidence: {confidence:.2f})",
                [
                    "Отправить на ручную проверку",
                    "Проанализировать контекст операции",
                    "Рассмотреть историю клиента",
                    "Принять решение о дальнейших действиях"
                ]
            )
        
        # Очень низкая уверенность - разрешить
        else:
            return (
                DecisionType.ALLOW,
                f"Очень низкая уверенность в наличии релевантных сигналов (confidence: {confidence:.2f})",
                [
                    "Разрешить операцию без дополнительных проверок",
                    "Записать в лог для статистики"
                ]
            )
    
    def _determine_risk_level(self, confidence: float, signals: Dict[str, Any]) -> RiskLevel:
        """Определение уровня риска"""
        # Учитываем терроризм
        terrorism_signals = signals.get('terrorism', {})
        terrorism_risk = terrorism_signals.get('risk_level', 'very_low')
        
        if terrorism_risk in ['high', 'critical']:
            return RiskLevel.CRITICAL
        elif terrorism_risk == 'medium':
            return RiskLevel.HIGH
        
        # Обычная логика на основе уверенности
        if confidence >= 0.8:
            return RiskLevel.HIGH
        elif confidence >= 0.6:
            return RiskLevel.MEDIUM
        elif confidence >= 0.3:
            return RiskLevel.LOW
        else:
            return RiskLevel.VERY_LOW
    
    def _is_excluded_text(self, text: str) -> bool:
        """Проверка на исключения"""
        text_stripped = text.strip().lower()
        
        for pattern in self.exclusion_patterns:
            if re.match(pattern, text_stripped, re.IGNORECASE):
                return True
        
        return False
    
    def _create_allow_decision(self, reason: str, start_time: float) -> DecisionResult:
        """Создание решения разрешения"""
        return DecisionResult(
            decision=DecisionType.ALLOW,
            confidence=0.0,
            risk_level=RiskLevel.VERY_LOW,
            reasoning=reason,
            detected_signals={},
            recommendations=["Разрешить без дополнительных проверок"],
            processing_time=time.time() - start_time,
            requires_escalation=False,
            metadata={}
        )
    
    def get_decision_statistics(self, decisions: List[DecisionResult]) -> Dict[str, Any]:
        """Получение статистики по решениям"""
        if not decisions:
            return {}
        
        total = len(decisions)
        decision_counts = {}
        risk_counts = {}
        avg_confidence = 0.0
        avg_processing_time = 0.0
        escalation_count = 0
        
        for decision in decisions:
            # Подсчет решений
            decision_type = decision.decision.value
            decision_counts[decision_type] = decision_counts.get(decision_type, 0) + 1
            
            # Подсчет уровней риска
            risk_level = decision.risk_level.value
            risk_counts[risk_level] = risk_counts.get(risk_level, 0) + 1
            
            # Суммирование для средних значений
            avg_confidence += decision.confidence
            avg_processing_time += decision.processing_time
            
            if decision.requires_escalation:
                escalation_count += 1
        
        return {
            'total_decisions': total,
            'decision_distribution': {k: v/total for k, v in decision_counts.items()},
            'risk_distribution': {k: v/total for k, v in risk_counts.items()},
            'average_confidence': avg_confidence / total,
            'average_processing_time': avg_processing_time / total,
            'escalation_rate': escalation_count / total,
            'decision_counts': decision_counts,
            'risk_counts': risk_counts
        }
    
    def update_thresholds(self, new_thresholds: Dict[str, float]) -> None:
        """Обновление порогов принятия решений"""
        for key, value in new_thresholds.items():
            if key in self.decision_thresholds:
                old_value = self.decision_thresholds[key]
                self.decision_thresholds[key] = value
                self.logger.info(f"Updated threshold {key}: {old_value} -> {value}")
            else:
                self.logger.warning(f"Unknown threshold key: {key}")
    
    def get_detailed_analysis(self, text: str) -> Dict[str, Any]:
        """Получение детального анализа для диагностики"""
        decision_result = self.make_decision(text)
        
        return {
            'input_text': text,
            'decision_result': {
                'decision': decision_result.decision.value,
                'confidence': decision_result.confidence,
                'risk_level': decision_result.risk_level.value,
                'reasoning': decision_result.reasoning,
                'requires_escalation': decision_result.requires_escalation,
                'processing_time': decision_result.processing_time
            },
            'detected_signals': decision_result.detected_signals,
            'recommendations': decision_result.recommendations,
            'metadata': decision_result.metadata,
            'thresholds_used': self.decision_thresholds,
            'signal_weights_used': self.signal_weights
        }