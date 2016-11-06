from TreeNode import TreeNode, Sugar, Bond
from Node import Node
from TreeWrapper import TreeWrapper as Tree
from pprint import pprint

def main():
    #tree1
    n1 = Node('A')
    n2 = Node('B')
    n3 = Node('C')
    n4 = Node('C')
    n5 = Node('A')
    n6 = Node('B')
    n7 = Node('C')
    n8 = Node('D')
    n7.addChild(n8)
    n5.addChild(n6)
    n5.addChild(n7)
    n2.addChild(n3)
    n2.addChild(n4)
    n1.addChild(n2)
    n1.addChild(n5)


    tree1 = Tree(n1)

    #tree2
    m1 = Node('A')
    m2 = Node('B')
    m3 = Node('C')
    m1.addChild(m2)
    m1.addChild(m3)

    tree2 = Tree(m1)

    tree1.compareTreeTo(tree2)







if __name__ == "__main__":
    main()