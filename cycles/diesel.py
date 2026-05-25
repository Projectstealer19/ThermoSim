import numpy as np


def diesel_cycle(T1: float, r: float, rc: float, V1: float) -> dict:
    """
    Ideal air-standard Diesel cycle simulation.

    Parameters
    ----------
    T1 : float  Temperature at State 1 (K)
    r  : float  Compression ratio  V1/V2  (dimensionless)
    rc : float  Cutoff ratio       V3/V2  (dimensionless)
    V1 : float  Specific volume at State 1 (m³/kg).
                Assumes m = 1 kg, so V1 is passed as absolute volume in m³
                and treated directly as specific volume.
                The caller is responsible for converting litres:
                    V1_m3 = V1_litres / 1000.0

    Returns
    -------
    dict
        T, P, V, S  – Python lists of 4 plain floats (SI units: K, Pa, m³, J/kg·K)
        Q_in        – specific heat added     (J/kg)
        Q_out       – specific heat rejected  (J/kg)
        W_net       – specific net work       (J/kg)
        efficiency  – thermal efficiency      (%)
        gamma, cv, cp, m
    """

    # ------------------------------------------------------------------
    # Air-standard constants
    # ------------------------------------------------------------------
    R     = 287.0          # Specific gas constant  (J/kg·K)
    gamma = 1.4            # Heat-capacity ratio
    cp    = 1005.0         # Constant-pressure specific heat  (J/kg·K)
    cv    = cp / gamma     # Constant-volume specific heat    (J/kg·K)  ≈ 717.86
    S1    = 100.0          # Reference entropy                (J/kg·K)

    # ------------------------------------------------------------------
    # State 1 — start of compression
    # m = 1 kg  →  V1 is specific volume (m³/kg)
    # Ideal gas law:  P1 = R·T1 / v1
    # ------------------------------------------------------------------
    P1 = (R * T1) / V1                  # Pa

    # ------------------------------------------------------------------
    # State 2 — after isentropic compression  (1 → 2)
    # ------------------------------------------------------------------
    V2 = V1 / r
    T2 = T1 * (r ** (gamma - 1.0))
    P2 = P1 * (r ** gamma)
    S2 = S1                             # ΔS = 0  (isentropic)

    # ------------------------------------------------------------------
    # State 3 — after constant-pressure heat addition  (2 → 3)
    # ------------------------------------------------------------------
    P3 = P2                             # isobaric
    V3 = V2 * rc
    T3 = T2 * rc                        # ideal gas at const P: T ∝ V
    S3 = S2 + cp * float(np.log(T3 / T2))

    # ------------------------------------------------------------------
    # State 4 — after isentropic expansion  (3 → 4)
    # ------------------------------------------------------------------
    V4 = V1                             # back to full cylinder volume
    T4 = T3 * ((V3 / V4) ** (gamma - 1.0))
    P4 = P3 * ((V3 / V4) ** gamma)
    S4 = S3                             # ΔS = 0  (isentropic)

    # ------------------------------------------------------------------
    # Performance  (all specific: per kg of air)
    # ------------------------------------------------------------------
    Q_in       = cp * (T3 - T2)
    Q_out      = cv * (T4 - T1)
    W_net      = Q_in - Q_out
    efficiency = (W_net / Q_in) * 100.0

    # ------------------------------------------------------------------
    # Return everything as plain Python floats — guarantees clean repr
    # when values are injected into JavaScript via f-string.
    # np.log / numpy arithmetic can return np.float64 whose repr changes
    # between numpy versions and can produce 'np.float64(x)' literals that
    # are invalid JS syntax.
    # ------------------------------------------------------------------
    return {
        "T":          [float(T1), float(T2), float(T3), float(T4)],
        "P":          [float(P1), float(P2), float(P3), float(P4)],
        "V":          [float(V1), float(V2), float(V3), float(V4)],
        "S":          [float(S1), float(S2), float(S3), float(S4)],
        "Q_in":       float(Q_in),
        "Q_out":      float(Q_out),
        "W_net":      float(W_net),
        "efficiency": float(efficiency),
        "gamma":      float(gamma),
        "cv":         float(cv),
        "cp":         float(cp),
    }