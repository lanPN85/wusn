import pyximport
pyximport.install()
import copy

from wusn.commons import WusnOutput, RelayPosition
from . import cutils


def lbsna2(prev: WusnOutput, verbose=True) -> WusnOutput:
    def verbose_print(*args, **kwargs):
        if verbose:
            print(*args, **kwargs)

    inp = prev.input
    _ = inp.loss
    out = WusnOutput(prev.input, sensors=prev.sensors[:],
                     relays=prev.relays[:], relay_to_sensors=copy.deepcopy(prev.relay_to_sensors))
    verbose_print('Starting LBSNA-2...')
    target_load = len(inp.sensors) // inp.relay_num
    verbose_print('Target load: %d' % target_load)

    current_relays = prev.relays[:]

    for i in range(inp.relay_num):
        verbose_print('Iter %d/%d' % (i+1, inp.relay_num))
        chosen = _find_optimal(current_relays, out)
        verbose_print('Chosen relay: %s' % chosen)
        current_relays.remove(chosen)
        load_relay(chosen, current_relays, out, target_load, verbose=verbose)

    return out


def load_relay(chosen: RelayPosition, relays, out: WusnOutput, target_load, verbose=True):
    """
    Loads up a relay until it reaches the specified target load. Modifies out in place.

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

    a_sensors = []
    for rn in relays:
        if rn == chosen:
            continue
        a_sensors.extend(out.relay_to_sensors[rn])
    sensors = a_sensors
    # e_sensors = out.relay_to_sensors[chosen]
    # sensors = list(filter(lambda s: s not in e_sensors, a_sensors))

    while len(out.relay_to_sensors[chosen]) < target_load:
        verbose_print(' Relay load: %d' % len(out.relay_to_sensors[chosen]))

        sq = _find_best_sensor(chosen, sensors, out.input.loss)
        # Find corresponding relay
        rq = list(filter(lambda r: sq in out.relay_to_sensors[r], relays))[0]
        verbose_print(' Chosen relay: %s' % rq)
        verbose_print(' Chosen sensor: %s' % sq)

        # Reassign
        out.relay_to_sensors[chosen].append(sq)
        out.relay_to_sensors[rq].remove(sq)
        sensors.remove(sq)


def _find_best_sensor(relay: RelayPosition, sensors, losses):
    return cutils.find_best_sensor(relay, sensors, losses)


def _find_optimal(relays, out: WusnOutput):
    opt = relays[0]
    opt_len = len(out.relay_to_sensors[opt])
    for rn in relays[1:]:
        sns = out.relay_to_sensors[rn]
        if len(sns) < opt_len:
            opt = rn
            opt_len = len(sns)

    return opt

