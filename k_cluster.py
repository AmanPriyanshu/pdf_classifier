from sklearn.cluster import KMeans
import numpy as np

def k_means(X, n_clusters):

  kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)
  return kmeans.labels_