# Hierarchical Agglomerative Clustering  

## Objective  
To implement Hierarchical Agglomerative Clustering (HAC) from scratch and compare it with Scikit-learn's implementation using the UCI Vehicle Silhouettes dataset.  

---

## Tasks  

### **Task 1: Data Loading and Preprocessing**  
- Loaded the UCI Vehicle Silhouettes dataset with 18 features.  

### **Task 2: Handling Duplicates and Missing Values**  
- Checked for duplicate and missing features.  
- Partitioned the dataset into training (80%) and test (20%) sets.  

### **Task 3: From-Scratch HAC Implementation**  
- Implemented HAC using:
  - **Euclidean Distance**: To compute pairwise distances.  
  - **Average Linkage**: To merge clusters based on average distances.  
- Derived 4 clusters and assigned all points to their closest clusters.  

### **Task 4: Scikit-learn HAC Implementation**  
- Used Scikit-learn’s `AgglomerativeClustering` with the same hyperparameters (Euclidean distance and average linkage).  

### **Task 5: Dendrogram**  
- Visualized the dendrogram for the clustering process to show hierarchical merges.  

### **Task 6: Consistent Label Assignment**  
- Renamed the cluster labels consistently for both the from-scratch and Scikit-learn implementations.  
- Labels were assigned from ‘0’ to ‘3’ based on the smallest to largest cluster centroids.  

### **Task 7: Comparison of Cluster Labels**  
- Compared cluster labels obtained from the from-scratch implementation with those obtained from Scikit-learn.  
- Reported the percentage of points where label assignments matched.  

### **Task 8: Cluster Consistency Analysis**  
- Evaluated the consistency of clusters using the ground truth labels.  
- For each cluster, reported the fraction of samples that belong to the 4 classes.  

---

## Results  

### **Performance Metrics**  
- **% Label Match**: `<value>`  
- **Cluster Consistency Fractions**:  
  - Cluster 0: `<value>`  
  - Cluster 1: `<value>`  
  - Cluster 2: `<value>`  
  - Cluster 3: `<value>`  

---

## How to Run  

1. Install the required libraries:  
   ```bash
   pip install numpy pandas matplotlib scikit-learn scipy
