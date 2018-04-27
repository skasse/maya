def textureSwap():
    for node in fileTextureList:
        timeofday = "ao"
        header = "_".join(node.split("_")[0:-3])
        tail = node.split("_")[-2]
        mc.setAttr("{}.fileTextureName".format(node), "images/bake/v0027/{0}/graded/{1}_{0}_e.png".format(timeofday, header), type="string" )
        print "{}.fileTextureName".format(node), "images/bake/v0027/{0}/graded/{1}_{0}_e.png".format(timeofday, header)
    
textureSwap()
