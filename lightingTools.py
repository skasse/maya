# Lighting Tools Created by Scott Kassekert
# VER201904051033


import maya.cmds as mc
import sys
sys.path.append('/net/homes/skasseke/python/maya')


# ============================================================================ 
def importTest():
    print("HEY! Nice work")
importTest()


# ============================================================================


def moveToOrigin(node):
    """moves node to origin"""
    bb = mc.xform(node, q=True, bb=True)
    def avg(a, b):
        return (a+b)/2
    t=[avg(bb[0], bb[1]),
       avg(bb[2], bb[3]),
       avg(bb[4], bb[5])]

    mc.xform(node, t=[-avg(bb[0], bb[3]),
                      -avg(bb[1], bb[4]),
                      -avg(bb[2], bb[5])],
                      a=True)

def multiUVxfer():
    """transfers uv's from first selection to all remaining"""
    nodes = mc.ls(sl=True)
    master = nodes[0]
    slaves = nodes[1:]
    for slave in slaves:
        mc.transferAttributes(master, slave,
                            transferPositions=0,
                            transferNormals=0,
                            transferUVs=2,
                            transferColors=0,
                            sampleSpace=4,
                            sourceUvSpace="map1",
                            targetUvSpace="map1",
                            searchMethod=0,
                            flipUVs=0,
                            colorBorders=1
                            )


# ============================================================================


def copyRigXForms(*args):
    """copys transforms from rig A to rig B"""
    def setxforms(node, xforms):
        mc.xform(node, t=xforms[0], ro=xforms[1], s=xforms[2])
        
    def getxforms(node):
        tv = mc.xform(node, q=True, t=True, a=True)
        rv = mc.xform(node, q=True, ro=True, a=True)
        sv = mc.xform(node, q=True, s=True, r=True)
        return(tv, rv, sv)
        
    if args and args == 2:
        selection = args
    else:
        selection = mc.ls(sl=True)
    children0 = mc.listRelatives(selection[0],
                                 c=True, ad=True, type='transform')
    children1 = mc.listRelatives(selection[1],
                                 c=True, ad=True, type='transform')
    for a, b in zip(children0, children1):
        setxforms(b, getxforms(a))


# ============================================================================


def extraAttrCopy():
    '''copies and transfers extra attributes
    from first selection to remaining selections'''
    nodes = mc.ls(sl=True)
    if nodes > 1:
        for attr in mc.listAttr(nodes[0], ud=True)[:-1]:
            for node in nodes[1:]:
                mc.setAttr("{}.{}".format(node, attr),
                           mc.getAttr("{}.{}".format(nodes[0], attr)))
    else:
        print("must select at least two nodes")


# ============================================================================


def createDictSets(args):
    '''createSets(setdict)'''
    for groups in args.keys():
        for set in args[groups]:
            if not mc.objExists(set):
                mc.sets(name=set, empty=True)
            mc.sets(args[groups][set], add=set)
            print("added {0} to {1}".format(args[groups][set], set))


# ============================================================================


def setLightLinks(*args):
    """setLightLink() or setLightLink(lightlinksdict)"""
    def setlinks():
        illum_objects = mc.lightlink(light=lights, q=True, t=True)
        mc.lightlink(light=lights, object=illum_objects, b=True)
        mc.lightlink(light=lights, object=geos, m=True)
        print("linked {} to {}".format(lights, geos))
    if not args:
        nodes = mc.ls(sl=True)
        for each in nodes:
            if "light_set" in each:
                lights = mc.sets(each, q=True)
            if "geo_set" in each:
                geos = mc.sets(each, q=True)
        setlinks()
    else:
        args = args[0]
        for key in args.keys():
            lights, geos = mc.sets(key, q=True), mc.sets(args[key], q=True)
            setlinks()


# ============================================================================
# rigging
# ============================================================================


def attrConnect(outattr, inattr, *args):
    """connects attributes of first selected node to remaining selection.
    eg. attrConnect('output', 'visibility')"""
    arg1 = mc.ls(sl=True)[0]
    args = mc.ls(sl=True)[1:]
    for node in args:
        mc.connectAttr('{0}.{1}'.format(arg1, outattr),
                       '{0}.{1}'.format(node, inattr), force=True)
        print('connected {0}.{1} to {2}.{3}'.format(arg1, outattr, node, inattr))


def lightCenterConstraint():
    mc.ls('*:lightCenter_LOC')
    mc.parentConstraint('*:lightCenter_LOC', mc.ls(sl=True))


def camDofRig():
    """creates locators and constraints to auto manage vray DOF"""
    locatorList = [
        'focusPoint_locator',
        'camera_locator',
    ]

    for each in locatorList:
        newTransform = mc.createNode('transform', name=each)
        mc.createNode('locator', name='{}Shape'.format(each), p=newTransform)

    mc.createNode('distanceBetween', name='focalDistance_node')

    mc.connectAttr('focusPoint_locator.worldPosition[0]',
                   'focalDistance_node.point1')
    mc.connectAttr('camera_locator.worldPosition[0]',
                   'focalDistance_node.point2')
    mc.connectAttr('focalDistance_node.distance',
                   'vraySettings.cam_dofFocalDist')
    mc.parentConstraint('*:render_CAM', 'camera_locator')
    mc.setAttr('vraySettings.cam_dofOn', 1)


# ============================================================================
# pass management
# ============================================================================


def createRenderpass(name):
    '''creates renderpasses with presets'''
    pass_name = name + "_PAS"
    mc.createNode('cmRenderPass', name=pass_name + "Shape", parent=pass_name)
    mc.setAttr('{}.postSwitchPython'.format(pass_name),
               "exec mc.getAttr('Globals_PASShape.postSwitchPython')",
               type="string")
    return pass_name


def createPalette(palette_name):
    '''create palette'''
    palette_name = palette_name + "_PAL"
    mc.createNode('cmPalette',
                  name=palette_name + "Shape", parent=palette_name)
    return palette_name


def createPass(arg1, arg2, *args):
    """createPass("Bty", "Reset", "Membership")"""
    mc.parent(createPalette(arg2), createRenderpass(arg1))
    if args:
        for arg in args:
            mc.parent(createPalette(arg), arg1 + "_PAS")


def createRP():
    """create framestore renderpass based on selected maya renderlayer"""
    #get name of current renderlayer
    active_renderlayer = mc.editRenderLayerGlobals(q=True, crl=True)
    render_pass = active_renderlayer+"_PAS"
    render_palette = active_renderlayer+"_PAL"
    #create renderpassb
    mc.createNode("cmRenderPass", parent=render_pass, name=render_pass+"Shape")
    #create default palette
    mc.createNode("cmPalette", parent=render_palette, name=render_palette+"Shape")
    #parent palette under renderPass
    mc.parent(render_palette, render_pass)
    #add pass switch attr
    mc.setAttr(render_pass+".preSwitchPython", 
               "import maya.cmds as mc\nmc.editRenderLayerGlobals(crl='{}')".format(active_renderlayer), 
               type="string")


# ============================================================================
# render globals
# ============================================================================


def setRenderGlobals(overrides, **kwargs):
    """sets vray render variables with key:value pairs.
    e.g. {"giOn":0} or setRenderGlobals(defaults)"""
    if overrides:
        for key, value in overrides.items():
            mc.setAttr('vraySettings.{}'.format(key), value)
            print('vraySettings.{}'.format(key), value)
    else:
        print("No overrides entered!")


# ============================================================================
# render Elements
# ============================================================================


def reToggle(value, *args):
    """toggles render elements on or off based on keyworded wildcards"""
    for each in mc.ls(args, exactType='VRayRenderElement', r=True):
        mc.setAttr('{}.enabled'.format(each), value)


# ============================================================================
# misc tools
# ============================================================================


def visTog(value, *args):
    for arg in args:
        for each in mc.ls("*{}*".format(arg)):
            mc.setAttr(each+".visibility", value)


def allVisOff(input):
    """hide all transforms without shapes"""
    for each in input:
        child = mc.listRelatives(each, type="transform")
        if child:
            if len(child) > 1:
                mc.setAttr(each+".visibility", 0)
                allVisOff(child)
            if len(child) == 1 and mc.objectType(child) != "mesh":
                mc.setAttr(each+".visibility", 0)


# hide all transforms
for each in mc.ls(transforms=True):
    mc.setAttr(each+".visibility", 0)


# show all transforms
for each in mc.ls(transforms=True):
    if each == "root" or each == "discard":
        continue
    mc.setAttr(each+".visibility", 1)


def tformVisToggle(value, input):
    ''' toggle visibility on all inputs types excluding shapes '''
    for each in input:
        child = mc.listRelatives(each)
        if child:
            if len(child) > 1:
                mc.setAttr(each+".visibility", value)
                tformVisToggle(value, child)
            elif len(child) == 1 and mc.objectType(child) == "mesh":
                continue           
            elif len(child) == 1 and mc.objectType(child) != "mesh":
                mc.setAttr(each+".visibility", value)
                
tformVisToggle(1, mc.ls(type="transform"))
tformVisToggle(0, mc.ls(type="transform"))


# ============================================================================


def addToSelfSet(input):
    if mc.objExists(input+"_set") == False:
        mc.sets(name=input+"_set", empty=True)
    mc.sets(mc.ls("*_{}*".format(input)), add=input+"_set")

def addToSet(set, *args):
    if mc.objExists(set+"_set") == False:
        mc.sets(name=set+"_set", empty=True)
    mc.sets(args, add=set+"_set")

def removeFromSet(set, args):
    if mc.objExists(set+"_set") == False:
        pass
    else:
        mc.sets(args, remove=set+"_set")


# ============================================================================


def renamer(keyword, namechange):
    nodes = mc.ls("*{}*".format(keyword))
    nodes = [x for x in nodes if mc.objectType(x) != "mesh"]
    for node in nodes:
        oldname = node
        newname = oldname.replace(keyword, namechange)
        mc.rename(oldname, newname)
        print("renamed {0} to {1}".format(oldname, newname))


def renamerAdd(keyword, adder):
    base = mc.ls("{}".format(keyword))
    for each in base:
        selector = each.replace(keyword, "")
        head = selector.split("_")[:-1]
        tail = selector.split("_")[-1:]
        newName = "_".join(head+[adder]+tail)
        mc.rename(selector, newName)


# conditional renaming based on groups
def conditionalRenamer(keyword, conditional):
    parents = mc.listRelatives(mc.ls("*{}*".format(keyword)), p=True)
    base = []
    for each in parents:
    #    print("".join(mc.listRelatives(each, c=True)))
        if conditional not in "".join(mc.listRelatives(each, c=True)):
            base.append(each)
    for each in base:
        for child in mc.listRelatives(each):
            if "Base" in child:  # should this be keyword instead?
                oldname = child
                newname = child.replace("_Base", "")
                mc.rename(child, newname)
                print(child)


def toCamelCase(input):
    nodename = input.split("_")
    tail = []
    for each in nodename[1:]:
        print(each)
        if len(each) == 0:
            continue
        if len(each) > 1:
            tail.append(each[0].upper()+each[1:].lower())
        else:
            tail.append(each[0].upper())
    newname = nodename[0].lower()+"".join(tail)
    return newname


def removeIndex(keyword, index):
    top_node = "model_GRP"
    for node in mc.listRelatives(top_node, ad=True, type="transform"):
        if keyword in node:
            nodename = node.split("_")
            keyword_index = nodename.index(keyword)
            keyword_tail = nodename[keyword_index+1]
            if len(nodename) - keyword_index <= 3:
                newname = node.replace(keyword+"_", "")
            else:
                newname = node.replace(keyword+"_"+keyword_tail, "")
            mc.rename(node, newname)


# ============================================================================


def isGroup(node):
    """determines if node is a group"""
    childs = mc.listRelatives(node, children=True)
    if childs:
        for child in childs:
            print(mc.nodeType(child))
            if mc.nodeType(child) != "transform":
                return False
    return True


def addNodeTag(top_node):
    """adds GRP and GEP tags to nodes"""
    for nodes in mc.listRelatives(top_node, ad=True, type="transform"):
        if isGroup(nodes) == True:
            if "GRP" in nodes:
                continue
            else:
                mc.rename(nodes, nodes+"_GRP")
        elif isGroup(nodes) == False:
            if "GEP" in nodes:
                continue
            else:
                mc.rename(nodes, nodes+"_GEP")


# =================================================================================
# MANIPULATION FROM SPREADSHEETS
# =================================================================================


def importSpreadsheet(filepath):
    import yaml
    # filepath = "/net/homes/skasseke/rpo_codes.yaml"
    with open(filepath, 'r') as f:
        yaml_doc = ''.join(f.readlines()).replace("\t", " ")
    return yaml.load(yaml_doc)


def discardFromSpreadsheet(trimlevel):
    trims = ["SLE", "SLEV", "SLT"]
    if not mc.objExists("discard_grp"):
        mc.createNode("transform", name="discard_grp")
    rpo_codes = importSpreadsheet("/net/homes/skasseke/rpo_codes.yaml")
    for k,v in rpo_codes.items():
        for node in mc.ls("*{}*".format(k), type="transform"):
            if v[trims.index(trimlevel)] == 0:
                try: mc.parent(node, "discard_grp")
                except: pass

    print("complete")

SLE = {
    "code" : "3SA",
    "Length" : "DC"
    }
SLEV = {
    "code" : "4SB",
    "Length" : "DC"
    }
SLT = {
    "code" : "4SA",
    "Length" : "CC"
    }

trimlevel = SLT
for node in mc.listRelatives("model_GRP", ad=True, type="transform"):
    if isGroup(node):
        attribute = "BodyStyleTrim"
        object = "{0}.{1}".format(node, attribute)
        if mc.objExists(object):
            if trimlevel["code"] not in mc.getAttr(object):
                try: mc.parent(node, "discard_grp")
                except: pass
        if "_DC" in node or "_CC" in node:
            if "_DC" in node and "_CC" in node:
                continue
            if trimlevel["Length"] not in node:
                try: mc.parent(node, "discard_grp")
                except: pass
        if trimlevel == SLT:
            for node in mc.ls("*CC_SHORT*"):
                try: mc.parent(node, "discard_grp")
                except: pass
trimlevel == SLT

for node in mc.ls("*CC_SHORT*"):
    try: mc.parent(node, "discard_grp")
    except: pass


# =================================================================================
# Clean UP
# =================================================================================

renamer("_Modeling_Geo_", "Modeling_Geo_")
renamer("CC_Short", "CC_SHORT")
renamer("_EC_", "_DC_")

sg_list = mc.ls("*", type="shadingEngine")
for sg in sg_list:
    matName = sg.replace("SG", "")
    matNodes = mc.ls("{}*".format(matName), type="transform")
    for node in matNodes:
        renamer(matName, toCamelCase(matName))

discardFromSpreadsheet("SLEV")

mc.xform("model_GRP",cp=1)
bb = mc.xform("model_GRP", q=True, bb=True)
def avg(a, b):
    return (a+b)/2
t=[avg(bb[0], bb[1]), avg(bb[2], bb[3]), avg(bb[4], bb[5])]
mc.xform("model_GRP", t=[-avg(bb[0], bb[3]), -avg(bb[1], bb[4]), -avg(bb[2], bb[5])], a=True)
mc.makeIdentity("model_GRP", a=True)


# =================================================================================
# 
# =================================================================================

def trimPicker(trimlevel):
    visTog(0, "root")
    for each in mc.ls(transforms=True):
        if each == "root" or each == "discard":
            continue
        mc.setAttr(each+".visibility", 1)
    toggleFromSpreadsheet(trimlevel)
    visTog(1, "root")

trimPicker("SLE2")


# ============================================================================

def isDuplicate(node):
    if len(mc.ls(node)) > 1:
        return True


def dupPadding(nodes):
    index = 0
    for name in nodes:
        newname = name.split("|")[-1].split("_")
        head = newname[:-2]
        tail = newname[-1]
        index += 1
        parent = mc.listRelatives(name, parent=True)
        newname = "_".join(head)+"_{:03d}_".format(index)+tail
        while mc.objExists(newname) == True:
            index += 1
            newname = "_".join(head)+"_{:03d}_".format(index)+tail
        mc.rename(name, newname)
        print("renamed {0} to {1}".format(name, newname))


def findDuplicates(node):
    count = 0
    children = mc.listRelatives(node, ad=True, type="transform")
    for each in children:
        if mc.objExists(each):
            if isDuplicate(each):
                count += 1
                dup_list = mc.ls(each)
                dupPadding(dup_list)
    print("found {} duplicates".format(count))


findDuplicates("model_GRP")


# ============================================================================
# Naming from applied Shading Groups
# 201904041700
# =================================================================================
'''
save as renameFromShadingGroup.py in scripts folder
use the two lines below for your shelf button

import renameFromShadingGroup as rfsg
reload(rfsg)
'''

import maya.cmds as mc

def getSG():
    '''Returns all Shading Groups with a 'MTLSG' tag'''
    output = []
    list = mc.ls(type="shadingEngine")
    for each in list:
        if "_MTLSG" in each:
            output.append(each)
    return output

def getMtl(input):
    '''Returns mtls children to input Shading Group'''
    connections = mc.listConnections(input)
    for connection in connections:
        if "_MTL" in connection:
            return connection

def getShadedNodes(input):
    '''Returns all nodes connected to input'''
    return mc.listConnections(input, type="shape")

def renameFromSG():
    sgDict = {}
    for SG in getSG():
        if getMtl(SG):
            sgDict = "{}_nodes".format(SG)
            sgDict = {
                "matName": getMtl(SG),
                "sgName": "{}SG".format(getMtl(SG)),
                "nodes": getShadedNodes(SG)
                }
            for node in sgDict["nodes"]:
                if node.split("_")[0] != sgDict["matName"].split("_")[0]:
                    newname = "{}_{}".format(sgDict["matName"].split("_")[0], node)
                    mc.rename(node, newname)
                    print("renamed {} to {}".format(node, newname))

renameFromSG()

# END SCRIPT


# =================================================================================
# create and assign mtl from named shapes
# 201904041700
# =================================================================================

'''
save as createMtlAssignFromNamed.py in scripts folder
use the two lines below for your shelf button

import createMtlAssignFromNamed as cmafn
reload(cmafn)
'''

# BEGIN SCRIPT

import maya.cmds as mc
import random

def getShapes(input):
    return mc.ls(input, type="mesh")

def getMtlName(input):
    return input.split(":")[-1].split("_")[0]

def randColor(index):
    colors = ["r", "g", "b"]
    i=random.randint(1,1000)
    outColor = []
    for color in colors:
        i+=1
        random.seed(index*1000+i)

        outColor.append(random.random())
    return outColor

def searchInput():
    try:
        input = raw_input("namespace to search?")
    except EOFError:
        print("\nyou didnt type anything...")
    else:
        print("\nyou're searching " + input)
        return input

def createMtlList(input):
    mtl_list = []
    search_input = mc.ls(input+"*", type="mesh", recursive=True)
    if len(search_input) < 1:
        print "That namespace doesn't have any shapes"
        return 0
    else:
        for each in getShapes(search_input):
            if getMtlName(each) not in mtl_list:
                mtl_list.append(getMtlName(each))
        return mtl_list

def shaderCreate():
    mtl_list = createMtlList(searchInput())
    if mtl_list == 0:
        print "no materials to create"
    else:
        for each in mtl_list :
            matName = each+"_MTL"
            sgName = matName+"SG"
       
            #create mtls
            if not mc.objExists(sgName):
                mc.sets(name=sgName, renderable=True, noSurfaceShader=True,  empty=True)
            if not mc.objExists(matName):
                mc.shadingNode("blinn", name=matName, asShader=True)
                mc.connectAttr("{}.outColor".format(matName), "{}.surfaceShader".format(sgName))
       
            #assign random baseColor
            index = mtl_list.index(each)
            mc.setAttr("{}.color".format(matName), randColor(index)[0], randColor(index)[1], randColor(index)[2])

       
            #assign materials
            nodes = mc.ls("*{}_*".format(each), type="shape", recursive=True)
            print(nodes)
            mc.sets(nodes, fe=sgName)

shaderCreate()

# END OF SCRIPT


# =================================================================================
# get os paths and rebuild stuff
# 201906061051
# =================================================================================

import os
PROJECT = os.environ["PL_DIVISION"]
DRIVE = os.environ["PL_SHOW"]
project_path = os.path.join('/job',DRIVE,PROJECT)

full_path = "/job/comms/corona_4001603/pv010/pv010_0000/work/lighting/lighting/maya/scenes/pv010_0000_lighting_default_v003.mb"
file_name = os.path.basename(full_path)
file_split = file_name.split("_")
sequence = file_split[0]
shot = file_split[1]
task = file_split[2]
stream = file_split[3]
#full_shot_name = file_split[0] + "_" + file_split[1]
rebuild_path = os.path.join(project_path,"{0}/{1}/work/{2}/{2}/maya/scenes".format(sequence, sequence+"_"+shot, task))


# END OF SCRIPT

# =================================================================================
# create vray mtl and connections from existing legacy shader
# 201906061051
# =================================================================================

import maya.cmds as mc

node = mc.ls(sl=1)
mtlName = node[0]+"_MTL"
sgName = mtlName+"SG"
mc.sets(name=sgName, renderable=True, noSurfaceShader=True,  empty=True)
mc.shadingNode("VRayMtl", name=mtlName, asShader=True)
mc.connectAttr("{}.outColor".format(mtlName), "{}.surfaceShader".format(sgName))
connections = mc.listConnections(node)

def recursion(connections):
    if len(connections) > 0:
        if mc.objectType(connections[0]) == "file":
            print "{} is a file".format(connections[0])
            connectType = mc.listConnections(connections[0], p=1, s=0)[-1].split(".")[-1]
            if connectType == "color":
                print "color"
                mc.connectAttr("{}.outColor".format(connections[0]), "{}.diffuseColor".format(mtlName))
            if connectType == "bumpValue":
                print "bump"
                mc.connectAttr("{}.outColor".format(connections[0]), "{}.bumpMap".format(mtlName))
            print "\n"
            
        if mc.objectType(connections[0]) == "bump2d":
            print "{} is a bump".format(connections[0])
            recursion(mc.listConnections(connections[0]))
        else:
            recursion(connections[1:])
    else:
        print "done"
recursion(connections)

# =================================================================================
# sets default attributes on textures in TEXTURE_SEL
# 201908221122
# =================================================================================

import maya.cmds as mc

if mc.objExists("TEXTURE_SEL"):
    textures = [tex for tex in mc.sets("TEXTURE_SEL", q=1) if mc.nodeType(tex)=="file"]
    for name in textures:
        filename = mc.getAttr("{}.fileTextureName".format(name))
        mc.setAttr("{}.alphaIsLuminance".format(name), 1)
        mc.setAttr("{}.defaultColorR".format(name), 0)
        mc.setAttr("{}.defaultColorG".format(name), 0)
        mc.setAttr("{}.defaultColorB".format(name), 0)
        if "sRGB" in filename:
            mc.setAttr("{}.colorSpace".format(name), "sRGB", type="string")


def shaderCreate(input_list):
    for each in input_list:
        matName = each.split("_")[0]+"_MTL"
        sgName = matName+"SG"
    
        #create mtls
        if not mc.objExists(sgName):
            mc.sets(name=sgName, renderable=True, noSurfaceShader=True,  empty=True)
        if not mc.objExists(matName):
            mc.shadingNode("VRayMtl", name=matName, asShader=True)
            mc.connectAttr("{}.outColor".format(matName), "{}.surfaceShader".format(sgName))
        if each.split("_")[3] == "COL":
            mc.connectAttr("{}.outColor".format(each), "{}.color".format(matName), force=True)
        if each.split("_")[3] == "IOR":
            remapValue = mc.shadingNode("remapValue", asUtility=True)
            mc.setAttr("{}.outputMin".format(remapValue), 2)    
            mc.connectAttr("{}.outAlpha".format(each), "{}.inputValue".format(remapValue), force=True)
            mc.connectAttr("{}.outValue".format(remapValue), "{}.refractionIOR".format(matName), force=True)
        if each.split("_")[3] == "METL":
            mc.connectAttr("{}.outAlpha".format(each), "{}.metalness".format(matName), force=True)
        if each.split("_")[3] == "MSK":
            continue
        if each.split("_")[3] == "NRM":
            mc.connectAttr("{}.outColor".format(each), "{}.bumpMap".format(matName), force=True)
            mc.setAttr("{}.bumpMapType".format(matName), 1)
        if each.split("_")[3] == "SPC":
            mc.connectAttr("{}.outColor".format(each), "{}.reflectionColor".format(matName), force=True)
        if each.split("_")[3] == "SPR":
            mc.connectAttr("{}.outAlpha".format(each), "{}.reflectionGlossiness".format(matName), force=True)
            mc.setAttr("{}.useRoughness".format(matName), 1)
        if each.split("_")[3] == "EMS":
            mc.connectAttr("{}.outColor".format(each), "{}.illumColor".format(matName), force=True)

shaderCreate(textures)

# =================================================================================
# updates selected node's file path version to highest published version
# 201909201122
# =================================================================================


import maya.cmds as mc
import os

def texUpdate(input):
    path = mc.getAttr("{}.fileTextureName".format(input))
    pathSplit = path.split("/")
    asset = pathSplit[5]
    mapType = pathSplit[11]
    version = pathSplit[13]
    versionPath = "/".join(pathSplit[0:13])
    highestVersion = max(os.listdir(versionPath))
    newpath = path.replace(version, highestVersion)
    mc.setAttr("{}.fileTextureName".format(input), newpath, type="string")
    print("updated {2}:{3} {0} to {1}".format(version, highestVersion, asset, mapType))


nodes = mc.ls(sl=1)
if len(nodes) == 0:
    print "select something first"
else:
    for node in nodes:
        texUpdate(node)
    print("Complete")


# END OF SCRIPT