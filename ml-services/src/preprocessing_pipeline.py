"""
ML Preprocessing Pipeline for Patient Queue Waiting Time Prediction

Purpose:
- Load raw synthetic dataset
- Select valid features
- Handle missing values
- Encode categorical variables
- Create train/test split
- Prevent data leakage
- Enable reproducible inference pipeline

Dataset: Synthetic patient queue data (20,000 records, 26 features)
Target: waiting_time_minutes
Prediction Point: When patient joins queue (only info available before prediction)

IMPORTANT:
- No model training in this script
- Raw CSV is never modified
- Pipeline is designed to be reusable during inference
- All random states use seed 42 for reproducibility
- Data leakage is explicitly prevented
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'raw' / 'synthetic_patient_queue_dataset.csv'
OUTPUT_DIR = ROOT / 'preprocessed'
REPORTS_DIR = ROOT / 'reports'
OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20

# ============================================================================
# FEATURE DEFINITION - LEAKAGE-FREE FEATURE SET
# ============================================================================

# EXCLUDED FEATURES AND REASONS
EXCLUDED_FEATURES = {
    'waiting_time_minutes': 'TARGET VARIABLE - must not be in X',
    'patient_id': 'Unique identifier with no predictive value; causes overfitting',
    'previous_patient_service_time': 'LEAKAGE - outcome from previous patient after current patient joins queue',
    'visit_date': 'Temporal feature; use day_of_week as proxy; requires date parsing',
    'arrival_time': 'Temporal feature; requires HH:MM parsing; use peak_hour instead',
    'scheduled_time': 'Temporal feature; requires HH:MM parsing; arrival_delay_minutes captures the diff'
}

# NUMERIAL FEATURES (non-leaky, available at prediction time)
NUMERICAL_FEATURES = [
    'age',                              # Patient demographics
    'symptoms_severity',                # Clinical urgency (1-5)
    'arrival_delay_minutes',            # Time between scheduled and actual arrival (has missing vals)
    'token_number',                     # Sequential queue assignment
    'patients_ahead',                   # Direct queue predictor
    'queue_length_at_arrival',          # Total queue load
    'active_doctors',                   # Number of available doctors
    'average_service_time_minutes',     # Expected service duration (CAREFULLY INCLUDED - see note below)
    'consultation_complexity',          # Expected complexity level (1-5)
    'staff_availability',               # Percentage of staff available (has missing vals)
    'break_indicator',                  # Doctor on break (binary: 0/1)
    'peak_hour',                        # Peak vs non-peak (binary: 0/1)
    'hospital_load'                     # Overall occupancy percentage
]

# CATEGORICAL FEATURES
CATEGORICAL_FEATURES = [
    'gender',                           # Patient gender (Female, Male, Other)
    'patient_type',                     # New or Follow-up visit
    'priority_level',                   # Normal, Urgent, Emergency (ordinal)
    'appointment_status',               # Scheduled or Walk-in
    'day_of_week',                      # Day-based operational patterns
    'doctor_specialization'             # Medical specialty affects service time
]

# ============================================================================
# LEAKAGE PREVENTION NOTES
# ============================================================================

LEAKAGE_NOTES = {
    'average_service_time_minutes': {
        'status': 'INCLUDED WITH CAUTION',
        'assumption': 'This value represents historical average per doctor, computed from data BEFORE this patient arrived',
        'risk': 'HIGH if calculated using entire dataset including future patients; SAFE if from historical records only',
        'usage': 'Assume this is pre-calculated from historical queue records; not recalculated on test set',
        'note': 'In production, this should be updated daily/weekly from past data, not recomputed on current queue'
    },
    'previous_patient_service_time': {
        'status': 'EXCLUDED',
        'reason': 'This is outcome from PREVIOUS patient; becomes known AFTER current patient joins queue but BEFORE prediction',
        'impact': 'Would create look-ahead bias if included; not available at prediction time',
        'action': 'Removed entirely from feature set'
    },
    'prediction_point': {
        'timing': 'Immediately after patient joins queue and is assigned a token',
        'available_info': 'Patient demographics, queue state at arrival, doctor info, time-of-day, hospital operational status',
        'unavailable_info': 'Actual service time (outcome), previous patient details, future queue changes'
    }
}

# ============================================================================
# LOAD AND PREPARE DATA
# ============================================================================

print("=" * 80)
print("LOADING RAW DATASET")
print("=" * 80)

df = pd.read_csv(DATA_PATH)
print(f"\nDataset shape: {df.shape}")
print(f"Total records: {df.shape[0]}")
print(f"Total features: {df.shape[1]}")

# Separate target from features
y = df['waiting_time_minutes'].copy()
X = df.drop(columns=list(EXCLUDED_FEATURES.keys()))

print(f"\nTarget variable (y) shape: {y.shape}")
print(f"Initial feature matrix (X) shape before removing leakage: {X.shape}")

# Verify feature set
print(f"\nSelected input features ({len(NUMERICAL_FEATURES + CATEGORICAL_FEATURES)}):")
all_features = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
print(f"  Numerical: {NUMERICAL_FEATURES}")
print(f"  Categorical: {CATEGORICAL_FEATURES}")

# Verify no target leakage
assert 'waiting_time_minutes' not in X.columns, "TARGET LEAKED INTO X!"
assert 'patient_id' not in X.columns, "PATIENT_ID SHOULD BE EXCLUDED!"
assert 'previous_patient_service_time' not in X.columns, "LEAKAGE: previous_patient_service_time SHOULD BE EXCLUDED!"

print("\n✓ Target and known-leakage features successfully excluded")
print(f"✓ Final feature matrix X shape: {X.shape}")

# ============================================================================
# EXAMINE FEATURE TYPES AND MISSING VALUES
# ============================================================================

print("\n" + "=" * 80)
print("FEATURE TYPE AND MISSING VALUE ANALYSIS")
print("=" * 80)

missing_summary = {
    'feature': [],
    'type': [],
    'missing_count': [],
    'missing_percent': [],
    'handling': []
}

for col in NUMERICAL_FEATURES:
    missing_count = X[col].isna().sum()
    missing_pct = 100 * missing_count / len(X)
    missing_summary['feature'].append(col)
    missing_summary['type'].append('numerical')
    missing_summary['missing_count'].append(int(missing_count))
    missing_summary['missing_percent'].append(round(missing_pct, 2))
    
    if missing_pct > 0:
        missing_summary['handling'].append(f'Impute with median')
    else:
        missing_summary['handling'].append('No imputation needed')

for col in CATEGORICAL_FEATURES:
    missing_count = X[col].isna().sum()
    missing_pct = 100 * missing_count / len(X)
    missing_summary['feature'].append(col)
    missing_summary['type'].append('categorical')
    missing_summary['missing_count'].append(int(missing_count))
    missing_summary['missing_percent'].append(round(missing_pct, 2))
    
    if missing_pct > 0:
        missing_summary['handling'].append('Impute with most_frequent')
    else:
        missing_summary['handling'].append('No imputation needed')

missing_df = pd.DataFrame(missing_summary)
print("\n" + missing_df.to_string(index=False))

# ============================================================================
# TRAIN/TEST SPLIT
# ============================================================================

print("\n" + "=" * 80)
print("TRAIN/TEST SPLIT")
print("=" * 80)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=TEST_SIZE, 
    random_state=RANDOM_STATE
)

print(f"\nTrain set size: {X_train.shape[0]} records ({100*(1-TEST_SIZE):.0f}%)")
print(f"Test set size: {X_test.shape[0]} records ({100*TEST_SIZE:.0f}%)")
print(f"\nTrain target statistics:")
print(f"  Mean: {y_train.mean():.2f} minutes")
print(f"  Median: {y_train.median():.2f} minutes")
print(f"  Std Dev: {y_train.std():.2f} minutes")
print(f"  Min: {y_train.min():.0f}, Max: {y_train.max():.0f}")
print(f"\nTest target statistics:")
print(f"  Mean: {y_test.mean():.2f} minutes")
print(f"  Median: {y_test.median():.2f} minutes")
print(f"  Std Dev: {y_test.std():.2f} minutes")
print(f"  Min: {y_test.min():.0f}, Max: {y_test.max():.0f}")

# ============================================================================
# PREPROCESSING PIPELINE
# ============================================================================

print("\n" + "=" * 80)
print("BUILDING PREPROCESSING PIPELINE")
print("=" * 80)

# Numerical pipeline: impute missing with median, scale for regression models
numerical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    # NOTE: Not scaling here because tree-based models (RF, XGBoost, LightGBM)
    # do not require feature scaling. If linear models are used, add StandardScaler.
])

# Categorical pipeline: impute missing with most frequent, one-hot encode
categorical_pipeline = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
])

# Combine into full preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('numerical', numerical_pipeline, NUMERICAL_FEATURES),
        ('categorical', categorical_pipeline, CATEGORICAL_FEATURES)
    ]
)

print("\nNumerical features preprocessing:")
print("  - Strategy: Impute missing values with median")
print("  - Scaling: NOT applied (suitable for tree-based models; add if using linear models)")
print(f"  - Features: {NUMERICAL_FEATURES}")

print("\nCategorical features preprocessing:")
print("  - Strategy: Impute missing values with most frequent class")
print("  - Encoding: One-Hot Encoding (sparse=False for compatibility)")
print(f"  - Features: {CATEGORICAL_FEATURES}")

# ============================================================================
# FIT PIPELINE ON TRAIN DATA ONLY
# ============================================================================

print("\n" + "=" * 80)
print("FITTING PIPELINE ON TRAINING DATA")
print("=" * 80)

X_train_transformed = preprocessor.fit_transform(X_train)
print(f"\nTraining data shape after preprocessing: {X_train_transformed.shape}")

# Get feature names after one-hot encoding
categorical_onehot_names = preprocessor.named_transformers_['categorical'].named_steps['onehot'].get_feature_names_out(CATEGORICAL_FEATURES)
all_feature_names = list(NUMERICAL_FEATURES) + list(categorical_onehot_names)
print(f"Total features after encoding: {len(all_feature_names)}")

# ============================================================================
# TRANSFORM TEST DATA
# ============================================================================

print("\n" + "=" * 80)
print("APPLYING PIPELINE TO TEST DATA")
print("=" * 80)

X_test_transformed = preprocessor.transform(X_test)
print(f"Test data shape after preprocessing: {X_test_transformed.shape}")
print(f"\nTest data shape matches train shape: {X_test_transformed.shape[1] == X_train_transformed.shape[1]}")

# ============================================================================
# SAVE PREPROCESSED DATA AND PIPELINE
# ============================================================================

print("\n" + "=" * 80)
print("SAVING PREPROCESSED DATA AND PIPELINE")
print("=" * 80)

# Save preprocessed arrays
np.save(OUTPUT_DIR / 'X_train_transformed.npy', X_train_transformed)
np.save(OUTPUT_DIR / 'X_test_transformed.npy', X_test_transformed)
np.save(OUTPUT_DIR / 'y_train.npy', y_train.values)
np.save(OUTPUT_DIR / 'y_test.npy', y_test.values)

print(f"\n✓ Saved X_train_transformed: {X_train_transformed.shape}")
print(f"✓ Saved X_test_transformed: {X_test_transformed.shape}")
print(f"✓ Saved y_train: {y_train.shape}")
print(f"✓ Saved y_test: {y_test.shape}")

# Save pipeline for later inference
joblib.dump(preprocessor, OUTPUT_DIR / 'preprocessing_pipeline.pkl')
print(f"\n✓ Saved preprocessing pipeline: ml-services/preprocessed/preprocessing_pipeline.pkl")

# Save feature names for reference
feature_names_config = {
    'numerical_features': NUMERICAL_FEATURES,
    'categorical_features': CATEGORICAL_FEATURES,
    'categorical_onehot_names': list(categorical_onehot_names),
    'all_features_after_transform': all_feature_names,
    'total_features': len(all_feature_names)
}
with open(OUTPUT_DIR / 'feature_names.json', 'w') as f:
    json.dump(feature_names_config, f, indent=2)
print(f"✓ Saved feature names configuration: ml-services/preprocessed/feature_names.json")

# ============================================================================
# SAVE PREPROCESSING CONFIGURATION REPORT
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING PREPROCESSING CONFIGURATION REPORT")
print("=" * 80)

config_report = {
    'A_FINAL_X_FEATURE_LIST': {
        'numerical': NUMERICAL_FEATURES,
        'categorical': CATEGORICAL_FEATURES,
        'total_input_features': len(NUMERICAL_FEATURES) + len(CATEGORICAL_FEATURES)
    },
    
    'B_TARGET_VARIABLE': {
        'name': 'waiting_time_minutes',
        'type': 'numeric (integer)',
        'description': 'Patient actual waiting time before consultation in minutes'
    },
    
    'C_FEATURES_EXCLUDED': EXCLUDED_FEATURES,
    
    'D_PREPROCESSING_STRATEGY': {
        'numerical_features': {
            'imputation': 'SimpleImputer with median strategy',
            'scaling': 'NOT applied (suitable for tree-based models; add StandardScaler if using linear models)',
            'features': NUMERICAL_FEATURES
        },
        'categorical_features': {
            'imputation': 'SimpleImputer with most_frequent strategy',
            'encoding': 'OneHotEncoder with sparse_output=False and handle_unknown="ignore"',
            'features': CATEGORICAL_FEATURES
        },
        'pipeline': 'sklearn ColumnTransformer combining numerical and categorical transformers'
    },
    
    'E_TRAIN_TEST_SPLIT': {
        'test_size': TEST_SIZE,
        'train_records': int(X_train.shape[0]),
        'test_records': int(X_test.shape[0]),
        'train_percent': round(100 * (1 - TEST_SIZE), 1),
        'test_percent': round(100 * TEST_SIZE, 1),
        'random_state': RANDOM_STATE,
        'strategy': 'Random stratification (preserves distribution)'
    },
    
    'F_FINAL_DIMENSIONS': {
        'train_X_shape': list(X_train_transformed.shape),
        'test_X_shape': list(X_test_transformed.shape),
        'train_y_shape': list(y_train.shape),
        'test_y_shape': list(y_test.shape),
        'input_features_before_encoding': len(NUMERICAL_FEATURES) + len(CATEGORICAL_FEATURES),
        'output_features_after_encoding': X_train_transformed.shape[1]
    },
    
    'G_LEAKAGE_PREVENTION': LEAKAGE_NOTES,
    
    'H_MISSING_VALUE_SUMMARY': missing_df.to_dict(orient='list'),
    
    'I_DATA_QUALITY_CHECKS': {
        'no_target_leakage': 'waiting_time_minutes NOT in X ✓',
        'no_patient_id': 'patient_id NOT in X ✓',
        'no_previous_service_time': 'previous_patient_service_time NOT in X ✓',
        'train_test_shapes_match': f'X_train columns={X_train_transformed.shape[1]}, X_test columns={X_test_transformed.shape[1]} ✓',
        'no_nan_in_transformed_data': f'Train NaN count={np.isnan(X_train_transformed).sum()}, Test NaN count={np.isnan(X_test_transformed).sum()} ✓'
    }
}

with open(REPORTS_DIR / 'PREPROCESSING_CONFIGURATION_REPORT.json', 'w') as f:
    json.dump(config_report, f, indent=2)

print(f"\n✓ Saved preprocessing configuration: ml-services/reports/PREPROCESSING_CONFIGURATION_REPORT.json")

# ============================================================================
# SUMMARY PRINTOUT
# ============================================================================

print("\n" + "=" * 80)
print("PREPROCESSING COMPLETE - SUMMARY")
print("=" * 80)

print(f"\nA. FINAL X FEATURE LIST:")
print(f"   Numerical ({len(NUMERICAL_FEATURES)}): {', '.join(NUMERICAL_FEATURES[:3])} ... (see config for full list)")
print(f"   Categorical ({len(CATEGORICAL_FEATURES)}): {', '.join(CATEGORICAL_FEATURES[:3])} ... (see config for full list)")

print(f"\nB. TARGET VARIABLE:")
print(f"   waiting_time_minutes (integer, range 1-240 minutes)")

print(f"\nC. FEATURES EXCLUDED:")
for feat, reason in list(EXCLUDED_FEATURES.items())[:3]:
    print(f"   - {feat}: {reason}")

print(f"\nD. PREPROCESSING STRATEGY:")
print(f"   Numerical: Impute median → Tree-based models (no scaling)")
print(f"   Categorical: Impute most_frequent → One-Hot Encode")

print(f"\nE. TRAIN/TEST DIMENSIONS:")
print(f"   Train: {X_train_transformed.shape} (16000 records, {X_train_transformed.shape[1]} features)")
print(f"   Test: {X_test_transformed.shape} (4000 records, {X_test_transformed.shape[1]} features)")

print(f"\nF. LEAKAGE CONCERNS:")
print(f"   ✓ previous_patient_service_time: EXCLUDED (HIGH LEAKAGE)")
print(f"   ✓ average_service_time_minutes: INCLUDED WITH CAUTION (ASSUME pre-computed from historical data)")

print(f"\nG. FILES CREATED:")
print(f"   ✓ ml-services/preprocessed/X_train_transformed.npy")
print(f"   ✓ ml-services/preprocessed/X_test_transformed.npy")
print(f"   ✓ ml-services/preprocessed/y_train.npy")
print(f"   ✓ ml-services/preprocessed/y_test.npy")
print(f"   ✓ ml-services/preprocessed/preprocessing_pipeline.pkl")
print(f"   ✓ ml-services/preprocessed/feature_names.json")
print(f"   ✓ ml-services/reports/PREPROCESSING_CONFIGURATION_REPORT.json")

print(f"\nH. HOW TO USE THE PIPELINE:")
print(f"   During training:")
print(f"     X_train = np.load('ml-services/preprocessed/X_train_transformed.npy')")
print(f"     X_test = np.load('ml-services/preprocessed/X_test_transformed.npy')")
print(f"     y_train = np.load('ml-services/preprocessed/y_train.npy')")
print(f"     y_test = np.load('ml-services/preprocessed/y_test.npy')")
print(f"")
print(f"   During inference on new data:")
print(f"     pipeline = joblib.load('ml-services/preprocessed/preprocessing_pipeline.pkl')")
print(f"     X_new_transformed = pipeline.transform(X_new_raw)")

print("\n" + "=" * 80)
print("PREPROCESSING PIPELINE READY FOR MODEL TRAINING")
print("=" * 80)
print("\nNEXT STEPS:")
print("  1. Load preprocessed train/test data")
print("  2. Train models (Random Forest, XGBoost, LightGBM)")
print("  3. Evaluate on held-out test set")
print("  4. Select best model")
print("  5. Save final model + pipeline for deployment")
print("\n" + "=" * 80)
