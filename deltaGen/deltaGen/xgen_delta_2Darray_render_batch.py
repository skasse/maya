import maya.cmds as mc
import os, json
from xg_tools import *
from datetime import datetime, date
from itertools import product
import time
# from glob import glob
# import xgenm as xge
# import xgenm.xgGlobal as xgg


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
    render_path = img_output_dir(project_path, dx[1], dy[1])

    print(f'render path defined')

    #########

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
    
    print(f'json exported')

    with open(fr'{render_path}{json_file}',  "w") as outfile:
        print("writing json metadata to {}".format(render_path+json_file))
        json.dump(metadata, outfile)
        print("writing metadata complete")

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


def main():
    groom_path:list = mc.fileDialog2(cap="CHOOSE UR GROOM", fm=1, dir="G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/")
    # project_path = "/".join(groom_path[0].split("/")[:-2])
    delta_path = "/".join(groom_path[0].split("/")[:-1])+"/deltaGen/"

    deltas = delta_retrieval(delta_path, '_coll')
    for delta in deltas["dh_noise"]:
        # renders identity matrix of each delta
        render(groom_path, delta, delta)
    for delta in deltas["dh_coil"]:
        # renders identity matrix of each delta
        render(groom_path, delta, delta)

    render(groom_path, deltas["dh_exp_gScale"], deltas['dh_cutClamp'])
    render(groom_path, deltas["dh_exp_gScale"], deltas['dh_cutPercent'])


if __name__ == "__main__":
    main()