import pandas as pd

df = pd.read_parquet("train_ember_2018_v2_features.parquet")

print("Total columns:", len(df.columns))
print(df.columns.tolist())
