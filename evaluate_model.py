import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score, recall_score

# Load the data
data = pd.read_csv('ecoli.csv')
X = data.drop('class', axis=1)
y_true = data['class']

# Load the model and scaler
model = joblib.load('ecoli.model')
scaler = joblib.load('scaler.pkl')

# Scale the features
X_scaled = scaler.transform(X)

# Make predictions
y_pred = model.predict(X_scaled)
y_pred_proba = model.predict_proba(X_scaled)

# Get the predicted probability for the predicted class
pred_probabilities = [probs[list(model.classes_).index(pred)] for pred, probs in zip(y_pred, y_pred_proba)]

# Create results DataFrame
results = pd.DataFrame({
    'MCG': X['mcg'],
    'GVH': X['gvh'],
    'LIP': X['lip'],
    'CHG': X['chg'],
    'AAC': X['aac'],
    'ALM1': X['alm1'],
    'ALM2': X['alm2'],
    'Actual_Class': y_true,
    'Predicted_Class': y_pred,
    'Prediction_Probability': pred_probabilities,
    'Prediction_Match': y_true == y_pred
})

# Calculate class-wise precision and recall
classes = sorted(list(set(y_true)))
precision = precision_score(y_true, y_pred, average=None, zero_division=0)
recall = recall_score(y_true, y_pred, average=None, zero_division=0)

# Create precision-recall summary
pr_summary = pd.DataFrame({
    'Class': classes,
    'Precision': precision,
    'Recall': recall
})

# Add overall accuracy
accuracy = (y_true == y_pred).mean()
pr_summary.loc[len(pr_summary)] = ['Overall', accuracy, accuracy]

# Save results
results.to_csv('pr.csv', index=False)
pr_summary.to_csv('pr_summary.csv', index=False)

# Print summary
print("\nPrecision-Recall Summary:")
print(pr_summary)

print("\nDetailed Results Summary:")
print(f"Total Samples: {len(results)}")
print(f"Correct Predictions: {results['Prediction_Match'].sum()}")
print(f"Incorrect Predictions: {(~results['Prediction_Match']).sum()}")
print(f"Accuracy: {accuracy:.4f}")

# Print misclassified examples
print("\nMisclassified Examples:")
misclassified = results[~results['Prediction_Match']]
print(misclassified[['Actual_Class', 'Predicted_Class', 'Prediction_Probability']])
