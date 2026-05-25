import numpy as np

def otto_cycle(T1, r, T3, V1):

    # ------------------------------------------------
    # AIR PROPERTIES (fixed)
    # ------------------------------------------------

    R     = 287           # J/kg-K
    gamma = 1.4           # specific heat ratio for air
    cv    = R / (gamma - 1)

    # ------------------------------------------------
    # ASSUMPTIONS
    # ------------------------------------------------

    S1 = 100              # J/kg-K  (reference entropy)

    # ------------------------------------------------
    # FIXED AIR MASS ASSUMPTION
    # ------------------------------------------------
    # Assumption:
    # 1 kg of ideal air trapped inside the cylinder
    # Initial pressure derived from ideal gas law
    # ------------------------------------------------

    m = 1.0               # kg

    # ------------------------------------------------
    # STATE 1
    # ------------------------------------------------

    P1_pa = (m * R * T1) / V1
    P1    = P1_pa / 1000.0      # convert Pa → kPa

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

    V3 = V2

    P3 = P2 * (T3 / T2)

    S3 = S2 + cv * np.log(T3 / T2)

    # ------------------------------------------------
    # STATE 3 → 4  Isentropic Expansion
    # ------------------------------------------------

    T4 = T3 / (r ** (gamma - 1))

    V4 = V1

    P4 = P3 * (V3 / V4) ** gamma

    S4 = S3

    # ------------------------------------------------
    # HEAT TRANSFER, WORK & EFFICIENCY
    # ------------------------------------------------

    Q_in = cv * (T3 - T2)

    Q_out = cv * (T4 - T1)

    W_net = Q_in - Q_out

    efficiency = (W_net / Q_in) * 100

    # ------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------

    return {

        "T": [T1, T2, T3, T4],

        "P": [P1, P2, P3, P4],   # kPa

        "V": [V1, V2, V3, V4],   # m³

        "S": [S1, S2, S3, S4],

        "Q_in": Q_in,

        "Q_out": Q_out,

        "W_net": W_net,

        "efficiency": efficiency,

        "gamma": gamma,

        "cv": cv,

        "mass": m
    }