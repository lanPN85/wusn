from wusn.propose.python_datastructure.graph import *
import queue
from wusn.propose.ecosys import EcoSys
from wusn.commons.output import WusnOutput
from ortools.graph.pywrapgraph import *
import random


class GraphF(Graph):
    def __init__(self):
        Graph.__init__(self)

    def add_edge(self, data1, data2, weight=1, un_dir=True, capacity=0, flow=0):
        vertex1 = self.find_vertex(data1)
        vertex2 = self.find_vertex(data2)
        vertex1.add_edge(vertex2, weight=weight, un_dir=True, capacity=capacity, flow=flow)


def get_re_graph(graph: Graph):
    r_graph = GraphF()
    start = 0
    temp_stack = Stack()
    visit = [False] * len(graph.vertices)
    temp_stack.push(start)
    r_graph.add_vertex(start)
    while not temp_stack.is_empty():
        current = temp_stack.pop()
        for vertex in graph.vertices[current].get_adjacency():
            push_index = graph.vertices.index(vertex)
            r_graph.add_vertex(push_index)
            edge = graph.get_edge(current, push_index)
            r_graph.add_edge(current, push_index, weight=edge.weight, capacity=(edge.capacity - edge.flow))
            if push_index is None:
                continue
            if not visit[push_index]:
                temp_stack.push(push_index)


def calculate_path(graph: Graph, path: list):
    if len(path) != 4:
        print("Error with graph\n")
        exit(0)
    return graph.get_edge(path[1], path[2]).weight


def check_individual(eco_sys, individual: list):
    count = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            count += 1
    if count != eco_sys.relays_num:
        print("not available individual")
        return False
    return True


def list_all_path(eco_sys: EcoSys, individual: list):
    if not check_individual(eco_sys, individual):
        return None
    start = 0
    end = eco_sys.sensors_num + eco_sys.poss_num + 1
    list_index_weight = {} # { index: weight}
    list_index_path = {} # {index : []}
    list_index_sorted = queue.PriorityQueue() #[index1, index2...]
    count = 0
    for i in range(1, eco_sys.poss_num + 1):
        if individual[i - 1] == 0:
            continue
        for j in range(eco_sys.poss_num + 1, eco_sys.poss_num + eco_sys.sensors_num+1):
            path = list()
            path.append(start)
            path.append(i)
            path.append(j)
            path.append(end)
            weight = calculate_path(eco_sys.graph, path)
            list_index_weight[count] = weight
            list_index_path[count] = list(path)
            list_index_sorted.put((weight, count))
            count += 1
    return list_index_path, priority_to_list(list_index_sorted), list_index_weight


def priority_to_list(priority_queue: queue.PriorityQueue):
    list_out = []
    while not priority_queue.empty():
        list_out.append(priority_queue.get())
    return list_out


def get_individual_graph(eco_sys: EcoSys, individual: list):
    if not check_individual(eco_sys, individual):
        return None
    graph = GraphF()
    graph.add_vertex(0)
    for i in range(1, eco_sys.poss_num + 1):
        if individual[i-1] == 0:
            continue
        graph.add_vertex(i)
    for j in range(eco_sys.poss_num+1, eco_sys.sensors_num+eco_sys.poss_num+1):
        graph.add_vertex(j)
    graph.add_vertex(eco_sys.poss_num + eco_sys.sensors_num + 1)
    graph = set_edge_individual_graph(eco_sys, graph, eco_sys.relays_num, eco_sys.sensors_num)
    return graph


def set_edge_individual_graph(eco_sys: EcoSys, i_graph: GraphF, relays_num, sensors_num):
    set_sink = True
    for i in range(1, relays_num + 1):
        i_graph.vertices[0].add_edge(i_graph.vertices[i])
        for j in range(relays_num+1, relays_num + sensors_num + 1):
            edge = eco_sys.graph.get_edge(i_graph.vertices[i].data, i_graph.vertices[j].data)
            i_graph.add_edge(i_graph.vertices[i].data, i_graph.vertices[j].data,
                             weight=edge.weight, flow=edge.flow, capacity=edge.capacity)
            if not set_sink:
                continue
            i_graph.add_edge(i_graph.vertices[j].data, i_graph.vertices[len(i_graph.vertices) - 1].data,
                             capacity=1, weight=1, flow=0)
        set_sink = False
    return i_graph


def check_maximum_flow(graph: Graph, list_path: list, optimal_value):  # original graph
    max_flow = SimpleMaxFlow()
    dict_use = {}
    for i in range(len(list_path)):
        for j in range(len(list_path[i])):
            if j == (len(list_path[i]) - 1):
                continue
            index1 = list_path[i][j]
            index2 = list_path[i][j+1]
            edge = graph.get_edge(index1, index2)
            if (index1, index2) not in dict_use:
                dict_use[(index1, index2)] = 1
                max_flow.AddArcWithCapacity(index1, index2, int(edge.capacity))
    if max_flow.Solve(list_path[0][0], list_path[0][3]) == max_flow.OPTIMAL:
        if max_flow.OptimalFlow() != optimal_value:
            # print("optimal value : " + str(max_flow.OptimalFlow()))
            return None
        # print("Optimal value : " + str(max_flow.OptimalFlow()))
        return max_flow
    else:
        return None


def get_list_of_path_with_index(index_path, index_sorted, index: int):
    list_path = []
    i = 0
    while True:
        if i >= len(index_sorted):
            break
        # if index_sorted[i][1] == index:
        if i == index:
            list_path.append(index_path[index_sorted[i][1]])
            break
        list_path.append(index_path[index_sorted[i][1]])
        i += 1
    return list_path


def check_max_flow_index(eco_sys: EcoSys, index_path, index_sorted, middle: int):
    # solve the maximum flow with the middle in dex of the sorted path list (binary search)
    if middle >= len(index_sorted):
        print("error out of index for index_sorted get_max_flow_index function")
        return None
    list_path = get_list_of_path_with_index(index_path, index_sorted, middle)
    return check_maximum_flow(eco_sys.graph, list_path, eco_sys.sensors_num)


def binary_solve(eco_sys: EcoSys, index_path, index_sorted, left: int, right: int):
    # binary solution
    # if right < left:
    #     print("error binary_solve with left > right")
    #     return None
    middle = int((left + right) / 2)
    max_flow = check_max_flow_index(eco_sys, index_path, index_sorted, middle)
    if right - left < 2:
        if max_flow is None:
            return check_max_flow_index(eco_sys, index_path, index_sorted, middle+1)
        return max_flow
    if max_flow is not None:
        return binary_solve(eco_sys, index_path, index_sorted, left, middle)
    else:
        return binary_solve(eco_sys, index_path, index_sorted, middle, right)


def get_output(max_flow: SimpleMaxFlow, eco_sys: EcoSys):
    output = WusnOutput(inp=eco_sys.wusn_input, sensors=eco_sys.sensors, relays=eco_sys.poss_locations)
    for i in range(max_flow.NumArcs()):
        first_vex = max_flow.Tail(i)
        if first_vex < 1 or first_vex > eco_sys.poss_num:
            continue
        second_vex = max_flow.Head(i) - eco_sys.poss_num - 1
        relay = output.relays[first_vex - 1]
        if relay not in output.relay_to_sensors:
            output.relay_to_sensors[relay] = []
        if max_flow.Flow(i) > 0:
            output.relay_to_sensors[relay].append(output.sensors[second_vex])
    return output


def solve_maximum_flow(eco_sys: EcoSys, individual: list):
    # i_graph = get_individual_graph(eco_sys, individual)
    index_path, index_sorted, index_weight = list_all_path(eco_sys, individual)
    max_flow = binary_solve(eco_sys, index_path, index_sorted, 0, len(index_sorted) - 1)
    if max_flow is None:
        print("Can nof find max flow")
        return None
    return max_flow

#
# #
# # def solve_maximum_flow(in_graph: GraphF, eco_sys: EcoSys)
# def init_individual(poss_num, relays_num):
#     individual = []
#     for i in range(poss_num):
#         if i < relays_num:
#             individual.append(1)
#         else:
#             individual.append(0)
#     random.shuffle(individual)
#     return individual
#
#
# eco_sys = EcoSys.get_instance()
# eco_sys.set_input("../../data/br-004.test")
# new_individual = init_individual(eco_sys.poss_num, eco_sys.relays_num)
# new_graph = get_individual_graph(eco_sys, new_individual)
# print(new_graph.vertices)
# (a, b, c) = list_all_path(eco_sys, new_individual)
# print("index path : ")
# print(a)
# print("length : " + str(len(a)))
# print("index sort : ")
# print(str(b))
# print("length : " + str(len(b)))
# # while not b.empty():
# #     print(b.get())
# print("index weight : ")
# print(c)
#
#

