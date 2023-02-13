from random import randint
from pathlib import Path
import pandas as pd
import numpy as np

df = pd.read_parquet('data/fhv/fhv_tripdata_2019-03.parquet')
df = df.replace(np.nan, -1)
df['DOlocationID'] = df['DOlocationID'].astype('Int64')
df['PUlocationID'] = df['PUlocationID'].astype('Int64')

print(df.isnull().sum())
