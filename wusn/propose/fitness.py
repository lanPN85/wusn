from wusn.propose.python_datastructure.graph import *
from ortools.graph.pywrapgraph import *
from wusn.propose.ecosys import *
from wusn.commons.output import *

#
# def get_fitness_value(individual: list, eco_sys:EcoSys, min_cost_flow=None):
#     if min_cost_flow is None:
#         min_cost_flow = get_min_cost_flow(individual, eco_sys.graph, eco_sys.poss_num,
#                                           eco_sys.sensors_num)
#     if min_cost_flow is None:
#         return 0
#     return min_cost_flow.OptimalCost() - eco_sys.sensors_num * 2


def get_fitness_value(individual: list, eco_sys:EcoSys, min_cost_flow=None):
    if min_cost_flow is None:
        min_cost_flow = get_min_cost_flow(individual, eco_sys.graph, eco_sys.poss_num,
                                          eco_sys.sensors_num)
    if min_cost_flow is None:
        return 0
    fitness = -1
    for i in range(min_cost_flow.NumArcs()):
        if min_cost_flow.Tail(i) > eco_sys.poss_num:
            continue
        if min_cost_flow.Tail(i) < 1:
            continue
        if min_cost_flow.Head(i) < eco_sys.poss_num + 1:
            continue
        if min_cost_flow.Head(i) > eco_sys.poss_num + eco_sys.sensors_num:
            continue
        if min_cost_flow.Flow(i) > 0:
            edge = eco_sys.graph.get_edge(min_cost_flow.Tail(i), min_cost_flow.Head(i))
            if fitness < edge.weight:
                fitness = edge.weight
        # if min_cost_flow.Flow(i) > fitness:
        #     fitness = min_cost_flow.Flow(i)
    return fitness


def get_output(min_cost_flow, eco_sys: EcoSys):
    output = WusnOutput(inp=eco_sys.wusn_input, sensors=eco_sys.sensors, relays=eco_sys.poss_locations)
    for i in range(min_cost_flow.NumArcs()):
        # print(str(min_cost_flow.Tail(i)) + " -> " + str(min_cost_flow.Head(i)) + " : " + str(min_cost_flow.Flow(i)) +
        #       " - " + str(min_cost_flow.Capacity(i)))
        first_ver = min_cost_flow.Tail(i)
        if first_ver < 1:
            continue
        if first_ver > eco_sys.poss_num:
            continue
        second_ver = min_cost_flow.Head(i) - eco_sys.poss_num - 1
        relay = output.relays[first_ver - 1]
        if relay not in output.relay_to_sensors:
            output.relay_to_sensors[relay] = []
        if min_cost_flow.Flow(i) > 0:
            output.relay_to_sensors[relay].append(output.sensors[second_ver])
    return output
    #     if first_ver - 1 not in output.relay_to_sensors:
    #         output.relay_to_sensors[first_ver-1] = []
    #     if min_cost_flow.Flow(i) > 0:
    #         output.relay_to_sensors[first_ver-1].append(second_ver)
    # return output


def get_min_cost_flow(individual: list, graph: Graph, poss_num: int, sensors_num:int):
    min_cost_flow = SimpleMinCostFlow()
    if len(individual) != poss_num:
        return -1
    set_edge_sink = True
    for i in range(1, poss_num + 1):
        edge = graph.get_edge(0, i)
        min_cost_flow.AddArcWithCapacityAndUnitCost(0, i, int(edge.capacity * individual[i - 1]),
                                                    1)
        for j in range(poss_num + 1, poss_num + sensors_num + 1):
            edge = graph.get_edge(i, j)
            weight = int(edge.weight)
            min_cost_flow.AddArcWithCapacityAndUnitCost(i, j, edge.capacity, weight)
            if set_edge_sink:
                min_cost_flow.AddArcWithCapacityAndUnitCost(j, poss_num + sensors_num + 1, 1,
                                                            1)
        set_edge_sink = False
    min_cost_flow.SetNodeSupply(0, sensors_num)
    min_cost_flow.SetNodeSupply(poss_num + sensors_num + 1, -sensors_num)
    fitness = min_cost_flow.Solve()
    if fitness == min_cost_flow.OPTIMAL:
        return min_cost_flow
    else:
        return None



# def fitness_value(individual: list,graph: Graph, poss_num: int, sensors_num: int):
#     min_cost_flow = SimpleMinCostFlow()
#     if len(individual) != poss_num:
#         return -1
#     set_edge_sink = True
#     for i in range(1, poss_num+1):
#         edge = graph.get_edge(0, i)
#         min_cost_flow.AddArcWithCapacityAndUnitCost(0, i, int(edge.capacity * individual[i-1]),
#                                                     1)
#         for j in range(poss_num+1, poss_num+sensors_num+1):
#             edge = graph.get_edge(i, j)
#             weight = int(edge.weight)
#             min_cost_flow.AddArcWithCapacityAndUnitCost(i, j, edge.capacity, weight)
#             if set_edge_sink:
#                 min_cost_flow.AddArcWithCapacityAndUnitCost(j, poss_num + sensors_num + 1, 1,
#                                                             1)
#         set_edge_sink=False
#     min_cost_flow.SetNodeSupply(0, sensors_num)
#     min_cost_flow.SetNodeSupply(poss_num+sensors_num+1, -sensors_num)
#     fitness = min_cost_flow.Solve()
#     if fitness == min_cost_flow.OPTIMAL:
#         redundant = 2*sensors_num
#         return min_cost_flow.OptimalCost() - redundant
#     return 0




# def get_output(individual: list, graph: Graph, poss_num: int, sensors_num: int):
#     min_cost_flow = SimpleMinCostFlow()
#     if len(individual) != poss_num:
#         return -1
#     set_edge_sin = True
#     for i in range(1, poss_num + 1):
#         edge = graph.set_edge(0, i)
#         min_cost_flow.AddArcWithCapacityAndUnitCost(0, i, int(edge.capacity * individual[i-1]), 1)
#         for j in range(poss_num + 1, poss_num + sensors_num + 1):
#             edge = graph.set_edge(i, j)
#             w

# test fitness:
# if __name__ == '__main__':
#     eco = EcoSys.get_instance()
#     eco.set_input("data/001.test")

