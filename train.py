import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
def load_data():
    df = pd.read_csv('ecoli.csv')
    X = df.drop('class', axis=1)
    y = df['class']
    return X, y

# Train the model
def train_model():
    # Load and split the data
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create optimized base models
    dt = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    xgb = XGBClassifier(
        n_estimators=100,
        max_depth=10,
        learning_rate=0.1,
        min_child_weight=2,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    
    # Create ensemble model using voting with optimized weights
    ensemble = VotingClassifier(
        estimators=[
            ('dt', dt),
            ('xgb', xgb)
        ],
        voting='soft',
        weights=[1, 2]  # Give more weight to XGBoost as it's generally more robust
    )
    
    # Train the ensemble model
    ensemble.fit(X_train_scaled, y_train)
    
    # Evaluate the model
    y_pred = ensemble.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Accuracy:", accuracy)
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model and scaler
    joblib.dump(ensemble, 'ecoli.model')
    joblib.dump(scaler, 'scaler.pkl')
    print("\nModel and scaler saved successfully!")

if __name__ == "__main__":
    train_model()
