import maya.cmds as mc
import os
# import xgenm as xge
# import xgenm.xgGlobal as xgg
from datetime import datetime, date
from itertools import product
from glob import glob


sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
xgPath = "/maya/base/scenes/base__head_coll.xgen"
maPath = "/maya/base/scenes/base.ma"
deltaPath = "maya/base_delta/scenes/deltaGen/"


def collExtract(path) -> str:
    """extracts collection name from file name based on pattern:
    {name}__{collection}__{modifier}__{attributes}"""
    return path.split('__')[-3]


def xgd_import():
    """ IMPORT XGD """
    importPath = mc.fileDialog2(fm=4) #open multi files
    for path in importPath:
        xge.applyDelta(collExtract(path), str(path))
    de = xgg.DescriptionEditor
    de.refresh("Full")


def xgd_export():
    """ EXPORT XGD """
    col = mc.ls("*_coll")[0]
    exportPath = mc.fileDialog2(fm=0)[0]
    xge.createDelta(str(col), str(exportPath))


def file_path(root_dir, groom_name:str = "", variant:str = "",):
    if variant:
        variant = f'variants/{variant}'
    else:
        variant = "base_delta"
    project_path = f'{root_dir}/{groom_name}/maya/{variant}/'
    full_path = project_path+"scenes/base.ma"
    return project_path, full_path


def xgen_set_prj(maya_prj_path, xgen_prj_path):
    # maya workspace
    mc.workspace(maya_prj_path, openWorkspace=True)
    # xgen project for hair collection root path
    xge.setProjectPath(xgen_prj_path)


def file_open(path):
    mc.file(new= True, f=True)
    mc.file(path,open=True)


def file_ref(path):
    mc.file(path, iv=1, gl=1, mnc=1, ns=":", options="v=0", reference=1)


def xgen_list_collections():
    return list(xge.palettes())


def refresh_ui():
    """refresh xgen UI after delta load"""
    de = xgg.DescriptionEditor #Get the description editor first.
    de.refresh("Full") #Do a full UI refresh


def apply_delta_from_paths(collection, paths:list):
    for path in paths:
        # print(path)
        xge.applyDelta(collection, path)
    refresh_ui()
    

def img_output_dir(dx, dy) -> str:
    """returns string representation of 2d array min/max"""
    output_suffix = "_".join([dx[0],dx[-1],dy[0],dy[-1]])
    img_output_path = f'{project_path}/images/{output_suffix}/'
    if not os.path.exists(img_output_path):
        os.mkdir(img_output_path)
        print("created dir:", img_output_path)
    return img_output_path


def get_deltas(delta_path:str) -> list:
    """get deltas thru file dialogue. Returns choices"""
    deltas = mc.fileDialog2(cap="CHOOSE UR DELTAS", fm=4, dir = "{}".format(delta_path))
    ids = [x.split("/")[-1].replace(".xgd", "") for x in deltas]
    return deltas, ids
# (['G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AliceRivera/maya/base_delta/scenes/deltaGen/dh_exp_gScale_1.3.xgd'], ['dh_exp_gScale_1.3'])


def delta_retrieval(path:str) -> dict:
    """ output dict as follows:
    {'modifier_name': ['delta_path_x[0:-1]y[0] for y[0:-1]', 'delta_names_extracted'**], ... }"""
    # deltaGen path
    # path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AmandaMoore/maya/base_delta/scenes/deltaGen"

    class delta:
        def __init__(self, path:str, filter:str):
            deltas = [x.replace(os.sep, '/') for x in glob(path+"/*.xgd")]
            self.paths = [x for x in deltas if filter in x]
            self.ids = [x.split("/")[-1].replace(".xgd", "") for x in self.paths]

    coil_deltas = delta(path, "dh_coil")
    noise_deltas = delta(path, "dh_noise")
    cutClamp_deltas = delta(path, "dh_cutClamp")
    cutPercent_deltas = delta(path, "dh_cutPercent")
    gScale_deltas = delta(path, "dh_exp_gScale")

    # get noise delta matrix min/max
    freq_set = set()
    mag_set = set()
    for id in noise_deltas.ids:
        freq_value = id.split("_")[2].strip('freq')
        try:
            freq_value = int(freq_value)
        except ValueError:
            freq_value = float(freq_value)
        freq_set.add(freq_value)
        mag_value = id.split("_")[3].strip('mag')
        try:
            mag_value = int(mag_value)
        except ValueError:
            mag_value = float(mag_value)
        mag_set.add(mag_value)
    # freq_list, mag_list = sorted(list(freq_set), key=float), sorted(list(mag_set), key=float)

    count_set = set()
    radius_set = set()
    for id in coil_deltas.ids:
        count_value = id.split("_")[2].strip('count')
        try:
            count_value = (count_value)
        except ValueError:
            count_value = float(count_value)
        count_set.add(count_value)
        radius_value = id.split("_")[3].strip('radius')
        try:
            radius_value = int(radius_value)
        except ValueError:
            radius_value = float(radius_value)
        radius_set.add(radius_value)
    # count_list, radius_list = sorted(list(count_set), key=float), sorted(list(radius_set), key=float)

    def sorted_sets(key, *args):
        arg_list = []
        for arg in args:
            arg_list.append(sorted(list(arg), key=key))
        return arg_list

    freq_list, mag_list, count_list, radius_list = sorted_sets(float, freq_set, mag_set, count_set, radius_set)

    # create a list of delta permutations | freq priority
    dh_noise_iters_list = [[] for i in range(0, len(freq_list))]
    for i, f in enumerate(freq_list, 0):
        for m in mag_list:
            dh_noise_iters_list[i].append(f'{path}/dh_noise_{f}freq_{m}mag_0.5corr.xgd')
   
    # create a list of delta permutations | radius priority
    dh_coil_iters_list = [[] for i in range(0, len(radius_list))]
    for i, r in enumerate(radius_list, 0):
        for c in count_list:
            dh_coil_iters_list[i].append(f'{path}/dh_coil_{c}count_{r}radius.xgd')
    

    # extract sorted ids from iter_list
    return {"dh_noise" : list(zip(dh_noise_iters_list, [[x.split('/')[-1].rstrip('.xgd') for x in iter] for iter in dh_noise_iters_list])),
        "dh_coil" : list(zip(dh_coil_iters_list, [[x.split('/')[-1].rstrip('.xgd') for x in iter] for iter in dh_coil_iters_list])),
        "dh_cutClamp" : [cutClamp_deltas.paths, cutClamp_deltas.ids],
        "dh_cutPercent": [cutPercent_deltas.paths, cutPercent_deltas.ids],
        "dh_exp_gScale": [gScale_deltas.paths, gScale_deltas.ids],
    }

def get_deltas(delta_path:str) -> list:
    """get deltas thru file dialogue. Returns choices"""
    deltas = mc.fileDialog2(cap="CHOOSE UR DELTAS", fm=4, dir = "{}".format(delta_path))
    ids = [x.split("/")[-1].replace(".xgd", "") for x in deltas]
    return deltas, ids

# for k,v in delta_retrieval("G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AmandaMoore/maya/base_delta/scenes/deltaGen").items():
    # print(v)
import pprint
pp = pprint.PrettyPrinter(indent=1)
path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AmandaMoore/maya/base_delta/scenes/deltaGen"
deltas = delta_retrieval(path)
# pp.pprint(deltas['dh_exp_gScale'])
pp.pprint(deltas)