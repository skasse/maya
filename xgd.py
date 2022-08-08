import maya.cmds as mc
import xgenm as xge

### IMPORT XGD ###
def xgd_import():
    col = mc.ls("*_coll")[0]
    importPath = mc.fileDialog2(fm=4) #open multi files
    for path in importPath:
        xge.applyDelta(str(col), str(path))
    de = xgg.DescriptionEditor
    de.refresh("Full")

### EXPORT XGD ###
def xgd_export():
    col = mc.ls("*_coll")[0]
    exportPath = mc.fileDialog2(fm=0)[0]
    xge.createDelta(str(col), str(exportPath))