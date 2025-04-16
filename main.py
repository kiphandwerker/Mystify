import Mystify

M = Mystify.Mystify()
MainData = M.GenerateData(100)
synthetic_data = M.Mystify(MainData, preserve_columns=['patient_id'])
synthetic_data = M.Mystify(MainData)
print(MainData)
print(synthetic_data)

M.SaveCSV(synthetic_data, "test")