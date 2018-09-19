from wusn.propose.python_datastructure.graph import Graph
from wusn.commons.point import *
from wusn.commons.config import *


def set_up_edge(graph: Graph, sensors_num, poss_num, relays_num, loss_dict, set_weight=True):
    set_sink = True
    count = 0
    balance = sensors_num / relays_num
    for i in range(1, poss_num+1):
        graph.vertices[0].add_edge(graph.vertices[i], weight=1, capacity=balance)
        for j in range(poss_num+1, poss_num+sensors_num+1):
            if set_sink is True:
                graph.vertices[j].add_edge(graph.vertices[poss_num+sensors_num+1], weight=1,
                                           capacity=1)
            # (d_ug, d_ag) = t_distances(graph.vertices[j].data, graph.vertices[i].data, get_air_refractive_index(),
            #                            get_soil_refractive_index())
            # weight = get_trans_loss(d_ug, d_ag)
            if set_weight is True:
                weight = loss_dict[(graph.vertices[j].data, graph.vertices[i].data)]
            else:
                weight = 1
            count += 1
            # print(""+ str(count) + ".   "+str(weight))
            graph.vertices[i].add_edge(graph.vertices[j], weight=weight, capacity=1)
        set_sink = False
    return graph


# def set_up_edge_balance(graph: Graph, sensors_num, poss_num, set_weight=False):
#     set_sink = True
#     count = 0
#     balance = sensors_num / poss_num
#     eco_sys = EcoSys.get_instance()
#     for i in range(1, poss_num + 1):
#         graph.vertices[0].add_edge(graph.vertices[i], weight=1, capacity=balance)
#         for j in range(poss_num + 1, poss_num + sensors_num + 1):
#             if set_sink is True:
#                 graph.vertices[j].add_edge(graph.vertices[poss_num + sensors_num + 1], weight=1,
#                                            capacity=1)
#             # (d_ug, d_ag) = t_distances(graph.vertices[j].data, graph.vertices[i].data, get_air_refractive_index(),
#             #                            get_soil_refractive_index())
#             # weight = get_trans_loss(d_ug, d_ag)
#
#             # weight = eco_sys.wusn_input().loss()[(graph.vertices[j].data, graph.vertices[i].data)]
#             # weight = get_trans_loss(1, 10)
#             if set_weight is True:
#                 weight = eco_sys.wusn_input.loss()[(graph.vertices[j].data, graph.vertices[i].data)]
#             else:
#                 weight = 1
#             count += 1
#             print("" + str(count) + ".   " + str(weight))
#             graph.vertices[i].add_edge(graph.vertices[j], weight=weight, capacity=1)
#         set_sink = False
#     return graph


def set_graph(sensors: list, poss_locations: list, relays_num: int, loss_dict: dict):
    sensors_num = len(sensors)
    poss_num = len(poss_locations)
    assert sensors_num % relays_num == 0
    graph = Graph()
    point = Point(-1,-1)
    graph.add_vertex(point)
    for i in range(len(poss_locations)):
        graph.add_vertex(poss_locations[i])
    for i in range(len(sensors)):
        graph.add_vertex(sensors[i])
    end = Point(-2,-2)
    graph.add_vertex(end)
    graph = set_up_edge(graph, sensors_num, poss_num, relays_num, loss_dict=loss_dict)
    return graph


