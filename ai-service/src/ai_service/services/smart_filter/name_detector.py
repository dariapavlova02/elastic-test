"""
Name Detector

Детектор для определения сигналов имен людей в тексте.
Использует лингвистические паттерны и словари имен для быстрого определения
потенциальных имен людей.
"""

import re
from typing import Dict, List, Any, Set
from dataclasses import dataclass

from ...utils.logging_config import get_logger
from ...data.dicts.smart_filter_patterns import (
    NAME_PATTERNS, PAYMENT_CONTEXT_PATTERNS, PHONETIC_PATTERNS, COMMON_WORDS
)

# Импорт словарей имен
try:
    from ...data.dicts import (
        english_names, russian_names, ukrainian_names, 
        asian_names, arabic_names, indian_names, 
        european_names, scandinavian_names
    )
    DICTIONARIES_AVAILABLE = True
except ImportError:
    DICTIONARIES_AVAILABLE = False


@dataclass
class NameSignal:
    """Сигнал обнаружения имени"""
    signal_type: str
    confidence: float
    matches: List[str]
    position: int
    context: str


class NameDetector:
    """Детектор имен людей"""
    
    def __init__(self):
        """Инициализация детектора"""
        self.logger = get_logger(__name__)
        
        # Загрузка словарей имен
        self.name_dictionaries = self._load_name_dictionaries()
        
        # Паттерны для определения имен (из словаря)
        self.name_patterns = NAME_PATTERNS.copy()
        
        # Расширенные паттерны для славянских фамилий
        self.surname_patterns = [
            # Украинские/Русские фамилии
            r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ов|ев|ін|ин|енко|ко|ук|юк|ич|ський|цький|ський|цкий)\b',
            r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ова|ева|іна|ина|енко|ко|ук|юк|ич|ська|цька|ська|цкая)\b',
            # Английские фамилии
            r'\b[A-Z][a-z]*(?:son|sen|berg|stein|man|mann|ski|sky|ova|ev|in|off|ov)\b'
        ]
        
        # Паттерны для отчеств
        self.patronymic_patterns = [
            # Мужские отчества
            r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ович|евич|йович|ійович|інович|инович)\b',
            r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ич)(?:\s|$)',
            # Женские отчества
            r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:івна|ївна|инична|овна|евна)\b',
        ]
        
        # Расширенные паттерны для имен
        self.enhanced_name_patterns = {
            'full_names_with_patronymics': [
                # Полное имя с отчеством (Имя Отчество Фамилия)
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]+\s+[А-ЯІЇЄҐ][а-яіїєґ]*(?:ович|евич|йович|ійович|івна|ївна|инична|овна|евна)\s+[А-ЯІЇЄҐ][а-яіїєґ]*(?:ов|ев|ін|ин|енко|ко|ук|юк|ич|ський|цький|ська|цька)\b',
                # Фамилия Имя Отчество
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ов|ев|ін|ин|енко|ко|ук|юк|ич|ський|цький|ська|цька)\s+[А-ЯІЇЄҐ][а-яіїєґ]+\s+[А-ЯІЇЄҐ][а-яіїєґ]*(?:ович|евич|йович|ійович|івна|ївна|инична|овна|евна)\b'
            ],
            'surnames_only': [
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:енко|ко)\b',  # -енко, -ко
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ов|ев|ін|ин)\b',  # -ов, -ев, -ін, -ин
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ський|цький|ська|цька)\b',  # -ський, -цький
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ич)(?:\s|$)',  # -ич в конце
            ],
            'patronymics_only': [
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:ович|евич|йович|ійович)(?:\s|$)',  # мужские отчества
                r'\b[А-ЯІЇЄҐ][а-яіїєґ]*(?:івна|ївна|инична|овна|евна)(?:\s|$)',  # женские отчества
            ]
        }
        
        # Паттерны для исключения
        self.exclusion_patterns = [
            r'^(оплата|платеж|перевод|счет|квитанция|документ)$',
            r'^(товариство|компанія|банк|організація)$',
            r'^(місто|город|вулиця|улица|будинок|дом)$',
            r'^\d+$',  # Только цифры
            r'^[^\w\s]+$'  # Только спецсимволы
        ]
        
        # Общие слова, которые не являются именами (из словаря)
        self.common_words = COMMON_WORDS.copy()
        
        self.logger.info("NameDetector initialized")
    
    def detect_name_signals(self, text: str) -> Dict[str, Any]:
        """
        Обнаружение сигналов имен в тексте
        
        Args:
            text: Текст для анализа
            
        Returns:
            Результаты обнаружения сигналов имен
        """
        if not text or not text.strip():
            return self._create_empty_result()
        
        signals = []
        total_confidence = 0.0
        
        # 1. Поиск полных имен
        full_name_signals = self._detect_full_names(text)
        if full_name_signals['confidence'] > 0:
            signals.append(full_name_signals)
            total_confidence += full_name_signals['confidence']
        
        # 2. Поиск имен с инициалами
        initials_signals = self._detect_initials(text)
        if initials_signals['confidence'] > 0:
            signals.append(initials_signals)
            total_confidence += initials_signals['confidence']
        
        # 3. Поиск одиночных имен (с проверкой по словарю)
        single_name_signals = self._detect_single_names(text)
        if single_name_signals['confidence'] > 0:
            signals.append(single_name_signals)
            total_confidence += single_name_signals['confidence']
        
        # 4. Поиск имен в контексте платежей
        context_signals = self._detect_payment_context_names(text)
        if context_signals['confidence'] > 0:
            signals.append(context_signals)
            total_confidence += context_signals['confidence']
        
        # 5. Поиск имен по фонетическим паттернам
        phonetic_signals = self._detect_phonetic_patterns(text)
        if phonetic_signals['confidence'] > 0:
            signals.append(phonetic_signals)
            total_confidence += phonetic_signals['confidence']
        
        # 6. Поиск славянских фамилий (-ов, -енко и т.д.)
        surname_signals = self._detect_slavic_surnames(text)
        if surname_signals['confidence'] > 0:
            signals.append(surname_signals)
            total_confidence += surname_signals['confidence']
        
        # 7. Поиск отчеств (-ович, -евич и т.д.)
        patronymic_signals = self._detect_patronymics(text)
        if patronymic_signals['confidence'] > 0:
            signals.append(patronymic_signals)
            total_confidence += patronymic_signals['confidence']
        
        # 8. Поиск полных имен с отчествами
        full_name_patronymic_signals = self._detect_full_names_with_patronymics(text)
        if full_name_patronymic_signals['confidence'] > 0:
            signals.append(full_name_patronymic_signals)
            total_confidence += full_name_patronymic_signals['confidence']
        
        # Нормализация общей уверенности
        normalized_confidence = min(total_confidence, 1.0)
        
        return {
            'confidence': normalized_confidence,
            'signals': signals,
            'signal_count': len(signals),
            'high_confidence_signals': [s for s in signals if s['confidence'] > 0.7],
            'detected_names': self._extract_detected_names(signals),
            'text_length': len(text),
            'analysis_complete': True
        }
    
    def _load_name_dictionaries(self) -> Dict[str, Set[str]]:
        """Загрузка словарей имен"""
        dictionaries = {}
        
        if DICTIONARIES_AVAILABLE:
            dictionaries = {
                'english': set(english_names.NAMES),
                'russian': set(russian_names.NAMES),
                'ukrainian': set(ukrainian_names.NAMES),
                'asian': set(asian_names.NAMES),
                'arabic': set(arabic_names.NAMES),
                'indian': set(indian_names.NAMES),
                'european': set(european_names.NAMES),
                'scandinavian': set(scandinavian_names.NAMES)
            }
        else:
            # Fallback - пустые словари
            dictionaries = {
                'english': set(),
                'russian': set(),
                'ukrainian': set(),
                'asian': set(),
                'arabic': set(),
                'indian': set(),
                'european': set(),
                'scandinavian': set()
            }
        
        return dictionaries
    
    def _detect_full_names(self, text: str) -> Dict[str, Any]:
        """Обнаружение полных имен"""
        matches = []
        
        for pattern in self.name_patterns['full_names']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Фильтрация по словарям имен
        filtered_matches = self._filter_by_dictionaries(matches)
        
        confidence = min(len(filtered_matches) * 0.4, 0.9) if filtered_matches else 0.0
        
        return {
            'signal_type': 'full_names',
            'confidence': confidence,
            'matches': list(set(filtered_matches)),
            'count': len(filtered_matches)
        }
    
    def _detect_initials(self, text: str) -> Dict[str, Any]:
        """Обнаружение имен с инициалами"""
        matches = []
        
        for pattern in self.name_patterns['initials']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.6, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'initials',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_single_names(self, text: str) -> Dict[str, Any]:
        """Обнаружение одиночных имен"""
        matches = []
        
        for pattern in self.name_patterns['single_names']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Фильтрация по словарям и исключение общих слов
        filtered_matches = self._filter_single_names(matches)
        
        confidence = min(len(filtered_matches) * 0.3, 0.6) if filtered_matches else 0.0
        
        return {
            'signal_type': 'single_names',
            'confidence': confidence,
            'matches': list(set(filtered_matches)),
            'count': len(filtered_matches)
        }
    
    def _detect_payment_context_names(self, text: str) -> Dict[str, Any]:
        """Обнаружение имен в контексте платежей"""
        matches = []
        for pattern in PAYMENT_CONTEXT_PATTERNS:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.5, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'payment_context',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_phonetic_patterns(self, text: str) -> Dict[str, Any]:
        """Обнаружение имен по фонетическим паттернам"""
        matches = []
        for pattern in PHONETIC_PATTERNS:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Фильтрация по словарям
        filtered_matches = self._filter_by_dictionaries(matches)
        
        confidence = min(len(filtered_matches) * 0.2, 0.5) if filtered_matches else 0.0
        
        return {
            'signal_type': 'phonetic_patterns',
            'confidence': confidence,
            'matches': list(set(filtered_matches)),
            'count': len(filtered_matches)
        }
    
    def _filter_by_dictionaries(self, matches: List[str]) -> List[str]:
        """Фильтрация совпадений по словарям имен"""
        if not DICTIONARIES_AVAILABLE:
            return matches
        
        filtered = []
        all_names = set()
        
        # Объединяем все словари
        for names in self.name_dictionaries.values():
            all_names.update(names)
        
        for match in matches:
            # Разбиваем на слова
            words = match.split()
            for word in words:
                if word.lower() in all_names:
                    filtered.append(match)
                    break
        
        return filtered
    
    def _filter_single_names(self, matches: List[str]) -> List[str]:
        """Фильтрация одиночных имен"""
        if not DICTIONARIES_AVAILABLE:
            return matches
        
        filtered = []
        all_names = set()
        
        # Объединяем все словари
        for names in self.name_dictionaries.values():
            all_names.update(names)
        
        # Объединяем общие слова
        all_common_words = set()
        for words in self.common_words.values():
            all_common_words.update(words)
        
        for match in matches:
            word_lower = match.lower()
            
            # Проверяем, что это не общее слово
            if word_lower in all_common_words:
                continue
            
            # Проверяем, что это имя из словаря
            if word_lower in all_names:
                filtered.append(match)
        
        return filtered
    
    def _extract_detected_names(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Извлечение всех обнаруженных имен"""
        all_names = []
        for signal in signals:
            if 'matches' in signal:
                all_names.extend(signal['matches'])
        return list(set(all_names))
    
    def _detect_slavic_surnames(self, text: str) -> Dict[str, Any]:
        """Обнаружение славянских фамилий (-ов, -енко, -ко, -ский и т.д.)"""
        matches = []
        
        for pattern in self.enhanced_name_patterns['surnames_only']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Дополнительная проверка по общим паттернам фамилий
        for pattern in self.surname_patterns:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Фильтрация общих слов
        filtered_matches = [match for match in matches if not self._is_common_word(match)]
        
        confidence = min(len(filtered_matches) * 0.7, 0.9) if filtered_matches else 0.0
        
        return {
            'signal_type': 'slavic_surnames',
            'confidence': confidence,
            'matches': list(set(filtered_matches)),
            'count': len(filtered_matches)
        }
    
    def _detect_patronymics(self, text: str) -> Dict[str, Any]:
        """Обнаружение отчеств (-ович, -евич, -івна и т.д.)"""
        matches = []
        
        for pattern in self.enhanced_name_patterns['patronymics_only']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Дополнительная проверка по паттернам отчеств
        for pattern in self.patronymic_patterns:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.8, 0.95) if matches else 0.0
        
        return {
            'signal_type': 'patronymics',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_full_names_with_patronymics(self, text: str) -> Dict[str, Any]:
        """Обнаружение полных имен с отчествами"""
        matches = []
        
        for pattern in self.enhanced_name_patterns['full_names_with_patronymics']:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.9, 1.0) if matches else 0.0
        
        return {
            'signal_type': 'full_names_with_patronymics',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _is_common_word(self, word: str) -> bool:
        """Проверка, является ли слово общим (не именем)"""
        word_lower = word.lower()
        
        # Объединяем все общие слова
        all_common_words = set()
        for words in self.common_words.values():
            all_common_words.update([w.lower() for w in words])
        
        return word_lower in all_common_words
    
    def get_detailed_name_analysis(self, text: str) -> Dict[str, Any]:
        """
        Получение детального анализа имен в тексте
        
        Args:
            text: Текст для анализа
            
        Returns:
            Детальный анализ имен
        """
        result = self.detect_name_signals(text)
        
        # Дополнительная статистика
        analysis = {
            'basic_result': result,
            'detailed_breakdown': {
                'surnames_detected': 0,
                'patronymics_detected': 0,
                'full_names_detected': 0,
                'initials_detected': 0,
                'single_names_detected': 0
            },
            'name_structure_analysis': {
                'has_slavic_surnames': False,
                'has_patronymics': False,
                'has_full_names_with_patronymics': False,
                'most_likely_language': 'unknown'
            }
        }
        
        # Анализ типов сигналов
        for signal in result.get('signals', []):
            signal_type = signal.get('signal_type', '')
            count = signal.get('count', 0)
            
            if signal_type == 'slavic_surnames':
                analysis['detailed_breakdown']['surnames_detected'] = count
                analysis['name_structure_analysis']['has_slavic_surnames'] = True
            elif signal_type == 'patronymics':
                analysis['detailed_breakdown']['patronymics_detected'] = count
                analysis['name_structure_analysis']['has_patronymics'] = True
            elif signal_type == 'full_names_with_patronymics':
                analysis['detailed_breakdown']['full_names_detected'] = count
                analysis['name_structure_analysis']['has_full_names_with_patronymics'] = True
            elif signal_type == 'initials':
                analysis['detailed_breakdown']['initials_detected'] = count
            elif signal_type == 'single_names':
                analysis['detailed_breakdown']['single_names_detected'] = count
        
        # Определение наиболее вероятного языка
        if analysis['name_structure_analysis']['has_patronymics'] or \
           analysis['name_structure_analysis']['has_slavic_surnames']:
            # Проверяем на украинские окончания
            if any(re.search(r'(енко|ко|івна|ійович|ських|цьк)', text, re.IGNORECASE) for _ in [1]):
                analysis['name_structure_analysis']['most_likely_language'] = 'ukrainian'
            else:
                analysis['name_structure_analysis']['most_likely_language'] = 'russian'
        elif any(re.search(r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b', text) for _ in [1]):
            analysis['name_structure_analysis']['most_likely_language'] = 'english'
        
        return analysis
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Создание пустого результата"""
        return {
            'confidence': 0.0,
            'signals': [],
            'signal_count': 0,
            'high_confidence_signals': [],
            'detected_names': [],
            'text_length': 0,
            'analysis_complete': True
        }
