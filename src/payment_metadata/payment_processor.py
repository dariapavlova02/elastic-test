"""
Payment metadata processor for vector testing.
"""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class PaymentProcessor:
    """Processes payment metadata for vector testing."""
    
    def __init__(self):
        """Initialize payment processor."""
        pass
    
    def create_payment_document(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a standardized payment document for Elasticsearch.
        
        Args:
            payment_data: Raw payment data
            
        Returns:
            Standardized payment document
        """
        try:
            # Generate unique payment ID if not provided
            payment_id = payment_data.get('payment_id', str(uuid.uuid4()))
            
            # Create standardized document
            document = {
                "payment_id": payment_id,
                "amount": float(payment_data.get('amount', 0.0)),
                "currency": payment_data.get('currency', 'USD'),
                "sender": payment_data.get('sender', ''),
                "receiver": payment_data.get('receiver', ''),
                "description": payment_data.get('description', ''),
                "timestamp": self._parse_timestamp(payment_data.get('timestamp')),
                "metadata": {
                    "bank_code": payment_data.get('bank_code', ''),
                    "transaction_type": payment_data.get('transaction_type', 'transfer'),
                    "country": payment_data.get('country', ''),
                    "risk_score": float(payment_data.get('risk_score', 0.0)),
                    "original_data": payment_data
                },
                "sanctions_match": False,
                "sanctions_entities": []
            }
            
            return document
        except Exception as e:
            logger.error(f"Failed to create payment document: {e}")
            raise
    
    def _parse_timestamp(self, timestamp: Any) -> str:
        """Parse timestamp to ISO format."""
        try:
            if timestamp is None:
                return datetime.now().isoformat()
            
            if isinstance(timestamp, str):
                # Try to parse various timestamp formats
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    return dt.isoformat()
                except ValueError:
                    pass
                
                # Try other common formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S']:
                    try:
                        dt = datetime.strptime(timestamp, fmt)
                        return dt.isoformat()
                    except ValueError:
                        continue
            
            elif isinstance(timestamp, (int, float)):
                # Unix timestamp
                dt = datetime.fromtimestamp(timestamp)
                return dt.isoformat()
            
            return datetime.now().isoformat()
        except Exception as e:
            logger.warning(f"Failed to parse timestamp {timestamp}: {e}")
            return datetime.now().isoformat()
    
    def add_sanctions_match(self, payment_document: Dict[str, Any], 
                           sanctions_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Add sanctions match information to payment document.
        
        Args:
            payment_document: Payment document
            sanctions_matches: List of sanctions matches
            
        Returns:
            Updated payment document
        """
        try:
            # Update sanctions match flag
            payment_document['sanctions_match'] = len(sanctions_matches) > 0
            
            # Add sanctions entities
            sanctions_entities = []
            for match in sanctions_matches:
                entity = match.get('entity', {})
                sanctions_entities.append({
                    "entity_id": entity.get('id', ''),
                    "entity_name": entity.get('name', ''),
                    "entity_type": entity.get('entity_type', ''),
                    "similarity_score": match.get('similarity_score', 0.0),
                    "match_rank": match.get('match_rank', 0)
                })
            
            payment_document['sanctions_entities'] = sanctions_entities
            
            return payment_document
        except Exception as e:
            logger.error(f"Failed to add sanctions match: {e}")
            return payment_document
    
    def validate_payment_data(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate payment data.
        
        Args:
            payment_data: Payment data to validate
            
        Returns:
            Validation result
        """
        errors = []
        warnings = []
        
        # Required fields
        required_fields = ['sender', 'receiver', 'amount']
        for field in required_fields:
            if field not in payment_data or not payment_data[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate amount
        if 'amount' in payment_data:
            try:
                amount = float(payment_data['amount'])
                if amount < 0:
                    errors.append("Amount cannot be negative")
                elif amount == 0:
                    warnings.append("Amount is zero")
            except (ValueError, TypeError):
                errors.append("Invalid amount format")
        
        # Validate currency
        if 'currency' in payment_data:
            currency = payment_data['currency']
            if not isinstance(currency, str) or len(currency) != 3:
                warnings.append("Currency should be 3-letter code")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    def process_payment_batch(self, payments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of payments.
        
        Args:
            payments: List of payment data
            
        Returns:
            List of processed payment documents
        """
        processed_payments = []
        
        for i, payment_data in enumerate(payments):
            try:
                # Validate payment data
                validation = self.validate_payment_data(payment_data)
                if not validation['valid']:
                    logger.warning(f"Payment {i} validation failed: {validation['errors']}")
                    continue
                
                # Create payment document
                document = self.create_payment_document(payment_data)
                processed_payments.append(document)
                
            except Exception as e:
                logger.error(f"Failed to process payment {i}: {e}")
                continue
        
        logger.info(f"Processed {len(processed_payments)} out of {len(payments)} payments")
        return processed_payments
