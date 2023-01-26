


sys.path.append("C:/Scripts/maya/scalpTransfer/scalpTransfer")
import maya.cmds as mc
import mayaDeformers as md

string = f'complete'
print(string)
target_file_path = "G:/Shared drives/TriplegangersGroom_ext/users/skassekert/xgen_transferring/maya/scenes/mark_scalpHiHead_vertexOrderMatch_bsTarget.ma"

base_mesh = "scalp_head_hi"
target_mesh = "target_mesh"

# shrinkWrap(base_mesh, target_mesh)

## if topo matches - blendshape


mc.blendShape([target_mesh, base_mesh], automatic=1)





path = "G:/Shared drives/TriplegangersGroom_ext/users/skassekert/xgen_transferring/maya/scenes/mark_scalpHiHead_vertexOrderMatch_bsTarget.ma"

target_mesh = mc.file(path, iv=1, mnc=1, ns=":", i=True, rnn=True)

#mc.rename(targetmesh[0], "target_mesh")
blendShapeName = "scalpBlendShape"
mc.blendShape([target_mesh[0], "scalpHiHead"], automatic=1, name=blendShapeName)
targetMeshName = target_mesh[0].lstrip("|")
mc.setAttr(f'{blendShapeName}.{targetMeshName}', 1)
for desc in xg.descriptions():
    mc.disconnectAttr("scalpHiHeadShape.worldMesh[0]", f'scalpHiHead_{desc}Shape.geometry')
mc.delete("scalpHiHead", ch=True)
for desc in xg.descriptions():
    mc.connectAttr("scalpHiHeadShape.worldMesh[0]", f'scalpHiHead_{desc}Shape.geometry')
mc.delete(targetMeshName)
mc.xgmPreview(xg.descriptions())


xg.palettes()







mc.xgmPreview(xg.descriptions(), c=True)

mc.ls(["*", "*:*"], type="mesh")

# target mesh file path
path = fr"G:\Shared drives\TriplegangersGroom_ext\users\skassekert\xgen_transferring\maya\scenes\topo_2_bsTarget.ma"

# import mesh target
target_mesh = mc.file(path, iv=1, mnc=1, ns=":", i=True, rnn=True)

# create blendshape and activate
blendShapeName = "scalpBlendShape"
mc.blendShape([target_mesh[0], "scalpHiHead"], automatic=1, name=blendShapeName)
targetMeshName = target_mesh[0].lstrip("|")
mc.setAttr(f'{blendShapeName}.{targetMeshName}', 1)

descriptions = [x for x in mc.listConnections("scalpHi*.worldMesh") if "scalpBlendShape" not in x]
# disconnect mesh from descriptions
for desc in descriptions:
    mc.disconnectAttr(f'{desc.split("_")[0]}Shape.worldMesh[0]', f'{desc}Shape.geometry')

# delete history
mc.delete("scalpHiHead", ch=True)

# connect mesh to descriptions
for desc in descriptions:
    mc.connectAttr(f'{desc.split("_")[0]}Shape.worldMesh[0]', f'{desc}Shape.geometry')

# remove target mesh from scene
mc.delete(targetMeshName)

# update xgen preview
mc.xgmPreview(xg.descriptions(), c=True, pb=True)



mc.objectType(mc.ls(sl=1))


wrapDeformer = mc.deformer("scalpHiPony", type="wrap")[0]




path = fr"G:\Shared drives\TriplegangersGroom_ext\users\skassekert\xgen_transferring\maya\scenes\topo_2_bsTarget.ma"

imports = mc.file(path, i=1, mnc=1, ns=":", rnn=1)

mark_v1 = 'mark_v1_bst'
mark_v2 = 'mark_v2_bst'

# create blendshape and activate for scalp
blendShapeName = "scalpBlendShape"
source, target = mark_v1, "scalpHiHead"
mc.blendShape([source, target], automatic=1, name=blendShapeName)
mc.setAttr(f'{blendShapeName}.{source}', 1)

md.shrinkWrap(mark_v1, mark_v2, projection=4)
mc.delete(mark_v1, ch=1)
md.wrap(mark_v1, mark_v2)

blendShapeName2 = "charXferBlendShape"
groomXferMorphs = ['target_01_bst', 'target_02_bst']
groomXferMorphs.extend([mark_v2])
mc.blendShape(groomXferMorphs, automatic=1, name=blendShapeName2)