from glob import glob
import pandas as pd
import os

path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/*/maya/base_delta/images/*/contactSheet.png"

df = pd.DataFrame([x.replace(os.sep,'/').split('/') for x in glob(path)])
# df = [x.replace(os.sep,'/').split('/') for x in glob(path)]
# print(df)

# unique in column
# print(df[4].unique())

# unique+count in column
print(df[4].value_counts())