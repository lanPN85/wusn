import copy

from wusn.commons import WusnOutput, WusnInput
from wusn.commons.point import *
from wusn.yuan.lbsna.lbsna1 import unload_relay
from wusn.yuan.lbsna.lbsna2 import load_relay


def lbsna3(prev: WusnOutput, verbose=True) -> WusnOutput:
    def verbose_print(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    inp = prev.input
    _ = inp.loss
    out = WusnOutput(prev.input, sensors=prev.sensors[:],
                     relays=prev.relays[:], relay_to_sensors=copy.deepcopy(prev.relay_to_sensors))
    Y = inp.relay_num
    verbose_print('Starting LBSNA-3...')
    target_load = len(inp.sensors) // inp.relay_num
    verbose_print('Target load: %d' % target_load)

    W = Point(0., 0.)
    for p in prev.sensors + prev.relays:
        W += Point(p.x, p.y)
    W /= (len(prev.sensors) + len(prev.relays))

    current_relays = prev.relays[:]

    for i in range(Y):
        verbose_print('Iter %d/%d' % (i + 1, Y))

        max_distance = -float("inf")
        chosen = None
        for rn in current_relays:
            if distance(rn, W) > max_distance:
                max_distance = distance(rn, W)
                chosen = rn
            sns = out.relay_to_sensors[rn]
            for sn in sns:
                if distance(sn, W) > max_distance:
                    max_distance = distance(sn, W)
                    chosen = rn

        verbose_print('Chosen relay: %s' % chosen)
        current_relays.remove(chosen)
        if len(out.relay_to_sensors[chosen]) > target_load:
            unload_relay(chosen, current_relays, out, target_load, verbose=verbose)
        else:
            load_relay(chosen, current_relays, out, target_load, verbose=verbose)

    return out
