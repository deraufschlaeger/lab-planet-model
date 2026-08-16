import numpy as np
#import matplotlib.pyplot as plt
import math
import pandas as pd

import scipy.interpolate as ipl

#-------------------READ-DATA-------------------------------------------------------

# Hydrogen data
data_h_raw = pd.read_csv(
    "apjs504506t2_mrt.txt",
    sep=r"\s+",
    skiprows=15,
    usecols=[0, 1, 2, 3],
    names=["rho_H_raw", "T_H_raw", "p_H_raw", "E_H_raw"]
)

E_H_raw = data_h_raw["E_H_raw"].to_numpy() * 1e6 #J/kg
p_H_raw = data_h_raw["p_H_raw"].to_numpy() * 1e9 #Pa
T_H_raw = data_h_raw["T_H_raw"].to_numpy() #K
rho_H_raw = data_h_raw["rho_H_raw"].to_numpy() * 1000 #kg/m^3

# take the log of all except the Energy
#rho_H_log = np.log(rho_H_raw)
#T_H_log = np.log(T_H_raw)
#p_H_log = np.log(p_H_raw)


#Tp_H_log = np.column_stack((T_H_log, p_H_log))
Tp_H_raw = np.column_stack((T_H_raw, p_H_raw))
#rhoT_log = np.column_stack((T_H_log, rho_H_log))
rhoT_raw = np.column_stack((T_H_raw, rho_H_raw))

#-----------------Create-Interpolator-------------------------------------------------

#linear_interp_rho_H_log = ipl.LinearNDInterpolator(Tp_H_log, rho_H_log) # rho(T, p)
linear_interp_rho_H_raw = ipl.LinearNDInterpolator(Tp_H_raw, rho_H_raw) # rho(T, p)

'''
# quickly plot
X=np.linspace(min(T_H_log), max(T_H_log))
Y=np.linspace(min(p_H_log), max(p_H_log))

X, Y = np.meshgrid(X, Y)

Z=linear_interp_rho_H_log(X, Y)

plt.pcolormesh(X, Y, np.exp(Z), shading='auto')
plt.colorbar()
plt.show()
'''
#linear_interp_E_H = ipl.LinearNDInterpolator(rhoT_log, E_H_raw) #E(rho, T)
linear_interp_E_H_raw = ipl.LinearNDInterpolator(rhoT_raw, E_H_raw) #E(rho, T)

#----------------test-interpolatoren-------------------------------------------------
def create_space(lower, upper, steps, spacetype='lin'):
    if spacetype=='lin':
        return np.linspace(lower, upper, steps)
    if spacetype=='log':
        return np.logspace(lower, upper, steps)

steps=100
spacetype='lin'

print(linear_interp_rho_H_raw(create_space(min(T_H_raw), max(T_H_raw), steps, spacetype=spacetype), create_space(min(p_H_raw), max(p_H_raw), steps, spacetype=spacetype)))

print(linear_interp_E_H_raw(create_space(min(rho_H_raw), max(rho_H_raw), steps, spacetype=spacetype), create_space(min(T_H_raw), max(T_H_raw), steps, spacetype=spacetype)))
#-----------------create-derivations-functions----------------------------------------

# Angenommen `my_linear_interp` ist dein bestehender linearer Interpolator
# Funktion: f(x, y)

def get_derivative_x(interp, x, y, h=1e-5):
    # Zentrale Differenz nach x
    return (interp(x + h, y) - interp(x - h, y)) / (2 * h)


def get_derivative_y(interp, x, y, h=1e-5):
    # Zentrale Differenz nach y
    return (interp(x, y + h) - interp(x, y - h)) / (2 * h)

# rho ableitungen

def get_drho_dp(T, p, **kwargs):
    return get_derivative_y(linear_interp_rho_H_raw, T, p, **kwargs)

def get_drho_dT(T, p, **kwargs):
    return get_derivative_x(linear_interp_rho_H_raw, T, p, **kwargs)

# Energie ableitungen

def get_dE_drho(rho, T, **kwargs):
    return get_derivative_x(linear_interp_E_H_raw, rho, T, **kwargs)

def get_dE_dT(rho, T, **kwargs):
    return get_derivative_y(linear_interp_E_H_raw, rho, T, **kwargs)

#----------------dT/dP---------------------------------------

def get_dT_dp(p, T, rho, h=1e-5, coeff=-1, **kwargs):
    dE_dT_val = get_dE_dT(rho, T, h=h, **kwargs)
    dE_drho_val = get_dE_drho(rho, T, h=h, **kwargs)
    drho_dp_val = get_drho_dp(T, p, h=h, **kwargs)
    drho_dT_val = get_drho_dT(T, p, h=h, **kwargs)

    print(
    f"rho={rho:.3e}, "
    f"dE_dT={dE_dT_val:.3e}, "
    f"dE_drho={dE_drho_val:.3e}, "
    f"drho_dp={drho_dp_val:.3e}, "
    f"drho_dT={drho_dT_val:.3e}"
    )
    
    return coeff*drho_dp_val/(drho_dT_val + dE_dT_val * (dE_drho_val - p/(rho**2))**(-1))

#--------------adiabatic-profile-creator--------------------------------

def get_adiabatic_temp_profile(p_profile, rho_profile, TN, **kwargs):
    '''
    INPUT:
    p_profile should look like this [p1, p2, p3, ..., pN] in Pascal
    rho_profile should look like this [rho1, rho2, rho3, ..., rhoN] in kg/m^3
    TN is surface temp in Kelvin

    OUTPUT:
    T_profile shoould look like [T1, T2, T3, ..., TN]
    '''
    
    N = len(p_profile)
    T_profile = np.zeros(N)
    T_profile[-1] = TN

    for i in range(N-1, 0, -1):
        p_val = p_profile[i]
        T_val = T_profile[i]
        rho_val = rho_profile[i]
 
        dT_dp_val = get_dT_dp(p_val, T_val, rho_val, **kwargs)
        if dT_dp_val < 0:
            dT_dp_val = 0
            print(f"dT_dp_val was negative for {i}")
        
        dp_val = np.abs(p_profile[i-1] - p_profile[i])
        T_profile[i-1] = T_profile[i] + dT_dp_val * dp_val   

    return T_profile
