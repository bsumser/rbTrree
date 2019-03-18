#binarySearchTree is a class for a binary search tree (BST)
# when called, a BST is initialized with no root and size 0.
# size keeps track of the number of nodes in the tree
from Node import RB_Node

class RedBlackTree:
    # initialize root and size
    def __init__(self):
        self.root = None
        self.size = 0
        
        # All leaf nodes point to self.sentinel, rather than 'None'
        # Parent of root should also be self.sentinel
        self.sentinel = RB_Node(None, color = 'black')
        self.sentinel.parent = self.sentinel
        self.sentinel.leftChild = self.sentinel
        self.sentinel.rightChild = self.sentinel

    '''
    Free Methods
    '''

    def sentinel(self):     
        return self.sentinel

    def root(self):
        return self.root

    def __iter__(self):
        # in-order iterator for your tree
        return self.root.__iter__()

    def getKey(self, key):
        # expects a key
        # returns the key if the node is found, or else raises a KeyError

        if self.root:
            # use helper function _get to find the node with the key
            res = self._get(key, self.root)
            if res: # if res is found return the key
                return res.key
            else:
                raise KeyError('Error, key not found')
        else:
            raise KeyError('Error, tree has no root')

    
    def getNode(self, key):
        # expects a key
        # returns the RB_Node object for the given key
        
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res
            else:
                raise KeyError('Error, key not found')
        else:
            raise KeyError('Error, tree has no root')

    # helper function _get receives a key and a node. Returns the node with
    # the given key
    def _get(self, key, currentNode):
        if currentNode is self.sentinel: # if currentNode does not exist return None
            print("couldnt find key: {}".format(key))
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            # recursively call _get with key and currentNode's leftChild
            return self._get( key, currentNode.leftChild )
        else: # key is greater than currentNode.key
            # recursively call _get with key and currentNode's rightChild
            return self._get( key, currentNode.rightChild )

    
    def __contains__(self, key):
        # overloads the 'in' operator, allowing commands like
        # if 22 in rb_tree:
        # ... print('22 found')

        if self._get(key, self.root):
            return True
        else:
            return False
    
    def delete(self, key):
        # Same as binary tree delete, except we call rb_delete fixup at the end.

        z = self.getNode(key)
        if z.leftChild is self.sentinel or z.rightChild is self.sentinel:
            y = z
        else:
            y = z.findSuccessor()
        
        if y.leftChild is not self.sentinel:
            x = y.leftChild
        else:
            x = y.rightChild
        
        if x is not self.sentinel:
            x.parent = y.parent

        if y.parent is self.sentinel:
            self.root = x

        else:
            if y == y.parent.leftChild:
                y.parent.leftChild = x
            else:
                y.parent.rightChild = x

        if y is not z:
            z.key = y.key
    
        if y.color == 'black':
            self._rb_Delete_Fixup(x)

    def traverse(self, order = "in-order", top = -1):
        # Same a BST traverse
        if top is -1:
            top = self.root
            last_call = True
        
        last_call = False

        if top is not self.sentinel :
            if order == "in-order":
                self.traverse(order, top.leftChild)
                print(top.key),
                self.traverse(order, top.rightChild)

            if order == "pre-order":
                print(top.key),
                self.traverse(order, top.leftChild)
                self.traverse(order, top.rightChild)

            if order == "post-order":
                self.traverse(order, top.leftChild)
                self.traverse(order, top.rightChild)
                print(top.key),

        if last_call:
            print

    '''
    Required Methods Begin Here
    '''

    def insert(self, key):
        # add a key to the tree.Don't forget to fix up the tree and balance the nodes.
        #root does not exist yet 

        y = self.sentinel
        x = self.root
        z = RB_Node(key, self.sentinel, self.sentinel, self.sentinel, 'red')

        #insert case for when tree is empty
        if self.size == 0:
            self.root = z
            self.size += 1
            print key 
            print 'key inserted as root'

        else:
            while x != self.sentinel:
                y = x
                if z.key < x.key:
                    x = x.leftChild
                else:
                    x = x.rightChild
            z.parent = y
            if y == self.sentinel:
                self.root = z # case for tree being empty
            elif z.key < y.key:
                y.leftChild = z
                print key 
                print 'key inserted as a left child'
            else:
                y.rightChild = z
                print key 
                print 'key inserted as a right child'
            z.leftChild = self.sentinel
            z.rightChild = self.sentinel
            z.color = 'red'
            self.size += 1

                    
    def _rbInsertFixup(self, z):
        # write a function to balance your tree after inserting
        
        #case 0 - z is the root
        #color z black

        #case 1 - z's uncle is red
        #recolor z's grandparent, parent, and uncle black

        #case 2 - z's uncle is black (triangle)
        #case 2a - z is left child and z.parent is right child
            #single rotate right z.parent
        #case 2b - z is right child and z.parent is left child
            #single rotate left z.parent

        #case 3 - z's uncle is black (line)
        #z and z.parent are both the same child to their
        #respective parents

            #case 3a - z and z.parent are left children
                #rotate z.grandparent right
                #recolor original z.parent and z.grandparent
            #case 3a - z and z.parent are right children
                #rotate z.grandparent left
                #recolor original z.parent and z.grandparent

        pass

    def _rb_Delete_Fixup(self, x):
        # receives a node, x, and fixes up the tree, balancing from x.
        pass

    def leftRotate(self, currentNode):
        # perform a left rotation from a given node
        y = x.rightChild #set y
        x.rightChild = y.leftChild #turn y's subtree into x's right subtree

        if y.leftChild != self.sentinel:
            y.leftChild.parent = x
        y.parent = x.parent #link x's parent to y
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.leftChild:
            x.parent.leftChild = y
        else:
            x.parent.rightChild = y
        y.leftChild = x
        x.parent = y

    def rightRotate(self, currentNode):
        # perform a right rotation from a given node
        y = x.leftChild #set y
        x.leftChild = y.rightChild #turn y's subtree into x's right subtree

        if y.rightChild != self.sentinel:
            y.rightChild.parent = x
        y.parent = x.parent #link x's parent to y
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.rightChild:
            x.parent.rightChild = y
        else:
            x.parent.leftChild = y
        y.rightChild = x
        x.parent = y

    '''
    Optional handy methods that you can imagine can start here
    '''

