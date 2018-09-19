from wusn.commons import WusnOutput, WusnInput


def lurns2(inp: WusnInput) -> WusnOutput:
    sensors = inp.sensors
    Y = inp.relay_num
    in_relays = inp.relays[:]
    out_relays = set()
    out_relays_to_sensors = {}
    loss = inp.loss  # L(sn, rn) = loss[(sn, rn)]

    print("Starting LURN-2...")
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
        out_relays.add(best_rn)
    out_relays = list(out_relays)

    while len(out_relays) > Y:
        T_min = float("inf")
        best_rn = None
        for fq in out_relays:
            Tc = -float("inf")

            out2 = out_relays[:]
            out2.remove(fq)
            for rn in out2:
                for sn in sensors:
                    ls = loss[(sn, rn)]
                    if ls > Tc:
                        Tc = ls

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
