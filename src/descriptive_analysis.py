
import pandas as pd
import numpy as np

# Set pandas display options to show all columns
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("Starting descriptive analysis...")

# Load the cleaned data
try:
    df = pd.read_csv('output/merged_cleaned_data.csv')
    print(f"Successfully loaded 'output/merged_cleaned_data.csv'. Shape: {df.shape}")
except FileNotFoundError:
    print("Error: 'output/merged_cleaned_data.csv' not found. Please run the data preparation script first.")
    exit()

# --- Column Cleanup ---
# Drop 'date' and 'townvill' as per the plan
columns_to_drop = ['date', 'townvill']
existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
if existing_columns_to_drop:
    df.drop(columns=existing_columns_to_drop, inplace=True)
    print(f"Dropped columns: {existing_columns_to_drop}")

# --- Overall Descriptive Statistics ---
print("\n--- Overall Descriptive Statistics ---")
# To avoid overwhelming output, describe() will be shown for key columns and a sample of features
key_cols = ['pos', 'egg']
# Sample a few feature columns to get an idea of the data
candidate_cols = df.columns.drop(key_cols + ['縣市'])
sample_size = min(5, len(candidate_cols))

if sample_size > 0:
    feature_sample = list(np.random.choice(candidate_cols, sample_size, replace=False))
    print(df[key_cols + feature_sample].describe())
else:
    print("No feature columns available to sample")
    print(df[key_cols].describe())


# --- Per-City Descriptive Statistics ---
print("\n--- Per-City Descriptive Statistics (for pos and egg) ---")
# Group by '縣市' and describe the target variables
city_grouped_stats = df.groupby('縣市')[key_cols].describe()
print(city_grouped_stats)

# Save the statistics to files for easier review
try:
    df.describe().to_csv('output/overall_descriptive_stats.csv')
    city_grouped_stats.to_csv('output/city_grouped_descriptive_stats.csv')
    print("\nSuccessfully saved full descriptive statistics to 'output/overall_descriptive_stats.csv' and 'output/city_grouped_descriptive_stats.csv'")
except Exception as e:
    print(f"\nError saving statistics files: {e}")

print("\nDescriptive analysis script finished.")
