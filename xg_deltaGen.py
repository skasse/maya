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
configFile = "delta_c000.toml"
xgPath = "/maya/base/scenes/base__head_coll.xgen"
maPath = "/maya/base/scenes/base.ma"
deltaPath = "maya/base_delta/scenes/deltaGen/"


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

def __load_config():
    """open config file with read + binary"""
    with open(sourcePath+configPath+configFile, 'rb') as f:
        config = tomli.load(f)
    return config


def prune(desc:list="", discard:list=["eye", "baby"]):
    """ with input list, remove discards """
    descp = [x for x in desc if not any(word in x.lower() for word in discard)]
    discards = [x for x in desc if any(word in x.lower() for word in discard)]
    print("retained:", descp), print("discarded:", discards)
    return descp


def file_reset(filename:str=""):
    with open(filename, 'w') as f:
        f.write("")
        f.close()


def clean_deltas():
    """removes all ../scenes/delta/ folders"""
    import shutil
    for groom in get_grooms(sourcePath):
        shutil.rmtree(deltaOutPath(groom))


def dh_coil_gen(groomName, count:list = "", radius:list = ""):
    """gets descriptions from groomName and outputs array of xgd from count/radius"""
    if isinstance(count, int):
        count = [count]
    if isinstance(radius, int):
        radius = [radius]
    palettes = prune(get_desc(groomName))
    permutations = list(product(*[count, radius]))
    for p in permutations:
        filename = deltaOutPath(groomName)+"dh_coil_{}c{}r.xgd".format(p[0], p[1])
        file_reset(filename)
        print(filename)
        for desc in palettes:
            with open(filename, 'a') as f:
                modifier = __load_config()["modifiers"]["dh_coil"][0]
                modifier = modifier.replace("<xgenDescName>", desc)
                modifier = modifier.replace("<count>", str(p[0]))
                modifier = modifier.replace("<radius>", str(p[1]))
                print(modifier)
                # f.write(modifier)
                

def dh_cutClamp_gen(groomName, cutLength:list = "", mask:float=1.0):
    """gets descriptions from groomName and outputs array of xgd from count/radius"""
    palettes = prune(get_desc(groomName))
    for c in cutLength:
        filename = deltaOutPath(groomName)+"dh_cutClamp_{}cmLength.xgd".format(c)
        file_reset(filename)
        print(filename)
        for desc in palettes:
            with open(filename, 'a') as f:
                modifier = __load_config()["modifiers"]["dh_cutClamp"][0]
                modifier = modifier.replace("<xgenDescName>", desc)
                modifier = modifier.replace("<cut_length>", str(c))
                f.write(modifier)  


def dh_noise_gen(groomName, frequency:list="", magnitude:list="", correlation:list=[.5]):
    """gets descriptions from groomName and outputs array of xgd from freq/mag"""
    palettes = prune(get_desc(groomName))
    for freq in frequency:
        for mag in magnitude:
            for corr in correlation:
                filename = deltaOutPath(groomName)+"dh_noise_{}freq_{}mag_{}corr.xgd".format(freq, mag, corr)
                file_reset(filename)
                print(filename)
                for desc in palettes:
                    with open(filename, 'a') as f:
                        modifier = __load_config()["modifiers"]["dh_noise"][0]
                        modifier = modifier.replace("<xgenDescName>", desc)
                        modifier = modifier.replace("<frequency>", str(freq))
                        modifier = modifier.replace("<magnitude>", str(mag))
                        modifier = modifier.replace("<correlation>", str(corr))
                        f.write(modifier)  


def dh_exp_gScale(groomName, gScale:list=""):
    """outputs expression for each desc in groom"""
    palettes = prune(get_desc(groomName))
    for scale in gScale:
        filename = deltaOutPath(groomName)+"dh_exp_gScale_{}.xgd".format(scale)
        file_reset(filename)
        print(filename)
        for desc in palettes:
            with open(filename, 'a') as f:
                modifier = __load_config()["modifiers"]["dh_exp_gScale"][0]
                modifier = modifier.replace("<xgenDescName>", desc)
                modifier = modifier.replace("<gScale>", str(scale))
                f.write(modifier)  


def dh_wind(groomName, 
    direction:list=[1.0, 0.0, 0.0],
    stiffness:list=[.1],
    constStrength:list=[2],
    gustStrength:list=[.5],
    shearStrength:list=[.1],
    seed:list=[13],
    ):
    """outputs xgen delta within variable ranges for each desc in groomName"""
    palettes = prune(get_desc(groomName))
    permutations = list(product(*[[direction],
        stiffness, constStrength, gustStrength, shearStrength, seed]))
    for p in permutations:
        filename = deltaOutPath(groomName)+"dh_wind_{}x{}y{}z__{}s_{}cs_{}gs_{}ss_{}s.xgd".format(p[0][0],p[0][1],p[0][2],
            p[1], p[2], p[3], p[4], p[5], )
        file_reset(filename)    
        for desc in palettes:
            with open(filename, 'a') as f:
                modifier = __load_config()["modifiers"]["dh_wind"][0]
                modifier = modifier.replace("<xgenDescName>", desc)
                modifier = modifier.replace("<direction>", str(p[0]))
                modifier = modifier.replace("<directionV>", str(p[0][0]))
                modifier = modifier.replace("<directionV>", str(p[0][1]))
                modifier = modifier.replace("<directionV>", str(p[0][2]))
                modifier = modifier.replace("<stiffness>", str(p[1]))
                modifier = modifier.replace("<constStrength>", str(p[2]))
                modifier = modifier.replace("<gustStrength>", str(p[3]))
                modifier = modifier.replace("<shearStrength>", str(p[4]))
                modifier = modifier.replace("<seed>", str(p[5]))
                f.write(modifier)  



### example usage

# groomName = get_grooms(sourcePath)
# namelist = ["SimonYuen", "WandaEdwards"]
# for groomName in namelist:
#     dh_wind(groomName, direction=[2, .2, 1], stiffness=[0.3, .6], constStrength=[2])

# for groomName in get_grooms(sourcePath):
#     expList = [
#         dh_exp_gScale(groomName, fit(.1, 5, 10, 1)),
#         # dh_noise_gen(groomName, fit(.1, 5, 10, 1), fit(1, 10, 5, 1)),
#         # dh_cutClamp_gen(groomName, fit(2, 10, 5, 1)),
#         # dh_coil_gen(groomName, fit(1,10,4,1), fit(.1,3,4,1)),
#         # dh_wind(groomName, direction=[2, .2, 1], stiffness=[0.3, .6], constStrength=[2])
#     ]

# dh_coil_gen("simonYuen", np.arange(.5, 2.1, .5), np.arange(0, 2.1, .5))
# dh_coil_gen("simonYuen", 1, 1)



