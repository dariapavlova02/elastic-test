"""
Company Detector

Детектор для определения сигналов компаний и организаций в тексте.
Использует лингвистические паттерны и ключевые слова для быстрого определения
потенциальных названий компаний.
"""

import re
from typing import Dict, List, Any, Set
from dataclasses import dataclass

from ...utils.logging_config import get_logger
from ...data.dicts.smart_filter_patterns import (
    COMPANY_KEYWORDS, COMPANY_PATTERNS, ADDRESS_PATTERNS, 
    REGISTRATION_PATTERNS, SIGNAL_WEIGHTS
)


@dataclass
class CompanySignal:
    """Сигнал обнаружения компании"""
    signal_type: str
    confidence: float
    matches: List[str]
    position: int
    context: str


class CompanyDetector:
    """Детектор компаний и организаций"""
    
    def __init__(self):
        """Инициализация детектора"""
        self.logger = get_logger(__name__)
        
        # Ключевые слова для определения компаний (из словаря)
        self.company_keywords = COMPANY_KEYWORDS.copy()
        
        # Паттерны для определения компаний (из словаря)
        self.company_patterns = COMPANY_PATTERNS.copy()
        
        # Паттерны для адресов и контактной информации (из словаря)
        self.address_patterns = ADDRESS_PATTERNS.copy()
        
        # Паттерны для регистрационных номеров (из словаря)
        self.registration_patterns = REGISTRATION_PATTERNS.copy()
        
        # Расширенные банковские термины
        self.banking_terms = {
            'ukrainian': [
                'банк', 'банківська', 'банківський', 'банківське', 'кредитний', 'кредитна', 'кредитне',
                'фінансовий', 'фінансова', 'фінансове', 'інвестиційний', 'інвестиційна', 'інвестиційне',
                'страховий', 'страхова', 'страхове', 'лізинговий', 'лізингова', 'лізингове',
                'факторинговий', 'факторингова', 'факторингове', 'мікрофінанс', 'мікрокредит',
                'платіжний', 'платіжна', 'платіжне', 'розрахунковий', 'розрахункова', 'розрахункове',
                'депозитний', 'депозитна', 'депозитне', 'валютний', 'валютна', 'валютне',
                'біржовий', 'біржова', 'біржове', 'брокерський', 'брокерська', 'брокерське',
                'трастовий', 'трастова', 'трастове', 'клірингова', 'клірингове', 'клірингової',
                'національний банк', 'центральний банк', 'комерційний банк', 'ощадний банк',
                'приват банк', 'альфа банк', 'укрексімбанк', 'ощадбанк', 'райффайзен',
                'кредитспілка', 'кредитна спілка', 'ломбард', 'мікрофінансова організація'
            ],
            'russian': [
                'банк', 'банковская', 'банковский', 'банковское', 'кредитный', 'кредитная', 'кредитное',
                'финансовый', 'финансовая', 'финансовое', 'инвестиционный', 'инвестиционная', 'инвестиционное',
                'страховой', 'страховая', 'страховое', 'лизинговый', 'лизинговая', 'лизинговое',
                'факторинговый', 'факторинговая', 'факторинговое', 'микрофинанс', 'микрокредит',
                'платежный', 'платежная', 'платежное', 'расчетный', 'расчетная', 'расчетное',
                'депозитный', 'депозитная', 'депозитное', 'валютный', 'валютная', 'валютное',
                'биржевой', 'биржевая', 'биржевое', 'брокерский', 'брокерская', 'брокерское',
                'трастовый', 'трастовая', 'трастовое', 'клиринговая', 'клиринговое', 'клиринговой',
                'национальный банк', 'центральный банк', 'коммерческий банк', 'сберегательный банк',
                'приват банк', 'альфа банк', 'сбербанк', 'втб', 'газпромбанк', 'россельхозбанк',
                'кредитный союз', 'ломбард', 'микрофинансовая организация'
            ],
            'english': [
                'bank', 'banking', 'financial', 'finance', 'investment', 'credit', 'loan',
                'insurance', 'leasing', 'factoring', 'microfinance', 'microcredit', 'payment',
                'settlement', 'deposit', 'currency', 'exchange', 'trading', 'brokerage',
                'trust', 'clearing', 'custodial', 'wealth', 'asset', 'fund', 'capital',
                'national bank', 'central bank', 'commercial bank', 'savings bank', 'investment bank',
                'private bank', 'retail bank', 'corporate bank', 'development bank',
                'jpmorgan', 'goldman sachs', 'morgan stanley', 'wells fargo', 'bank of america',
                'credit union', 'credit card', 'debit card', 'atm', 'swift', 'wire transfer',
                'correspondent bank', 'nostro', 'vostro', 'clearing house', 'settlement system'
            ]
        }
        
        # Специальные паттерны для финансовых услуг
        self.financial_services_patterns = [
            r'\b(?:банк|bank|банківський|банковский|banking)\b',
            r'\b(?:кредит|credit|loan|позика|заем)\b',
            r'\b(?:страхування|страхование|insurance|страховка)\b',
            r'\b(?:інвестиції|инвестиции|investment|вложения)\b',
            r'\b(?:біржа|биржа|exchange|trading|торги)\b',
            r'\b(?:брокер|broker|брокерський|брокерский)\b',
            r'\b(?:фінанси|финансы|finance|фінансовий|финансовый)\b',
            r'\b(?:платіжний|платежный|payment|оплата|платеж)\b',
            r'\b(?:депозит|deposit|вклад|депозитний|депозитный)\b',
            r'\b(?:валюта|currency|обмін|обмен|exchange)\b',
        ]
        
        self.logger.info("CompanyDetector initialized")
    
    def detect_company_signals(self, text: str) -> Dict[str, Any]:
        """
        Обнаружение сигналов компаний в тексте
        
        Args:
            text: Текст для анализа
            
        Returns:
            Результаты обнаружения сигналов компаний
        """
        if not text or not text.strip():
            return self._create_empty_result()
        
        signals = []
        total_confidence = 0.0
        
        # 1. Поиск ключевых слов компаний
        keyword_signals = self._detect_keywords(text)
        if keyword_signals['confidence'] > 0:
            signals.append(keyword_signals)
            total_confidence += keyword_signals['confidence']
        
        # 2. Поиск паттернов юридических лиц
        legal_entity_signals = self._detect_legal_entities(text)
        if legal_entity_signals['confidence'] > 0:
            signals.append(legal_entity_signals)
            total_confidence += legal_entity_signals['confidence']
        
        # 3. Поиск паттернов типов бизнеса
        business_type_signals = self._detect_business_types(text)
        if business_type_signals['confidence'] > 0:
            signals.append(business_type_signals)
            total_confidence += business_type_signals['confidence']
        
        # 4. Поиск адресной информации
        address_signals = self._detect_addresses(text)
        if address_signals['confidence'] > 0:
            signals.append(address_signals)
            total_confidence += address_signals['confidence']
        
        # 5. Поиск регистрационных номеров
        registration_signals = self._detect_registration_numbers(text)
        if registration_signals['confidence'] > 0:
            signals.append(registration_signals)
            total_confidence += registration_signals['confidence']
        
        # 6. Поиск названий с заглавных букв (потенциальные названия компаний)
        capitalized_signals = self._detect_capitalized_names(text)
        if capitalized_signals['confidence'] > 0:
            signals.append(capitalized_signals)
            total_confidence += capitalized_signals['confidence']
        
        # 7. Поиск банковских терминов
        banking_signals = self._detect_banking_terms(text)
        if banking_signals['confidence'] > 0:
            signals.append(banking_signals)
            total_confidence += banking_signals['confidence']
        
        # 8. Поиск финансовых услуг
        financial_services_signals = self._detect_financial_services(text)
        if financial_services_signals['confidence'] > 0:
            signals.append(financial_services_signals)
            total_confidence += financial_services_signals['confidence']
        
        # Нормализация общей уверенности
        normalized_confidence = min(total_confidence, 1.0)
        
        return {
            'confidence': normalized_confidence,
            'signals': signals,
            'signal_count': len(signals),
            'high_confidence_signals': [s for s in signals if s['confidence'] > 0.7],
            'detected_keywords': self._extract_detected_keywords(signals),
            'text_length': len(text),
            'analysis_complete': True
        }
    
    def _detect_keywords(self, text: str) -> Dict[str, Any]:
        """Обнаружение ключевых слов компаний"""
        matches = []
        text_lower = text.lower()
        
        for language, keywords in self.company_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matches.append(keyword)
        
        confidence = min(len(matches) * 0.2, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'keywords',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_legal_entities(self, text: str) -> Dict[str, Any]:
        """Обнаружение юридических лиц"""
        matches = []
        
        for pattern in self.company_patterns['legal_entities']:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.3, 0.9) if matches else 0.0
        
        return {
            'signal_type': 'legal_entities',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_business_types(self, text: str) -> Dict[str, Any]:
        """Обнаружение типов бизнеса"""
        matches = []
        
        for pattern in self.company_patterns['business_types']:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.25, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'business_types',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_addresses(self, text: str) -> Dict[str, Any]:
        """Обнаружение адресной информации"""
        matches = []
        
        for pattern in self.address_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.4, 0.7) if matches else 0.0
        
        return {
            'signal_type': 'addresses',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_registration_numbers(self, text: str) -> Dict[str, Any]:
        """Обнаружение регистрационных номеров"""
        matches = []
        
        for pattern in self.registration_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.5, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'registration_numbers',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_capitalized_names(self, text: str) -> Dict[str, Any]:
        """Обнаружение названий с заглавных букв"""
        # Паттерн для слов, начинающихся с заглавной буквы
        pattern = r'\b[A-ZА-ЯІЇЄҐ][a-zа-яіїєґ]{2,}(?:\s+[A-ZА-ЯІЇЄҐ][a-zа-яіїєґ]{2,})*\b'
        matches = re.findall(pattern, text)
        
        # Фильтрация общих слов
        common_words = {'Оплата', 'Платеж', 'Перевод', 'Счет', 'Квитанция', 'Документ'}
        filtered_matches = [match for match in matches if match not in common_words]
        
        confidence = min(len(filtered_matches) * 0.15, 0.6) if filtered_matches else 0.0
        
        return {
            'signal_type': 'capitalized_names',
            'confidence': confidence,
            'matches': list(set(filtered_matches)),
            'count': len(filtered_matches)
        }
    
    def _extract_detected_keywords(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Извлечение всех обнаруженных ключевых слов"""
        all_keywords = []
        for signal in signals:
            if 'matches' in signal:
                all_keywords.extend(signal['matches'])
        return list(set(all_keywords))
    
    def _detect_banking_terms(self, text: str) -> Dict[str, Any]:
        """Обнаружение банковских терминов"""
        matches = []
        text_lower = text.lower()
        
        # Поиск по всем языкам
        for language, terms in self.banking_terms.items():
            for term in terms:
                if term.lower() in text_lower:
                    matches.append(term)
        
        confidence = min(len(matches) * 0.6, 0.9) if matches else 0.0
        
        return {
            'signal_type': 'banking_terms',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_financial_services(self, text: str) -> Dict[str, Any]:
        """Обнаружение финансовых услуг по паттернам"""
        matches = []
        
        for pattern in self.financial_services_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.5, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'financial_services',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def get_enhanced_company_analysis(self, text: str) -> Dict[str, Any]:
        """
        Получение расширенного анализа компании
        
        Args:
            text: Текст для анализа
            
        Returns:
            Расширенный анализ компании
        """
        result = self.detect_company_signals(text)
        
        # Дополнительная статистика
        analysis = {
            'basic_result': result,
            'detailed_breakdown': {
                'legal_entities': 0,
                'business_types': 0,
                'banking_terms': 0,
                'financial_services': 0,
                'addresses': 0,
                'registration_numbers': 0,
                'capitalized_names': 0
            },
            'company_type_analysis': {
                'is_financial_institution': False,
                'is_legal_entity': False,
                'has_registration_info': False,
                'most_likely_sector': 'unknown'
            }
        }
        
        # Анализ типов сигналов
        for signal in result.get('signals', []):
            signal_type = signal.get('signal_type', '')
            count = signal.get('count', 0)
            
            if signal_type in analysis['detailed_breakdown']:
                analysis['detailed_breakdown'][signal_type] = count
            
            # Анализ типа компании
            if signal_type in ['banking_terms', 'financial_services']:
                analysis['company_type_analysis']['is_financial_institution'] = True
            elif signal_type == 'legal_entities':
                analysis['company_type_analysis']['is_legal_entity'] = True
            elif signal_type == 'registration_numbers':
                analysis['company_type_analysis']['has_registration_info'] = True
        
        # Определение сектора
        if analysis['company_type_analysis']['is_financial_institution']:
            analysis['company_type_analysis']['most_likely_sector'] = 'financial'
        elif analysis['detailed_breakdown'].get('legal_entities', 0) > 0:
            analysis['company_type_analysis']['most_likely_sector'] = 'commercial'
        elif analysis['detailed_breakdown'].get('business_types', 0) > 0:
            analysis['company_type_analysis']['most_likely_sector'] = 'business'
        
        return analysis
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Создание пустого результата"""
        return {
            'confidence': 0.0,
            'signals': [],
            'signal_count': 0,
            'high_confidence_signals': [],
            'detected_keywords': [],
            'text_length': 0,
            'analysis_complete': True
        }
