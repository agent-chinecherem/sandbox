#!/usr/bin/env python3
"""
Mathematical Music Analysis Tool
Exploring the deep mathematical relationships in musical harmony across cultures
"""

import math
import numpy as np
import json
from fractions import Fraction
from typing import Dict, List, Tuple

class MusicalMathematics:
    """
    A comprehensive toolkit for analyzing mathematical relationships in music.
    """
    
    def __init__(self):
        # Define fundamental musical ratios
        self.perfect_ratios = {
            'unison': (1, 1),
            'octave': (2, 1),
            'perfect_fifth': (3, 2),
            'perfect_fourth': (4, 3),
            'major_third_just': (5, 4),
            'minor_third_just': (6, 5),
            'major_sixth_just': (5, 3),
            'minor_sixth_just': (8, 5),
            'major_seventh_just': (15, 8),
            'minor_seventh_just': (16, 9)
        }
        
        # Cultural scale systems with their mathematical properties
        self.scale_systems = {
            'western_12tet': {
                'name': 'Western 12-Tone Equal Temperament',
                'cents_per_step': 100,
                'steps_per_octave': 12,
                'mathematical_basis': 'Equal division of octave',
                'advantages': 'Perfect transposition, modulation freedom',
                'disadvantages': 'Slightly impure intervals except octave'
            },
            'just_intonation': {
                'name': 'Just Intonation',
                'ratios': [1, 16/15, 9/8, 6/5, 5/4, 4/3, 45/32, 3/2, 8/5, 5/3, 16/9, 15/8, 2],
                'mathematical_basis': 'Perfect integer ratios',
                'advantages': 'Pure consonant intervals, no beating',
                'disadvantages': 'Key-dependent, complex modulation'
            },
            'pythagorean': {
                'name': 'Pythagorean Tuning',
                'generation_ratio': 3/2,
                'mathematical_basis': 'Generated from perfect fifths',
                'wolf_fifth': 'One severely diminished fifth',
                'cents_major_third': 408  # Notably different from just 386
            },
            'arabic_24tet': {
                'name': 'Arabic 24-Tone Equal Temperament',
                'cents_per_step': 50,  # Quarter-tones
                'steps_per_octave': 24,
                'neutral_intervals': True,
                'mathematical_basis': 'Quarter-tone equal division'
            },
            'chinese_pentatonic': {
                'name': 'Chinese Pentatonic',
                'ratios': [1, 9/8, 5/4, 3/2, 27/16, 2],
                'mathematical_basis': 'Built on perfect fifths',
                'cultural_significance': 'Avoids tritone, emphasizes consonance'
            }
        }

    def frequency_to_cents(self, freq1: float, freq2: float) -> float:
        """Convert frequency ratio to cents."""
        return 1200 * math.log2(freq2 / freq1)
    
    def cents_to_ratio(self, cents: float) -> float:
        """Convert cents to frequency ratio."""
        return 2 ** (cents / 1200)
    
    def ratio_to_cents(self, numerator: int, denominator: int) -> float:
        """Convert integer ratio to cents."""
        return self.frequency_to_cents(denominator, numerator)
    
    def find_simplest_ratio(self, frequency_ratio: float, max_denominator: int = 32) -> Tuple[int, int]:
        """
        Find the simplest integer ratio approximating a frequency ratio.
        Uses continued fractions for optimal approximation.
        """
        frac = Fraction(frequency_ratio).limit_denominator(max_denominator)
        return (frac.numerator, frac.denominator)
    
    def analyze_consonance(self, ratio: Tuple[int, int]) -> Dict:
        """
        Analyze consonance based on mathematical complexity.
        Lower integers in ratios tend to sound more consonant.
        """
        num, den = ratio
        complexity = num + den
        lcm = (num * den) // math.gcd(num, den)
        
        consonance_levels = {
            (1, 1): "Perfect Consonance",
            (2, 1): "Perfect Consonance", 
            (3, 2): "Perfect Consonance",
            (4, 3): "Perfect Consonance",
            (5, 4): "Imperfect Consonance",
            (6, 5): "Imperfect Consonance",
            (5, 3): "Imperfect Consonance",
            (8, 5): "Imperfect Consonance"
        }
        
        consonance = consonance_levels.get(ratio, "Dissonant" if complexity > 12 else "Mild Dissonance")
        
        return {
            'ratio': f"{num}:{den}",
            'complexity': complexity,
            'lcm': lcm,
            'consonance': consonance,
            'cents': self.ratio_to_cents(num, den),
            'mathematical_explanation': f"Waveforms align every {lcm} cycles"
        }
    
    def generate_harmonic_series(self, fundamental: float, harmonics: int = 16) -> List[Dict]:
        """Generate harmonic series with mathematical analysis."""
        series = []
        
        for n in range(1, harmonics + 1):
            frequency = fundamental * n
            ratio = (n, 1)
            interval_from_fundamental = self.frequency_to_cents(fundamental, frequency)
            
            # Find interval from previous harmonic
            if n > 1:
                interval_from_previous = self.frequency_to_cents(fundamental * (n-1), frequency)
                prev_ratio = (n, n-1)
            else:
                interval_from_previous = 0
                prev_ratio = (1, 1)
            
            series.append({
                'harmonic_number': n,
                'frequency': frequency,
                'ratio_from_fundamental': f"{n}:1",
                'ratio_from_previous': f"{prev_ratio[0]}:{prev_ratio[1]}",
                'cents_from_fundamental': interval_from_fundamental,
                'cents_from_previous': interval_from_previous,
                'musical_significance': self.get_harmonic_significance(n)
            })
        
        return series
    
    def get_harmonic_significance(self, harmonic_num: int) -> str:
        """Get musical significance of harmonic numbers."""
        significance = {
            1: "Fundamental frequency",
            2: "Octave - defines pitch class",
            3: "Perfect fifth - most important consonance after octave", 
            4: "Double octave",
            5: "Major third - defines major quality",
            6: "Perfect fifth + octave",
            7: "Septimal minor seventh - not in 12-TET",
            8: "Triple octave",
            9: "Major ninth - compound major second",
            10: "Major third + double octave",
            11: "Undecimal tritone - microtonal",
            12: "Perfect fifth + double octave",
            13: "Tridecimal sixth - microtonal",
            14: "Septimal minor seventh + octave",
            15: "Major seventh - leading tone",
            16: "Quadruple octave"
        }
        
        return significance.get(harmonic_num, f"Complex harmonic relationship")
    
    def compare_tuning_systems(self, note_ratios: List[float]) -> Dict:
        """Compare how different tuning systems handle the same scale."""
        results = {}
        
        for system_name, system_data in self.scale_systems.items():
            if 'ratios' in system_data:
                ratios = system_data['ratios']
            elif system_name == 'western_12tet':
                # Generate 12-TET ratios
                ratios = [2**(i/12) for i in range(13)]
            elif system_name == 'arabic_24tet':
                # Generate 24-TET ratios (showing subset)
                ratios = [2**(i/24) for i in range(0, 25, 2)]  # Every quarter-tone
            else:
                continue
                
            results[system_name] = {
                'name': system_data['name'],
                'ratios': ratios[:len(note_ratios)],
                'cents': [self.frequency_to_cents(1, r) for r in ratios[:len(note_ratios)]],
                'deviations_from_just': []
            }
            
            # Calculate deviations from just intonation
            just_ratios = self.scale_systems['just_intonation']['ratios']
            for i, ratio in enumerate(ratios[:len(just_ratios)]):
                if i < len(just_ratios):
                    deviation = self.frequency_to_cents(just_ratios[i], ratio)
                    results[system_name]['deviations_from_just'].append(deviation)
        
        return results
    
    def analyze_cultural_scale(self, scale_name: str, root_frequency: float = 261.63) -> Dict:
        """Deep analysis of a cultural scale system."""
        if scale_name not in self.scale_systems:
            return {'error': 'Scale system not found'}
        
        system = self.scale_systems[scale_name]
        analysis = {
            'name': system['name'],
            'mathematical_basis': system['mathematical_basis'],
            'frequencies': [],
            'intervals': [],
            'consonance_analysis': [],
            'cultural_context': {}
        }
        
        # Generate frequencies based on system type
        if 'ratios' in system:
            frequencies = [root_frequency * ratio for ratio in system['ratios']]
        elif 'cents_per_step' in system:
            steps = system['steps_per_octave']
            frequencies = [root_frequency * 2**(i * system['cents_per_step'] / 1200) 
                         for i in range(steps + 1)]
        else:
            return analysis
        
        analysis['frequencies'] = frequencies
        
        # Analyze intervals between adjacent notes
        for i in range(1, len(frequencies)):
            interval_cents = self.frequency_to_cents(frequencies[i-1], frequencies[i])
            ratio = self.find_simplest_ratio(frequencies[i] / frequencies[i-1])
            consonance = self.analyze_consonance(ratio)
            
            analysis['intervals'].append({
                'from_note': i-1,
                'to_note': i,
                'cents': interval_cents,
                'ratio': ratio,
                'consonance': consonance['consonance']
            })
        
        # Cultural and mathematical insights
        if scale_name == 'chinese_pentatonic':
            analysis['cultural_context'] = {
                'philosophy': 'Based on cosmic harmony, five elements',
                'mathematical_beauty': 'No tritone, all intervals are consonant',
                'generation_method': 'Built by stacking perfect fifths'
            }
        elif scale_name == 'arabic_24tet':
            analysis['cultural_context'] = {
                'neutral_intervals': 'Quarter-tones create neutral thirds and sixths',
                'maqam_system': 'Enables complex melodic modes impossible in 12-TET',
                'microtonal_expression': 'Allows subtle emotional inflections'
            }
        elif scale_name == 'just_intonation':
            analysis['cultural_context'] = {
                'historical_importance': 'Natural resonance of acoustic instruments',
                'mathematical_purity': 'Perfect integer ratios eliminate beating',
                'limitations': 'Key-dependent, comma problems in modulation'
            }
        
        return analysis
    
    def calculate_beating_frequency(self, freq1: float, freq2: float) -> float:
        """
        Calculate beating frequency between two close pitches.
        Beating occurs when frequencies are close but not identical.
        """
        return abs(freq1 - freq2)
    
    def analyze_chord_harmony(self, frequencies: List[float]) -> Dict:
        """Analyze the harmonic content of a chord."""
        analysis = {
            'frequencies': frequencies,
            'intervals': [],
            'overall_consonance': 0,
            'harmonic_relationships': []
        }
        
        # Analyze all interval pairs in the chord
        consonance_scores = []
        
        for i in range(len(frequencies)):
            for j in range(i+1, len(frequencies)):
                ratio = frequencies[j] / frequencies[i]
                simple_ratio = self.find_simplest_ratio(ratio)
                consonance_analysis = self.analyze_consonance(simple_ratio)
                
                # Assign numerical consonance scores
                score_map = {
                    "Perfect Consonance": 5,
                    "Imperfect Consonance": 3,
                    "Mild Dissonance": 1,
                    "Dissonant": 0
                }
                
                score = score_map.get(consonance_analysis['consonance'], 0)
                consonance_scores.append(score)
                
                analysis['intervals'].append({
                    'note1_index': i,
                    'note2_index': j,
                    'frequency_ratio': ratio,
                    'simple_ratio': simple_ratio,
                    'consonance': consonance_analysis['consonance'],
                    'cents': consonance_analysis['cents']
                })
        
        analysis['overall_consonance'] = sum(consonance_scores) / len(consonance_scores) if consonance_scores else 0
        
        return analysis

def main():
    """Demonstrate the mathematical music analysis capabilities."""
    music_math = MusicalMathematics()
    
    print("🎵 Mathematical Music Analysis")
    print("=" * 50)
    
    # 1. Analyze perfect ratios
    print("\n1. Perfect Consonant Ratios:")
    for name, ratio in music_math.perfect_ratios.items():
        analysis = music_math.analyze_consonance(ratio)
        print(f"   {name.replace('_', ' ').title()}: {analysis['ratio']} = {analysis['cents']:.1f} cents")
    
    # 2. Generate and analyze harmonic series
    print("\n2. Harmonic Series Analysis (A3 = 220 Hz):")
    harmonics = music_math.generate_harmonic_series(220, 8)
    for h in harmonics:
        print(f"   H{h['harmonic_number']}: {h['frequency']:.2f} Hz - {h['musical_significance']}")
    
    # 3. Compare tuning systems
    print("\n3. Tuning System Comparison (Major Scale):")
    comparison = music_math.compare_tuning_systems([1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2])
    
    for system_name, data in comparison.items():
        print(f"\n   {data['name']}:")
        major_third_cents = data['cents'][2] if len(data['cents']) > 2 else 0
        perfect_fifth_cents = data['cents'][4] if len(data['cents']) > 4 else 0
        print(f"     Major Third: {major_third_cents:.1f} cents")
        print(f"     Perfect Fifth: {perfect_fifth_cents:.1f} cents")
    
    # 4. Analyze cultural scales
    print("\n4. Cultural Scale Analysis:")
    
    scales_to_analyze = ['chinese_pentatonic', 'arabic_24tet', 'just_intonation']
    for scale in scales_to_analyze:
        analysis = music_math.analyze_cultural_scale(scale)
        print(f"\n   {analysis['name']}:")
        print(f"     Mathematical Basis: {analysis['mathematical_basis']}")
        if 'cultural_context' in analysis and analysis['cultural_context']:
            for key, value in analysis['cultural_context'].items():
                print(f"     {key.replace('_', ' ').title()}: {value}")
    
    # 5. Chord harmony analysis
    print("\n5. Chord Harmony Analysis:")
    
    # C Major triad in just intonation: C, E, G
    c_major_just = [261.63, 327.04, 392.44]  # C4, E4, G4 in just intonation
    chord_analysis = music_math.analyze_chord_harmony(c_major_just)
    print(f"   C Major Triad (Just Intonation):")
    print(f"     Overall Consonance Score: {chord_analysis['overall_consonance']:.1f}/5.0")
    
    # Minor chord
    c_minor_just = [261.63, 313.96, 392.44]  # C4, Eb4, G4
    chord_analysis_minor = music_math.analyze_chord_harmony(c_minor_just)
    print(f"   C Minor Triad (Just Intonation):")
    print(f"     Overall Consonance Score: {chord_analysis_minor['overall_consonance']:.1f}/5.0")
    
    print(f"\n🎼 Analysis complete! The mathematical beauty of music revealed.")

if __name__ == "__main__":
    main()