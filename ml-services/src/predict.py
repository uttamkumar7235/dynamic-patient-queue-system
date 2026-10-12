"""
Prediction Module for Patient Queue Waiting Time

Purpose:
- Load saved preprocessing pipeline and LightGBM model
- Validate input features
- Return predicted waiting time in minutes
- Exclude target variable and leakage features

Model: LightGBM (Temporal Validation Results)
- MAE: 8.01 min
- R²: 0.9451
- Trained on 16,000 records (temporal split)
"""

import numpy as np
import pandas as pd
import json
import joblib
from pathlib import Path
from typing import Dict, Tuple, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT / 'models'
PREPROCESSED_DIR = ROOT / 'preprocessed'

# Features (matching preprocessing pipeline)
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

ALL_INPUT_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# Excluded features (cannot use for prediction)
EXCLUDED_FEATURES = {
    'waiting_time_minutes': 'TARGET - must not be in input',
    'patient_id': 'Unique identifier - causes overfitting',
    'previous_patient_service_time': 'LEAKAGE - outcome from previous patient',
    'visit_date': 'Temporal feature - not used in current model',
    'arrival_time': 'Temporal feature - not used in current model',
    'scheduled_time': 'Temporal feature - not used in current model',
}

# ============================================================================
# GLOBAL STATE (loaded once)
# ============================================================================

_model = None
_preprocessor = None
_feature_config = None

# ============================================================================
# INITIALIZATION
# ============================================================================

def load_artifacts():
    """Load preprocessing pipeline, model, and feature configuration."""
    global _model, _preprocessor, _feature_config
    
    if _model is not None:
        return  # Already loaded
    
    # Load feature configuration
    with open(PREPROCESSED_DIR / 'feature_names.json', 'r') as f:
        _feature_config = json.load(f)
    
    # Load preprocessor (fitted on training data)
    _preprocessor = joblib.load(PREPROCESSED_DIR / 'preprocessor.pkl')
    
    # Load model
    _model = joblib.load(MODELS_DIR / 'lightgbm_model.pkl')

# ============================================================================
# VALIDATION
# ============================================================================

def validate_input(input_dict: Dict) -> Tuple[bool, str]:
    """
    Validate that input contains required features and no excluded features.
    
    Returns:
        (is_valid, error_message)
    """
    # Check for excluded features
    for excluded_feature in EXCLUDED_FEATURES.keys():
        if excluded_feature in input_dict:
            return False, f"Feature '{excluded_feature}' not allowed: {EXCLUDED_FEATURES[excluded_feature]}"
    
    # Check for required features
    missing = []
    for feature in ALL_INPUT_FEATURES:
        if feature not in input_dict:
            missing.append(feature)
    
    if missing:
        return False, f"Missing required features: {', '.join(missing)}"
    
    # Type and value validation
    for feature in NUMERICAL_FEATURES:
        val = input_dict[feature]
        if not isinstance(val, (int, float, np.number)):
            return False, f"Feature '{feature}' must be numeric, got {type(val).__name__}"
        if not np.isfinite(val):
            return False, f"Feature '{feature}' must be finite (not NaN or Inf)"
    
    for feature in CATEGORICAL_FEATURES:
        val = input_dict[feature]
        if not isinstance(val, str):
            return False, f"Feature '{feature}' must be string, got {type(val).__name__}"
        if len(val.strip()) == 0:
            return False, f"Feature '{feature}' must not be empty"
    
    return True, ""

# ============================================================================
# PREDICTION
# ============================================================================

def predict_waiting_time(input_dict: Dict) -> Dict:
    """
    Predict waiting time for a single patient.
    
    Args:
        input_dict: Dictionary with 19 required features (excluding target and leakage features)
        
    Returns:
        {
            'success': bool,
            'predicted_waiting_time_minutes': float (if success),
            'error': str (if not success),
            'model_info': dict (metadata)
        }
    
    Example:
        >>> input_data = {
        ...     'age': 45,
        ...     'symptoms_severity': 3,
        ...     'arrival_delay_minutes': 5.0,
        ...     'token_number': 12,
        ...     'patients_ahead': 8,
        ...     'queue_length_at_arrival': 10,
        ...     'active_doctors': 2,
        ...     'average_service_time_minutes': 15.0,
        ...     'consultation_complexity': 2,
        ...     'staff_availability': 85.0,
        ...     'break_indicator': 0,
        ...     'peak_hour': 1,
        ...     'hospital_load': 65.0,
        ...     'gender': 'Male',
        ...     'patient_type': 'New',
        ...     'priority_level': 'Normal',
        ...     'appointment_status': 'Scheduled',
        ...     'day_of_week': 'Monday',
        ...     'doctor_specialization': 'General Medicine'
        ... }
        >>> result = predict_waiting_time(input_data)
        >>> print(f"Predicted wait: {result['predicted_waiting_time_minutes']:.2f} min")
    """
    
    # Load artifacts on first call
    load_artifacts()
    
    # Validate input
    is_valid, error_msg = validate_input(input_dict)
    if not is_valid:
        return {
            'success': False,
            'error': error_msg,
            'model_info': {
                'model_type': 'LightGBM',
                'input_features': len(ALL_INPUT_FEATURES),
                'expected_features': ALL_INPUT_FEATURES
            }
        }
    
    try:
        # Prepare input dataframe with correct feature order
        input_df = pd.DataFrame([input_dict])
        input_df = input_df[ALL_INPUT_FEATURES]  # Ensure correct order
        
        # Transform input
        X_transformed = _preprocessor.transform(input_df)
        
        # Predict
        prediction = _model.predict(X_transformed)[0]
        
        # Validate prediction output
        if not np.isfinite(prediction):
            return {
                'success': False,
                'error': f"Model returned invalid prediction: {prediction}",
                'model_info': {'model_type': 'LightGBM'}
            }
        
        if prediction < 0:
            # Clip to realistic minimum
            prediction = max(1.0, prediction)
        
        return {
            'success': True,
            'predicted_waiting_time_minutes': float(prediction),
            'model_info': {
                'model_type': 'LightGBM',
                'model_mae': 8.01,
                'model_r2': 0.9451,
                'confidence_interval_typical': f"±{6.79:.2f} min (50th percentile)",
                'confidence_interval_worst_case': f"±{19.95:.2f} min (95th percentile)"
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': f"Prediction failed: {str(e)}",
            'model_info': {'model_type': 'LightGBM'}
        }

# ============================================================================
# INFERENCE PIPELINE
# ============================================================================

def predict_batch(input_list: list) -> list:
    """
    Predict waiting time for multiple patients.
    
    Args:
        input_list: List of input dictionaries
        
    Returns:
        List of prediction results
    """
    load_artifacts()
    results = [predict_waiting_time(inp) for inp in input_list]
    return results

# ============================================================================
# CLI / STANDALONE EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Test case: Valid input
    sample_input = {
        'age': 45,
        'symptoms_severity': 3,
        'arrival_delay_minutes': 5.0,
        'token_number': 12,
        'patients_ahead': 8,
        'queue_length_at_arrival': 10,
        'active_doctors': 2,
        'average_service_time_minutes': 15.0,
        'consultation_complexity': 2,
        'staff_availability': 85.0,
        'break_indicator': 0,
        'peak_hour': 1,
        'hospital_load': 65.0,
        'gender': 'Male',
        'patient_type': 'New',
        'priority_level': 'Normal',
        'appointment_status': 'Scheduled',
        'day_of_week': 'Monday',
        'doctor_specialization': 'General Medicine'
    }
    
    print("=" * 80)
    print("WAITING TIME PREDICTION MODULE TEST")
    print("=" * 80)
    print("\n[1] Testing valid input...")
    result = predict_waiting_time(sample_input)
    
    if result['success']:
        pred = result['predicted_waiting_time_minutes']
        print(f"  [PASS] Prediction successful")
        print(f"    Predicted waiting time: {pred:.2f} minutes")
        print(f"    Model: {result['model_info']['model_type']}")
        print(f"    MAE: {result['model_info']['model_mae']} min")
        print(f"    R²: {result['model_info']['model_r2']}")
        print(f"    Typical error: {result['model_info']['confidence_interval_typical']}")
        print(f"    Worst-case error: {result['model_info']['confidence_interval_worst_case']}")
        
        # Validation checks
        assert isinstance(pred, float), "Prediction not float"
        assert np.isfinite(pred), "Prediction not finite"
        assert pred > 0, "Prediction not positive"
        print(f"\n  [PASS] All validation checks passed")
    else:
        print(f"  [FAIL] Prediction failed: {result['error']}")
        exit(1)
    
    print("\n[2] Testing invalid input (missing feature)...")
    bad_input = sample_input.copy()
    del bad_input['age']
    result = predict_waiting_time(bad_input)
    assert not result['success'], "Should reject missing feature"
    assert 'Missing' in result['error'], "Error message unclear"
    print(f"  [PASS] Correctly rejected: {result['error']}")
    
    print("\n[3] Testing excluded feature rejection...")
    bad_input = sample_input.copy()
    bad_input['waiting_time_minutes'] = 100  # Target variable
    result = predict_waiting_time(bad_input)
    assert not result['success'], "Should reject target variable"
    print(f"  [PASS] Correctly rejected: {result['error']}")
    
    print("\n" + "=" * 80)
    print("[SUCCESS] ALL TESTS PASSED")
    print("=" * 80)
