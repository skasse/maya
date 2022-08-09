import os
import re
from glob import glob
# import maya.cmds as mc
import xgenm as xge

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


def dc_extract(groomName):
    """parses ma file looking for collections and descriptions.  returns dictionary"""
    sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/{}/maya/base/scenes/".format(groomName)
    xgPath = sourcePath+"/base__head.xgen"
    maPath = sourcePath+"/base.ma"
    descPattern = r'[A-Za-z]*Desc\b'
    collPattern = r'base__.*.xgen'

    def descOut(filename,  pattern):
        s = None
        with open(filename, 'r') as f:
            s = f.read()#.splitlines()
        return list(set(re.findall(pattern, s)))

    collections = {}
    if os.path.exists(maPath):
        for colls in descOut(maPath, collPattern):
            collections[colls] = descOut(sourcePath+colls, descPattern)
        return collections


def gather_palettes(paths:list="", discard:list=""):
    """ iterate thru all grooms and create sets of coll(s) and desc(s) and discard(s)"""
    colls = set()
    descs = set()
    for groom in paths:
        palettes = dc_extract(groom)
        if palettes:
            # print(palettes)
            for key in palettes:
                # print(palettes.keys())
                colls.add(key)
                for items in palettes[key]:
                    descs.add(items)
    descp = [x for x in descs if not any(word in x for word in discard)]
    discards = [x for x in descs if any(word in x for word in discard)]
    return colls, descp, discards


def prune(desc:list="", discard:list=["eye", "baby"]):
    """ with input list, remove discards """
    descp = [x for x in desc if not any(word in x.lower() for word in discard)]
    discards = [x for x in desc if any(word in x.lower() for word in discard)]
    print("retained:", descp), print("discarded:", discards)
    return descp


def get_grooms(path:str=sourcePath, name:str="**"):
    """ get grooms from source path.  default name = '**' """
    return [x.replace(os.sep, '/').split('/')[-1] for x in glob(path+name)]


def fit(min, max, length, decimals):
    step = (max - min)/length
    x = [round(x, decimals) for x in np.arange(min, max, step)]
    return(x)

def deltaOutPath(groomName):
    outputPath = "{0}{1}/{2}".format(sourcePath, groomName, deltaPath)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        print("created dir:", outputPath)
    return outputPath

def get_desc(groomName, ):
    xgenPath =  "{}{}{}".format(sourcePath, groomName, xgPath)
    desc_names=[]
    xg_file =  open(xgenPath, 'r')
    lines = xg_file.readlines()
    xg_file.close()
    for i in range(len(lines)):
        ck = lines[i]
        if ck.startswith("Description"):
            desc_names.append(lines[i+1].rpartition("\t")[2].rstrip("\n"))
    return desc_names