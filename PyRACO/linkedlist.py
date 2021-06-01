import struct_graph as strgr


class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

class Link:
    def __init__(self):
        self.head = None

    def append(self,data):
        if self.head:
            pointer = self.head
            while (pointer.next):
                pointer = pointer.next
            pointer.next = Node(data)
        else:
            self.head = Node(data)

    def __getitem__(self,index):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("Indice errado")

        if pointer:
            return pointer.data
        
