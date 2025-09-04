"""
Terrorism Indicators Signal Detector

Детектор для определения сигналов терроризма в тексте.
Использует характерные короткие паттерны для быстрого определения
потенциальных индикаторов террористической активности.

ВАЖНО: Этот модуль предназначен ТОЛЬКО для защитных целей и 
противодействия терроризму в финансовых системах.
"""

import re
from typing import Dict, List, Any, Set
from dataclasses import dataclass

from ...utils.logging_config import get_logger


@dataclass
class TerrorismSignal:
    """Сигнал обнаружения индикатора терроризма"""
    signal_type: str
    confidence: float
    matches: List[str]
    position: int
    context: str
    risk_level: str


class TerrorismDetector:
    """Детектор индикаторов терроризма для защитных целей"""
    
    def __init__(self):
        """Инициализация детектора"""
        self.logger = get_logger(__name__)
        
        # Паттерны для финансирования терроризма (общие индикаторы)
        self.financing_patterns = [
            # Подозрительные термины для переводов
            r'\b(?:джихад|jihad|муджахид|mujahid|шахид|shahid|мученик|martyr)\b',
            r'\b(?:халифат|caliphate|emirate|эмират|имарат)\b',
            r'\b(?:фонд|fund|foundation|благотвор|charity|زكاة|закят|zakat)\s*(?:помощи|помощь|support|aid|relief)\b',
            
            # Кодовые слова (общие паттерны)
            r'\b(?:операция|operation|миссия|mission|проект|project)\s+[А-ЯІЇЄҐA-Z][а-яіїєґa-z]+\b',
            r'\b(?:братья|brothers|сестры|sisters|товарищи|comrades)\s+(?:по|in|from)\s+[а-яіїєґa-z]+\b',
            
            # Подозрительные географические регионы (общие)
            r'\b(?:syria|сирия|iraq|ирак|afghanistan|афганистан|somalia|сомали)\b',
            r'\b(?:tribal|племенн|region|регион|border|граница|frontier)\s+(?:area|зона|territory|территория)\b',
        ]
        
        # Паттерны для оружия и взрывчатых веществ (оборонительные)
        self.weapons_patterns = [
            r'\b(?:explosive|взрывчат|bomb|бомба|ied|взрывн|device|устройство)\b',
            r'\b(?:ammunition|боеприпас|weapons|оружие|arms|вооружение)\b',
            r'\b(?:training|тренировк|preparation|подготовк|equipment|оборудование)\b',
            r'\b(?:chemical|химическ|biological|биологическ|nuclear|ядерн|radioactive|радиоактивн)\b',
        ]
        
        # Паттерны для подозрительных организаций (защитные списки)
        self.organization_patterns = [
            # Общие паттерны для подозрительных структур
            r'\b(?:cell|ячейка|network|сеть|group|группа|wing|крыло|brigade|бригада)\b',
            r'\b(?:movement|движение|front|фронт|liberation|освобождение|resistance|сопротивление)\b',
            r'\b(?:foundation|фонд|charity|благотвор|relief|помощь|aid|поддержка)\s+(?:international|международн|global|глобальн)\b',
        ]
        
        # Паттерны для подозрительной активности
        self.activity_patterns = [
            # Финансовые операции
            r'\b(?:cash|наличные|courier|курьер|transfer|перевод|hawala|хавала|informal|неформальн)\s+(?:service|сервис|system|система|network|сеть)\b',
            r'\b(?:multiple|множественн|frequent|частые|unusual|необычн|suspicious|подозрительн)\s+(?:transactions|операции|transfers|переводы|payments|платежи)\b',
            
            # Коммуникации
            r'\b(?:encrypted|зашифрован|secure|защищен|anonymous|анонимн|coded|кодирован)\s+(?:message|сообщение|communication|связь|channel|канал)\b',
            r'\b(?:meeting|встреча|gathering|собрание|assembly|ассамблея|conference|конференция)\s+(?:secret|секретн|private|частн|closed|закрыт)\b',
            
            # Поездки и перемещения
            r'\b(?:travel|поездка|journey|путешествие|trip|поход|visit|визит)\s+(?:to|в|from|из|via|через)\s+(?:conflict|конфликт|war|война|unstable|нестабильн)\b',
            r'\b(?:border|граница|crossing|пересечение|entry|въезд|exit|выезд)\s+(?:point|пункт|control|контроль)\b',
        ]
        
        # Исключения (слова, которые могут ложно срабатывать)
        self.exclusion_patterns = [
            r'\b(?:игра|game|фильм|movie|книга|book|история|story|новости|news)\b',
            r'\b(?:university|университет|school|школа|education|образование|academic|академическ)\b',
            r'\b(?:historical|историческ|documentary|документальн|research|исследование)\b',
            r'\b(?:legitimate|законн|official|официальн|registered|зарегистрирован)\b',
        ]
        
        # Весовые коэффициенты для разных типов индикаторов
        self.pattern_weights = {
            'financing': 0.8,
            'weapons': 0.9,
            'organization': 0.7,
            'activity': 0.6
        }
        
        # Пороги риска
        self.risk_thresholds = {
            'high': 0.8,
            'medium': 0.5,
            'low': 0.3
        }
        
        self.logger.info("TerrorismDetector initialized for defensive purposes")
    
    def detect_terrorism_signals(self, text: str) -> Dict[str, Any]:
        """
        Обнаружение индикаторов терроризма в тексте (защитные цели)
        
        Args:
            text: Текст для анализа
            
        Returns:
            Результаты обнаружения индикаторов терроризма
        """
        if not text or not text.strip():
            return self._create_empty_result()
        
        # Предварительная проверка на исключения
        if self._is_excluded_content(text):
            return self._create_empty_result()
        
        signals = []
        total_confidence = 0.0
        max_risk_level = 'low'
        
        # 1. Поиск финансовых индикаторов
        financing_signals = self._detect_financing_patterns(text)
        if financing_signals['confidence'] > 0:
            signals.append(financing_signals)
            total_confidence += financing_signals['confidence'] * self.pattern_weights['financing']
            if financing_signals['risk_level'] == 'high':
                max_risk_level = 'high'
            elif financing_signals['risk_level'] == 'medium' and max_risk_level != 'high':
                max_risk_level = 'medium'
        
        # 2. Поиск индикаторов оружия/взрывчатых веществ
        weapons_signals = self._detect_weapons_patterns(text)
        if weapons_signals['confidence'] > 0:
            signals.append(weapons_signals)
            total_confidence += weapons_signals['confidence'] * self.pattern_weights['weapons']
            if weapons_signals['risk_level'] == 'high':
                max_risk_level = 'high'
            elif weapons_signals['risk_level'] == 'medium' and max_risk_level != 'high':
                max_risk_level = 'medium'
        
        # 3. Поиск организационных индикаторов
        org_signals = self._detect_organization_patterns(text)
        if org_signals['confidence'] > 0:
            signals.append(org_signals)
            total_confidence += org_signals['confidence'] * self.pattern_weights['organization']
            if org_signals['risk_level'] == 'high':
                max_risk_level = 'high'
            elif org_signals['risk_level'] == 'medium' and max_risk_level != 'high':
                max_risk_level = 'medium'
        
        # 4. Поиск подозрительной активности
        activity_signals = self._detect_activity_patterns(text)
        if activity_signals['confidence'] > 0:
            signals.append(activity_signals)
            total_confidence += activity_signals['confidence'] * self.pattern_weights['activity']
            if activity_signals['risk_level'] == 'high':
                max_risk_level = 'high'
            elif activity_signals['risk_level'] == 'medium' and max_risk_level != 'high':
                max_risk_level = 'medium'
        
        # Нормализация общей уверенности
        normalized_confidence = min(total_confidence, 1.0)
        
        # Определение общего уровня риска
        if normalized_confidence >= self.risk_thresholds['high']:
            overall_risk = 'high'
        elif normalized_confidence >= self.risk_thresholds['medium']:
            overall_risk = 'medium'
        elif normalized_confidence >= self.risk_thresholds['low']:
            overall_risk = 'low'
        else:
            overall_risk = 'very_low'
        
        return {
            'confidence': normalized_confidence,
            'risk_level': overall_risk,
            'signals': signals,
            'signal_count': len(signals),
            'high_risk_signals': [s for s in signals if s.get('risk_level') == 'high'],
            'detected_indicators': self._extract_detected_indicators(signals),
            'text_length': len(text),
            'analysis_complete': True,
            'requires_manual_review': normalized_confidence >= self.risk_thresholds['medium']
        }
    
    def _detect_financing_patterns(self, text: str) -> Dict[str, Any]:
        """Обнаружение паттернов финансирования терроризма"""
        matches = []
        
        for pattern in self.financing_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE | re.UNICODE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.3, 0.9) if matches else 0.0
        risk_level = self._determine_risk_level(confidence)
        
        return {
            'signal_type': 'financing_terrorism',
            'confidence': confidence,
            'risk_level': risk_level,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_weapons_patterns(self, text: str) -> Dict[str, Any]:
        """Обнаружение паттернов оружия и взрывчатых веществ"""
        matches = []
        
        for pattern in self.weapons_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE | re.UNICODE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.4, 0.95) if matches else 0.0
        risk_level = self._determine_risk_level(confidence)
        
        return {
            'signal_type': 'weapons_explosives',
            'confidence': confidence,
            'risk_level': risk_level,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_organization_patterns(self, text: str) -> Dict[str, Any]:
        """Обнаружение паттернов подозрительных организаций"""
        matches = []
        
        for pattern in self.organization_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE | re.UNICODE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.25, 0.8) if matches else 0.0
        risk_level = self._determine_risk_level(confidence)
        
        return {
            'signal_type': 'suspicious_organizations',
            'confidence': confidence,
            'risk_level': risk_level,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_activity_patterns(self, text: str) -> Dict[str, Any]:
        """Обнаружение паттернов подозрительной активности"""
        matches = []
        
        for pattern in self.activity_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE | re.UNICODE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.2, 0.7) if matches else 0.0
        risk_level = self._determine_risk_level(confidence)
        
        return {
            'signal_type': 'suspicious_activity',
            'confidence': confidence,
            'risk_level': risk_level,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _is_excluded_content(self, text: str) -> bool:
        """Проверка на исключения (ложные срабатывания)"""
        text_lower = text.lower()
        
        for pattern in self.exclusion_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _determine_risk_level(self, confidence: float) -> str:
        """Определение уровня риска на основе уверенности"""
        if confidence >= self.risk_thresholds['high']:
            return 'high'
        elif confidence >= self.risk_thresholds['medium']:
            return 'medium'
        elif confidence >= self.risk_thresholds['low']:
            return 'low'
        else:
            return 'very_low'
    
    def _extract_detected_indicators(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Извлечение всех обнаруженных индикаторов"""
        all_indicators = []
        for signal in signals:
            if 'matches' in signal:
                all_indicators.extend(signal['matches'])
        return list(set(all_indicators))
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Создание пустого результата"""
        return {
            'confidence': 0.0,
            'risk_level': 'very_low',
            'signals': [],
            'signal_count': 0,
            'high_risk_signals': [],
            'detected_indicators': [],
            'text_length': 0,
            'analysis_complete': True,
            'requires_manual_review': False
        }
    
    def get_risk_assessment(self, signals_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Получение детальной оценки риска
        
        Args:
            signals_result: Результат анализа сигналов
            
        Returns:
            Детальная оценка риска
        """
        risk_level = signals_result.get('risk_level', 'very_low')
        confidence = signals_result.get('confidence', 0.0)
        
        recommendations = {
            'high': {
                'action': 'IMMEDIATE_REVIEW_REQUIRED',
                'description': 'Высокий риск - требуется немедленная проверка',
                'escalation': True,
                'block_transaction': True
            },
            'medium': {
                'action': 'MANUAL_REVIEW_RECOMMENDED',
                'description': 'Средний риск - рекомендуется ручная проверка',
                'escalation': True,
                'block_transaction': False
            },
            'low': {
                'action': 'MONITOR',
                'description': 'Низкий риск - требуется мониторинг',
                'escalation': False,
                'block_transaction': False
            },
            'very_low': {
                'action': 'ALLOW',
                'description': 'Очень низкий риск - можно разрешить',
                'escalation': False,
                'block_transaction': False
            }
        }
        
        recommendation = recommendations.get(risk_level, recommendations['very_low'])
        
        return {
            'risk_level': risk_level,
            'confidence': confidence,
            'recommendation': recommendation,
            'signals_detected': signals_result.get('signal_count', 0),
            'high_risk_signals': len(signals_result.get('high_risk_signals', [])),
            'requires_escalation': recommendation['escalation'],
            'suggested_action': recommendation['action'],
            'description': recommendation['description']
        }