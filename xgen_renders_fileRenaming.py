from glob import glob
import os
import shutil

path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/SimonYuen/maya/base_delta/images/dh_exp_gScale_0.1_dh_exp_gScale_2.6_dh_coil_0.5c0.1r_dh_coil_0.5c3.6r/**.tif"
# glob(path)
paths = [x.replace(os.sep, '/').rpartition('/')[0] for x in glob(path)]
names = [x.replace(os.sep, '/').rpartition('/')[-1] for x in glob(path)]
# print(paths)
# print(names)
frames = [x.split('.')[1].split('_')[0] for x in names]

for frame in frames:
    old = f'{frame}_'
    new = f'{int(frame):04}_'
    # print(old, new)

# for frame, name in zip(frames, names):
    # print(name.replace(f'{frame}_', f'{int(frame):04}_'))

newNames = [name.replace(f'{frame}_', f'{int(frame):04}_') for frame, name in zip(frames, names)]
# print(names, newNames)

oldpath = [f'{a}/{b}' for a,b in zip(paths, names)]
newpath = [f'{a}/{b}' for a,b in zip(paths, newNames)]

[shutil.move(a, b) for a, b in zip(oldpath, newpath)]