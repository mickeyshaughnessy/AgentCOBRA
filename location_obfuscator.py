# Location Obfuscation System
# Generate false location data for privacy protection based on customer preferences

import random
import hashlib
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from customer_loader import CustomerDataLoader

class LocationObfuscator:
    """Generate false location data for privacy protection using customer preferences"""
    
    def __init__(self, customer_loader: CustomerDataLoader = None):
        self.customer_loader = customer_loader or CustomerDataLoader()
        
        # Major city coordinates for realistic false locations
        self.city_coordinates = {
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'Chicago': (41.8781, -87.6298),
            'Houston': (29.7604, -95.3698),
            'Phoenix': (33.4484, -112.0740),
            'Philadelphia': (39.9526, -75.1652),
            'San Antonio': (29.4241, -98.4936),
            'San Diego': (32.7157, -117.1611),
            'Dallas': (32.7767, -96.7970),
            'San Jose': (37.3382, -121.8863),
            'Austin': (30.2672, -97.7431),
            'Jacksonville': (30.3322, -81.6557),
            'San Francisco': (37.7749, -122.4194),
            'Columbus': (39.9612, -82.9988),
            'Charlotte': (35.2271, -80.8431),
            'Fort Worth': (32.7555, -97.3308),
            'Detroit': (42.3314, -83.0458),
            'El Paso': (31.7619, -106.4850),
            'Memphis': (35.1495, -90.0490),
            'Seattle': (47.6062, -122.3321),
            'Denver': (39.7392, -104.9903),
            'Washington DC': (38.9072, -77.0369),
            'Boston': (42.3601, -71.0589),
            'Nashville': (36.1627, -86.7816),
            'Baltimore': (39.2904, -76.6122),
            'Oklahoma City': (35.4676, -97.5164),
            'Louisville': (38.2527, -85.7585),
            'Portland': (45.5152, -122.6784),
            'Las Vegas': (36.1699, -115.1398),
            'Milwaukee': (43.0389, -87.9065),
            'Albuquerque': (35.0844, -106.6504),
            'Tucson': (32.2226, -110.9747),
            'Fresno': (36.7378, -119.7871),
            'Sacramento': (38.5816, -121.4944),
            'Mesa': (33.4152, -111.8315),
            'Kansas City': (39.0997, -94.5786),
            'Atlanta': (33.7490, -84.3880),
            'Miami': (25.7617, -80.1918)
        }
    
    def get_customer_cities(self, customer_id: str) -> List[Tuple[float, float]]:
        """Get coordinate list for customer's preferred cities"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        preferred_cities = customer_prefs.get('preferred_cities', ['New York', 'Los Angeles'])
        
        coordinates = []
        for city in preferred_cities:
            if city in self.city_coordinates:
                coordinates.append(self.city_coordinates[city])
            else:
                # If city not found, use a random major city
                coordinates.append(random.choice(list(self.city_coordinates.values())))
        
        return coordinates
    
    def calculate_obfuscation_radius(self, privacy_level: str) -> float:
        """Calculate obfuscation radius based on privacy level"""
        radius_mapping = {
            'low': 0.01,      # ~1km
            'medium': 0.05,   # ~5km
            'high': 0.1,      # ~10km
            'maximum': 0.2    # ~20km
        }
        return radius_mapping.get(privacy_level, 0.05)
    
    def generate_false_gps_for_customer(self, customer_id: str) -> Dict:
        """Generate realistic but false GPS coordinates for specific customer"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs.get('location_obfuscation', True):
            return {'message': 'Location obfuscation disabled for this customer'}
        
        customer_cities = self.get_customer_cities(customer_id)
        base_lat, base_lng = random.choice(customer_cities)
        
        # Get obfuscation radius based on privacy level
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        max_offset = self.calculate_obfuscation_radius(privacy_level)
        
        # Add random offset within specified radius
        lat_offset = random.uniform(-max_offset, max_offset)
        lng_offset = random.uniform(-max_offset, max_offset)
        
        # Generate realistic accuracy based on privacy level
        accuracy_ranges = {
            'low': (3.0, 10.0),
            'medium': (5.0, 30.0),
            'high': (10.0, 50.0),
            'maximum': (20.0, 100.0)
        }
        min_acc, max_acc = accuracy_ranges.get(privacy_level, (5.0, 30.0))
        
        return {
            'customer_id': customer_id,
            'latitude': base_lat + lat_offset,
            'longitude': base_lng + lng_offset,
            'accuracy': random.uniform(min_acc, max_acc),
            'altitude': random.uniform(0.0, 100.0),
            'speed': random.uniform(0.0, 30.0),  # m/s
            'bearing': random.uniform(0.0, 360.0),
            'timestamp': datetime.now().isoformat(),
            'privacy_level': privacy_level,
            'obfuscation_radius_km': max_offset * 111  # Convert degrees to km (rough)
        }
    
    def generate_location_trail(self, customer_id: str, duration_hours: int = 24, 
                              points_per_hour: int = 4) -> List[Dict]:
        """Generate a trail of false location points over time"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs.get('location_obfuscation', True):
            return [{'message': 'Location obfuscation disabled for this customer'}]
        
        trail_points = []
        customer_cities = self.get_customer_cities(customer_id)
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        max_offset = self.calculate_obfuscation_radius(privacy_level)
        
        # Start from a random preferred city
        current_lat, current_lng = random.choice(customer_cities)
        
        total_points = duration_hours * points_per_hour
        
        for point_idx in range(total_points):
            # Calculate timestamp
            time_offset = timedelta(hours=point_idx / points_per_hour)
            timestamp = datetime.now() + time_offset
            
            # Add some movement simulation (random walk with bias toward staying near cities)
            if random.random() < 0.1:  # 10% chance to "teleport" to another preferred city
                current_lat, current_lng = random.choice(customer_cities)
            else:
                # Small movement
                lat_movement = random.uniform(-max_offset/10, max_offset/10)
                lng_movement = random.uniform(-max_offset/10, max_offset/10)
                current_lat += lat_movement
                current_lng += lng_movement
            
            # Add noise
            lat_noise = random.uniform(-max_offset/20, max_offset/20)
            lng_noise = random.uniform(-max_offset/20, max_offset/20)
            
            trail_point = {
                'point_id': f"{customer_id}_LOC_{point_idx:04d}",
                'latitude': current_lat + lat_noise,
                'longitude': current_lng + lng_noise,
                'accuracy': random.uniform(5.0, 50.0),
                'timestamp': timestamp.isoformat(),
                'speed': random.uniform(0.0, 25.0),
                'bearing': random.uniform(0.0, 360.0)
            }
            trail_points.append(trail_point)
        
        return trail_points
    
    def generate_false_wifi_signatures(self, customer_id: str, count: int = None) -> List[Dict]:
        """Generate false WiFi network signatures based on customer location preferences"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if count is None:
            # Determine count based on privacy level
            count_mapping = {
                'low': 5,
                'medium': 10,
                'high': 20,
                'maximum': 30
            }
            count = count_mapping.get(customer_prefs.get('privacy_level', 'medium'), 10)
        
        wifi_networks = []
        
        # Generate network names based on customer's preferred cities
        preferred_cities = customer_prefs.get('preferred_cities', ['New York'])
        
        for i in range(count):
            # Generate realistic MAC address
            mac_address = ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)])
            
            # Generate SSID based on location context
            city_context = random.choice(preferred_cities)
            ssid_patterns = [
                f"{city_context}_WiFi_{random.randint(1000, 9999)}",
                f"Network_{random.randint(1000, 9999)}",
                f"Guest_{random.randint(100, 999)}",
                f"Secure_{random.randint(1000, 9999)}",
                f"{city_context}Public",
                f"Business_{random.randint(100, 999)}"
            ]
            
            wifi_network = {
                'bssid': mac_address,
                'ssid': random.choice(ssid_patterns),
                'signal_strength': random.randint(-80, -30),
                'frequency': random.choice([2.4, 5.0, 6.0]),
                'security': random.choice(['WPA2', 'WPA3', 'Open', 'WEP']),
                'channel': random.randint(1, 165),
                'vendor': random.choice(['Cisco', 'Netgear', 'Linksys', 'TP-Link', 'Unknown']),
                'first_seen': datetime.now().isoformat(),
                'location_context': city_context
            }
            wifi_networks.append(wifi_network)
        
        return wifi_networks
    
    def generate_cellular_tower_data(self, customer_id: str) -> List[Dict]:
        """Generate false cellular tower connection data"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        customer_cities = self.get_customer_cities(customer_id)
        
        tower_count = {
            'low': 3,
            'medium': 5,
            'high': 8,
            'maximum': 12
        }.get(customer_prefs.get('privacy_level', 'medium'), 5)
        
        cellular_towers = []
        
        for i in range(tower_count):
            # Place towers near customer's preferred cities
            base_lat, base_lng = random.choice(customer_cities)
            tower_lat = base_lat + random.uniform(-0.1, 0.1)
            tower_lng = base_lng + random.uniform(-0.1, 0.1)
            
            tower = {
                'tower_id': f"CELL_{random.randint(10000, 99999)}",
                'mcc': random.choice([310, 311, 312]),  # US mobile country codes
                'mnc': random.randint(1, 999),
                'lac': random.randint(1000, 9999),
                'cell_id': random.randint(100000, 999999),
                'latitude': tower_lat,
                'longitude': tower_lng,
                'signal_strength': random.randint(-110, -50),
                'technology': random.choice(['LTE', '5G', 'UMTS', 'GSM']),
                'frequency_band': random.choice(['700MHz', '850MHz', '1900MHz', '2100MHz']),
                'distance_estimate': random.uniform(0.1, 10.0),  # km
                'timestamp': datetime.now().isoformat()
            }
            cellular_towers.append(tower)
        
        return cellular_towers

# Example usage and testing
def demo_location_obfuscation():
    """Demonstrate the location obfuscation system with customer data"""
    print("=== Location Obfuscation System Demo ===")
    
    # Initialize system
    obfuscator = LocationObfuscator()
    
    # Test with specific customers
    customers_to_test = ["CUST_001", "CUST_002", "CUST_004"]
    
    for customer_id in customers_to_test:
        print(f"\n--- Customer {customer_id} ---")
        
        # Generate false GPS
        false_gps = obfuscator.generate_false_gps_for_customer(customer_id)
        if 'latitude' in false_gps:
            print(f"False GPS: {false_gps['latitude']:.4f}, {false_gps['longitude']:.4f}")
            print(f"Privacy level: {false_gps['privacy_level']}")
            print(f"Obfuscation radius: {false_gps['obfuscation_radius_km']:.1f} km")
        else:
            print(f"GPS: {false_gps['message']}")
        
        # Generate location trail
        trail = obfuscator.generate_location_trail(customer_id, duration_hours=6, points_per_hour=2)
        if isinstance(trail, list) and len(trail) > 0 and 'latitude' in trail[0]:
            print(f"Generated location trail with {len(trail)} points")
            print(f"Trail span: {trail[0]['timestamp']} to {trail[-1]['timestamp']}")
        
        # Generate WiFi signatures
        wifi_sigs = obfuscator.generate_false_wifi_signatures(customer_id)
        print(f"Generated {len(wifi_sigs)} WiFi signatures")
        
        # Generate cellular tower data
        cellular_data = obfuscator.generate_cellular_tower_data(customer_id)
        print(f"Generated {len(cellular_data)} cellular tower connections")

if __name__ == "__main__":
    demo_location_obfuscation()