import hashlib
import random

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
        else:
            self._insert(key, value, self.root)

    def _insert(self, key, value, node):
        if key < node.key:
            if not node.left:
                node.left = Node(key, value)
            else:
                self._insert(key, value, node.left)
        else:
            if not node.right:
                node.right = Node(key, value)
            else:
                self._insert(key, value, node.right)

    def search(self, key):
        return self._search(key, self.root)

    def _search(self, key, node):
        if not node:
            return None
        elif key == node.key:
            return node.value
        elif key < node.key:
            return self._search(key, node.left)
        else:
            return self._search(key, node.right)

class RainbowTable:
    def __init__(self):
        self.password_space = ''
        self.password_length = 0
        self.chain_length = 0
        self.num_chains = 0
        self.rainbow_table = []

    def init(self, password_space, password_length, chain_length, num_chains):
        self.password_space = password_space
        self.password_length = password_length
        self.chain_length = chain_length
        self.num_chains = num_chains
        self.build_table()

    def build_table(self):
        # Implement the hash function (MD5)
        def hash_password(password):
            hashed_password = hashlib.md5(password.encode())
            return hashed_password.hexdigest()

        # Define the reduction function (takes a portion of the hash value and maps it to a character in the password space)
        def reduce_password(hashed_password, i):
            reduced_password = ''
            for j in range(self.password_length):
                index = (i + j) % len(hashed_password)
                char_index = int(hashed_password[index], 16)
                reduced_password += self.password_space[char_index % len(self.password_space)]
            return reduced_password

        # Generate chains (start with a random password, hash it, and reduce the hash value to obtain a new password)
        def generate_chain():
            start_password = ''.join(random.choice(self.password_space) for i in range(self.password_length))
            end_password = start_password
            for i in range(self.chain_length):
                hashed_password = hash_password(end_password)
                reduced_password = reduce_password(hashed_password, i)
                end_password = reduced_password
            return (start_password, end_password)

        # Build the rainbow table (generate multiple chains starting from different random passwords)
        for i in range(self.num_chains):
            chain = generate_chain()
            self.rainbow_table.append(chain)

        # Sort the rainbow table based on the end password values
        self.rainbow_table.sort(key=lambda x: x[1])

    def print_table(self):
        for chain in self.rainbow_table:
            print(f"Start password: {chain[0]}")
            print(f"End password: {chain[1]}")

    def search(self, end_password):
        # Binary search the rainbow table for the given end password
        low = 0
        high = len(self.rainbow_table) - 1
        while low <= high:
            mid = (low + high) // 2
            if end_password == self.rainbow_table[mid][1]:
                # Found the chain with the given end password
                return self.rainbow_table[mid][0]
            elif end_password < self.rainbow_table[mid][1]:
                high = mid - 1
            else:
                low = mid + 1
        # The given end password is not in the rainbow table
        return None

 # create a rainbow table instance and initialize it
rt = RainbowTable()
rt.init('abcdefghijklmnopqrstuvwxyz', 6, 1000, 100)
# print the rainbow table
rt.print_table()
# search for an end password
end_password = input("Enter end password: ")
start_password = rt.search(end_password)
if start_password:
    print(f"Found start password: {start_password}")
else:
    print("End password not found in the rainbow table")