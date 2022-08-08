"""this reads toml data, xgd template and outputs to an xgd """

import tomli
import os
import numpy as np
from itertools import product
from xgd_parser_v20220708 import prune
from xgd_parser_v20220708 import get_desc
from xgd_parser_v20220708 import get_grooms
from glob import glob



# pathing
sourcePath = "G:/Shared drives/TriplegangersGroom_ext/Groom_INTERNAL/"
configPath = "0000_base_delta/template/"
configFile = "delta_c000.toml"
deltaPath = "maya/base_delta/scenes/deltaGen/"

# open config file with read + binary
def __load_config():
    with open(sourcePath+configPath+configFile, 'rb') as f:
        config = tomli.load(f)
    return config


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
                f.write(modifier)
                

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
    stiffness:list=[.3],
    constStrength:list=[2],
    gustStrength:list=[.5],
    shearStrength:list=[.1],
    seed:list=[1],
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


# groomName = get_grooms(sourcePath)
# namelist = ["SimonYuen", "WandaEdwards"]
# for groomName in namelist:
#     dh_wind(groomName, direction=[2, .2, 1], stiffness=[0.3, .6], constStrength=[2])

for groomName in get_grooms(sourcePath):
    expList = [
        dh_exp_gScale(groomName, fit(.1, 5, 10, 1)),
        dh_noise_gen(groomName, fit(.1, 5, 10, 1), fit(1, 10, 5, 1)),
        dh_cutClamp_gen(groomName, fit(2, 10, 5, 1)),
        dh_coil_gen(groomName, fit(1,10,4,1), fit(.1,3,4,1)),
        dh_wind(groomName, direction=[2, .2, 1], stiffness=[0.3, .6], constStrength=[2])
    ]




