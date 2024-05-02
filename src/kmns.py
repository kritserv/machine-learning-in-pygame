import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def kmeans(data):
	if not os.path.exists("created_model"):
		os.makedirs("created_model")

	n_clusters = 3
		
	# Extract the features
	features = data[1:, :-1].astype(float)  # all columns except the last

	# Create a KMeans model
	model = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)

	# Fit the model
	model.fit(features)

	# Save the model
	joblib.dump(model, os.path.join("created_model", "kmeans_model.pkl"))

	# Print the cluster centers
	print(f"Cluster centers: {model.cluster_centers_}\nCluster Model Saved\ncreated_model/kmeans_model.pkl")

	return f"Cluster centers: {model.cluster_centers_}\nCluster Model Saved\ncreated_model/kmeans_model.pkl"