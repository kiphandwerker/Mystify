import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import timedelta
fake = Faker()

class Mystify:

    def __init__(self):
        self.phi_keywords = {
            # Personal Identifiers
            'name': lambda: fake.name(),
            'first_name': lambda: fake.first_name(),
            'last_name': lambda: fake.last_name(),
            'middle_name': lambda: fake.first_name(),
            'prefix': lambda: fake.prefix(),
            'suffix': lambda: fake.suffix(),
            'ssn': lambda: fake.ssn(),
            'dob': lambda: fake.date_of_birth(minimum_age=18, maximum_age=90),
            'age': lambda: random.randint(18, 90),
            'gender': lambda: random.choice(['Male', 'Female', 'Non-binary', 'Other']),
            'marital_status': lambda: random.choice(['Single', 'Married', 'Divorced', 'Widowed']),

            # Contact Information
            'email': lambda: fake.email(),
            'phone': lambda: fake.phone_number(),
            'phone_mobile': lambda: fake.phone_number(),
            'phone_home': lambda: fake.phone_number(),
            'phone_work': lambda: fake.phone_number(),

            # Address Information
            'address': lambda: fake.address().replace("\n", ", "),
            'street_address': lambda: fake.street_address(),
            'secondary_address': lambda: fake.secondary_address(),
            'city': lambda: fake.city(),
            'state': lambda: fake.state(),
            'zip': lambda: fake.zipcode(),
            'country': lambda: fake.country(),

            # Employment/Insurance
            'employer': lambda: fake.company(),
            'job_title': lambda: fake.job(),
            'insurance_provider': lambda: fake.company(),
            'insurance_id': lambda: fake.bothify(text='??########'),

            # Medical Info (simulated, not directly supported by Faker)
            'medical_record_number': lambda: fake.bothify(text='MRN#######'),
            'patient_id': lambda: fake.uuid4(),
            'physician': lambda: fake.name(),
            'diagnosis': lambda: fake.sentence(nb_words=4).rstrip('.'),
            'treatment': lambda: fake.sentence(nb_words=6).rstrip('.'),
            'medication': lambda: fake.word().capitalize(),

            # Financial Info
            'credit_card': lambda: fake.credit_card_number(),
            'credit_card_provider': lambda: fake.credit_card_provider(),
            'bank_account': lambda: fake.bban(),
            'routing_number': lambda: fake.iban(),

            # Unique Identifiers
            'device_id': lambda: fake.uuid4(),
            'ip_address': lambda: fake.ipv4_public(),
            'mac_address': lambda: fake.mac_address(),
            'user_id': lambda: fake.user_name(),
            'url': lambda: fake.url()
        }

    def ShowPHIvars(self):
        for key in self.phi_keywords:
            print(key)

    def GenerateData(self,n = 100):
        data = pd.DataFrame({
            'patient_id': [f'P{str(i).zfill(4)}' for i in range(1, n+1)],  # Unique identifier
            'first_name': [fake.first_name() for _ in range(1, n+1)],
            'last_name': [fake.last_name() for _ in range(1, n+1)],
            'ssn':[fake.ssn() for _ in range(1, n+1)],
            'age': np.random.randint(18, 90, size=n),                      # Numeric: age
            'gender': np.random.choice(['Male', 'Female'], size=n),       # Categorical: gender
            'bmi': np.round(np.random.normal(27, 5, size=n), 1),           # Numeric: BMI
            'smoker': np.random.choice(['Yes', 'No'], size=n, p=[0.2, 0.8]),  # Categorical: smoking status
            'systolic_bp': np.random.randint(100, 180, size=n),            # Numeric: systolic blood pressure
            'cholesterol_level': np.random.choice(['Normal', 'Borderline', 'High'], size=n, p=[0.5, 0.3, 0.2]),  # Categorical
            'visit_date': pd.to_datetime('2025-01-01') + pd.to_timedelta(np.random.randint(0, 365, size=n), unit='days')  # Date
        })
        return data

    def MystifyData(self, df, seed=42, preserve_columns=None):
        if preserve_columns is None:
            preserve_columns = []

        np.random.seed(seed)
        random.seed(seed)
        Faker.seed(seed)
        mystified = pd.DataFrame()

        def detect_phi_column(col_name):
            col_name_lower = col_name.lower()
            if col_name_lower in self.phi_keywords:
                return self.phi_keywords[col_name_lower]
            for key in self.phi_keywords:
                if key in col_name_lower:
                    return self.phi_keywords[key]
            return None

        for col in df.columns:
            if col in preserve_columns:
                mystified[col] = df[col].copy()
                continue

            dtype = df[col].dtype
            gen_phi = detect_phi_column(col)

            if gen_phi:
                mystified[col] = [gen_phi() for _ in range(len(df))]

            elif pd.api.types.is_numeric_dtype(df[col]):
                min_val, max_val = df[col].min(), df[col].max()
                if pd.api.types.is_integer_dtype(df[col]):
                    mystified[col] = np.random.randint(min_val, max_val + 1, size=len(df))
                else:
                    mystified[col] = np.random.uniform(min_val, max_val, size=len(df)).round(2)

            elif pd.api.types.is_categorical_dtype(df[col]) or df[col].dtype == 'object':
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) > 0:
                    mystified[col] = np.random.choice(unique_vals, size=len(df))
                else:
                    mystified[col] = ['' for _ in range(len(df))]

            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                min_date, max_date = df[col].min(), df[col].max()
                date_range = (max_date - min_date).days
                mystified[col] = [min_date + timedelta(days=np.random.randint(0, date_range + 1)) for _ in range(len(df))]

            else:
                mystified[col] = [None for _ in range(len(df))]

        return mystified
    
    @staticmethod
    def SaveCSV(df,name):
        print("Saving CSV")
        out = pd.DataFrame(df)
        out.to_csv(f"..\\Mystify\\{name}.csv",header=True, index=False)
