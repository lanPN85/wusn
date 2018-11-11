from wusn.commons import WusnOutput, WusnInput


def lurns1(inp: WusnInput) -> WusnOutput:
    sensors = inp.sensors
    in_relays = inp.relays[:]
    Y = inp.relay_num
    out_relays = []
    out_relays_to_sensors = {}
    loss = inp.loss  # L(sn, rn) = loss[(sn, rn)]

    print("Starting LURNS-1...")
    while len(out_relays) < Y:
        min_T = float("inf")
        best_rn = None
        for fq in in_relays:
            losses = []
            for id1, sn in enumerate(sensors):
                Ts = float('inf')
                for rn in out_relays + [fq]:
                    ls = loss[(sn, rn)]
                    if ls < Ts:
                        Ts = ls
                losses.append(Ts)
            Tc = max(losses)
            if Tc < min_T:
                min_T = Tc
                best_rn = fq
        print('[%d] Picked relay: %s' % (len(out_relays), best_rn))
        out_relays.append(best_rn)
        in_relays.remove(best_rn)

    # Gan cac sn cho rn
    for rn in out_relays:
        out_relays_to_sensors[rn] = []

    for sn in sensors:
        t_min = float("inf")
        best_rn = None
        for rn in out_relays:
            ls = loss[(sn, rn)]
            if ls < t_min:
                t_min = ls
                best_rn = rn
        out_relays_to_sensors[best_rn].append(sn)

    # Ket qua
    out = WusnOutput(inp, sensors, out_relays, out_relays_to_sensors)
    return out
