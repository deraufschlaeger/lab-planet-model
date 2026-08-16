import numpy as np
import argparse
from joblib import load
from pathlib import Path

G = 6.674e-11

# -----------------------LOAD-INTERPOLATORS------------------------------------------
interp_dirname = 'interpolators'

interpolator = load(f"./{interp_dirname}/rho_Tp_log_log_Hydrogen_interp.joblib")

interpolatorHe = load(f"./{interp_dirname}/rho_Tp_log_log_Helium_interp.joblib")

interpolatorENer = load(f"./{interp_dirname}/E_rhoT_raw_raw_Hydrogen.joblib")

interpolatorENerHe = load(f"./{interp_dirname}/E_rhoT_raw_raw_Helium.joblib")

#derivatives

interpolator_dE_dT_H = load(f"./{interp_dirname}/dE_dT_T_rho_raw_raw_Hydrogen.joblib")

interpolator_dE_dT_He = load(f"./{interp_dirname}/dE_dT_T_rho_raw_raw_Helium.joblib")

interpolator_dE_drho_H = load(f"./{interp_dirname}/dE_drho_T_rho_raw_raw_Hydrogen.joblib")

interpolator_dE_drho_He = load(f"./{interp_dirname}/dE_drho_T_rho_raw_raw_Helium.joblib")

# ----------------------derivative-functions-------------------------------------------
def drho_dT_H3(T_, p_, rhoo, h = 1e-4):
    logT = np.log(T_)
    logp = np.log(p_)

    dlogrho_dlogT = (
        interpolator(logT + h, logp)
        - interpolator(logT, logp)
    ) / h

    return (rhoo / T_) * dlogrho_dlogT

def drho_dT_He3(T_, p_, rhoo, h = 1e-4):
    logT = np.log(T_)
    logp = np.log(p_)

    dlogrho_dlogT = (
        interpolatorHe(logT + h, logp)
        - interpolatorHe(logT, logp)
    ) / h

    return (rhoo / T_) * dlogrho_dlogT

def drho_dp_H3(T_, p_, rhoo, h = 1e-4):
    logT = np.log(T_)
    logp = np.log(p_)

    dlogrho_dlogp = (
        interpolator(logT, logp + h)
        - interpolator(logT, logp)
    ) / h

    return (rhoo / p_) * dlogrho_dlogp

def drho_dp_He3(T_, p_, rhoo, h = 1e-4):
    logT = np.log(T_)
    logp = np.log(p_)

    dlogrho_dlogp = (
        interpolatorHe(logT, logp + h)
        - interpolatorHe(logT, logp)
    ) / h

    return (rhoo / p_) * dlogrho_dlogp

#-----------------------RADIUS-FUNCTION----------------------------------------------

from radius_function import find_radius_profile

#-------------------------PRESSURE-FUNCTION--------------------------------------------

from pressure_function import find_pressure_profile

#----------------------------------TEMPERATURE-FUNCTION-------------------------------

from adiabatic_temperature_function import find_T_profile

#-----------------------------------ONE-CYCLE-FUNCTION---------------------------------
def create_eos_profile(layers_def):
    '''INPUT Example:

    layer_definitions_example = [
    {
        'eos_type': 'rocky',
        'params': {'k_0': 200e9, 'k_d': 3.5, 'rho_0': 5500},
        'num_layers': 50 # 50 layers for the rocky core
    },
    {
        'eos_type': 'h',
        'params': {'temperature': 100000}, # Assuming a constant temperature for this hydrogen section
        'num_layers': 50 # 50 layers for the hydrogen shell
    }
]

    OUTPUT should be a list of dictionaries for each layer containing information of th EOS to use in this layer
  '''
    full_eos_profile=[]

    for layer_dict in layers_def:
        eos_type = layer_dict['eos_type']
        if 'params' in layer_dict:
            params_dict = layer_dict['params']
        n_layers = int(layer_dict['num_layers'])
        for _ in range(n_layers):
            layer={'eos': eos_type}
            layer.update(params_dict)
            full_eos_profile.append(layer)

    return full_eos_profile

from eos_mixture_function import density_from_eos_profile

def one_cycle_var(mass_profile, first_density, temperature, eos_profile, **kwargs):
  ''' INPUT:
      mass_profile = [m1,m2,m3,..., mN]
      first_density = constant value or array of values
      temperature = [T1, T2, ..., Tn]
      eos_profile = {first transition: 'eos_below_first_transition',
                     second transition: 'eos_between_first_and_second_transition',
                     ...}
      FUNCTION represents one cycle

      OUTPUT should look like
      new_density = [[rho1lower, rho1, rho1upper], [rho2lower, rho2, rho2upper], ..., [rhoNlower, rhoN, rhoNupper]]
      '''

  r_profile = find_radius_profile(first_density, mass_profile) #RADIUS
  p_profile = find_pressure_profile(r_profile, mass_profile) #PRESSURE

  new_density = density_from_eos_profile(p_profile, temperature, eos_profile, interpH=interpolator, interpHe=interpolatorHe, **kwargs) #EQUATION OF STATE

  temp_profile = find_T_profile(p_profile, eos_profile, new_density, temperature[-1], **kwargs)

  return r_profile, p_profile, new_density, temp_profile

#-------------------------MULTI-CYCLE-FUNCTION----------------------------------------

from create_profiles import create_mass_profile, create_temp_profile, create_density_profile

################################################################################

def multi_iteration(starting_density, mass_total, N, T, eos_profile, mass_profile=None,
                    mass_distro_profile='constant', temp_distro_profile='constant',
                    density_distro_profile='constant', tolerance=1e-6, max_iter=20,
                    quiet=True, print_iter=2, **kwargs):
  if mass_profile==None:
    mass_profile = create_mass_profile(mass_total, N, profile=mass_distro_profile)
  else:
    mass_profile = np.array(mass_profile)

  if type(T) in [np.ndarray, list]:
    T = T
  else:
    T = create_temp_profile(T, N, profile=temp_distro_profile)

  if type(starting_density) in [np.ndarray, list]:
    rho = starting_density
  else:
    rho = create_density_profile(starting_density, N, profile=density_distro_profile)

  #Model-Check------------------  
  iter_counter=0
  radius_for_each_iter_array=[]
  #---------------------------
  
  for iteration in range(max_iter):
    iter_counter+=1  
    r_profile, p_profile, new_rho, temp_profile = one_cycle_var(mass_profile, rho, T, eos_profile, **kwargs)

    rel_diff = abs(new_rho[0] - rho[0]) / rho[0]

    if quiet == False: #and iteration >= max_iter-print_iter:
      print(f"Relative Änderung bei Iteration {iteration+1}:", rel_diff)
      
    radius_for_each_iter_array.append(r_profile[-1][-1])
    
    # Abbruchbedingung
    if rel_diff < tolerance:
      if quiet == False:
        print("\nKonvergenz erreicht.")
      break

    # neues Profil übernehmen
    rho = new_rho.copy()
    T = temp_profile.copy()

  if quiet == False:
    print("\nFinales Radiusprofil:")
    print(r_profile)

    print("\nFinales Druckprofil:")
    print(p_profile)

    print("\nFinales Dichteprofil:")
    print(new_rho)

    print("\nFinales Temperaturprofil:")
    print(temp_profile)

  return r_profile, p_profile, new_rho, temp_profile

#, iter_counter, radius_for_each_iter_array
