
delta_rho_oi = rho_profile[:-1] - rho_profile[1:]

#-LOCALSTUFF------------------------------------------------------------------
from eos_function import calc_density_eos
from joblib import load

interp_dirname = 'interpolators'

interpolator = load(f"./{interp_dirname}/rho_Tp_log_log_Hydrogen_interp.joblib")

interpolatorHe = load(f"./{interp_dirname}/rho_Tp_log_log_Helium_interp.joblib")
#-----------------------------------------------------------------------------


for i, delta_rho in enumerate(delta_rho_oi):
    if delta_rho < 0:
        print(f'delta_rho from shell transition {i} to {i+1} is negative, so got less dense from outside to inside')
        temp_sur = temp_profile[i:i+2]
        p_sur = p_profile[i:i+2]
        rho_sur = rho_profile[i:i+2]

        print('density H', calc_density_eos(p_sur, temp_sur, interp=interpolator))
        print('density He', calc_density_eos(p_sur, temp_sur, interp=interpolatorHe))
