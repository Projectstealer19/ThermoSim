import math
def brayton_cycle(T1 , T3 , rp , gamma):
    R = 8.314
    exp = (gamma-1)/gamma
    T2 = T1 * (rp ** exp)
    T4 = T3 /rp ** exp
    efficiency = 1 - (1/(rp ** exp))
    # Cp = gamma * R / (gamma -1)
    # delta_s = Cp * math.log(T3/T2)
    return { "T1" : T1 , "T2" : T2 , "T3" : T3 , "T4" : T4 , "efficiency" : efficiency*100}