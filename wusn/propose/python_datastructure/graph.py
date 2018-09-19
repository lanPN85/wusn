from wusn.propose.python_datastructure.queue import Queue
from wusn.propose.python_datastructure.stack import Stack


class Vertex:
    def __init__(self, data=None):
        self.data = data
        self.adjacent_vertices = []
        self.list_edge = []

    def add_edge(self, other, weight=None, capacity=0, flow=0, un_dir=False):
        if type(other) != type(self):
            return
        edge = Edge()
        for temp in self.adjacent_vertices:
            if temp.data == other.data:
                return
        edge.connect(self, other, weight, capacity=capacity, flow=flow)
        self.list_edge.append(edge)
        self.adjacent_vertices.append(other)
        if un_dir:
            other.add_edge(self, weight=weight)

    def check_adjacent(self, other):
        if type(other) != type(self):
            return False
        for element in self.adjacent_vertices:
            if element.data == other.data:
                return True
        return False

    def get_adjacency(self):
        return self.adjacent_vertices

    def get_edges(self):
        return self.list_edge
    
    def get_edge(self, vertex):
        for edge in self.list_edge:
            if edge.second_vertex == vertex:
                return edge
        return None

    def delete_edge(self, vertex):
        for edge in self.list_edge:
            if edge.second_vertex.data == vertex.data:
                self.list_edge.remove(edge)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    def __eq__(self, other):
        if type(other) is not Vertex:
            return False
        elif self.data == other.data:
            return True
        else:
            return False


class Edge:
    def __init__(self, first_vertex=None, second_vertex=None, weight=None, flow=0,capacity=0):
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.weight = weight
        self.flow = flow
        self.capacity=capacity

    def connect(self, first_vertex, second_vertex, weight=None, flow=0, capacity=0):
        self.first_vertex = first_vertex
        self.second_vertex = second_vertex
        self.flow = flow
        self.capacity = capacity
        if weight is None:
            self.weight = 1
        else:
            self.weight = weight


class Graph:
    def __init__(self):
        self.vertices = []

    def get_adjacency(self, data):
        for vertex in self.vertices:
            if vertex.data == data:
                return vertex.get_adjacency()

    def add_vertex(self, data):
        new_vertex = Vertex(data=data)
        for temp in self.vertices:
            if temp.data == data:
                return None
        self.vertices.append(new_vertex)

    def find_vertex(self, data):
        for temp in self.vertices:
            if temp.data == data:
                return temp

    def add_edge(self, data1, data2, weight=1, un_dir=True):
        vertex1 = self.find_vertex(data1)
        vertex2 = self.find_vertex(data2)
        vertex1.add_edge(vertex2, weight=weight, un_dir=un_dir)

    def get_edge(self, index1, index2):
        vertex1 = self.vertices[index1]
        vertex2 = self.vertices[index2]
        return vertex1.get_edge(vertex2)

    def check_adjacent(self, data1, data2):
        vertex1 = self.find_vertex(data1)
        vertex2 = self.find_vertex(data2)
        if vertex1 is None or vertex2 is None:
            return False
        if vertex1.check_adjacent(vertex2):
            return True
        else:
            return False

    def dfs(self, data=None, num=0):
        if data is None and num is None:
            return None
        if data is not None:
            vertex = self.find_vertex(data)
            if vertex is None:
                return None
            start = self.vertices.index(vertex)
        else:
            start = num
        temp_stack = Stack()
        visit = []
        count = 0
        for vertex in self.vertices:
            visit.append(False)
        temp_stack.push(start)
        while not temp_stack.is_empty():
            index = temp_stack.pop()
            if index is None:
                return
            if not visit[index]:
                visit[index] = True
                print(self.vertices[index])
                for vertex in self.vertices[index].get_adjacency():
                    index2 = self.vertices.index(vertex)
                    if index2 is None:
                        continue
                    if not visit[index2]:
                        temp_stack.push(index2)

    def bfs(self, data=None, num=0):
        if data is None and num is None:
            return None
        if data is not None:
            vertex = self.find_vertex(data)
            if vertex is None:
                return None
            start = self.vertices.index(vertex)
        else:
            start = num
        visit = []
        for vertex in self.vertices:
            visit.append(False)
        index_queue = Queue()
        index_queue.enqueue(start)
        while not index_queue.is_empty():
            index = index_queue.de_queue()
            if not visit[index]:
                visit[index] = True
                print(self.vertices[index])
                for vertex in self.vertices[index].get_adjacency():
                    index2 = self.vertices.index(vertex)
                    if not visit[index2]:
                        index_queue.enqueue(index2)

    def __str__(self):
        return self.vertices





# 
# graph = Graph()
# graph.add_vertex(5)
# graph.add_vertex(6)
# list_vertex = graph.vertices
# print(list_vertex)
# print("\n")
# graph.add_vertex(5)
# graph.add_vertex(6)
# graph.add_vertex(7)
# print(graph.vertices)
# print("add edge test")
# graph.add_edge(5, 6)
# graph.add_edge(6, 7)
# graph.add_edge(7, 8)
# v = graph.find_vertex(5)
# new_list = v.get_adjacency()
# print(new_list)
# v = graph.find_vertex(7)
# new_list = v.get_adjacency()
# print(new_list)
# v = graph.find_vertex(6)
# new_list = v.get_adjacency()
# print(new_list)
# graph.add_vertex(9)
# graph.add_vertex(10)
# graph.add_vertex(8)
# graph.add_edge(8, 9)
# graph.add_edge(9, 10)
# graph.add_edge(7, 8)
# graph.add_edge(8, 5)
# print("bfs")
# graph.bfs(5)
# print("dfs")
# graph.dfs(5)


