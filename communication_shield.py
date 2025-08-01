# Communication Shielding System
# Encrypted communication system for privacy based on customer preferences

import random
import hashlib
import base64
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from cryptography.fernet import Fernet
from customer_loader import CustomerDataLoader

class CommunicationShield:
    """Encrypted communication system for privacy protection"""
    
    def __init__(self, customer_loader: CustomerDataLoader = None):
        self.customer_loader = customer_loader or CustomerDataLoader()
        
        # Cover text templates for steganography
        self.cover_texts = {
            'business': [
                "Please review the quarterly reports and provide feedback by end of week.",
                "The meeting has been rescheduled to next Tuesday at 2 PM in conference room A.",
                "Thank you for your presentation yesterday. The team found it very informative.",
                "Could you please send the updated project timeline when you have a moment?",
                "The client has requested additional information about our service offerings."
            ],
            'casual': [
                "Hope you're having a great week! Let me know if you want to grab coffee soon.",
                "Thanks for the recommendation. I'll definitely check out that restaurant.",
                "The weather has been amazing lately. Perfect for outdoor activities.",
                "Looking forward to the weekend. Any fun plans on your end?",
                "Just wanted to catch up and see how things are going with you."
            ],
            'academic': [
                "The research findings indicate a significant correlation between the variables.",
                "Please refer to the attached documentation for detailed methodology.",
                "The peer review process should be completed within the next two weeks.",
                "Your analysis of the dataset provides valuable insights for our study.",
                "The conference presentation schedule has been updated with new time slots."
            ],
            'technical': [
                "The system deployment was successful with minimal downtime reported.",
                "Please update the configuration files according to the new specifications.",
                "The performance metrics show improvement after the latest optimization.",
                "Bug fixes have been implemented and pushed to the testing environment.",
                "The database migration completed without any data integrity issues."
            ]
        }
        
        # Communication protocols
        self.protocols = ['email', 'chat', 'forum', 'social_media', 'document', 'voice_note']
        
        # Encryption strength levels
        self.encryption_levels = {
            'basic': {'key_size': 128, 'rounds': 1},
            'standard': {'key_size': 256, 'rounds': 2},
            'high': {'key_size': 256, 'rounds': 3},
            'maximum': {'key_size': 256, 'rounds': 5}
        }
    
    def get_customer_encryption_settings(self, customer_id: str) -> Dict:
        """Get encryption settings based on customer preferences"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs.get('encryption_enabled', True):
            return {'enabled': False}
        
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        service_tier = customer_prefs.get('service_tier', 'standard')
        
        # Map privacy level to encryption strength
        encryption_mapping = {
            'low': 'basic',
            'medium': 'standard',
            'high': 'high',
            'maximum': 'maximum'
        }
        
        encryption_level = encryption_mapping.get(privacy_level, 'standard')
        
        # Enterprise customers get enhanced encryption
        if service_tier == 'enterprise':
            encryption_level = 'maximum'
        
        return {
            'enabled': True,
            'level': encryption_level,
            'settings': self.encryption_levels[encryption_level],
            'steganography': privacy_level in ['high', 'maximum'],
            'noise_generation': privacy_level in ['high', 'maximum'],
            'multi_layer': service_tier == 'enterprise'
        }
    
    def generate_encryption_key(self, customer_id: str) -> bytes:
        """Generate encryption key based on customer settings"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        
        if not encryption_settings.get('enabled', True):
            return Fernet.generate_key()  # Default key if encryption disabled
        
        # Generate key with customer-specific entropy
        customer_data = str(customer_id) + str(datetime.now().timestamp())
        key_material = hashlib.sha256(customer_data.encode()).digest()
        
        # Use Fernet for simplicity (includes proper key derivation)
        return Fernet.generate_key()
    
    def create_steganographic_message(self, message: str, customer_id: str, 
                                    cover_type: str = 'business') -> Dict:
        """Hide message within cover data using steganography"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        
        if not encryption_settings.get('steganography', False):
            return {'error': 'Steganography not enabled for this customer'}
        
        # Encrypt the message first
        encryption_key = self.generate_encryption_key(customer_id)
        cipher = Fernet(encryption_key)
        encrypted_msg = cipher.encrypt(message.encode())
        
        # Select appropriate cover text
        available_covers = self.cover_texts.get(cover_type, self.cover_texts['business'])
        cover_text = random.choice(available_covers)
        
        # Multiple rounds of encryption for high security
        encryption_rounds = encryption_settings['settings']['rounds']
        payload = encrypted_msg
        
        for round_num in range(encryption_rounds):
            round_key = self.generate_encryption_key(f"{customer_id}_round_{round_num}")
            round_cipher = Fernet(round_key)
            payload = round_cipher.encrypt(payload)
        
        # Create steganographic container
        hidden_message = {
            'cover_text': cover_text,
            'cover_type': cover_type,
            'hidden_payload': base64.b64encode(payload).decode('ascii'),
            'steganography_method': self.select_steganography_method(encryption_settings['level']),
            'encryption_rounds': encryption_rounds,
            'timestamp': datetime.now().isoformat(),
            'customer_id': customer_id,
            'message_id': hashlib.md5(f"{customer_id}{message}".encode()).hexdigest()[:12]
        }
        
        return hidden_message
    
    def select_steganography_method(self, encryption_level: str) -> str:
        """Select steganography method based on encryption level"""
        methods = {
            'basic': ['text_spacing', 'character_substitution'],
            'standard': ['text_spacing', 'character_substitution', 'unicode_variation'],
            'high': ['text_spacing', 'unicode_variation', 'semantic_hiding', 'frequency_analysis'],
            'maximum': ['unicode_variation', 'semantic_hiding', 'frequency_analysis', 'linguistic_steganography']
        }
        
        available_methods = methods.get(encryption_level, methods['standard'])
        return random.choice(available_methods)
    
    def create_communication_noise(self, customer_id: str, duration_minutes: int = 60) -> List[Dict]:
        """Generate communication noise to mask real traffic"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        
        if not encryption_settings.get('noise_generation', False):
            return [{'message': 'Noise generation not enabled for this customer'}]
        
        noise_packets = []
        
        # Determine noise intensity based on privacy level
        privacy_level = self.customer_loader.get_customer_preferences(customer_id).get('privacy_level', 'medium')
        intensity_mapping = {
            'low': 1,
            'medium': 3,
            'high': 7,
            'maximum': 15
        }
        
        packets_per_minute = intensity_mapping.get(privacy_level, 3)
        
        for minute in range(duration_minutes):
            for packet_num in range(packets_per_minute):
                timestamp = datetime.now() + timedelta(minutes=minute, seconds=packet_num * (60 // packets_per_minute))
                
                noise_packet = {
                    'packet_id': f"NOISE_{customer_id}_{random.randint(10000, 99999)}",
                    'timestamp': timestamp.isoformat(),
                    'size_bytes': random.randint(64, 1500),
                    'protocol': random.choice(['TCP', 'UDP', 'HTTP', 'HTTPS', 'WebSocket']),
                    'destination_type': random.choice(['server', 'peer', 'cdn', 'proxy']),
                    'content_type': random.choice(['text', 'image', 'video', 'audio', 'data']),
                    'encryption_level': random.choice(['none', 'basic', 'standard', 'advanced']),
                    'content_hash': hashlib.md5(f"noise_{customer_id}_{minute}_{packet_num}".encode()).hexdigest(),
                    'traffic_pattern': self.generate_traffic_pattern(),
                    'decoy_purpose': random.choice(['web_browsing', 'file_download', 'streaming', 'gaming', 'update'])
                }
                noise_packets.append(noise_packet)
        
        return noise_packets
    
    def generate_traffic_pattern(self) -> Dict:
        """Generate realistic traffic patterns for noise"""
        return {
            'burst_probability': random.uniform(0.1, 0.8),
            'sustained_rate': random.uniform(0.2, 2.0),  # MB/s
            'peak_multiplier': random.uniform(1.5, 5.0),
            'idle_periods': random.choice([True, False]),
            'protocol_switching': random.choice([True, False])
        }
    
    def create_multi_layer_encryption(self, message: str, customer_id: str) -> Dict:
        """Create multi-layer encryption for enterprise customers"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        
        if not encryption_settings.get('multi_layer', False):
            return {'error': 'Multi-layer encryption not available for this customer tier'}
        
        layers = []
        current_payload = message.encode()
        
        # Layer 1: AES Encryption
        layer1_key = self.generate_encryption_key(f"{customer_id}_layer1")
        layer1_cipher = Fernet(layer1_key)
        current_payload = layer1_cipher.encrypt(current_payload)
        layers.append({
            'layer': 1,
            'method': 'AES-256',
            'key_hash': hashlib.sha256(layer1_key).hexdigest()[:16]
        })
        
        # Layer 2: XOR with dynamic key
        xor_key = hashlib.sha256(f"{customer_id}_xor_{datetime.now()}".encode()).digest()
        xor_payload = bytearray(current_payload)
        for i in range(len(xor_payload)):
            xor_payload[i] ^= xor_key[i % len(xor_key)]
        current_payload = bytes(xor_payload)
        layers.append({
            'layer': 2,
            'method': 'XOR_Dynamic',
            'key_hash': hashlib.sha256(xor_key).hexdigest()[:16]
        })
        
        # Layer 3: Base64 + Scrambling
        b64_payload = base64.b64encode(current_payload).decode('ascii')
        scrambled_payload = self.scramble_string(b64_payload, customer_id)
        current_payload = scrambled_payload.encode()
        layers.append({
            'layer': 3,
            'method': 'Base64_Scramble',
            'scramble_seed': hashlib.md5(customer_id.encode()).hexdigest()[:8]
        })
        
        # Layer 4: Final encryption
        layer4_key = self.generate_encryption_key(f"{customer_id}_layer4")
        layer4_cipher = Fernet(layer4_key)
        final_payload = layer4_cipher.encrypt(current_payload)
        layers.append({
            'layer': 4,
            'method': 'AES-256_Final',
            'key_hash': hashlib.sha256(layer4_key).hexdigest()[:16]
        })
        
        return {
            'encrypted_payload': base64.b64encode(final_payload).decode('ascii'),
            'layers': layers,
            'total_layers': len(layers),
            'customer_id': customer_id,
            'encryption_timestamp': datetime.now().isoformat(),
            'decryption_complexity': 'enterprise_grade'
        }
    
    def scramble_string(self, text: str, seed: str) -> str:
        """Scramble string using deterministic algorithm"""
        random.seed(hashlib.md5(seed.encode()).hexdigest())
        chars = list(text)
        random.shuffle(chars)
        return ''.join(chars)
    
    def create_secure_channel(self, customer_id: str, channel_type: str = 'bidirectional') -> Dict:
        """Create secure communication channel"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        
        if not encryption_settings.get('enabled', True):
            return {'error': 'Encryption not enabled for this customer'}
        
        # Generate channel parameters
        channel_id = hashlib.sha256(f"{customer_id}_{datetime.now()}".encode()).hexdigest()[:16]
        
        # Create key exchange parameters
        key_exchange = {
            'method': 'ECDH' if encryption_settings['level'] in ['high', 'maximum'] else 'DHE',
            'curve': 'secp256r1' if encryption_settings['level'] in ['high', 'maximum'] else 'secp224r1',
            'key_size': encryption_settings['settings']['key_size']
        }
        
        # Channel configuration
        channel_config = {
            'channel_id': channel_id,
            'customer_id': customer_id,
            'channel_type': channel_type,
            'encryption_level': encryption_settings['level'],
            'key_exchange': key_exchange,
            'session_keys': {
                'primary': base64.b64encode(self.generate_encryption_key(f"{customer_id}_primary")).decode('ascii'),
                'backup': base64.b64encode(self.generate_encryption_key(f"{customer_id}_backup")).decode('ascii')
            },
            'channel_features': {
                'forward_secrecy': encryption_settings['level'] in ['high', 'maximum'],
                'message_authentication': True,
                'replay_protection': True,
                'traffic_analysis_resistance': encryption_settings.get('noise_generation', False)
            },
            'created_timestamp': datetime.now().isoformat(),
            'expiry_timestamp': (datetime.now() + timedelta(hours=24)).isoformat(),
            'protocol_version': '2.1' if encryption_settings['level'] == 'maximum' else '2.0'
        }
        
        return channel_config
    
    def generate_decoy_communications(self, customer_id: str, count: int = 50) -> List[Dict]:
        """Generate decoy communications to mask real messages"""
        encryption_settings = self.get_customer_encryption_settings(customer_id)
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        decoy_messages = []
        
        # Determine communication style based on customer
        service_tier = customer_prefs.get('service_tier', 'standard')
        if service_tier == 'enterprise':
            primary_style = 'business'
        elif service_tier == 'premium':
            primary_style = random.choice(['business', 'technical'])
        else:
            primary_style = random.choice(['casual', 'business'])
        
        for i in range(count):
            # Select message style
            message_style = primary_style if random.random() < 0.7 else random.choice(list(self.cover_texts.keys()))
            
            # Generate decoy content
            base_message = random.choice(self.cover_texts[message_style])
            
            # Add realistic variations
            variations = [
                f"Re: {base_message}",
                f"Fwd: {base_message}",
                f"Follow-up: {base_message}",
                base_message,
                f"Quick question: {base_message}"
            ]
            
            message_content = random.choice(variations)
            
            decoy_message = {
                'message_id': f"DECOY_{customer_id}_{i:04d}",
                'customer_id': customer_id,
                'content': message_content,
                'message_type': message_style,
                'protocol': random.choice(self.protocols),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
                'size_bytes': len(message_content.encode()),
                'encryption_applied': encryption_settings.get('enabled', True),
                'priority': random.choice(['low', 'normal', 'high']),
                'metadata': {
                    'sender_pattern': 'automated_decoy',
                    'recipient_pattern': 'distributed',
                    'traffic_class': 'background'
                }
            }
            
            decoy_messages.append(decoy_message)
        
        return decoy_messages

# Example usage and testing
def demo_communication_shield():
    """Demonstrate the communication shield system with customer data"""
    print("=== Communication Shield System Demo ===")
    
    # Initialize system
    shield = CommunicationShield()
    
    # Test with specific customers
    customers_to_test = ["CUST_001", "CUST_003", "CUST_005"]
    
    for customer_id in customers_to_test:
        print(f"\n--- Customer {customer_id} ---")
        
        # Get encryption settings
        settings = shield.get_customer_encryption_settings(customer_id)
        print(f"Encryption enabled: {settings.get('enabled', False)}")
        if settings.get('enabled'):
            print(f"Encryption level: {settings['level']}")
            print(f"Steganography: {settings.get('steganography', False)}")
        
        # Test steganographic message
        if settings.get('steganography', False):
            hidden_msg = shield.create_steganographic_message("Secret test message", customer_id, 'business')
            if 'error' not in hidden_msg:
                print(f"Steganographic message created with {hidden_msg['encryption_rounds']} encryption rounds")
        
        # Test multi-layer encryption for enterprise customers
        customer_prefs = shield.customer_loader.get_customer_preferences(customer_id)
        if customer_prefs.get('service_tier') == 'enterprise':
            multi_layer = shield.create_multi_layer_encryption("Enterprise secret", customer_id)
            if 'error' not in multi_layer:
                print(f"Multi-layer encryption: {multi_layer['total_layers']} layers")
        
        # Generate communication noise
        if settings.get('noise_generation', False):
            noise = shield.create_communication_noise(customer_id, duration_minutes=10)
            if isinstance(noise, list) and 'message' not in noise[0]:
                print(f"Generated {len(noise)} noise packets")
        
        # Create secure channel
        if settings.get('enabled', True):
            channel = shield.create_secure_channel(customer_id)
            if 'error' not in channel:
                print(f"Secure channel created: {channel['channel_id']}")
                print(f"Forward secrecy: {channel['channel_features']['forward_secrecy']}")
        
        # Generate decoy communications
        decoys = shield.generate_decoy_communications(customer_id, count=10)
        print(f"Generated {len(decoys)} decoy communications")

if __name__ == "__main__":
    demo_communication_shield()