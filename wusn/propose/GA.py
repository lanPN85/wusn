from deap import base
from deap import creator
from deap import tools
from wusn.propose.ecosys import EcoSys
import random
import math
from wusn.propose.fitness import *
from deap import algorithms
import os
import time
import sys

N_GEN = 200

CXPB = 0.8

MUTPD = 0.05

TERMINATE = 30


def init_individual(poss_num, relays_num):
    individual = []
    for i in range(poss_num):
        if i < relays_num:
            individual.append(1)
        else:
            individual.append(0)
    random.shuffle(individual)
    return creator.Individual(individual)


def choose_from_list(a_list, n):
    choice_list = []
    b_list = list(a_list)
    for i in range(n):
        x = random.choice(b_list)
        choice_list.append(x)
        b_list.remove(x)
    return choice_list


def re_fine(relays_num):
    def decorator(func):
        def wrapper(*args, **kargs):
            offspring = func(*args, **kargs)
            for individual in offspring:
                n = len(individual)
                list_1 = []
                list_0 = []
                count = 0
                for i in range(n):
                    if individual[i] != 0 or individual != 1:
                        individual[i] = random.randint(0, 1)
                    if individual[i] == 1:
                        count += 1
                        list_1.append(i)
                    elif individual[i] == 0:
                        list_0.append(i)
                choice_list = []
                if count < relays_num:
                    change = relays_num - count
                    choice_list = choose_from_list(list_0, change)
                elif count > relays_num:
                    change = count - relays_num
                    choice_list = choose_from_list(list_1, change)
                else:
                    return offspring
                for i in range(len(choice_list)):
                    individual[choice_list[i]] = abs(individual[choice_list[i]] - 1)
            return offspring
        return wrapper
    return decorator


def get_best(pop):
    max_pop = pop[0]
    for i in range(len(pop)):
        if pop[i].fitness.values[0] < max_pop.fitness.values[0]:
            max_pop = pop[i]
    return max_pop


def do_nothing(pop):
    hello = 0

# #test init
# a = init_individual(20, 8)
# print(a)
# a = [1,1,0,0,0,1,0,1,0,0,0,0,0,0,0]
# re_fine(a, 6)
# print(a)
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)


def ga(file_name):
    eco_sys = EcoSys.get_instance()
    eco_sys.set_input(file_name)
    toolbox = base.Toolbox()

    toolbox.register("individual", init_individual, len(eco_sys.poss_locations),
                     eco_sys.relays_num)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxTwoPoint)
    #toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.decorate("mate", re_fine(eco_sys.relays_num))
    toolbox.decorate("mutate", re_fine(eco_sys.relays_num))
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", get_fitness_value, eco_sys=eco_sys)
    pop = toolbox.population(N_GEN)
    best_ind = toolbox.clone(pop[0])
    prev = -1 #use for termination
    count_term = 0 # use for termination
    for g in range(N_GEN):
        # offspring = map(toolbox.clone, toolbox.select(pop, len(pop)))
        offspring = map(toolbox.clone, toolbox.select(pop, len(pop)-1))
        offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPD)
        invalid_ind = []
        for ind in offspring:
            invalid_ind.append(ind)
        invalid_ind.append(best_ind)
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        # for i in range(len(invalid_ind)):
        #     invalid_ind[i].fitness.values = toolbox.evaluate(invalid_ind[i])
        z = zip(invalid_ind, fitnesses)
        min_value = 99999999.0
        for ind, fit in z:
            ind.fitness.values = [fit]
            if min_value > fit:
                min_value = fit
                best_ind = toolbox.clone(ind)
        b = round(min_value, 6)
        if prev == b:
            count_term += 1
        else:
            count_term = 0
        print("max value this pop %d : %f " % (g, min_value))
        pop[:] = offspring
        prev = b
        if count_term == TERMINATE:
            break
    max_pop = best_ind
    max_pop_min_cost_flow = get_min_cost_flow(max_pop, eco_sys.graph, eco_sys.poss_num,
                                              eco_sys.sensors_num)
    output = get_output(max_pop_min_cost_flow, eco_sys)
    return output




#
# eco_sys = EcoSys.get_instance()
# eco_sys.set_input("/home/dungdinh/SDev/wusn/small_data/001.test")
# toolbox = base.Toolbox()
#
# toolbox.register("individual", init_individual, len(eco_sys.poss_locations),
#                  eco_sys.relays_num)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# toolbox.register("mate", tools.cxTwoPoint)
# toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.2, indpb=0.2)
# toolbox.decorate("mate", re_fine(eco_sys.relays_num))
# toolbox.decorate("mutate", re_fine(eco_sys.relays_num))
# toolbox.register("select", tools.selTournament, tournsize=3)
# toolbox.register("evaluate", get_fitness_value, eco_sys=eco_sys)
#
# pop = toolbox.population(N_GEN)
# for g in range(N_GEN):
#     offspring = map(toolbox.clone, toolbox.select(pop, len(pop)))
#     offspring = algorithms.varAnd(offspring, toolbox, CXPB, MUTPD)
#     invalid_ind = []
#     for ind in offspring:
#         invalid_ind.append(ind)
#     fitnesses = toolbox.map(toolbox.evaluate,  invalid_ind)
#     # for i in range(len(invalid_ind)):
#     #     invalid_ind[i].fitness.values = toolbox.evaluate(invalid_ind[i])
#     z = zip(invalid_ind, fitnesses)
#     count = 0
#     for ind, fit in z:
#         count += 1
#         print('count : %d'%(count), end='\r')
#         ind.fitness.values = [fit]
#     pop[:] = offspring
#
# max_pop = get_best(pop)
# max_pop_min_cost_flow = get_min_cost_flow(max_pop, eco_sys.graph, eco_sys.poss_num,
#                                           eco_sys.sensors_num)
# output = get_output(max_pop_min_cost_flow, eco_sys)


# test fitness
# individual = toolbox.individual()
# print("Fitness : " + str(fitness_value(eco_sys.graph, individual, eco_sys.poss_num, eco_sys.sensors_num)))



# for x in output.relay_to_sensors:
#     print(str(x) + ": ", end='', flush=True)
#     for y in output.relay_to_sensors[x]:
#         print(str(y) + ",", end='', flush=True)
#     print("")


# algorithms.eaSimple(pop, toolbox, cxpb= CXPB, mutpb= MUTPD, ngen= N_GEN)