
import pandas as pd
import numpy as np
import random
from datetime import timedelta
import SampleData

def Mystify(df, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    synthetic = pd.DataFrame()

    for col in df.columns:
        dtype = df[col].dtype

        if pd.api.types.is_numeric_dtype(df[col]):
            # Preserve range and type
            min_val, max_val = df[col].min(), df[col].max()
            if pd.api.types.is_integer_dtype(df[col]):
                synthetic[col] = np.random.randint(min_val, max_val + 1, size=len(df))
            else:
                synthetic[col] = np.random.uniform(min_val, max_val, size=len(df))
                synthetic[col] = synthetic[col].round(2)

        elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
            unique_vals = df[col].dropna().unique()
            synthetic[col] = np.random.choice(unique_vals, size=len(df))

        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            min_date, max_date = df[col].min(), df[col].max()
            date_range = (max_date - min_date).days
            synthetic[col] = [min_date + timedelta(days=np.random.randint(0, date_range + 1)) for _ in range(len(df))]

        else:
            # For unsupported or unknown types, just fill with NaNs
            synthetic[col] = np.nan

    return synthetic

np.random.seed(42)

# Number of rows
n = 100

# Generate the dataset
data = pd.DataFrame({
    'patient_id': [f'P{str(i).zfill(4)}' for i in range(1, n+1)],  # Unique identifier
    'age': np.random.randint(18, 90, size=n),                      # Numeric: age
    'gender': np.random.choice(['Male', 'Female'], size=n),       # Categorical: gender
    'bmi': np.round(np.random.normal(27, 5, size=n), 1),           # Numeric: BMI
    'smoker': np.random.choice(['Yes', 'No'], size=n, p=[0.2, 0.8]),  # Categorical: smoking status
    'systolic_bp': np.random.randint(100, 180, size=n),            # Numeric: systolic blood pressure
    'cholesterol_level': np.random.choice(['Normal', 'Borderline', 'High'], size=n, p=[0.5, 0.3, 0.2]),  # Categorical
    'visit_date': pd.to_datetime('2025-01-01') + pd.to_timedelta(np.random.randint(0, 365, size=n), unit='days')  # Date
})

synthetic_data = Mystify(data)
print(synthetic_data.head())