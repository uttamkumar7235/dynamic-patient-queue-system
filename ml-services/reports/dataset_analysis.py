from pathlib import Path
import json

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / 'data' / 'raw' / 'synthetic_patient_queue_dataset.csv'
OUT_DIR = ROOT / 'reports'
OUT_DIR.mkdir(exist_ok=True)


def save_json(path, payload):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, default=str)


df = pd.read_csv(DATA_PATH)

summary = {
    'rows': int(df.shape[0]),
    'columns': int(df.shape[1]),
    'column_names': list(df.columns),
    'dtypes': df.dtypes.astype(str).to_dict(),
    'missing_values': {k: int(v) for k, v in df.isna().sum().items()},
    'duplicate_rows': int(df.duplicated().sum()),
    'numerical_descriptive_stats': df.describe(include='number').round(4).to_dict(),
    'categorical_unique_values': {
        col: sorted(df[col].dropna().unique().tolist())[:20] for col in df.select_dtypes(include=['object', 'category']).columns
    },
    'head': df.head(5).to_dict(orient='records')
}

save_json(OUT_DIR / 'dataset_summary.json', summary)

print('DATASET_SHAPE', df.shape)
print('COLUMNS', list(df.columns))
print('DTYPES')
print(df.dtypes)
print('MISSING_VALUES')
print(df.isna().sum())
print('DUPLICATE_ROWS', df.duplicated().sum())
print('NUMERICAL_STATS')
print(df.describe(include='number').round(4))
print('CATEGORICAL_UNIQUE_VALUES')
for col in df.select_dtypes(include=['object', 'category']).columns:
    print(f'-- {col}: {df[col].dropna().unique()[:20]}')

# Target inference heuristics from column names and basic correlations
numeric_cols = df.select_dtypes(include='number').columns.tolist()
likely_target_candidates = []
for col in numeric_cols:
    if any(token in col.lower() for token in ['wait', 'time', 'minutes', 'duration', 'delay']):
        likely_target_candidates.append(col)

print('LIKELY_TARGET_CANDIDATES', likely_target_candidates)

# Distibution and outlier plots
plt.figure(figsize=(10, 5))
if likely_target_candidates:
    target_col = likely_target_candidates[0]
    sns.histplot(df[target_col], kde=True, bins=30)
    plt.title(f'Distribution of {target_col}')
    plt.xlabel(target_col)
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig(OUT_DIR / f'{target_col}_distribution.png', dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    sns.boxplot(x=df[target_col])
    plt.title(f'Outlier check for {target_col}')
    plt.xlabel(target_col)
    plt.tight_layout()
    plt.savefig(OUT_DIR / f'{target_col}_boxplot.png', dpi=200)
    plt.close()

# Numeric feature overview
if len(numeric_cols) > 1:
    plt.figure(figsize=(14, 8))
    corr = df[numeric_cols].corr(numeric_only=True)
    sns.heatmap(corr, annot=False, cmap='coolwarm', fmt='.2f')
    plt.title('Numeric feature correlation heatmap')
    plt.tight_layout()
    plt.savefig(OUT_DIR / 'numeric_correlation_heatmap.png', dpi=200)
    plt.close()

# Categorical counts
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
for col in cat_cols[:5]:
    plt.figure(figsize=(10, 4))
    sns.countplot(data=df, x=col, order=df[col].value_counts().index)
    plt.title(f'Value counts for {col}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(OUT_DIR / f'{col}_value_counts.png', dpi=200)
    plt.close()

print('ANALYSIS_REPORT_SAVED', OUT_DIR / 'dataset_summary.json')
print('PLOTS_SAVED', list(OUT_DIR.glob('*.png')))
