import maya.cmds as mc

def getSG():
    '''Returns all Shading Groups'''
    list = mc.ls(type="shadingEngine")
    return list

def getShadedNodes(input):
    '''Returns all nodes connected to input'''
    return mc.listConnections(input, type="mesh")

if not mc.objExists("originalGeo_GRP"):
    mc.createNode('transform', name="originalGeo_GRP")
if not mc.objExists("Model_GRP"):
    mc.createNode('transform', name="model_GRP")

def meshSplitter():
    
    print("BEGIN")
    i = 0
    totalSG = len(getSG())
    modifiedGeo = []
    for shadingGroup in getSG():
        i+=1
        shadedNodes = []
        if not getShadedNodes(shadingGroup):
        	print("skipping shading group {0}, {1} of {2}, no assigned geometry".format(shadingGroup, i, totalSG))
    	else:
            print("beginning shading group {0}, {1} of {2}".format(shadingGroup, i, totalSG))
            
            for each in getShadedNodes(shadingGroup):
                if each not in shadedNodes:
                    shadedNodes.append(each)
            for each in shadedNodes:
                mc.duplicate(each, name=each+"_"+shadingGroup, un=True)
                if each not in modifiedGeo:
                    modifiedGeo.append(each)
            # combines all remaining faces into Shading Engine named Mesh
            newname = "geo"+"_{}".format(shadingGroup)
            if len(mc.ls("*_{}".format(shadingGroup)))>1:
                mc.polyUnite("*_{}".format(shadingGroup), name = newname, ch=0)
            else: 
                mc.rename("*_{}".format(shadingGroup), newname)
            #  select faces assigned to SG
            mc.select(shadingGroup, replace=True)
            # create list of faces
            shadedFaces = mc.polyListComponentConversion(mc.ls(sl=True), tf=True)
           
            # create list of only duplicated geo's faces
            SGFaces = []
            for face in shadedFaces:
                if shadingGroup in face:
                    SGFaces.append(face)
           
            # select all duplicated geo's faces
            mc.select("*_{}.f[*]".format(shadingGroup))
            # toggle off SG faces
            mc.select(SGFaces, d=True)
            facesToRemove = mc.ls(sl=True)
            mc.delete(facesToRemove)
            mc.parent(newname, "model_GRP")
            print("{0} complete.".format(shadingGroup))
    mc.parent(modifiedGeo, "originalGeo_GRP")


meshSplitter()