# Biometric Spoofing Countermeasures
# Generate countermeasures for biometric recognition based on customer preferences

import random
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from customer_loader import CustomerDataLoader

class BiometricCountermeasures:
    """Generate countermeasures for biometric recognition systems"""
    
    def __init__(self, customer_loader: CustomerDataLoader = None):
        self.customer_loader = customer_loader or CustomerDataLoader()
        
        # Facial landmark indices (68-point model)
        self.facial_landmarks = {
            'jaw_line': list(range(0, 17)),
            'right_eyebrow': list(range(17, 22)),
            'left_eyebrow': list(range(22, 27)),
            'nose_bridge': list(range(27, 31)),
            'nose_tip': list(range(31, 36)),
            'right_eye': list(range(36, 42)),
            'left_eye': list(range(42, 48)),
            'mouth_outer': list(range(48, 60)),
            'mouth_inner': list(range(60, 68))
        }
        
        # Biometric modalities
        self.biometric_types = [
            'facial_recognition', 'fingerprint', 'iris_scan', 'voice_print',
            'gait_analysis', 'hand_geometry', 'retinal_scan', 'palm_print',
            'ear_shape', 'keystroke_dynamics', 'behavioral_patterns'
        ]
        
        # Countermeasure techniques
        self.countermeasure_techniques = {
            'facial_recognition': ['landmark_modification', 'texture_variation', 'lighting_manipulation', 'geometric_distortion'],
            'fingerprint': ['ridge_pattern_variation', 'minutiae_modification', 'pressure_variation', 'temperature_masking'],
            'iris_scan': ['pupil_dilation', 'texture_overlay', 'reflection_manipulation', 'color_shift'],
            'voice_print': ['pitch_modulation', 'formant_shifting', 'noise_injection', 'prosody_alteration'],
            'gait_analysis': ['step_timing_variation', 'posture_modification', 'stride_length_change', 'ground_contact_pattern'],
            'keystroke_dynamics': ['typing_rhythm_variation', 'pressure_modulation', 'dwell_time_change', 'flight_time_alteration']
        }
    
    def get_customer_biometric_settings(self, customer_id: str) -> Dict:
        """Get biometric protection settings based on customer preferences"""
        customer_prefs = self.customer_loader.get_customer_preferences(customer_id)
        
        if not customer_prefs.get('biometric_protection', True):
            return {'enabled': False}
        
        privacy_level = customer_prefs.get('privacy_level', 'medium')
        service_tier = customer_prefs.get('service_tier', 'standard')
        device_types = customer_prefs.get('device_types', ['smartphone'])
        
        # Determine countermeasure intensity
        intensity_mapping = {
            'low': 'minimal',
            'medium': 'standard',
            'high': 'aggressive',
            'maximum': 'comprehensive'
        }
        
        intensity = intensity_mapping.get(privacy_level, 'standard')
        
        # Determine applicable biometric types based on devices
        applicable_biometrics = []
        for device in device_types:
            if device in ['smartphone', 'tablet']:
                applicable_biometrics.extend(['facial_recognition', 'fingerprint', 'voice_print'])
            elif device == 'laptop':
                applicable_biometrics.extend(['facial_recognition', 'keystroke_dynamics'])
            elif device == 'smartwatch':
                applicable_biometrics.extend(['gait_analysis', 'behavioral_patterns'])
        
        return {
            'enabled': True,
            'intensity': intensity,
            'applicable_biometrics': list(set(applicable_biometrics)),
            'continuous_protection': privacy_level in ['high', 'maximum'],
            'adaptive_countermeasures': service_tier in ['premium', 'enterprise'],
            'multi_modal_protection': privacy_level == 'maximum'
        }
    
    def generate_face_variation_map_for_customer(self, customer_id: str) -> Dict:
        """Create facial feature variation patterns for specific customer"""
        settings = self.get_customer_biometric_settings(customer_id)
        
        if not settings.get('enabled', True):
            return {'message': 'Biometric protection disabled for this customer'}
        
        if 'facial_recognition' not in settings.get('applicable_biometrics', []):
            return {'message': 'Facial recognition protection not applicable for customer devices'}
        
        return self.generate_face_variation_map(settings['intensity'], customer_id)
    
    def generate_face_variation_map(self, intensity: str = 'standard', customer_id: str = None) -> Dict:
        """Create facial feature variation patterns"""
        
        # Variation ranges based on intensity
        variation_ranges = {
            'minimal': {'landmark_offset': 1.0, 'lighting_range': 0.2, 'geometric_scale': 0.05},
            'standard': {'landmark_offset': 2.0, 'lighting_range': 0.4, 'geometric_scale': 0.1},
            'aggressive': {'landmark_offset': 3.5, 'lighting_range': 0.6, 'geometric_scale': 0.2},
            'comprehensive': {'landmark_offset': 5.0, 'lighting_range': 0.8, 'geometric_scale': 0.3}
        }
        
        ranges = variation_ranges.get(intensity, variation_ranges['standard'])
        
        variations = {
            'customer_id': customer_id,
            'intensity_level': intensity,
            'facial_landmarks': [],
            'lighting_adjustments': [],
            'geometric_transforms': [],
            'texture_modifications': [],
            'temporal_variations': []
        }
        
        # Generate facial landmark variations
        for landmark_id in range(68):
            feature_group = self.get_landmark_group(landmark_id)
            
            # More sensitive variations for key features
            sensitivity_multiplier = 1.5 if feature_group in ['right_eye', 'left_eye', 'nose_tip'] else 1.0
            
            variation = {
                'landmark_id': landmark_id,
                'feature_group': feature_group,
                'x_offset': random.uniform(-ranges['landmark_offset'] * sensitivity_multiplier, 
                                         ranges['landmark_offset'] * sensitivity_multiplier),
                'y_offset': random.uniform(-ranges['landmark_offset'] * sensitivity_multiplier, 
                                         ranges['landmark_offset'] * sensitivity_multiplier),
                'confidence': random.uniform(0.7, 1.0),
                'temporal_stability': random.uniform(0.5, 0.9)
            }
            variations['facial_landmarks'].append(variation)
        
        # Generate lighting adjustments
        lighting_zones = ['forehead', 'left_cheek', 'right_cheek', 'nose', 'chin', 'around_eyes']
        for zone in lighting_zones:
            lighting_adj = {
                'zone': zone,
                'brightness_delta': random.uniform(-ranges['lighting_range'], ranges['lighting_range']),
                'contrast_delta': random.uniform(-ranges['lighting_range'], ranges['lighting_range']),
                'saturation_delta': random.uniform(-ranges['lighting_range']/2, ranges['lighting_range']/2),
                'shadow_intensity': random.uniform(0.0, ranges['lighting_range'])
            }
            variations['lighting_adjustments'].append(lighting_adj)
        
        # Generate geometric transformations
        transform_types = ['rotation', 'scale', 'shear', 'perspective']
        for transform_type in transform_types:
            if transform_type == 'rotation':
                params = {'angle_degrees': random.uniform(-ranges['geometric_scale']*10, ranges['geometric_scale']*10)}
            elif transform_type == 'scale':
                params = {
                    'scale_x': random.uniform(1-ranges['geometric_scale'], 1+ranges['geometric_scale']),
                    'scale_y': random.uniform(1-ranges['geometric_scale'], 1+ranges['geometric_scale'])
                }
            elif transform_type == 'shear':
                params = {
                    'shear_x': random.uniform(-ranges['geometric_scale'], ranges['geometric_scale']),
                    'shear_y': random.uniform(-ranges['geometric_scale'], ranges['geometric_scale'])
                }
            else:  # perspective
                params = {
                    'perspective_strength': random.uniform(0, ranges['geometric_scale']),
                    'focal_point_x': random.uniform(0.3, 0.7),
                    'focal_point_y': random.uniform(0.3, 0.7)
                }
            
            transform = {
                'transform_type': transform_type,
                'parameters': params,
                'application_probability': random.uniform(0.3, 0.8)
            }
            variations['geometric_transforms'].append(transform)
        
        # Generate texture modifications for higher intensity levels
        if intensity in ['aggressive', 'comprehensive']:
            texture_mods = ['skin_smoothing', 'pore_enhancement', 'wrinkle_variation', 'color_shift']
            for mod_type in texture_mods:
                texture_mod = {
                    'modification_type': mod_type,
                    'intensity': random.uniform(0.1, 0.4),
                    'local_regions': random.sample(['forehead', 'cheeks', 'nose', 'chin'], 
                                                 k=random.randint(1, 3)),
                    'blending_factor': random.uniform(0.6, 0.9)
                }
                variations['texture_modifications'].append(texture_mod)
        
        # Generate temporal variations for continuous protection
        if intensity == 'comprehensive':
            for time_slot in range(24):  # Hourly variations
                temporal_var = {
                    'hour': time_slot,
                    'landmark_drift': random.uniform(0.1, 0.3),
                    'lighting_cycle': math.sin(time_slot * math.pi / 12) * 0.2,
                    'expression_bias': random.choice(['neutral', 'slight_smile', 'focused', 'relaxed']),
                    'micro_expression_rate': random.uniform(0.05, 0.15)
                }
                variations['temporal_variations'].append(temporal_var)
        
        variations['generation_timestamp'] = datetime.now().isoformat()
        return variations
    
    def get_landmark_group(self, landmark_id: int) -> str:
        """Get the facial feature group for a landmark ID"""
        for group_name, indices in self.facial_landmarks.items():
            if landmark_id in indices:
                return group_name
        return 'unknown'
    
    def generate_gait_modification_pattern(self, customer_id: str) -> Dict:
        """Create gait analysis countermeasures for specific customer"""
        settings = self.get_customer_biometric_settings(customer_id)
        
        if not settings.get('enabled', True):
            return {'message': 'Biometric protection disabled for this customer'}
        
        if 'gait_analysis' not in settings.get('applicable_biometrics', []):
            return {'message': 'Gait analysis protection not applicable for customer devices'}
        
        intensity = settings['intensity']
        
        # Intensity-based modification ranges
        modification_ranges = {
            'minimal': {'step_variance': 0.05, 'cadence_variance': 0.03, 'posture_variance': 0.02},
            'standard': {'step_variance': 0.1, 'cadence_variance': 0.05, 'posture_variance': 0.05},
            'aggressive': {'step_variance': 0.15, 'cadence_variance': 0.08, 'posture_variance': 0.1},
            'comprehensive': {'step_variance': 0.2, 'cadence_variance': 0.12, 'posture_variance': 0.15}
        }
        
        ranges = modification_ranges.get(intensity, modification_ranges['standard'])
        
        gait_params = {
            'customer_id': customer_id,
            'intensity_level': intensity,
            'step_modifications': {
                'step_length_variation': random.uniform(1-ranges['step_variance'], 1+ranges['step_variance']),
                'step_width_variation': random.uniform(1-ranges['step_variance']/2, 1+ranges['step_variance']/2),
                'step_height_variation': random.uniform(1-ranges['step_variance']/3, 1+ranges['step_variance']/3),
                'asymmetry_introduction': random.uniform(0, ranges['step_variance'])
            },
            'temporal_modifications': {
                'cadence_modification': random.uniform(1-ranges['cadence_variance'], 1+ranges['cadence_variance']),
                'stance_time_ratio': random.uniform(0.6-ranges['cadence_variance'], 0.8+ranges['cadence_variance']),
                'swing_phase_timing': random.uniform(0.3-ranges['cadence_variance'], 0.5+ranges['cadence_variance']),
                'double_support_time': random.uniform(0.1, 0.25)
            },
            'kinematic_modifications': {
                'ankle_angle_variation': random.uniform(-ranges['posture_variance']*10, ranges['posture_variance']*10),
                'knee_angle_variation': random.uniform(-ranges['posture_variance']*5, ranges['posture_variance']*5),
                'hip_angle_variation': random.uniform(-ranges['posture_variance']*8, ranges['posture_variance']*8),
                'pelvic_tilt_variation': random.uniform(-ranges['posture_variance']*3, ranges['posture_variance']*3)
            },
            'ground_contact_pattern': [random.uniform(0.2, 1.0) for _ in range(10)],
            'pressure_distribution': {
                'heel_strike': random.uniform(0.3, 0.7),
                'midfoot_contact': random.uniform(0.1, 0.4),
                'toe_off': random.uniform(0.4, 0.8),
                'medial_lateral_balance': random.uniform(0.4, 0.6)
            }
        }
        
        # Add environmental adaptations for comprehensive protection
        if intensity == 'comprehensive':
            gait_params['environmental_adaptations'] = {
                'surface_type_adjustments': {
                    'concrete': {'modification_factor': 1.0},
                    'carpet': {'modification_factor': 1.1},
                    'grass': {'modification_factor': 1.15},
                    'stairs': {'modification_factor': 1.3}
                },
                'speed_dependent_changes': {
                    'slow_walk': {'cadence_factor': 0.8, 'step_factor': 0.9},
                    'normal_walk': {'cadence_factor': 1.0, 'step_factor': 1.0},
                    'fast_walk': {'cadence_factor': 1.2, 'step_factor': 1.1}
                },
                'carrying_condition_effects': {
                    'no_load': {'posture_change': 1.0},
                    'backpack': {'posture_change': 1.05},
                    'handbag': {'posture_change': 1.02},
                    'briefcase': {'posture_change': 1.03}
                }
            }
        
        gait_params['generation_timestamp'] = datetime.now().isoformat()
        return gait_params
    
    def generate_keystroke_dynamics_variation(self, customer_id: str) -> Dict:
        """Generate keystroke dynamics countermeasures"""
        settings = self.get_customer_biometric_settings(customer_id)
        
        if not settings.get('enabled', True):
            return {'message': 'Biometric protection disabled for this customer'}
        
        if 'keystroke_dynamics' not in settings.get('applicable_biometrics', []):
            return {'message': 'Keystroke dynamics protection not applicable for customer devices'}
        
        intensity = settings['intensity']
        
        # Common key combinations and words for analysis
        test_sequences = [
            'password', 'username', 'the quick brown fox', '1234567890',
            'qwertyuiop', 'common', 'privacy', 'security'
        ]
        
        keystroke_variations = {
            'customer_id': customer_id,
            'intensity_level': intensity,
            'typing_patterns': [],
            'rhythm_modifications': {},
            'pressure_variations': {},
            'error_patterns': {}
        }
        
        # Generate variations for each test sequence
        for sequence in test_sequences:
            pattern_data = {
                'sequence': sequence,
                'dwell_times': [],  # Time key is held down
                'flight_times': [],  # Time between key releases and presses
                'pressure_values': [],
                'typing_speed_wpm': random.uniform(40, 80)
            }
            
            # Generate timing data for each character
            for i, char in enumerate(sequence):
                # Dwell time (key press duration)
                base_dwell = random.uniform(80, 150)  # milliseconds
                if intensity == 'comprehensive':
                    dwell_variation = random.uniform(0.7, 1.4)
                elif intensity == 'aggressive':
                    dwell_variation = random.uniform(0.8, 1.3)
                else:
                    dwell_variation = random.uniform(0.9, 1.2)
                
                dwell_time = base_dwell * dwell_variation
                pattern_data['dwell_times'].append(dwell_time)
                
                # Flight time (between keys)
                if i < len(sequence) - 1:
                    base_flight = random.uniform(50, 200)
                    flight_variation = dwell_variation  # Use similar variation
                    flight_time = base_flight * flight_variation
                    pattern_data['flight_times'].append(flight_time)
                
                # Pressure values (if supported)
                base_pressure = random.uniform(0.3, 0.8)
                pressure_variation = random.uniform(0.8, 1.2)
                pattern_data['pressure_values'].append(base_pressure * pressure_variation)
            
            keystroke_variations['typing_patterns'].append(pattern_data)
        
        # Generate rhythm modification parameters
        keystroke_variations['rhythm_modifications'] = {
            'burst_typing_probability': random.uniform(0.1, 0.3),
            'pause_insertion_rate': random.uniform(0.05, 0.15),
            'speed_variation_range': random.uniform(0.2, 0.4),
            'micro_pause_frequency': random.uniform(0.1, 0.25)
        }
        
        # Generate pressure variation parameters
        keystroke_variations['pressure_variations'] = {
            'pressure_range_multiplier': random.uniform(0.8, 1.3),
            'pressure_consistency': random.uniform(0.6, 0.9),
            'fatigue_simulation': intensity in ['aggressive', 'comprehensive'],
            'stress_response_simulation': intensity == 'comprehensive'
        }
        
        # Generate error pattern modifications
        keystroke_variations['error_patterns'] = {
            'backspace_frequency': random.uniform(0.02, 0.08),
            'correction_speed_factor': random.uniform(0.8, 1.2),
            'typo_insertion_rate': random.uniform(0.01, 0.04),
            'common_character_substitutions': {
                'a': ['s', 'q'], 'e': ['w', 'r'], 'i': ['u', 'o'],
                'o': ['i', 'p'], 'u': ['y', 'i']
            }
        }
        
        keystroke_variations['generation_timestamp'] = datetime.now().isoformat()
        return keystroke_variations
    
    def generate_voice_print_countermeasures(self, customer_id: str) -> Dict:
        """Generate voice print countermeasures"""
        settings = self.get_customer_biometric_settings(customer_id)
        
        if not settings.get('enabled', True):
            return {'message': 'Biometric protection disabled for this customer'}
        
        if 'voice_print' not in settings.get('applicable_biometrics', []):
            return {'message': 'Voice print protection not applicable for customer devices'}
        
        intensity = settings['intensity']
        
        voice_modifications = {
            'customer_id': customer_id,
            'intensity_level': intensity,
            'acoustic_modifications': {},
            'prosodic_variations': {},
            'linguistic_patterns': {},
            'environmental_factors': {}
        }
        
        # Acoustic modifications
        voice_modifications['acoustic_modifications'] = {
            'fundamental_frequency': {
                'pitch_shift_semitones': random.uniform(-2, 2) * (1 + (intensity == 'comprehensive')),
                'pitch_variability': random.uniform(0.8, 1.3),
                'vibrato_introduction': intensity in ['aggressive', 'comprehensive']
            },
            'formant_frequencies': {
                'f1_shift_hz': random.uniform(-50, 50),
                'f2_shift_hz': random.uniform(-100, 100),
                'f3_shift_hz': random.uniform(-150, 150),
                'formant_bandwidth_variation': random.uniform(0.9, 1.2)
            },
            'spectral_characteristics': {
                'harmonic_emphasis': random.uniform(0.8, 1.3),
                'noise_component_addition': random.uniform(0.0, 0.1),
                'spectral_tilt_modification': random.uniform(-2, 2)
            }
        }
        
        # Prosodic variations
        voice_modifications['prosodic_variations'] = {
            'rhythm_patterns': {
                'speech_rate_multiplier': random.uniform(0.85, 1.15),
                'pause_duration_variation': random.uniform(0.8, 1.4),
                'syllable_timing_jitter': random.uniform(0.02, 0.08)
            },
            'stress_patterns': {
                'stress_placement_variation': random.uniform(0.1, 0.3),
                'stress_intensity_modification': random.uniform(0.9, 1.2),
                'secondary_stress_introduction': random.uniform(0.1, 0.25)
            },
            'intonation_changes': {
                'contour_modification': random.choice(['rising', 'falling', 'plateau', 'variable']),
                'range_expansion_factor': random.uniform(0.9, 1.3),
                'declination_alteration': random.uniform(-0.1, 0.1)
            }
        }
        
        # Linguistic pattern modifications
        voice_modifications['linguistic_patterns'] = {
            'articulation_changes': {
                'consonant_precision': random.uniform(0.8, 1.2),
                'vowel_centralization': random.uniform(0.0, 0.2),
                'coarticulation_effects': random.uniform(0.9, 1.1)
            },
            'disfluency_introduction': {
                'filler_word_rate': random.uniform(0.01, 0.05),
                'hesitation_frequency': random.uniform(0.02, 0.06),
                'false_start_probability': random.uniform(0.01, 0.03)
            }
        }
        
        # Environmental factors simulation
        voice_modifications['environmental_factors'] = {
            'background_noise': {
                'noise_type': random.choice(['white', 'pink', 'brown', 'traffic', 'crowd']),
                'snr_db': random.uniform(15, 35),
                'dynamic_noise': intensity == 'comprehensive'
            },
            'recording_conditions': {
                'microphone_response_simulation': random.choice(['flat', 'bright', 'warm', 'compressed']),
                'room_acoustics': random.choice(['dry', 'reverberant', 'echoey', 'muffled']),
                'distance_variation': random.uniform(0.5, 2.0)  # meters
            }
        }
        
        voice_modifications['generation_timestamp'] = datetime.now().isoformat()
        return voice_modifications
    
    def generate_multi_modal_countermeasures(self, customer_id: str) -> Dict:
        """Generate comprehensive multi-modal biometric countermeasures"""
        settings = self.get_customer_biometric_settings(customer_id)
        
        if not settings.get('multi_modal_protection', False):
            return {'message': 'Multi-modal protection not enabled for this customer'}
        
        # Generate countermeasures for all applicable biometric types
        multi_modal_system = {
            'customer_id': customer_id,
            'protection_level': 'multi_modal_comprehensive',
            'synchronized_countermeasures': {},
            'adaptive_strategies': {},
            'coordination_matrix': {}
        }
        
        applicable_biometrics = settings.get('applicable_biometrics', [])
        
        # Generate countermeasures for each applicable biometric
        for biometric_type in applicable_biometrics:
            if biometric_type == 'facial_recognition':
                multi_modal_system['synchronized_countermeasures']['facial'] = self.generate_face_variation_map('comprehensive', customer_id)
            elif biometric_type == 'gait_analysis':
                multi_modal_system['synchronized_countermeasures']['gait'] = self.generate_gait_modification_pattern(customer_id)
            elif biometric_type == 'keystroke_dynamics':
                multi_modal_system['synchronized_countermeasures']['keystroke'] = self.generate_keystroke_dynamics_variation(customer_id)
            elif biometric_type == 'voice_print':
                multi_modal_system['synchronized_countermeasures']['voice'] = self.generate_voice_print_countermeasures(customer_id)
        
        # Generate adaptive strategies
        multi_modal_system['adaptive_strategies'] = {
            'threat_level_response': {
                'low_threat': 'minimal_countermeasures',
                'medium_threat': 'standard_countermeasures',
                'high_threat': 'aggressive_countermeasures',
                'critical_threat': 'maximum_countermeasures'
            },
            'context_awareness': {
                'location_based_adjustments': True,
                'time_based_variations': True,
                'device_specific_optimization': True,
                'usage_pattern_adaptation': True
            },
            'learning_mechanisms': {
                'effectiveness_tracking': True,
                'countermeasure_refinement': True,
                'false_positive_minimization': True,
                'performance_optimization': True
            }
        }
        
        # Generate coordination matrix for synchronized protection
        coordination_pairs = []
        for i, bio1 in enumerate(applicable_biometrics):
            for bio2 in applicable_biometrics[i+1:]:
                coordination_pairs.append((bio1, bio2))
        
        for bio1, bio2 in coordination_pairs:
            coordination_key = f"{bio1}_{bio2}"
            multi_modal_system['coordination_matrix'][coordination_key] = {
                'synchronization_level': random.uniform(0.7, 0.95),
                'mutual_reinforcement': random.uniform(0.6, 0.9),
                'conflict_resolution_strategy': random.choice(['priority_based', 'weighted_average', 'adaptive_blend']),
                'timing_coordination': random.uniform(0.8, 1.0)
            }
        
        multi_modal_system['generation_timestamp'] = datetime.now().isoformat()
        return multi_modal_system

# Example usage and testing
def demo_biometric_countermeasures():
    """Demonstrate the biometric countermeasures system with customer data"""
    print("=== Biometric Countermeasures System Demo ===")
    
    # Initialize system
    bio_counter = BiometricCountermeasures()
    
    # Test with specific customers
    customers_to_test = ["CUST_001", "CUST_003", "CUST_005"]
    
    for customer_id in customers_to_test:
        print(f"\n--- Customer {customer_id} ---")
        
        # Get biometric settings
        settings = bio_counter.get_customer_biometric_settings(customer_id)
        print(f"Biometric protection enabled: {settings.get('enabled', False)}")
        
        if settings.get('enabled'):
            print(f"Protection intensity: {settings['intensity']}")
            print(f"Applicable biometrics: {', '.join(settings['applicable_biometrics'])}")
            
            # Test facial recognition countermeasures
            if 'facial_recognition' in settings['applicable_biometrics']:
                face_vars = bio_counter.generate_face_variation_map_for_customer(customer_id)
                if 'facial_landmarks' in face_vars:
                    print(f"Facial variations: {len(face_vars['facial_landmarks'])} landmarks, "
                          f"{len(face_vars['lighting_adjustments'])} lighting zones")
            
            # Test gait analysis countermeasures
            if 'gait_analysis' in settings['applicable_biometrics']:
                gait_mods = bio_counter.generate_gait_modification_pattern(customer_id)
                if 'step_modifications' in gait_mods:
                    print(f"Gait modifications: step variance {gait_mods['step_modifications']['step_length_variation']:.3f}")
            
            # Test keystroke dynamics countermeasures
            if 'keystroke_dynamics' in settings['applicable_biometrics']:
                keystroke_vars = bio_counter.generate_keystroke_dynamics_variation(customer_id)
                if 'typing_patterns' in keystroke_vars:
                    print(f"Keystroke variations: {len(keystroke_vars['typing_patterns'])} test sequences")
            
            # Test voice print countermeasures
            if 'voice_print' in settings['applicable_biometrics']:
                voice_mods = bio_counter.generate_voice_print_countermeasures(customer_id)
                if 'acoustic_modifications' in voice_mods:
                    pitch_shift = voice_mods['acoustic_modifications']['fundamental_frequency']['pitch_shift_semitones']
                    print(f"Voice modifications: pitch shift {pitch_shift:.2f} semitones")
            
            # Test multi-modal protection for maximum privacy customers
            customer_prefs = bio_counter.customer_loader.get_customer_preferences(customer_id)
            if customer_prefs.get('privacy_level') == 'maximum':
                multi_modal = bio_counter.generate_multi_modal_countermeasures(customer_id)
                if 'synchronized_countermeasures' in multi_modal:
                    print(f"Multi-modal protection: {len(multi_modal['synchronized_countermeasures'])} biometric types")

if __name__ == "__main__":
    demo_biometric_countermeasures()