!pip install ucimlrepo

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

"""# **Task-1**"""

from ucimlrepo import fetch_ucirepo

# fetch dataset
statlog_vehicle_silhouettes = fetch_ucirepo(id=149)

# data (as pandas dataframes)
X = statlog_vehicle_silhouettes.data.features
y = statlog_vehicle_silhouettes.data.targets

# metadata
print(statlog_vehicle_silhouettes.metadata)

# variable information
print(statlog_vehicle_silhouettes.variables)

display(X)

"""# **Task-2**"""

X.isnull().sum()

y.isnull().sum()

X.duplicated().sum()

X.describe()

# use transformer for preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Define the preprocessing pipeline with imputation
preprocessing_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Transform the feature data
X_preprocessed = preprocessing_pipeline.fit_transform(X)

X_preprocessed

# Split the data into training and testing sets
from sklearn.model_selection import train_test_split
# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

print("\nTraining set shape:", X_train.shape)
print("Test set shape:", X_test.shape)

"""# **Task-3**"""

import numpy as np
from scipy.spatial.distance import cdist

class HAC:
    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters  # Desired number of clusters

    def fit(self, X):
        # Step 1: Initialize each point as its own cluster
        self.clusters = {i: [X[i]] for i in range(len(X))}
        self.cluster_centroids = np.copy(X)  # Initially, each point is its own centroid

        # Step 2: Compute initial pairwise distances between all clusters
        distances = cdist(X, X, metric='euclidean')
        np.fill_diagonal(distances, np.inf)  # Ignore distances to itself

        # Step 3: Iteratively merge clusters until reaching the target number of clusters
        while len(self.clusters) > self.n_clusters:
            # Find the closest two clusters (smallest distance)
            min_dist_idx = np.unravel_index(np.argmin(distances), distances.shape)
            cluster_a, cluster_b = sorted(min_dist_idx)

            # Merge the clusters
            self.clusters[cluster_a].extend(self.clusters[cluster_b])
            del self.clusters[cluster_b]

            # Update distances: Calculate average distance between the merged cluster and other clusters
            for i in list(self.clusters.keys()):
                if i != cluster_a:
                    # Compute the average distance using all points in both clusters
                    avg_dist = np.mean(cdist(self.clusters[cluster_a], self.clusters[i], metric='euclidean'))
                    distances[cluster_a, i] = distances[i, cluster_a] = avg_dist

            # Set merged cluster distances to infinity to avoid reuse
            distances[cluster_b] = distances[:, cluster_b] = np.inf

            # Update the centroid for the merged cluster
            self.cluster_centroids[cluster_a] = np.mean(self.clusters[cluster_a], axis=0)

        # Step 4: Assign each point to a final cluster based on the closest centroid
        self.labels_ = np.empty(len(X), dtype=int)
        for label, points in enumerate(self.clusters.values()):
            for point in points:
                point_idx = np.where(np.all(X == point, axis=1))[0][0]
                self.labels_[point_idx] = label  # Assign the label based on the final cluster

# Perform HAC from scratch
print("Performing HAC from scratch...")
# Perform HAC
hac = HAC(n_clusters=4)
hac.fit(X_train)

# Retrieve cluster labels
labels = hac.labels_

# Print the cluster labels
print("Cluster labels:")
print(labels)

"""# **Task-4**"""

from sklearn.cluster import AgglomerativeClustering

# Perform clustering using scikit-learn
n_clusters = 4  # Same number of clusters as in your custom HAC implementation

# Create an instance of AgglomerativeClustering
hac_sklearn = AgglomerativeClustering(n_clusters=n_clusters, linkage='average')

# Fit the model to the training data
sklearn_labels = hac_sklearn.fit_predict(X_train)  # Use hac_sklearn here

# Output the cluster labels
print("Cluster labels from scikit-learn HAC:")
print(sklearn_labels)

"""# **Task-5**"""

import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch

# Create a dendrogram
plt.figure(figsize=(15, 8))
dendrogram = sch.dendrogram(
    sch.linkage(X_train, method='average'),
    leaf_rotation=90,  # Rotate leaf labels for better visibility
    leaf_font_size=10,  # Set the font size for leaf labels
    truncate_mode='lastp',  # Show only the last p merged clusters
    p=30  # Adjust this number to display fewer sample labels
)

plt.title('Dendrogram')
plt.xlabel('Samples')
plt.ylabel('Euclidean Distance')
plt.show()

"""# **Task-6**"""

def rename_labels(pred_labels):
    unique_labels = np.unique(pred_labels)
    sorted_labels = sorted(unique_labels, key=lambda x: np.mean(X_train[pred_labels == x], axis=0).mean())
    label_mapping = {old: new for new, old in enumerate(sorted_labels)}

    print("Label Mapping:", label_mapping)
    print("Unique Labels:", unique_labels)
    print("Sorted Labels:", sorted_labels)

    return np.array([label_mapping[label] for label in pred_labels])

"""# **Task-7**"""

renamed_hac = rename_labels(labels)
renamed_hac_sklearn = rename_labels(sklearn_labels)

# Calculate the percentage of matching labels
matching_labels = (renamed_hac == renamed_hac_sklearn).sum()
total_points = len(renamed_hac)
percentage_match = (matching_labels / total_points) * 100

print(f"Percentage of matching labels: {percentage_match:.2f}%")

"""Visualize the clustering"""

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Perform PCA for visualization
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)

# Plot custom HAC clusters
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=renamed_hac, cmap='viridis', marker='o', s=50)
plt.title('Custom HAC Clustering')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')

# Plot sklearn HAC clusters
plt.subplot(1, 2, 2)
plt.scatter(X_train_pca[:, 0], X_train_pca[:, 1], c=renamed_hac_sklearn, cmap='viridis', marker='o', s=50)
plt.title('Sklearn HAC Clustering')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')

plt.tight_layout()
plt.show()

"""# **Task-8**"""

from collections import Counter

# Assuming y_train contains ground truth labels
def cluster_consistency(renamed_labels, ground_truth):
    cluster_stats = {}
    for cluster in np.unique(renamed_labels):
        cluster_indices = np.where(renamed_labels == cluster)[0]
        cluster_ground_truth = ground_truth.iloc[cluster_indices]
        counts = Counter(cluster_ground_truth)
        total_count = sum(counts.values())
        cluster_stats[cluster] = {label: count / total_count for label, count in counts.items()}

    return cluster_stats

consistency_hac = cluster_consistency(renamed_hac, y_train)
consistency_sklearn = cluster_consistency(renamed_hac_sklearn, y_train)

print('Cluster consistency (HAC from scratch):')
print(consistency_hac)

print('Cluster consistency (HAC sklearn):')
print(consistency_sklearn)

