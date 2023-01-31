import maya.cmds as mc
import xgenm as xge
import xgenm.xgGlobal as xgg


sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
xgPath = "/maya/base/scenes/base__head_coll.xgen"
maPath = "/maya/base/scenes/base.ma"
deltaPath = "maya/base_delta/scenes/deltaGen/"

def xgd_import():
    """ IMPORT XGD """
    col = mc.ls("*_coll")[0]
    importPath = mc.fileDialog2(fm=4) #open multi files
    for path in importPath:
        xge.applyDelta(str(col), str(path))
    de = xgg.DescriptionEditor
    de.refresh("Full")


def xgd_export():
    """ EXPORT XGD """
    col = mc.ls("*_coll")[0]
    exportPath = mc.fileDialog2(fm=0)[0]
    xge.createDelta(str(col), str(exportPath))