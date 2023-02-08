import maya.cmds as mc
import json

class setsNode:
    def __init__(self, name, parent=None):
        self.name = name
        self._parent = parent
        self._children = []

def traverse(node, parent=None):
        print(node, parent)
        children = list(node.keys())
        print(children)
        for child in children:
            # if child.endswith('_set'):
            if 'set' in child:
                print(f'{child} : {node[child]}')
                mc.sets(n=child)
                if not parent == None:
                    mc.sets(child, fe=parent)
                traverse(node[child], child)
            if child == 'items':
                for item in node[child]:
                    print(item, parent, child)
                    mc.sets(item, fe=parent)

def import_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data

def main(file_path):
    data = import_json(file_path)
    traverse(data)

# main(file_path=r'N:/tmp/test.json')