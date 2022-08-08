import maya.standalone as ms
import maya.cmds as mc
import os
import xgenm as xge
import xgenm.xgGlobal as xgg
from datetime import datetime
import toml

# establish project and file paths
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


def legacy2Igs(collection):
    '''convert all xgen legacy groom to igs
    select_collection > Generate > Convert to Interactive Groom
    '''
    mc.select(collection)
    return [mc.listRelatives(i,p=True)[0] for i in mc.xgmGroomConvert(prefix="")]


def refresh_ui():
    #Get the description editor first.
    de = xgg.DescriptionEditor
    #Do a full UI refresh
    de.refresh("Full")


def __apply_delta_by_id(root_dir, delta_dir, delta_id):
    if type(delta_id)==int or type(delta_id)==str:
        delta_path = "{0}/{1}/delta{2}.xgd".format(root_dir, delta_dir, str(delta_id))
        xge.applyDelta("head_coll", delta_path)
        print(delta_path)
    elif type(delta_id) == list:
        for i in delta_id:
            delta_path = "{0}/{1}/delta{2}.xgd".format(root_dir, delta_dir, i)
            xge.applyDelta("head_coll", delta_path)
            print(delta_path)
    else:
        print("broken??", type(delta_id))
    de = xgg.DescriptionEditor
    de.refresh("Full")


def apply_delta_from_paths(collection, paths:list):
    for path in paths:
        # print(path)
        xge.applyDelta(collection, path)
    de = xgg.DescriptionEditor
    de.refresh("Full")
    

def img_output_dir(dx, dy):
    # output_suffix = "_".join([str(x) for x in (dx[0]+dx[-1]+dy[0]+dy[-1])])
    output_suffix = "_".join([dx[0],dx[-1],dy[0],dy[-1]])
    img_output_path = "{0}/images/{1}".format(project_path,output_suffix)
    if not os.path.exists(img_output_path):
        os.mkdir(img_output_path)
        print("created dir:", img_output_path)
    return img_output_path


def get_deltas():
    """get deltas thru file dialogue. Returns choices"""
    deltas = mc.fileDialog2(cap="CHOOSE UR DELTAS", fm=4, dir = "{}".format(delta_path))
    ids = [x.split("/")[-1].replace(".xgd", "") for x in deltas]
    return deltas, ids


def __load_config(path):
    with open(path, 'rb') as f:
        config = tomli.load(f)
    return config


# ROOT DIRECTORY
groom_path = mc.fileDialog2(cap="CHOOSE UR GROOM", fm=1, dir="G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/")
project_path = "/".join(groom_path[0].split("/")[:-2])
delta_path = "/".join(groom_path[0].split("/")[:-1])+"/deltaGen/"
# groom_name = "SimonYuen"
variant = "None"
# project_path = file_path(root_dir, groom_name)[0]
# full_path = file_path(root_dir, groom_name)[1]
renderSettings = __load_config("G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/0000_base_delta/template/renderSettings.toml")

turntable_path = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/turntableQC/scenes/turntableQC_light.ma"
renderWidth = renderHeight = 1000
camera = "camera1"
startFrame = 1002
endFrame = 1002

dx = get_deltas()
dy = get_deltas()

# set project
xgen_set_prj(project_path, project_path)
render_path = img_output_dir(dx[1], dy[1])
print("creating render matrix from {0} and {1}".format(dx[1], dy[1]))
sequence_start = datetime.now()
print("begin!")
i = 0 #dx counter
c = 1 #image counter
for x in dx[0]:
    j=0 #dy counter
    for y in dy[0]:
        img_path = "{0}/delta.{1}".format(render_path, c)
        print(img_path)
        file_open(groom_path) #open turntable
        file_ref(turntable_path) #reference groom
        apply_delta_from_paths("head_coll", [dx[0][i], dy[0][j]])
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
        print("rendering {0} out of {1}".format(c, len(dx[0])*len(dy[0])))
        print("rendering delta {}".format([d.split("/")[-1] for d in [x,y]]))
        print("render starting @", image_start)
        mc.arnoldRender(w=renderWidth, h=renderHeight, seq="1002", b=False)#, cam=camera)
        image_end = datetime.now()
        print("render complete @", image_end)
        print("render time was", image_end - image_start)
        print("render output path = {}".format(img_path))
        c+=1
        j+=1
    i+=1
print("sequence complete: \n total render time was: {}".format(datetime.now() - sequence_start))

