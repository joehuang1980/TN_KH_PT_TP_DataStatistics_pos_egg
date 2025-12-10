
import pandas as pd
import glob
import os

# Define file paths and city names
# Paths can be overridden using environment variables for portability
file_paths = {
    '高雄': os.getenv(
        'KAOHSIUNG_DATA_PATH',
        '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_高雄_pos_egg.csv'
    ),
    '屏東': os.getenv(
        'PINGTUNG_DATA_PATH',
        '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_屏東_pos_egg.csv'
    ),
    '台北': os.getenv(
        'TAIPEI_DATA_PATH',
        '/home/joe/Documents/2025_TPE_model/DATA/2020to2024allfeatures_labels_台北_pos_egg.csv'
    ),
    '台南': os.getenv(
        'TAINAN_DATA_PATH',
        '/home/joe/Documents/2023_semi_supervised_learning/Data/2019to2024allfeatures_labels_recent_pos_egg_data.csv'
    )
}

# List to hold dataframes
df_list = []

print("Starting data loading and preprocessing...")

# Loop through the file paths, read csv, and add city column
for city, path in file_paths.items():
    try:
        print(f"Reading data for {city} from {path}...")
        df = pd.read_csv(path)
        df['縣市'] = city
        df_list.append(df)
        print(f"Successfully loaded {city} data. Shape: {df.shape}")
    except FileNotFoundError:
        print(f"Error: File not found at {path}. Skipping this file.")
    except Exception as e:
        print(f"An error occurred while reading {path}: {e}")

# Concatenate all dataframes into one
if not df_list:
    print("No data was loaded. Exiting.")
else:
    merged_df = pd.concat(df_list, ignore_index=True)
    print(f"\nInitial merged data shape: {merged_df.shape}")

    # --- Data Cleaning ---
    # 1. Drop rows with any missing values
    initial_rows = len(merged_df)
    merged_df.dropna(inplace=True)
    final_rows = len(merged_df)
    print(f"Dropped {initial_rows - final_rows} rows containing missing values.")

    # 2. Remove '日期' and '里名' columns if they exist
    columns_to_drop = ['日期', '里名']
    existing_columns_to_drop = [col for col in columns_to_drop if col in merged_df.columns]
    if existing_columns_to_drop:
        merged_df.drop(columns=existing_columns_to_drop, inplace=True)
        print(f"Dropped columns: {existing_columns_to_drop}")
    else:
        print("Columns '日期' and '里名' not found in the dataframe.")

    # --- Save Cleaned Data ---
    output_path = 'output/merged_cleaned_data.csv'
    try:
        merged_df.to_csv(output_path, index=False)
        print(f"\nSuccessfully saved cleaned data to {output_path}")
        print(f"Final data shape: {merged_df.shape}")
        print("\nFirst 5 rows of the cleaned data:")
        print(merged_df.head())
    except Exception as e:
        print(f"Error saving file to {output_path}: {e}")
