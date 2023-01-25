
import os, shutil
from glob import glob
import pandas as pd

path = r'G:\Shared drives\TriplegangersGroom_ext\Groom_INTERNAL\*\maya\base_delta\images\*\contactSheet.png'
dest_path = r"G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/image_DB/"
images = pd.Series([x.replace(os.sep, '/') for x in glob(path)])
# split images and create a dataframe of elements
images_split = pd.DataFrame(pd.Series([x.split("/") for x in images]).tolist())
 # create smaller db from desired columns
df = pd.concat([images, images_split.iloc[:,4], images_split.iloc[:,8]], axis=1)

print(df)
# for c, i in enumerate(df[0]):
#     print(df.iloc[c,1])

for row, contactSheet in enumerate(df[0]):
    newpath = f'{dest_path}{df.iloc[row,1]}/'
    newname = f'{df.iloc[row,2]}.png'
    os.makedirs(os.path.dirname(newpath), exist_ok=True)
    shutil.copy(df.iloc[row,0], newpath+newname)
    print(f'copied {newpath}: {row} of {len(df[0])}')