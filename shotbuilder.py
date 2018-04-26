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
mc.setAttr("vraySettings.animType", 1)
mc.setAttr('vraySettings.animBatchOnly', 1)
mc.setAttr("defaultRenderGlobals.startFrame", 1001)
mc.setAttr("defaultRenderGlobals.endFrame", 1096)

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

# assign switch Attribute
mc.select('*_Wall*', r=True)
geo_w_glass = mc.ls(sl=True, tr=True)
for node in geo_w_glass:
    mc.vray("addAttributesFromGroup", node, "vray_user_attributes", 1)
    mc.setAttr('{}.vrayUserAttributes'.format(node), "switch_Alpha=0", type="string")

"GEO_siriAthome_cylinder"
"GEO_siriAthome_rectangle"
"GEO_House_Terrain"
GEO_HP_living_Room
GEO_HP_kitchen
GEO_HP_bedroom

"terrain_mtl" : 0

#=============================================================

GEO_AshTree

"ashTree_mtl" : 1

#=============================================================

GEO_BirchTree

"birchTree_mtl" : 2

#=============================================================

GEO_House_interior

interior_SG

#=============================================================

GEO_House_Roof
GEO_House_Floor

homeExterior_SG

#=============================================================

GEO_Front_Wall_Whole
GEO_Left_Wall_Whole
GEO_Back_Wall_Whole
GEO_Right_Wall_Whole

exteriorWalls_SG

#=============================================================
MATERIALS = {
    "terrain_mtl" : 0,
    "ashTree_mtl" : 1,
    "birchTree_mtl" : 2,
    "interior_mtl" : 3,
    "homeExterior_mtl" : 4,
    "exteriorWalls_BLEND_mtl": 5,
}

MATERIALS.get("terrain_mtl")


# create VOP
VOPname = "vrayobjectproperties"
mc.createNode("VRayObjectProperties", name=VOPname)
mc.setAttr("{}.primaryVisibility".format(VOPname), 0)
mc.setAttr("{}.shadowVisibility".format(VOPname), 0)
mc.setAttr("{}.giVisibility".format(VOPname), 0)

VOPnodes = [
    "GEO_Roof",
    "GEO_Front_Wall_Whole"
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

for each in membership_AO:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.editRenderLayerGlobals(currentRenderLayer=currentlayer)
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="AO_blend_SG")

# ==================================================================================================
# MORNING RenderLayer Setup
# ==================================================================================================

currentlayer = "morning"

members = [
    "ASSET_GRP",
    "MORNING_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in members:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.editRenderLayerGlobals(currentRenderLayer=currentlayer)
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="DEFAULT_blend_SG")

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

for each in membership_EVENING:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.editRenderLayerGlobals(currentRenderLayer=currentlayer)
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="DEFAULT_blend_SG")

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
shapesList = mc.listRelatives(LightsList_EVENING, children=True)
for each in shapesList:
    mc.editRenderLayerAdjustment("{}.enabled".format(each))
    mc.setAttr("{}.enabled".format(each), 1)

# ==================================================================================================
# NIGHT RenderLayer Setup
# ==================================================================================================

currentlayer = "night"

members = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in members:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.editRenderLayerGlobals(currentRenderLayer=currentlayer)
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="DEFAULT_blend_SG")

mc.select("IES_*", r=True)
nightLightsList = mc.ls(sl=True, transforms=True)
shapesList = mc.listRelatives(nightLightsList, children=True)
for each in shapesList:
    mc.editRenderLayerAdjustment("{}.enabled".format(each))
    mc.setAttr("{}.enabled".format(each), 1)

# ==================================================================================================
# BEDTIME RenderLayer Setup
# ==================================================================================================

currentlayer = "bedtime"

membership_BEDTIME = [
    "ASSET_GRP",
    "NIGHT_GRP",
    "INTERIOR_LIGHTS_GRP"
]

for each in membership_BEDTIME:
    mc.editRenderLayerMembers(currentlayer, each, noRecurse=True);

mc.editRenderLayerGlobals(currentRenderLayer=currentlayer)
mc.select("ASSET_GRP", r=True)
mc.hyperShade(assign="DEFAULT_blend_SG")

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

shapesList = mc.listRelatives(LightsList_BEDTIME, children=True)
for each in shapesList:
    mc.editRenderLayerAdjustment("{}.enabled".format(each))
    mc.setAttr("{}.enabled".format(each), 1)

# ==================================================================================================
# ASSET IMPORT
# ==================================================================================================

mc.file("R:/TASKS/default/skassekert/renderData/Camera/TurnTableCam_v0002.mb", i=True, namespace="Shotcam");
mc.file("R:/TASKS/default/skassekert/renderData/lightRig/LightRig_v0002.mb", i=True)
mc.file("R:/TASKS/default/skassekert/renderData/shaders/DEFAULT_blend_SG.mb", i=True)
mc.file("R:/TASKS/default/skassekert/renderData/shaders/AO_blend_SG.mb", i=True)
mc.file("", r=True)
