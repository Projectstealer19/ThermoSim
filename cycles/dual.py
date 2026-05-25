import numpy as np

def dual_cycle(T1, r, alpha, rc, V1):

    # ------------------------------------------------
    # AIR PROPERTIES (fixed)
    # ------------------------------------------------

    R     = 287           # J/kg-K
    gamma = 1.4           # specific heat ratio for air
    cv    = R / (gamma - 1)
    cp    = gamma * cv

    # ------------------------------------------------
    # ASSUMPTION
    # ------------------------------------------------

    S1 = 100              # J/kg-K  (reference entropy)

    # ------------------------------------------------
    # DERIVE P1 FROM IDEAL GAS LAW  (m = 1 kg)
    # ------------------------------------------------

    P1 = R * T1 / V1

    # ------------------------------------------------
    # STATE 1 → 2  Isentropic Compression
    # ------------------------------------------------

    T2 = T1 * (r ** (gamma - 1))
    V2 = V1 / r
    P2 = P1 * (r ** gamma)
    S2 = S1

    # ------------------------------------------------
    # STATE 2 → 3  Constant Volume Heat Addition
    # ------------------------------------------------

    P3 = P2 * alpha
    V3 = V2
    T3 = T2 * alpha
    S3 = S2 + cv * np.log(T3 / T2)

    # ------------------------------------------------
    # STATE 3 → 4  Constant Pressure Heat Addition
    # ------------------------------------------------

    P4 = P3
    V4 = V3 * rc
    T4 = T3 * rc
    S4 = S3 + cp * np.log(T4 / T3)

    # ------------------------------------------------
    # STATE 4 → 5  Isentropic Expansion
    # ------------------------------------------------

    V5 = V1
    T5 = T4 * (V4 / V5) ** (gamma - 1)
    P5 = P4 * (V4 / V5) ** gamma
    S5 = S4

    # ------------------------------------------------
    # HEAT TRANSFER, WORK & EFFICIENCY
    # ------------------------------------------------

    Q23       = cv * (T3 - T2)
    Q34       = cp * (T4 - T3)
    Q_in      = Q23 + Q34
    Q_out     = cv * (T5 - T1)
    W_net     = Q_in - Q_out
    efficiency = (W_net / Q_in) * 100

    return {
        "T": [T1, T2, T3, T4, T5],
        "P": [P1, P2, P3, P4, P5],
        "V": [V1, V2, V3, V4, V5],
        "S": [S1, S2, S3, S4, S5],
        "Q_in":      Q_in,
        "Q_out":     Q_out,
        "W_net":     W_net,
        "efficiency": efficiency,
        "gamma":     gamma,
        "R":         R,
        "cp":        cp,
        "cv":        cv,
    }