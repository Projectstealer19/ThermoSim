import numpy as np

def diesel_cycle(T1, r, rc, gamma):

    R  = 287
    cv = R / (gamma - 1)
    cp = gamma * cv

    # Internal defaults
    V1 = 0.001
    P1 = 101325

    # State 2: isentropic compression
    T2 = T1 * (r ** (gamma - 1))
    V2 = V1 / r
    P2 = P1 * (r ** gamma)

    # State 3: constant pressure heat addition
    T3 = T2 * rc
    V3 = V2 * rc
    P3 = P2

    # State 4: isentropic expansion
    T4 = T3 * (rc / r) ** (gamma - 1)
    V4 = V1
    P4 = P3 * (V3 / V4) ** gamma

    # Entropy
    S1 = 100
    S2 = S1
    S3 = S2 + cp * np.log(T3 / T2)
    S4 = S3

    Q_in  = cp * (T3 - T2)
    Q_out = cv * (T4 - T1)
    W_net = Q_in - Q_out
    efficiency = (W_net / Q_in) * 100

    return {

    "T": [T1, T2, T3, T4],

    "S": [S1, S2, S3, S4],

    "V": [V1, V2, V3, V4],

    "P": [P1, P2, P3, P4],

    "Q_in": Q_in,

    "Q_out": Q_out,

    "W_net": W_net,

    "efficiency": efficiency,

    "gamma": gamma,

    "R": R,

    "cp": cp,

    "cv": cv
}