# Identity Multiplication System
# Create multiple false digital identities for privacy based on customer preferences

import random
import hashlib
import string
from datetime import datetime, timedelta
from typing import Dict, List
from customer_loader import CustomerDataLoader

class IdentityMultiplier:
    """Create multiple false digital identities for privacy protection"""
    
    def __init__(self, customer_loader: CustomerDataLoader = None):
        self.customer_loader = customer_loader or CustomerDataLoader()
        
        # Name pools for generating identities
        self.first_names = {
            'common': ['Alex', 'Jordan', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Avery', 'Quinn'],
            'traditional': ['John', 'Mary', 'James', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda'],
            'modern': ['Aiden', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Ethan', 'Sophia'],
            'international': ['Ahmed', 'Priya', 'Chen', 'Maria', 'Dimitri', 'Yuki', 'Hassan', 'Elena']
        }
        
        self.last_names = {
            'common': ['Smith', 'Johnson', 'Williams', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore'],
            'regional': ['Anderson', 'Taylor', 'Thomas', 'Jackson', 'White', 'Harris', 'Martin', 'Thompson'],
            'international': ['Rodriguez', 'Martinez', 'Garcia', 'Kumar', 'Chen', 'Kim', 'Patel', 'Singh']
        }
        
        # Email domains
        self.email_domains = {
            'secure': ['securemail.com', 'privatenet.org', 'shieldmail.net', 'anonmail.com', 'cryptomail.io'],
            'common': ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com'],
            'business': ['company.com', 'corp.net', 'business.org', 'enterprise.co', 'firm.io']
        }
        
        # Profile characteristics
        self.interests = [
            'technology', 'sports', 'music', 'travel', 'cooking', 'reading', 'photography',
            'gaming', 'fitness', 'art', 'science', 'movies', 'nature', 'fashion', 'education'
        ]
        
        self.occupations = [
            'Software Engineer', 'Teacher', 'Designer', 'Manager', 'Consultant', 'Analyst',
            'Developer', 'Coordinator', 'Specialist', 'Administrator', 'Technician', 'Director'
        ]
    
    def get_name_style(self, customer_id: str) -> str:
        """Determine name style based on customer preferences"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        # Use service tier to influence name style
        service_tier = customer_prefs.get('service_tier', 'standard')
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        
        if service_tier == 'enterprise' or privacy_level == 'maximum':
            return 'international'  # More diverse names for higher security
        elif service_tier == 'premium' or privacy_level == 'high':
            return 'modern'
        else:
            return 'common'
    
    def generate_identity_name(self, style: str = 'common') -> Dict[str, str]:
        """Generate a realistic name based on style"""
        first_name = random.choice(self.first_names.get(style, self.first_names['common']))
        last_name = random.choice(self.last_names.get(style, self.last_names['common']))
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'full_name': f"{first_name} {last_name}"
        }
    
    def generate_email_address(self, name_data: Dict, customer_id: str) -> str:
        """Generate email address based on customer preferences"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        # Choose domain type based on customer preferences
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        if privacy_level in ['high', 'maximum']:
            domain_type = 'secure'
        elif customer_prefs.get('service_tier') == 'enterprise':
            domain_type = 'business'
        else:
            domain_type = 'common'
        
        domain = random.choice(self.email_domains[domain_type])
        
        # Generate email variants
        first = name_data['first_name'].lower()
        last = name_data['last_name'].lower()
        
        email_patterns = [
            f"{first}.{last}",
            f"{first}{last}",
            f"{first}_{last}",
            f"{first[0]}{last}",
            f"{first}.{last[0]}",
            f"{first}{random.randint(1, 999)}"
        ]
        
        email_base = random.choice(email_patterns)
        return f"{email_base}@{domain}"
    
    def generate_social_media_handles(self, name_data: Dict) -> Dict[str, str]:
        """Generate social media handles"""
        first = name_data['first_name'].lower()
        last = name_data['last_name'].lower()
        
        handle_patterns = [
            f"{first}_{last}",
            f"{first}{last}",
            f"{first}{random.randint(10, 99)}",
            f"{first}_{random.randint(100, 999)}",
            f"{last}_{first}",
            f"{first[0]}{last}{random.randint(1, 99)}"
        ]
        
        platforms = ['twitter', 'instagram', 'linkedin', 'facebook', 'tiktok']
        handles = {}
        
        for platform in platforms:
            if random.random() < 0.7:  # 70% chance of having each platform
                handles[platform] = random.choice(handle_patterns)
        
        return handles
    
    def generate_false_identities_for_customer(self, customer_id: str) -> List[Dict]:
        """Generate multiple false identities customized for specific customer"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs:
            print(f"Customer {customer_id} not found, using default settings")
            return self.generate_false_identities(25)
        
        count = customer_prefs.get('identity_count', 25)
        name_style = self.get_name_style(customer_id)
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        
        return self.generate_false_identities(count, customer_id, name_style, privacy_level)
    
    def generate_false_identities(self, count: int = 100, customer_id: str = None, 
                                 name_style: str = 'common', privacy_level: str = 'medium') -> List[Dict]:
        """Generate multiple false digital identities"""
        identities = []
        
        # Determine identity complexity based on privacy level
        complexity_mapping = {
            'low': 'basic',
            'medium': 'standard',
            'high': 'detailed',
            'maximum': 'comprehensive'
        }
        complexity = complexity_mapping.get(privacy_level, 'standard')
        
        for i in range(count):
            # Generate base identity
            name_data = self.generate_identity_name(name_style)
            email = self.generate_email_address(name_data, customer_id) if customer_id else self.generate_email_address(name_data, 'default')
            
            # Base identity structure
            identity = {
                'identity_id': f"ID_{random.randint(100000, 999999)}",
                'customer_id': customer_id,
                'name': name_data,
                'email': email,
                'created_date': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                'activity_score': random.uniform(0.1, 1.0),
                'digital_fingerprint': hashlib.sha256(f"{name_data['full_name']}{email}{i}".encode()).hexdigest()[:16],
                'complexity_level': complexity
            }
            
            # Add details based on complexity level
            if complexity in ['standard', 'detailed', 'comprehensive']:
                identity.update({
                    'phone': self.generate_phone_number(),
                    'birth_year': random.randint(1970, 2005),
                    'interests': random.sample(self.interests, k=random.randint(2, 5)),
                    'social_media': self.generate_social_media_handles(name_data)
                })
            
            if complexity in ['detailed', 'comprehensive']:
                identity.update({
                    'occupation': random.choice(self.occupations),
                    'education_level': random.choice(['High School', 'Bachelor\'s', 'Master\'s', 'PhD']),
                    'location_history': self.generate_location_history(),
                    'device_preferences': self.generate_device_preferences(),
                    'online_behavior': self.generate_online_behavior_profile()
                })
            
            if complexity == 'comprehensive':
                identity.update({
                    'financial_profile': self.generate_financial_profile(),
                    'health_data': self.generate_health_profile(),
                    'travel_patterns': self.generate_travel_patterns(),
                    'purchase_history': self.generate_purchase_history(),
                    'network_connections': self.generate_network_connections(i)
                })
            
            identities.append(identity)
        
        return identities
    
    def generate_phone_number(self) -> str:
        """Generate a realistic phone number"""
        area_codes = ['212', '213', '312', '415', '617', '713', '202', '305', '404', '503']
        area_code = random.choice(area_codes)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"+1-{area_code}-{exchange}-{number}"
    
    def generate_location_history(self) -> List[Dict]:
        """Generate location history for identity"""
        locations = []
        for i in range(random.randint(2, 5)):
            location = {
                'city': random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                'duration_months': random.randint(6, 36),
                'purpose': random.choice(['work', 'education', 'family', 'personal'])
            }
            locations.append(location)
        return locations
    
    def generate_device_preferences(self) -> Dict:
        """Generate device and technology preferences"""
        return {
            'primary_device': random.choice(['iPhone', 'Android', 'Windows Phone']),
            'operating_system': random.choice(['iOS', 'Android', 'Windows', 'macOS', 'Linux']),
            'browser': random.choice(['Chrome', 'Firefox', 'Safari', 'Edge']),
            'tech_savviness': random.choice(['beginner', 'intermediate', 'advanced', 'expert'])
        }
    
    def generate_online_behavior_profile(self) -> Dict:
        """Generate online behavior patterns"""
        return {
            'daily_screen_time': random.uniform(2.0, 12.0),
            'preferred_communication': random.choice(['email', 'text', 'social_media', 'voice']),
            'shopping_frequency': random.choice(['rarely', 'occasionally', 'regularly', 'frequently']),
            'social_media_activity': random.choice(['lurker', 'occasional_poster', 'active', 'influencer']),
            'privacy_consciousness': random.choice(['low', 'medium', 'high', 'paranoid'])
        }
    
    def generate_financial_profile(self) -> Dict:
        """Generate financial behavior profile"""
        return {
            'income_bracket': random.choice(['low', 'medium', 'high', 'very_high']),
            'spending_pattern': random.choice(['conservative', 'moderate', 'liberal', 'impulsive']),
            'investment_interest': random.choice(['none', 'basic', 'moderate', 'advanced']),
            'credit_usage': random.choice(['minimal', 'moderate', 'heavy'])
        }
    
    def generate_health_profile(self) -> Dict:
        """Generate health and fitness profile"""
        return {
            'fitness_level': random.choice(['sedentary', 'lightly_active', 'moderately_active', 'very_active']),
            'health_consciousness': random.choice(['low', 'medium', 'high']),
            'medical_conditions': random.choice(['none', 'minor', 'managed', 'multiple']),
            'wellness_tracking': random.choice(['none', 'basic', 'comprehensive'])
        }
    
    def generate_travel_patterns(self) -> Dict:
        """Generate travel behavior patterns"""
        return {
            'travel_frequency': random.choice(['never', 'rarely', 'occasionally', 'frequently']),
            'preferred_destinations': random.choice(['domestic', 'international', 'both']),
            'travel_style': random.choice(['budget', 'mid-range', 'luxury']),
            'business_travel': random.choice([True, False])
        }
    
    def generate_purchase_history(self) -> List[Dict]:
        """Generate purchase history patterns"""
        categories = ['electronics', 'clothing', 'food', 'entertainment', 'travel', 'books', 'health']
        purchases = []
        
        for category in random.sample(categories, k=random.randint(3, 6)):
            purchase = {
                'category': category,
                'frequency': random.choice(['monthly', 'quarterly', 'yearly', 'rarely']),
                'average_amount': random.uniform(20.0, 500.0),
                'preferred_method': random.choice(['online', 'in_store', 'both'])
            }
            purchases.append(purchase)
        
        return purchases
    
    def generate_network_connections(self, identity_index: int) -> Dict:
        """Generate social network connection patterns"""
        return {
            'connection_count': random.randint(50, 500),
            'network_density': random.uniform(0.1, 0.8),
            'primary_groups': random.sample(['family', 'work', 'school', 'hobby', 'neighborhood'], k=random.randint(2, 4)),
            'influence_score': random.uniform(0.1, 1.0),
            'cross_platform_consistency': random.uniform(0.3, 0.9)
        }
    
    def generate_identity_lifecycle_events(self, identity: Dict) -> List[Dict]:
        """Generate lifecycle events for an identity"""
        events = []
        
        # Account creation events
        events.append({
            'event_type': 'account_creation',
            'timestamp': identity['created_date'],
            'platform': 'primary_email',
            'details': {'verification_method': 'email'}
        })
        
        # Random lifecycle events
        event_types = ['password_change', 'profile_update', 'privacy_setting_change', 
                      'device_addition', 'location_change', 'activity_spike']
        
        num_events = random.randint(5, 15)
        for i in range(num_events):
            event_date = datetime.now() - timedelta(days=random.randint(1, 300))
            event = {
                'event_type': random.choice(event_types),
                'timestamp': event_date.isoformat(),
                'platform': random.choice(['email', 'social_media', 'banking', 'shopping', 'work']),
                'details': {'automated': True, 'risk_score': random.uniform(0.1, 0.5)}
            }
            events.append(event)
        
        return sorted(events, key=lambda x: x['timestamp'])

# Example usage and testing
def demo_identity_multiplication():
    """Demonstrate the identity multiplication system with customer data"""
    print("=== Identity Multiplication System Demo ===")
    
    # Initialize system
    multiplier = IdentityMultiplier()
    
    # Test with specific customers
    customers_to_test = ["CUST_001", "CUST_003", "CUST_005"]
    
    for customer_id in customers_to_test:
        print(f"\n--- Customer {customer_id} ---")
        
        # Generate identities for customer
        identities = multiplier.generate_false_identities_for_customer(customer_id)
        
        print(f"Generated {len(identities)} false identities")
        print(f"Sample identity: {identities[0]['name']['full_name']} ({identities[0]['email']})")
        print(f"Complexity level: {identities[0]['complexity_level']}")
        
        # Show additional details for high-complexity identities
        if identities[0]['complexity_level'] in ['detailed', 'comprehensive']:
            sample = identities[0]
            print(f"Occupation: {sample.get('occupation', 'N/A')}")
            print(f"Interests: {', '.join(sample.get('interests', []))}")
            print(f"Social media platforms: {len(sample.get('social_media', {}))}")
        
        # Generate lifecycle events for sample identity
        lifecycle_events = multiplier.generate_identity_lifecycle_events(identities[0])
        print(f"Generated {len(lifecycle_events)} lifecycle events")

if __name__ == "__main__":
    demo_identity_multiplication()