
class Node:

    def __init__(self, data):
        self.data = data
        self.parent = None
        self.children = []
        # self.num = -1

    '''
    def setNum(self, newNum):
        self.num = newNum

    def getNum(self):
        return self.num
    '''
    def addChild(self, node):
        self.children.append(node)
        node.parent = self

    def removeChild(self, node):
        index = self.children.find(node)
        if index != False:
            self.children[index] = None


    def hasChild(self, node):
        index = self.children.find(node)
        if index != False:
            return self.children[index]
        return False

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent

    def __str__(self):
        if len(self.children) == 0: return str(self.data)
        st = str(self.data) + "=["
        for node in self.children:
            st += str(node) + ""
        return st + "]"