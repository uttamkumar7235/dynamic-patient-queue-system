# QUICK START: PREDICTION MODULE
## Using the LightGBM Model

---

## Quick Test

```bash
cd ml-services
.venv\Scripts\python.exe src/predict.py
```

Expected output:
```
✅ ALL TESTS PASSED
Predicted waiting time: 78.41 minutes
```

---

## Using Predictions in Code

```python
from src.predict import predict_waiting_time

# Prepare input (19 required features)
input_data = {
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

# Get prediction
result = predict_waiting_time(input_data)

# Check result
if result['success']:
    wait_time = result['predicted_waiting_time_minutes']
    mae = result['model_info']['model_mae']
    print(f"Predicted wait: {wait_time:.1f} ± {mae} minutes")
else:
    print(f"Error: {result['error']}")
```

---

## Model Performance

| Metric | Value |
|--------|-------|
| MAE | 8.01 min |
| R² | 0.9451 |
| Typical Error (50th) | ±6.79 min |
| Worst Error (95th) | ±19.95 min |

---

## Required Features (19 Total)

**Numerical (13):**
age, symptoms_severity, arrival_delay_minutes, token_number, patients_ahead, 
queue_length_at_arrival, active_doctors, average_service_time_minutes, 
consultation_complexity, staff_availability, break_indicator, peak_hour, hospital_load

**Categorical (6):**
gender, patient_type, priority_level, appointment_status, day_of_week, doctor_specialization

---

## Excluded Features (Cannot Use)

- waiting_time_minutes ❌ (target)
- previous_patient_service_time ❌ (leakage)
- patient_id ❌ (overfitting)
- visit_date ❌ (use day_of_week)
- arrival_time ❌ (use peak_hour)
- scheduled_time ❌ (redundant)

---

## What's Saved

✅ `models/lightgbm_model.pkl` - Trained model (37 features)
✅ `preprocessed/preprocessor.pkl` - Fitted preprocessing (19 → 37)
✅ `preprocessed/feature_names.json` - Feature config
✅ `src/predict.py` - Prediction module
✅ `reports/ML_FINAL_REPORT.md` - Full documentation

---

## Status

🟢 **Prediction Module:** Operational ✅
🟢 **Input Validation:** Complete ✅  
🟢 **Test Coverage:** 100% ✅  
🟢 **Documentation:** Comprehensive ✅  

🔴 **Production:** Synthetic data only, not for clinical use

---

See `PHASE3_COMPLETION.md` for detailed summary.
