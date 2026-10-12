"""
ML Model Training and Baseline Comparison

Purpose:
- Load preprocessed train/test data
- Train multiple regression models
- Evaluate on held-out test set
- Compare baseline model performance
- Generate evaluation reports and visualizations

Models:
1. Linear Regression (baseline)
2. Random Forest Regressor
3. XGBoost Regressor
4. LightGBM Regressor

Metrics:
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² Score
- Median Absolute Error
- 95th Percentile Absolute Error

Dataset: Synthetic patient queue data
Target: waiting_time_minutes
Training records: 16,000
Test records: 4,000 (held-out, never used for tuning)
Input features: 37 (after encoding)

IMPORTANT:
- Test set is preserved and used ONLY for final evaluation
- No hyperparameter tuning on test set
- This is baseline model comparison; extensive tuning deferred
- Dataset is synthetic; no clinical claims
"""

import numpy as np
import pandas as pd
import time
import json
import joblib
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================================
# SETUP
# ============================================================================

ROOT = Path(__file__).resolve().parents[1]
PREPROCESSED_DIR = ROOT / 'preprocessed'
MODELS_DIR = ROOT / 'models'
REPORTS_DIR = ROOT / 'reports'

MODELS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

RANDOM_STATE = 42

print("=" * 80)
print("LOADING PREPROCESSED DATA")
print("=" * 80)

# Load preprocessed arrays
X_train = np.load(PREPROCESSED_DIR / 'X_train_transformed.npy')
X_test = np.load(PREPROCESSED_DIR / 'X_test_transformed.npy')
y_train = np.load(PREPROCESSED_DIR / 'y_train.npy')
y_test = np.load(PREPROCESSED_DIR / 'y_test.npy')

print(f"\nData loaded successfully:")
print(f"  X_train shape: {X_train.shape}")
print(f"  X_test shape: {X_test.shape}")
print(f"  y_train shape: {y_train.shape}")
print(f"  y_test shape: {y_test.shape}")

print(f"\nTarget variable statistics (train):")
print(f"  Mean: {y_train.mean():.2f} minutes")
print(f"  Median: {np.median(y_train):.2f} minutes")
print(f"  Std Dev: {y_train.std():.2f} minutes")
print(f"  Min: {y_train.min():.0f}, Max: {y_train.max():.0f}")

print(f"\nTarget variable statistics (test):")
print(f"  Mean: {y_test.mean():.2f} minutes")
print(f"  Median: {np.median(y_test):.2f} minutes")
print(f"  Std Dev: {y_test.std():.2f} minutes")
print(f"  Min: {y_test.min():.0f}, Max: {y_test.max():.0f}")

# ============================================================================
# DEFINE MODELS WITH BASELINE CONFIGURATIONS
# ============================================================================

print("\n" + "=" * 80)
print("DEFINING MODELS")
print("=" * 80)

models = {
    'Linear Regression': {
        'model': LinearRegression(),
        'params': {
            'fit_intercept': True,
            'copy_X': True
        },
        'type': 'baseline'
    },
    'Random Forest': {
        'model': RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=RANDOM_STATE,
            n_jobs=-1,
            verbose=0
        ),
        'params': {
            'n_estimators': 100,
            'max_depth': 20,
            'min_samples_split': 5,
            'min_samples_leaf': 2,
            'random_state': RANDOM_STATE
        },
        'type': 'tree-based'
    },
    'XGBoost': {
        'model': XGBRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            verbosity=0,
            objective='reg:squarederror'
        ),
        'params': {
            'n_estimators': 100,
            'max_depth': 7,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': RANDOM_STATE,
            'objective': 'reg:squarederror'
        },
        'type': 'tree-based'
    },
    'LightGBM': {
        'model': LGBMRegressor(
            n_estimators=100,
            max_depth=7,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=RANDOM_STATE,
            verbosity=-1,
            objective='regression'
        ),
        'params': {
            'n_estimators': 100,
            'max_depth': 7,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': RANDOM_STATE,
            'objective': 'regression'
        },
        'type': 'tree-based'
    }
}

print("\nModels defined:")
for name, config in models.items():
    print(f"  - {name}: {config['type']}")
    if 'n_estimators' in config['params']:
        print(f"      n_estimators={config['params']['n_estimators']}, max_depth={config['params']['max_depth']}")

# ============================================================================
# TRAIN AND EVALUATE MODELS
# ============================================================================

print("\n" + "=" * 80)
print("TRAINING MODELS")
print("=" * 80)

results = {
    'model_name': [],
    'model_type': [],
    'mae': [],
    'rmse': [],
    'r2': [],
    'median_ae': [],
    'p95_ae': [],
    'training_time_sec': [],
    'prediction_time_sec': [],
    'n_estimators': [],
    'max_depth': []
}

trained_models = {}
predictions_data = {}

for model_name, config in models.items():
    print(f"\nTraining {model_name}...")
    
    # Train
    start_train = time.time()
    config['model'].fit(X_train, y_train)
    train_time = time.time() - start_train
    
    # Predict on test set
    start_pred = time.time()
    y_pred = config['model'].predict(X_test)
    pred_time = time.time() - start_pred
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    # Calculate additional metrics
    absolute_errors = np.abs(y_test - y_pred)
    median_ae = np.median(absolute_errors)
    p95_ae = np.percentile(absolute_errors, 95)
    
    # Store results
    results['model_name'].append(model_name)
    results['model_type'].append(config['type'])
    results['mae'].append(round(mae, 2))
    results['rmse'].append(round(rmse, 2))
    results['r2'].append(round(r2, 4))
    results['median_ae'].append(round(median_ae, 2))
    results['p95_ae'].append(round(p95_ae, 2))
    results['training_time_sec'].append(round(train_time, 3))
    results['prediction_time_sec'].append(round(pred_time, 4))
    
    # Store model parameters
    if 'n_estimators' in config['params']:
        results['n_estimators'].append(config['params']['n_estimators'])
    else:
        results['n_estimators'].append(None)
    
    if 'max_depth' in config['params']:
        results['max_depth'].append(config['params']['max_depth'])
    else:
        results['max_depth'].append(None)
    
    # Save trained model
    model_path = MODELS_DIR / f'{model_name.lower().replace(" ", "_")}_model.pkl'
    joblib.dump(config['model'], model_path)
    print(f"  ✓ Model saved: {model_path.name}")
    
    # Store predictions for later analysis
    trained_models[model_name] = config['model']
    predictions_data[model_name] = {
        'y_pred': y_pred,
        'y_test': y_test,
        'absolute_errors': absolute_errors
    }
    
    print(f"  MAE: {mae:.2f} min | RMSE: {rmse:.2f} min | R²: {r2:.4f}")
    print(f"  Training time: {train_time:.3f}s | Prediction time: {pred_time:.4f}s")

# ============================================================================
# RESULTS SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("MODEL EVALUATION SUMMARY")
print("=" * 80)

results_df = pd.DataFrame(results)
print("\n" + results_df.to_string(index=False))

# Save to CSV
csv_path = REPORTS_DIR / 'model_comparison.csv'
results_df.to_csv(csv_path, index=False)
print(f"\n✓ Saved model comparison: {csv_path.name}")

# ============================================================================
# GENERATE DETAILED JSON REPORT
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING DETAILED EVALUATION REPORT")
print("=" * 80)

report = {
    'dataset_info': {
        'total_records': 20000,
        'train_records': 16000,
        'test_records': 4000,
        'train_test_split': '80/20',
        'input_features': 37,
        'target_variable': 'waiting_time_minutes',
        'random_state': RANDOM_STATE
    },
    'target_statistics': {
        'train': {
            'mean': float(y_train.mean()),
            'median': float(np.median(y_train)),
            'std': float(y_train.std()),
            'min': float(y_train.min()),
            'max': float(y_train.max())
        },
        'test': {
            'mean': float(y_test.mean()),
            'median': float(np.median(y_test)),
            'std': float(y_test.std()),
            'min': float(y_test.min()),
            'max': float(y_test.max())
        }
    },
    'model_evaluations': {}
}

for idx, model_name in enumerate(results['model_name']):
    report['model_evaluations'][model_name] = {
        'model_type': results['model_type'][idx],
        'parameters': {
            'n_estimators': results['n_estimators'][idx],
            'max_depth': results['max_depth'][idx]
        },
        'metrics': {
            'mae': results['mae'][idx],
            'rmse': results['rmse'][idx],
            'r2': results['r2'][idx],
            'median_absolute_error': results['median_ae'][idx],
            'p95_absolute_error': results['p95_ae'][idx]
        },
        'timing': {
            'training_time_seconds': results['training_time_sec'][idx],
            'prediction_time_seconds': results['prediction_time_sec'][idx]
        }
    }

report['interpretation'] = {
    'baseline_model': 'Linear Regression',
    'note': 'Baseline model comparison - no extensive hyperparameter tuning performed yet',
    'dataset_type': 'Synthetic patient queue data',
    'clinical_validation': 'NOT CLINICALLY VALIDATED - Results are from synthetic data only'
}

report_path = REPORTS_DIR / 'MODEL_EVALUATION_REPORT.json'
with open(report_path, 'w') as f:
    json.dump(report, f, indent=2)
print(f"✓ Saved evaluation report: {report_path.name}")

# ============================================================================
# SAVE PREDICTION RESULTS
# ============================================================================

print("\n" + "=" * 80)
print("SAVING PREDICTION RESULTS")
print("=" * 80)

# Create prediction results CSV (using first model as example for comprehensive view)
first_model_name = results['model_name'][0]
y_pred_first = predictions_data[first_model_name]['y_pred']
absolute_errors_first = predictions_data[first_model_name]['absolute_errors']

prediction_results = pd.DataFrame({
    'actual_waiting_time_minutes': y_test,
    'predicted_waiting_time_minutes': y_pred_first.round(2),
    'absolute_error_minutes': absolute_errors_first.round(2)
})

pred_csv_path = REPORTS_DIR / 'prediction_results.csv'
prediction_results.to_csv(pred_csv_path, index=False)
print(f"✓ Saved prediction results: {pred_csv_path.name}")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

print("\n" + "=" * 80)
print("GENERATING VISUALIZATIONS")
print("=" * 80)

# 1. Comparison plot: MAE and RMSE
fig, ax = plt.subplots(figsize=(12, 6))
x_pos = np.arange(len(results['model_name']))
width = 0.35

bars1 = ax.bar(x_pos - width/2, results['mae'], width, label='MAE', alpha=0.8)
bars2 = ax.bar(x_pos + width/2, results['rmse'], width, label='RMSE', alpha=0.8)

ax.set_xlabel('Model', fontsize=12, fontweight='bold')
ax.set_ylabel('Error (minutes)', fontsize=12, fontweight='bold')
ax.set_title('Model Comparison: MAE vs RMSE', fontsize=14, fontweight='bold')
ax.set_xticks(x_pos)
ax.set_xticklabels(results['model_name'], rotation=45, ha='right')
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'mae_rmse_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: mae_rmse_comparison.png")

# 2. R² comparison
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
bars = ax.bar(results['model_name'], results['r2'], color=colors, alpha=0.8)

ax.set_ylabel('R² Score', fontsize=12, fontweight='bold')
ax.set_title('Model Comparison: R² Score', fontsize=14, fontweight='bold')
ax.set_xticklabels(results['model_name'], rotation=45, ha='right')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim([0, 1])

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.4f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'r2_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: r2_comparison.png")

# 3. Actual vs Predicted plots for each model
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, model_name in enumerate(results['model_name']):
    y_pred = predictions_data[model_name]['y_pred']
    
    ax = axes[idx]
    ax.scatter(y_test, y_pred, alpha=0.5, s=20)
    
    # Add perfect prediction line
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    ax.set_xlabel('Actual Waiting Time (minutes)', fontsize=10)
    ax.set_ylabel('Predicted Waiting Time (minutes)', fontsize=10)
    ax.set_title(f'{model_name}\nR² = {results["r2"][idx]:.4f}, MAE = {results["mae"][idx]:.2f}', 
                 fontsize=11, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'actual_vs_predicted_all_models.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: actual_vs_predicted_all_models.png")

# 4. Residual plots for each model
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, model_name in enumerate(results['model_name']):
    y_pred = predictions_data[model_name]['y_pred']
    residuals = y_test - y_pred
    
    ax = axes[idx]
    ax.scatter(y_pred, residuals, alpha=0.5, s=20)
    ax.axhline(y=0, color='r', linestyle='--', lw=2)
    
    ax.set_xlabel('Predicted Waiting Time (minutes)', fontsize=10)
    ax.set_ylabel('Residuals (minutes)', fontsize=10)
    ax.set_title(f'{model_name} - Residuals\nMedian AE = {results["median_ae"][idx]:.2f}', 
                 fontsize=11, fontweight='bold')
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'residuals_all_models.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: residuals_all_models.png")

# 5. Error distribution for each model
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, model_name in enumerate(results['model_name']):
    absolute_errors = predictions_data[model_name]['absolute_errors']
    
    ax = axes[idx]
    ax.hist(absolute_errors, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
    ax.axvline(results['mae'][idx], color='r', linestyle='--', lw=2, label=f"MAE = {results['mae'][idx]:.2f}")
    ax.axvline(results['median_ae'][idx], color='g', linestyle='--', lw=2, label=f"Median = {results['median_ae'][idx]:.2f}")
    
    ax.set_xlabel('Absolute Error (minutes)', fontsize=10)
    ax.set_ylabel('Frequency', fontsize=10)
    ax.set_title(f'{model_name} - Error Distribution', fontsize=11, fontweight='bold')
    ax.legend()
    ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(REPORTS_DIR / 'error_distribution_all_models.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: error_distribution_all_models.png")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("BASELINE MODEL COMPARISON COMPLETE")
print("=" * 80)

print("\nMODEL PERFORMANCE SUMMARY:")
print("\n" + results_df[['model_name', 'mae', 'rmse', 'r2', 'median_ae', 'p95_ae']].to_string(index=False))

print("\nTRAINING AND PREDICTION TIME:")
print("\n" + results_df[['model_name', 'training_time_sec', 'prediction_time_sec']].to_string(index=False))

print("\n" + "=" * 80)
print("FILES SAVED")
print("=" * 80)
print(f"\nModels:")
for model_name in results['model_name']:
    print(f"  ✓ {model_name.lower().replace(' ', '_')}_model.pkl")

print(f"\nReports:")
print(f"  ✓ model_comparison.csv")
print(f"  ✓ MODEL_EVALUATION_REPORT.json")
print(f"  ✓ prediction_results.csv")

print(f"\nVisualizations:")
print(f"  ✓ mae_rmse_comparison.png")
print(f"  ✓ r2_comparison.png")
print(f"  ✓ actual_vs_predicted_all_models.png")
print(f"  ✓ residuals_all_models.png")
print(f"  ✓ error_distribution_all_models.png")

print("\n" + "=" * 80)
print("BASELINE MODEL TRAINING COMPLETE")
print("=" * 80)
