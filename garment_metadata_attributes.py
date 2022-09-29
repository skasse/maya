"""
injects metadata from a dictionary in the form of extra attributes on a transform node. 
"""
import maya.cmds as mc

metadata = {
"garmentType": "shirt:pants:skirt:socks:shoes:jacket", 
"garmentSize": "small:medium:large", 
"collarType": "straight:curved:floppy"
}

node = mc.ls(sl=True)
for data in metadata:
    mc.select(node)
    print([data])
    if data in mc.deleteAttr(node, q=True):
        mc.deleteAttr(at=data)
    mc.addAttr(ln=data, at="enum", en=metadata[data])