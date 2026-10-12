"""
FastAPI ML Service for Patient Queue Waiting Time Prediction

Provides REST API endpoints for:
- Health check
- Single patient waiting time prediction
- Model information

Uses:
- LightGBM model (trained on 16k records, MAE: 8.01 min)
- Preprocessing pipeline (fitted on training data only)
- 19 input features with comprehensive validation
"""

import logging
from pathlib import Path
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
import numpy as np

# Import the prediction module
from src.predict import (
    predict_waiting_time,
    load_artifacts,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    EXCLUDED_FEATURES
)

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# STARTUP / SHUTDOWN
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load model artifacts on startup, clean up on shutdown.
    """
    logger.info("Loading model artifacts...")
    try:
        load_artifacts()
        logger.info("Model artifacts loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model artifacts: {e}")
        raise
    
    yield
    
    logger.info("Shutting down...")

# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Patient Queue ML Service",
    description="ML service for predicting patient waiting times",
    version="1.0.0",
    lifespan=lifespan
)

# ============================================================================
# DATA MODELS
# ============================================================================

class PredictionInput(BaseModel):
    """Input schema for waiting time prediction."""
    
    # Numerical features
    age: float = Field(..., ge=0, le=150, description="Patient age (0-150)")
    symptoms_severity: int = Field(..., ge=0, le=5, description="Severity score (0-5)")
    arrival_delay_minutes: float = Field(..., ge=0, description="Minutes late from arrival time")
    token_number: int = Field(..., gt=0, description="Queue token number")
    patients_ahead: int = Field(..., ge=0, description="Number of patients ahead")
    queue_length_at_arrival: int = Field(..., ge=0, description="Queue length at arrival")
    active_doctors: int = Field(..., ge=0, le=20, description="Number of active doctors (0-20)")
    average_service_time_minutes: float = Field(..., ge=1, le=120, description="Average service time (1-120 min)")
    consultation_complexity: int = Field(..., ge=0, le=5, description="Complexity score (0-5)")
    staff_availability: float = Field(..., ge=0, le=100, description="Staff availability percentage (0-100)")
    break_indicator: int = Field(..., ge=0, le=1, description="Break indicator (0 or 1)")
    peak_hour: int = Field(..., ge=0, le=1, description="Peak hour indicator (0 or 1)")
    hospital_load: float = Field(..., ge=0, le=100, description="Hospital load percentage (0-100)")
    
    # Categorical features
    gender: str = Field(..., description="Patient gender (e.g., 'Male', 'Female')")
    patient_type: str = Field(..., description="Type of patient (e.g., 'New', 'Follow-up')")
    priority_level: str = Field(..., description="Priority level (e.g., 'Normal', 'Urgent')")
    appointment_status: str = Field(..., description="Appointment status (e.g., 'Scheduled', 'Walk-in')")
    day_of_week: str = Field(..., description="Day of week (e.g., 'Monday', 'Tuesday')")
    doctor_specialization: str = Field(..., description="Doctor specialization (e.g., 'Cardiology', 'General Medicine')")
    
    @validator('gender', 'patient_type', 'priority_level', 'appointment_status', 'day_of_week', 'doctor_specialization')
    def validate_categorical(cls, v):
        """Ensure categorical fields are non-empty strings."""
        if not isinstance(v, str) or len(v.strip()) == 0:
            raise ValueError("Categorical field must be a non-empty string")
        return v.strip()
    
    @validator('age', 'arrival_delay_minutes', 'average_service_time_minutes', 
               'staff_availability', 'hospital_load')
    def validate_finite(cls, v):
        """Ensure numerical fields are finite."""
        if not np.isfinite(v):
            raise ValueError("Numerical field must be a finite number")
        return v

    class Config:
        schema_extra = {
            "example": {
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
        }

class PredictionResponse(BaseModel):
    """Response schema for waiting time prediction."""
    success: bool = Field(..., description="Whether prediction succeeded")
    predicted_waiting_time_minutes: Optional[float] = Field(None, ge=0, description="Predicted waiting time in minutes")
    error: Optional[str] = Field(None, description="Error message if prediction failed")
    model_info: dict = Field(..., description="Model metadata and performance info")

class HealthResponse(BaseModel):
    """Response schema for health check."""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(..., description="API version")

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the ML service is running and model is loaded"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns service status and whether the model is loaded.
    """
    try:
        # Verify model is loaded by checking if predict module can be called
        load_artifacts()
        return HealthResponse(
            status="healthy",
            model_loaded=True,
            version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not available"
        )

@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
    summary="Predict Waiting Time",
    description="Predict patient waiting time based on queue and patient information",
    responses={
        200: {"description": "Prediction successful or validation error"},
        400: {"description": "Invalid input format"},
        422: {"description": "Validation error in input data"},
        500: {"description": "Internal server error"}
    }
)
async def predict(input_data: PredictionInput) -> PredictionResponse:
    """
    Predict waiting time for a patient.
    
    Accepts:
    - 13 numerical features (age, symptoms severity, queue metrics, etc.)
    - 6 categorical features (gender, patient type, priority level, etc.)
    
    Returns:
    - Predicted waiting time in minutes
    - Model performance metrics
    - Error details if validation fails
    
    Automatically rejects:
    - Target variable (waiting_time_minutes)
    - Leakage features (previous_patient_service_time)
    - Temporal features (patient_id, visit_date, etc.)
    - Invalid data types or out-of-range values
    """
    try:
        # Convert input to dictionary
        input_dict = input_data.dict()
        
        logger.info(f"Received prediction request for patient with token {input_dict.get('token_number')}")
        
        # Call prediction module
        result = predict_waiting_time(input_dict)
        
        if result['success']:
            logger.info(f"Prediction successful: {result['predicted_waiting_time_minutes']:.2f} minutes")
            return PredictionResponse(
                success=True,
                predicted_waiting_time_minutes=result['predicted_waiting_time_minutes'],
                error=None,
                model_info=result['model_info']
            )
        else:
            # Validation or prediction error
            logger.warning(f"Prediction failed: {result['error']}")
            return PredictionResponse(
                success=False,
                predicted_waiting_time_minutes=None,
                error=result.get('error', 'Unknown error'),
                model_info=result['model_info']
            )
    
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=False)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during prediction"
        )

@app.get(
    "/model-info",
    tags=["Information"],
    summary="Model Information",
    description="Get information about the deployed model"
)
async def model_info():
    """
    Return information about the deployed model.
    
    Includes:
    - Model type and version
    - Performance metrics
    - Input feature requirements
    - Excluded features
    """
    return {
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
            "numerical": NUMERICAL_FEATURES,
            "categorical": CATEGORICAL_FEATURES,
            "total_required": len(NUMERICAL_FEATURES) + len(CATEGORICAL_FEATURES)
        },
        "excluded_features": EXCLUDED_FEATURES,
        "api": {
            "version": "1.0.0",
            "endpoints": ["/health", "/predict", "/model-info"],
            "status": "active"
        }
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions without exposing internal details."""
    return {
        "success": False,
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions safely."""
    logger.error(f"Unexpected error: {exc}", exc_info=False)
    return {
        "success": False,
        "error": "Internal server error",
        "status_code": 500
    }

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Information"])
async def root():
    """Root endpoint - returns API information."""
    return {
        "service": "Patient Queue ML Service",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "health": "GET /health",
            "predict": "POST /predict",
            "model_info": "GET /model-info"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
