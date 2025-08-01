# COBRA Personal Devices - Digital Signature Generator
# Generates diverse digital signatures for privacy protection

import random
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List
from customer_loader import CustomerDataLoader

class COBRADevice:
    """Conceptual device for generating diverse digital signatures based on customer preferences"""
    
    def __init__(self, customer_loader: CustomerDataLoader = None):
        self.customer_loader = customer_loader or CustomerDataLoader()
        
        # Base data streams available
        self.data_streams = [
            'accelerometer', 'gyroscope', 'magnetometer', 'temperature',
            'humidity', 'pressure', 'light_sensor', 'proximity', 'wifi_scan',
            'bluetooth_scan', 'cellular_signal', 'battery_level', 'cpu_usage',
            'memory_usage', 'network_latency', 'gps_accuracy', 'microphone_ambient',
            'camera_exposure', 'touch_pressure', 'vibration_pattern'
        ]
        
        # Device-specific streams
        self.device_streams = {
            'smartphone': ['accelerometer', 'gyroscope', 'wifi_scan', 'bluetooth_scan', 
                          'cellular_signal', 'battery_level', 'gps_accuracy', 'microphone_ambient'],
            'laptop': ['temperature', 'cpu_usage', 'memory_usage', 'network_latency', 
                      'wifi_scan', 'battery_level', 'camera_exposure'],
            'tablet': ['accelerometer', 'gyroscope', 'touch_pressure', 'light_sensor', 
                      'wifi_scan', 'battery_level', 'gps_accuracy'],
            'smartwatch': ['accelerometer', 'gyroscope', 'heart_rate', 'skin_temperature', 
                          'step_count', 'vibration_pattern', 'ambient_light']
        }
    
    def get_device_streams(self, device_types: List[str]) -> List[str]:
        """Get available data streams for customer's devices"""
        available_streams = set()
        for device_type in device_types:
            if device_type in self.device_streams:
                available_streams.update(self.device_streams[device_type])
        return list(available_streams)
    
    def generate_sensor_value(self, stream_name: str) -> float:
        """Generate realistic sensor values based on stream type"""
        if 'accel' in stream_name or 'gyro' in stream_name:
            return random.uniform(-10.0, 10.0)
        elif 'temp' in stream_name:
            return random.uniform(15.0, 35.0)
        elif 'pressure' in stream_name:
            return random.uniform(950.0, 1050.0)
        elif 'battery' in stream_name:
            return random.uniform(20.0, 100.0)
        elif 'heart_rate' in stream_name:
            return random.uniform(60.0, 100.0)
        elif 'step_count' in stream_name:
            return random.randint(0, 10000)
        elif 'usage' in stream_name:
            return random.uniform(0.0, 100.0)
        elif 'latency' in stream_name:
            return random.uniform(1.0, 500.0)
        else:
            return random.uniform(0.0, 100.0)
    
    def generate_false_signatures_for_customer(self, customer_id: str) -> Dict:
        """Generate false digital signatures customized for specific customer"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs:
            print(f"Customer {customer_id} not found, using default settings")
            return self.generate_false_signatures(25)
        
        # Get streams based on customer's devices
        available_streams = self.get_device_streams(customer_prefs['device_types'])
        
        # Determine number of streams based on privacy level
        privacy_multipliers = {
            'low': 0.5,
            'medium': 1.0,
            'high': 1.5,
            'maximum': 2.0
        }
        
        base_streams = len(available_streams)
        multiplier = privacy_multipliers.get(customer_prefs['privacy_level'], 1.0)
        num_streams = int(base_streams * multiplier)
        
        return self.generate_false_signatures(num_streams, available_streams, customer_id)
    
    def generate_false_signatures(self, num_streams: int = 50, 
                                available_streams: List[str] = None,
                                customer_id: str = None) -> Dict:
        """Generate false digital signatures across multiple data streams"""
        if available_streams is None:
            available_streams = self.data_streams
        
        signatures = {}
        signature_metadata = {
            'customer_id': customer_id,
            'generation_time': datetime.now().isoformat(),
            'total_signatures': num_streams,
            'device_coverage': len(available_streams)
        }
        
        for i in range(num_streams):
            stream_name = random.choice(available_streams)
            value = self.generate_sensor_value(stream_name)
            
            # Add temporal variation
            time_offset = random.randint(-300, 300)  # ±5 minutes
            timestamp = datetime.now() + timedelta(seconds=time_offset)
            
            signature_key = f"{stream_name}_{i}_{int(timestamp.timestamp())}"
            signatures[signature_key] = {
                'stream_type': stream_name,
                'value': value,
                'timestamp': timestamp.isoformat(),
                'checksum': hashlib.md5(str(value).encode()).hexdigest()[:8],
                'variance_factor': random.uniform(0.8, 1.2),
                'confidence_score': random.uniform(0.7, 1.0)
            }
        
        return {
            'signatures': signatures,
            'metadata': signature_metadata
        }
    
    def generate_device_fingerprint(self, customer_id: str) -> Dict:
        """Generate a unique device fingerprint for the customer"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        fingerprint_data = {
            'customer_id': customer_id,
            'device_types': customer_prefs.get('device_types', ['smartphone']),
            'os_variants': [f"OS_{random.randint(10, 15)}.{random.randint(0, 9)}" 
                           for _ in customer_prefs.get('device_types', ['smartphone'])],
            'hardware_signatures': {},
            'network_characteristics': {},
            'generation_timestamp': datetime.now().isoformat()
        }
        
        # Generate hardware signatures for each device
        for device_type in customer_prefs.get('device_types', ['smartphone']):
            fingerprint_data['hardware_signatures'][device_type] = {
                'cpu_model': f"Processor_{random.randint(1000, 9999)}",
                'memory_size': random.choice([4, 8, 16, 32]),
                'storage_size': random.choice([64, 128, 256, 512, 1024]),
                'screen_resolution': random.choice(['1920x1080', '2560x1440', '3840x2160']),
                'device_id_hash': hashlib.sha256(f"{customer_id}_{device_type}".encode()).hexdigest()[:16]
            }
        
        # Generate network characteristics
        fingerprint_data['network_characteristics'] = {
            'ip_range_pattern': f"192.168.{random.randint(1, 255)}.xxx",
            'dns_servers': [f"8.8.{random.randint(1, 9)}.{random.randint(1, 9)}" for _ in range(2)],
            'connection_types': random.sample(['wifi', 'cellular', 'ethernet'], k=random.randint(1, 3)),
            'bandwidth_profile': {
                'download_mbps': random.uniform(10.0, 1000.0),
                'upload_mbps': random.uniform(5.0, 100.0),
                'latency_ms': random.uniform(1.0, 50.0)
            }
        }
        
        return fingerprint_data
    
    def create_noise_signatures(self, duration_minutes: int = 30, customer_id: str = None) -> List[Dict]:
        """Create noise signatures to mask real device activity"""
        noise_signatures = []
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id) if customer_id else {}
        
        # Generate noise based on privacy level
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        noise_multipliers = {'low': 0.5, 'medium': 1.0, 'high': 2.0, 'maximum': 3.0}
        noise_factor = noise_multipliers.get(privacy_level, 1.0)
        
        signatures_per_minute = int(10 * noise_factor)  # Base 10 signatures per minute
        
        for minute in range(duration_minutes):
            for sig in range(signatures_per_minute):
                timestamp = datetime.now() + timedelta(minutes=minute, seconds=sig*6)
                
                noise_signature = {
                    'signature_id': f"NOISE_{random.randint(100000, 999999)}",
                    'timestamp': timestamp.isoformat(),
                    'stream_type': random.choice(self.data_streams),
                    'noise_value': random.uniform(-100.0, 100.0),
                    'noise_pattern': random.choice(['gaussian', 'uniform', 'spike', 'drift']),
                    'amplitude': random.uniform(0.1, 2.0),
                    'frequency_hz': random.uniform(0.1, 10.0)
                }
                noise_signatures.append(noise_signature)
        
        return noise_signatures

# Example usage and testing
def demo_cobra_system():
    """Demonstrate the COBRA device system with customer data"""
    print("=== COBRA Device System Demo ===")
    
    # Initialize system
    cobra = COBRADevice()
    
    # Test with specific customers
    customers_to_test = ["CUST_001", "CUST_003", "CUST_005"]
    
    for customer_id in customers_to_test:
        print(f"\n--- Customer {customer_id} ---")
        
        # Generate signatures for customer
        sig_data = cobra.generate_false_signatures_for_customer(customer_id)
        signatures = sig_data['signatures']
        metadata = sig_data['metadata']
        
        print(f"Generated {len(signatures)} signatures")
        print(f"Device coverage: {metadata['device_coverage']} streams")
        print(f"Sample signatures: {list(signatures.keys())[:3]}")
        
        # Generate device fingerprint
        fingerprint = cobra.generate_device_fingerprint(customer_id)
        print(f"Device types: {fingerprint['device_types']}")
        
        # Generate noise signatures
        noise_sigs = cobra.create_noise_signatures(duration_minutes=5, customer_id=customer_id)
        print(f"Generated {len(noise_sigs)} noise signatures")

if __name__ == "__main__":
    demo_cobra_system()
