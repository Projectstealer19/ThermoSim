def carnot_cycle(Th , Tc , Qh):
    if Tc >= Th:
        return None
    eff = 1 - (Tc/Th)
    W = eff*Qh
    Qc = Qh - W
    delta_s = Qh/Th
    return { "efficiency" : eff*100 , "work_done" : W , "heat_rejected" : Qc , "delta_s" : delta_s }