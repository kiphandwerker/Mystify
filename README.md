# Mystify

```Mystify``` is a Python function used for generating and anonymizing (or mystifying) datasets containing Personally Identifiable Information (PHI). It's useful for testing, demoing, or sharing healthcare-related data while preserving data structure and utility.

# Table of Contents
- [Features](#features)
- [Installation](#installation)
- [File Structure](#file-structure)
- [How it works](#how-it-works)
- [Usage](#usage)

# Features
</ul>
<li>🔒 Replace PHI fields with realistic fake data using the Faker library

<li>🧪 Generate synthetic patient datasets for development or testing

<li>🌀 Randomize numeric, categorical, and datetime columns

<li>🎯 Preserve specific columns from being modified

<li>💾 Export datasets to CSV

</ul>

# Installation

<ol>
<li>Clone the git repository

```git
git clone https://github.com/kiphandwerker/Mystify.git
```

<li> Install dependencies

```python
pip install -r requirements.txt
```
</ol>

# File Structure

```bash
/Mystify
├───main.py             # Executable code that resembles Usage
├───Mystify.py          # Class and functions
├───requirements.txt    # Dependencies
└───test.csv            # Sample output
```



# How It Works
The Mystify class includes tools to:
<ul>

<li>Generate synthetic patient data (GenerateData)

<li>Replace sensitive fields with randomized but realistic values (Mystify)

<li>View configurable PHI variable definitions (ShowPHIvars)

<li>Save the modified dataset to a .csv file (SaveCSV)

</ul>

# Usage

```python
# Import the function
import Mystify      

# Initilize the function
M = Mystify.Mystify()

# Create a fake dataset with 100 people
MainData = M.GenerateData(100)

# Mystify the data
synthetic_data = M.MystifyData(MainData)

# Mystify the data but preserve patient_id
synthetic_data = M.MystifyData(MainData, preserve_columns=['patient_id'])

# Save for future exploration
M.SaveCSV(synthetic_data, "MystifiedData")
```