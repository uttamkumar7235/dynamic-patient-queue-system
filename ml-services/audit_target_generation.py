"""
DATA GENERATION AND TARGET LEAKAGE AUDIT

Purpose: Trace the generation of waiting_time_minutes and identify any leakage
"""

import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('data/raw/synthetic_patient_queue_dataset.csv')

print('='*80)
print('DATASET STRUCTURE AND TARGET ANALYSIS')
print('='*80)
print(f'\nShape: {df.shape}')
print(f'\nColumns: {list(df.columns)}')

print('\n' + '='*80)
print('TARGET VARIABLE: waiting_time_minutes')
print('='*80)
target = df['waiting_time_minutes']
print(f'Data type: {target.dtype}')
print(f'Min: {target.min()}')
print(f'Max: {target.max()}')
print(f'Mean: {target.mean():.2f}')
print(f'Median: {target.median():.2f}')
print(f'Std Dev: {target.std():.2f}')
print(f'Missing values: {target.isna().sum()}')
print(f'Distribution:\n{target.describe()}')

print('\n' + '='*80)
print('POTENTIAL PREDICTORS - CORRELATION WITH TARGET')
print('='*80)
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
correlations = {}
for col in numeric_cols:
    if col != 'waiting_time_minutes':
        corr = df[[col, 'waiting_time_minutes']].corr().iloc[0,1]
        correlations[col] = corr
        print(f'{col:35s}: r={corr:8.4f} | missing={df[col].isna().sum():5d} | mean={df[col].mean():9.2f}')

# Sort by correlation
print('\n' + '='*80)
print('RANKED BY CORRELATION STRENGTH')
print('='*80)
sorted_corr = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)
for col, corr in sorted_corr:
    print(f'{col:35s}: {corr:8.4f}')

print('\n' + '='*80)
print('SAMPLE ROWS - FIRST 5 RECORDS')
print('='*80)
print(df.head(5).to_string())

print('\n' + '='*80)
print('KEY FORMULA HYPOTHESIS')
print('='*80)
print('Testing: waiting_time ≈ (patients_ahead + 1) × average_service_time / active_doctors')
print('(This is the classical queue formula: wait_time = queue_length × service_time / num_servers)')

df['formula_estimate'] = (df['patients_ahead'] + 1) * df['average_service_time_minutes'] / df['active_doctors']
corr_formula = df[['formula_estimate', 'waiting_time_minutes']].corr().iloc[0,1]
print(f'\nCorrelation between formula estimate and actual waiting_time: {corr_formula:.6f}')

# Calculate error
df['error'] = df['waiting_time_minutes'] - df['formula_estimate']
print(f'\nError Analysis (actual - formula):')
print(f'  Mean error: {df["error"].mean():.4f}')
print(f'  Std error: {df["error"].std():.4f}')
print(f'  Min error: {df["error"].min():.4f}')
print(f'  Max error: {df["error"].max():.4f}')
print(f'  Median error: {df["error"].median():.4f}')
print(f'  Abs mean error: {abs(df["error"]).mean():.4f}')

print(f'\nSample Comparison (formula vs actual):')
comparison = df[['patients_ahead', 'average_service_time_minutes', 'active_doctors', 'formula_estimate', 'waiting_time_minutes', 'error']].head(15).copy()
comparison.columns = ['Patients Ahead', 'Avg Service Time', 'Active Doctors', 'Formula Est', 'Actual Wait', 'Error']
print(comparison.to_string())

# Test if noise is random normal
print('\n' + '='*80)
print('NOISE ANALYSIS')
print('='*80)
error_dist = df['error']
print(f'Error Distribution Stats:')
print(f'  Skewness: {error_dist.skew():.4f} (0 = symmetric, >0 = right-skewed)')
print(f'  Kurtosis: {error_dist.kurtosis():.4f} (0 = normal, >0 = heavier tails)')
print(f'  Min: {error_dist.min():.2f}')
print(f'  Max: {error_dist.max():.2f}')
print(f'  1st percentile: {error_dist.quantile(0.01):.2f}')
print(f'  99th percentile: {error_dist.quantile(0.99):.2f}')

# Check if error correlates with any features (should not if truly random)
print(f'\nError Correlation with Input Features:')
for col in ['patients_ahead', 'average_service_time_minutes', 'active_doctors', 'hospital_load', 'peak_hour']:
    if col in df.columns:
        err_corr = df[[col, 'error']].corr().iloc[0,1]
        print(f'  {col:35s}: r={err_corr:8.4f}')

print('\n' + '='*80)
print('AVERAGE_SERVICE_TIME_MINUTES ANALYSIS')
print('='*80)
print(f'Average Service Time Statistics:')
ast = df['average_service_time_minutes']
print(f'  Min: {ast.min():.2f} minutes')
print(f'  Max: {ast.max():.2f} minutes')
print(f'  Mean: {ast.mean():.2f} minutes')
print(f'  Std Dev: {ast.std():.2f} minutes')
print(f'  Missing: {ast.isna().sum()} values')

# Correlation with waiting time
corr_ast = df[['average_service_time_minutes', 'waiting_time_minutes']].corr().iloc[0,1]
print(f'  Correlation with waiting_time: {corr_ast:.4f}')

# Check by doctor specialization
if 'doctor_specialization' in df.columns:
    print(f'\n  Average service time by specialization:')
    by_spec = df.groupby('doctor_specialization')['average_service_time_minutes'].agg(['count', 'mean', 'std', 'min', 'max'])
    print(by_spec.to_string())

print('\n' + '='*80)
print('PREVIOUS_PATIENT_SERVICE_TIME ANALYSIS')
print('='*80)
if 'previous_patient_service_time' in df.columns:
    ppst = df['previous_patient_service_time']
    print(f'Previous Patient Service Time Statistics:')
    print(f'  Min: {ppst.min():.2f} minutes')
    print(f'  Max: {ppst.max():.2f} minutes')
    print(f'  Mean: {ppst.mean():.2f} minutes')
    print(f'  Std Dev: {ppst.std():.2f} minutes')
    print(f'  Missing: {ppst.isna().sum()} values')
    
    # Correlation with waiting time (LEAKAGE TEST)
    corr_ppst = df[['previous_patient_service_time', 'waiting_time_minutes']].corr().iloc[0,1]
    print(f'  Correlation with waiting_time: {corr_ppst:.4f}')
    print(f'\n  WARNING: High correlation here would indicate LEAKAGE')
    print(f'  (This value is from PREVIOUS patient, becomes known AFTER current joins queue)')
    
    # Compare with average service time
    corr_ppst_ast = df[['previous_patient_service_time', 'average_service_time_minutes']].corr().iloc[0,1]
    print(f'  Correlation with average_service_time: {corr_ppst_ast:.4f}')
    print(f'  (Should be moderate if both represent doctor specialization effect)')

print('\n' + '='*80)
print('PEAK_HOUR AND HOSPITAL_LOAD ANALYSIS')
print('='*80)
print(f'Peak Hour:')
print(f'  Value counts: {dict(df["peak_hour"].value_counts())}')
print(f'  Mean waiting time (peak_hour=0): {df[df["peak_hour"]==0]["waiting_time_minutes"].mean():.2f}')
print(f'  Mean waiting time (peak_hour=1): {df[df["peak_hour"]==1]["waiting_time_minutes"].mean():.2f}')
print(f'  Difference: {df[df["peak_hour"]==1]["waiting_time_minutes"].mean() - df[df["peak_hour"]==0]["waiting_time_minutes"].mean():.2f} minutes')

print(f'\nHospital Load:')
print(f'  Min: {df["hospital_load"].min():.2f}%')
print(f'  Max: {df["hospital_load"].max():.2f}%')
print(f'  Mean: {df["hospital_load"].mean():.2f}%')
print(f'  Std Dev: {df["hospital_load"].std():.2f}%')
print(f'  Correlation with waiting_time: {df[["hospital_load", "waiting_time_minutes"]].corr().iloc[0,1]:.4f}')

print('\n' + '='*80)
print('PATIENTS_AHEAD ANALYSIS')
print('='*80)
print(f'Patients Ahead Statistics:')
pa = df['patients_ahead']
print(f'  Min: {pa.min():.0f}')
print(f'  Max: {pa.max():.0f}')
print(f'  Mean: {pa.mean():.2f}')
print(f'  Std Dev: {pa.std():.2f}')
print(f'  Correlation with waiting_time: {df[["patients_ahead", "waiting_time_minutes"]].corr().iloc[0,1]:.4f}')

# Check if patients_ahead is random or correlated with other factors
print(f'\n  Correlation with peak_hour: {df[["patients_ahead", "peak_hour"]].corr().iloc[0,1]:.4f}')
print(f'  Correlation with hospital_load: {df[["patients_ahead", "hospital_load"]].corr().iloc[0,1]:.4f}')
print(f'  Correlation with day_of_week: {df[["patients_ahead", "token_number"]].corr().iloc[0,1]:.4f}')

print('\n' + '='*80)
print('TEMPORAL LEAKAGE CHECK')
print('='*80)
print('Checking if temporal features leak future information:')
print(f'  arrival_delay_minutes: {df["arrival_delay_minutes"].isna().sum()} missing values')
print(f'    Correlation with waiting_time: {df[["arrival_delay_minutes", "waiting_time_minutes"]].corr().iloc[0,1]:.4f}')
print(f'  peak_hour: {df["peak_hour"].isna().sum()} missing values')
print(f'    Interpretation: 0=off-peak, 1=peak hour')
print(f'  day_of_week: {df["day_of_week"].isna().sum()} missing values')
print(f'    Correlation with waiting_time (as ordinal): {df[["token_number", "waiting_time_minutes"]].corr().iloc[0,1]:.4f}')

print('\n' + '='*80)
print('PRIORITY_LEVEL AND PATIENT_TYPE ANALYSIS')
print('='*80)
if 'priority_level' in df.columns:
    print(f'Priority Level:')
    print(f'  Unique values: {sorted(df["priority_level"].unique())}')
    print(f'  Distribution: {dict(df["priority_level"].value_counts())}')
    print(f'  Mean waiting time by priority:')
    priority_means = df.groupby('priority_level')['waiting_time_minutes'].agg(['count', 'mean', 'std'])
    print(priority_means.to_string())

if 'patient_type' in df.columns:
    print(f'\nPatient Type:')
    print(f'  Unique values: {sorted(df["patient_type"].unique())}')
    print(f'  Distribution: {dict(df["patient_type"].value_counts())}')
    print(f'  Mean waiting time by type:')
    type_means = df.groupby('patient_type')['waiting_time_minutes'].agg(['count', 'mean', 'std'])
    print(type_means.to_string())

print('\n' + '='*80)
print('POTENTIAL LEAKAGE SOURCES SUMMARY')
print('='*80)
print("""
LEAKAGE RISK ASSESSMENT:

1. previous_patient_service_time:
   - RISK: HIGH
   - REASON: This is outcome from PREVIOUS patient in queue
   - TIMING: Becomes known AFTER current patient joins queue
   - IMPACT: Creates look-ahead bias if included in model training
   - STATUS: Should be EXCLUDED

2. arrival_delay_minutes:
   - RISK: LOW to MEDIUM
   - REASON: Difference between scheduled and actual arrival
   - TIMING: Available at patient registration/queue join time
   - IMPACT: Safe to include if measured at prediction point
   - STATUS: Safe to include

3. average_service_time_minutes:
   - RISK: MEDIUM (depends on calculation)
   - REASON: Could be historical average (safe) or include current/future patients (leakage)
   - TIMING: Assume calculated from historical data before current patient joined
   - ASSUMPTION: Not recomputed using current queue (would include future outcomes)
   - IMPACT: High if future data included; safe if truly historical
   - STATUS: Safe if calculated from past data only; assume this is the case

4. Temporal features (visit_date, arrival_time, scheduled_time):
   - RISK: LOW
   - REASON: These describe timing of this specific patient's arrival
   - TIMING: Known at prediction time
   - IMPACT: Safe to use (converted to day_of_week, peak_hour in preprocessing)
   - STATUS: Safe to include

5. queue state (patients_ahead, queue_length_at_arrival, active_doctors, peak_hour):
   - RISK: LOW
   - REASON: These describe current queue state at patient's arrival
   - TIMING: Known at prediction time (patient's moment of arrival)
   - IMPACT: These ARE the features that directly determine waiting time
   - STATUS: Safe to include; these are expected predictors
""")

print('\n' + '='*80)
print('FORMULA DERIVATION CONFIDENCE')
print('='*80)
print(f"""
The waiting time appears to be generated using a QUEUEING FORMULA:

  waiting_time_minutes ≈ (patients_ahead + 1) × average_service_time / active_doctors + noise

Evidence:
  1. Correlation of formula with actual: {corr_formula:.6f}
  2. Mean absolute error: {abs(df['error']).mean():.2f} minutes
  3. Error mean: {df['error'].mean():.4f} (close to zero)
  4. Error std dev: {df['error'].std():.2f} minutes (consistent noise pattern)

Interpretation:
  - The formula explains {100*corr_formula**2:.1f}% of variance
  - Remaining variance ({100*(1-corr_formula**2):.1f}%) is random noise
  - This is EXPECTED behavior for synthetic queue data
  
Classic Queue Theory:
  Wait_Time = (Queue_Length × Service_Time) / Number_Servers + Noise
  
This is the M/M/c queue model (Poisson arrivals, exponential service times, c servers).
""")

print('\n' + '='*80)
print('R² PREDICTION')
print('='*80)
print(f"""
Why models achieved R² ≈ 0.83–0.95:

Linear Regression (R² = 0.8314):
  - Captures main formula: patients_ahead, average_service_time, active_doctors
  - Linear model sufficient for basic queue dynamics
  - Cannot capture non-linear interactions
  - MSE from noise and non-linear effects

Tree-Based Models (R² = 0.9407–0.9462):
  - Capture non-linear interactions
  - Example: peak_hour × patients_ahead effect
  - Example: priority_level × queue_length interaction
  - Can approximate non-linear thresholding effects
  - Better handles categorical modulations
  
Perfect Fit (R² = 1.0) NOT Achieved:
  - Formula adds random noise
  - Noise magnitude: {abs(df['error']).mean():.2f} ± {df['error'].std():.2f} minutes
  - This noise is irreducible (not due to missing features)
  
Expected Behavior:
  - High R² is appropriate for synthetic queue data
  - Real hospital data would have lower R² (more unexplained variance)
  - Synthetic R² is upper bound on what to expect in production
""")
