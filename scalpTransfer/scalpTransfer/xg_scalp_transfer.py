import maya.cmds as mc
import mayaDeformers as md

def xg_scalp_transfer(**kwargs):

    path = 'G:/Shared drives/TriplegangersGroom_ext/users/skassekert/xgen_transferring/maya/scenes/'

    def abcImport(path):
        return mc.file(path, i=1, mnc=1, ns=":", rnn=1)[0].lstrip('|')

    mark_v1 = abcImport(f'{path}mark_v1_bs.abc')
    mark_v2 = abcImport(f'{path}mark_v2_bs.abc')
    newChar = abcImport(f'{path}eugene_v2_bs.abc')

    # create blendshape and activate for scalp
    blendShapeName = "scalpBlendShape"
    source, target, bsName = mark_v1, "scalpHiHead", "scalpBlendShape"
    mc.blendShape([source, target], automatic=1, name=bsName)
    mc.setAttr(f'{blendShapeName}.{source}', 1)

    # shrinkwrap -> delete -> wrap
    sw = md.shrinkWrap(mark_v1, mark_v2, projection=4)
    mc.delete(mark_v1, ch=1)
    md.wrap(mark_v1, mark_v2)

    # blendshape to new character
    bsName2 = "charXferBlendShape"
    mc.blendShape([newChar, mark_v2], automatic=1, name=bsName2)
    mc.setAttr(f'{bsName2}.{newChar}', 1)

    # delete history from scalp before export
    def shampoo(**kwargs):
        scalp = kwargs.get('scalp') or 'scalpHiHead'
        ignore_list = ["scalpBlendShape", 'groupParts1']
        descriptions = [x for x in mc.listConnections(f'{scalp}.worldMesh') if not any( w in x for w in ignore_list)]
        # disconnect mesh from descriptions
        for desc in descriptions:
            mc.disconnectAttr(f'{desc.split("_")[0]}Shape.worldMesh[0]', f'{desc}Shape.geometry')

        # delete history
        mc.delete(scalp, ch=True)

        # connect mesh to descriptions
        for desc in descriptions:
            mc.connectAttr(f'{desc.split("_")[0]}Shape.worldMesh[0]', f'{desc}Shape.geometry')

        # remove target mesh from scene
        mc.delete([mark_v1, mark_v2, newChar])
    shampoo()
    print('xgen scalp transfer complete')