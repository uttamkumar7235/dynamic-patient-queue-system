"""
Save the preprocessing pipeline fitted on training data.
This is a one-time setup to create the preprocessor artifact.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / 'data' / 'raw' / 'synthetic_patient_queue_dataset.csv'
PREPROCESSED_DIR = ROOT / 'preprocessed'

# Feature definitions (same as in preprocessing_pipeline.py)
NUMERICAL_FEATURES = [
    'age', 'symptoms_severity', 'arrival_delay_minutes', 'token_number',
    'patients_ahead', 'queue_length_at_arrival', 'active_doctors',
    'average_service_time_minutes', 'consultation_complexity',
    'staff_availability', 'break_indicator', 'peak_hour', 'hospital_load'
]

CATEGORICAL_FEATURES = [
    'gender', 'patient_type', 'priority_level', 'appointment_status',
    'day_of_week', 'doctor_specialization'
]

print("Loading raw dataset and creating preprocessing pipeline...")

# Load data
df = pd.read_csv(DATA_PATH)

# Use temporal split for consistency (first 80%)
split_idx = int(len(df) * 0.8)
df_train = df.iloc[:split_idx].copy()

# Extract training features
X_train = df_train[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()

print(f"Training set shape: {X_train.shape}")

# Build preprocessing pipeline
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, NUMERICAL_FEATURES),
        ('cat', categorical_transformer, CATEGORICAL_FEATURES)
    ]
)

# Fit preprocessor on training data
print("Fitting preprocessor on training data...")
preprocessor.fit(X_train)

# Save preprocessor
preprocessor_path = PREPROCESSED_DIR / 'preprocessor.pkl'
joblib.dump(preprocessor, preprocessor_path)
print(f"✓ Saved preprocessor to {preprocessor_path.name}")

# Verify
X_train_transformed = preprocessor.transform(X_train)
print(f"✓ Transformed shape: {X_train_transformed.shape}")
print("✓ Preprocessor ready for prediction module")
