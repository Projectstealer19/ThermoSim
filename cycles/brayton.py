import numpy as np

def brayton_cycle(T1, T3, rp, V1):
    # ------------------------------------------------
    # AIR PROPERTIES (fixed for Brayton cycle)
    # ------------------------------------------------
    R = 287                 # J/kg-K
    gamma = 1.4
    cp = gamma * R / (gamma - 1)
    cv = cp - R

    # ------------------------------------------------
    # REFERENCE CONDITIONS
    # ------------------------------------------------
    P1 = R * T1 / V1
    S1 = 100                # J/kg-K reference entropy

    # ------------------------------------------------
    # STATE 1 → 2: Isentropic Compression
    # ------------------------------------------------
    exponent = (gamma - 1) / gamma
    T2 = T1 * (rp ** exponent)
    P2 = P1 * rp
    V2 = V1 * (T2 / T1) / rp
    S2 = S1

    # ------------------------------------------------
    # STATE 2 → 3: Constant Pressure Heat Addition
    # ------------------------------------------------
    P3 = P2
    T3 = T3
    V3 = V2 * (T3 / T2)
    S3 = S2 + cp * np.log(T3 / T2)

    # ------------------------------------------------
    # STATE 3 → 4: Isentropic Expansion
    # ------------------------------------------------
    T4 = T3 / (rp ** exponent)
    P4 = P1
    V4 = V3 * (T4 / T3) * (P3 / P4)
    S4 = S3

    # ------------------------------------------------
    # HEAT TRANSFER
    # ------------------------------------------------
    Q_in = cp * (T3 - T2)
    Q_out = cp * (T4 - T1)

    # ------------------------------------------------
    # WORK
    # ------------------------------------------------
    W_compressor = cp * (T2 - T1)
    W_turbine = cp * (T3 - T4)
    W_net = W_turbine - W_compressor

    # ------------------------------------------------
    # BACK WORK RATIO
    # ------------------------------------------------
    back_work_ratio = W_compressor / W_turbine

    # ------------------------------------------------
    # THERMAL EFFICIENCY
    # ------------------------------------------------
    efficiency = (W_net / Q_in) * 100

    return {
        "T": [T1, T2, T3, T4],
        "P": [P1, P2, P3, P4],
        "V": [V1, V2, V3, V4],
        "S": [S1, S2, S3, S4],
        "Q_in": Q_in,
        "Q_out": Q_out,
        "W_net": W_net,
        "W_compressor": W_compressor,
        "W_turbine": W_turbine,
        "back_work_ratio": back_work_ratio,
        "efficiency": efficiency,
        "gamma": gamma,
        "R": R,
        "cp": cp,
        "cv": cv,
        "rp": rp
    }