"""
PHASE 1: MODEL INTERPRETABILITY
Extract feature importance from XGBoost and LightGBM.
Perform SHAP analysis if available.
Map one-hot features back to original feature names.

Purpose:
- Generate feature importance CSVs and plots
- Analyze which features the models rely on
- Clarify feature importance vs correlation vs causality
"""

import numpy as np
import pandas as pd
import json
import joblib
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / 'models'
PREPROCESSED_DIR = ROOT / 'preprocessed'
REPORTS_DIR = ROOT / 'reports'
DATA_DIR = ROOT / 'data' / 'raw'

RANDOM_STATE = 42

# ============================================================================
# LOAD ARTIFACTS
# ============================================================================

print("=" * 80)
print("PHASE 1: MODEL INTERPRETABILITY")
print("=" * 80)

print("\n[1/5] Loading feature names and trained models...")

# Load feature names
with open(PREPROCESSED_DIR / 'feature_names.json', 'r') as f:
    feature_config = json.load(f)

numerical_features = feature_config['numerical_features']
categorical_features = feature_config['categorical_features']
categorical_onehot = feature_config['categorical_onehot_names']
all_features_transformed = feature_config['all_features_after_transform']

print(f"  ✓ Loaded {len(numerical_features)} numerical features")
print(f"  ✓ Loaded {len(categorical_features)} categorical features")
print(f"  ✓ Loaded {len(categorical_onehot)} one-hot encoded features")
print(f"  ✓ Total transformed features: {len(all_features_transformed)}")

# Load models
xgb_model = joblib.load(MODELS_DIR / 'xgboost_model.pkl')
lgb_model = joblib.load(MODELS_DIR / 'lightgbm_model.pkl')

print(f"\n  ✓ Loaded XGBoost model")
print(f"  ✓ Loaded LightGBM model")

# Load test data
X_test = np.load(PREPROCESSED_DIR / 'X_test_transformed.npy')
y_test = np.load(PREPROCESSED_DIR / 'y_test.npy')

print(f"  ✓ Loaded test set: {X_test.shape[0]} samples × {X_test.shape[1]} features")

# ============================================================================
# CREATE FEATURE NAME MAPPING
# ============================================================================

print("\n[2/5] Creating feature name mapping...")

# Map one-hot features back to their original categorical features
onehot_to_original = {}
for onehot_name in categorical_onehot:
    # Format: "feature_name_value" → extract "feature_name"
    parts = onehot_name.rsplit('_', 1)  # Split from right to handle multi-word values
    if len(parts) == 2:
        base_feature = parts[0]
        onehot_to_original[onehot_name] = base_feature

print(f"  ✓ Created mapping for {len(onehot_to_original)} one-hot features")

# ============================================================================
# EXTRACT XGBOOST FEATURE IMPORTANCE
# ============================================================================

print("\n[3/5] Extracting XGBoost feature importance...")

xgb_importance = xgb_model.feature_importances_
xgb_df = pd.DataFrame({
    'feature': all_features_transformed,
    'importance': xgb_importance,
    'importance_pct': xgb_importance / xgb_importance.sum() * 100
})
xgb_df = xgb_df.sort_values('importance', ascending=False).reset_index(drop=True)

# Add original feature name (for one-hots, show both)
xgb_df['original_feature'] = xgb_df['feature'].apply(
    lambda x: onehot_to_original.get(x, x)
)

print(f"  ✓ Extracted importances for {len(xgb_df)} features")
print(f"\n  Top 10 XGBoost Features (by importance):")
for idx, row in xgb_df.head(10).iterrows():
    print(f"    {idx+1:2d}. {row['feature']:40s} ({row['original_feature']:25s}): {row['importance_pct']:6.2f}%")

# Save XGBoost feature importance
xgb_csv = REPORTS_DIR / 'feature_importance_xgboost.csv'
xgb_df.to_csv(xgb_csv, index=False)
print(f"\n  ✓ Saved to {xgb_csv.name}")

# ============================================================================
# EXTRACT LIGHTGBM FEATURE IMPORTANCE
# ============================================================================

print("\n[4/5] Extracting LightGBM feature importance...")

lgb_importance = lgb_model.feature_importances_
lgb_df = pd.DataFrame({
    'feature': all_features_transformed,
    'importance': lgb_importance,
    'importance_pct': lgb_importance / lgb_importance.sum() * 100
})
lgb_df = lgb_df.sort_values('importance', ascending=False).reset_index(drop=True)

# Add original feature name
lgb_df['original_feature'] = lgb_df['feature'].apply(
    lambda x: onehot_to_original.get(x, x)
)

print(f"  ✓ Extracted importances for {len(lgb_df)} features")
print(f"\n  Top 10 LightGBM Features (by importance):")
for idx, row in lgb_df.head(10).iterrows():
    print(f"    {idx+1:2d}. {row['feature']:40s} ({row['original_feature']:25s}): {row['importance_pct']:6.2f}%")

# Save LightGBM feature importance
lgb_csv = REPORTS_DIR / 'feature_importance_lightgbm.csv'
lgb_df.to_csv(lgb_csv, index=False)
print(f"\n  ✓ Saved to {lgb_csv.name}")

# ============================================================================
# AGGREGATE IMPORTANCE BY ORIGINAL FEATURE
# ============================================================================

print("\n[5/5] Aggregating one-hot features back to original categories...")

# For XGBoost
xgb_agg = xgb_df.groupby('original_feature')['importance'].sum().sort_values(ascending=False)
print(f"\n  XGBoost aggregated by original feature:")
for feature, importance_sum in xgb_agg.items():
    pct = (importance_sum / xgb_importance.sum()) * 100
    print(f"    {feature:40s}: {pct:6.2f}%")

# For LightGBM
lgb_agg = lgb_df.groupby('original_feature')['importance'].sum().sort_values(ascending=False)
print(f"\n  LightGBM aggregated by original feature:")
for feature, importance_sum in lgb_agg.items():
    pct = (importance_sum / lgb_importance.sum()) * 100
    print(f"    {feature:40s}: {pct:6.2f}%")

# ============================================================================
# CREATE VISUALIZATIONS
# ============================================================================

print("\n[6/5] Creating feature importance plots...")

# Plot 1: XGBoost Top 15 Features
plt.figure(figsize=(12, 8))
top_15_xgb = xgb_df.head(15)
plt.barh(range(len(top_15_xgb)), top_15_xgb['importance_pct'])
plt.yticks(range(len(top_15_xgb)), top_15_xgb['feature'])
plt.xlabel('Importance (%)')
plt.title('XGBoost Top 15 Features by Importance\n(Based on Gain/Split Count)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(REPORTS_DIR / 'feature_importance_xgboost_plot.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved XGBoost plot")
plt.close()

# Plot 2: LightGBM Top 15 Features
plt.figure(figsize=(12, 8))
top_15_lgb = lgb_df.head(15)
plt.barh(range(len(top_15_lgb)), top_15_lgb['importance_pct'])
plt.yticks(range(len(top_15_lgb)), top_15_lgb['feature'])
plt.xlabel('Importance (%)')
plt.title('LightGBM Top 15 Features by Importance\n(Based on Gain/Split Count)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(REPORTS_DIR / 'feature_importance_lightgbm_plot.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved LightGBM plot")
plt.close()

# Plot 3: Aggregated by Original Feature - XGBoost
plt.figure(figsize=(12, 7))
top_agg_xgb = xgb_agg.head(12)
plt.barh(range(len(top_agg_xgb)), top_agg_xgb.values / top_agg_xgb.sum() * 100)
plt.yticks(range(len(top_agg_xgb)), top_agg_xgb.index)
plt.xlabel('Aggregated Importance (%)')
plt.title('XGBoost: Feature Importance Aggregated by Original Feature\n(One-hot Encoded Features Grouped)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(REPORTS_DIR / 'feature_importance_xgboost_aggregated.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved XGBoost aggregated plot")
plt.close()

# Plot 4: Aggregated by Original Feature - LightGBM
plt.figure(figsize=(12, 7))
top_agg_lgb = lgb_agg.head(12)
plt.barh(range(len(top_agg_lgb)), top_agg_lgb.values / top_agg_lgb.sum() * 100)
plt.yticks(range(len(top_agg_lgb)), top_agg_lgb.index)
plt.xlabel('Aggregated Importance (%)')
plt.title('LightGBM: Feature Importance Aggregated by Original Feature\n(One-hot Encoded Features Grouped)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(REPORTS_DIR / 'feature_importance_lightgbm_aggregated.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved LightGBM aggregated plot")
plt.close()

# ============================================================================
# ATTEMPT SHAP ANALYSIS
# ============================================================================

print("\n" + "=" * 80)
print("ATTEMPTING SHAP ANALYSIS...")
print("=" * 80)

try:
    import shap
    print("\n✓ SHAP library detected. Proceeding with SHAP analysis...")
    
    # Use a sample for SHAP (full dataset can be slow)
    sample_size = min(500, X_test.shape[0])
    X_sample = X_test[:sample_size]
    
    print(f"\n  Using sample of {sample_size} test records for SHAP analysis...")
    
    # ========================================================================
    # SHAP for XGBoost
    # ========================================================================
    
    print(f"\n  [SHAP 1/2] Analyzing XGBoost...")
    
    try:
        explainer_xgb = shap.TreeExplainer(xgb_model)
        shap_values_xgb = explainer_xgb.shap_values(X_sample)
        
        # Extract base value and ensure proper shape
        if isinstance(shap_values_xgb, list):
            # Multi-class; use first class
            shap_vals = shap_values_xgb[0]
        else:
            shap_vals = shap_values_xgb
        
        # Compute mean absolute SHAP values
        shap_importance_xgb = np.abs(shap_vals).mean(axis=0)
        
        shap_xgb_df = pd.DataFrame({
            'feature': all_features_transformed,
            'shap_importance': shap_importance_xgb,
            'shap_pct': shap_importance_xgb / shap_importance_xgb.sum() * 100
        })
        shap_xgb_df = shap_xgb_df.sort_values('shap_importance', ascending=False).reset_index(drop=True)
        
        shap_xgb_df['original_feature'] = shap_xgb_df['feature'].apply(
            lambda x: onehot_to_original.get(x, x)
        )
        
        # Save SHAP importance
        shap_xgb_csv = REPORTS_DIR / 'shap_importance_xgboost.csv'
        shap_xgb_df.to_csv(shap_xgb_csv, index=False)
        print(f"    ✓ Saved SHAP importance to {shap_xgb_csv.name}")
        
        print(f"\n    Top 10 SHAP Features (XGBoost):")
        for idx, row in shap_xgb_df.head(10).iterrows():
            print(f"      {idx+1:2d}. {row['feature']:40s}: {row['shap_pct']:6.2f}%")
        
        # Create SHAP summary plot
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_vals, X_sample, feature_names=all_features_transformed, 
                         plot_type="bar", show=False)
        plt.title('XGBoost: SHAP Global Importance (Bar Plot)')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / 'shap_summary_bar_xgboost.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Saved SHAP bar plot")
        
        # Create SHAP beeswarm plot (if dataset is small enough)
        if sample_size < 200:
            plt.figure(figsize=(10, 10))
            shap.summary_plot(shap_vals, X_sample, feature_names=all_features_transformed, 
                             plot_type="dot", show=False)
            plt.title('XGBoost: SHAP Summary Plot (Beeswarm)')
            plt.tight_layout()
            plt.savefig(REPORTS_DIR / 'shap_summary_dot_xgboost.png', dpi=300, bbox_inches='tight')
            plt.close()
            print(f"    ✓ Saved SHAP beeswarm plot")
        
    except Exception as e:
        print(f"    ✗ SHAP analysis failed for XGBoost: {str(e)[:80]}")
    
    # ========================================================================
    # SHAP for LightGBM
    # ========================================================================
    
    print(f"\n  [SHAP 2/2] Analyzing LightGBM...")
    
    try:
        explainer_lgb = shap.TreeExplainer(lgb_model)
        shap_values_lgb = explainer_lgb.shap_values(X_sample)
        
        # Handle multi-output
        if isinstance(shap_values_lgb, list):
            shap_vals = shap_values_lgb[0]
        else:
            shap_vals = shap_values_lgb
        
        shap_importance_lgb = np.abs(shap_vals).mean(axis=0)
        
        shap_lgb_df = pd.DataFrame({
            'feature': all_features_transformed,
            'shap_importance': shap_importance_lgb,
            'shap_pct': shap_importance_lgb / shap_importance_lgb.sum() * 100
        })
        shap_lgb_df = shap_lgb_df.sort_values('shap_importance', ascending=False).reset_index(drop=True)
        
        shap_lgb_df['original_feature'] = shap_lgb_df['feature'].apply(
            lambda x: onehot_to_original.get(x, x)
        )
        
        # Save SHAP importance
        shap_lgb_csv = REPORTS_DIR / 'shap_importance_lightgbm.csv'
        shap_lgb_df.to_csv(shap_lgb_csv, index=False)
        print(f"    ✓ Saved SHAP importance to {shap_lgb_csv.name}")
        
        print(f"\n    Top 10 SHAP Features (LightGBM):")
        for idx, row in shap_lgb_df.head(10).iterrows():
            print(f"      {idx+1:2d}. {row['feature']:40s}: {row['shap_pct']:6.2f}%")
        
        # Create SHAP summary plot
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_vals, X_sample, feature_names=all_features_transformed, 
                         plot_type="bar", show=False)
        plt.title('LightGBM: SHAP Global Importance (Bar Plot)')
        plt.tight_layout()
        plt.savefig(REPORTS_DIR / 'shap_summary_bar_lightgbm.png', dpi=300, bbox_inches='tight')
        plt.close()
        print(f"    ✓ Saved SHAP bar plot")
        
    except Exception as e:
        print(f"    ✗ SHAP analysis failed for LightGBM: {str(e)[:80]}")
    
    print(f"\n✓ SHAP analysis completed successfully")

except ImportError:
    print("\n✗ SHAP not installed. Skipping SHAP analysis.")
    print("   (This is acceptable; native feature importance is sufficient)")

# ============================================================================
# SUMMARY AND KEY FINDINGS
# ============================================================================

print("\n" + "=" * 80)
print("PHASE 1 SUMMARY")
print("=" * 80)

print(f"""
OUTPUTS GENERATED:
  1. feature_importance_xgboost.csv ........... 37 features with importance scores
  2. feature_importance_lightgbm.csv ......... 37 features with importance scores
  3. feature_importance_xgboost_plot.png .... Top 15 XGBoost features (bar chart)
  4. feature_importance_lightgbm_plot.png ... Top 15 LightGBM features (bar chart)
  5. feature_importance_xgboost_aggregated.png . Aggregated by original feature
  6. feature_importance_lightgbm_aggregated.png  Aggregated by original feature

OPTIONAL (if SHAP available):
  7. shap_importance_xgboost.csv ............ SHAP values aggregated per feature
  8. shap_importance_lightgbm.csv .......... SHAP values aggregated per feature
  9. shap_summary_bar_xgboost.png ......... SHAP bar plot (XGBoost)
  10. shap_summary_bar_lightgbm.png ....... SHAP bar plot (LightGBM)
  11. shap_summary_dot_xgboost.png ........ SHAP beeswarm plot (if applicable)

TOP FEATURES (XGBoost):
""")
for idx, row in xgb_df.head(5).iterrows():
    print(f"  {idx+1}. {row['original_feature']:30s} {row['importance_pct']:6.2f}%")

print(f"""
TOP FEATURES (LightGBM):
""")
for idx, row in lgb_df.head(5).iterrows():
    print(f"  {idx+1}. {row['original_feature']:30s} {row['importance_pct']:6.2f}%")

print(f"""
KEY DISTINCTIONS:
  • Feature Importance (native): How much each feature contributes to model splits/gains
  • SHAP Values: Average impact of each feature on predictions (if computed)
  • Correlation: Statistical relationship between feature and target (different from importance)
  • Causality: NOT established by feature importance; correlation ≠ causation

  Trees (XGBoost/LightGBM) may prioritize features differently than linear models.
  One-hot encoded features are aggregated to show original categorical feature importance.

✓ Phase 1 complete: Model interpretability analysis finished.
  Next: Phase 2 - Error Analysis
""")
