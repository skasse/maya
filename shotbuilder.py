

# ==================================================================================================
# import python
# ==================================================================================================

import maya.cmds as mc

# ==================================================================================================
# CREATE RENDERLAYERS
# ==================================================================================================

mc.createRenderLayer(name="ao", number=1, empty=True)
mc.createRenderLayer(name="morning", number=1, empty=True)
mc.createRenderLayer(name="evening", number=1, empty=True)
mc.createRenderLayer(name="night", number=1, empty=True)
mc.createRenderLayer(name="bedtime", number=1, empty=True)

# ==================================================================================================
# SELECT RENDERLAYERS
# ==================================================================================================

mc.editRenderLayerGlobals(currentRenderLayer="ao")
mc.editRenderLayerGlobals(currentRenderLayer="morning")
mc.editRenderLayerGlobals(currentRenderLayer="evening")
mc.editRenderLayerGlobals(currentRenderLayer="night")
mc.editRenderLayerGlobals(currentRenderLayer="bedtime")

# ==================================================================================================
# Create Layer Override
# ==================================================================================================
selection = mc.ls(sl=True)
for each in selection:
    mc.editRenderLayerAdjustment("{}.enabled".format(each))

# ==================================================================================================
# Remove Layer Override
# ==================================================================================================
selection = mc.ls(sl=True)
for each in selection:
    mc.editRenderLayerAdjustment("{}.enabled".format(each), remove=True)

# select hierarchy
mc.select(hi=True)
# list selected
print mc.ls(sl=True)

# rename iterator
selection = mc.ls(sl=True)
children = mc.listRelatives(children=True)
i = 0
for each in selection:
    i += 1
    mc.rename(each, "{}_{}".format("IES_bedroomCeiling", i))

# =================================================================================================
# IES ASSIGNMENT
# ==================================================================================================
#GENERIC ASSIGNMENT
IES_Path = "R:\PRODUCTS\IES_lights\ll\Decorative Indoor\Autry LED Fabric Shaded Dome\FMASSL_6_F01.ies"
selection = mc.ls(sl=True)
for each in selection:
    #global IES_Path
    mc.setAttr("{}.iesFile".format(each), IES_Path, type="string")

#HOMEPOD ASSIGNMENT
IES_Path = "R:\PRODUCTS\IES_lights\ll\Decorative Indoor\Autry LED Fabric Saucer\FMASRL_6.ies"
homepodLightList = ["IES_homepod_livingroom_1", "IES_homepod_kitchen_1", "IES_homepod_bedroom_1"]
for each in homepodLightList:
    mc.setAttr("{}Shape.iesFile".format(each), IES_Path, type="string")

homepodLightList = ["IES_homepod_livingroom_1", "IES_homepod_kitchen_1", "IES_homepod_bedroom_1"]
for each in homepodLightList:
    currentIntensity = mc.getAttr("{}Shape.intensity".format(each))
    newIntensity = currentIntensity * 2
    mc.setAttr("{}Shape.intensity".format(each), newIntensity)

# ==================================================================================================
# SCENE CREATION
# ==================================================================================================
#  set frame range
mc.playbackOptions(ast=1001, aet=1096)
mc.playbackOptions(min=1001, max=1096)

# set to animation
#mc.setAttr("vraySettings.animType", 1)
#mc.setAttr('vraySettings.animBatchOnly', 1)
#mc.setAttr("defaultRenderGlobals.startFrame", 1001)
#mc.setAttr("defaultRenderGlobals.endFrame", 1096)

# create vray bake nodes
mc.createNode("VRayBakeOptions", name="vrayBakeOptions")
mc.sets(selection, forceElement='vrayBakeOptions')

# create asset group nodes
mc.createNode('transform', name="ASSET_GRP")
mc.select("GEO*", r=True)
selection = mc.ls(sl=True, tr=True)
mc.parent(selection, "ASSET_GRP")

# ASSIGN SHADER
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="DEFAULT_blend_SG")
mc.hyperShade(assign="AO_blend_SG")


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

# create VOP # ==================================================================================================

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

mc.select("GEO_*", r=True)
selection = mc.ls(sl=True, s=True)
for each in selection:
    mc.setAttr("{}.visibleInReflections".format(each), 1)
    mc.setAttr("{}.visibleInRefractions".format(each), 1)

# ==================================================================================================
# AO RenderLayer Setup
# ==================================================================================================

currentlayer = "ao"

membership_AO = [
    "ASSET_GRP",
]

mc.connectAttr("MASTER_SG", "{}.shadingGroupOverride".format(currentlayer), force=True)

# ==================================================================================================
# MORNING RenderLayer Setup
# ==================================================================================================

currentlayer = "morning"

members = [
    "ASSET_GRP",
    "MORNING_GRP",
    "INTERIOR_LIGHTS_GRP"
]

mc.connectAttr("MASTER_SG", "{}.shadingGroupOverride".format(currentlayer), force=True)

LightsList_MORNING = [
    u'IES_kitchenCeiling_3',
    u'IES_livingroomCeiling_1',
    u'IES_livingroomCeiling_2',
    u'IES_livingroomCeiling_3',
    u'IES_livingroomCeiling_4',
    u'IES_livingroomCeiling_5',
    u'IES_lamp_floor_1',
    u'IES_lamp_floor_2',
    u'IES_lamp_floor_3',
    u'IES_livingroomCeiling_6',
    u'IES_livingroomCeiling_7',
    u'IES_livingroomCeiling_8'
    ]

shapesList = mc.listRelatives(LightsList_MORNING, children=True)
for each in shapesList:
    mc.editRenderLayerAdjustment("{}.enabled".format(each))
    mc.setAttr("{}.enabled".format(each), 1)

# ==================================================================================================
# EVENING RenderLayer Setup
# ==================================================================================================
currentlayer = "evening"

membership_EVENING = [
    "ASSET_GRP",
    "EVENING_GRP",
    "INTERIOR_LIGHTS_GRP"
]

mc.connectAttr("MASTER_SG", "{}.shadingGroupOverride".format(currentlayer), force=True)

LightsList_EVENING = [
    "IES_lamp_table_1",
    "IES_cabinet_1",
    "IES_cabinet_2",
    "IES_cabinet_3",
    "IES_cabinet_4",
    "IES_cabinet_5",
    "IES_bathroomCeiling_1",
    "IES_bathroomCeiling_2",
    "IES_bathroomCeiling_3",
    "IES_bathroomCeiling_4",
    "IES_bathroomCeiling_5"
]


# ==================================================================================================
# NIGHT RenderLayer Setup
# ==================================================================================================

currentlayer = "night"

members = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

mc.connectAttr("MASTER_SG", "{}.shadingGroupOverride".format(currentlayer), force=True)


# ==================================================================================================
# BEDTIME RenderLayer Setup
# ==================================================================================================

currentlayer = "bedtime"

membership_BEDTIME = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

mc.connectAttr("MASTER_SG", "{}.shadingGroupOverride".format(currentlayer), force=True)

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
# ASSET IMPORT
# ==================================================================================================

mc.file("R:/TASKS/default/skassekert/renderData/Camera/TurnTableCam_v0002.mb", i=True, namespace="Shotcam");
mc.file("R:/TASKS/default/skassekert/renderData/lightRig/LightRig_v0002.mb", i=True)
mc.file("R:/TASKS/default/skassekert/renderData/shaders/DEFAULT_blend_SG.mb", i=True)
mc.file("R:/TASKS/default/skassekert/renderData/shaders/AO_blend_SG.mb", i=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_leftWall_whole.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_frontWall_whole.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_backWall_whole.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_roof.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_rightWall_whole.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_floor.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_interior.dae", r=True)
mc.file("R:/PRODUCTS/SourceContent/HomePod/Siri_At_Home/Model/SM_terrain.dae", r=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Bedroom.dae", r=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_Homepod_LivingRoom.dae", r=True)
mc.file("R:\PRODUCTS\SourceContent\HomePod\Siri_At_Home\Model\SM_HomePod_Kitchen.dae", r=True)



#=======================================================================================================================
#COPY LIGHTMAP TO MAP1 - REMOVES NEED FOR TRIPLE SWITCH AND ENABLES LIGHTMAP VIEWING IN VIEWPORT
#=======================================================================================================================
for node in mc.ls(sl=True):
    lightmapName = mc.polyUVSet(node, q=True, auv=True)[-1]
    mapName = mc.polyUVSet(node, q=True, auv=True)[0]
    mc.polyCopyUV(node, uvSetNameInput=lightmapName, uvSetName=mapName)

#=======================================================================================================================
#SWITCHES FILE READ PATH RATHER THAN CREATING 5 SEPARATE SHADERS
#USE AS CUSTOM SHELF BUTTONS
#=======================================================================================================================
def textureSwap(timeofday):
    fileTextureList = [
        u'T_siriHouse_siriAthome_rectangle_evening_e_1',
        u'T_siriHouse_Back_Wall_Whole_evening_e_1',
        u'T_siriHouse_Front_Wall_Whole_evening_e_1',
        u'T_siriHouse_siriAthome_cylinder_evening_e_1',
        u'T_siriHouse_Left_Wall_Whole_evening_e_1',
        u'T_siriHouse_HP_living_Room_evening_e_1',
        u'T_siriHouse_Right_Wall_Whole_evening_e_1',
        u'T_siriHouse_blindsFrontWall_evening_e_1',
        u'T_siriHouse_House_Roof_evening_e_1',
        u'T_siriHouse_blindsLeftWall_evening_e_1',
        u'T_siriHouse_House_Terrain_evening_e_1',
        u'T_siriHouse_blindsBackWall_evening_e_1',
        u'T_siriHouse_House_interior_evening_e_1',
        u'T_siriHouse_House_Floor_evening_e_1',
        u'T_siriHouse_HP_bedroom_evening_e_1',
        u'T_siriHouse_HP_kitchen_evening_e_1',
        u'T_siriHouse_BirchTree_evening_e_1',
        u'T_siriHouse_AshTree_evening_e_1'
    ]
    for node in fileTextureList:
        header = "_".join(node.split("_")[0:-3])
        tail = node.split("_")[-2]
        mc.setAttr("{}.fileTextureName".format(node),
                   "images/bake/v0027/{0}/graded/{1}_{0}_e.png".format(timeofday, header), type="string")
        print "{}.fileTextureName".format(node), "images/bake/v0027/{0}/graded/{1}_{0}_e.png".format(timeofday, header)


textureSwap("ao")
textureSwap("morning")
textureSwap("evening")
textureSwap("night")
textureSwap("bedtime")
