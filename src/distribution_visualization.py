
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

print("Starting distribution visualization...")

# Load the cleaned data
data_path = 'output/merged_cleaned_data.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found. Please run the data preparation script first.")
    exit()
df = pd.read_csv(data_path)

# Set plot style
sns.set_style("whitegrid")
# Resolve font display issues for Chinese characters
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial'] # Common fonts that support Chinese
plt.rcParams['axes.unicode_minus'] = False # Display minus sign correctly

# --- Create Visualizations ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Distribution Analysis of POS (Positivity Rate) and EGG (Egg Count)', fontsize=16)

# 1. Histogram for POS
sns.histplot(df['pos'], bins=50, kde=True, ax=axes[0, 0])
axes[0, 0].set_title('Overall Distribution of POS')
axes[0, 0].set_xlabel('POS (Positivity Rate)')
axes[0, 0].set_ylabel('Frequency')

# 2. Histogram for EGG
# Since EGG is heavily skewed, use a log scale for better visualization
sns.histplot(df['egg'], bins=50, kde=True, ax=axes[0, 1], log_scale=True)
axes[0, 1].set_title('Overall Distribution of EGG (Log Scale)')
axes[0, 1].set_xlabel('EGG (Egg Count) - Log Scale')
axes[0, 1].set_ylabel('Frequency')

# 3. Box Plot for POS by City
sns.boxplot(x='縣市', y='pos', data=df, ax=axes[1, 0])
axes[1, 0].set_title('POS Distribution by City')
axes[1, 0].set_xlabel('City')
axes[1, 0].set_ylabel('POS (Positivity Rate)')

# 4. Box Plot for EGG by City
# Use a log scale for the y-axis due to extreme outliers
sns.boxplot(x='縣市', y='egg', data=df, ax=axes[1, 1])
axes[1, 1].set_yscale('log')
axes[1, 1].set_title('EGG Distribution by City (Log Scale)')
axes[1, 1].set_xlabel('City')
axes[1, 1].set_ylabel('EGG (Egg Count) - Log Scale')


plt.tight_layout(rect=[0, 0, 1, 0.95])

# Save the figure
output_path = 'output/distribution_plots.png'
try:
    plt.savefig(output_path)
    print(f"Successfully saved visualization to {output_path}")
except Exception as e:
    print(f"Error saving plot: {e}")

plt.close()
print("\nDistribution visualization script finished.")
