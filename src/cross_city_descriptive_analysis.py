"""
Cross-city descriptive statistics and comparison analysis.

This script calculates:
1. Complete descriptive statistics for POS/EGG (mean, median, SD, IQR, min-max)
2. Data collection time range for each city
3. Kruskal-Wallis H-test for cross-city comparison
4. Dunn's post-hoc pairwise comparison with Bonferroni correction

Output: CSV and Markdown tables
"""

import pandas as pd
import numpy as np
from scipy import stats
import scikit_posthocs as sp
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import analysis_config as config


def load_city_data():
    """
    Load raw data from all four cities.

    Returns
    -------
    dict
        Dictionary with city_key as key and DataFrame as value
    """
    city_data = {}

    print("Loading city data...")
    for city_key in config.CITY_ORDER:
        city_info = config.CITIES[city_key]
        path = city_info['path']

        if not os.path.exists(path):
            print(f"  Warning: {city_info['name_en']} data file not found: {path}")
            continue

        print(f"  Loading {city_info['name_en']}...", end=" ")
        df = pd.read_csv(path)

        # Filter to rows with non-null pos and egg values
        df_filtered = df.dropna(subset=['pos', 'egg'])

        city_data[city_key] = {
            'full': df,
            'filtered': df_filtered,
            'name_en': city_info['name_en'],
            'name_zh': city_info['name_zh']
        }

        print(f"Loaded {len(df_filtered):,} valid obs from {len(df):,} total rows")

    return city_data


def calculate_descriptive_stats(city_data):
    """
    Calculate comprehensive descriptive statistics for POS and EGG.

    Parameters
    ----------
    city_data : dict
        Dictionary with city data loaded from load_city_data()

    Returns
    -------
    pd.DataFrame
        DataFrame with descriptive statistics for each city
    """
    print("\nCalculating descriptive statistics...")

    stats_list = []

    for city_key in config.CITY_ORDER:
        if city_key not in city_data:
            continue

        data = city_data[city_key]
        df = data['filtered']
        df_full = data['full']

        # Extract date range
        if 'date' in df_full.columns:
            dates = pd.to_datetime(df_full['date'], errors='coerce')
            date_start = dates.min().strftime('%Y-%m-%d') if pd.notna(dates.min()) else 'N/A'
            date_end = dates.max().strftime('%Y-%m-%d') if pd.notna(dates.max()) else 'N/A'
        else:
            date_start = 'N/A'
            date_end = 'N/A'

        row = {
            'City': data['name_en'],
            'City_ZH': data['name_zh'],
            'Date_Start': date_start,
            'Date_End': date_end,
            'N_Observations': len(df),
        }

        # Calculate statistics for POS
        pos = df['pos'].dropna()
        row['POS_Mean'] = pos.mean()
        row['POS_SD'] = pos.std()
        row['POS_Median'] = pos.median()
        row['POS_Q1'] = pos.quantile(0.25)
        row['POS_Q3'] = pos.quantile(0.75)
        row['POS_IQR'] = row['POS_Q3'] - row['POS_Q1']
        row['POS_Min'] = pos.min()
        row['POS_Max'] = pos.max()

        # Calculate statistics for EGG
        egg = df['egg'].dropna()
        row['EGG_Mean'] = egg.mean()
        row['EGG_SD'] = egg.std()
        row['EGG_Median'] = egg.median()
        row['EGG_Q1'] = egg.quantile(0.25)
        row['EGG_Q3'] = egg.quantile(0.75)
        row['EGG_IQR'] = row['EGG_Q3'] - row['EGG_Q1']
        row['EGG_Min'] = egg.min()
        row['EGG_Max'] = egg.max()

        stats_list.append(row)

        print(f"  {data['name_en']}: n={len(df):,}, "
              f"POS mean={row['POS_Mean']:.4f}, "
              f"EGG mean={row['EGG_Mean']:.2f}")

    return pd.DataFrame(stats_list)


def perform_kruskal_wallis(city_data):
    """
    Perform Kruskal-Wallis H-test for cross-city comparison.

    Parameters
    ----------
    city_data : dict
        Dictionary with city data

    Returns
    -------
    pd.DataFrame
        Kruskal-Wallis test results
    """
    print("\nPerforming Kruskal-Wallis H-test...")

    results = []

    for target in ['pos', 'egg']:
        # Collect data from all cities
        groups = []
        group_names = []

        for city_key in config.CITY_ORDER:
            if city_key not in city_data:
                continue

            data = city_data[city_key]
            df = data['filtered']
            values = df[target].dropna().values

            if len(values) > 0:
                groups.append(values)
                group_names.append(data['name_en'])

        # Perform Kruskal-Wallis test
        if len(groups) >= 2:
            h_stat, p_value = stats.kruskal(*groups)

            result = {
                'Target': target.upper(),
                'H_Statistic': h_stat,
                'p_value': p_value,
                'Significant': 'Yes' if p_value < 0.05 else 'No',
                'N_Groups': len(groups)
            }
            results.append(result)

            print(f"  {target.upper()}: H={h_stat:.2f}, p={p_value:.4e}, "
                  f"{'Significant' if p_value < 0.05 else 'Not Significant'}")

    return pd.DataFrame(results)


def perform_dunn_posthoc(city_data):
    """
    Perform Dunn's post-hoc test with Bonferroni correction.

    Parameters
    ----------
    city_data : dict
        Dictionary with city data

    Returns
    -------
    dict
        Dictionary with Dunn's test results for POS and EGG
    """
    print("\nPerforming Dunn's post-hoc pairwise comparison...")

    dunn_results = {}

    for target in ['pos', 'egg']:
        # Combine all data with city labels
        combined_data = []

        for city_key in config.CITY_ORDER:
            if city_key not in city_data:
                continue

            data = city_data[city_key]
            df = data['filtered']

            temp_df = pd.DataFrame({
                'value': df[target].dropna(),
                'city': data['name_en']
            })
            combined_data.append(temp_df)

        if len(combined_data) >= 2:
            combined_df = pd.concat(combined_data, ignore_index=True)

            # Perform Dunn's test with Bonferroni correction
            dunn_matrix = sp.posthoc_dunn(
                combined_df,
                val_col='value',
                group_col='city',
                p_adjust='bonferroni'
            )

            dunn_results[target] = dunn_matrix

            print(f"  {target.upper()}: Pairwise comparison matrix generated")

            # Print significant pairs
            n_significant = 0
            for i, city1 in enumerate(dunn_matrix.index):
                for j, city2 in enumerate(dunn_matrix.columns):
                    if i < j and dunn_matrix.loc[city1, city2] < 0.05:
                        n_significant += 1

            print(f"    {n_significant} significant pairs (p < 0.05, Bonferroni corrected)")

    return dunn_results


def save_results(desc_stats, kruskal_results, dunn_results, output_dir):
    """
    Save all results to CSV and Markdown files.

    Parameters
    ----------
    desc_stats : pd.DataFrame
        Descriptive statistics DataFrame
    kruskal_results : pd.DataFrame
        Kruskal-Wallis test results
    dunn_results : dict
        Dunn's post-hoc test results
    output_dir : str
        Output directory path
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\nSaving results to {output_dir}...")

    # 1. Save descriptive statistics (CSV)
    desc_csv_path = os.path.join(output_dir, 'overall_descriptive_stats.csv')
    desc_stats.to_csv(desc_csv_path, index=False)
    print(f"  Saved: {desc_csv_path}")

    # 2. Save descriptive statistics (Markdown)
    desc_md_path = os.path.join(output_dir, 'overall_descriptive_stats.md')
    with open(desc_md_path, 'w', encoding='utf-8') as f:
        f.write("# Overall Descriptive Statistics\n\n")
        f.write("## Summary Table\n\n")

        # Create formatted table
        f.write("| City | Date Range | N | POS Mean (SD) | POS Median [IQR] | POS Range | EGG Mean (SD) | EGG Median [IQR] | EGG Range |\n")
        f.write("|------|------------|--:|---------------|------------------|-----------|---------------|------------------|----------|\n")

        for _, row in desc_stats.iterrows():
            pos_mean_sd = f"{row['POS_Mean']:.4f} ({row['POS_SD']:.4f})"
            pos_median_iqr = f"{row['POS_Median']:.4f} [{row['POS_Q1']:.4f}-{row['POS_Q3']:.4f}]"
            pos_range = f"{row['POS_Min']:.4f}-{row['POS_Max']:.4f}"

            egg_mean_sd = f"{row['EGG_Mean']:.2f} ({row['EGG_SD']:.2f})"
            egg_median_iqr = f"{row['EGG_Median']:.2f} [{row['EGG_Q1']:.2f}-{row['EGG_Q3']:.2f}]"
            egg_range = f"{row['EGG_Min']:.2f}-{row['EGG_Max']:.2f}"

            date_range = f"{row['Date_Start']} ~ {row['Date_End']}"

            f.write(f"| {row['City']} | {date_range} | {row['N_Observations']:,} | "
                   f"{pos_mean_sd} | {pos_median_iqr} | {pos_range} | "
                   f"{egg_mean_sd} | {egg_median_iqr} | {egg_range} |\n")

        # Add detailed per-city tables
        f.write("\n## Detailed Statistics by City\n\n")

        for _, row in desc_stats.iterrows():
            f.write(f"### {row['City']} ({row['City_ZH']})\n\n")
            f.write(f"- **Monitoring Period**: {row['Date_Start']} to {row['Date_End']}\n")
            f.write(f"- **N Observations**: {row['N_Observations']:,}\n\n")

            f.write("| Statistic | POS (Positive Rate) | EGG (Egg Count) |\n")
            f.write("|-----------|--------------------:|----------------:|\n")
            f.write(f"| Mean | {row['POS_Mean']:.4f} | {row['EGG_Mean']:.2f} |\n")
            f.write(f"| SD | {row['POS_SD']:.4f} | {row['EGG_SD']:.2f} |\n")
            f.write(f"| Median | {row['POS_Median']:.4f} | {row['EGG_Median']:.2f} |\n")
            f.write(f"| Q1 (25%) | {row['POS_Q1']:.4f} | {row['EGG_Q1']:.2f} |\n")
            f.write(f"| Q3 (75%) | {row['POS_Q3']:.4f} | {row['EGG_Q3']:.2f} |\n")
            f.write(f"| IQR | {row['POS_IQR']:.4f} | {row['EGG_IQR']:.2f} |\n")
            f.write(f"| Min | {row['POS_Min']:.4f} | {row['EGG_Min']:.2f} |\n")
            f.write(f"| Max | {row['POS_Max']:.4f} | {row['EGG_Max']:.2f} |\n\n")

    print(f"  Saved: {desc_md_path}")

    # 3. Save Kruskal-Wallis results (CSV)
    kw_csv_path = os.path.join(output_dir, 'kruskal_wallis_results.csv')
    kruskal_results.to_csv(kw_csv_path, index=False)
    print(f"  Saved: {kw_csv_path}")

    # 4. Save Kruskal-Wallis results (Markdown)
    kw_md_path = os.path.join(output_dir, 'kruskal_wallis_results.md')
    with open(kw_md_path, 'w', encoding='utf-8') as f:
        f.write("# Kruskal-Wallis H-Test Results\n\n")
        f.write("## Cross-City Distribution Comparison\n\n")
        f.write("The Kruskal-Wallis H-test is a non-parametric test used to compare ")
        f.write("distributions across multiple groups.\n\n")
        f.write("### Results\n\n")
        f.write("| Target | H-Statistic | p-value | Significant (p<0.05) |\n")
        f.write("|--------|------------:|--------:|:--------------------:|\n")

        for _, row in kruskal_results.iterrows():
            p_display = f"{row['p_value']:.4e}" if row['p_value'] < 0.0001 else f"{row['p_value']:.4f}"
            f.write(f"| {row['Target']} | {row['H_Statistic']:.2f} | {p_display} | {row['Significant']} |\n")

        f.write("\n### Interpretation\n\n")
        for _, row in kruskal_results.iterrows():
            if row['p_value'] < 0.05:
                f.write(f"- **{row['Target']}**: The distribution differs significantly across cities ")
                f.write(f"(H = {row['H_Statistic']:.2f}, p = {row['p_value']:.4e}).\n")
            else:
                f.write(f"- **{row['Target']}**: No significant difference in distribution across cities ")
                f.write(f"(H = {row['H_Statistic']:.2f}, p = {row['p_value']:.4f}).\n")

    print(f"  Saved: {kw_md_path}")

    # 5. Save Dunn's post-hoc results
    for target, dunn_matrix in dunn_results.items():
        # CSV
        dunn_csv_path = os.path.join(output_dir, f'dunn_posthoc_{target}.csv')
        dunn_matrix.to_csv(dunn_csv_path)
        print(f"  Saved: {dunn_csv_path}")

        # Markdown
        dunn_md_path = os.path.join(output_dir, f'dunn_posthoc_{target}.md')
        with open(dunn_md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Dunn's Post-Hoc Pairwise Comparison - {target.upper()}\n\n")
            f.write("## Method\n\n")
            f.write("Dunn's test with Bonferroni correction for multiple comparisons.\n\n")
            f.write("## P-Value Matrix\n\n")

            # Format the matrix as markdown table
            cities = list(dunn_matrix.columns)
            header = "| |" + "|".join(cities) + "|"
            separator = "|---|" + "|".join(["---:" for _ in cities]) + "|"

            f.write(header + "\n")
            f.write(separator + "\n")

            for city1 in cities:
                row_str = f"| {city1} |"
                for city2 in cities:
                    p = dunn_matrix.loc[city1, city2]
                    if city1 == city2:
                        row_str += " - |"
                    elif p < 0.001:
                        row_str += f" **{p:.2e}** |"
                    elif p < 0.05:
                        row_str += f" **{p:.4f}** |"
                    else:
                        row_str += f" {p:.4f} |"
                f.write(row_str + "\n")

            f.write("\n**Bold** values indicate significant differences (p < 0.05).\n\n")

            # List significant pairs
            f.write("## Significant Pairwise Comparisons\n\n")

            significant_pairs = []
            for i, city1 in enumerate(cities):
                for j, city2 in enumerate(cities):
                    if i < j:
                        p = dunn_matrix.loc[city1, city2]
                        if p < 0.05:
                            significant_pairs.append((city1, city2, p))

            if significant_pairs:
                f.write("| City Pair | p-value |\n")
                f.write("|-----------|--------:|\n")
                for city1, city2, p in sorted(significant_pairs, key=lambda x: x[2]):
                    p_display = f"{p:.2e}" if p < 0.001 else f"{p:.4f}"
                    f.write(f"| {city1} vs {city2} | {p_display} |\n")
            else:
                f.write("No significant pairwise differences found.\n")

        print(f"  Saved: {dunn_md_path}")

    # 6. Create summary table
    summary_path = os.path.join(output_dir, 'summary_table.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("# Summary Table: Cross-City POS/EGG Statistics\n\n")
        f.write("## Data Overview\n\n")

        f.write("| City | Monitoring Period | N | POS Mean±SD | POS Median (IQR) | EGG Mean±SD | EGG Median (IQR) |\n")
        f.write("|:-----|:------------------|--:|:------------|:-----------------|:------------|:-----------------|\n")

        for _, row in desc_stats.iterrows():
            date_range = f"{row['Date_Start']} ~ {row['Date_End']}"
            pos_mean_sd = f"{row['POS_Mean']:.3f}±{row['POS_SD']:.3f}"
            pos_med_iqr = f"{row['POS_Median']:.3f} ({row['POS_IQR']:.3f})"
            egg_mean_sd = f"{row['EGG_Mean']:.1f}±{row['EGG_SD']:.1f}"
            egg_med_iqr = f"{row['EGG_Median']:.1f} ({row['EGG_IQR']:.1f})"

            f.write(f"| {row['City']} | {date_range} | {row['N_Observations']:,} | "
                   f"{pos_mean_sd} | {pos_med_iqr} | {egg_mean_sd} | {egg_med_iqr} |\n")

        f.write("\n## Cross-City Comparison (Kruskal-Wallis H-Test)\n\n")

        for _, row in kruskal_results.iterrows():
            p_display = f"{row['p_value']:.4e}" if row['p_value'] < 0.0001 else f"{row['p_value']:.4f}"
            sig = "***" if row['p_value'] < 0.001 else "**" if row['p_value'] < 0.01 else "*" if row['p_value'] < 0.05 else ""
            f.write(f"- **{row['Target']}**: H = {row['H_Statistic']:.2f}, p = {p_display} {sig}\n")

        f.write("\n## Pairwise Comparisons (Dunn's Test with Bonferroni Correction)\n\n")

        for target in ['pos', 'egg']:
            if target in dunn_results:
                f.write(f"### {target.upper()}\n\n")
                dunn_matrix = dunn_results[target]
                cities = list(dunn_matrix.columns)

                # List significant pairs
                significant_pairs = []
                for i, city1 in enumerate(cities):
                    for j, city2 in enumerate(cities):
                        if i < j:
                            p = dunn_matrix.loc[city1, city2]
                            if p < 0.05:
                                significant_pairs.append((city1, city2, p))

                if significant_pairs:
                    for city1, city2, p in sorted(significant_pairs, key=lambda x: x[2]):
                        p_display = f"{p:.4e}" if p < 0.001 else f"{p:.4f}"
                        f.write(f"- {city1} vs {city2}: p = {p_display}\n")
                else:
                    f.write("- No significant pairwise differences\n")
                f.write("\n")

        f.write("\n---\n")
        f.write("*Note: \\* p<0.05, \\*\\* p<0.01, \\*\\*\\* p<0.001*\n")

    print(f"  Saved: {summary_path}")

    print(f"\nAll results saved to {output_dir}")


def main():
    """Main function to run the cross-city descriptive analysis."""
    print("=" * 70)
    print("Cross-City Descriptive Statistics and Comparison Analysis")
    print("=" * 70)

    # 1. Load data
    city_data = load_city_data()

    if len(city_data) < 2:
        print("Error: Need at least 2 cities for comparison analysis.")
        return

    # 2. Calculate descriptive statistics
    desc_stats = calculate_descriptive_stats(city_data)

    # 3. Perform Kruskal-Wallis test
    kruskal_results = perform_kruskal_wallis(city_data)

    # 4. Perform Dunn's post-hoc test
    dunn_results = perform_dunn_posthoc(city_data)

    # 5. Save results
    output_dir = config.COMPARISON_OUTPUT_DIR
    save_results(desc_stats, kruskal_results, dunn_results, output_dir)

    print("\n" + "=" * 70)
    print("Analysis Complete!")
    print("=" * 70)

    # Print summary
    print("\nSummary:")
    print(f"  - Analyzed {len(city_data)} cities")
    print(f"  - Total observations: {desc_stats['N_Observations'].sum():,}")

    for _, row in kruskal_results.iterrows():
        print(f"  - {row['Target']}: Kruskal-Wallis H={row['H_Statistic']:.2f}, "
              f"p={row['p_value']:.4e} ({'Significant' if row['p_value'] < 0.05 else 'Not significant'})")

    return desc_stats, kruskal_results, dunn_results


if __name__ == '__main__':
    main()
