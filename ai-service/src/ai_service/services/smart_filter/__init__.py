"""
Smart Filter Module

Умный предварительный фильтр для определения потенциальных имен и названий компаний
в тексте назначения платежа. Позволяет избежать избыточного поиска по Ахо-Корасик
для текстов, которые не содержат релевантных сигналов.
"""

from .smart_filter_service import SmartFilterService
from .company_detector import CompanyDetector
from .name_detector import NameDetector
from .confidence_scorer import ConfidenceScorer

__all__ = [
    'SmartFilterService',
    'CompanyDetector', 
    'NameDetector',
    'ConfidenceScorer'
]
