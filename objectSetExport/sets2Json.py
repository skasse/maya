import maya.cmds as mc
import json

class SetsNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.items = []
        self._parent = parent
        self._children = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent
        parent.add_child(self)

    @property
    def children(self):
        return self._children
 
    def add_child(self, child):
        self._children.append(child)

    def as_json(self):
        data = {self.name: {'items': self.items}}
        for child in self.children:
            data[self.name][child.name] = child.as_json()[child.name]
        return data

def traversal(node):
    children = mc.sets(node.name, q=1)
    for child in children:
        if mc.objectType(child) == 'objectSet':
            childNode = SetsNode(child)
            childNode.parent = node
            traversal(childNode)
        else:
            node.items.append(child)

def export_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def main(root_node, file_path):
    # create node and traverse it to get sets hierarchy data in the maya scene
    root = SetsNode(root_node)
    traversal(root)

    # output data to specific path as json file
    # file_path = r'N:/tmp/test.json'
    data = root.as_json()
    export_json(file_path, data)
    print(f'complete')

# main(root_node='top_set', file_path=r'N:/tmp/test.json')