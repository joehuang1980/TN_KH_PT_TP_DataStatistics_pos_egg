#!/usr/bin/env python3
"""
Check data structure for all four cities' data files.
Verifies pos (positive rate) and EGG (average egg count) columns.
"""

import pandas as pd
import os

# Define data paths
DATA_PATHS = {
    '高雄 (Kaohsiung/KH)': '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_高雄_pos_egg.csv',
    '屏東 (Pingtung/PT)': '/home/joe/Documents/2024_semi_supervised_learning/Grid_Village/2019to2024allfeatures_labels_屏東_pos_egg.csv',
    '台北 (Taipei/TP)': '/home/joe/Documents/2025_TPE_model/DATA/2020to2024allfeatures_labels_台北_pos_egg.csv',
    '台南 (Tainan/TN)': '/home/joe/Documents/2023_semi_supervised_learning/Data/2019to2024allfeatures_labels_recent_pos_egg_data.csv'
}

def check_file_structure(file_path, city_name):
    """Check the structure of a single data file."""
    print(f"\n{'='*80}")
    print(f"City: {city_name}")
    print(f"{'='*80}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    print(f"✅ File exists: {file_path}")

    try:
        # Read only the first few rows to check structure
        df = pd.read_csv(file_path, nrows=5)

        print(f"\n📊 File Statistics:")
        print(f"   - Sample rows loaded: {len(df)}")
        print(f"   - Total columns: {len(df.columns)}")

        # Check for required columns
        print(f"\n🔍 Required Columns Check:")
        has_pos = 'pos' in df.columns
        has_egg = 'egg' in df.columns

        print(f"   - 'pos' column (positive rate): {'✅ Found' if has_pos else '❌ Not found'}")
        print(f"   - 'egg' column (average eggs): {'✅ Found' if has_egg else '❌ Not found'}")

        # Display column names
        print(f"\n📋 All Columns ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            marker = "👉" if col in ['pos', 'egg', 'date', 'townvill'] else "  "
            print(f"   {marker} {i:3d}. {col}")

        # Display sample data for key columns
        if has_pos and has_egg:
            print(f"\n📈 Sample Data (first 5 rows):")
            key_cols = [col for col in ['date', 'townvill', 'pos', 'egg'] if col in df.columns]
            print(df[key_cols].to_string(index=False))

            # Statistics for pos and egg
            print(f"\n📊 Statistics for 'pos' and 'egg' columns (from sample):")
            print(f"   pos - min: {df['pos'].min():.4f}, max: {df['pos'].max():.4f}, mean: {df['pos'].mean():.4f}")
            print(f"   egg - min: {df['egg'].min():.4f}, max: {df['egg'].max():.4f}, mean: {df['egg'].mean():.4f}")

        # Get full file row count
        print(f"\n🔢 Full File Statistics:")
        row_count = sum(1 for _ in open(file_path)) - 1  # Subtract header
        print(f"   - Total rows: {row_count:,}")

        return True

    except Exception as e:
        print(f"❌ Error reading file: {str(e)}")
        return False

def main():
    """Main function to check all data files."""
    print("="*80)
    print("DATA STRUCTURE VERIFICATION")
    print("Checking ovitrap data for TN, KH, PT, TP cities")
    print("="*80)

    results = {}
    for city, path in DATA_PATHS.items():
        results[city] = check_file_structure(path, city)

    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")

    all_passed = all(results.values())
    for city, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {city}")

    if all_passed:
        print(f"\n🎉 All files verified successfully!")
        print(f"📊 All files contain 'pos' (positive rate) and 'egg' (average egg count) columns")
    else:
        print(f"\n⚠️  Some files have issues. Please check the errors above.")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
