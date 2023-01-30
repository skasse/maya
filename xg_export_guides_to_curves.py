import maya.cmds as cmds
import xgenm as xg
import xgenm.xgGlobal as xgg

if xgg.Maya:
    palettes = xg.palettes()
    for palette in palettes:
        descriptions = xg.descriptions(palette)
        for description in descriptions:
            print(" Description:" + description)
            guidesName = xg.descriptionGuides(description)
            print(guidesName)
            cmds.select(guidesName, r = True)
            mel.eval('xgmCreateCurvesFromGuidesOption(0, 0, "%s")' % (description+"_Curves"))