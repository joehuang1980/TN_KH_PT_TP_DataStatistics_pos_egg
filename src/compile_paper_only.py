#!/usr/bin/env python3
"""
Compile academic paper from existing analysis results.
"""

import os
from config import analysis_config as config

def compile_paper():
    """Compile methods and results from all analyses into final paper."""

    # Create compiled_paper directory
    paper_dir = os.path.join(config.OUTPUT_DIR, 'compiled_paper')
    os.makedirs(paper_dir, exist_ok=True)

    print("="*80)
    print("COMPILING ACADEMIC PAPER")
    print("="*80)
    print()

    # =======================
    # COMPILE METHODS SECTION
    # =======================

    methods_sections = []

    # Introduction
    methods_sections.append("# Methods\n")
    methods_sections.append(
        "## Study Design and Data Collection\n\n"
        "This multi-city surveillance study analyzed ovitrap-based mosquito monitoring data from four "
        "cities in Taiwan: Taipei, Kaohsiung, Pingtung, and Tainan. Data included 175 "
        "environmental and demographic features and two outcome variables: ovitrap positive "
        "rate (POS) and average egg count (EGG).\n"
    )

    # Read methods from each analysis type (using Taipei as template)
    methods_files = [
        ('Statistical Correlation Analysis', 'output/taipei/statistical/methods.md'),
        ('Dimensionality Reduction and Clustering', 'output/taipei/pca_clustering/methods.md'),
        ('Temporal Lag Analysis', 'output/taipei/lag_rolling/methods.md'),
        ('Cross-City Comparison', 'output/comparison/methods.md')
    ]

    for title, filepath in methods_files:
        methods_sections.append(f"\n## {title}\n")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
                # Remove the first "# Methods" line if present
                lines = content.split('\n')
                if lines and lines[0].startswith('# Methods'):
                    content = '\n'.join(lines[1:])
                methods_sections.append(content)
        else:
            methods_sections.append(f"*Methods file not found: {filepath}*\n")

    # Save full methods
    full_methods = "\n".join(methods_sections)
    methods_path = os.path.join(paper_dir, 'full_methods.md')
    with open(methods_path, 'w') as f:
        f.write(full_methods)

    print(f"✓ Saved: full_methods.md ({len(full_methods)} characters)")

    # =======================
    # COMPILE RESULTS SECTION
    # =======================

    results_sections = []
    results_sections.append("# Results\n")

    # Add city-specific results
    for city_key in config.CITY_ORDER:
        city_name = config.CITIES[city_key]['name_en']
        results_sections.append(f"\n## {city_name}\n")

        # Read results from each analysis type
        city_results_files = [
            ('Statistical Analysis', f'output/{city_key}/statistical/results.md'),
            ('PCA and Clustering', f'output/{city_key}/pca_clustering/results.md'),
            ('Temporal Lag Analysis', f'output/{city_key}/lag_rolling/results.md')
        ]

        for subtitle, filepath in city_results_files:
            results_sections.append(f"\n### {subtitle}\n")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = f.read()
                    # Remove headers
                    lines = content.split('\n')
                    # Skip lines that start with # or ##
                    filtered_lines = [line for line in lines if not line.startswith('# ')]
                    content = '\n'.join(filtered_lines)
                    results_sections.append(content)
            else:
                results_sections.append(f"*Results file not found: {filepath}*\n")

    # Add cross-city comparison results
    results_sections.append("\n## Cross-City Comparison\n")
    comp_results_path = 'output/comparison/results.md'
    if os.path.exists(comp_results_path):
        with open(comp_results_path, 'r') as f:
            content = f.read()
            # Remove headers
            lines = content.split('\n')
            filtered_lines = [line for line in lines if not line.startswith('# ')]
            content = '\n'.join(filtered_lines)
            results_sections.append(content)
    else:
        results_sections.append(f"*Comparison results file not found*\n")

    # Save full results
    full_results = "\n".join(results_sections)
    results_path = os.path.join(paper_dir, 'full_results.md')
    with open(results_path, 'w') as f:
        f.write(full_results)

    print(f"✓ Saved: full_results.md ({len(full_results)} characters)")

    # =======================
    # CREATE README
    # =======================

    readme_content = f"""# Compiled Academic Paper

This directory contains the compiled academic paper sections generated from the multi-city mosquito surveillance analysis.

## Files

- **full_methods.md**: Complete Methods section covering all analyses
- **full_results.md**: Complete Results section for all 4 cities and cross-city comparison

## Structure

### Methods Section
1. Study Design and Data Collection
2. Statistical Correlation Analysis
3. Dimensionality Reduction and Clustering
4. Temporal Lag Analysis
5. Cross-City Comparison

### Results Section
1. Taipei
   - Statistical Analysis
   - PCA and Clustering
   - Temporal Lag Analysis
2. Kaohsiung
   - Statistical Analysis
   - PCA and Clustering
   - Temporal Lag Analysis
3. Pingtung
   - Statistical Analysis
   - PCA and Clustering
   - Temporal Lag Analysis
4. Tainan
   - Statistical Analysis
   - PCA and Clustering
   - Temporal Lag Analysis
5. Cross-City Comparison

## Source Data

Generated from analysis outputs in:
- output/taipei/
- output/kaohsiung/
- output/pingtung/
- output/tainan/
- output/comparison/

## Date Generated

{os.popen('date').read().strip()}
"""

    readme_path = os.path.join(paper_dir, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"✓ Saved: README.md")
    print()
    print("="*80)
    print("PAPER COMPILATION COMPLETE")
    print("="*80)
    print(f"\nCompiled paper files saved to: {paper_dir}")
    print(f"  - full_methods.md")
    print(f"  - full_results.md")
    print(f"  - README.md")
    print()

if __name__ == '__main__':
    compile_paper()
