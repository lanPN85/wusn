from wusn.propose.python_datastructure.node import Node


class SingleLinkList:
    def __init__(self):
        self.root = None
        self.current = None

    def insert_at_root(self, data):
        if self.root is None:
            self.root = Node(data)
            self.current = self.root
            return
        new_node = Node(data)
        new_node.next = self.root
        self.root = new_node

    def insert_at_current(self, data):
        if self.root is None:
            return self.insert_at_root(data)
        new_node = Node(data)
        self.current.next = new_node
        self.current = self.current.next

    def search(self, data):
        if self.root is None:
            return None
        new_node = self.root
        while new_node is not None:
            if new_node.data == data:
                return new_node
            new_node = new_node.next
        return

    def search_prev_node(self,obj):
        if type(obj) is Node:
            is_node = True
        else:
            is_node = False
        new_node = self.root
        while new_node is not None:
            if is_node:
                if new_node.next == obj:
                    return new_node
            else:
                if new_node.next.data == obj:
                    return new_node

            new_node = new_node.next
        return None

    def delete_at_root(self):
        if self.root is None:
            print("empty list")
            return
        data = self.root.data
        self.root = self.root.next
        return data

    def delete_current(self):
        if self.root is None:
            print("empty list")
            return
        data = self.current.data
        self.current = self.search_prev_node(self.current)
        if self.current is not None:
            self.current.next = None
        return data

    def delete_node(self, data):
        if self.root is None:
            print("Empty list")
            return
        temp_node = self.search(data)
        if temp_node is None:
            print("data not found")
            return
        if temp_node is self.current:
            self.delete_current()
            return
        prev_temp = self.search_prev_node(temp_node)
        if prev_temp is None:
            data = temp_node.data
            return data
        prev_temp.next = temp_node.next
        data = temp_node.data
        temp_node = None
        return data

    def is_empty(self):
        return self.root is None

    def __str__(self):
        data = ""
        new_node = self.root
        while new_node is not None:
            data += str(new_node.data)
            data += " "
            new_node = new_node.next
        return data



# list1 = SingleLinkList();
# list1.insert_at_root(5);
# list1.insert_at_root(6);
# list1.insert_at_root(7);
# list1.insert_at_current(8);
# list1.delete_node(8);
# print(list1);
# list1.delete_at_root();
# list1.delete_current();
# print(list1);
#


