import pulp
import numpy as np

from wusn.commons import WusnInput, WusnOutput


def model_lp(inp: WusnInput, lax=False):
    _ = inp.loss
    vtype = pulp.LpContinuous if lax else pulp.LpBinary
    prob = pulp.LpProblem('RelaySelection')
    N, M, Y = len(inp.sensors), len(inp.relays), inp.relay_num

    # Model assignment matrix
    a = [[] for _ in range(N)]
    for i in range(N):
        for j in range(M):
            a[i].append(pulp.LpVariable(name='A_%d_%d' % (i, j), lowBound=0,
                                        upBound=1, cat=vtype))
    a = np.asarray(a, dtype=np.object)

    # Model deployment array
    z = []
    for i in range(M):
        z.append(pulp.LpVariable(name='Z_%d' % i, lowBound=0,
                                 upBound=1, cat=vtype))
        s = pulp.lpSum(a[:, i])
        prob += s - z[i] * N <= 0
        prob += s - z[i] >= 0

    z = np.asarray(z, dtype=np.object)

    # Constraints
    prob += (pulp.lpSum(z) == Y)

    for i in range(M):
        c = [a[j, i] for j in range(N)]
        prob += (pulp.lpSum(c) == N // Y * z[i])

    for i in range(N):
        c = [a[i, j] for j in range(M)]
        prob += (pulp.lpSum(c) == 1)

    # Loss function
    C = pulp.LpVariable('C', lowBound=0)

    # Loss function as N constraints
    for i in range(N):
        c = [inp.loss_index[i][j] * a[i, j] for j in range(M)]
        prob += (pulp.lpSum(c) <= C)

    prob.setObjective(C)

    return prob


def solve_lp(prob: pulp.LpProblem, inp: WusnInput):
    status = prob.solve()
    if status == pulp.LpStatusOptimal:
        if prob.isMIP():
            return prob_to_out(prob, inp)
        else:
            return prob.variablesDict()['C']
    else:
        raise RuntimeError('LP solver returned %s' % pulp.LpStatus[status])


def prob_to_out(prob: pulp.LpProblem, inp: WusnInput):
    N, M, Y = len(inp.sensors), len(inp.relays), inp.relay_num
    v = prob.variablesDict()
    sensors, all_relays = inp.sensors, inp.relays

    relay_to_sensors = {}
    relays = []

    # Get assignment matrix
    for i in range(N):
        sn = sensors[i]
        for j in range(M):
            a = v['A_%d_%d' % (i, j)]
            if a.value() > 0:
                rn = all_relays[j]
                relays.append(rn)
                if rn not in relay_to_sensors.keys():
                    relay_to_sensors[rn] = [sn]
                else:
                    relay_to_sensors[rn].append(sn)
                break

    out = WusnOutput(inp, sensors=inp.sensors, relays=relays,
                     relay_to_sensors=relay_to_sensors)

    return out
