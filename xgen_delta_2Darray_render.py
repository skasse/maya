import maya.cmds as mc
import os
import xgenm as xge
import xgenm.xgGlobal as xgg
from datetime import datetime
from itertools import product
from natron_contactSheet import natron_write


def file_path(root_dir, groom_name:str = "", variant:str = "",):
    if variant:
        variant = "variants/{1}".format(variant)
    else:
        variant = "base" or "None"
    project_path = "{}/{}/maya/{}/".format(root_dir, groom_name, variant)
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
    mc.file(path, reference=True, mergeNamespacesOnClash=False, iv=True)


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
    

def img_output_dir(dx, dy):
    # output_suffix = "_".join([str(x) for x in (dx[0]+dx[-1]+dy[0]+dy[-1])])
    output_suffix = "_".join([dx[0],dx[-1],dy[0],dy[-1]])
    img_output_path = "{0}/images/{1}/".format(project_path,output_suffix)
    if not os.path.exists(img_output_path):
        os.mkdir(img_output_path)
        print("created dir:", img_output_path)
    return img_output_path


def get_deltas():
    """get deltas thru file dialogue. Returns choices"""
    deltas = mc.fileDialog2(cap="CHOOSE UR DELTAS", fm=4, dir = "{}".format(delta_path))
    ids = [x.split("/")[-1].replace(".xgd", "") for x in deltas]
    return deltas, ids


# ROOT DIRECTORY
groom_path = mc.fileDialog2(cap="CHOOSE UR GROOM", fm=1, dir="G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/")
project_path = "/".join(groom_path[0].split("/")[:-2])
delta_path = "/".join(groom_path[0].split("/")[:-1])+"/deltaGen/"
turntable_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/turntableQC/scenes/turntableQC_light.ma"
renderWidth = renderHeight = 2048
camera = "camera1"
startFrame = 1002
endFrame = 1002

dx = get_deltas()
dy = get_deltas()

pathcombos = list(product(*[dx[0], dy[0]]))
namecombos = list(product(*[dx[1], dy[1]]))

xgen_set_prj(project_path, project_path) # set project
render_path = img_output_dir(dx[1], dy[1])
print("creating render matrix from {0} and {1}".format(dx[1], dy[1]))
sequence_start = datetime.now()
print("begin!")
for path in enumerate(pathcombos, 0):
    img_path = "{0}delta.{1}".format(render_path, path[0]+1)
    print("image.{0}.txt: writing {1}".format(path[0]+1, namecombos[path[0]]))
    txt_path = "{0}delta.{1}.txt".format(render_path, path[0]+1)
    with open(txt_path, 'w') as f:
        f.write("{0}\n{1}".format(namecombos[path[0]][0], namecombos[path[0]][1]))
    file_open(groom_path) # open groom
    file_ref(turntable_path) # reference lighting Turntable
    apply_delta_from_paths("head_coll", [path[1][0], path[1][1]])
    mc.currentTime(1002, edit=True)
    mc.setAttr("defaultArnoldDriver.mergeAOVs", 1)
    mc.setAttr("defaultArnoldRenderOptions.renderDevice", 1) #enable GPU
    mc.setAttr("defaultRenderGlobals.imageFilePrefix", img_path, type="string")
    mc.setAttr("defaultRenderGlobals.animationRange", 0)
    mc.setAttr("defaultRenderGlobals.startFrame", startFrame)
    mc.setAttr("defaultRenderGlobals.endFrame", endFrame)
    mc.setAttr("defaultArnoldDriver.ai_translator", "png", type="string")
    mc.setAttr("defaultRenderGlobals.animation", 0)
    mc.setAttr("perspShape.renderable", 0)
    mc.setAttr("defaultRenderGlobals.putFrameBeforeExt", 1)
    mc.setAttr("defaultResolution.width", renderWidth)
    mc.setAttr("defaultResolution.height", renderHeight)
    mc.setAttr("defaultResolution.deviceAspectRatio", 1)
    image_start = datetime.now()
    print("rendering {0} out of {1}".format(path[0]+1, len(pathcombos)))
    print("rendering delta {}".format([d.split("/")[-1] for d in [path[1][0], path[1][1]]]))
    print("render starting @", image_start)
    mc.arnoldRender(w=renderWidth, h=renderHeight, seq="1002", b=False)#, cam=camera)
    image_end = datetime.now()
    print("render complete @", image_end)
    print("render time was", image_end - image_start)
    print("render output path = {}".format(img_path))
print("sequence complete:\ntotal render time was: {0}\navg render time was:{1}".format(
    datetime.now() - sequence_start, (datetime.now() - sequence_start)/len(pathcombos)))

natron_write(render_path, len(dx[1]), len(dy[1]))


