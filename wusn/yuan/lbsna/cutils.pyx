from wusn.commons import RelayPosition


def find_best_sensor(relay: RelayPosition, sensors, losses):
    best = None
    cdef float best_loss = 99999.0
    cdef float loss = 0.0
    cdef int slen = len(sensors)

    for i in range(0, slen):
        sn = sensors[i]
        loss  = losses[(sn, relay)]
        if loss < best_loss:
            best = sn
            best_loss = loss

    return best


def find_best_pair(relays, sensors, losses):
    best_pair = (None, None)
    cdef float best_loss = 99999.0
    cdef float loss = 0.0
    cdef:
        int rlen = len(relays)
        int slen = len(sensors)

    for i in range(0, rlen):
        for j in range(0, slen):
            pair = (sensors[j], relays[i])
            loss = losses[pair]
            if loss < best_loss:
                best_loss = loss
                best_pair = pair

    return best_pair
