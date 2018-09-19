import sys
sys.path.append('.')

from wusn.commons import WusnInput, WusnOutput
from wusn.propose2.init import kmeans_greedy
from wusn.propose2.utils import Evaluator, ind_to_output
from wusn.propose.ecosys import EcoSys
from wusn.propose.fitness import get_min_cost_flow, get_output, get_fitness_value
from wusn.propose.r_graph import *


if __name__ == '__main__':

    INP = '../medium_data/br-001.test'

    RUNS = 200
    
    ec = EcoSys.get_instance()
    ec.set_input(INP)
    inp = ec.wusn_input
    ev = Evaluator(inp)
    
    for i in range(RUNS):
        ind = kmeans_greedy(inp, heuristic=True)
        # Calculate loss
        ls1 = ev.evaluate(ind)[0]
        ls4 = ind_to_output(ind, inp).max_loss
        # Apply MCF
        relays = ind[ind.sensor_count:]
        ind1 = [0] * len(inp.relays)
        for i, r in enumerate(inp.relays):
            if r in relays:
                ind1[i] = 1
        # mcf = get_min_cost_flow(ind1, ec.graph, len(inp.relays), len(inp.sensors))
        # omcf = get_output(mcf, ec)
        mcf = solve_maximum_flow(eco_sys=ec, individual=ind1)
        output_temp = get_output(mcf, ec)
        # omcf.clean_relays()
        ls2 = get_fitness_value(ind1, ec, mcf)
        ls3 = output_temp.max_loss
        print('LB3 Loss: %f' % ls1)
        print('Output LB3 Loss: %f' % ls4)
        print('MCF Loss: %f' % ls2)
        print('Output MCF Loss: %f' % ls3)
        #print(omcf.relays)
        #print()
        #print(ind_to_output(ind, inp).relays)
        input('Enter to continue...')
