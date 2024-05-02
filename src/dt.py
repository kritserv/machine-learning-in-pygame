import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def decision_tree(data):
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

	# Create a decision tree model
	model = DecisionTreeClassifier()

	# Train the model
	model.fit(X_train, y_train)

	# Save the model
	joblib.dump(model, os.path.join("created_model", "dt_model.pkl"))

	# Make predictions using the test set
	y_pred = model.predict(X_test)

	# Evaluate the model
	accuracy = accuracy_score(y_test, y_pred)
	print(f"DT Accuracy: {accuracy}\nDT Model Saved \ncreated_model/dt_model.pkl")

	return f"DT Accuracy: {accuracy}\nDT Model Saved \ncreated_model/dt_model.pkl"