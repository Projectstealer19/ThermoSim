from CoolProp.CoolProp import PropsSI

def refrigeration_cycle(T_evap, T_cond, eta_comp):

    # ------------------------------------------------
    # REFRIGERANT
    # ------------------------------------------------

    refrigerant = 'R134a'

    # ------------------------------------------------
    # PRESSURES
    # ------------------------------------------------

    P_evap = PropsSI(
        'P',
        'T', T_evap,
        'Q', 1,
        refrigerant
    )

    P_cond = PropsSI(
        'P',
        'T', T_cond,
        'Q', 0,
        refrigerant
    )

    # ------------------------------------------------
    # STATE 1
    # Saturated vapor leaving evaporator
    # ------------------------------------------------

    H1 = PropsSI(
        'H',
        'T', T_evap,
        'Q', 1,
        refrigerant
    )

    S1 = PropsSI(
        'S',
        'T', T_evap,
        'Q', 1,
        refrigerant
    )

    # ------------------------------------------------
    # STATE 2s
    # Ideal compressor outlet
    # ------------------------------------------------

    H2s = PropsSI(
        'H',
        'P', P_cond,
        'S', S1,
        refrigerant
    )

    # ------------------------------------------------
    # STATE 2
    # Actual compressor outlet
    # ------------------------------------------------

    H2 = H1 + (H2s - H1) / eta_comp

    T2 = PropsSI(
        'T',
        'P', P_cond,
        'H', H2,
        refrigerant
    )

    S2 = PropsSI(
        'S',
        'P', P_cond,
        'H', H2,
        refrigerant
    )

    # ------------------------------------------------
    # STATE 3
    # Saturated liquid leaving condenser
    # ------------------------------------------------

    H3 = PropsSI(
        'H',
        'T', T_cond,
        'Q', 0,
        refrigerant
    )

    S3 = PropsSI(
        'S',
        'T', T_cond,
        'Q', 0,
        refrigerant
    )

    # ------------------------------------------------
    # STATE 4
    # Throttling valve
    # h3 = h4
    # ------------------------------------------------

    H4 = H3

    T4 = PropsSI(
        'T',
        'P', P_evap,
        'H', H4,
        refrigerant
    )

    S4 = PropsSI(
        'S',
        'P', P_evap,
        'H', H4,
        refrigerant
    )

    # ------------------------------------------------
    # STATE TEMPERATURES
    # ------------------------------------------------

    T1 = T_evap

    T3 = T_cond

    # ------------------------------------------------
    # PERFORMANCE
    # ------------------------------------------------

    Q_in = H1 - H4

    W_comp = H2 - H1

    COP = Q_in / W_comp

    # ------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------

    return {

        "T": [T1, T2, T3, T4],

        "P": [P_evap, P_cond],

        "H": [H1, H2, H3, H4],

        "S": [S1, S2, S3, S4],

        "Q_in": Q_in,

        "W_comp": W_comp,

        "COP": COP
    }