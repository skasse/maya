'''new test of git branching.  lets see how we do!'''


"""this reads toml data, xgd template and outputs to an xgd for given groomnames"""
import os
import re
import numpy as np
from glob import glob
import tomli
from itertools import product


# pathing
sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
configPath = "0000_base_delta/template/"
xgd_configFile = "delta_c000.toml"
xgPath = "/maya/base/scenes/base__head_coll_coll.xgen" # head_coll collections only
maPath = "/maya/base/scenes/base.ma"
deltaPath = "maya/base_delta/scenes/deltaGen/"


def __dc_extract(groomName) -> dict:
    """
    parses maya .ma file looking for collections and descriptions
    returns {"collection": "desc1", "desc2", "etc"}"
    """
    sourcePath = f"G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/{groomName}/maya/base/scenes/"
    maPath = sourcePath+"/base.ma"
    descPattern = r'[A-Za-z]*Desc\b'
    collPattern = r'base__.*.xgen'

    def descOut(filename,  pattern) -> list:
        s = None
        with open(filename, 'r') as f:
            s = f.read()
        return list(set(re.findall(pattern, s)))

    collections = {}
    if os.path.exists(maPath):
        for colls in descOut(maPath, collPattern):
            collections[colls.split("__")[-1].rstrip('.xgen')] = descOut(sourcePath+colls, descPattern)
        return collections

def prune(desc:list="", discard:list=["eye", "baby"]):
    """ with input list, remove discards """
    descp = [x for x in desc if not any(word in x.lower() for word in discard)]
    discards = [x for x in desc if any(word in x.lower() for word in discard)]
    # print("retained:", descp), print("discarded:", discards)
    return descp

def get_grooms(path:str=sourcePath, name:str="**"):
    """ get grooms from source path.  default name = '**' """
    print(f'search path: {path}, name filters: {name}')
    exclude = ["turntableQC", "0000_base_delta", "image_DB"]
    groomList = [x.replace(os.sep, '/').split('/')[-1] for x in glob(path+name)]
    groomList = [x for x in groomList if x not in exclude]
    return groomList

def _get_desc(groomName):
    '''
    returns descriptions from .xgen file
    '''
    xgenPath = f'{sourcePath}{groomName}{xgPath}'
    desc_names=[]
    xg_file =  open(xgenPath, 'r')
    lines = xg_file.readlines()
    xg_file.close()
    for i in range(len(lines)):
        ck = lines[i]
        if ck.startswith("Description"):
            desc_names.append(lines[i+1].rpartition("\t")[2].rstrip("\n"))
    return desc_names

def fit(min, max, length, decimals):
    step = (max - min)/length
    x = [round(x, decimals) for x in np.arange(min, max, step)]
    return(x)

def deltaOutPath(groomName):
    """creates delta output path if its doesnt exist"""
    outputPath = "{0}{1}/{2}".format(sourcePath, groomName, deltaPath)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
        print("created dir:", outputPath)
    return outputPath

def __load_config():
    """open config file with read + binary"""
    with open(sourcePath+configPath+xgd_configFile, 'rb') as f:
        config = tomli.load(f)
    return config

def file_reset(filename:str=""):
    with open(filename, 'w') as f:
        f.write("")
        f.close()

def clean_deltas(groomName:str = '**'):
    """removes all ../scenes/delta/ folders"""
    import shutil
    for groom in get_grooms(sourcePath, groomName):
        print(groom)
        shutil.rmtree(deltaOutPath(groom))
    print("clean complete")

def deltaGen(groomName:str, collection:list[str], modifier:str, **kwargs):
    """
    take groomName, collection, modifier, and kwargs as input; XGen xgd file as output

    available modifiers:
    dh_coil: [count, radius], mask
    dh_cutClamp: [cutLength], mask
    dh_cutPercent: [percent], mask
    dh_noiseGen: [frequency, magnitude, correlation], mask
    dh_exp_gScale: [gScale]
    dh_wind: [direction, stiffness, constStrength, ]
    """

    #  get descriptions from groom
    for coll in collection:
        palettes = prune(__dc_extract(groomName)[coll])

        x = [x for x in kwargs] # kwargs list
        p = product(*[kwargs.get(x) for x in kwargs]) # cartesian product of kwarg values

        for a in p:
            xpzip = list(zip(x, a))
            name_list = []
            for w in xpzip:
                name_list.extend([w[0][:1],w[1]])
            filename  = deltaOutPath(groomName)+f'{groomName}__{coll}__{modifier}__{"_".join([str(x) for x in name_list])}.xgd'
            file_reset(filename)
            for desc in palettes:
                with open(filename, 'a') as f:
                    workfile = __load_config()["modifiers"][f'{modifier}'][0]
                    workfile = workfile.replace("<xgenDescName>", desc)
                    for w in xpzip:
                        workfile = workfile.replace(f'<{w[0]}>', str(w[1]))
                        # print(f'replacing <{w[0]}> with {str(w[1])}')
                    f.write(workfile)