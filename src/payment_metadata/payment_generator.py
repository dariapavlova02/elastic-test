"""
Payment data generator for testing purposes.
"""
import logging
import random
import uuid
from typing import List, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PaymentGenerator:
    """Generates test payment data for vector testing."""
    
    def __init__(self):
        """Initialize payment generator."""
        # Sample data for generating realistic payments
        self.senders = [
            "John Smith", "Maria Garcia", "Ahmed Hassan", "Li Wei", "Anna Kowalski",
            "Ivan Petrov", "Sarah Johnson", "Mohammed Ali", "Elena Rodriguez", "David Kim"
        ]
        
        self.receivers = [
            "ABC Corporation", "XYZ Ltd", "Global Trading Co", "Tech Solutions Inc",
            "International Bank", "Finance Group", "Investment Partners", "Trade House",
            "Business Services", "Financial Solutions"
        ]
        
        self.descriptions = [
            "Payment for services", "Invoice payment", "Salary transfer", "Business transaction",
            "International transfer", "Payment for goods", "Consulting fees", "Rent payment",
            "Investment transfer", "Refund processing"
        ]
        
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY"]
        
        self.countries = ["US", "UK", "DE", "FR", "IT", "ES", "CA", "AU", "JP", "CN"]
        
        self.bank_codes = ["001", "002", "003", "004", "005", "006", "007", "008", "009", "010"]
        
        self.transaction_types = ["transfer", "payment", "salary", "invoice", "refund", "investment"]
    
    def generate_payment(self, payment_id: str = None) -> Dict[str, Any]:
        """
        Generate a single test payment.
        
        Args:
            payment_id: Optional payment ID
            
        Returns:
            Generated payment data
        """
        try:
            # Generate random amounts
            amount = round(random.uniform(100, 10000), 2)
            
            # Generate random timestamp within last 30 days
            now = datetime.now()
            days_ago = random.randint(0, 30)
            timestamp = now - timedelta(days=days_ago)
            
            payment = {
                "payment_id": payment_id or str(uuid.uuid4()),
                "amount": amount,
                "currency": random.choice(self.currencies),
                "sender": random.choice(self.senders),
                "receiver": random.choice(self.receivers),
                "description": random.choice(self.descriptions),
                "timestamp": timestamp.isoformat(),
                "bank_code": random.choice(self.bank_codes),
                "transaction_type": random.choice(self.transaction_types),
                "country": random.choice(self.countries),
                "risk_score": round(random.uniform(0.0, 1.0), 3)
            }
            
            return payment
        except Exception as e:
            logger.error(f"Failed to generate payment: {e}")
            raise
    
    def generate_payment_batch(self, count: int) -> List[Dict[str, Any]]:
        """
        Generate a batch of test payments.
        
        Args:
            count: Number of payments to generate
            
        Returns:
            List of generated payments
        """
        try:
            payments = []
            for i in range(count):
                payment = self.generate_payment()
                payments.append(payment)
            
            logger.info(f"Generated {count} test payments")
            return payments
        except Exception as e:
            logger.error(f"Failed to generate payment batch: {e}")
            raise
    
    def generate_suspicious_payment(self, sanctions_entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a suspicious payment that might match sanctions.
        
        Args:
            sanctions_entities: List of sanctions entities to potentially match
            
        Returns:
            Suspicious payment data
        """
        try:
            # Start with a normal payment
            payment = self.generate_payment()
            
            # Randomly choose to make it suspicious
            if random.random() < 0.7:  # 70% chance of being suspicious
                # Use a name from sanctions list
                if sanctions_entities:
                    entity = random.choice(sanctions_entities)
                    if entity.get('entity_type') == 'person':
                        payment['sender'] = entity.get('name', payment['sender'])
                    elif entity.get('entity_type') == 'company':
                        payment['receiver'] = entity.get('name', payment['receiver'])
                
                # Add suspicious description
                suspicious_descriptions = [
                    "Urgent transfer", "Confidential payment", "Special transaction",
                    "High priority transfer", "Expedited payment", "Private transfer"
                ]
                payment['description'] = random.choice(suspicious_descriptions)
                
                # Increase risk score
                payment['risk_score'] = round(random.uniform(0.7, 1.0), 3)
            
            return payment
        except Exception as e:
            logger.error(f"Failed to generate suspicious payment: {e}")
            raise
    
    def generate_test_dataset(self, normal_count: int, suspicious_count: int, 
                            sanctions_entities: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Generate a test dataset with normal and suspicious payments.
        
        Args:
            normal_count: Number of normal payments
            suspicious_count: Number of suspicious payments
            sanctions_entities: List of sanctions entities for suspicious payments
            
        Returns:
            Test dataset
        """
        try:
            dataset = []
            
            # Generate normal payments
            normal_payments = self.generate_payment_batch(normal_count)
            dataset.extend(normal_payments)
            
            # Generate suspicious payments
            suspicious_payments = []
            for i in range(suspicious_count):
                suspicious_payment = self.generate_suspicious_payment(sanctions_entities or [])
                suspicious_payments.append(suspicious_payment)
            
            dataset.extend(suspicious_payments)
            
            # Shuffle the dataset
            random.shuffle(dataset)
            
            logger.info(f"Generated test dataset: {normal_count} normal, {suspicious_count} suspicious payments")
            return dataset
        except Exception as e:
            logger.error(f"Failed to generate test dataset: {e}")
            raise
