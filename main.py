# Import the function
import Mystify      

# Initilize the function
M = Mystify.Mystify()

# Create a fake dataset with 100 people with defaults values
MainData = M.GenerateData(100)

# Get a list of all the PHI variables available
M.ShowPHIvars()

# Include specific variables
MainData = M.GenerateData(n=100, MoreFields=['email', 'phone', 'insurance_id', 'diagnosis'])

# Mystify the data
synthetic_data = M.MystifyData(MainData)

# Mystify the data but preserve patient_id
synthetic_data = M.MystifyData(MainData, preserve_columns=['patient_id'])

# Save for future exploration
M.SaveCSV(synthetic_data, "MystifiedData")