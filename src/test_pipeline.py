"""
Test pipeline on Taipei only to validate functionality.
"""

import os
import sys
import warnings
warnings.filterwarnings('ignore')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from run_full_analysis import run_city_analysis, compile_academic_paper
from core.data_loader import DataLoader
from analyzers.comparison_analyzer import CrossCityComparisonAnalyzer
from config import analysis_config as config

print("="*80)
print("TESTING PIPELINE ON TAIPEI")
print("="*80)

# Load Taipei data
loader = DataLoader()
df_taipei, metadata = loader.load_city_data('taipei', preprocess=True)

# Run all analyses on Taipei
taipei_results = run_city_analysis('taipei', df_taipei)

print("\n✓ Test complete!")
print(f"\nGenerated outputs in:")
for analysis_type in ['statistical', 'pca_clustering', 'lag_rolling']:
    output_dir = config.get_city_output_dir('taipei', analysis_type)
    print(f"  - {output_dir}")
