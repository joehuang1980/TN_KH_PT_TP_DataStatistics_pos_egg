
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import re

print("Starting lag effect analysis...")

# Load the data
data_path = 'output/data_with_clusters.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()
df = pd.read_csv(data_path)

# Define variable groups to analyze based on prefixes
var_groups = {
    'M_temp': [col for col in df.columns if col.startswith('M_temp_lag_') and not 'rolling' in col],
    'H_temp': [col for col in df.columns if col.startswith('H_temp_lag_') and not 'rolling' in col],
    'L_temp': [col for col in df.columns if col.startswith('L_temp_lag_') and not 'rolling' in col],
    'Rainfall': [col for col in df.columns if col.startswith('R_lag_') and not 'rolling' in col],
    'NDVI_mean': [col for col in df.columns if col.startswith('NDVImean_lag_') and not 'rolling' in col]
}

cities = df['縣市'].unique()
targets = ['pos', 'egg']
results = []

print("Analyzing optimal lag for each city and variable...")

# Function to extract lag number from column name
def get_lag_num(col_name):
    match = re.search(r'_(\d+)$', col_name)
    return int(match.group(1)) if match else 0

# Iterate over each city, variable group, and target
for city in cities:
    city_df = df[df['縣市'] == city]
    for var_name, cols in var_groups.items():
        for target in targets:
            if not cols: continue
            # Calculate correlations for all lags of the variable
            corrs = city_df[cols + [target]].corr(method='spearman')[target].drop(target)
            if corrs.empty: continue
            
            # Find the lag with the highest absolute correlation
            best_lag_col = corrs.abs().idxmax()
            best_corr_val = corrs.loc[best_lag_col]
            optimal_lag = get_lag_num(best_lag_col)
            
            results.append({
                'City': city,
                'Variable': var_name,
                'Target': target,
                'Optimal_Lag_Week': optimal_lag,
                'Correlation': best_corr_val
            })

# Create a summary dataframe
results_df = pd.DataFrame(results)

# --- Print and Pivot the results for easy viewing ---
print("\n--- Optimal Lag Weeks for POS ---")
pos_pivot = results_df[results_df['Target'] == 'pos'].pivot_table(
    index='Variable', columns='City', values='Optimal_Lag_Week'
)
print(pos_pivot)

print("\n--- Optimal Lag Weeks for EGG ---")
egg_pivot = results_df[results_df['Target'] == 'egg'].pivot_table(
    index='Variable', columns='City', values='Optimal_Lag_Week'
)
print(egg_pivot)

# --- Visualize as Heatmaps ---
fig, axes = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
fig.suptitle('Optimal Lag Week for Key Variables by City', fontsize=16)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

sns.heatmap(pos_pivot, ax=axes[0], annot=True, cmap='viridis', fmt='.0f')
axes[0].set_title('Target: POS')
axes[0].set_xlabel('City')
axes[0].set_ylabel('Variable')

sns.heatmap(egg_pivot, ax=axes[1], annot=True, cmap='viridis', fmt='.0f')
axes[1].set_title('Target: EGG')
axes[1].set_xlabel('City')
axes[1].set_ylabel('')

output_path = 'output/lag_effect_heatmap.png'
plt.savefig(output_path)
print(f"\nSuccessfully saved heatmap to {output_path}")
plt.close()

print("\nLag effect analysis script finished.")
