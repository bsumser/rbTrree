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

        if x == None:
            self.root = z
            x = self.root

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
            #print key, 
            #print 'inserted as a left child of ',
            #print y.key
        else:
            y.rightChild = z
            #print key, 
            #print ' inserted as a right child of',
            #print y.key
        z.leftChild = self.sentinel
        z.rightChild = self.sentinel
        z.color = 'red'
        self.size += 1
        self._rbInsertFixup(z)
                    
    def _rbInsertFixup(self, z):
        #print 'insert fixedup called' 
        # write a function to balance your tree after inserting

        while z.parent.color == 'red':
            if z.parent == z.parent.parent.leftChild:
                y = z.parent.parent.rightChild
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.rightChild:
                        z = z.parent
                        self.leftRotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.rightRotate(z)
            else:
                y = z.parent.parent.leftChild
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else:
                    if z == z.parent.leftChild:
                        z = z.parent
                        self.rightRotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.leftRotate(z.parent.parent)
        #case 0 - z is the root
        #color z black
        self.root.color = 'black'

    def _rb_Delete_Fixup(self, x):
        #print 'delete fixup called' 
        # receives a node, x, and fixes up the tree, balancing from x.
        while x != self.root and x.color == 'black':
            if x == x.parent.leftChild:
                w = x.parent.rightChild
                if w.color == 'red':
                    w.color = 'black'       #case 1: x's sibling w is red
                    x.parent.color = 'red'
                    self.leftRotate(x.parent)
                    w = x.parent.rightChild
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'         #case 2:x's sibling w is black and both of
                    x = x.parent            # w's children are black
                elif w.rightChild.color == 'black':
                    w.leftChild.color = 'black'         #case 3:x's sibling w is black, w.leftChild is red
                    w.color = 'red'                     # w.rightChild is black
                    self.rightRotate(w)
                    w = x.parent.rightChild
                    w.color = x.parent.color            #case 4:x's sibling is black, w's right child is red
                    x.parent.color = 'black'
                    w.rightChild.color = 'black'
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                w = x.parent.leftChild
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.rightRotate(x.parent)
                    w = x.parent.leftChild
                if w.rightChild.color == 'black' and w.leftChild.color == 'black':
                    w.color = 'red'
                    x = x.parent
                elif w.leftChild.color == 'black':
                    w.rightChild.color = 'black'
                    w.color = 'red'
                    self.leftRotate(w)
                    w = x.parent.leftChild
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.leftChild.color = 'black'
                    self.rightRotate(x.parent)
                    x = self.root
        x.color = 'black'


    def leftRotate(self, x):
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

    def rightRotate(self, x):
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

