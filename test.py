import math


class Node[T]:
    def __init__(self, value:T) -> None:
        self.left:Node[T] = None
        self.right:Node[T] = None
        self.value:T = value

class Tree[T]:
    def __init__(self):
        self.values = set[T]()
        self._compiled = False

        self.root:Node[T] = None

    def addValue(self, value:T):
        if self._compiled:
            raise SyntaxError("Tree is already compiled")
        self.values.add(value)

    def compile(self):
        if self._compiled:
            raise SyntaxError("Tree is already compiled")
        
        self.root = Tree._compile(self.values)
        self._compiled = True

    @staticmethod
    def _compile(possibleValues:list[T]) -> Node[T]:
        if len(possibleValues) == 0:
            return None
        elif len(possibleValues) == 1:
            return Node(possibleValues[0])
        else:
            sortedValues = sorted(possibleValues)

            if len(possibleValues) == 2:
                node = Node((possibleValues[0] + possibleValues[1]) / 2)
                node.left = Node(possibleValues[0])
                node.right = Node(possibleValues[1])

                return node
            else:
                medianValue = sortedValues[math.floor(len(possibleValues) / 2) ]

                node = Node(medianValue)
                node.left = Tree._compile(list([v for v in possibleValues if v < medianValue]))
                node.right = Tree._compile(list([v for v in possibleValues if v >= medianValue]))

                return node

    def prettyPrint(self):
        Tree._prettyPrint(self.root)

    @staticmethod
    def _prettyPrint(root:Node[T]=None, depth=0):
        if not root:
            return
        prefix = "".join(["|" for _ in range(depth)])

        if root.left == None and root.right == None:
            print("{}{}".format(prefix, root.value))
        else:
            print("{}if X < {}:".format(prefix, root.value))
            Tree._prettyPrint(root.left, depth+1)
            print("{}if X >= {}:".format(prefix, root.value))
            Tree._prettyPrint(root.right, depth+1)

if __name__ == "__main__":
    tree = Tree[int]()
    tree.addValue(5)
    tree.addValue(10)
    tree.addValue(15)

    tree.compile()
    tree.prettyPrint()