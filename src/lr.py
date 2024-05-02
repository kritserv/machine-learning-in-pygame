import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def linear_regression(data):
	if not os.path.exists("created_model"):
		os.makedirs("created_model")
		
	# Extract the features and target
	features = data[1:, :-1].astype(float)  # all columns except the last
	target = data[1:, -1]  # last column

	# Convert the categorical target variable into a numerical format
	le = LabelEncoder()
	target = le.fit_transform(target)

	# Split the data into training and test sets
	X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

	# Create a linear regression model
	model = LinearRegression()

	# Train the model
	model.fit(X_train, y_train)

	# Save the model
	joblib.dump(model, os.path.join("created_model", "lr_model.pkl"))

	# Make predictions using the test set
	y_pred = model.predict(X_test)

	# Evaluate the model
	mse = mean_squared_error(y_test, y_pred)
	print(f"LinearRegression MSE: {mse}\nLR Model Saved\ncreated_model/lr_model.pkl")

	return f"LinearRegression MSE: {mse}\nLR Model Saved\ncreated_model/lr_model.pkl"