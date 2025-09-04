"""
Document Signal Detector

Детектор для определения сигналов документов в тексте.
Обнаруживает ИНН, даты, адреса, номера документов и другую
документарную информацию.
"""

import re
from typing import Dict, List, Any, Set
from dataclasses import dataclass
from datetime import datetime

from ...utils.logging_config import get_logger


@dataclass
class DocumentSignal:
    """Сигнал обнаружения документа"""
    signal_type: str
    confidence: float
    matches: List[str]
    position: int
    context: str


class DocumentDetector:
    """Детектор документарных сигналов"""
    
    def __init__(self):
        """Инициализация детектора"""
        self.logger = get_logger(__name__)
        
        # Паттерны для ИНН (различные форматы)
        self.inn_patterns = [
            r'\b(?:ИНН|інн|inn|ідентифікаційний\s+номер|идентификационный\s+номер)[:\s]*(\d{8,12})\b',
            r'\b(\d{8})\b(?=.*(?:ИНН|інн|inn))',  # 8 цифр в контексте ИНН
            r'\b(\d{10})\b(?=.*(?:ИНН|інн|inn))',  # 10 цифр в контексте ИНН
            r'\b(\d{12})\b(?=.*(?:ИНН|інн|inn))',  # 12 цифр в контексте ИНН
            r'\b\d{3}\s*\d{3}\s*\d{3}\s*\d{3}\b',  # Форматированный ИНН
        ]
        
        # Паттерны для дат (различные форматы)
        self.date_patterns = [
            r'\b\d{1,2}[./\-]\d{1,2}[./\-]\d{2,4}\b',  # DD/MM/YYYY, DD-MM-YYYY
            r'\b\d{2,4}[./\-]\d{1,2}[./\-]\d{1,2}\b',  # YYYY/MM/DD, YYYY-MM-DD
            r'\b\d{1,2}\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+\d{2,4}\b',
            r'\b\d{1,2}\s+(січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)\s+\d{2,4}\b',
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}\b',
        ]
        
        # Паттерны для номеров документов
        self.document_patterns = [
            # Паспорт
            r'\b(?:паспорт|passport|пасп)[:\s]*([А-ЯІЇЄҐA-Z]{2}\d{6})\b',
            r'\b([А-ЯІЇЄҐA-Z]{2}\s*\d{6})\b',
            
            # Водительские права
            r'\b(?:водій|водитель|driver|rights|посвідчення)[:\s]*([А-ЯІЇЄҐA-Z]{3}\d{6})\b',
            
            # Свидетельство о рождении
            r'\b(?:свідоцтво|свидетельство|birth|certificate)[:\s]*([А-ЯІЇЄҐA-Z]{1,3}-[А-ЯІЇЄҐA-Z]{1,3}\s*\d{6})\b',
            
            # Другие документы с буквенно-цифровыми кодами
            r'\b[А-ЯІЇЄҐA-Z]{2,4}\s*\d{6,10}\b',
            r'\b\d{4,6}-[А-ЯІЇЄҐA-Z]{2,4}-\d{4,6}\b',
        ]
        
        # Паттерны для адресов
        self.address_patterns = [
            # Индексы
            r'\b\d{5,6}\b(?=.*(?:індекс|индекс|поштовий|почтовый|zip|postal))',
            r'\b(?:індекс|индекс|поштовий|почтовий|zip|postal)[:\s]*(\d{5,6})\b',
            
            # Полные адреса
            r'\b(?:адреса|адрес|address)[:\s]*([^\n\r]{20,100})\b',
            r'\b(?:м\.|місто|город|city)[:\s]*([А-ЯІЇЄҐA-Z][а-яіїєґa-z\s\-\']+)\b',
            r'\b(?:вул\.|вулиця|улица|street)[:\s]*([А-ЯІЇЄҐA-Z][а-яіїєґa-z\s\-\']+)\b',
            r'\b(?:буд\.|будинок|дом|building)[:\s]*(\d+[а-яіїєґa-z]*)\b',
            r'\b(?:кв\.|квартира|квартира|apartment)[:\s]*(\d+)\b',
            
            # Координаты
            r'\b\d{1,3}\.\d{4,6},?\s*\d{1,3}\.\d{4,6}\b',  # Широта/долгота
        ]
        
        # Паттерны для банковских реквизитов
        self.bank_patterns = [
            r'\b(?:МФО|мфо|BIC|bic|swift|SWIFT)[:\s]*([А-ЯІЇЄҐA-Z0-9]{6,11})\b',
            r'\b(?:рахунок|счет|account|IBAN|iban)[:\s]*([А-ЯІЇЄҐA-Z0-9\s]{10,34})\b',
            r'\b(?:картка|карта|card)[:\s]*(\d{4}\s*\*{4,12}\s*\d{4})\b',
            r'\bUA\d{2}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{4}\s*\d{4}\b',  # IBAN Ukraine
        ]
        
        # Паттерны для номеров телефонов
        self.phone_patterns = [
            r'\b(?:\+?38)?[\s\-\(]?0[\d\s\-\(\)]{8,12}\b',  # Ukrainian phones
            r'\b\+?1[\s\-\(]?\d{3}[\s\-\)]?\d{3}[\s\-]?\d{4}\b',  # US phones
            r'\b\+?7[\s\-\(]?\d{3}[\s\-\)]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}\b',  # Russian phones
            r'\b\+?\d{1,4}[\s\-\(]?\d{1,4}[\s\-\)]?\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4}\b',
        ]
        
        # Паттерны для email адресов
        self.email_patterns = [
            r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
        ]
        
        # Контекстные слова для документов
        self.document_context_words = {
            'ukrainian': [
                'документ', 'документи', 'паспорт', 'посвідчення', 'свідоцтво',
                'довідка', 'довідки', 'сертифікат', 'ліцензія', 'дозвіл',
                'договір', 'контракт', 'угода', 'протокол', 'акт',
                'рахунок', 'інн', 'податковий', 'номер', 'код'
            ],
            'russian': [
                'документ', 'документы', 'паспорт', 'удостоверение', 'свидетельство',
                'справка', 'справки', 'сертификат', 'лицензия', 'разрешение',
                'договор', 'контракт', 'соглашение', 'протокол', 'акт',
                'счет', 'инн', 'налоговый', 'номер', 'код'
            ],
            'english': [
                'document', 'documents', 'passport', 'certificate', 'license',
                'permit', 'contract', 'agreement', 'protocol', 'act',
                'account', 'tax', 'number', 'code', 'id', 'identification'
            ]
        }
        
        self.logger.info("DocumentDetector initialized")
    
    def detect_document_signals(self, text: str) -> Dict[str, Any]:
        """
        Обнаружение сигналов документов в тексте
        
        Args:
            text: Текст для анализа
            
        Returns:
            Результаты обнаружения сигналов документов
        """
        if not text or not text.strip():
            return self._create_empty_result()
        
        signals = []
        total_confidence = 0.0
        
        # 1. Поиск ИНН
        inn_signals = self._detect_inn(text)
        if inn_signals['confidence'] > 0:
            signals.append(inn_signals)
            total_confidence += inn_signals['confidence']
        
        # 2. Поиск дат
        date_signals = self._detect_dates(text)
        if date_signals['confidence'] > 0:
            signals.append(date_signals)
            total_confidence += date_signals['confidence']
        
        # 3. Поиск номеров документов
        document_signals = self._detect_document_numbers(text)
        if document_signals['confidence'] > 0:
            signals.append(document_signals)
            total_confidence += document_signals['confidence']
        
        # 4. Поиск адресов
        address_signals = self._detect_addresses(text)
        if address_signals['confidence'] > 0:
            signals.append(address_signals)
            total_confidence += address_signals['confidence']
        
        # 5. Поиск банковских реквизитов
        bank_signals = self._detect_bank_details(text)
        if bank_signals['confidence'] > 0:
            signals.append(bank_signals)
            total_confidence += bank_signals['confidence']
        
        # 6. Поиск контактной информации
        contact_signals = self._detect_contact_info(text)
        if contact_signals['confidence'] > 0:
            signals.append(contact_signals)
            total_confidence += contact_signals['confidence']
        
        # Нормализация общей уверенности
        normalized_confidence = min(total_confidence, 1.0)
        
        return {
            'confidence': normalized_confidence,
            'signals': signals,
            'signal_count': len(signals),
            'high_confidence_signals': [s for s in signals if s['confidence'] > 0.7],
            'detected_documents': self._extract_detected_documents(signals),
            'text_length': len(text),
            'analysis_complete': True
        }
    
    def _detect_inn(self, text: str) -> Dict[str, Any]:
        """Обнаружение ИНН"""
        matches = []
        
        for pattern in self.inn_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(found_matches[0] if found_matches else None, tuple):
                matches.extend([match[0] for match in found_matches])
            else:
                matches.extend(found_matches)
        
        # Валидация ИНН (базовая проверка длины)
        validated_matches = []
        for match in matches:
            if re.match(r'^\d{8}$|^\d{10}$|^\d{12}$', match):
                validated_matches.append(match)
        
        confidence = min(len(validated_matches) * 0.8, 0.95) if validated_matches else 0.0
        
        return {
            'signal_type': 'inn',
            'confidence': confidence,
            'matches': list(set(validated_matches)),
            'count': len(validated_matches)
        }
    
    def _detect_dates(self, text: str) -> Dict[str, Any]:
        """Обнаружение дат"""
        matches = []
        
        for pattern in self.date_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            matches.extend(found_matches)
        
        # Валидация дат
        validated_matches = []
        for match in matches:
            if self._is_valid_date(match):
                validated_matches.append(match)
        
        confidence = min(len(validated_matches) * 0.3, 0.7) if validated_matches else 0.0
        
        return {
            'signal_type': 'dates',
            'confidence': confidence,
            'matches': list(set(validated_matches)),
            'count': len(validated_matches)
        }
    
    def _detect_document_numbers(self, text: str) -> Dict[str, Any]:
        """Обнаружение номеров документов"""
        matches = []
        
        for pattern in self.document_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(found_matches[0] if found_matches else None, tuple):
                matches.extend([match[0] for match in found_matches])
            else:
                matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.6, 0.9) if matches else 0.0
        
        return {
            'signal_type': 'document_numbers',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_addresses(self, text: str) -> Dict[str, Any]:
        """Обнаружение адресов"""
        matches = []
        
        for pattern in self.address_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(found_matches[0] if found_matches else None, tuple):
                matches.extend([match[0] for match in found_matches])
            else:
                matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.4, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'addresses',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_bank_details(self, text: str) -> Dict[str, Any]:
        """Обнаружение банковских реквизитов"""
        matches = []
        
        for pattern in self.bank_patterns:
            found_matches = re.findall(pattern, text, re.IGNORECASE)
            if isinstance(found_matches[0] if found_matches else None, tuple):
                matches.extend([match[0] for match in found_matches])
            else:
                matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.7, 0.9) if matches else 0.0
        
        return {
            'signal_type': 'bank_details',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _detect_contact_info(self, text: str) -> Dict[str, Any]:
        """Обнаружение контактной информации"""
        matches = []
        
        # Телефоны
        for pattern in self.phone_patterns:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        # Email
        for pattern in self.email_patterns:
            found_matches = re.findall(pattern, text)
            matches.extend(found_matches)
        
        confidence = min(len(matches) * 0.5, 0.8) if matches else 0.0
        
        return {
            'signal_type': 'contact_info',
            'confidence': confidence,
            'matches': list(set(matches)),
            'count': len(matches)
        }
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Базовая валидация даты"""
        # Простая проверка на разумность дат
        try:
            # Попытка парсинга различных форматов
            date_formats = ['%d/%m/%Y', '%d.%m.%Y', '%d-%m-%Y', 
                          '%Y/%m/%d', '%Y.%m.%d', '%Y-%m-%d']
            
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    # Проверяем, что дата в разумных пределах
                    if 1900 <= parsed_date.year <= 2100:
                        return True
                except ValueError:
                    continue
            
            return False
        except Exception:
            return False
    
    def _extract_detected_documents(self, signals: List[Dict[str, Any]]) -> List[str]:
        """Извлечение всех обнаруженных документов"""
        all_documents = []
        for signal in signals:
            if 'matches' in signal:
                all_documents.extend(signal['matches'])
        return list(set(all_documents))
    
    def _create_empty_result(self) -> Dict[str, Any]:
        """Создание пустого результата"""
        return {
            'confidence': 0.0,
            'signals': [],
            'signal_count': 0,
            'high_confidence_signals': [],
            'detected_documents': [],
            'text_length': 0,
            'analysis_complete': True
        }