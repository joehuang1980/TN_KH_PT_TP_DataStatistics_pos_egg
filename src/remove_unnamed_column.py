#!/usr/bin/env python3
"""
Remove 'Unnamed: 0' column from Taipei and Tainan data files.
Creates backup of original files before modification.
"""

import pandas as pd
import os
import shutil
from datetime import datetime

# Define data paths
DATA_FILES = {
    '台北 (Taipei/TP)': '/home/joe/Documents/2025_TPE_model/DATA/2020to2024allfeatures_labels_台北_pos_egg.csv',
    '台南 (Tainan/TN)': '/home/joe/Documents/2023_semi_supervised_learning/Data/2019to2024allfeatures_labels_recent_pos_egg_data.csv'
}

def backup_file(file_path):
    """Create a backup of the original file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{file_path}.backup_{timestamp}"

    print(f"  📦 Creating backup: {os.path.basename(backup_path)}")
    shutil.copy2(file_path, backup_path)
    print(f"  ✅ Backup created successfully")

    return backup_path

def remove_unnamed_column(file_path, city_name):
    """Remove 'Unnamed: 0' column from CSV file."""
    print(f"\n{'='*80}")
    print(f"Processing: {city_name}")
    print(f"{'='*80}")

    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False

    print(f"📂 File: {file_path}")

    try:
        # Create backup first
        backup_path = backup_file(file_path)

        # Read CSV file
        print(f"\n  📊 Reading CSV file...")
        df = pd.read_csv(file_path)

        original_shape = df.shape
        print(f"  ✅ Loaded: {original_shape[0]:,} rows × {original_shape[1]} columns")

        # Check if 'Unnamed: 0' exists
        if 'Unnamed: 0' not in df.columns:
            print(f"  ⚠️  'Unnamed: 0' column not found - no changes needed")
            # Remove backup since no changes
            os.remove(backup_path)
            print(f"  🗑️  Backup removed (no changes needed)")
            return True

        # Remove 'Unnamed: 0' column
        print(f"\n  🔧 Removing 'Unnamed: 0' column...")
        df_cleaned = df.drop(columns=['Unnamed: 0'])

        new_shape = df_cleaned.shape
        print(f"  ✅ New shape: {new_shape[0]:,} rows × {new_shape[1]} columns")
        print(f"  📉 Removed: {original_shape[1] - new_shape[1]} column(s)")

        # Save cleaned file
        print(f"\n  💾 Saving cleaned file...")
        df_cleaned.to_csv(file_path, index=False)
        print(f"  ✅ File saved successfully")

        # Verify the saved file
        print(f"\n  🔍 Verifying saved file...")
        df_verify = pd.read_csv(file_path, nrows=5)

        if 'Unnamed: 0' in df_verify.columns:
            print(f"  ❌ Verification failed: 'Unnamed: 0' still exists!")
            # Restore from backup
            print(f"  🔄 Restoring from backup...")
            shutil.copy2(backup_path, file_path)
            print(f"  ✅ Original file restored")
            return False
        else:
            print(f"  ✅ Verification passed: 'Unnamed: 0' successfully removed")
            print(f"  ✅ Verified columns: {len(df_verify.columns)} (expected: {new_shape[1]})")

        # Display first few column names
        print(f"\n  📋 First 5 columns after cleanup:")
        for i, col in enumerate(df_verify.columns[:5], 1):
            print(f"     {i}. {col}")

        print(f"\n  🎉 Processing completed successfully!")
        print(f"  📦 Backup kept at: {backup_path}")

        return True

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

        # Try to restore from backup if it exists
        if 'backup_path' in locals() and os.path.exists(backup_path):
            print(f"  🔄 Restoring from backup...")
            try:
                shutil.copy2(backup_path, file_path)
                print(f"  ✅ Original file restored")
            except Exception as restore_error:
                print(f"  ❌ Restore failed: {str(restore_error)}")

        return False

def main():
    """Main function to process all files."""
    print("="*80)
    print("REMOVE 'Unnamed: 0' COLUMN FROM DATA FILES")
    print("="*80)

    results = {}
    for city, path in DATA_FILES.items():
        results[city] = remove_unnamed_column(path, city)

    # Summary
    print(f"\n\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")

    success_count = sum(results.values())
    total_count = len(results)

    for city, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{status} - {city}")

    print(f"\n📊 Results: {success_count}/{total_count} files processed successfully")

    if success_count == total_count:
        print(f"🎉 All files processed successfully!")
        print(f"✅ 'Unnamed: 0' column removed from all files")
        print(f"📦 Backups created for safety")
    else:
        print(f"⚠️  Some files failed processing. Check errors above.")

    print(f"\n{'='*80}")

if __name__ == "__main__":
    main()
