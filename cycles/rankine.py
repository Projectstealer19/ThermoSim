from CoolProp.CoolProp import PropsSI

def rankine_cycle(
        P_boiler,
        P_cond,
        T3,
        eta_turbine,
        eta_pump
):

    # ------------------------------------------------
    # STATE 1
    # Saturated liquid at condenser pressure
    # ------------------------------------------------

    h1 = PropsSI('H', 'P', P_cond, 'Q', 0, 'Water')

    s1 = PropsSI('S', 'P', P_cond, 'Q', 0, 'Water')

    T1 = PropsSI('T', 'P', P_cond, 'Q', 0, 'Water')

    # ------------------------------------------------
    # STATE 2s (Ideal Pump)
    # ------------------------------------------------

    s2s = s1

    h2s = PropsSI('H', 'P', P_boiler, 'S', s2s, 'Water')

    # ------------------------------------------------
    # STATE 2 (Actual Pump)
    # ------------------------------------------------

    h2 = h1 + ((h2s - h1) / eta_pump)

    T2 = PropsSI('T', 'P', P_boiler, 'H', h2, 'Water')

    s2 = PropsSI('S', 'P', P_boiler, 'H', h2, 'Water')

    # ------------------------------------------------
    # STATE 3
    # Boiler outlet / Turbine inlet
    # ------------------------------------------------

    h3 = PropsSI('H', 'P', P_boiler, 'T', T3, 'Water')

    s3 = PropsSI('S', 'P', P_boiler, 'T', T3, 'Water')

    # ------------------------------------------------
    # STATE 4s (Ideal Turbine)
    # ------------------------------------------------

    s4s = s3

    h4s = PropsSI('H', 'P', P_cond, 'S', s4s, 'Water')

    # ------------------------------------------------
    # STATE 4 (Actual Turbine)
    # ------------------------------------------------

    h4 = h3 - eta_turbine * (h3 - h4s)

    T4 = PropsSI('T', 'P', P_cond, 'H', h4, 'Water')

    s4 = PropsSI('S', 'P', P_cond, 'H', h4, 'Water')

    # ------------------------------------------------
    # PERFORMANCE CALCULATIONS
    # ------------------------------------------------

    W_turbine = h3 - h4

    W_pump = h2 - h1

    Q_in = h3 - h2

    efficiency = ((W_turbine - W_pump) / Q_in) * 100

    # ------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------

    return {

        "T": [T1, T2, T3, T4],

        "S": [s1, s2, s3, s4],

        "H": [h1, h2, h3, h4],

        "efficiency": efficiency,

        "W_turbine": W_turbine,

        "W_pump": W_pump,

        "Q_in": Q_in
    }