# Customer Data Loader
# Handles loading and managing customer privacy settings

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class CustomerDataLoader:
    """Load and manage customer privacy configuration data"""
    
    def __init__(self, data_file="customers.json"):
        self.data_file = data_file
        self.customers = {}
        self.load_customer_data()
    
    def load_customer_data(self):
        """Load customer data from JSON file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for customer in data.get('customers', []):
                        self.customers[customer['customer_id']] = customer
                print(f"Loaded {len(self.customers)} customer profiles")
            else:
                print(f"Warning: Customer data file {self.data_file} not found")
                self.customers = {}
        except Exception as e:
            print(f"Error loading customer data: {e}")
            self.customers = {}
    
    def get_customer(self, customer_id: str) -> Optional[Dict]:
        """Get customer data by ID"""
        return self.customers.get(customer_id)
    
    def get_all_customers(self) -> List[Dict]:
        """Get all customer data"""
        return list(self.customers.values())
    
    def get_customers_by_privacy_level(self, privacy_level: str) -> List[Dict]:
        """Get customers filtered by privacy level"""
        return [customer for customer in self.customers.values() 
                if customer.get('privacy_level') == privacy_level]
    
    def get_customers_with_service(self, service_name: str) -> List[Dict]:
        """Get customers who have a specific service enabled"""
        return [customer for customer in self.customers.values() 
                if customer.get(service_name, False)]
    
    def update_customer(self, customer_id: str, updates: Dict):
        """Update customer data"""
        if customer_id in self.customers:
            self.customers[customer_id].update(updates)
            self.save_customer_data()
    
    def save_customer_data(self):
        """Save customer data back to file"""
        try:
            data = {"customers": list(self.customers.values())}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving customer data: {e}")
    
    def get_customer_preferences(self, customer_id: str) -> Dict:
        """Get customer privacy preferences in a standardized format"""
        customer = self.get_customer(customer_id)
        if not customer:
            return {}
        
        return {
            'privacy_level': customer.get('privacy_level', 'medium'),
            'location_obfuscation': customer.get('location_obfuscation', True),
            'identity_count': customer.get('identity_multiplication_count', 25),
            'device_types': customer.get('device_types', ['smartphone']),
            'preferred_cities': customer.get('preferred_cities', ['New York', 'Los Angeles']),
            'encryption_enabled': customer.get('communication_encryption', True),
            'biometric_protection': customer.get('biometric_protection', True),
            'service_tier': customer.get('service_tier', 'standard')
        }

# Example usage
if __name__ == "__main__":
    loader = CustomerDataLoader()
    
    # Test customer data loading
    print("=== Customer Data Loader Demo ===")
    
    # Get a specific customer
    customer = loader.get_customer("CUST_001")
    if customer:
        print(f"Customer: {customer['name']} ({customer['customer_id']})")
        print(f"Privacy Level: {customer['privacy_level']}")
    
    # Get customers by privacy level
    high_privacy_customers = loader.get_customers_by_privacy_level("high")
    print(f"\nHigh privacy customers: {len(high_privacy_customers)}")
    
    # Get customers with specific services
    encrypted_comm_customers = loader.get_customers_with_service("communication_encryption")
    print(f"Customers with encrypted communication: {len(encrypted_comm_customers)}")
    
    # Get preferences for a customer
    prefs = loader.get_customer_preferences("CUST_003")
    print(f"\nCustomer CUST_003 preferences: {prefs}")