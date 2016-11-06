from Node import Node
import pprint
from Queue import *

''' Developed by Andy Baay at Davidson College based on Kuo-Chung Tai's
1979 paper, 'The Tree-to-Tree Correction Problem'.'''

class TreeWrapper:

    DEBUG = True
    UPPER_SENTINEL= 100000

    def __init__(self, root):
        self.root = root
        self.node = [None]
        self.parent = [None]
        self.__numberNodes(self.root, None)

        self.__debug()



    ######################
    ## ACCESSOR METHODS ##
    ######################

    def getNumNodes(self):
        return len(self.node) - 1


    def getParentNum(self, index):
        try:
            return self.parent[index]
        except:
            return None

    def getChildOnPath(self, current, bottom):
        new_bottom = self.getParentNum(bottom)
        if new_bottom == None:
            return None
        if new_bottom == current:
            return bottom
        else:
            self.getChildOnPath(current, new_bottom)

    ######################
    ## INSTANCE METHODS ##
    ######################

    def compareTreeTo(self, tree2):

        self.nodeNum = self.getNumNodes() + 1
        t2nodes = tree2.getNumNodes() + 1

        # A six dimensional array to hold all combinatorial count varibles
        # for generating the tree mappings. E[self.nodes][][][t2nodes][][]
        E = [[[[[[None] * t2nodes] * t2nodes] * t2nodes] * self.nodeNum] * \
            self.nodeNum] * self.nodeNum

        mapping = []
        skipped = Queue()

        for i in range(1, self.getNumNodes() + 1):
            for j in range(1, tree2.getNumNodes() + 1):
                u = i
                while u != None:
                    s = u
                    while s != None:
                        v = j
                        while v != None:
                            t = v
                            while t != None:
                                if (s == u == i and t == v == j):
                                    #mapping.append((s,u,i,t,v,j))
                                    #mapping.append((i, j))
                                    #print("Trying %d, %d" % (i,j))
                                    E[s][u][i][t][v][j] = self._r(self.node[i],
                                                                  tree2.node[j])
                                elif (s == u == i) or (t < v == j):
                                    #mapping.append((i, j))
                                    #print("Skipping %d, %d" % (i, j))
                                    #skipped.put((s,u,i,t,v,j))
                                    print "Pulling: ",tree2.getParentNum(j), \
                                        (j-1), E[s][u][i][t][
                                        tree2.getParentNum(j)][j - 1]
                                    E[s][u][i][t][v][j] = E[s][u][i][t][tree2.getParentNum(j)][j - 1] \
                                                          + self._r(None, tree2.node[j])
                                elif (s < u == i) or (t == v == j):
                                    E[s][u][i][t][v][j] = E[s][
                                                              self.getParentNum(i)][i - 1][t][v][j] \
                                                          + self._r(self.node[i],  None)
                                else:

                                    # x is the son of u on the path to i
                                    x = self.getChildOnPath(u, i)
                                    y = tree2.getChildOnPath(v, j)

                                    e1 = self.UPPER_SENTINEL
                                    e2 = self.UPPER_SENTINEL
                                    e3 = self.UPPER_SENTINEL
                                    if x != None:
                                        e1 = E[s][x][i][t][v][j]

                                    if y != None:
                                        e2 = E[s][u][i][t][y][j]

                                    if x != None and y != None:
                                        print "Case 4, Addition: "
                                        e3 = E[s][u][x-1][t][v][y-1] +\
                                            E[x][x][i][y][y][j]

                                    E[s][u][i][t][v][j] = min(e1,e2,e3)

                                if s == 1 and t == 1:
                                    print("E[%d][%d][%d][%d][%d][%d] = %.2f" % (
                                     s,u,i,t,v,j,E[s][u][i][t][v][j]))
                                t = tree2.parent[t]
                            v = tree2.parent[v]
                        s = self.parent[s]
                    u = self.parent[u]

        #Now find the minimum mapping from all the submaps, 0 indices are empty

        min_M = [[0]* t2nodes]* self.nodeNum
        min_M[1][1] = 0
        for i in range(1, self.getNumNodes() + 1):
            for j in range(1, tree2.getNumNodes() + 1):
                min_M[i][j] = self.UPPER_SENTINEL
                s = self.getParentNum(i)
                while s != None:
                    t = tree2.getParentNum(j)
                    while t != None:
                        temp = self.UPPER_SENTINEL
                        if self.getParentNum(i) != None and \
                                tree2.getParentNum(j) != None:
                            r_val = self._r(self.node[s], tree2.node[t])
                            if r_val == None: r_val = 0
                            temp = min_M[s][t] + E[s][self.getParentNum(i)][
                                i-1][t][tree2.getParentNum(j)][j-1] - r_val
                        min_M[i][j] = min(temp, min_M[i][j])
                        t = tree2.getParentNum(t)
                    min_M[i][j] = min_M[i][j] + self._r(self.node[i],
                                                        tree2.node[j])
                    s = self.getParentNum(s)
        print min_M[8][3]
        return mapping



    ######################
    ## INTERNAL METHODS ##
    ######################

    ''' Scoring method'''
    def _r(self, node, t2node):
        if node == None or t2node == None:
            return -.5
        if node.data == t2node.data:
            return 5
        else:
            return 2


    def __numberNodes(self, node, parent):
        # update lists with the current node's info
        self.node.append(node)
        self.parent.append(parent)
        #node.setNum(len(self.node) - 1)

        # set new_parent to the index we just placed current node into before
        # recursively calling the child nodes
        new_parent = len(self.node) - 1

        for child in node.getChildren():
            self.__numberNodes(child, new_parent)
        return

    def __debug(self):
        print "Node : Parent : Tree"
        print "--------------------"
        for i in range(0, len(self.node)):
            print "  %d  :  %s  : %s" % (i, str(self.parent[i]), self.node[i])