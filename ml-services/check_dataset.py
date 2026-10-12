#!/usr/bin/env python3
"""Quick check of dataset structure and visit_date format."""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path('data/raw/synthetic_patient_queue_dataset.csv')

print("="*80)
print("DATASET STRUCTURE CHECK")
print("="*80)

df = pd.read_csv(DATA_PATH)

print(f"\nDataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")

print("\n--- VISIT_DATE ANALYSIS ---")
print(f"Column type: {df['visit_date'].dtype}")
print(f"\nFirst 5 values:")
print(df['visit_date'].head())

# Parse dates
df['visit_date'] = pd.to_datetime(df['visit_date'])

print(f"\nDate range:")
print(f"  Min: {df['visit_date'].min()}")
print(f"  Max: {df['visit_date'].max()}")
print(f"  Span: {(df['visit_date'].max() - df['visit_date'].min()).days} days")

print(f"\nDate value counts (first 10):")
print(df['visit_date'].value_counts().head(10))

print(f"\nDataset sorted by visit_date:")
df_sorted = df.sort_values('visit_date')
print(f"  First date: {df_sorted['visit_date'].iloc[0]}")
print(f"  Last date: {df_sorted['visit_date'].iloc[-1]}")

# Show split point for 80/20
split_idx = int(len(df) * 0.8)
print(f"\n--- PROPOSED 80/20 TEMPORAL SPLIT ---")
print(f"Total records: {len(df)}")
print(f"Training (80%, earlier dates): {split_idx} records")
print(f"Testing (20%, later dates): {len(df) - split_idx} records")

print(f"\nTraining date range: {df_sorted['visit_date'].iloc[0]} to {df_sorted['visit_date'].iloc[split_idx-1]}")
print(f"Testing date range: {df_sorted['visit_date'].iloc[split_idx]} to {df_sorted['visit_date'].iloc[-1]}")
