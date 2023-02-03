import maya.cmds as mc
import os
# import xgenm as xge
# import xgenm.xgGlobal as xgg
from datetime import datetime, date
from itertools import product
from glob import glob


# sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
# xgPath = "/maya/base/scenes/base__head_coll.xgen"
# maPath = "/maya/base/scenes/base.ma"
# deltaPath = "maya/base_delta/scenes/deltaGen/"

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


# def file_path(root_dir, groom_name:str = "", variant:str = "",):
#     if variant:
#         variant = f'variants/{variant}'
#     else:
#         variant = "base_delta"
#     project_path = f'{root_dir}/{groom_name}/maya/{variant}/'
#     full_path = project_path+"scenes/base.ma"
#     return project_path, full_path


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
    

def img_output_dir(project_path, dx, dy) -> str:
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


def delta_retrieval(path:str, collection:str) -> dict:
    # deltaGen path
    # path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AliceRivera/maya/base_delta/scenes/deltaGen"

    deltas = [x.replace(os.sep, '/') for x in glob(path+"/*.xgd")] # get all xgd in path
    modifiers = set([x.split('__')[-2] for x in deltas]) # modifiers available
    # collections = set([x.split('__')[-3] for x in deltas]) # colletions available

    class delta:
        def __init__(self, modifier:str):
            self.paths = [x for x in deltas if modifier in x and collection in x] # filtered xgd by mod and col
            self.ids = [x.split("/")[-1].replace(".xgd", "") for x in self.paths] # filename only

    def _func(input):
        """ returns an organized zip list of deltas from the input modifier call"""
        save = set()
        single = False
        for id in input.ids:
            split = id.split('__')[-1].split('_')
            if len(split) % 2 != 0:
                print("somethings wrong with the filenames")
            if len(split) == 2:
                single = True
                save.add('_'.join(split[:2]))
            else:
                save.add('_'.join(split[:2])+'_')

        """filter paths based on saved set"""
        d={}
        for i in save:
            for x in input.paths:
                if i in x:
                    if i not in d:
                        if single == False:
                            d[i] = [x]
                        else:
                            d[i] = x
                    else:
                        # pass
                        d[i].append(x)
        iters_list = sorted(d.values())
        if single == True:
            return [list(iters_list), [x.split('/')[-1].rstrip('.xgd') for x in iters_list]]
        else:
            return list(zip(iters_list, [[x.split('/')[-1].rstrip('.xgd') for x in iter] for iter in iters_list]))


    return { mod:_func(delta(mod)) for mod in modifiers}

def get_deltas(delta_path:str) -> list:
    """get deltas thru file dialogue. Returns choices"""
    deltas = mc.fileDialog2(cap="CHOOSE UR DELTAS", fm=4, dir = "{}".format(delta_path))
    ids = [x.split("/")[-1].replace(".xgd", "") for x in deltas]
    return deltas, ids

# for k,v in delta_retrieval("G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AmandaMoore/maya/base_delta/scenes/deltaGen").items():
    # print(v)
# import pprint
# pp = pprint.PrettyPrinter(indent=1)
# path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/AmandaMoore/maya/base_delta/scenes/deltaGen"
# deltas = delta_retrieval(path)
# # pp.pprint(deltas['dh_exp_gScale'])
# pp.pprint(deltas)