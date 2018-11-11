from wusn.commons import WusnOutput, WusnInput


def lurns2(inp: WusnInput) -> WusnOutput:
    sensors = inp.sensors
    Y = inp.relay_num
    in_relays = inp.relays[:]
    out_relays = list()
    or_set = set()
    out_relays_to_sensors = {}
    loss = inp.loss  # L(sn, rn) = loss[(sn, rn)]

    print("Starting LURNS-2...")
    for sn in sensors:
        best_rn = None
        t_min = float("inf")
        for rn in in_relays:
            ls = loss[(sn, rn)]
            if ls < t_min:
                t_min = ls
                best_rn = rn
        print('[%d] Picking %s' % (len(out_relays), best_rn))
        # out_relays.append(best_rn)
        # in_relays.remove(best_rn)
        if best_rn not in or_set:
            or_set.add(best_rn)
            out_relays.append(best_rn)
    del or_set
    out_relays = list(out_relays)

    while len(out_relays) > Y:
        T_min = float("inf")
        best_rn = None
        for fq in out_relays:
            out2 = out_relays[:]
            out2.remove(fq)
            losses = []
            for sn in sensors:
                Ts = float('inf')
                for rn in out2:
                    ls = loss[(sn, rn)]
                    if ls < Ts:
                        Ts = ls
                losses.append(Ts)
            Tc = max(losses)
            if Tc < T_min:
                T_min = Tc
                best_rn = fq
        print('[%d] Removing %s' % (len(out_relays), best_rn))
        out_relays.remove(best_rn)

    # Gan cac sn cho rn
    for rn in out_relays:
        out_relays_to_sensors[rn] = []

    for sn in sensors:
        best_rn = None
        t_min = float("inf")
        for rn in out_relays:
            ls = loss[(sn, rn)]
            if ls < t_min:
                t_min = ls
                best_rn = rn
        out_relays_to_sensors[best_rn].append(sn)

    # Ket qua
    out = WusnOutput(inp, sensors, out_relays, out_relays_to_sensors)
    return out
