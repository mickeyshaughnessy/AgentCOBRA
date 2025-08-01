# Main Privacy Protection System Demo
# Demonstrates all components working together with customer data

import json
import os
from datetime import datetime
from customer_loader import CustomerDataLoader
from cobra_device import COBRADevice
from location_obfuscator import LocationObfuscator
from identity_multiplier import IdentityMultiplier
from communication_shield import CommunicationShield
from biometric_countermeasures import BiometricCountermeasures

class PrivacyProtectionSuite:
    """Complete privacy protection system integrating all components"""
    
    def __init__(self, customer_data_file="customers.json"):
        print("Initializing Privacy Protection Suite...")
        
        # Initialize customer data loader
        self.customer_loader = CustomerDataLoader(customer_data_file)
        
        # Initialize all protection systems
        self.cobra_device = COBRADevice(self.customer_loader)
        self.location_obfuscator = LocationObfuscator(self.customer_loader)
        self.identity_multiplier = IdentityMultiplier(self.customer_loader)
        self.communication_shield = CommunicationShield(self.customer_loader)
        self.biometric_countermeasures = BiometricCountermeasures(self.customer_loader)
        
        print("Privacy Protection Suite initialized successfully!")
    
    def generate_customer_protection_profile(self, customer_id: str) -> dict:
        """Generate complete protection profile for a customer"""
        print(f"\nGenerating protection profile for customer {customer_id}...")
        
        customer = self.customer_loader.get_customer(customer_id)
        if not customer:
            return {"error": f"Customer {customer_id} not found"}
        
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        protection_profile = {
            "customer_info": {
                "customer_id": customer_id,
                "name": customer["name"],
                "privacy_level": customer_prefs["privacy_level"],
                "service_tier": customer_prefs["service_tier"],
                "profile_generated": datetime.now().isoformat()
            },
            "protection_components": {}
        }
        
        # 1. COBRA Device Signatures
        print("  - Generating COBRA device signatures...")
        cobra_data = self.cobra_device.generate_false_signatures_for_customer(customer_id)
        device_fingerprint = self.cobra_device.generate_device_fingerprint(customer_id)
        noise_signatures = self.cobra_device.create_noise_signatures(duration_minutes=30, customer_id=customer_id)
        
        protection_profile["protection_components"]["cobra_device"] = {
            "digital_signatures": {
                "count": len(cobra_data["signatures"]),
                "device_coverage": cobra_data["metadata"]["device_coverage"],
                "sample_signatures": list(cobra_data["signatures"].keys())[:5]
            },
            "device_fingerprint": {
                "device_types": device_fingerprint["device_types"],
                "hardware_variants": len(device_fingerprint["hardware_signatures"]),
                "network_characteristics": device_fingerprint["network_characteristics"]
            },
            "noise_generation": {
                "noise_signatures_count": len(noise_signatures),
                "duration_minutes": 30
            }
        }
        
        # 2. Location Obfuscation
        if customer_prefs["location_obfuscation"]:
            print("  - Generating location obfuscation data...")
            false_gps = self.location_obfuscator.generate_false_gps_for_customer(customer_id)
            location_trail = self.location_obfuscator.generate_location_trail(customer_id, duration_hours=12, points_per_hour=4)
            wifi_signatures = self.location_obfuscator.generate_false_wifi_signatures(customer_id)
            cellular_data = self.location_obfuscator.generate_cellular_tower_data(customer_id)
            
            protection_profile["protection_components"]["location_obfuscation"] = {
                "false_gps": {
                    "obfuscation_radius_km": false_gps.get("obfuscation_radius_km", 0),
                    "accuracy_range": f"{false_gps.get('accuracy', 0):.1f}m" if 'accuracy' in false_gps else "N/A"
                },
                "location_trail": {
                    "points_generated": len(location_trail) if isinstance(location_trail, list) else 0,
                    "duration_hours": 12
                },
                "wifi_signatures": len(wifi_signatures),
                "cellular_towers": len(cellular_data)
            }
        else:
            protection_profile["protection_components"]["location_obfuscation"] = {
                "status": "disabled_per_customer_preference"
            }
        
        # 3. Identity Multiplication
        print("  - Generating false identities...")
        false_identities = self.identity_multiplier.generate_false_identities_for_customer(customer_id)
        
        # Generate lifecycle events for first few identities
        sample_identity = false_identities[0] if false_identities else None
        lifecycle_events = []
        if sample_identity:
            lifecycle_events = self.identity_multiplier.generate_identity_lifecycle_events(sample_identity)
        
        protection_profile["protection_components"]["identity_multiplication"] = {
            "false_identities_count": len(false_identities),
            "complexity_level": false_identities[0]["complexity_level"] if false_identities else "N/A",
            "sample_identity": {
                "name": false_identities[0]["name"]["full_name"] if false_identities else "N/A",
                "email_domain": false_identities[0]["email"].split("@")[1] if false_identities else "N/A"
            },
            "lifecycle_events_sample": len(lifecycle_events)
        }
        
        # 4. Communication Shield
        if customer_prefs["encryption_enabled"]:
            print("  - Generating communication protection...")
            encryption_settings = self.communication_shield.get_customer_encryption_settings(customer_id)
            
            # Create steganographic message if enabled
            steganographic_msg = None
            if encryption_settings.get("steganography", False):
                steganographic_msg = self.communication_shield.create_steganographic_message(
                    "Test secure message", customer_id, "business"
                )
            
            # Generate communication noise
            comm_noise = []
            if encryption_settings.get("noise_generation", False):
                comm_noise = self.communication_shield.create_communication_noise(customer_id, duration_minutes=20)
            
            # Create secure channel
            secure_channel = self.communication_shield.create_secure_channel(customer_id)
            
            # Generate decoy communications
            decoy_comms = self.communication_shield.generate_decoy_communications(customer_id, count=25)
            
            protection_profile["protection_components"]["communication_shield"] = {
                "encryption_level": encryption_settings["level"],
                "steganography_enabled": encryption_settings.get("steganography", False),
                "noise_generation_enabled": encryption_settings.get("noise_generation", False),
                "secure_channel": {
                    "channel_id": secure_channel.get("channel_id", "N/A"),
                    "forward_secrecy": secure_channel.get("channel_features", {}).get("forward_secrecy", False)
                },
                "communication_noise_packets": len(comm_noise) if isinstance(comm_noise, list) else 0,
                "decoy_communications": len(decoy_comms)
            }
        else:
            protection_profile["protection_components"]["communication_shield"] = {
                "status": "disabled_per_customer_preference"
            }
        
        # 5. Biometric Countermeasures
        if customer_prefs["biometric_protection"]:
            print("  - Generating biometric countermeasures...")
            bio_settings = self.biometric_countermeasures.get_customer_biometric_settings(customer_id)
            
            countermeasures = {}
            
            # Facial recognition countermeasures
            if "facial_recognition" in bio_settings.get("applicable_biometrics", []):
                face_variations = self.biometric_countermeasures.generate_face_variation_map_for_customer(customer_id)
                if "facial_landmarks" in face_variations:
                    countermeasures["facial_recognition"] = {
                        "landmark_variations": len(face_variations["facial_landmarks"]),
                        "lighting_adjustments": len(face_variations["lighting_adjustments"]),
                        "geometric_transforms": len(face_variations["geometric_transforms"])
                    }
            
            # Gait analysis countermeasures
            if "gait_analysis" in bio_settings.get("applicable_biometrics", []):
                gait_modifications = self.biometric_countermeasures.generate_gait_modification_pattern(customer_id)
                if "step_modifications" in gait_modifications:
                    countermeasures["gait_analysis"] = {
                        "step_modifications": True,
                        "temporal_modifications": True,
                        "kinematic_modifications": True
                    }
            
            # Keystroke dynamics countermeasures
            if "keystroke_dynamics" in bio_settings.get("applicable_biometrics", []):
                keystroke_variations = self.biometric_countermeasures.generate_keystroke_dynamics_variation(customer_id)
                if "typing_patterns" in keystroke_variations:
                    countermeasures["keystroke_dynamics"] = {
                        "typing_patterns": len(keystroke_variations["typing_patterns"]),
                        "rhythm_modifications": True,
                        "pressure_variations": True
                    }
            
            # Voice print countermeasures
            if "voice_print" in bio_settings.get("applicable_biometrics", []):
                voice_modifications = self.biometric_countermeasures.generate_voice_print_countermeasures(customer_id)
                if "acoustic_modifications" in voice_modifications:
                    countermeasures["voice_print"] = {
                        "acoustic_modifications": True,
                        "prosodic_variations": True,
                        "environmental_factors": True
                    }
            
            # Multi-modal protection for maximum privacy customers
            if customer_prefs["privacy_level"] == "maximum":
                multi_modal = self.biometric_countermeasures.generate_multi_modal_countermeasures(customer_id)
                if "synchronized_countermeasures" in multi_modal:
                    countermeasures["multi_modal"] = {
                        "synchronized_biometrics": len(multi_modal["synchronized_countermeasures"]),
                        "adaptive_strategies": True,
                        "coordination_matrix": len(multi_modal["coordination_matrix"])
                    }
            
            protection_profile["protection_components"]["biometric_countermeasures"] = {
                "protection_intensity": bio_settings["intensity"],
                "applicable_biometrics": bio_settings["applicable_biometrics"],
                "countermeasures": countermeasures
            }
        else:
            protection_profile["protection_components"]["biometric_countermeasures"] = {
                "status": "disabled_per_customer_preference"
            }
        
        print(f"Protection profile generated successfully for {customer['name']}!")
        return protection_profile
    
    def generate_privacy_report(self, customer_id: str) -> str:
        """Generate a comprehensive privacy protection report"""
        protection_profile = self.generate_customer_protection_profile(customer_id)
        
        if "error" in protection_profile:
            return f"Error: {protection_profile['error']}"
        
        customer_info = protection_profile["customer_info"]
        components = protection_profile["protection_components"]
        
        report = f"""
# Privacy Protection Report
**Customer:** {customer_info['name']} ({customer_info['customer_id']})
**Privacy Level:** {customer_info['privacy_level'].title()}
**Service Tier:** {customer_info['service_tier'].title()}
**Report Generated:** {customer_info['profile_generated']}

## Protection Components Summary

### 1. COBRA Device Signatures
- **Digital Signatures Generated:** {components['cobra_device']['digital_signatures']['count']}
- **Device Coverage:** {components['cobra_device']['digital_signatures']['device_coverage']} data streams
- **Device Types:** {', '.join(components['cobra_device']['device_fingerprint']['device_types'])}
- **Noise Signatures:** {components['cobra_device']['noise_generation']['noise_signatures_count']} over {components['cobra_device']['noise_generation']['duration_minutes']} minutes

### 2. Location Obfuscation
"""
        
        if "status" in components["location_obfuscation"]:
            report += f"- **Status:** {components['location_obfuscation']['status']}\n"
        else:
            loc_comp = components["location_obfuscation"]
            report += f"""- **Obfuscation Radius:** {loc_comp['false_gps']['obfuscation_radius_km']:.1f} km
- **GPS Accuracy Range:** {loc_comp['false_gps']['accuracy_range']}
- **Location Trail Points:** {loc_comp['location_trail']['points_generated']} over {loc_comp['location_trail']['duration_hours']} hours
- **WiFi Signatures:** {loc_comp['wifi_signatures']}
- **Cellular Towers:** {loc_comp['cellular_towers']}
"""
        
        report += f"""
### 3. Identity Multiplication
- **False Identities Generated:** {components['identity_multiplication']['false_identities_count']}
- **Complexity Level:** {components['identity_multiplication']['complexity_level']}
- **Sample Identity:** {components['identity_multiplication']['sample_identity']['name']}
- **Email Domain Type:** {components['identity_multiplication']['sample_identity']['email_domain']}
- **Lifecycle Events (Sample):** {components['identity_multiplication']['lifecycle_events_sample']}

### 4. Communication Shield
"""
        
        if "status" in components["communication_shield"]:
            report += f"- **Status:** {components['communication_shield']['status']}\n"
        else:
            comm_comp = components["communication_shield"]
            report += f"""- **Encryption Level:** {comm_comp['encryption_level']}
- **Steganography:** {'Enabled' if comm_comp['steganography_enabled'] else 'Disabled'}
- **Noise Generation:** {'Enabled' if comm_comp['noise_generation_enabled'] else 'Disabled'}
- **Secure Channel ID:** {comm_comp['secure_channel']['channel_id']}
- **Forward Secrecy:** {'Yes' if comm_comp['secure_channel']['forward_secrecy'] else 'No'}
- **Communication Noise Packets:** {comm_comp['communication_noise_packets']}
- **Decoy Communications:** {comm_comp['decoy_communications']}
"""
        
        report += f"""
### 5. Biometric Countermeasures
"""
        
        if "status" in components["biometric_countermeasures"]:
            report += f"- **Status:** {components['biometric_countermeasures']['status']}\n"
        else:
            bio_comp = components["biometric_countermeasures"]
            report += f"""- **Protection Intensity:** {bio_comp['protection_intensity']}
- **Applicable Biometrics:** {', '.join(bio_comp['applicable_biometrics'])}
- **Active Countermeasures:**
"""
            for biometric, details in bio_comp["countermeasures"].items():
                report += f"  - **{biometric.replace('_', ' ').title()}:** "
                if isinstance(details, dict):
                    detail_list = [f"{k}: {v}" for k, v in details.items() if v is not False]
                    report += ", ".join(detail_list) + "\n"
                else:
                    report += f"{details}\n"
        
        report += f"""
## Summary
This privacy protection profile provides comprehensive coverage across all enabled protection systems. The configuration is optimized for {customer_info['privacy_level']} privacy level with {customer_info['service_tier']} service tier features.

---
*Generated by Privacy Protection Suite v2.0*
"""
        
        return report
    
    def demonstrate_all_customers(self):
        """Demonstrate the system with all customers in the database"""
        print("\n" + "="*80)
        print("PRIVACY PROTECTION SUITE - COMPREHENSIVE DEMONSTRATION")
        print("="*80)
        
        customers = self.customer_loader.get_all_customers()
        
        print(f"\nLoaded {len(customers)} customers from database")
        print("Generating protection profiles for all customers...\n")
        
        for customer in customers:
            customer_id = customer["customer_id"]
            print(f"\n{'='*60}")
            print(f"CUSTOMER: {customer['name']} ({customer_id})")
            print(f"Privacy Level: {customer['privacy_level']} | Service: {customer['service_tier']}")
            print(f"{'='*60}")
            
            # Generate and display protection profile
            protection_profile = self.generate_customer_protection_profile(customer_id)
            
            if "error" not in protection_profile:
                self.display_protection_summary(protection_profile)
            else:
                print(f"Error generating profile: {protection_profile['error']}")
    
    def display_protection_summary(self, protection_profile):
        """Display a concise summary of protection components"""
        components = protection_profile["protection_components"]
        
        # COBRA Device Summary
        cobra = components["cobra_device"]
        print(f"📱 COBRA Device: {cobra['digital_signatures']['count']} signatures, "
              f"{cobra['digital_signatures']['device_coverage']} data streams, "
              f"{cobra['noise_generation']['noise_signatures_count']} noise signatures")
        
        # Location Summary
        if "status" not in components["location_obfuscation"]:
            loc = components["location_obfuscation"]
            print(f"📍 Location: {loc['false_gps']['obfuscation_radius_km']:.1f}km radius, "
                  f"{loc['location_trail']['points_generated']} trail points, "
                  f"{loc['wifi_signatures']} WiFi + {loc['cellular_towers']} cellular")
        else:
            print(f"📍 Location: {components['location_obfuscation']['status']}")
        
        # Identity Summary
        identity = components["identity_multiplication"]
        print(f"👤 Identity: {identity['false_identities_count']} false identities, "
              f"{identity['complexity_level']} complexity")
        
        # Communication Summary
        if "status" not in components["communication_shield"]:
            comm = components["communication_shield"]
            print(f"🔒 Communication: {comm['encryption_level']} encryption, "
                  f"{'stego' if comm['steganography_enabled'] else 'no-stego'}, "
                  f"{comm['decoy_communications']} decoys")
        else:
            print(f"🔒 Communication: {components['communication_shield']['status']}")
        
        # Biometric Summary
        if "status" not in components["biometric_countermeasures"]:
            bio = components["biometric_countermeasures"]
            print(f"🔍 Biometric: {bio['protection_intensity']} intensity, "
                  f"{len(bio['applicable_biometrics'])} modalities, "
                  f"{len(bio['countermeasures'])} active countermeasures")
        else:
            print(f"🔍 Biometric: {components['biometric_countermeasures']['status']}")
    
    def save_customer_report(self, customer_id: str, filename: str = None):
        """Save customer protection report to file"""
        if filename is None:
            filename = f"privacy_report_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        report = self.generate_privacy_report(customer_id)
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"Report saved to: {filename}")
        return filename

def main():
    """Main demonstration function"""
    # Initialize the privacy protection suite
    suite = PrivacyProtectionSuite()
    
    # Demonstrate with all customers
    suite.demonstrate_all_customers()
    
    # Generate detailed reports for premium/enterprise customers
    print("\n" + "="*80)
    print("GENERATING DETAILED REPORTS FOR PREMIUM/ENTERPRISE CUSTOMERS")
    print("="*80)
    
    premium_customers = suite.customer_loader.get_customers_by_privacy_level("high") + \
                       suite.customer_loader.get_customers_by_privacy_level("maximum")
    
    for customer in premium_customers:
        customer_id = customer["customer_id"]
        print(f"\nGenerating detailed report for {customer['name']} ({customer_id})...")
        
        report_filename = suite.save_customer_report(customer_id)
        print(f"Report saved: {report_filename}")

if __name__ == "__main__":
    main()
