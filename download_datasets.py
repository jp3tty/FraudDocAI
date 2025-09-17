#!/usr/bin/env python3
"""
FraudDocAI Dataset Downloader
Downloads and prepares real-world datasets for fraud detection testing
"""

import os
import requests
import zipfile
import json
import pandas as pd
from typing import Dict, List, Any
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetDownloader:
    """Download and prepare datasets for FraudDocAI testing"""
    
    def __init__(self):
        self.datasets_dir = "datasets"
        self.processed_dir = "processed_datasets"
        os.makedirs(self.datasets_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        # Dataset URLs and information
        self.datasets = {
            "credit_card_fraud": {
                "url": "https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud/download",
                "filename": "creditcard.csv",
                "description": "Credit card fraud detection dataset",
                "size": "284,807 transactions (492 fraudulent)",
                "use_case": "Transaction fraud patterns"
            },
            "synthetic_financial": {
                "url": "https://github.com/AnalystHarpal007/Synthetic-Financial-Datasets-For-Fraud-Detection/archive/refs/heads/main.zip",
                "filename": "synthetic_financial.zip",
                "description": "Synthetic financial fraud datasets",
                "use_case": "Safe testing without privacy concerns"
            }
        }
    
    def download_kaggle_dataset(self, dataset_name: str) -> bool:
        """Download dataset from Kaggle (requires kaggle API)"""
        try:
            import kaggle
            logger.info(f"Downloading {dataset_name} from Kaggle...")
            
            if dataset_name == "credit_card_fraud":
                kaggle.api.dataset_download_files(
                    'mlg-ulb/creditcardfraud',
                    path=self.datasets_dir,
                    unzip=True
                )
                logger.info("✅ Credit card fraud dataset downloaded successfully")
                return True
                
        except ImportError:
            logger.error("❌ Kaggle API not installed. Install with: pip install kaggle")
            return False
        except Exception as e:
            logger.error(f"❌ Error downloading {dataset_name}: {e}")
            return False
    
    def download_github_dataset(self, repo_url: str, filename: str) -> bool:
        """Download dataset from GitHub repository"""
        try:
            logger.info(f"Downloading {filename} from GitHub...")
            
            # For GitHub, we'll create a simple download script
            # In practice, you'd clone the repo or download specific files
            logger.info("📝 To download GitHub datasets:")
            logger.info(f"   1. Clone: git clone {repo_url}")
            logger.info(f"   2. Copy relevant files to {self.datasets_dir}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error downloading {filename}: {e}")
            return False
    
    def process_credit_card_data(self) -> Dict[str, Any]:
        """Process credit card fraud dataset for document testing"""
        try:
            csv_path = os.path.join(self.datasets_dir, "creditcard.csv")
            if not os.path.exists(csv_path):
                logger.error("❌ Credit card dataset not found. Please download it first.")
                return {}
            
            logger.info("Processing credit card fraud dataset...")
            df = pd.read_csv(csv_path)
            
            # Create document-like representations of transactions
            documents = []
            
            # Sample some fraudulent transactions
            fraud_df = df[df['Class'] == 1].head(50)
            legitimate_df = df[df['Class'] == 0].head(50)
            
            for idx, row in fraud_df.iterrows():
                # Create a document representation of a fraudulent transaction
                doc = f"""TRANSACTION RECORD - FRAUDULENT
Amount: ${row['Amount']:.2f}
Time: {row['Time']} seconds
Transaction Type: Suspicious Activity
Risk Level: HIGH
Fraud Indicators: Multiple unusual patterns detected
Confidential - Internal Use Only"""
                
                documents.append({
                    "content": doc,
                    "fraud_score": 0.8,
                    "risk_level": "high",
                    "source": "credit_card_fraud",
                    "original_amount": row['Amount']
                })
            
            for idx, row in legitimate_df.iterrows():
                # Create a document representation of a legitimate transaction
                doc = f"""TRANSACTION RECORD - LEGITIMATE
Amount: ${row['Amount']:.2f}
Time: {row['Time']} seconds
Transaction Type: Normal Activity
Risk Level: LOW
Status: Approved
Standard Processing"""
                
                documents.append({
                    "content": doc,
                    "fraud_score": 0.1,
                    "risk_level": "low",
                    "source": "credit_card_fraud",
                    "original_amount": row['Amount']
                })
            
            # Save processed documents
            output_file = os.path.join(self.processed_dir, "credit_card_documents.json")
            with open(output_file, 'w') as f:
                json.dump(documents, f, indent=2)
            
            logger.info(f"✅ Processed {len(documents)} documents from credit card dataset")
            return {"documents": documents, "output_file": output_file}
            
        except Exception as e:
            logger.error(f"❌ Error processing credit card data: {e}")
            return {}
    
    def create_financial_document_templates(self) -> Dict[str, List[str]]:
        """Create templates for various financial documents"""
        templates = {
            "wire_transfer_requests": [
                "URGENT: Wire transfer of ${amount} to account {account}",
                "IMMEDIATE: Please process wire transfer for ${amount}",
                "CRITICAL: Emergency wire transfer needed - ${amount}"
            ],
            "invoice_documents": [
                "INVOICE #{invoice_num}\nAmount: ${amount}\nDue: {due_date}",
                "BILLING STATEMENT\nTotal Due: ${amount}\nPayment Terms: {terms}",
                "PAYMENT REQUEST\nAmount: ${amount}\nAccount: {account}"
            ],
            "bank_statements": [
                "BANK STATEMENT\nAccount: {account}\nBalance: ${amount}",
                "ACCOUNT SUMMARY\nCurrent Balance: ${amount}\nLast Transaction: {date}",
                "FINANCIAL STATEMENT\nTotal Assets: ${amount}\nLiabilities: ${liabilities}"
            ],
            "loan_applications": [
                "LOAN APPLICATION\nRequested Amount: ${amount}\nPurpose: {purpose}",
                "CREDIT REQUEST\nAmount: ${amount}\nTerm: {term} months",
                "FINANCING APPLICATION\nLoan Amount: ${amount}\nCollateral: {collateral}"
            ]
        }
        
        return templates
    
    def generate_document_variations(self, templates: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Generate document variations with different fraud levels"""
        import random
        from datetime import datetime, timedelta
        
        documents = []
        
        # High fraud risk documents
        for i in range(20):
            template = random.choice(templates["wire_transfer_requests"])
            amount = random.randint(10000, 100000)
            account = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            
            content = template.format(amount=amount, account=account)
            
            # Add fraud indicators
            fraud_indicators = [
                "URGENT", "IMMEDIATE", "CONFIDENTIAL", "OFFSHORE", "EMERGENCY"
            ]
            
            for indicator in random.sample(fraud_indicators, random.randint(2, 4)):
                content += f"\n{indicator}"
            
            documents.append({
                "content": content,
                "fraud_score": random.uniform(0.7, 0.9),
                "risk_level": "high",
                "document_type": "wire_transfer_request",
                "fraud_indicators": fraud_indicators[:random.randint(2, 4)]
            })
        
        # Medium fraud risk documents
        for i in range(20):
            template = random.choice(templates["invoice_documents"])
            amount = random.randint(1000, 10000)
            invoice_num = f"INV-{random.randint(1000, 9999)}"
            due_date = (datetime.now() + timedelta(days=random.randint(1, 7))).strftime("%Y-%m-%d")
            
            content = template.format(
                amount=amount, 
                invoice_num=invoice_num, 
                due_date=due_date,
                terms="Net 15",
                account=random.randint(1000000000, 9999999999)
            )
            
            # Add some suspicious elements
            if random.random() > 0.5:
                content += "\nWire transfer preferred"
            if random.random() > 0.7:
                content += "\nConfidential transaction"
            
            documents.append({
                "content": content,
                "fraud_score": random.uniform(0.3, 0.6),
                "risk_level": "medium",
                "document_type": "invoice",
                "fraud_indicators": ["wire transfer preferred"] if "wire transfer" in content else []
            })
        
        # Low fraud risk documents
        for i in range(20):
            template = random.choice(templates["invoice_documents"])
            amount = random.randint(100, 2000)
            invoice_num = f"LEG-{random.randint(1000, 9999)}"
            due_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            
            content = template.format(
                amount=amount,
                invoice_num=invoice_num,
                due_date=due_date,
                terms="Net 30",
                account=random.randint(1000000000, 9999999999)
            )
            
            # Add legitimate elements
            content += "\nPayment methods: Check, ACH, Credit Card"
            content += "\nThank you for your business!"
            
            documents.append({
                "content": content,
                "fraud_score": random.uniform(0.0, 0.2),
                "risk_level": "low",
                "document_type": "invoice",
                "fraud_indicators": []
            })
        
        return documents
    
    def save_documents_to_files(self, documents: List[Dict[str, Any]]) -> None:
        """Save documents to individual text files"""
        for i, doc in enumerate(documents):
            filename = f"{doc['risk_level']}_{doc['document_type']}_{i+1}.txt"
            filepath = os.path.join(self.processed_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(doc['content'])
            
            # Save metadata
            metadata_file = filepath.replace('.txt', '_metadata.json')
            with open(metadata_file, 'w') as f:
                json.dump({
                    "fraud_score": doc['fraud_score'],
                    "risk_level": doc['risk_level'],
                    "document_type": doc['document_type'],
                    "fraud_indicators": doc['fraud_indicators']
                }, f, indent=2)
    
    def run_dataset_preparation(self):
        """Run the complete dataset preparation process"""
        logger.info("🚀 Starting FraudDocAI Dataset Preparation")
        logger.info("=" * 50)
        
        # Create document templates
        templates = self.create_financial_document_templates()
        
        # Generate document variations
        documents = self.generate_document_variations(templates)
        
        # Save documents to files
        self.save_documents_to_files(documents)
        
        # Save summary
        summary = {
            "total_documents": len(documents),
            "high_risk": len([d for d in documents if d['risk_level'] == 'high']),
            "medium_risk": len([d for d in documents if d['risk_level'] == 'medium']),
            "low_risk": len([d for d in documents if d['risk_level'] == 'low']),
            "generated_at": datetime.now().isoformat()
        }
        
        summary_file = os.path.join(self.processed_dir, "dataset_summary.json")
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✅ Dataset preparation complete!")
        logger.info(f"📁 Output directory: {self.processed_dir}")
        logger.info(f"📊 Total documents: {summary['total_documents']}")
        logger.info(f"🔴 High risk: {summary['high_risk']}")
        logger.info(f"🟡 Medium risk: {summary['medium_risk']}")
        logger.info(f"🟢 Low risk: {summary['low_risk']}")
        
        return documents

def main():
    """Main function to run dataset preparation"""
    downloader = DatasetDownloader()
    
    print("🎯 FraudDocAI Dataset Preparation")
    print("=" * 40)
    print("1. Generate synthetic test documents")
    print("2. Download real-world datasets (requires setup)")
    print("3. Process and prepare all datasets")
    
    # For now, just generate synthetic documents
    documents = downloader.run_dataset_preparation()
    
    print("\n📋 Next Steps:")
    print("1. Copy generated documents to your test directory")
    print("2. Test with your FraudDocAI system")
    print("3. Validate fraud detection accuracy")
    print("4. Use for comprehensive system testing")

if __name__ == "__main__":
    main()
