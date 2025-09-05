"""
Service for creating name and surname search patterns
Used for preparing data for Aho-Corasick algorithm in Module 3
"""

import re
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from datetime import datetime

from ..utils import get_logger


@dataclass
class NamePattern:
    """Name search pattern"""
    pattern: str
    pattern_type: str
    language: str
    confidence: float
    source: str
    created_at: str = None


class PatternService:
    """Service for creating name and surname search patterns"""
    
    def __init__(self):
        """Initialize pattern service"""
        self.logger = get_logger(__name__)
        
        # Basic regex patterns for different languages
        self.name_patterns = {
            'en': {
                'full_name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
                'initials_surname': r'\b[A-Z]\. [A-Z]\. [A-Z][a-z]+\b',
                'surname_initials': r'\b[A-Z][a-z]+ [A-Z]\. [A-Z]\.\b',
                'single_initial_surname': r'\b[A-Z]\.\s*[A-Z][a-z]+\b',
                'surname_only': r'\b[A-Z][a-z]{2,}\b',
                'name_only': r'\b[A-Z][a-z]{2,}\b'
            },
            'ru': {
                'full_name': r'\b[А-ЯІЇЄ][а-яіїє]+ [А-ЯІЇЄ][а-яіїє]+\b',
                'initials_surname': r'\b[А-ЯІЇЄ]\. [А-ЯІЇЄ]\. [А-ЯІЇЄ][а-яіїє]+\b',
                'surname_initials': r'\b[А-ЯІЇЄ][а-яіїє]+ [А-ЯІЇЄ]\. [А-ЯІЇЄ]\.\b',
                'single_initial_surname': r'\b[А-ЯІЇЄ]\.\s*[А-ЯІЇЄ][а-яіїє]+\b',
                'surname_only': r'\b[А-ЯІЇЄ][а-яіїє]{2,}\b',
                'name_only': r'\b[А-ЯІЇЄ][а-яіїє]{2,}\b'
            },
            'uk': {
                'full_name': r'\b[А-ЯІЇЄ][а-яіїє]+ [А-ЯІЇЄ][а-яіїє]+\b',
                'initials_surname': r'\b[А-ЯІЇЄ]\. [А-ЯІЇЄ]\. [А-ЯІЇЄ][а-яіїє]+\b',
                'surname_initials': r'\b[А-ЯІЇЄ][а-яіїє]+ [А-ЯІЇЄ]\. [А-ЯІЇЄ]\.\b',
                'single_initial_surname': r'\b[А-ЯІЇЄ]\.\s*[А-ЯІЇЄ][а-яіїє]+\b',
                'surname_only': r'\b[А-ЯІЇЄ][а-яіїє]{2,}\b',
                'name_only': r'\b[А-ЯІЇЄ][а-яіїє]{2,}\b'
            },
            'fr': {
                'full_name': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
                'initials_surname': r'\b[A-Z]\. [A-Z]\. [A-Z][a-z]+\b',
                'surname_initials': r'\b[A-Z][a-z]+ [A-Z]\. [A-Z]\.\b',
                'surname_only': r'\b[A-Z][a-z]{2,}\b',
                'name_only': r'\b[A-Z][a-z]{2,}\b',
                'compound_name': r'\b[A-Z][a-z]+-[A-Z][a-z]+\b'  # For names like Jean-Baptiste
            },
            'es': {
                'full_name': r'\b[A-Z][a-záéíóúñÁÉÍÓÚÑ]+ [A-Z][a-záéíóúñÁÉÍÓÚÑ]+\b',
                'initials_surname': r'\b[A-Z]\. [A-Z]\. [A-Z][a-záéíóúñÁÉÍÓÚÑ]+\b',
                'surname_initials': r'\b[A-Z][a-záéíóúñÁÉÍÓÚÑ]+ [A-Z]\. [A-Z]\.\b',
                'surname_only': r'\b[A-Z][a-záéíóúñÁÉÍÓÚÑ]{2,}\b',
                'name_only': r'\b[A-Z][a-záéíóúñÁÉÍÓÚÑ]{2,}\b'
            }
        }
        
        # Prefer external dictionaries; fallback to minimal in-file sets
        try:
            from ..data.dicts.russian_names import NAMES as EXT_RU_NAMES
        except Exception:
            EXT_RU_NAMES = {}
        try:
            from ..data.dicts.ukrainian_names import NAMES as EXT_UK_NAMES
        except Exception:
            EXT_UK_NAMES = {}
        try:
            from ..data.dicts.english_names import NAMES as EXT_EN_NAMES
        except Exception:
            EXT_EN_NAMES = {}

        ru_name_set = set(EXT_RU_NAMES.keys()) or {'Иван', 'Петр', 'Сергей', 'Владимир', 'Анна', 'Мария'}
        uk_name_set = set(EXT_UK_NAMES.keys()) or {'Іван', 'Петро', 'Сергій', 'Володимир', 'Анна', 'Марія'}
        en_name_set = set(EXT_EN_NAMES.keys()) or {'John', 'Peter', 'Michael', 'Anna', 'Maria'}

        # External packs usually don't contain surnames; keep small heuristic fallback
        ru_surnames = {'Иванов', 'Петров', 'Сидоров', 'Порошенко'}
        uk_surnames = {'Іванов', 'Петренко', 'Сидоренко', 'Порошенко'}
        fr_names = {'Jean', 'Pierre', 'Marie', 'Sophie', 'Baptiste', 'Antoine', 'Claude'}
        fr_surnames = {'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit'}
        es_names = {'María', 'José', 'Carlos', 'Ana', 'Luis', 'Carmen', 'Miguel'}
        es_surnames = {'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez', 'Sánchez'}

        self.name_dictionaries = {
            'ru': {
                'names': ru_name_set,
                'surnames': ru_surnames
            },
            'uk': {
                'names': uk_name_set,
                'surnames': uk_surnames
            },
            'en': {
                'names': en_name_set,
                'surnames': set()  # keep empty unless provided externally
            },
            'fr': {
                'names': fr_names,
                'surnames': fr_surnames
            },
            'es': {
                'names': es_names,
                'surnames': es_surnames
            }
        }
        
        # Payment context patterns are built from external triggers
        self.payment_patterns = {'ru': [], 'uk': [], 'en': []}
        try:
            from ..data.dicts.payment_triggers import build_trigger_regex
            from ..data.dicts.company_triggers import COMPANY_TRIGGERS
            for lang in ('ru', 'uk', 'en'):
                tr = build_trigger_regex(lang)
                # Basic patterns
                if lang == 'en':
                    name = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})'
                    init_surname = r'([A-Z])\.?\s*([A-Z][a-z]+)'
                    context = tr.get('context', r'(?:payment|transfer|remittance)')
                    preps = tr.get('preps', r'(?:from|for|to)')
                else:
                    name = r'([А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+(?:\s+[А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+){0,3})'
                    init_surname = r'([А-ЯЁІЇЄҐ])\.?\s*([А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+)'
                    context = tr.get('context', r'(?:платеж|оплата|перевод)')
                    preps = tr.get('preps', r'(?:от|для)')

                patterns = [
                    rf'{context}[\s,:;-]*{preps}[\s,:;-]*{name}',
                    rf'\b{preps}[\s,:;-]*{name}',
                    rf'{context}[\s,:;-]*{preps}[\s,:;-]*{init_surname}',
                    # Recipient/sender first
                    rf'(?:получатель|одержувач)[\s:,-]*{name}',
                    rf'(?:получатель|одержувач)[\s:,-]*{init_surname}',
                    # “on behalf/name” style
                    rf'(?:на\s+имя|на\s+ім[\'ʼ]я)[\s,:;-]*{name}',
                ]
                self.payment_patterns[lang] = patterns
            # Build company context patterns
            self.company_patterns = {'ru': [], 'uk': [], 'en': []}
            for lang in ('ru', 'uk', 'en'):
                tr = build_trigger_regex(lang)
                legal = COMPANY_TRIGGERS.get(lang, {}).get('legal_entities', [])
                if legal:
                    legal_alt = r'(?:' + '|'.join(re.escape(le) for le in legal) + r')'
                else:
                    legal_alt = r'(?:ООО|ТОВ|ПП|ЗАО|ПАО|ОАО|АТ|ПрАТ|ФОП|ИП)'
                # Company name core: quoted or multi-token uppercase-ish words
                comp_core = r'(?:["“«][^"”»\n]{2,}["”»]|[A-ZА-ЯІЇЄҐ0-9][\w\-]+(?:\s+(?:[a-zа-яіїєґ]{1,5}|[A-ZА-ЯІЇЄҐ0-9][\w\-]+)){0,6})'
                comp_name = rf'({comp_core})(?=$|\s|["»”])'
                if lang == 'en':
                    preps = tr.get('preps', r'(?:from|for|to)')
                    context = tr.get('context', r'(?:payment|transfer|remittance|funds|money|credit|debit|incoming)')
                else:
                    preps = tr.get('preps', r'(?:от|для|від)')
                    context = tr.get('context', r'(?:платеж|оплата|перевод|переказ)')
                self.company_patterns[lang] = [
                    rf'{context}[\s,:;-]*{preps}[\s,:;-]*(?:{legal_alt}[\s\.]+)?{comp_name}',
                    rf'\b(?:получатель|одержувач|beneficiary|recipient)[:\s,-]*(?:{legal_alt}[\s\.]+)?{comp_name}',
                    rf'(?:на\s+имя|на\s+ім[\'ʼ]я|on\s+behalf\s+of)[\s,:;-]*(?:{legal_alt}[\s\.]+)?{comp_name}',
                    rf'\b(?:{legal_alt})[\s\.]+{comp_name}'
                ]
        except Exception:
            # Fallback simple patterns if triggers are not available
            self.payment_patterns = {
                'ru': [
                    r'(?:платеж|оплата|перевод)[\s,:;-]*(?:от|для)[\s,:;-]*([А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+(?:\s+[А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+){0,3})',
                    r'\b(?:от|для)[\s,:;-]*([А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+(?:\s+[А-ЯЁІЇЄҐ][а-яёіїєґ\'-]+){0,3})'
                ],
                'uk': [
                    r'(?:платіж|оплата|переказ)[\s,:;-]*(?:від|для)[\s,:;-]*([А-ЯІЇЄҐ][а-яіїєґ\'-]+(?:\s+[А-ЯІЇЄҐ][а-яіїєґ\'-]+){0,3})',
                    r'\b(?:від|для)[\s,:;-]*([А-ЯІЇЄҐ][а-яіїєґ\'-]+(?:\s+[А-ЯІЇЄҐ][а-яіїєґ\'-]+){0,3})'
                ],
                'en': [
                    r'(?:payment|transfer|remittance)[\s,:;-]*(?:from|for|to)[\s,:;-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})',
                    r'\b(?:from|for|to)[\s,:;-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})'
                ]
            }

        # Optional custom stop-words per language (loaded if provided by user)
        try:
            from ..data.dicts.stop_words import STOP_WORDS as _USER_STOP_WORDS
            self.stop_words = _USER_STOP_WORDS
        except Exception:
            # Default stop words + legal phrases that should be dropped
            self.stop_words = {
                'ru': { 'платеж', 'оплата', 'перевод', 'перечисление', 'зачисление', 'списание', 'от', 'для',
                        'общество с ограниченной ответственностью', 'компания', 'товарищество' },
                'uk': { 'платіж', 'оплата', 'переказ', 'перерахування', 'зарахування', 'списання', 'від', 'для',
                        'товариство з обмеженою відповідальністю', 'компанія' },
                'en': { 'payment', 'transfer', 'remittance', 'from', 'for', 'to', 'limited liability company', 'company' }
            }
        
        self.logger.info("PatternService initialized")
    
    def generate_patterns(
        self,
        text: str,
        language: str = 'auto'
    ) -> List[NamePattern]:
        """
        Generate patterns for searching names in text
        
        Args:
            text: Input text
            language: Text language ('auto', 'en', 'ru', 'uk')
            
        Returns:
            List of search patterns
        """
        if not text or not text.strip():
            return []
        
        # Auto-detect language if needed
        if language == 'auto':
            language = self._detect_language_simple(text)
        
        patterns = []
        
        # 1. Basic name patterns
        basic_patterns = self._extract_basic_name_patterns(text, language)
        patterns.extend(basic_patterns)
        
        # 2. Payment context patterns
        context_patterns = self._extract_payment_context_patterns(text, language)
        patterns.extend(context_patterns)
        
        # 2b. Company context patterns
        if hasattr(self, 'company_patterns'):
            company_patterns = self._extract_company_context_patterns(text, language)
            patterns.extend(company_patterns)
        
        # 3. Dictionary patterns
        dict_patterns = self._extract_dictionary_name_patterns(text, language)
        patterns.extend(dict_patterns)
        
        # 4. Position patterns (3-4 word)
        position_patterns = self._extract_position_patterns(text, language)
        patterns.extend(position_patterns)
        
        # 5. Deduplicate patterns
        unique_patterns = self._remove_duplicate_patterns(patterns)
        
        self.logger.info(f"Generated {len(unique_patterns)} unique patterns for language: {language}")
        return unique_patterns
    
    def _remove_duplicate_patterns(self, patterns: List[NamePattern]) -> List[NamePattern]:
        """Remove duplicate patterns"""
        seen = set()
        unique_patterns = []
        
        for pattern in patterns:
            # Create a key for uniqueness based on pattern text, type, and language
            # Preserve original case for uniqueness
            key = (pattern.pattern.lower(), pattern.pattern_type, pattern.language)
            
            if key not in seen:
                seen.add(key)
                unique_patterns.append(pattern)
        
        return unique_patterns
    
    def _extract_company_context_patterns(self, text: str, language: str) -> List[NamePattern]:
        """Extract company context patterns"""
        patterns = []
        comp_patterns = getattr(self, 'company_patterns', {}).get(language)
        if not comp_patterns:
            return patterns
        
        for regex in comp_patterns:
            matches = re.finditer(regex, text, re.IGNORECASE)
            for m in matches:
                # Company name often captured in the last group
                name_text = None
                if m.lastindex:
                    for gi in range(m.lastindex, 0, -1):
                        g = m.group(gi)
                        if g and len(g.strip()) > 0:
                            name_text = g
                            break
                if not name_text:
                    continue
                cleaned = re.sub(r'^["«»\']\s*|\s*["«»\']$', '', name_text.strip())
                cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                if len(cleaned) < 2:
                    continue
                pattern = NamePattern(
                    pattern=cleaned,
                    pattern_type='company_context',
                    language=language,
                    confidence=0.85,
                    source='company_context',
                    created_at=datetime.now().isoformat()
                )
                patterns.append(pattern)
        return patterns
    
    def _extract_basic_name_patterns(self, text: str, language: str) -> List[NamePattern]:
        """Extract basic name patterns"""
        patterns = []
        
        if language not in self.name_patterns:
            return patterns
        
        for pattern_type, regex in self.name_patterns[language].items():
            matches = re.finditer(regex, text, re.IGNORECASE)
            
            for match in matches:
                matched_text = match.group()
                
                # Create pattern in original case
                pattern = NamePattern(
                    pattern=matched_text,
                    pattern_type=pattern_type,
                    language=language,
                    confidence=0.8,
                    source='regex',
                    created_at=datetime.now().isoformat()
                )
                patterns.append(pattern)
                
                # Additionally create pattern in lowercase for better coverage
                if matched_text != matched_text.lower():
                    pattern_lower = NamePattern(
                        pattern=matched_text.lower(),
                        pattern_type=pattern_type,
                        language=language,
                        confidence=0.7,
                        source='regex_lowercase',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern_lower)
                
                # And in title case
                if matched_text != matched_text.title():
                    pattern_title = NamePattern(
                        pattern=matched_text.title(),
                        pattern_type=pattern_type,
                        language=language,
                        confidence=0.7,
                        source='regex_titlecase',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern_title)
        
        return patterns
    
    def _extract_payment_context_patterns(self, text: str, language: str) -> List[NamePattern]:
        """Extract payment context patterns"""
        patterns = []
        
        if language not in self.payment_patterns:
            return patterns
        
        for regex in self.payment_patterns[language]:
            matches = re.finditer(regex, text, re.IGNORECASE)

            for match in matches:
                # Support both variants: only name or initial+surname
                if match.group(1) and not match.lastindex or (match.lastindex and match.lastindex == 1):
                    raw = match.group(1)
                    name_text = self._strip_stop_words(raw.strip(), language)
                elif match.lastindex and match.lastindex >= 2 and match.group(1) and match.group(2):
                    initial = match.group(1).strip()
                    surname = match.group(2).strip()
                    name_text = f"{initial}. {surname}"
                else:
                    continue

                # Heuristic: allow multiword names or initials+surname
                tokens = re.findall(r"[A-Za-zА-Яа-яІіЇїЄєҐґ\'-]+", name_text)
                ok = False
                if len(tokens) >= 2:
                    if self._looks_like_name(tokens[0], language) or self._looks_like_name(tokens[1], language):
                        ok = True
                elif len(tokens) == 1:
                    ok = self._looks_like_name(tokens[0], language)

                if ok:
                    pattern = NamePattern(
                        pattern=name_text,
                        pattern_type='payment_context',
                        language=language,
                        confidence=0.9,
                        source='payment_context',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern)
        
        return patterns

    def _strip_stop_words(self, text: str, language: str) -> str:
        """Remove configured stop words from boundaries of the text."""
        if not text:
            return text
        sw = set(self.stop_words.get(language, []))
        if not sw:
            return text
        tokens = re.findall(r"[A-Za-zА-Яа-яІіЇїЄєҐґ\'\u02BC\u2019\-]+", text)
        if not tokens:
            return text
        # Drop leading stop-words
        while tokens and tokens[0].lower() in sw:
            tokens.pop(0)
        # Drop trailing stop-words
        while tokens and tokens[-1].lower() in sw:
            tokens.pop()
        cleaned = ' '.join(tokens)
        return cleaned.strip()
    
    def _extract_dictionary_name_patterns(self, text: str, language: str) -> List[NamePattern]:
        """Extract patterns from name dictionaries"""
        patterns = []
        
        if language not in self.name_dictionaries:
            return patterns
        
        # Improved regex for handling apostrophes and hyphens in names
        words = re.findall(r"\b[A-ZА-ЯІЇЄ][a-zA-Zа-яіїє\'\u02BC\u2019\-]+\b", text)
        
        # Check names
        for word in words:
            if word in self.name_dictionaries[language]['names']:
                pattern = NamePattern(
                    pattern=word,  # Preserve original spelling
                    pattern_type='dictionary_name',
                    language=language,
                    confidence=0.95,
                    source='name_dictionary',
                    created_at=datetime.now().isoformat()
                )
                patterns.append(pattern)
            
            # Additionally check compound name parts (e.g., "O'Connor" -> "OConnor")
            if "'" in word or "-" in word:
                # Remove apostrophes and hyphens for checking
                clean_word = re.sub(r'[\'-]', '', word)
                if clean_word in self.name_dictionaries[language]['names']:
                    pattern = NamePattern(
                        pattern=clean_word,
                        pattern_type='dictionary_name_clean',
                        language=language,
                        confidence=0.9,
                        source='name_dictionary_clean',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern)
        
        # Check surnames
        for word in words:
            if word in self.name_dictionaries[language]['surnames']:
                pattern = NamePattern(
                    pattern=word,
                    pattern_type='dictionary_surname',
                    language=language,
                    confidence=0.95,
                    source='surname_dictionary',
                    created_at=datetime.now().isoformat()
                )
                patterns.append(pattern)
            
            # Clean compound surnames
            if "'" in word or "-" in word:
                clean_word = re.sub(r'[\'-]', '', word)
                if clean_word in self.name_dictionaries[language]['surnames']:
                    pattern = NamePattern(
                        pattern=clean_word,
                        pattern_type='dictionary_surname_clean',
                        language=language,
                        confidence=0.9,
                        source='surname_dictionary_clean',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _extract_position_patterns(self, text: str, language: str) -> List[NamePattern]:
        """Extract patterns by position (3-4 word)"""
        patterns = []
        
        words = text.strip().split()
        
        # 3-4 word potentially could be name + surname
        for i in range(2, min(4, len(words))):
            if i < len(words):
                # Check if it looks like name + surname
                potential_name = words[i]
                if self._looks_like_name(potential_name, language):
                    pattern = NamePattern(
                        pattern=potential_name,
                        pattern_type='position_based',
                        language=language,
                        confidence=0.6,
                        source='position_analysis',
                        created_at=datetime.now().isoformat()
                    )
                    patterns.append(pattern)
        
        return patterns
    
    def _looks_like_name(self, word: str, language: str) -> bool:
        """Check if word looks like a name"""
        if not word or len(word) < 2:
            return False
        
        # Basic rules
        if language in ['ru', 'uk']:
            # Cyrillic: first letter uppercase, rest lowercase
            return bool(re.match(r'^[А-ЯІЇЄ][а-яіїє]+$', word))
        else:
            # Latin: first letter uppercase, rest lowercase
            return bool(re.match(r'^[A-Z][a-z]+$', word))
    
    def _looks_like_surname(self, word: str, language: str) -> bool:
        """Check if word looks like a surname"""
        if not word or len(word) < 3:
            return False
        
        # Surnames are usually longer than names
        if len(word) < 4:
            return False
        
        # Same rules as for names
        return self._looks_like_name(word, language)
    
    def _detect_language_simple(self, text: str) -> str:
        """Simple language detection by characters"""
        cyrillic_chars = len(re.findall(r'[а-яіїєА-ЯІЇЄ]', text))
        latin_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if cyrillic_chars > 0:
            # Determine Ukrainian vs Russian by specific letters
            ukrainian_specific = len(re.findall(r'[іїєґІЇЄҐ]', text))
            if ukrainian_specific > 0:
                return 'uk'
            else:
                return 'ru'
        elif latin_chars > 0:
            return 'en'
        else:
            return 'en'  # Default to English
    
    def get_pattern_statistics(self, patterns: List[NamePattern]) -> Dict[str, Any]:
        """Get pattern statistics"""
        if not patterns:
            return {
                'total_patterns': 0,
                'by_type': {},
                'by_language': {},
                'by_source': {}
            }
        
        stats = {
            'total_patterns': len(patterns),
            'by_type': {},
            'by_language': {},
            'by_source': {}
        }
        
        # By type
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            stats['by_type'][pattern_type] = stats['by_type'].get(pattern_type, 0) + 1
        
        # By language
        for pattern in patterns:
            language = pattern.language
            stats['by_language'][language] = stats['by_language'].get(language, 0) + 1
        
        # By source
        for pattern in patterns:
            source = pattern.source
            stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
        
        return stats
