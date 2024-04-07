import math

class Node[K,V]:
    def __init__(self, key:K, value:V) -> None:
        self.left:Node[K,V] = None
        self.right:Node[K,V] = None
        self.key:K = key
        self.value:V = value

class Tree[K,V]:
    def __init__(self):
        self.entries = dict[K,V]()
        self._compiled = False

        self.root:Node[K,V] = None

    def addEntry(self, key:K, value:V):
        if self._compiled:
            raise SyntaxError("Tree is already compiled")
        self.entries[key] = value

    def compile(self):
        if self._compiled:
            raise SyntaxError("Tree is already compiled")
        
        self.root = Tree._compile(self.entries)
        self._compiled = True

    def search(self, key:K) -> V:
        if not self._compiled:
            self.compile()
        return Tree._search(key, self.root)

    @staticmethod
    def _search(key:K, node:Node[K,V]) -> V:
        if node == None:
            raise ValueError("Search found a non-existant node")
        
        if (node.left == None) and (node.right == None):
            return node.value
        else:
            if key < node.key:
                return Tree._search(key, node.left)
            else:
                return Tree._search(key, node.left)

    @staticmethod
    def _compile(entries:dict[K,V]) -> Node[K,V]:
        if len(entries) == 0:
            return None
        elif len(entries) == 1:
            item = entries.popitem()
            return Node(item[0], item[1])
        else:
            sortedKeys = sorted(entries.keys())

            if len(entries) == 2:
                a = entries.popitem()
                b = entries.popitem()

                node = Node((a[0] + b[0]) / 2, None)

                if a[0] < b[0]:
                    node.left = Node(*a)
                    node.right = Node(*b)
                else:
                    node.left = Node(*b)
                    node.right = Node(*a)
                return node
            else:
                medianKey = sortedKeys[math.floor(len(entries) / 2) ]

                node = Node(medianKey, None)
                node.left = Tree._compile(dict({k: v for k,v in entries.items() if k < medianKey }))
                node.right = Tree._compile(dict({k: v for k,v in entries.items() if k >= medianKey }))

                return node

    def prettyPrint(self):
        Tree._prettyPrint(self.root)

    @staticmethod
    def _prettyPrint(root:Node[K,V]=None, depth=0):
        if not root:
            return
        prefix = "".join(["|" for _ in range(depth)])

        if root.left == None and root.right == None:
            print("{}{}".format(prefix, root.value))
        else:
            print("{}if X < {}:".format(prefix, root.key))
            Tree._prettyPrint(root.left, depth+1)
            print("{}if X >= {}:".format(prefix, root.key))
            Tree._prettyPrint(root.right, depth+1)
