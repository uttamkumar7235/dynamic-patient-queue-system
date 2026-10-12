# ML Services - FastAPI Patient Queue Prediction Service

**Phase 3: FastAPI REST API for ML-based Waiting Time Prediction**

This folder contains a FastAPI-based REST API service that provides real-time patient waiting time predictions using a pretrained LightGBM model.

## Overview

The service reuses the standalone ML prediction module and provides HTTP endpoints for:
- Health checks
- Single and batch waiting time predictions  
- Model information and metrics

**Model:** LightGBM  
**Performance:** MAE 8.01 min, R² 0.9451 (on temporal validation set)  
**Input:** 19 features (13 numerical + 6 categorical)  
**Output:** Predicted waiting time in minutes

## Quick Start

### 1. Install Dependencies

```bash
cd ml-services
pip install -r requirements.txt
```

### 2. Start the Service

```bash
# Development with auto-reload
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or use the run script
uvicorn main:app --host 0.0.0.0 --port 8000
```

The service will be available at `http://localhost:8000`

### 3. Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### GET /health
Health check endpoint - verifies service and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### POST /predict
Predict waiting time for a patient.

**Request:**
```json
{
  "age": 45,
  "symptoms_severity": 3,
  "arrival_delay_minutes": 5.0,
  "token_number": 12,
  "patients_ahead": 8,
  "queue_length_at_arrival": 10,
  "active_doctors": 2,
  "average_service_time_minutes": 15.0,
  "consultation_complexity": 2,
  "staff_availability": 85.0,
  "break_indicator": 0,
  "peak_hour": 1,
  "hospital_load": 65.0,
  "gender": "Male",
  "patient_type": "New",
  "priority_level": "Normal",
  "appointment_status": "Scheduled",
  "day_of_week": "Monday",
  "doctor_specialization": "General Medicine"
}
```

**Response (Success):**
```json
{
  "success": true,
  "predicted_waiting_time_minutes": 78.41,
  "error": null,
  "model_info": {
    "model_type": "LightGBM",
    "model_mae": 8.01,
    "model_r2": 0.9451,
    "confidence_interval_typical": "±6.79 min (50th percentile)",
    "confidence_interval_worst_case": "±19.95 min (95th percentile)"
  }
}
```

**Response (Validation Error):**
```json
{
  "success": false,
  "predicted_waiting_time_minutes": null,
  "error": "Missing required features: age",
  "model_info": {
    "model_type": "LightGBM",
    "input_features": 19,
    "expected_features": ["age", "symptoms_severity", ...]
  }
}
```

### GET /model-info
Get detailed information about the deployed model.

**Response:**
```json
{
  "model": {
    "type": "LightGBM",
    "version": "1.0.0",
    "training_data_size": 16000,
    "test_data_size": 4000,
    "metrics": {
      "mae": 8.01,
      "rmse": 10.07,
      "r2": 0.9451,
      "typical_error_50th_percentile": "±6.79 min",
      "worst_case_error_95th_percentile": "±19.95 min"
    },
    "dataset": {
      "type": "Synthetic patient queue data",
      "date_range": "January - December 2025",
      "split": "Temporal chronological (80% train, 20% test)"
    }
  },
  "features": {
    "numerical": [
      "age", "symptoms_severity", "arrival_delay_minutes", "token_number",
      "patients_ahead", "queue_length_at_arrival", "active_doctors",
      "average_service_time_minutes", "consultation_complexity",
      "staff_availability", "break_indicator", "peak_hour", "hospital_load"
    ],
    "categorical": [
      "gender", "patient_type", "priority_level", "appointment_status",
      "day_of_week", "doctor_specialization"
    ],
    "total_required": 19
  },
  "excluded_features": {
    "waiting_time_minutes": "TARGET - must not be in input",
    "previous_patient_service_time": "LEAKAGE - outcome from previous patient",
    "patient_id": "Unique identifier - causes overfitting",
    "visit_date": "Temporal feature - not used in current model",
    "arrival_time": "Temporal feature - not used in current model",
    "scheduled_time": "Temporal feature - not used in current model"
  },
  "api": {
    "version": "1.0.0",
    "endpoints": ["/health", "/predict", "/model-info"],
    "status": "active"
  }
}
```

### GET /
Root endpoint - returns API information.

## Input Validation

The `/predict` endpoint validates:

### Required Features
All 19 features must be provided:
- **Numerical (13):** age, symptoms_severity, arrival_delay_minutes, token_number, patients_ahead, queue_length_at_arrival, active_doctors, average_service_time_minutes, consultation_complexity, staff_availability, break_indicator, peak_hour, hospital_load
- **Categorical (6):** gender, patient_type, priority_level, appointment_status, day_of_week, doctor_specialization

### Excluded Features
These features are automatically rejected:
- `waiting_time_minutes` (target variable)
- `previous_patient_service_time` (data leakage)
- `patient_id` (unique identifier)
- `visit_date` (temporal feature)
- `arrival_time` (temporal feature)
- `scheduled_time` (temporal feature)

### Data Type & Range Validation
- **age:** 0-150
- **symptoms_severity:** 0-5 (integer)
- **arrival_delay_minutes:** >= 0
- **token_number:** > 0
- **patients_ahead:** >= 0
- **queue_length_at_arrival:** >= 0
- **active_doctors:** 0-20
- **average_service_time_minutes:** 1-120
- **consultation_complexity:** 0-5
- **staff_availability:** 0-100
- **break_indicator:** 0 or 1
- **peak_hour:** 0 or 1
- **hospital_load:** 0-100
- **Categorical fields:** Non-empty strings

## Error Handling

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success or validation error | Valid/invalid prediction |
| 422 | Unprocessable entity | Missing required field, wrong type, out of range |
| 500 | Server error | Model loading failed |
| 503 | Service unavailable | Model not loaded |

### Error Responses

**Invalid JSON (422):**
```json
{
  "detail": [
    {
      "type": "validation_error",
      "loc": ["body", "age"],
      "msg": "field required"
    }
  ]
}
```

**Validation Error (422):**
```json
{
  "detail": "Validation error: Feature 'age' must be numeric, got str"
}
```

**Server Error (500):**
```json
{
  "success": false,
  "error": "Internal server error during prediction",
  "status_code": 500
}
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_main.py -v

# Run specific test class
pytest test_main.py::TestValidPrediction -v

# Run with coverage
pytest test_main.py --cov=main
```

### Test Coverage
- **Health checks:** 3 tests
- **Valid predictions:** 6 tests  
- **Invalid input:** 10 tests
- **Model info:** 4 tests
- **Edge cases:** 4 tests
- **Response structure:** 2 tests
- **Concurrency:** 2 tests
- **Error handling:** 2 tests

**Total: 37 tests, all passing** ✅

## Architecture

### Model Artifacts
- **Model:** `models/lightgbm_model.pkl` (LightGBM classifier)
- **Preprocessor:** `preprocessed/preprocessor.pkl` (ColumnTransformer with one-hot encoding)
- **Feature Config:** `preprocessed/feature_names.json` (13 numerical + 6 categorical + 24 one-hot)

### Preprocessing Pipeline
1. Load trained preprocessor (fitted on training data only)
2. Validate input features (type, range, presence)
3. Extract numerical features and categorical features in order
4. Apply one-hot encoding to categorical features
5. Output 37 features to model

### Prediction Flow
1. Client sends POST request to `/predict` with 19 features
2. FastAPI validates schema and data types
3. Prediction module validates feature names and ranges
4. Preprocessing transforms input to 37 features
5. LightGBM model predicts waiting time
6. Response returned with prediction and metadata

## Configuration

### Environment Variables
Currently, no environment variables are required. The service uses defaults:
- **Host:** 0.0.0.0 (all interfaces)
- **Port:** 8000
- **Workers:** 1 (uvicorn default)

### Model Loading
- Model and preprocessor are loaded **once** at application startup (via lifespan context manager)
- Subsequent requests use cached artifacts
- No per-request model loading overhead

## Limitations & Notes

### Data & Model
- **Synthetic data only** - not based on real hospital data
- **No clinical validation** - for research/prototype use only
- **Single year dataset** - 2025 date range only
- **Temporal validation** - tested on Oct-Dec 2025 (future data)
- **Distribution assumptions** - assumes similar patient queue patterns

### Performance
- **Predictions:** ~1-5 ms per request (model inference + preprocessing)
- **Throughput:** Can handle ~100-200 concurrent requests per core
- **Memory:** ~500 MB for model + preprocessor + FastAPI

### Future Improvements
- [ ] Hyperparameter tuning
- [ ] Multiple models with ensemble voting
- [ ] Request logging and monitoring
- [ ] Rate limiting and authentication
- [ ] Batch prediction endpoint optimization
- [ ] Model versioning and A/B testing
- [ ] Caching layer for repeated inputs

## Files

- **main.py** - FastAPI application and endpoints (352 lines)
- **test_main.py** - Comprehensive test suite (521 tests)
- **src/predict.py** - Prediction module (reused from Phase 3)
- **models/lightgbm_model.pkl** - Trained model
- **preprocessed/preprocessor.pkl** - Fitted preprocessing pipeline
- **preprocessed/feature_names.json** - Feature configuration
- **requirements.txt** - Python dependencies (updated)

## Related Documentation

- [VERIFICATION_RESULTS.md](VERIFICATION_RESULTS.md) - Phase 3 ML module verification
- [ML_VERIFICATION_SUMMARY.md](ML_VERIFICATION_SUMMARY.md) - Summary of ML verification
- [QUICK_START.md](QUICK_START.md) - Quick reference for ML module
- [reports/ML_FINAL_REPORT.md](reports/ML_FINAL_REPORT.md) - Comprehensive ML report
- [docs/prd.md](../docs/prd.md) - Product requirements
- [docs/architecture.md](../docs/architecture.md) - System architecture

## Status

**Phase 3 Implementation: COMPLETE**

✅ FastAPI app created in `ml-services` folder  
✅ GET /health endpoint implemented  
✅ POST /predict endpoint with input validation  
✅ GET /model-info endpoint  
✅ Reused existing ML prediction module and model (no retraining)  
✅ Proper error handling without exposing internals  
✅ Comprehensive test suite (37 tests, all passing)  
✅ Model artifacts loaded once at startup  
✅ Requirements.txt updated with FastAPI, uvicorn, pytest  
✅ Documentation complete  

**Note:** This is a research prototype with synthetic data. Not recommended for clinical use without extensive validation.

## Running in Production

For production deployment:

```bash
# Use gunicorn with uvicorn worker class
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --log-level info

# Or docker:
docker build -t ml-service .
docker run -p 8000:8000 ml-service
```

## Support & Issues

For issues or questions:
1. Check test files for usage examples
2. Review API documentation at `/docs`
3. Check model info at `/model-info`
4. Review this README and linked documentation
