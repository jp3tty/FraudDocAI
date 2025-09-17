#!/usr/bin/env python3
"""
FraudDocAI Test Data Generator
Generates comprehensive test documents for fraud detection testing
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import os

class FraudDocTestDataGenerator:
    """Generate test documents for FraudDocAI system"""
    
    def __init__(self):
        self.output_dir = "test_documents_generated"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Fraud patterns and keywords
        self.fraud_keywords = [
            "urgent", "immediate", "confidential", "wire transfer", "bitcoin",
            "cryptocurrency", "offshore", "tax haven", "shell company",
            "forged", "fake", "duplicate", "altered", "tampered",
            "asap", "rush", "emergency", "critical", "expedite"
        ]
        
        self.legitimate_keywords = [
            "payment terms", "net 30", "invoice", "receipt", "statement",
            "professional services", "consulting", "contract", "agreement",
            "standard procedure", "normal processing", "regular payment"
        ]
        
        # Company names for realistic documents
        self.companies = [
            "Acme Corporation", "Global Solutions Inc", "Tech Innovations LLC",
            "Financial Services Group", "Business Partners Ltd", "Enterprise Systems",
            "Professional Consulting", "Strategic Advisors", "Market Leaders Inc"
        ]
        
        # Fraud scenarios
        self.fraud_scenarios = [
            "urgent_wire_transfer",
            "fake_invoice", 
            "duplicate_payment",
            "offshore_transfer",
            "cryptocurrency_scam",
            "phishing_invoice",
            "fake_contract",
            "forged_document"
        ]
    
    def generate_urgent_wire_transfer(self) -> str:
        """Generate urgent wire transfer scam document"""
        scenarios = [
            "URGENT: Please wire transfer ${amount} immediately to offshore account.\nThis is confidential and must be done ASAP!\nAccount: {account}\nRouting: {routing}\nConfidential - Do not share with anyone!",
            
            "IMMEDIATE ACTION REQUIRED\nWire transfer of ${amount} needed urgently.\nOffshore account details:\nAccount: {account}\nThis is a confidential business transaction.\nDo not discuss with anyone!",
            
            "CRITICAL: Emergency wire transfer needed\nAmount: ${amount}\nAccount: {account}\nRouting: {routing}\nThis is URGENT and CONFIDENTIAL!\nPlease process immediately!"
        ]
        
        template = random.choice(scenarios)
        amount = random.randint(10000, 100000)
        account = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        routing = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        
        return template.format(amount=amount, account=account, routing=routing)
    
    def generate_fake_invoice(self) -> str:
        """Generate fake invoice with fraud indicators"""
        invoice_num = f"FAKE-{random.randint(1000, 9999)}"
        amount = random.randint(5000, 50000)
        company = random.choice(self.companies)
        
        templates = [
            f"""INVOICE #{invoice_num}
Amount: ${amount}
Due: IMMEDIATELY
URGENT PAYMENT REQUIRED
Wire transfer only - no checks accepted
Offshore account details provided upon payment confirmation
CONFIDENTIAL BUSINESS TRANSACTION""",
            
            f"""INVOICE #{invoice_num}
{company}
Amount: ${amount}
Due: ASAP
URGENT: Payment must be made via wire transfer
This is a confidential transaction
Do not share with anyone
Offshore account: {''.join([str(random.randint(0, 9)) for _ in range(10)])}""",
            
            f"""FAKE INVOICE #{invoice_num}
Amount: ${amount}
URGENT PAYMENT REQUIRED
Wire transfer only
Confidential - Do not discuss
Account details upon confirmation
This is an emergency transaction"""
        ]
        
        return random.choice(templates)
    
    def generate_legitimate_invoice(self) -> str:
        """Generate legitimate business invoice"""
        invoice_num = f"LEG-{random.randint(1000, 9999)}"
        amount = random.randint(500, 5000)
        company = random.choice(self.companies)
        date = datetime.now().strftime("%B %d, %Y")
        due_date = (datetime.now() + timedelta(days=30)).strftime("%B %d, %Y")
        
        return f"""INVOICE #{invoice_num}
Date: {date}
Bill To: {company}
123 Business Street
Business City, BC 12345

Description: Professional Services
Amount: ${amount}.00
Due Date: {due_date}

Payment Terms: Net 30
Payment Methods: Check, ACH, Credit Card
Contact: accounts@{company.lower().replace(' ', '')}.com
Phone: (555) 123-4567

Thank you for your business!"""
    
    def generate_suspicious_invoice(self) -> str:
        """Generate suspicious invoice with some fraud indicators"""
        invoice_num = f"SUS-{random.randint(1000, 9999)}"
        amount = random.randint(2000, 15000)
        company = random.choice(self.companies)
        
        templates = [
            f"""Invoice #{invoice_num}
Services Rendered: Consulting
Amount: ${amount}
Payment Terms: Net 30
Please remit payment to:
Account: {''.join([str(random.randint(0, 9)) for _ in range(10)])}
Note: Payment must be made via wire transfer only""",
            
            f"""INVOICE #{invoice_num}
{company}
Amount: ${amount}
Due: Within 24 hours
Payment: Wire transfer preferred
Confidential business transaction
Please process immediately""",
            
            f"""Invoice #{invoice_num}
Amount: ${amount}
URGENT: Payment required
Wire transfer only
Account: {''.join([str(random.randint(0, 9)) for _ in range(10)])}
This is a confidential transaction"""
        ]
        
        return random.choice(templates)
    
    def generate_bank_statement(self, is_fraudulent: bool = False) -> str:
        """Generate bank statement (legitimate or fraudulent)"""
        account_num = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        date = datetime.now().strftime("%B %d, %Y")
        
        if is_fraudulent:
            return f"""BANK STATEMENT - CONFIDENTIAL
Account: {account_num}
Date: {date}

URGENT: Account requires immediate attention
Large withdrawal of $50,000 needed
Wire transfer to offshore account
This is confidential - do not share
Account details: {''.join([str(random.randint(0, 9)) for _ in range(10)])}
IMMEDIATE ACTION REQUIRED"""
        else:
            return f"""BANK STATEMENT
Account: {account_num}
Statement Period: {date}
Balance: ${random.randint(1000, 50000)}.00

Recent Transactions:
- Deposit: $2,500.00
- Withdrawal: $1,200.00
- Service Fee: $15.00

This statement is for your records.
Contact us at 1-800-BANK-123 for questions."""
    
    def generate_loan_application(self, is_fraudulent: bool = False) -> str:
        """Generate loan application document"""
        if is_fraudulent:
            return f"""LOAN APPLICATION - URGENT
Amount: $100,000
URGENT: Need immediate approval
Confidential business opportunity
Wire transfer to offshore account
This is an emergency
Do not share with anyone
Account: {''.join([str(random.randint(0, 9)) for _ in range(10)])}
IMMEDIATE PROCESSING REQUIRED"""
        else:
            return f"""LOAN APPLICATION
Amount: $25,000
Purpose: Business expansion
Company: {random.choice(self.companies)}
Contact: (555) 123-4567
Email: contact@{random.choice(self.companies).lower().replace(' ', '')}.com

This application is for legitimate business purposes.
Standard processing time: 5-7 business days."""
    
    def generate_test_documents(self, count_per_type: int = 5) -> Dict[str, List[str]]:
        """Generate comprehensive test document set"""
        documents = {
            "high_risk": [],
            "medium_risk": [],
            "low_risk": []
        }
        
        print(f"Generating {count_per_type} documents per risk level...")
        
        # High Risk Documents (Expected 60-80% fraud score)
        for i in range(count_per_type):
            doc_type = random.choice(["urgent_wire", "fake_invoice", "fraudulent_bank_statement", "fraudulent_loan"])
            
            if doc_type == "urgent_wire":
                content = self.generate_urgent_wire_transfer()
            elif doc_type == "fake_invoice":
                content = self.generate_fake_invoice()
            elif doc_type == "fraudulent_bank_statement":
                content = self.generate_bank_statement(is_fraudulent=True)
            else:  # fraudulent_loan
                content = self.generate_loan_application(is_fraudulent=True)
            
            filename = f"high_risk_{doc_type}_{i+1}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            documents["high_risk"].append({
                "filename": filename,
                "content": content,
                "expected_fraud_score": random.uniform(0.6, 0.8),
                "fraud_indicators": self._extract_fraud_indicators(content)
            })
        
        # Medium Risk Documents (Expected 30-50% fraud score)
        for i in range(count_per_type):
            content = self.generate_suspicious_invoice()
            filename = f"medium_risk_suspicious_invoice_{i+1}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            documents["medium_risk"].append({
                "filename": filename,
                "content": content,
                "expected_fraud_score": random.uniform(0.3, 0.5),
                "fraud_indicators": self._extract_fraud_indicators(content)
            })
        
        # Low Risk Documents (Expected 0-20% fraud score)
        for i in range(count_per_type):
            content = self.generate_legitimate_invoice()
            filename = f"low_risk_legitimate_invoice_{i+1}.txt"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            documents["low_risk"].append({
                "filename": filename,
                "content": content,
                "expected_fraud_score": random.uniform(0.0, 0.2),
                "fraud_indicators": self._extract_fraud_indicators(content)
            })
        
        return documents
    
    def _extract_fraud_indicators(self, content: str) -> List[str]:
        """Extract fraud indicators from document content"""
        indicators = []
        content_lower = content.lower()
        
        for keyword in self.fraud_keywords:
            if keyword in content_lower:
                indicators.append(keyword)
        
        return indicators
    
    def generate_test_metadata(self, documents: Dict[str, List[str]]) -> None:
        """Generate metadata file for test documents"""
        metadata = {
            "generated_at": datetime.now().isoformat(),
            "total_documents": sum(len(docs) for docs in documents.values()),
            "risk_levels": {
                "high_risk": {
                    "count": len(documents["high_risk"]),
                    "expected_fraud_score_range": "0.6-0.8",
                    "description": "Documents with clear fraud indicators"
                },
                "medium_risk": {
                    "count": len(documents["medium_risk"]),
                    "expected_fraud_score_range": "0.3-0.5",
                    "description": "Documents with suspicious patterns"
                },
                "low_risk": {
                    "count": len(documents["low_risk"]),
                    "expected_fraud_score_range": "0.0-0.2",
                    "description": "Legitimate business documents"
                }
            },
            "fraud_keywords_used": self.fraud_keywords,
            "legitimate_keywords_used": self.legitimate_keywords,
            "test_scenarios": self.fraud_scenarios
        }
        
        metadata_file = os.path.join(self.output_dir, "test_metadata.json")
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Test metadata saved to: {metadata_file}")
    
    def run_generation(self, count_per_type: int = 10):
        """Run the complete test data generation process"""
        print("🚀 Starting FraudDocAI Test Data Generation")
        print("=" * 50)
        
        # Generate documents
        documents = self.generate_test_documents(count_per_type)
        
        # Generate metadata
        self.generate_test_metadata(documents)
        
        # Print summary
        print(f"\n✅ Test data generation complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📊 Total documents generated: {sum(len(docs) for docs in documents.values())}")
        print(f"🔴 High risk documents: {len(documents['high_risk'])}")
        print(f"🟡 Medium risk documents: {len(documents['medium_risk'])}")
        print(f"🟢 Low risk documents: {len(documents['low_risk'])}")
        
        return documents

def main():
    """Main function to run test data generation"""
    generator = FraudDocTestDataGenerator()
    documents = generator.run_generation(count_per_type=10)
    
    print("\n🎯 Next Steps:")
    print("1. Copy generated documents to FraudDocAI/backend/test_documents/")
    print("2. Test with your fraud detection system")
    print("3. Validate fraud scores match expected ranges")
    print("4. Use for system testing and validation")

if __name__ == "__main__":
    main()
