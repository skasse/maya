import maya.cmds as mc
import os
import xgenm as xge
import xgenm.xgGlobal as xgg
from datetime import datetime, date
from itertools import product
from glob import glob
# import mtoa.aovs as aovs



# from natron_contactSheet import natron_write


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

    def sorted_sets(key, *args, **kwargs):
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


def render(groom_path, dx:list(), dy:list(), resolution:int = 2048):
    project_path = "/".join(groom_path[0].split("/")[:-2])
    turntable_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/turntableQC/scenes/turntableQC_light.ma"
    renderWidth = renderHeight = resolution
    camera = "camera1"
    startFrame = 1002
    endFrame = 1002


    pathcombos = list(product(*[dx[0], dy[0]]))
    namecombos = list(product(*[dx[1], dy[1]]))

    xgen_set_prj(project_path, project_path) # set project
    render_path = img_output_dir(dx[1], dy[1])

    #########

    import json
    project_dir = render_path
    json_file = "metadata.json"
    metadata = {"MASTER_CTRL" : {
                    "rows" : len(dx[1]), 
                    "columns" : len(dy[1]), 
                    "resolution" : 500,
                    "project_dir" : str(project_dir),
                    "final_frame" : len(namecombos), 
                    "date" : str(date.today()),
                    "input_deltas" : str(namecombos)
                }, 
                "root" : {
                    "project_directory" : str(project_dir),
                    # "last_frame" : len(namecombos)
                }
    }

    with open(fr'{render_path}{json_file}',  "w") as outfile:
        print("writing json metadata to {}".format(render_path+json_file))
        json.dump(metadata, outfile)
        print("writing metadata complete")
    # with open("C:/Scripts/maya/xgen_renderSettings.json") as infile:
    #     rendersettings = json.load(infile)
    ######
    import time
    print("creating render matrix from {0} and {1}".format(dx[1], dy[1]))
    sequence_start = datetime.now()
    print("begin!")
    mc.progressWindow(isInterruptable=1)
    for path in enumerate(pathcombos, 1):
            progress_amount = int(((path[0])/len(pathcombos)*100))
            mc.progressWindow(edit=True, progress=progress_amount, status=f'{groom_path[0].split("/")[4]}: rendering {path[0]} out of {len(pathcombos)}', title=f'{path[1]}')
            time.sleep(.05)
            img_path = f'{render_path}delta.{path[0]:04}'
            if not os.path.isfile(f'{img_path}_1.tif'):
                file_open(groom_path) # open groom
                print("fileopen")  
                file_ref(turntable_path) # reference lighting Turntable
                print("file referenced")
                mc.sets("scalpHiHead", fe="head_mtlSG")
                apply_delta_from_paths("head_coll", [path[1][0], path[1][1]])
                print("apply deltas")
                mc.currentTime(1002, edit=True)
                # RENDER SETTINGS 
                mc.setAttr('defaultArnoldRenderOptions.AASamples', 6)
                mc.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', 5)
                mc.setAttr('defaultArnoldRenderOptions.GISpecularSamples', 5)
                mc.setAttr('defaultArnoldRenderOptions.GITransmissionSamples', 5)
                mc.setAttr('defaultArnoldRenderOptions.GISssSamples', 5)
                # mc.setAttr("defaultArnoldDriver.mergeAOVs", 1)
                # aovs.AOVInterface().addAOV('RGBA')
                # aovs.AOVInterface().addAOV('Z')
                mc.setAttr("defaultRenderGlobals.imageFilePrefix", img_path, type="string")
                mc.setAttr("defaultArnoldRenderOptions.renderDevice", 1) #enable GPU
                mc.setAttr("defaultRenderGlobals.animationRange", 0)
                mc.setAttr("defaultRenderGlobals.startFrame", startFrame)
                mc.setAttr("defaultRenderGlobals.endFrame", endFrame)
                mc.setAttr("defaultArnoldDriver.ai_translator", "tif", type="string")
                mc.setAttr("defaultRenderGlobals.animation", 0)
                mc.setAttr("perspShape.renderable", 0)
                mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
                mc.setAttr("defaultResolution.width", renderWidth)
                mc.setAttr("defaultResolution.height", renderHeight)
                mc.setAttr("defaultResolution.deviceAspectRatio", 1)
                image_start = datetime.now()
                print("rendering {0} out of {1}".format(path[0], len(pathcombos)))
                print("rendering delta {}".format([d.split("/")[-1] for d in [path[1][0], path[1][1]]]))
                print("render starting @", image_start)
                mc.arnoldRender(w=renderWidth, h=renderHeight, seq="1002", b=False)#, cam=camera)
                image_end = datetime.now()
                print("render complete @", image_end)
                print("render time was", image_end - image_start)
                print("render output path = {}".format(img_path))
            else:
                print(f'{img_path} exists.  Skipping render')
    mc.progressWindow(endProgress=1)
    
    print("sequence complete:\ntotal render time was: {0}\navg render time was:{1}".format(
        datetime.now() - sequence_start, (datetime.now() - sequence_start)/len(pathcombos)))

    if not os.path.isfile(f'{render_path}contactSheet.png'):
        print("Beginning comp in Nuke.  Launching Nuke Now")
        # write inputs and metadata

        # render images

        # render contact sheet
        from subprocess import Popen, PIPE
        process = Popen(["C:/Program Files/Nuke13.2v4/Nuke13.2.exe", "--nukex", "-x", "-i", "C:/Scripts/nuke/runonstart.py", project_dir, "1,1"], stdout=PIPE, stderr=PIPE)
        stdout,stderr = process.communicate()
        print(stdout)

        print("***RENDERING COMPLETE***")
        print(render_path)
    else:
        print("contactSheet exists. skipping render")



groom_path:list = mc.fileDialog2(cap="CHOOSE UR GROOM", fm=1, dir="G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/")
project_path = "/".join(groom_path[0].split("/")[:-2])
delta_path = "/".join(groom_path[0].split("/")[:-1])+"/deltaGen/"

deltas = delta_retrieval(delta_path)
for delta in deltas["dh_noise"]:
    # renders identity matrix of each delta
    # print(delta)
    render(groom_path, delta, delta)
for delta in deltas["dh_coil"]:
    # renders identity matrix of each delta
    render(groom_path, delta, delta)

render(groom_path, deltas["dh_exp_gScale"], deltas['dh_cutClamp'])
render(groom_path, deltas["dh_exp_gScale"], deltas['dh_cutPercent'])