
# ==================================================================================================
# import python
# ==================================================================================================

import maya.cmds as mc

# ==================================================================================================
# ASSET IMPORT
# ==================================================================================================

mc.file("R:/TASKS/default/skassekert/renderData/Camera/TurnTableCam_v0002.mb", i=True, namespace="Shotcam");
mc.file("R:/TASKS/default/skassekert/renderData/lightRig/LightRig_v0004.mb", i=True)
mc.file("R:/TASKS/default/skassekert/renderData/shaders/MASTER_SWITCH_SG.ma", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_leftWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_frontWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_backWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_roof.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_rightWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_floor.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_interior.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_terrain.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Bedroom.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_Homepod_LivingRoom.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Kitchen.dae", i=True)

# ==================================================================================================
# SCENE CREATION
# ==================================================================================================
#  set frame range
mc.playbackOptions(ast=1001, aet=1096)
mc.playbackOptions(min=1001, max=1096)

# set to animation
# mc.setAttr("vraySettings.animType", 1)
# mc.setAttr('vraySettings.animBatchOnly', 1)
# mc.setAttr("defaultRenderGlobals.startFrame", 1001)
# mc.setAttr("defaultRenderGlobals.endFrame", 1096)

# create asset group nodes
mc.createNode('transform', name="ASSET_GRP")
selection = mc.ls("GEO*", tr=True)
mc.parent(selection, "ASSET_GRP")


# ==================================================================================================
# RENDERLAYERS
# ==================================================================================================

# CREATE RENDERLAYERS
mc.createRenderLayer(name="ao", number=1, empty=True)
mc.createRenderLayer(name="morning", number=1, empty=True)
mc.createRenderLayer(name="evening", number=1, empty=True)
mc.createRenderLayer(name="night", number=1, empty=True)
mc.createRenderLayer(name="bedtime", number=1, empty=True)

# # Create Layer Override
# selection = mc.ls(sl=True)
# for each in selection:
#     mc.editRenderLayerAdjustment("{}.enabled".format(each))
#
# # Remove Layer Override
# selection = mc.ls(sl=True)
# for each in selection:
#     mc.editRenderLayerAdjustment("{}.enabled".format(each), remove=True)

# ==================================================================================================
# AO RenderLayer Setup
# ==================================================================================================

currentlayer = "ao"

membershipList = [
    "ASSET_GRP",
]

for each in membershipList:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.connectAttr("MASTER_SWITCH_SG.message", "{}.shadingGroupOverride".format(currentlayer), force=True)

# SELECT RENDERLAYER
mc.editRenderLayerGlobals(currentRenderLayer="ao")

# ASSIGN SWITCH OVERRIDE
mc.editRenderLayerAdjustment("MASTER_SWITCH_mtl.materialsSwitch")
mc.setAttr("MASTER_SWITCH_mtl.materialsSwitch", 1)


# ==================================================================================================
# MORNING RenderLayer Setup
# ==================================================================================================

currentlayer = "morning"

membershipList = [
    "ASSET_GRP",
    "MORNING_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in membershipList:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.connectAttr("MASTER_SWITCH_SG.message", "{}.shadingGroupOverride".format(currentlayer), force=True)
# SELECT RENDERLAYER
mc.editRenderLayerGlobals(currentRenderLayer="morning")


# ==================================================================================================
# EVENING RenderLayer Setup
# ==================================================================================================
currentlayer = "evening"

membershipList = [
    "ASSET_GRP",
    "EVENING_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in membershipList:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.connectAttr("MASTER_SWITCH_SG.message", "{}.shadingGroupOverride".format(currentlayer), force=True)
# SELECT RENDERLAYER
mc.editRenderLayerGlobals(currentRenderLayer="evening")


# ==================================================================================================
# NIGHT RenderLayer Setup
# ==================================================================================================

currentlayer = "night"

membershipList = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in membershipList:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.connectAttr("MASTER_SWITCH_SG.message", "{}.shadingGroupOverride".format(currentlayer), force=True)
# SELECT RENDERLAYER
mc.editRenderLayerGlobals(currentRenderLayer="night")

# ==================================================================================================
# BEDTIME RenderLayer Setup
# ==================================================================================================

currentlayer = "bedtime"

membershipList = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in membershipList:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.connectAttr("MASTER_SWITCH_SG.message", "{}.shadingGroupOverride".format(currentlayer), force=True)
# SELECT RENDERLAYER
mc.editRenderLayerGlobals(currentRenderLayer="bedtime")

LightsList_BEDTIME = [
    "IES_cabinet_1",
    # "IES_cabinet_2",
    # "IES_cabinet_3",
    # "IES_cabinet_4",
    # "IES_cabinet_5",
    # "IES_lamp_floor_1",
    # "IES_lamp_floor_2",
    # "IES_lamp_floor_3",
    "IES_lamp_table_1"
]

for each in mc.listRelatives(LightsList_BEDTIME, children=True):
    mc.editRenderLayerAdjustment("{}.enabled".format(each))
    mc.setAttr("{}.enabled".format(each), 1)


# ==================================================================================================
# assign switch Attribute
# ==================================================================================================

def masterSwitchCreate():
    material_assignment_dict = {
        "GEO_siriAthome_cylinder": 0,
        "GEO_siriAthome_rectangle": 0,
        "GEO_House_Terrain": 0,
        "GEO_HP_living_Room": 6,
        "GEO_HP_kitchen": 7,
        "GEO_HP_bedroom": 6,
        "GEO_AshTree": 1,
        "GEO_BirchTree": 2,
        "GEO_House_interior": 3,
        "GEO_House_Roof": 4,
        "GEO_House_Floor": 4,
        "GEO_Front_Wall_Whole": 5,
        "GEO_Left_Wall_Whole": 5,
        "GEO_Back_Wall_Whole": 5,
        "GEO_Right_Wall_Whole": 5
    }

    assetList = mc.listRelatives("ASSET_GRP", children=True, shapes=False)

    for each in assetList:
        if each in material_assignment_dict:
            # print "{0} exists with {1}".format(each, material_assignment_dict[each])
            mc.vray("addAttributesFromGroup", each, "vray_user_attributes", 1)
            mc.setAttr('{}.vrayUserAttributes'.format(each),
                       "MASTER_mtl_switch={}".format(material_assignment_dict[each]), type="string")
        else:
            print "{} does not have a switch assignment! SKIPPING".format(each)
            continue

masterSwitchCreate()

# ==================================================================================================
# create VOP
# ==================================================================================================
def vopCreate():
    VOPname = "vrayobjectproperties"
    mc.createNode("VRayObjectProperties", name=VOPname)
    mc.setAttr("{}.primaryVisibility".format(VOPname), 0)
    mc.setAttr("{}.shadowVisibility".format(VOPname), 0)
    mc.setAttr("{}.giVisibility".format(VOPname), 0)

    VOPnodes = [
        "GEO_Roof",
        "GEO_Front_Wall_Whole",
        "GEO_blindsFrontWall"
    ]
    mc.sets(VOPnodes, forceElement=VOPname)

vopCreate()


# ==================================================================================================
# set default renderstats
# ==================================================================================================
mc.select("GEO_*", r=True)
selection = mc.ls(sl=True, s=True)
for each in selection:
    mc.setAttr("{}.visibleInReflections".format(each), 1)
    mc.setAttr("{}.visibleInRefractions".format(each), 1)



# =================================================================================================
# IES ASSIGNMENTS
# ==================================================================================================
# GENERIC IES ASSIGNMENT
def iesFilePath():
    IES_Path = "R:\PRODUCTS\IES_lights\ll\Decorative Indoor\Autry LED Fabric Shaded Dome\FMASSL_6_F01.ies"
    selection = mc.ls(sl=True)
    for each in selection:
        mc.setAttr("{}.iesFile".format(each), IES_Path, type="string")

iesFilePath()


# HOMEPOD IES ASSIGNMENT
def iesFilePathHP():
    IES_Path = "R:\PRODUCTS\IES_lights\ll\Decorative Indoor\Autry LED Fabric Saucer\FMASRL_6.ies"
    homepodLightList = ["IES_homepod_livingroom_1", "IES_homepod_kitchen_1", "IES_homepod_bedroom_1"]
    for each in homepodLightList:
        mc.setAttr("{}Shape.iesFile".format(each), IES_Path, type="string")

iesFilePathHP()


# ==================================================================================================
# REALTIME VIEW SCENE AND FUNCTIONS
# ==================================================================================================




# ==================================================================================================
# import python
# ==================================================================================================

import maya.cmds as mc

# ==================================================================================================
# ASSET IMPORT
# ==================================================================================================

mc.file("R:/TASKS/default/skassekert/renderData/shaders/MASTER_SWITCH_SG.ma", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_leftWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_frontWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_backWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_roof.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_rightWall_whole.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_floor.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_interior.dae", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_terrain.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Bedroom.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_Homepod_LivingRoom.dae", i=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Kitchen.dae", i=True)

# create asset group nodes
mc.createNode('transform', name="ASSET_GRP")
selection = mc.ls("GEO*", tr=True)
mc.parent(selection, "ASSET_GRP")

# =======================================================================================================================
# COPY LIGHTMAP TO MAP1 - REMOVES NEED FOR TRIPLE SWITCH AND ENABLES LIGHTMAP VIEWING IN VIEWPORT
# =======================================================================================================================
def lightmapXfer():
    assetList = mc.listRelatives("ASSET_GRP", children=True, shapes=False)
    for node in assetList:
        lightmapName = mc.polyUVSet(node, q=True, auv=True)[-1]
        mapName = mc.polyUVSet(node, q=True, auv=True)[0]
        mc.polyCopyUV(node, uvSetNameInput=lightmapName, uvSetName=mapName)

lightmapXfer()

def shaderCreate():
    assetList = mc.listRelatives("ASSET_GRP", children=True, shapes=False)
    imagepath="R:\\TASKS\\default\\skassekert\\images\\bake\\v0022\\ao"
    fileTextureList = []
    for node in assetList:
        imagename="T_siriHouse_{0}_{1}_e".format(node.split("GEO_")[1], renderLayer)
        sgname="{}_SG".format(node)
        mc.sets(name=sgname, renderable=True, nss=True, empty=True)
        mtlname="{}_mtl".format(node)
        mc.shadingNode("surfaceShader", name=mtlname, asShader=True)
        mc.connectAttr("{}.outColor".format(mtlname), "{}.surfaceShader".format(sgname), force=True)
        filename="{}_file".format(node)
        fileTextureList.append(filename)
        mc.shadingNode("file", name=filename, asTexture=True)
        mc.setAttr("{}.fileTextureName".format(filename), "{}\\{}.png".format(imagepath, imagename), type="string")
        mc.connectAttr("{}.outColor".format(filename), "{}.outColor".format(mtlname))
        mc.sets(node, forceElement=sgname)
    return fileTextureList

fileTextureList = shaderCreate()


mc.select("ASSET_GRP", replace=True)
mc.sets(forceElement="initialShadingGroup")

# =======================================================================================================================
# SWITCHES FILE READ PATH RATHER THAN CREATING 5 SEPARATE SHADERS
# USE AS CUSTOM SHELF BUTTONS
# =======================================================================================================================
def textureSwap(timeofday, fileTextureList):
    for node in fileTextureList:
        imagename="T_siriHouse_{0}_{1}_e".format("_".join(node.split("_")[1:-1]), timeofday)
        mc.setAttr("{}.fileTextureName".format(node),
                   "images/bake/v0022/{0}/{1}.png".format(timeofday, imagename), type="string")
        print "{}.fileTextureName".format(node), "images/bake/v0027/{0}/{1}.png".format(timeofday, imagename)


textureSwap("ao")
textureSwap("morning")
textureSwap("evening")
textureSwap("night")
textureSwap("bedtime")

# =================================================================================================
# MISC FUNCTIONS
# ==================================================================================================

# # select hierarchy
# mc.select(hi=True)
#
# # list selected
# print mc.ls(sl=True)

# rename iterator
def renameIter():
    new_name = raw_input()
    selection = mc.ls(sl=True)
    children = mc.listRelatives(children=True, shapes=False)
    i = 1
    for each in selection:
        mc.rename(each, "{}_{}".format(new_name, i))
        i += 1

renameIter()
