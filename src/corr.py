import numpy as np

def correlation_analysis(data):
	# Extract the features
	features = data[1:, :-1].astype(float)  # all columns except the last

	# Calculate the correlation matrix
	corr_matrix = np.corrcoef(features, rowvar=False)

	print(f"Correlation matrix: \n{corr_matrix}")

	return f"Correlation matrix: \n{corr_matrix}"