import maya.cmds as mc
def getSG():
    list = mc.ls(type="shadingEngine")
    return list
    
x = getSG()
print(x)

def getShadedNodes(input):
    return mc.listConnections(input, type='mesh')

getShadedNodes(x)

for sg in x[3:]:
    mtlname = mc.listConnections(f'{sg}.surfaceShader', d=True)[0]
    mc.rename(sg,f'{mtlname}_SG')

mesh = 'c_skin_lo'
mc.select(mesh)

mc.listRelatives(mc.ls(sl=1))

mc.listConnections(f'{mesh}Shape', type='shadingEngine', source=True)


# get all sets connected to mesh

objectSets = {}
for x in mc.ls(type='objectSet'):
    if mc.objectType(x) == 'objectSet':
        if 'c_skin_lo' in mc.listConnections(x, d=True):
            print(True, x)
            objectSets[x].append("test")
        else:
            print(False, x)
print(objectSets)


setfaces = mc.sets('ears_SG', q=True)
mc.select(setfaces)

mtl = mc.shadingNode('blinn', name='earsSet', asShader=True)
sg = mc.sets(empty=True, renderable=True, noSurfaceShader=True, name=f'{mtl}SG')
mc.connectAttr(f'{mtl}.outColor', f'{sg}.surfaceShader')

for face in setfaces:
mc.sets(setfaces, e=1, fe=sg)
mc.sets(f'{newssg}SG', fe='pCube1')

mc.sets(renderable=1, name='test')



# sets TBD
selectionSets = {
    "NonWatertight_headSet": {
        "",
    },
    'wrap' : {
        'carunclesSet' : "", 
        'mouthSet' : "", 
        'noseSet' : "", 
    },
    'other': {
        'eyesShelf': "", 
        'lipsSet' : "",
        'topoSymmetrySet' : "", 
        'extEarLoopSet' : "", 
    }
}




# 1. select set

# 2. get children of the set

# 3. for each child in set, is it a set or soemthing else?

# 4. if its a set, go back to 2. 

# 5. if its something else, put that into a dictionary {child : something else}

# 6. return dictionary of children and members


input = ['digitalHuman_setGRP']
input = ['set1']


def test(input:list):
    # print(f'{"Begin!":=<80}')
    print(f'input = {input}')
    # if not type(input) == list or type(input) ==  tuple:
    #     raise TypeError('input is not list')
    # # print(len(input))
    # else:
    # input = mc.ls(input)[0]
    if len(input) > 1:
        test(input[1:])
    else:
        children = mc.sets(input, q=1)
        print(f'children = {children}')
        if children == None:
            print(f'no children, return input: {input}')
            return input
        else: 
            print(f'recursion attempt')
            return {input: [test([children[0]]), test(children[1:])]}


print(f'{"Begin!":=<80}')
test(input)


list = [{1 : [2, 3]},2,3,4,5,6,7,8]

def test(input):
    if len(input) == 1:
        return input
    else:
        if not type(input[0]) == list:
            input[0] = [input[0]]
        return test(input[0]) + test(input[1:])

print(test(list))

input = ['set1']
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=1)


def test(input):# -> dict:
    if len(input) == 1:
        if mc.objectType(input) == 'objectSet':
            children = mc.sets(input,  q=1)
            if children:
                return {input[0] : test(children)}
            else:
                return input[0]
    else:
        return test(input[:1]), test(input[1:])

print(f'{"Begin!":=<80}')
pp.pprint(test(input))

{
    'set1': ({
        'set2': {
            'set4': 'set3'
            }},
                ({'set4': 'set3'},
        'set3'))}

input = ['set1']
print(len(input) == 1) #True
print(mc.objectType(input) == 'objectSet') # True 
children = mc.sets(input, q=1)
print(children) # ['set2', 'set3']
# return {'set1' : children}

input = ['set2', 'set3']
print(input[:1])
print(input[1:])
print(len(input) == 1) # False
print(not type(input[0:]) == list) # True
input[0] = [input[0]]
print(input[0])




I cant figure out how to get recursion working.  will come back to it later


print(mc.ls(['set1', 'set2']))

def test(input):
    # topSet = mc.ls(input)
    nodes = mc.ls(input)
    if len(nodes) == 1:
        if mc.objectType(nodes) == 'objectSet':
            # def test(input):
            children = mc.sets(nodes, q=1)
            if children:
                for child in children:
                    print(child)
                    return {nodes[0] : test(child)}
    else:
        return test(nodes[:1]), test(nodes[1:])
print(test(input))








def returnSets(input = list) -> dict:
    if not type(input) == list:
        print(type(input))
        raise TypeError("input is not a list")
    else:
        if len(input) > 1:
            return [returnSets([input[0]]), returnSets(input[1:])]
        else:
            if not mc.objectType(input) == 'objectSet':
                return input
            else:
                children = list(mc.sets(input, q=1))  # get child sets from input
                print(children)
                if len(children) == 0 or children == None: # check if its empty
                    print(f'{input} has no children. Empty Set?')
                    return None
                elif len(children) == 1: # if theres only one, return it
                    print(f'{input}: {returnSets(children)}')
                    return { input : returnSets(children) }
                else:
                    print('you have too many kids')
                    return {
                        input : [returnSets([children[0]]), returnSets(children[1:])]
                        }


returnSets(input)


input = 'set1'

children = mc.sets(input, q=1)

input.items.append(children)



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

def main():
    # create node and traverse it to get sets hierarchy data in the maya scene
    root = SetsNode('set1')
    traversal(root)

    # output data to specific path as json file
    file_path = r'e:/tmp/test.json'
    data = root.as_json()
    export_json(file_path, data)