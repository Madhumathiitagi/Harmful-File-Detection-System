import pandas as pd

df = pd.read_parquet("ember/train_ember_2018_v2_features.parquet")
print(df["Label"].value_counts())
