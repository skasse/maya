from xgd_parser_v20220708 import dc_extract 
from glob import glob
import os


grooms = [x.replace(os.sep, '/').split('/')[-1] for x in glob("G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/**")]
collections = dc_extract(grooms[19])
for k,v in collections.items():
    print(v)