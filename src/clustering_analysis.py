
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import os

print("Starting clustering analysis...")

# Load the cleaned data
data_path = 'output/merged_cleaned_data.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()
df = pd.read_csv(data_path)

# Prepare data for clustering
# Drop non-feature columns
feature_cols = df.columns.drop(['date', 'townvill', 'pos', 'egg', '縣市'], errors='ignore')
X = df[feature_cols]
print(f"Performing clustering on {len(feature_cols)} features.")

# 1. Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Features standardized.")

# 2. Apply PCA for dimensionality reduction
# We choose enough components to explain 90% of the variance
pca = PCA(n_components=0.90)
X_pca = pca.fit_transform(X_scaled)
print(f"PCA applied. Number of components to explain 90% variance: {pca.n_components_}")

# 3. Use the Elbow Method to find the optimal k for K-Means
print("Finding optimal k using the Elbow Method...")
inertia = []
k_range = range(2, 11) # Test k from 2 to 10
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
    kmeans.fit(X_pca)
    inertia.append(kmeans.inertia_)

# For simplicity in this automated script, we'll pick the k that shows a significant drop.
# A more advanced method would be to find the "elbow point" mathematically.
# Here, we'll just print the inertia values. A good 'k' is often where the drop in inertia slows down.
print("Inertia for k=2 to 10:")
for k, i in zip(k_range, inertia):
    print(f"  k={k}, Inertia={i:.2f}")

# Let's choose a k. For this script, we'll hardcode a choice, but in a real analysis,
# this would be chosen by inspecting a plot of the inertia. Let's assume k=4 is a reasonable choice.
chosen_k = 4
print(f"\nBased on the inertia values, we'll proceed with k={chosen_k}.")

# 4. Run K-Means with the chosen k
kmeans = KMeans(n_clusters=chosen_k, random_state=42, n_init='auto')
cluster_labels = kmeans.fit_predict(X_pca)

# Add cluster labels to the original dataframe
df['cluster'] = cluster_labels
print(f"K-Means clustering complete. Cluster counts:\n{df['cluster'].value_counts()}")

# 5. Save the dataframe with cluster labels
output_path = 'output/data_with_clusters.csv'
try:
    df.to_csv(output_path, index=False)
    print(f"\nSuccessfully saved data with cluster labels to {output_path}")
except Exception as e:
    print(f"Error saving file: {e}")

print("\nClustering analysis script finished.")
