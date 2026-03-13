#!/usr/bin/env python3
"""
Bioluminescence Data Analyzer
A Python script to analyze patterns in bioluminescent organisms and their biochemical mechanisms.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter, defaultdict
import seaborn as sns

def load_bioluminescence_data():
    """Load the bioluminescent organisms database."""
    try:
        with open('bioluminescent_organisms_database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Database file not found. Please ensure bioluminescent_organisms_database.json exists.")
        return None

def analyze_wavelength_distribution(data):
    """Analyze the distribution of bioluminescent wavelengths."""
    wavelengths = []
    colors = []
    names = []
    
    for org in data['organisms']:
        wavelength = org['bioluminescence']['wavelength_nm']
        color = org['bioluminescence']['color']
        name = org['common_name']
        
        wavelengths.append(wavelength)
        colors.append(color)
        names.append(name)
    
    return wavelengths, colors, names

def analyze_environments(data):
    """Analyze the distribution of organisms across different environments."""
    environments = []
    for org in data['organisms']:
        env = org['environment'].split(' - ')[0]  # Get main environment type
        environments.append(env)
    
    return Counter(environments)

def analyze_luciferin_types(data):
    """Analyze the distribution of different luciferin types."""
    luciferins = []
    for org in data['organisms']:
        luciferin = org['bioluminescence']['luciferin_type']
        luciferins.append(luciferin)
    
    return Counter(luciferins)

def create_wavelength_spectrum_plot(wavelengths, colors, names):
    """Create a visualization of bioluminescent wavelengths on the visible spectrum."""
    plt.figure(figsize=(14, 8))
    
    # Create spectrum background
    spectrum_wavelengths = np.linspace(380, 750, 100)
    spectrum_colors = []
    
    for wl in spectrum_wavelengths:
        if wl < 450:
            # Violet to Blue
            r, g, b = (450-wl)/70, 0, 1
        elif wl < 495:
            # Blue to Cyan
            r, g, b = 0, (wl-450)/45, 1
        elif wl < 570:
            # Cyan to Green
            r, g, b = 0, 1, (570-wl)/75
        elif wl < 590:
            # Green to Yellow
            r, g, b = (wl-570)/20, 1, 0
        elif wl < 620:
            # Yellow to Orange
            r, g, b = 1, (620-wl)/30, 0
        else:
            # Orange to Red
            r, g, b = 1, 0, 0
        
        spectrum_colors.append((r, g, b))
    
    # Plot spectrum background
    for i, (wl, color) in enumerate(zip(spectrum_wavelengths, spectrum_colors)):
        plt.axvline(x=wl, color=color, alpha=0.3, linewidth=2)
    
    # Plot organism wavelengths
    for i, (wl, name) in enumerate(zip(wavelengths, names)):
        plt.axvline(x=wl, color='black', linewidth=3, alpha=0.8)
        plt.scatter(wl, i+1, s=200, c='white', edgecolor='black', linewidth=2, zorder=5)
        plt.text(wl, i+1.3, name, rotation=45, ha='left', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xlim(380, 750)
    plt.ylim(0, len(wavelengths)+2)
    plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold')
    plt.ylabel('Organisms', fontsize=14, fontweight='bold')
    plt.title('Bioluminescent Wavelengths on the Visible Spectrum', fontsize=16, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Add color labels
    color_regions = [
        (400, 'Violet'), (450, 'Blue'), (495, 'Green'), 
        (570, 'Yellow'), (590, 'Orange'), (620, 'Red')
    ]
    for wl, label in color_regions:
        plt.text(wl, len(wavelengths)+1.5, label, ha='center', va='center', 
                fontsize=12, fontweight='bold', 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('bioluminescence_spectrum.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_environment_distribution_plot(env_counts):
    """Create a pie chart of organism distribution across environments."""
    plt.figure(figsize=(10, 8))
    
    colors_map = {
        'Marine': '#1f77b4',
        'Terrestrial': '#2ca02c', 
        'Deep sea': '#9467bd'
    }
    
    colors = [colors_map.get(env, '#ff7f0e') for env in env_counts.keys()]
    
    plt.pie(env_counts.values(), labels=env_counts.keys(), autopct='%1.1f%%',
            startangle=90, colors=colors, explode=[0.1 if count == max(env_counts.values()) else 0 for count in env_counts.values()])
    plt.title('Distribution of Bioluminescent Organisms by Environment', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.savefig('environment_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_luciferin_analysis_plot(luciferin_counts, data):
    """Create a bar chart showing luciferin types and their properties."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Luciferin type distribution
    ax1.bar(range(len(luciferin_counts)), list(luciferin_counts.values()), 
            color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    ax1.set_xticks(range(len(luciferin_counts)))
    ax1.set_xticklabels(list(luciferin_counts.keys()), rotation=45, ha='right')
    ax1.set_ylabel('Number of Organisms', fontweight='bold')
    ax1.set_title('Distribution of Luciferin Types', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Wavelength vs Environment scatter plot
    wavelengths = []
    environments = []
    organism_names = []
    
    for org in data['organisms']:
        wavelengths.append(org['bioluminescence']['wavelength_nm'])
        env = org['environment'].split(' - ')[0]
        environments.append(env)
        organism_names.append(org['common_name'])
    
    env_colors = {'Marine': '#1f77b4', 'Terrestrial': '#2ca02c', 'Deep sea': '#9467bd'}
    
    for env in set(environments):
        env_wavelengths = [w for w, e in zip(wavelengths, environments) if e == env]
        env_y = [environments.index(env) + 1 + np.random.normal(0, 0.1) for _ in env_wavelengths]
        ax2.scatter(env_wavelengths, env_y, c=env_colors.get(env, '#ff7f0e'), 
                   label=env, s=100, alpha=0.7, edgecolors='black')
    
    ax2.set_xlabel('Wavelength (nm)', fontweight='bold')
    ax2.set_ylabel('Environment', fontweight='bold')
    ax2.set_title('Wavelength Distribution by Environment', fontweight='bold')
    ax2.set_yticks([1, 2, 3])
    ax2.set_yticklabels(list(set(environments)))
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('luciferin_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_biochemistry_summary(data):
    """Generate a summary of biochemical mechanisms."""
    print("\n" + "="*60)
    print("BIOLUMINESCENCE BIOCHEMISTRY SUMMARY")
    print("="*60)
    
    print(f"\nGeneral Reaction:")
    print(f"  {data['biochemical_mechanisms']['general_reaction']}")
    
    print(f"\nLuciferin Types Found:")
    for luciferin_type, details in data['biochemical_mechanisms']['luciferin_types'].items():
        print(f"  • {luciferin_type.replace('_', '-').title()}:")
        print(f"    Formula: {details['chemical_formula']}")
        print(f"    Found in: {', '.join(details['found_in'])}")
        print(f"    Structure: {details['structure']}")
        print()
    
    print(f"Evolutionary Insights:")
    print(f"  • {data['evolutionary_insights']['convergent_evolution']}")
    print(f"  • {data['evolutionary_insights']['marine_dominance']}")
    print(f"  • Functions: {', '.join(data['evolutionary_insights']['functions'])}")

def main():
    """Main analysis function."""
    print("🌟 Bioluminescence Data Analyzer 🌟")
    print("Loading database...")
    
    data = load_bioluminescence_data()
    if not data:
        return
    
    print(f"Loaded data for {len(data['organisms'])} bioluminescent organisms")
    
    # Analyze data
    wavelengths, colors, names = analyze_wavelength_distribution(data)
    env_counts = analyze_environments(data)
    luciferin_counts = analyze_luciferin_types(data)
    
    print(f"\nWavelength range: {min(wavelengths)}-{max(wavelengths)} nm")
    print(f"Most common environment: {env_counts.most_common(1)[0][0]}")
    print(f"Most common luciferin: {luciferin_counts.most_common(1)[0][0]}")
    
    # Create visualizations
    print("\nGenerating visualizations...")
    create_wavelength_spectrum_plot(wavelengths, colors, names)
    create_environment_distribution_plot(env_counts)
    create_luciferin_analysis_plot(luciferin_counts, data)
    
    # Generate summary
    generate_biochemistry_summary(data)
    
    print(f"\n✨ Analysis complete! Visualizations saved as PNG files.")

if __name__ == "__main__":
    main()