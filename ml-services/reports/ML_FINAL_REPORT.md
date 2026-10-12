# ML FINAL REPORT
## AI-Based Dynamic Patient Queue and Waiting Time Prediction System

**Report Date:** October 12, 2026  
**Report Status:** Synthetic Data Research Prototype - No Clinical Validation  
**Phase:** Baseline Model Selection & Prediction Module Complete  
**Data Type:** Synthetic (Research Use Only)

---

## 1. PROJECT OVERVIEW

**Project Name:** AI-Based Dynamic Patient Queue and Waiting Time Prediction System  
**Objective:** Build a machine learning model to predict patient waiting times in a hospital queue  
**Dataset:** Synthetically generated patient queue data  
**Model Type:** Regression (predicting continuous waiting time in minutes)  
**Technology Stack:** Python, scikit-learn, XGBoost, LightGBM, pandas, numpy

**Status:** ✅ Prediction module operational; ready for integration

---

## 2. DATASET CHARACTERISTICS

### Data Source & Size
- **Total Records:** 20,000 patient queue entries
- **Time Range:** January 1, 2025 to December 31, 2025 (1 year)
- **Fields:** 26 columns (features + target + excluded)
- **Data Type:** Synthetic (generated, not from real hospital)

### Target Variable
- **Name:** `waiting_time_minutes`
- **Type:** Continuous numeric (integer)
- **Range:** 1 to 240 minutes
- **Mean:** ~74 minutes (both train and test)
- **Std Dev:** ~45 minutes
- **Distribution:** Right-skewed with long tail

### Input Feature Set (19 Features)

**Numerical Features (13):**
1. `age` - Patient age in years
2. `symptoms_severity` - Severity level 1-5
3. `arrival_delay_minutes` - Minutes late vs scheduled
4. `token_number` - Sequential queue token
5. `patients_ahead` - Number of patients in queue ahead
6. `queue_length_at_arrival` - Total queue size at arrival
7. `active_doctors` - Number of available doctors
8. `average_service_time_minutes` - Historical avg consultation time
9. `consultation_complexity` - Complexity level 1-5
10. `staff_availability` - Percentage of staff available
11. `break_indicator` - Binary (0=no break, 1=on break)
12. `peak_hour` - Binary (0=off-peak, 1=peak hours)
13. `hospital_load` - Hospital occupancy percentage

**Categorical Features (6):**
1. `gender` - Female, Male, Other
2. `patient_type` - New, Follow-up
3. `priority_level` - Normal, Urgent, Emergency
4. `appointment_status` - Scheduled, Walk-in
5. `day_of_week` - Monday through Sunday
6. `doctor_specialization` - Cardiology, Dermatology, ENT, General Medicine, Gynecology, Orthopedics, Pediatrics

### Excluded Features & Reasons
| Feature | Reason |
|---------|--------|
| `waiting_time_minutes` | Target variable - cannot be input |
| `patient_id` | Unique identifier; causes overfitting |
| `previous_patient_service_time` | **LEAKAGE** - outcome from previous patient after current patient arrives |
| `visit_date` | Temporal feature; use `day_of_week` as proxy |
| `arrival_time` | Temporal feature; use `peak_hour` as proxy |
| `scheduled_time` | Temporal feature; redundant with `arrival_delay_minutes` |

---

## 3. DATA PREPROCESSING

### Pipeline Overview

**Step 1: Feature Selection**
- Select 19 features (13 numerical + 6 categorical)
- Exclude 6 leakage-prone and redundant features
- Preserve all raw data (never modify source CSV)

**Step 2: Numerical Imputation**
- Strategy: Median imputation
- Features: All 13 numerical features
- Missing value handling: Replace NaN with column median

**Step 3: Categorical Encoding**
- Strategy: One-hot encoding
- Missing value handling: Most frequent category
- Unknown categories: Ignore (don't create new category)

**Step 4: Train/Test Split**
- Method: Temporal chronological split (simulates real deployment)
- Training: Earlier records (80%, Jan-Oct 2025, 16,000 records)
- Testing: Later records (20%, Oct-Dec 2025, 4,000 records)
- Fit preprocessing on training data ONLY (prevent leakage)

### Feature Transformation
- **Input Features:** 19 (13 numerical + 6 categorical)
- **After One-Hot Encoding:** 37 features
  - Numerical: 13 (unchanged)
  - One-hot encoded: 24 (from 6 categorical with multiple categories)
- **Example Expansion:** 
  - `gender` (3 categories) → `gender_Female`, `gender_Male`, `gender_Other` (3 features)
  - `doctor_specialization` (7 specializations) → 7 one-hot features

### No Scaling
- Tree-based models (XGBoost, LightGBM, Random Forest) are invariant to feature scaling
- Scaling not applied (speeds up preprocessing, maintains interpretability)

---

## 4. BASELINE MODEL TRAINING (Phase 1)

### Training Configuration
- **Data:** Random 80/20 split with seed=42
- **Models Trained:** 4 baseline models
- **Hyperparameters:** Default/conservative settings (no tuning)
- **Evaluation Metric:** MAE, RMSE, R², Median AE, P95 AE

### Baseline Results (Random 80/20 Split)

| Model | MAE | RMSE | R² | Median AE | P95 AE | Status |
|-------|-----|------|-----|-----------|---------|--------|
| Linear Regression | 13.31 min | 18.37 min | 0.8314 | 9.97 min | 37.04 min | ✅ |
| Random Forest | 8.54 min | 10.89 min | 0.9407 | 7.06 min | 21.75 min | ✅ |
| **XGBoost** | **8.16 min** | **10.38 min** | **0.9462** | **6.69 min** | **20.80 min** | ✅ |
| **LightGBM** | **8.16 min** | **10.38 min** | **0.9461** | **6.61 min** | **20.84 min** | ✅ |

**Key Observations:**
- Boosted models (XGBoost, LightGBM) dramatically outperform linear baseline
- XGBoost and LightGBM show nearly identical performance
- Tree models reduce MAE by 38-39% vs linear regression baseline
- Tree models explain 94% of variance vs 83% for linear

---

## 5. FEATURE IMPORTANCE ANALYSIS (Phase 1)

### XGBoost Top 10 Features
1. `doctor_specialization_General Medicine` (41.2%)
2. `peak_hour` (14.2%)
3. `doctor_specialization_Cardiology` (13.8%)
4. `priority_level_Normal` (9.4%)
5. `active_doctors` (5.3%)
6. `priority_level_Emergency` (4.3%)
7. `patients_ahead` (3.0%)
8. `average_service_time_minutes` (1.6%)
9. `doctor_specialization_Dermatology` (1.5%)
10. `queue_length_at_arrival` (1.1%)

**Interpretation:** Doctor specialization and peak hours dominate predictions; queue metrics are secondary.

### LightGBM Top 10 Features
1. `average_service_time_minutes` (20.3%)
2. `patients_ahead` (12.3%)
3. `hospital_load` (8.4%)
4. `active_doctors` (8.3%)
5. `priority_level_Normal` (5.5%)
6. `age` (4.9%)
7. `staff_availability` (4.7%)
8. `queue_length_at_arrival` (4.4%)
9. `priority_level_Emergency` (4.3%)
10. `arrival_delay_minutes` (3.8%)

**Interpretation:** LightGBM emphasizes service time and queue state metrics; more distributed feature usage than XGBoost.

---

## 6. TEMPORAL VALIDATION ANALYSIS (Phase 2)

### Temporal Split Methodology
- **Purpose:** Validate model generalization to chronologically future data
- **Train Set:** 16,000 records (Jan 1 - Oct 17, 2025)
- **Test Set:** 4,000 records (Oct 17 - Dec 31, 2025)
- **Split Type:** Chronological (not random)
- **Preprocessing:** Fit ONLY on training data (simulate real deployment)

### Distribution Shift Detected
- Training mean: 75.50 min
- Testing mean: 69.46 min
- **Difference:** -6.04 min (-7.9%)
- **Interpretation:** Later periods have slightly shorter wait times

### Temporal Validation Results

| Model | MAE | RMSE | R² | Median AE | P95 AE | vs Baseline |
|-------|-----|------|-----|-----------|---------|------------|
| Linear Regression | 13.18 min | 17.91 min | 0.8267 | 10.03 min | 36.27 min | +0.98% ↑ |
| Random Forest | 8.57 min | 10.85 min | 0.9363 | 7.10 min | 21.61 min | -0.35% ↑ |
| **XGBoost** | **8.06 min** | **10.15 min** | **0.9443** | **6.77 min** | **20.57 min** | **+1.23% ↑** |
| **LightGBM** | **8.01 min** | **10.07 min** | **0.9451** | **6.79 min** | **19.95 min** | **+1.84% ↑** |

**Key Finding:** All models perform within ±2% of baseline, showing excellent generalization to temporal shift.

### Ranking Stability
- **Baseline Ranking:** LightGBM ≈ XGBoost > Random Forest > Linear ✅
- **Temporal Ranking:** LightGBM > XGBoost > Random Forest > Linear ✅
- **Stability:** Perfect (identical ranking)

---

## 7. MODEL SELECTION & RECOMMENDATION

### Selection Criteria
1. **Performance:** MAE (primary), R² (secondary)
2. **Robustness:** Consistency across random and temporal splits
3. **Generalization:** Performance on unseen future data
4. **Error Bounds:** Median AE and P95 AE for operational context
5. **Interpretability:** Feature importance explainability (secondary)

### Selected Model: **LightGBM**

**Justification:**
- ✅ **Best MAE:** 8.01 min (temporal validation)
- ✅ **Excellent R²:** 0.9451 (explains 94.51% of variance)
- ✅ **Improved P95 AE:** 19.95 min (-4.3% vs baseline, best worst-case error)
- ✅ **Temporal Robust:** +1.84% improvement vs baseline on temporal data
- ✅ **Training Speed:** Fast (~156ms for 16k samples)
- ✅ **Inference Speed:** Fast (<10ms per prediction)
- ✅ **Implementation:** Stable, production-ready

**Model Artifacts:**
- Location: `ml-services/models/lightgbm_model.pkl`
- Input Features: 37 (13 numerical + 24 one-hot)
- Output: Single numeric value (predicted waiting time in minutes)

### Alternative Models
- **XGBoost:** Nearly identical performance (8.06 min MAE); alternative if LightGBM unavailable
- **Random Forest:** Solid fallback (8.57 min MAE); better interpretability
- **Linear Regression:** Not recommended (13.18 min MAE); 38% higher error

---

## 8. PREDICTION MODULE

### Module: `src/predict.py`

**Purpose:** Load preprocessing pipeline and LightGBM model; return predictions for single patients

**Key Functions:**

```python
# Main prediction function
result = predict_waiting_time(input_dict)
# input_dict: 19 required features (excluding target and leakage)
# Returns: {'success': bool, 'predicted_waiting_time_minutes': float, ...}

# Batch prediction
results = predict_batch(input_list)
# input_list: List of input dictionaries
# Returns: List of prediction results
```

**Input Validation:**
- ✅ Rejects target variable (`waiting_time_minutes`)
- ✅ Rejects leakage features (`previous_patient_service_time`)
- ✅ Checks for all 19 required features
- ✅ Validates numerical types and finiteness
- ✅ Validates categorical types and non-empty strings

**Output Format:**
```json
{
  "success": true,
  "predicted_waiting_time_minutes": 78.41,
  "model_info": {
    "model_type": "LightGBM",
    "model_mae": 8.01,
    "model_r2": 0.9451,
    "confidence_interval_typical": "±6.79 min (50th percentile)",
    "confidence_interval_worst_case": "±19.95 min (95th percentile)"
  }
}
```

**Test Results:**
- ✅ Valid input: Prediction successful (78.41 min)
- ✅ Missing feature: Correctly rejected
- ✅ Target variable in input: Correctly rejected
- ✅ All validation checks passed

---

## 9. PREPROCESSING ARTIFACTS

### Saved Files
- `ml-services/preprocessed/preprocessor.pkl` - Fitted pipeline
- `ml-services/preprocessed/feature_names.json` - Feature configuration
- `ml-services/models/lightgbm_model.pkl` - Trained model

### Reproducibility
- Random seed: 42 (all results reproducible)
- Preprocessing: Fitted on training data only
- Data splits: Fixed and documented
- Feature order: Preserved in configuration

---

## 10. PERFORMANCE EVALUATION METRICS

### Metrics Definitions

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **MAE** | Mean Absolute Error | Average prediction error (typical mistake) |
| **RMSE** | Root Mean Squared Error | Penalizes large errors more heavily |
| **R²** | Coefficient of Determination | Variance explained by model (0-1) |
| **Median AE** | Median Absolute Error | 50th percentile error (typical case) |
| **P95 AE** | 95th Percentile Absolute Error | Worst 5% of predictions |

### LightGBM Performance Summary
- **Typical Prediction Error:** ±6.79 min (50th percentile)
  - Meaning: 50% of predictions within ±6.79 min of actual
  - Example: For 75 min actual, prediction likely 68-82 min

- **Worst-Case Error:** ±19.95 min (95th percentile)
  - Meaning: 95% of predictions within ±19.95 min of actual
  - Example: For 75 min actual, worst 5% might be 55-95 min

- **Mean Error:** -0.08 min (negligible bias)
  - Meaning: Model neither systematically over nor under-predicts

---

## 11. LIMITATIONS & DISCLAIMERS

### ⚠️ Synthetic Data Only
- Dataset is synthetically generated using predefined rules
- **NOT derived from real hospital operations**
- **NO clinical validation or regulatory approval**
- Patterns may not reflect real-world complexity

### ⚠️ Limited Temporal Coverage
- Single year of data (2025)
- No multi-year seasonal trends
- Real deployment would require 2+ years of history

### ⚠️ Distribution Shift Risk
- 7.9% mean difference between train and test
- Larger shifts possible in real data (seasonal, events, procedure changes)
- Requires monitoring and periodic retraining

### ⚠️ Concept Drift Not Evaluated
- Model assumes stable relationships over time
- Real hospitals have:
  - Equipment failures and maintenance (change wait patterns)
  - Staffing changes (new doctors, resignations)
  - Procedure modifications (new treatments)
  - Emergencies and mass events (disruption)
- Current model does NOT account for these

### ⚠️ No Fairness Analysis
- No evaluation of error rates across demographics
- No bias audit (gender, age, priority level effects)
- Not recommended for real clinical use without fairness review

### ⚠️ Training/Test Set Integrity
- Test set never used for hyperparameter tuning
- Test set never used for feature selection
- Random state fixed (reproducible, not randomized)

---

## 12. USE CASES & DEPLOYMENT CONTEXT

### Intended Use
✅ Academic research and final-year project demonstration  
✅ Prototype development and proof-of-concept  
✅ Machine learning pipeline architecture reference  
✅ Baseline performance benchmarking  

### NOT Intended For
❌ Real-time hospital queue management  
❌ Clinical decision-making  
❌ Patient-facing wait time displays (without clinical validation)  
❌ Regulatory compliance (healthcare compliance requirements not met)  
❌ Production deployment without extensive testing  

### Operational Deployment (If Considered)
**Critical Requirements Before Deployment:**
1. Real hospital data validation (replace synthetic data)
2. Clinical expert review and approval
3. Fairness and bias audit (demographic analysis)
4. Regulatory compliance assessment (HIPAA, medical device regulations)
5. Monitoring and retraining pipeline
6. User acceptance testing with hospital staff
7. Confidence interval communication strategy

---

## 13. REMAINING WORK

### Completed ✅
- [x] Data exploration and preprocessing
- [x] Baseline model training (4 models)
- [x] Feature importance analysis
- [x] Temporal validation
- [x] Model selection
- [x] Prediction module development
- [x] Module testing

### Next Phases (If Project Continues)
- [ ] **Phase 3:** Hyperparameter tuning (5-15% improvement expected)
- [ ] **Phase 4:** Ensemble methods and model stacking
- [ ] **Phase 5:** FastAPI REST service
- [ ] **Phase 6:** MERN frontend/backend integration
- [ ] **Phase 7:** Production monitoring and retraining pipeline
- [ ] **Phase 8:** Clinical validation (real hospital data)

### Not Included (Out of Scope)
- Real-time Socket.io integration
- Database persistence (MongoDB)
- User authentication and roles
- Patient privacy compliance (HIPAA)
- Clinical validation
- Regulatory approval

---

## 14. FILES & ARTIFACTS

### Source Code
- `src/predict.py` - Prediction module (19 features → waiting time)
- `src/save_preprocessor.py` - One-time preprocessing pipeline creation
- `src/train_baseline_models.py` - Baseline training script (Phase 1)
- `src/preprocessing_pipeline.py` - Original preprocessing script
- `src/phase1_interpretability.py` - Feature importance extraction
- `src/temporal_validation.py` - Temporal validation pipeline

### Models & Data
- `models/lightgbm_model.pkl` - Selected model (37 features → prediction)
- `models/xgboost_model.pkl` - Alternative model
- `models/random_forest_model.pkl` - Fallback model
- `models/linear_regression_model.pkl` - Baseline model
- `preprocessed/preprocessor.pkl` - Fitted preprocessing pipeline
- `preprocessed/feature_names.json` - Feature configuration
- `data/raw/synthetic_patient_queue_dataset.csv` - Raw dataset (20k records)

### Reports & Analysis
- `reports/model_comparison.csv` - Baseline metrics
- `reports/temporal_model_comparison.csv` - Temporal validation metrics
- `reports/temporal_validation_analysis.md` - Detailed temporal analysis
- `reports/BASELINE_EVALUATION_ANALYSIS.md` - Baseline evaluation
- `reports/TRAINING_COMPLETION_SUMMARY.md` - Training summary
- `reports/PREPROCESSING_CONFIGURATION_REPORT.json` - Preprocessing config
- `reports/feature_importance_xgboost.csv` - XGBoost features
- `reports/feature_importance_lightgbm.csv` - LightGBM features

### Visualizations
- `reports/temporal_actual_vs_predicted_all_models.png`
- `reports/temporal_error_distribution_all_models.png`
- `reports/temporal_mae_rmse_comparison.png`
- `reports/temporal_r2_comparison.png`
- `reports/actual_vs_predicted_all_models.png` (baseline)
- `reports/error_distribution_all_models.png` (baseline)

---

## 15. CONCLUSION

### Summary
Successfully developed and validated a machine learning model to predict patient waiting times using synthetic data. LightGBM selected as the production model with 8.01 min MAE and 0.9451 R² on temporal validation. Prediction module operational with input validation and error handling.

### Key Achievements
✅ **Model Performance:** 94% variance explained, ±7 min typical error  
✅ **Temporal Robustness:** Consistent performance across time splits  
✅ **Feature Engineering:** 19 carefully selected features, no leakage  
✅ **Prediction Module:** Functional, tested, validated  
✅ **Code Quality:** Modular, documented, reproducible  

### Confidence Level
🟢 **Research Prototype:** Suitable for academic demonstration  
🟡 **Proof-of-Concept:** Ready for small-scale testing  
🔴 **Production Deployment:** NOT RECOMMENDED without real data and clinical validation  

### Recommendation
Model is ready for academic presentation and proof-of-concept demonstrations. For real clinical use, extensive additional work required including real hospital data, fairness audits, compliance review, and regulatory approval.

---

**Report Prepared:** October 12, 2026  
**Data Type:** Synthetic (Research Use Only)  
**Clinical Validation:** Not Performed  
**Disclaimer:** This is a research prototype using synthetic data. No real-world hospital validation. Not suitable for clinical decision-making without extensive additional validation.

