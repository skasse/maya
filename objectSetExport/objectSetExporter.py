# writes out selected objectSets to json file for later application if lost or corrupted in scene file.
# TODO - break into separate pieces. make __main__ and modules. 
import maya.cmds as mc
import json

class objectSetExport(object):
    
    def __init__(self):
        
        winID = "jsonExporter"
        
        if mc.window("jsonExporter", exists=True):
            mc.deleteUI(winID)
        
        winID = mc.window(winID, title='Import/Export Object Sets')
        mc.columnLayout()
        mc.button(label = "select Mesh", command = self.meshSelect)
        self.selectedMesh = mc.textFieldGrp(label='Selected mesh: ', adj=1,pht="pSphere1")
        mc.button(label = "choose Path", command = self.savePath)
        self.json_path = mc.textFieldGrp(label='json path: ', adj=1,pht="C:/Scripts/test.json")
        mc.button(label = "Export selected mesh's objectSets", command = self.export_json_sets)
        mc.button(label = "Import and apply json file to select mesh", command = self.apply_json_sets_from_file)
        mc.showWindow(winID)
    
    def meshSelect(self, *args):
        self.node = mc.ls(sl=1)
        mc.textFieldGrp(self.selectedMesh, edit=True, text=self.node[0])
        return self.node
    
    def savePath(self, *args):
        save_path = mc.fileDialog2(cap="Choose your file path", fm=0, ff='*.json')
        mc.textFieldGrp(self.json_path, edit=True, text=save_path[0])
    
    def export_json_sets(self, *args):
        # gather set names to save
        sets_to_save = None
        print(f'{"BEGIN":=^80}')
        exportNode = self.node
        if len(exportNode) != 1:
            mc.confirmDialog(message="Wrong number of mesh selected.\nCan only Select one mesh to export at a time", button="OK")
        else:
            sceneSets = mc.ls(type="objectSet")
            sets_to_save = {}
            for set in sceneSets:
                members = mc.sets(set, q=1)
                print(f"members: {members}")
                if not members:
                    print(f"{set} is empty set, pass")
                    pass
                else:
                    mesh_members = [x for x in members if x.split('.')[0] == exportNode[0]]
                    print(f'mesh_members: {mesh_members}')
                    if len(mesh_members) == 0:
                        print(f'empty set, pass')
                        pass
                    else:
                        sets_to_save[set] =  mesh_members
                        print(set, mesh_members)

        sets_to_export = {x: [x.replace(exportNode[0], "__miguelGuerreroRocks!__") for x in sets_to_save[x]] for x in sets_to_save}
        
        # export set info to json file
        json_path = (mc.textFieldGrp(self.json_path, q=True, tx=True))
        json_object = json.dumps(sets_to_export, indent=4)
        with open(json_path, 'w') as outfile:
            outfile.write(json_object)
        print(f'Exported {sets_to_export.keys()}')
        print(f'{"Export Complete":=^80}')
    
    def apply_json_sets_from_file(self, *args):
        imported_sets = None
        importNode = mc.ls(sl=1)
        if len(importNode) != 1:
            mc.confirmDialog(message="Wrong number of mesh selected.\nCan only Select one mesh to export at a time", button="OK")
        else:
            json_path = (mc.textFieldGrp(self.json_path, q=True, tx=True))
            # retrieve sets to apply to mesh
            with open(json_path, 'r') as infile:
                imported_sets = json.load(infile)
            sets_to_apply = {x: [x.replace("__miguelGuerreroRocks!__", importNode[0]) for x in imported_sets[x]] for x in imported_sets}
            for set in sets_to_apply:
                if not mc.objExists(set):
                    mc.sets(n=set)
            # for set in sets_to_apply:
            #     mc.sets(sets_to_apply[set], add=set)
            [mc.sets(sets_to_apply[set], add=set) for set in sets_to_apply]
            print(f'{"Import Complete":=^80}')

def main():
    objectSetExport()

if __name__ == "__main__":
    print("running from main")
    main()