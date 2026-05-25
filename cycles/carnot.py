import numpy as np

def carnot_cycle(Th, Tc, Qh, V1=0.01, gamma=1.4):

    # ------------------------------------------------
    # VALIDATION
    # ------------------------------------------------

    if Tc >= Th:
        return None

    # ------------------------------------------------
    # REFERENCE CONDITIONS
    # ------------------------------------------------

    R = 8.314      # J/mol-K
    n = 1          # mol
    S1 = 100       # J/K (reference entropy — fixed assumption)
    nR = n * R

    # ------------------------------------------------
    # STATE 1
    # ------------------------------------------------

    P1 = nR * Th / V1

    # ------------------------------------------------
    # STATE 1 → 2
    # Isothermal Expansion at Th
    # ------------------------------------------------

    delta_s = Qh / Th
    S2 = S1 + delta_s
    V2 = V1 * np.exp(delta_s / nR)
    P2 = nR * Th / V2

    # ------------------------------------------------
    # STATE 2 → 3
    # Adiabatic Expansion
    # ------------------------------------------------

    V3 = V2 * (Th / Tc) ** (1 / (gamma - 1))
    P3 = nR * Tc / V3
    S3 = S2

    # ------------------------------------------------
    # STATE 3 → 4
    # Isothermal Compression at Tc
    # ------------------------------------------------

    S4 = S1
    V4 = V1 * (Th / Tc) ** (1 / (gamma - 1))
    P4 = nR * Tc / V4

    # ------------------------------------------------
    # PERFORMANCE
    # ------------------------------------------------

    efficiency    = 1 - (Tc / Th)
    work_done     = efficiency * Qh
    heat_rejected = Qh - work_done

    # ------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------

    return {
        "T":            [Th, Th, Tc, Tc],
        "P":            [P1, P2, P3, P4],
        "V":            [V1, V2, V3, V4],
        "S":            [S1, S2, S3, S4],
        "efficiency":   efficiency * 100,
        "work_done":    work_done,
        "heat_rejected": heat_rejected,
        "delta_s":      delta_s,
        "gamma":        gamma,
        "Th":           Th,
        "Tc":           Tc,
        "nR":           nR,
        "V1":           V1,
    }