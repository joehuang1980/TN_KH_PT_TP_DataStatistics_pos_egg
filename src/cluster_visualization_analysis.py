
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import kruskal
import numpy as np

print("Starting cluster visualization and analysis...")

# Load the data with cluster labels
data_path = 'output/data_with_clusters.csv'
if not os.path.exists(data_path):
    print(f"Error: {data_path} not found.")
    exit()
df = pd.read_csv(data_path)

# --- 1. t-SNE Visualization ---
print("Performing t-SNE for visualization. This may take a moment...")

# Re-create the PCA data used for clustering
feature_cols = df.columns.drop(['date', 'townvill', 'pos', 'egg', '縣市', 'cluster'], errors='ignore')
X = df[feature_cols]
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=15) # Using the same n_components as in the clustering script
X_pca = pca.fit_transform(X_scaled)

# To speed up t-SNE, we can use a random sample of the data
n_samples_for_tsne = 5000
if len(df) > n_samples_for_tsne:
    sample_indices = np.random.choice(df.index, n_samples_for_tsne, replace=False)
    X_pca_sample = X_pca[sample_indices]
    labels_sample = df.loc[sample_indices, 'cluster']
else:
    X_pca_sample = X_pca
    labels_sample = df['cluster']

tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=300)
X_tsne = tsne.fit_transform(X_pca_sample)

# --- 2. Create Plots ---
fig, axes = plt.subplots(1, 3, figsize=(24, 7))
fig.suptitle('Cluster Analysis and Relationship with POS/EGG', fontsize=16)
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# t-SNE plot
sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=labels_sample, palette='viridis', ax=axes[0], legend='full')
axes[0].set_title('t-SNE Visualization of Clusters')
axes[0].set_xlabel('t-SNE Component 1')
axes[0].set_ylabel('t-SNE Component 2')

# Box plot for POS by cluster
sns.boxplot(x='cluster', y='pos', data=df, ax=axes[1])
axes[1].set_title('POS Distribution by Cluster')
axes[1].set_xlabel('Cluster')
axes[1].set_ylabel('POS (Positivity Rate)')

# Box plot for EGG by cluster (log scale)
sns.boxplot(x='cluster', y='egg', data=df, ax=axes[2])
axes[2].set_yscale('log')
axes[2].set_title('EGG Distribution by Cluster (Log Scale)')
axes[2].set_xlabel('Cluster')
axes[2].set_ylabel('EGG (Egg Count) - Log Scale')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save the figure
output_path = 'output/cluster_analysis_plots.png'
plt.savefig(output_path)
print(f"Successfully saved visualization to {output_path}")
plt.close()

# --- 3. Statistical Analysis ---
print("\n--- Statistical Test: Kruskal-Wallis H-test for POS/EGG across clusters ---")
# Kruskal-Wallis is a non-parametric alternative to ANOVA, suitable for non-normally distributed data.

# Test for POS
clusters_pos = [df['pos'][df['cluster'] == i] for i in df['cluster'].unique()]
h_stat_pos, p_val_pos = kruskal(*clusters_pos)
print(f"POS: H-statistic={h_stat_pos:.2f}, p-value={p_val_pos:.4f}")
if p_val_pos < 0.05:
    print("  -> The difference in POS across clusters is statistically significant.")
else:
    print("  -> The difference in POS across clusters is not statistically significant.")

# Test for EGG
clusters_egg = [df['egg'][df['cluster'] == i] for i in df['cluster'].unique()]
h_stat_egg, p_val_egg = kruskal(*clusters_egg)
print(f"EGG: H-statistic={h_stat_egg:.2f}, p-value={p_val_egg:.4f}")
if p_val_egg < 0.05:
    print("  -> The difference in EGG across clusters is statistically significant.")
else:
    print("  -> The difference in EGG across clusters is not statistically significant.")

print("\nCluster visualization and analysis script finished.")
