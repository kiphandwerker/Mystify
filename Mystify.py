import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta
fake = Faker()

class Mystify:

    def GenerateData(n = 100):
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
        return data

    def Mystify(df, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        Faker.seed(seed)
        synthetic = pd.DataFrame()

        # Basic PHI keyword matching (can be extended)
        phi_keywords = {
            'name': lambda: fake.name(),
            'first_name': lambda: fake.first_name(),
            'last_name': lambda: fake.last_name(),
            'email': lambda: fake.email(),
            'address': lambda: fake.address().replace("\n", ", "),
            'phone': lambda: fake.phone_number(),
            'ssn': lambda: fake.ssn(),
            'zip': lambda: fake.zipcode(),
            'city': lambda: fake.city(),
            'state': lambda: fake.state(),
            'dob': lambda: fake.date_of_birth(minimum_age=18, maximum_age=90),
        }

        def detect_phi_column(col_name):
            for key in phi_keywords:
                if key in col_name.lower():
                    return phi_keywords[key]
            return None

        for col in df.columns:
            dtype = df[col].dtype
            gen_phi = detect_phi_column(col)

            if gen_phi:
                synthetic[col] = [gen_phi() for _ in range(len(df))]

            elif pd.api.types.is_numeric_dtype(df[col]):
                min_val, max_val = df[col].min(), df[col].max()
                if pd.api.types.is_integer_dtype(df[col]):
                    synthetic[col] = np.random.randint(min_val, max_val + 1, size=len(df))
                else:
                    synthetic[col] = np.random.uniform(min_val, max_val, size=len(df))
                    synthetic[col] = synthetic[col].round(2)

            elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) > 0:
                    synthetic[col] = np.random.choice(unique_vals, size=len(df))
                else:
                    synthetic[col] = ['' for _ in range(len(df))]

            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                min_date, max_date = df[col].min(), df[col].max()
                date_range = (max_date - min_date).days
                synthetic[col] = [min_date + timedelta(days=np.random.randint(0, date_range + 1)) for _ in range(len(df))]

            else:
                synthetic[col] = [None for _ in range(len(df))]

        return synthetic
    
    def SaveCSV(df,name):
        print("Saving CSV")
        out = pd.DataFrame(df)
        out.to_csv(f"..\\Mystify\\{name}.csv",header=True)

# df = pd.DataFrame({
#     'patient_id': ['P001', 'P002', 'P003'],
#     'first_name': ['Alice', 'Bob', 'Carol'],
#     'email': ['a@example.com', 'b@example.com', 'c@example.com'],
#     'age': [34, 45, 29],
#     'bmi': [25.1, 30.2, 22.8],
#     'visit_date': pd.to_datetime(['2023-01-10', '2023-02-15', '2023-03-20'])
# })
