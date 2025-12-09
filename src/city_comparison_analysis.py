
import pandas as pd
import scikit_posthocs as sp
import os

print("Starting city comparison analysis...")

# Load the data
data_path = 'output/data_with_clusters.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()
df = pd.read_csv(data_path)

# --- Kruskal-Wallis and Dunn's Post-Hoc Test ---

def perform_comparison(dataframe, target_col):
    """Performs Kruskal-Wallis and Dunn's post-hoc test for a given target column."""
    print(f"\n--- Analysis for: {target_col.upper()} ---")
    
    # Kruskal-Wallis test to see if there's any significant difference among all cities
    # We need to import the function from scipy.stats
    from scipy.stats import kruskal
    
    city_groups = [group[target_col].values for name, group in dataframe.groupby('縣市')]
    h_stat, p_val = kruskal(*city_groups)
    
    print(f"Kruskal-Wallis H-test result:")
    print(f"  H-statistic: {h_stat:.2f}")
    print(f"  p-value: {p_val:.4f}")
    
    if p_val < 0.05:
        print("  -> The difference between cities is statistically significant.")
        print("\nPerforming Dunn's post-hoc test to see which pairs are different...")
        
        # Dunn's test
        dunn_results = sp.posthoc_dunn(dataframe, val_col=target_col, group_col='縣市', p_adjust='bonferroni')
        
        print("Dunn's Test Results (p-values):")
        print("A low p-value (< 0.05) indicates a significant difference between the pair.")
        print(dunn_results)
    else:
        print("  -> No statistically significant difference found between cities.")

# Perform the analysis for both 'pos' and 'egg'
perform_comparison(df, 'pos')
perform_comparison(df, 'egg')

print("\nCity comparison analysis finished.")
print("Note: The boxplots visualizing these differences are in 'output/distribution_plots.png' from Step 2.")
