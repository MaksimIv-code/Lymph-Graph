class Node:
    def __init__(self, node_id, complex_param):
        self.node_id = node_id
        self.complex_param = complex_param
        self.left = None
        self.right = None
        self.height = 1


#Recursive AVL tree with some basic methods and methods that will be used in the visualization
class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance_factor(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node):
        if node:
            node.height = max(self.height(node.left), self.height(node.right)) + 1

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def insert(self, node_id, complex_param):
        self.root = self._insert(self.root, node_id, complex_param)

    def _insert(self, node, node_id, complex_param):
        if not node:
            return Node(node_id, complex_param)

        if complex_param < node.complex_param:
            node.left = self._insert(node.left, node_id, complex_param)
        elif complex_param > node.complex_param:
            node.right = self._insert(node.right, node_id, complex_param)
        else:
            return node  

        self.update_height(node)
        balance = self.balance_factor(node)

        if balance > 1 and complex_param < node.left.complex_param:
            return self.rotate_right(node)
        if balance < -1 and complex_param > node.right.complex_param:
            return self.rotate_left(node)
        if balance > 1 and complex_param > node.left.complex_param:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance < -1 and complex_param < node.right.complex_param:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def get_top_n(self, n):
        result = []
        self._inorder(self.root, result, n)
        return result[:n]

    def _inorder(self, node, result, n):
        if node and len(result) < n:
            self._inorder(node.right, result, n) 
            if len(result) < n:
                result.append((node.node_id, node.complex_param))
            self._inorder(node.left, result, n)