
import pandas as pd
import os

print("Starting correlation analysis...")

# Load the data
data_path = 'output/data_with_clusters.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()
df = pd.read_csv(data_path)

# Prepare data for correlation
# We can drop columns that are not features or targets
cols_to_drop = ['date', 'townvill', '縣市', 'cluster']
df_corr = df.drop(columns=cols_to_drop, errors='ignore')

# --- Calculate Spearman Correlation ---
# Spearman is used as it's non-parametric and suitable for non-normally distributed data.
print("Calculating Spearman correlations with POS and EGG...")
correlations = df_corr.corr(method='spearman')

# Get correlations with target variables
corr_pos = correlations['pos'].drop(['pos', 'egg'])
corr_egg = correlations['egg'].drop(['pos', 'egg'])

# --- Analyze and Print Top Correlations ---

def print_top_correlations(series, target_name):
    """Prints the top positive and negative correlations for a given series."""
    print(f"\n--- Top Correlations with {target_name} ---")
    
    # Top 10 Positive
    top_pos = series.sort_values(ascending=False).head(10)
    print(f"\nTop 10 Positive Correlations with {target_name}:")
    print(top_pos)
    
    # Top 10 Negative
    top_neg = series.sort_values(ascending=True).head(10)
    print(f"\nTop 10 Negative Correlations with {target_name}:")
    print(top_neg)

print_top_correlations(corr_pos, 'POS')
print_top_correlations(corr_egg, 'EGG')

# --- Save Full Correlation Matrix ---
output_path = 'output/correlations.csv'
try:
    correlations.to_csv(output_path)
    print(f"\nSuccessfully saved full correlation matrix to {output_path}")
except Exception as e:
    print(f"Error saving file: {e}")

print("\nCorrelation analysis script finished.")
