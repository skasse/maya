import re
from glob import glob
import os

#path = "C:\\tmp\\"
path = "G:\\Shared drives\\TriplegangersGroom_ext\\Groom_INTERNAL\\"
grooms = [x for x in glob(path+"**\\maya\\**\\scenes\\")]
for groom in grooms:
    filename = groom+"base.ma"
    if os.path.exists(filename):
        print(filename)
        with open(filename) as f:
            s = f.read()
        with open(filename, 'w') as f:
            s = re.sub(r'(\w*_{2})', 'base__', s)
            f.write(s)