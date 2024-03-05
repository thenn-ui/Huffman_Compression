

class TreeNode:
    key = None
    lch = None
    rch = None
    parent = None


    def __init__(self, value):
        self.key = value
        self.lch = None
        self.rch = None
        self.parent = None


    def set_lchild(self, lchild):
        self.lch = lchild

    def set_rchild(self, rchild):
        self.rch = rchild

    def set_parent(self, par):
        self.parent = par


class StarNode(TreeNode):
    
    def __init__(self):
        #del self.key
        self.lch = None
        self.rch = None
        self.parent = None


class BinaryTree:
    root = None
    num_nodes = None

    def __init__(self):
        self.root = StarNode()
        self.num_nodes = 0

    def set_root(self, rtnode, nnodes):
        self.root = rtnode
        self.num_nodes = nnodes

    def traverse_inorder(self, node):
        if node.lch is not None:
            self.traverse_inorder(node.lch)

        if not isinstance(node, StarNode):
            print(node.key)

        if node.rch is not None:
            self.traverse_inorder(node.rch)

    

class PriorityQueue(BinaryTree):


    def get_insertpoint(self):
        queue = []

        queue.append(self.root)

        while(queue != []):
            node = queue.pop(0)
            if isinstance(node.lch, StarNode):
                return node.lch
            elif isinstance(node.rch, StarNode):
                return node.rch

            if node.lch is not None:
                queue.append(node.lch)

            if node.rch is not None:
                queue.append(node.rch)

    def get_deletepoint(self):
        queue = []

        queue.append(self.root)

        point = self.root

        while(queue != []):
            node = queue.pop(0)

            if not isinstance(node.lch, StarNode):
                queue.append(node.lch)
                point = node.lch

            if not isinstance(node.rch, StarNode):
                queue.append(node.rch)
                point = node.rch
        
        return point


    def percolate_down(self, node):

        while(not isinstance(node.lch, StarNode) and not isinstance(node.rch, StarNode)):
            print("Node - ", node, "lch - ", node.lch, "rch - ", node.rch)
            if node.key > node.lch.key and node.key > node.rch.key:
                if(node.lch.key < node.rch.key):
                    node.key, node.lch.key = node.lch.key, node.key
                    node = node.lch
                else:
                    node.key, node.rch.key = node.rch.key, node.key
                    node = node.rch
            elif node.key > node.lch.key:
                node.key, node.lch.key = node.lch.key, node.key
                node = node.lch
            elif node.key < node.rch.key:
                node.key, node.rch.key = node.rch.key, node.key
                node = node.rch
            else:
                break


        if(not isinstance(node.lch, StarNode)):
            if node.key > node.lch.key:
                node.lch.key, node.key = node.key, node.lch.key



    def add(self, key):

        '''Maintain the structure property'''
        node = TreeNode(key)
        node.set_lchild(StarNode())
        node.set_rchild(StarNode())
        node.lch.parent = node
        node.rch.parent = node

        if isinstance(self.root, StarNode):
            self.root = node
            
        else:
            tempnode = self.get_insertpoint()
            if isinstance(tempnode, StarNode):
                node.parent = tempnode.parent
                if tempnode.parent.lch == tempnode:
                    tempnode.parent.lch = node

                else:
                    tempnode.parent.rch = node

                del tempnode

        '''Maintain the key order property for min heap'''
        while(node.parent is not None):
            if node.key < node.parent.key:
                node.parent.key, node.key = node.key, node.parent.key
            else:
                break

            node = node.parent

    def pop(self):

        tempnode = self.get_deletepoint()
        self.root.key, tempnode.key = tempnode.key, self.root.key

        if tempnode.parent.lch == tempnode:
            tempnode.parent.lch = StarNode()
        else:
            tempnode.parent.rch = StarNode()

        tempnode.parent = None
        self.percolate_down(self.root)

        return tempnode.key
        

    def isEmpty(self):
        if isinstance(self.root, StarNode):
            return True
        
        return False
            

if __name__ == '__main__':

    node1 = TreeNode(5)
    node2 = TreeNode(6)
    node3 = TreeNode(7)
    node3.set_lchild(node1)
    node3.set_rchild(node2)
    node2.set_parent(node3)
    node1.set_parent(node3)

    tree = BinaryTree()
    tree.set_root(node3, 3)

    tree.traverse_inorder(tree.root)

 
    print('===================')

    pq = PriorityQueue()

    pq.add(40)
    pq.add(11)
    pq.add(3)
    pq.add(7)
    pq.add(12)
    pq.add(1)
    pq.add(23)

    pq.traverse_inorder(pq.root)

    print(pq.pop())

    print("[POPPED]")

    pq.traverse_inorder(pq.root)

    print("[Final Phase]")

    while(not pq.isEmpty()):
        print(pq.pop())






