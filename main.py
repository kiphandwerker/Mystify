import Mystify

df = Mystify.GenerateData(100)
synthetic_data = Mystify.Mystify(df)
#print(synthetic_data)
print(synthetic_data.head())
Mystify.SaveCSV(df,"test")