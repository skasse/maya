import maya.cmds as mc
import maya.mel as mm

def legacy2Igs(collection):
    '''convert all xgen legacy groom to igs
    select_collection > Generate > Convert to Interactive Groom
    '''
    mc.select(collection)
    return [mc.listRelatives(i,p=True)[0] for i in mc.xgmGroomConvert(prefix="")]

def exportIgs2Usd(out_path,select=[]):
    """ export static hair curves from selected igs without material
    args:
        out_path : usd file output path with extention
        warning for lock disk , add "/This PC/"
        e.g) /This PC/C:/temp/test.usd
        select : igs descriptions
    """
    if not out_path:
        print("selt output file path")
 
    if not select:
        select = mc.ls(sl=True)
    mc.select(select)
    print(select)
    #options for XGen
    # set to prop
    mm.eval("optionVar -iv omniverse_export_objecttype 1")
 
    # export selection only
    mm.eval("optionVar -iv omniverse_export_collectontype 2")
 
    # animation off
    mm.eval("optionVar -iv omniverse_export_useanimation 0")
 
    # include mdl off
    mm.eval("optionVar -iv omniverse_embed_materials 0")
 
    # Yup
    mm.eval("optionVar -iv export_up_axis_type 1")
 
    # Xgen option
    #print(mm.eval("optionVar -q omniverse_export_xgen_wrap_type"))
    #print(mm.eval("optionVar -q omniverse_export_xgen_uv_interp_type"))
 
    # wrap type:: pinned (or:: nonperiodic , periodic)
    mm.eval("optionVar -sv omniverse_export_xgen_wrap_type pinned")
    # interp type:: uniform (or:: vertex)
    mm.eval("optionVar -sv omniverse_export_xgen_uv_interp_type uniform")
 
    # excute export
    mm.eval('OmniExportCmd -file "{}"'.format(out_path))
    print("//Done! export to usd :: ", out_path)

def main(**kwargs):
    outPath = kwargs.get('outPath') or "/This PC/N:/tmp/test_hairs.usd"
    scalpGeo = kwargs.get('scalpGeo') or "scalpHiHead"
    igs_descs = legacy2Igs("head_coll")
    items = []
    items.extend(igs_descs)
    items.append(kwargs.get(scalpGeo))
    mc.select(items)
    exportIgs2Usd(outPath,select= items)

