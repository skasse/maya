import os
from glob import glob
import json
import shutil


path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/SimonYuen/maya/base_delta/images/dh_coil_2.0c0.1r_dh_coil_2.0c3.6r_dh_noise_2.1freq_0.6mag_0.5corr_dh_noise_2.1freq_4.6mag_0.5corr/"
source_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/SimonYuen/maya/base_delta/images/"
dest_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/image_DB/"
folders = [x.replace(os.sep, '/')+'/' for x in glob(f'{source_path}**')]
results = []
for folder in folders:
    if os.path.exists(folder+"/metadata.json"):

        images = [x.replace(os.sep, '/').split('/')[-1] for x in glob(f'{folder}/*.tif')]

        with open(folder+"metadata.json", 'r') as f:
            metadata = json.load(f)

        groom_name = metadata['MASTER_CTRL']['project_dir'].split('/')[4]

        deltas = list(metadata['MASTER_CTRL']['input_deltas'].lstrip('[').rstrip(']').lstrip('(').rstrip(')').split('), ('))
        deltas = [x.replace("', '", '__').strip("'") for x in deltas]

        for image, delta in zip(images, deltas):
            if not os.path.exists(dest_path+groom_name+"__"+delta+".tif"):
                print(f'copy {image} to {groom_name}__{delta}.tif')
                shutil.copy(folder+image, dest_path+groom_name+"__"+delta+".tif")
            else:
                print(f'{dest_path}{groom_name}__{delta}.tif exists.  Copy aborted.')





