"""
TEMPORAL VALIDATION ANALYSIS
Chronological split based on visit_date

Purpose:
- Split dataset by temporal order (earlier dates = train, later dates = test)
- Refit preprocessing on training data only
- Evaluate 4 models on held-out temporal test set
- Compare with baseline random 80/20 split results

Key Requirements:
- No data leakage from test to train
- Preprocessing fit only on training data
- Use same feature set and exclusions as baseline
- Preserve existing feature selection rules
- Save results separately (never overwrite baseline)
- Compute: MAE, RMSE, R², Median AE, P95 AE
"""

import numpy as np
import pandas as pd
import json
import joblib
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, median_absolute_error

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'raw' / 'synthetic_patient_queue_dataset.csv'
REPORTS_DIR = ROOT / 'reports'
MODELS_DIR = ROOT / 'models'

RANDOM_STATE = 42

# Feature definitions (same as baseline preprocessing)
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

TARGET = 'waiting_time_minutes'

# ============================================================================
# STEP 1: LOAD AND SORT DATA BY VISIT_DATE
# ============================================================================

print("=" * 80)
print("TEMPORAL VALIDATION: CHRONOLOGICAL SPLIT")
print("=" * 80)

print("\n[1/6] Loading and sorting data by visit_date...")

df = pd.read_csv(DATA_PATH)
print(f"  ✓ Loaded dataset: {df.shape}")

# Convert visit_date to datetime and sort
df['visit_date'] = pd.to_datetime(df['visit_date'])
df_sorted = df.sort_values('visit_date').reset_index(drop=True)

print(f"  ✓ Date range: {df_sorted['visit_date'].min()} to {df_sorted['visit_date'].max()}")

# 80/20 temporal split
split_idx = int(len(df_sorted) * 0.8)
df_train = df_sorted.iloc[:split_idx].copy()
df_test = df_sorted.iloc[split_idx:].copy()

print(f"\n  Temporal Split (80/20):")
print(f"    Training:  {len(df_train)} records ({df_train['visit_date'].min()} to {df_train['visit_date'].max()})")
print(f"    Testing:   {len(df_test)} records ({df_test['visit_date'].min()} to {df_test['visit_date'].max()})")

# ============================================================================
# STEP 2: EXTRACT FEATURES AND TARGET
# ============================================================================

print("\n[2/6] Extracting features and target...")

# Extract X and y for train and test
X_train = df_train[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()
y_train = df_train[TARGET].copy()

X_test = df_test[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()
y_test = df_test[TARGET].copy()

print(f"  ✓ Training set: X {X_train.shape}, y {y_train.shape}")
print(f"  ✓ Testing set: X {X_test.shape}, y {y_test.shape}")

print(f"\n  Target Statistics (Training):")
print(f"    Mean: {y_train.mean():.2f}, Std: {y_train.std():.2f}")
print(f"    Min: {y_train.min():.2f}, Max: {y_train.max():.2f}")

print(f"\n  Target Statistics (Testing):")
print(f"    Mean: {y_test.mean():.2f}, Std: {y_test.std():.2f}")
print(f"    Min: {y_test.min():.2f}, Max: {y_test.max():.2f}")

# ============================================================================
# STEP 3: BUILD PREPROCESSING PIPELINE (FIT ON TRAINING ONLY)
# ============================================================================

print("\n[3/6] Building preprocessing pipeline (fitted on training data)...")

# Numerical: Impute median, no scaling for tree-based
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median'))
])

# Categorical: One-hot encoding
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Full preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, NUMERICAL_FEATURES),
        ('cat', categorical_transformer, CATEGORICAL_FEATURES)
    ]
)

# FIT PREPROCESSING ON TRAINING DATA ONLY (no leakage)
print("  ✓ Fitting preprocessor on training data...")
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

print(f"  ✓ Transformed shapes: train {X_train_transformed.shape}, test {X_test_transformed.shape}")

# ============================================================================
# STEP 4: TRAIN MODELS
# ============================================================================

print("\n[4/6] Training models on temporal training set...")

models = {}
predictions = {}

# Linear Regression
print("  - Linear Regression...")
lr_model = LinearRegression()
lr_model.fit(X_train_transformed, y_train)
models['Linear Regression'] = lr_model
predictions['Linear Regression'] = lr_model.predict(X_test_transformed)

# Random Forest
print("  - Random Forest...")
rf_model = RandomForestRegressor(n_estimators=100, max_depth=20, random_state=RANDOM_STATE, n_jobs=-1)
rf_model.fit(X_train_transformed, y_train)
models['Random Forest'] = rf_model
predictions['Random Forest'] = rf_model.predict(X_test_transformed)

# XGBoost
if HAS_XGB:
    print("  - XGBoost...")
    xgb_model = XGBRegressor(n_estimators=100, max_depth=7, learning_rate=0.1, random_state=RANDOM_STATE, verbosity=0)
    xgb_model.fit(X_train_transformed, y_train)
    models['XGBoost'] = xgb_model
    predictions['XGBoost'] = xgb_model.predict(X_test_transformed)
else:
    print("  ⚠ XGBoost not available")

# LightGBM
if HAS_LGBM:
    print("  - LightGBM...")
    lgb_model = LGBMRegressor(n_estimators=100, max_depth=7, learning_rate=0.1, random_state=RANDOM_STATE, verbosity=-1)
    lgb_model.fit(X_train_transformed, y_train)
    models['LightGBM'] = lgb_model
    predictions['LightGBM'] = lgb_model.predict(X_test_transformed)
else:
    print("  ⚠ LightGBM not available")

print(f"\n  ✓ Trained {len(models)} models")

# ============================================================================
# STEP 5: COMPUTE METRICS
# ============================================================================

print("\n[5/6] Computing evaluation metrics...")

metrics_list = []
y_test_values = y_test.values

for model_name in models.keys():
    y_pred = predictions[model_name]
    
    mae = mean_absolute_error(y_test_values, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test_values, y_pred))
    r2 = r2_score(y_test_values, y_pred)
    median_ae = median_absolute_error(y_test_values, y_pred)
    p95_ae = np.percentile(np.abs(y_test_values - y_pred), 95)
    
    metrics_list.append({
        'Model': model_name,
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'R²': round(r2, 4),
        'Median AE': round(median_ae, 2),
        'P95 AE': round(p95_ae, 2),
    })
    
    print(f"\n  {model_name}:")
    print(f"    MAE: {mae:.2f} min")
    print(f"    RMSE: {rmse:.2f} min")
    print(f"    R²: {r2:.4f}")
    print(f"    Median AE: {median_ae:.2f} min")
    print(f"    P95 AE: {p95_ae:.2f} min")

# Create comparison dataframe
metrics_df = pd.DataFrame(metrics_list)
print("\n  ✓ Metrics summary:")
print(metrics_df.to_string(index=False))

# Save metrics to CSV
metrics_csv = REPORTS_DIR / 'temporal_model_comparison.csv'
metrics_df.to_csv(metrics_csv, index=False)
print(f"\n  ✓ Saved to {metrics_csv.name}")

# ============================================================================
# STEP 6: SAVE DETAILED REPORT (JSON)
# ============================================================================

print("\n[6/6] Saving detailed temporal validation report...")

report = {
    'timestamp': datetime.now().isoformat(),
    'split_type': 'temporal_chronological',
    'date_range': {
        'min_date': str(df_sorted['visit_date'].min()),
        'max_date': str(df_sorted['visit_date'].max()),
    },
    'split_dates': {
        'train_end': str(df_train['visit_date'].max()),
        'test_start': str(df_test['visit_date'].min()),
    },
    'dataset': {
        'total_records': len(df_sorted),
        'train_records': len(df_train),
        'test_records': len(df_test),
        'train_test_split_pct': '80/20',
    },
    'input_features': {
        'numerical_count': len(NUMERICAL_FEATURES),
        'categorical_count': len(CATEGORICAL_FEATURES),
        'total_count': len(NUMERICAL_FEATURES) + len(CATEGORICAL_FEATURES),
    },
    'target_variable': TARGET,
    'target_statistics': {
        'train': {
            'mean': float(y_train.mean()),
            'std': float(y_train.std()),
            'median': float(y_train.median()),
            'min': float(y_train.min()),
            'max': float(y_train.max()),
        },
        'test': {
            'mean': float(y_test.mean()),
            'std': float(y_test.std()),
            'median': float(y_test.median()),
            'min': float(y_test.min()),
            'max': float(y_test.max()),
        },
    },
    'model_evaluations': {}
}

for model_name in models.keys():
    y_pred = predictions[model_name]
    abs_errors = np.abs(y_test_values - y_pred)
    
    report['model_evaluations'][model_name] = {
        'metrics': {
            'mae': float(mean_absolute_error(y_test_values, y_pred)),
            'rmse': float(np.sqrt(mean_squared_error(y_test_values, y_pred))),
            'r2': float(r2_score(y_test_values, y_pred)),
            'median_absolute_error': float(median_absolute_error(y_test_values, y_pred)),
            'p95_absolute_error': float(np.percentile(abs_errors, 95)),
            'p75_absolute_error': float(np.percentile(abs_errors, 75)),
            'p50_absolute_error': float(np.percentile(abs_errors, 50)),
            'p25_absolute_error': float(np.percentile(abs_errors, 25)),
        },
        'error_distribution': {
            'mean_error': float(np.mean(y_pred - y_test_values)),
            'std_error': float(np.std(y_pred - y_test_values)),
            'min_error': float(np.min(y_pred - y_test_values)),
            'max_error': float(np.max(y_pred - y_test_values)),
            'pct_over_prediction': float(np.mean(y_pred > y_test_values) * 100),
        },
    }

# Save JSON report
report_json = REPORTS_DIR / 'temporal_validation_report.json'
with open(report_json, 'w') as f:
    json.dump(report, f, indent=2)
print(f"  ✓ Saved {report_json.name}")

# ============================================================================
# STEP 7: CREATE VISUALIZATIONS
# ============================================================================

print("\n[7/6] Creating visualizations...")

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 5)

# 1. Actual vs Predicted (all models)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Temporal Validation: Actual vs Predicted Waiting Time', fontsize=16, fontweight='bold')

for idx, model_name in enumerate(list(models.keys())[:4]):
    ax = axes[idx // 2, idx % 2]
    y_pred = predictions[model_name]
    
    ax.scatter(y_test_values, y_pred, alpha=0.5, s=20)
    ax.plot([y_test_values.min(), y_test_values.max()],
            [y_test_values.min(), y_test_values.max()],
            'r--', lw=2, label='Perfect Prediction')
    
    mae = mean_absolute_error(y_test_values, y_pred)
    r2 = r2_score(y_test_values, y_pred)
    
    ax.set_xlabel('Actual Waiting Time (min)', fontsize=11)
    ax.set_ylabel('Predicted Waiting Time (min)', fontsize=11)
    ax.set_title(f'{model_name}\nMAE: {mae:.2f} min | R²: {r2:.4f}', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'temporal_actual_vs_predicted_all_models.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved temporal_actual_vs_predicted_all_models.png")

# 2. Error Distribution (all models)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Temporal Validation: Error Distribution by Model', fontsize=16, fontweight='bold')

for idx, model_name in enumerate(list(models.keys())[:4]):
    ax = axes[idx // 2, idx % 2]
    y_pred = predictions[model_name]
    errors = y_pred - y_test_values
    
    ax.hist(errors, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    ax.axvline(errors.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {errors.mean():.2f}')
    ax.axvline(np.median(errors), color='green', linestyle='--', linewidth=2, label=f'Median: {np.median(errors):.2f}')
    
    ax.set_xlabel('Prediction Error (min)', fontsize=11)
    ax.set_ylabel('Frequency', fontsize=11)
    ax.set_title(f'{model_name}\nStd: {errors.std():.2f} min', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'temporal_error_distribution_all_models.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved temporal_error_distribution_all_models.png")

# 3. MAE/RMSE Comparison
fig, ax = plt.subplots(figsize=(12, 6))
x_pos = np.arange(len(metrics_df))
width = 0.35

ax.bar(x_pos - width/2, metrics_df['MAE'], width, label='MAE', color='steelblue', edgecolor='black')
ax.bar(x_pos + width/2, metrics_df['RMSE'], width, label='RMSE', color='coral', edgecolor='black')

ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_ylabel('Error (minutes)', fontsize=12, fontweight='bold')
ax.set_title('Temporal Validation: MAE vs RMSE Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(metrics_df['Model'], rotation=0)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, v in enumerate(metrics_df['MAE']):
    ax.text(i - width/2, v + 0.3, f'{v:.2f}', ha='center', va='bottom', fontsize=10)
for i, v in enumerate(metrics_df['RMSE']):
    ax.text(i + width/2, v + 0.3, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'temporal_mae_rmse_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved temporal_mae_rmse_comparison.png")

# 4. R² Comparison
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(metrics_df)]
bars = ax.bar(metrics_df['Model'], metrics_df['R²'], color=colors, edgecolor='black', linewidth=1.5)

ax.set_ylabel('R² Score', fontsize=12, fontweight='bold')
ax.set_title('Temporal Validation: R² Score Comparison', fontsize=14, fontweight='bold')
ax.set_ylim([0, 1])
ax.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f'{height:.4f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(REPORTS_DIR / 'temporal_r2_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("  ✓ Saved temporal_r2_comparison.png")

print("\n" + "=" * 80)
print("✅ TEMPORAL VALIDATION COMPLETE")
print("=" * 80)
print(f"\nResults saved to:")
print(f"  - {metrics_csv.name}")
print(f"  - {report_json.name}")
print(f"  - temporal_actual_vs_predicted_all_models.png")
print(f"  - temporal_error_distribution_all_models.png")
print(f"  - temporal_mae_rmse_comparison.png")
print(f"  - temporal_r2_comparison.png")
