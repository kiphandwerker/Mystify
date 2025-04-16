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