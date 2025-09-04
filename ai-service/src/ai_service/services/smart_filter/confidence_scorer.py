"""
Confidence Scorer

Система оценки уверенности для умного фильтра.
Объединяет результаты различных детекторов и вычисляет общую уверенность
в необходимости обработки текста.
"""

import math
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass

from ...utils.logging_config import get_logger
from ...data.dicts.smart_filter_patterns import SIGNAL_WEIGHTS, CONFIDENCE_THRESHOLDS


@dataclass
class ScoringWeights:
    """Веса для различных типов сигналов"""
    company_keywords: float = 0.3
    company_legal_entities: float = 0.4
    company_business_types: float = 0.3
    company_addresses: float = 0.2
    company_registration: float = 0.5
    company_capitalized: float = 0.1
    
    name_full_names: float = 0.6
    name_initials: float = 0.5
    name_single_names: float = 0.3
    name_payment_context: float = 0.4
    name_phonetic: float = 0.2
    
    # Общие веса
    company_weight: float = 0.6
    name_weight: float = 0.4


class ConfidenceScorer:
    """Система оценки уверенности"""
    
    def __init__(self):
        """Инициализация системы оценки"""
        self.logger = get_logger(__name__)
        
        # Веса для различных типов сигналов (из словаря)
        self.weights = ScoringWeights(
            company_keywords=SIGNAL_WEIGHTS['company_keywords'],
            company_legal_entities=SIGNAL_WEIGHTS['company_legal_entities'],
            company_business_types=SIGNAL_WEIGHTS['company_business_types'],
            company_addresses=SIGNAL_WEIGHTS['company_addresses'],
            company_registration=SIGNAL_WEIGHTS['company_registration'],
            company_capitalized=SIGNAL_WEIGHTS['company_capitalized'],
            name_full_names=SIGNAL_WEIGHTS['name_full_names'],
            name_initials=SIGNAL_WEIGHTS['name_initials'],
            name_single_names=SIGNAL_WEIGHTS['name_single_names'],
            name_payment_context=SIGNAL_WEIGHTS['name_payment_context'],
            name_phonetic=SIGNAL_WEIGHTS['name_phonetic'],
            company_weight=SIGNAL_WEIGHTS['company_weight'],
            name_weight=SIGNAL_WEIGHTS['name_weight']
        )
        
        # Пороги для различных уровней уверенности (из словаря)
        self.thresholds = CONFIDENCE_THRESHOLDS.copy()
        
        # Коэффициенты для нормализации
        self.normalization_factors = {
            'company': 1.0,
            'name': 1.0,
            'combined': 1.2  # Бонус за комбинацию сигналов
        }
        
        self.logger.info("ConfidenceScorer initialized")
    
    def calculate_confidence(self, signals: Dict[str, Any]) -> float:
        """
        Вычисление общей уверенности на основе всех сигналов
        
        Args:
            signals: Словарь с результатами всех детекторов
            
        Returns:
            Общая уверенность (0.0 - 1.0)
        """
        if not signals:
            return 0.0
        
        # Вычисление уверенности для компаний
        company_confidence = self._calculate_company_confidence(signals.get('companies', {}))
        
        # Вычисление уверенности для имен
        name_confidence = self._calculate_name_confidence(signals.get('names', {}))
        
        # Объединение результатов
        combined_confidence = self._combine_confidences(company_confidence, name_confidence)
        
        # Применение нормализации
        normalized_confidence = self._normalize_confidence(combined_confidence, signals)
        
        return min(normalized_confidence, 1.0)
    
    def _calculate_company_confidence(self, company_signals: Dict[str, Any]) -> float:
        """Вычисление уверенности для сигналов компаний"""
        if not company_signals or not company_signals.get('signals'):
            return 0.0
        
        total_confidence = 0.0
        signal_count = 0
        
        for signal in company_signals['signals']:
            signal_type = signal.get('signal_type', '')
            confidence = signal.get('confidence', 0.0)
            count = signal.get('count', 0)
            
            # Применение весов в зависимости от типа сигнала
            weight = self._get_company_signal_weight(signal_type)
            weighted_confidence = confidence * weight
            
            # Бонус за количество совпадений
            count_bonus = min(count * 0.1, 0.3)
            
            total_confidence += weighted_confidence + count_bonus
            signal_count += 1
        
        # Нормализация по количеству сигналов
        if signal_count > 0:
            avg_confidence = total_confidence / signal_count
            # Применение общего веса для компаний
            return avg_confidence * self.weights.company_weight
        
        return 0.0
    
    def _calculate_name_confidence(self, name_signals: Dict[str, Any]) -> float:
        """Вычисление уверенности для сигналов имен"""
        if not name_signals or not name_signals.get('signals'):
            return 0.0
        
        total_confidence = 0.0
        signal_count = 0
        
        for signal in name_signals['signals']:
            signal_type = signal.get('signal_type', '')
            confidence = signal.get('confidence', 0.0)
            count = signal.get('count', 0)
            
            # Применение весов в зависимости от типа сигнала
            weight = self._get_name_signal_weight(signal_type)
            weighted_confidence = confidence * weight
            
            # Бонус за количество совпадений
            count_bonus = min(count * 0.1, 0.3)
            
            total_confidence += weighted_confidence + count_bonus
            signal_count += 1
        
        # Нормализация по количеству сигналов
        if signal_count > 0:
            avg_confidence = total_confidence / signal_count
            # Применение общего веса для имен
            return avg_confidence * self.weights.name_weight
        
        return 0.0
    
    def _combine_confidences(self, company_confidence: float, name_confidence: float) -> float:
        """Объединение уверенности для компаний и имен"""
        # Если есть оба типа сигналов, даем бонус
        if company_confidence > 0 and name_confidence > 0:
            # Используем максимум + бонус за комбинацию
            max_confidence = max(company_confidence, name_confidence)
            combination_bonus = min(company_confidence, name_confidence) * 0.3
            return min(max_confidence + combination_bonus, 1.0)
        
        # Если есть только один тип сигналов
        return max(company_confidence, name_confidence)
    
    def _normalize_confidence(self, confidence: float, signals: Dict[str, Any]) -> float:
        """Нормализация уверенности с учетом контекста"""
        if confidence <= 0:
            return 0.0
        
        # Базовая нормализация
        normalized = confidence
        
        # Бонус за высокое качество сигналов
        high_quality_bonus = self._calculate_high_quality_bonus(signals)
        normalized += high_quality_bonus
        
        # Штраф за низкое качество текста
        quality_penalty = self._calculate_quality_penalty(signals)
        normalized -= quality_penalty
        
        # Применение логарифмической нормализации для сглаживания
        if normalized > 0.5:
            # Для высоких значений используем квадратный корень
            normalized = math.sqrt(normalized)
        else:
            # Для низких значений используем квадрат
            normalized = normalized ** 2
        
        return max(0.0, min(normalized, 1.0))
    
    def _get_company_signal_weight(self, signal_type: str) -> float:
        """Получение веса для сигнала компании"""
        weights_map = {
            'keywords': self.weights.company_keywords,
            'legal_entities': self.weights.company_legal_entities,
            'business_types': self.weights.company_business_types,
            'addresses': self.weights.company_addresses,
            'registration_numbers': self.weights.company_registration,
            'capitalized_names': self.weights.company_capitalized
        }
        return weights_map.get(signal_type, 0.1)
    
    def _get_name_signal_weight(self, signal_type: str) -> float:
        """Получение веса для сигнала имени"""
        weights_map = {
            'full_names': self.weights.name_full_names,
            'initials': self.weights.name_initials,
            'single_names': self.weights.name_single_names,
            'payment_context': self.weights.name_payment_context,
            'phonetic_patterns': self.weights.name_phonetic
        }
        return weights_map.get(signal_type, 0.1)
    
    def _calculate_high_quality_bonus(self, signals: Dict[str, Any]) -> float:
        """Вычисление бонуса за высокое качество сигналов"""
        bonus = 0.0
        
        # Бонус за высокую уверенность в сигналах
        for signal_type, signal_data in signals.items():
            if isinstance(signal_data, dict) and 'high_confidence_signals' in signal_data:
                high_conf_count = len(signal_data['high_confidence_signals'])
                if high_conf_count > 0:
                    bonus += min(high_conf_count * 0.05, 0.2)
        
        return bonus
    
    def _calculate_quality_penalty(self, signals: Dict[str, Any]) -> float:
        """Вычисление штрафа за низкое качество текста"""
        penalty = 0.0
        
        # Штраф за очень короткие тексты
        for signal_type, signal_data in signals.items():
            if isinstance(signal_data, dict) and 'text_length' in signal_data:
                text_length = signal_data['text_length']
                if text_length < 10:
                    penalty += 0.3
                elif text_length < 20:
                    penalty += 0.1
        
        return penalty
    
    def get_confidence_level(self, confidence: float) -> str:
        """Получение уровня уверенности"""
        if confidence >= self.thresholds['very_high']:
            return 'very_high'
        elif confidence >= self.thresholds['high']:
            return 'high'
        elif confidence >= self.thresholds['medium']:
            return 'medium'
        elif confidence >= self.thresholds['low']:
            return 'low'
        else:
            return 'very_low'
    
    def get_processing_recommendation(self, confidence: float, signals: Dict[str, Any]) -> str:
        """Получение рекомендации по обработке"""
        level = self.get_confidence_level(confidence)
        
        recommendations = {
            'very_high': "Очень высокая уверенность - обязательно обработать",
            'high': "Высокая уверенность - рекомендуется обработать",
            'medium': "Средняя уверенность - можно обработать",
            'low': "Низкая уверенность - обработка не рекомендуется",
            'very_low': "Очень низкая уверенность - не обрабатывать"
        }
        
        base_recommendation = recommendations.get(level, "Неопределенная рекомендация")
        
        # Дополнительные рекомендации на основе типов сигналов
        signal_types = []
        for signal_type, signal_data in signals.items():
            if isinstance(signal_data, dict) and signal_data.get('confidence', 0) > 0:
                signal_types.append(signal_type)
        
        if signal_types:
            base_recommendation += f" (обнаружены сигналы: {', '.join(signal_types)})"
        
        return base_recommendation
    
    def get_detailed_analysis(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """Получение детального анализа уверенности"""
        company_confidence = self._calculate_company_confidence(signals.get('companies', {}))
        name_confidence = self._calculate_name_confidence(signals.get('names', {}))
        combined_confidence = self.combine_confidences(company_confidence, name_confidence)
        normalized_confidence = self._normalize_confidence(combined_confidence, signals)
        
        return {
            'company_confidence': company_confidence,
            'name_confidence': name_confidence,
            'combined_confidence': combined_confidence,
            'normalized_confidence': normalized_confidence,
            'confidence_level': self.get_confidence_level(normalized_confidence),
            'processing_recommendation': self.get_processing_recommendation(normalized_confidence, signals),
            'high_quality_bonus': self._calculate_high_quality_bonus(signals),
            'quality_penalty': self._calculate_quality_penalty(signals)
        }
