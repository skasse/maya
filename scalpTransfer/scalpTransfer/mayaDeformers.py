### This function uses mayas built in deformers, but sets up the connections along with it. ###
import maya.cmds as mc

def getTargetMesh(targetTrans=str):

    sh = mc.ls(targetTrans, dag=True, shapes=True)
    # Find if at least one of them is an allowable target type
    for s in sh:
        io = mc.getAttr(s+".io")
        if io:
            continue

        mtype = mc.nodeType(s)
        if mtype == "mesh":
            return s
    return None


def shrinkWrap(mesh, target, **kwargs):

    targetMesh = getTargetMesh(target) # find a not intermediate shape

    # Find all the surf transforms that have been selected
    surf = mc.listRelatives(mesh, path=True)

    surface = surf[0]
    
    # SET A BUNCH OF ATTRIBUTES WITH KWARGS or with default value    
    projection = kwargs.get('projection') or 3
    closestIfNoIntersection = kwargs.get('closestIfNoIntersection') or 1
    reverse = kwargs.get('reverse') or 0
    bidirectional = kwargs.get('bidirectional') or 1
    boundingBoxCenter = kwargs.get('boundingBoxCenter') or 1
    axisReference = kwargs.get('axisReference') or 0
    alongX = kwargs.get('alongX') or 0
    alongY = kwargs.get('alongY') or 0
    alongZ = kwargs.get('alongZ') or 0
    offset = kwargs.get('offset') or 0
    targetInflation = kwargs.get('targetInflation') or 0

    shrinkwrapNode = mc.deformer(surface, type='shrinkWrap')[0]

    mc.setAttr(shrinkwrapNode + ".projection", projection)
    mc.setAttr(shrinkwrapNode + ".closestIfNoIntersection", closestIfNoIntersection)
    mc.setAttr(shrinkwrapNode + ".reverse", reverse)
    mc.setAttr(shrinkwrapNode + ".bidirectional", bidirectional)
    mc.setAttr(shrinkwrapNode + ".boundingBoxCenter", boundingBoxCenter)
    mc.setAttr(shrinkwrapNode + ".axisReference", axisReference)
    mc.setAttr(shrinkwrapNode + ".alongX", alongX)
    mc.setAttr(shrinkwrapNode + ".alongY", alongY)
    mc.setAttr(shrinkwrapNode + ".alongZ", alongZ)
    mc.setAttr(shrinkwrapNode + ".offset", offset)
    mc.setAttr(shrinkwrapNode + ".targetInflation", targetInflation)

    # Add the target object
    #
    mc.connectAttr(targetMesh + ".w", shrinkwrapNode + ".tgt")
    # connect up the smooth target attributes
    # so the smoothed target follows the target shape's settings
    #
    mc.connectAttr(targetMesh + ".co", shrinkwrapNode + ".co")
    mc.connectAttr(targetMesh + ".suv", shrinkwrapNode + ".suv")
    mc.connectAttr(targetMesh + ".kb", shrinkwrapNode + ".kb")
    mc.connectAttr(targetMesh + ".bnr", shrinkwrapNode + ".bnr")
    mc.connectAttr(targetMesh + ".khe", shrinkwrapNode + ".khe")
    mc.connectAttr(targetMesh + ".peh", shrinkwrapNode + ".peh")
    mc.connectAttr(targetMesh + ".kmb", shrinkwrapNode + ".kmb")

    mc.select(clear=True)
    return shrinkwrapNode

def wrap(mesh, target, **kwargs):

    targetMesh = getTargetMesh(target) # find a not intermediate shape
    baseShape = mc.duplicate(target, name=target+'Base')[0]
    mc.hide(baseShape)

    # Find all the surf transforms that have been selected
    surf = mc.listRelatives(mesh, path=True)

    surface = surf[0]
    
    # SET A BUNCH OF ATTRIBUTES WITH KWARGS or with default value    
    autoWeightThreshold = kwargs.get('autoWeightThreshold') or 1
    maxDistance = kwargs.get('maxDistance') or 1
    weightThreshold = kwargs.get('weightThreshold') or 0
    exclusiveBind = kwargs.get('exclusiveBind') or 1
    falloffMode = kwargs.get('falloffMode') or 0


    wrapNode = mc.deformer(surface, type='wrap')[0]

    mc.setAttr(wrapNode + ".autoWeightThreshold", autoWeightThreshold)
    mc.setAttr(wrapNode + ".maxDistance", maxDistance)
    mc.setAttr(wrapNode + ".weightThreshold", weightThreshold)
    mc.setAttr(wrapNode + ".exclusiveBind", exclusiveBind)
    mc.setAttr(wrapNode + ".falloffMode", falloffMode)

    # Add the target object
    #
    mc.connectAttr(targetMesh + ".worldMesh[0]", wrapNode + ".driverPoints[0]")
    mc.connectAttr(surface + ".worldMatrix[0]", wrapNode + ".geomMatrix")
    # connect up the smooth target attributes
    # so the smoothed target follows the target shape's settings
    #
    attrs = {'dropoff':['double', 4], 'inflType':['short', 2], 'smoothness':['double', 0]}
    for k,v in attrs.items():
        mc.addAttr(target, longName=k, attributeType=v[0], defaultValue=v[1], )
    mc.connectAttr(target + ".dropoff", wrapNode + ".dropoff[0]")
    mc.connectAttr(target + ".smoothness", wrapNode + ".smoothness[0]")
    mc.connectAttr(target + ".inflType", wrapNode + ".inflType[0]")
    mc.connectAttr(f'{baseShape}Shape' + ".worldMesh[0]", wrapNode + ".basePoints[0]")


    mc.select(clear=True)
    return wrapNode
