import pyximport
pyximport.install()

from wusn.commons import WusnOutput, RelayPosition
from . import cutils


def lbsna1(prev: WusnOutput, verbose=True) -> WusnOutput:
    def verbose_print(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    inp = prev.input
    _ = inp.loss
    out = WusnOutput(prev.input, sensors=prev.sensors[:],
                     relays=prev.relays[:], relay_to_sensors=prev.relay_to_sensors.copy())
    verbose_print('Starting LBSNA-1...')
    target_load = len(inp.sensors) // inp.relay_num
    verbose_print('Target load: %d' % target_load)

    current_relays = prev.relays[:]

    for i in range(inp.relay_num):
        verbose_print('Iter %d/%d' % (i+1, inp.relay_num))
        chosen = _find_optimal(current_relays, out)
        verbose_print('Chosen relay: %s' % chosen)
        current_relays.remove(chosen)
        unload_relay(chosen, current_relays, out, target_load, verbose=verbose)

    return out


def unload_relay(chosen: RelayPosition, relays, out: WusnOutput, target_load, verbose=True):
    """
    Unloads a relay until it reaches the specified target load. Modifies out in place.
    :param verbose:
    :param chosen: The chosen relay
    :param relays: The list of relays to consider. Should not contain chosen.
    :param out: The output object whose relay_to_sensors will be changed
    :param target_load: The target_load amount for each relay.
    :return: None
    """
    def verbose_print(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    while len(out.relay_to_sensors[chosen]) > target_load:
        verbose_print(' Relay load: %d' % len(out.relay_to_sensors[chosen]))
        sensors = out.relay_to_sensors[chosen]
        sq, rq = _find_best_pair(relays, sensors, out.input.loss)
        verbose_print(' Chosen relay: %s' % rq)
        verbose_print(' Chosen sensor: %s' % sq)

        # Reassign
        out.relay_to_sensors[chosen].remove(sq)
        out.relay_to_sensors[rq].append(sq)


def _find_best_pair(relays, sensors, losses):
    return cutils.find_best_pair(relays, sensors, losses)
    # best_pair = (None, None)
    # best_loss = float('inf')
    #
    # for rn in relays:
    #     for sn in sensors:
    #         loss = losses[(sn, rn)]
    #         if loss < best_loss:
    #             best_loss = loss
    #             best_pair = (sn, rn)
    #
    # return best_pair


def _find_optimal(relays, out: WusnOutput):
    opt = relays[0]
    opt_len = len(out.relay_to_sensors[opt])
    for rn in relays[1:]:
        sns = out.relay_to_sensors[rn]
        if len(sns) > opt_len:
            opt = rn
            opt_len = len(sns)

    return opt
