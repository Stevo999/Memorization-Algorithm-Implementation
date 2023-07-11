class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.memo = None

class MemoizingBST:
    def __init__(self, ordering_function, memo_function):
        self.root = None
        self.ordering_function = ordering_function
        self.memo_function = memo_function

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return

        self._insert_recursive(self.root, key, value)

    def _insert_recursive(self, node, key, value):
        if self.ordering_function(key, node.key):
            if node.left:
                self._insert_recursive(node.left, key, value)
            else:
                node.left = Node(key, value)
        else:
            if node.right:
                self._insert_recursive(node.right, key, value)
            else:
                node.right = Node(key, value)

        # Update memo value of the node
        node.memo = self.memo_function(
            node.value,
            node.left.memo if node.left else None,
            node.right.memo if node.right else None
        )

    def query(self, start_key, end_key):
        return self._query_recursive(self.root, start_key, end_key)

    def _query_recursive(self, node, start_key, end_key):
        if not node:
            return None

        if start_key <= node.key <= end_key:
            return node.memo
        elif node.key < start_key:
            return self._query_recursive(node.right, start_key, end_key)
        else:
            return self._query_recursive(node.left, start_key, end_key)


def example_ordering_function(a, b):
    # Example ordering function for persons ordered by age
    return a < b

def example_memo_function(value, left_memo, right_memo):
    # Example memo function to find the maximum income within a range
    memos = [m for m in (left_memo, right_memo) if m is not None]
    return max([value] + memos) if memos else value

# Usage example
tree = MemoizingBST(example_ordering_function, example_memo_function)
tree.insert(20, 50000)
tree.insert(18, 35000)
tree.insert(25, 70000)
tree.insert(22, 60000)
tree.insert(30, 80000)

start_key = float(input("Enter the start key: "))
end_key = float(input("Enter the end key: "))

result = tree.query(start_key, end_key)
print(f"Maximum income between {start_key} and {end_key}: {result}")
