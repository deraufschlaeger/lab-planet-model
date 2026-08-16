import numpy as np

def keywords_check(dictionary, index, *keywords):
    missing = [key for key in keywords if key not in dictionary]

    if missing:
        raise ValueError(
            f"Missing keywords {missing} in Shell with index {index}!"
        )

from eos_function import rocky_eos
from eos_function import calc_density_eos

def density_from_eos_profile(pressure_profile, temperature, eos_profile, interpH=None, interpHe=None, **kwargs):
  ''' INPUT:
      pressure_profile = [[p1lower, p1, p1upper], [p2lower. p2, p2upper], ..., [pNlower, pN, pNupper]]
      temperature = [T1, T2, ..., Tn]
      eos_profile = list of dics. One dictionary for each layer. The keyword 'eos' gives which equation of state to use. "he", "h", "rocky"(then K_0 and K'_0 (called 'k_d') and rho_0 need to be provided).
                    If eos is a list of either ['h', 'he'] or ['rocky_1', 'rocky_2'] then the parameter keyword 'X_H', 'Y_He' or 'M_{1,2}' need to be given

      FUNCTION gives the density from an equation of state. Different Equation of states are given in the eos_profile list of layer dictionaries

      OUTOUT should look like
      density = [rho1, rho2, ..., rhoN]
      '''
  N = len(pressure_profile)
  if N != len(eos_profile):
      raise ValueError('eos_profile needs to be same lenght as pressure_profile')

  if type(temperature) not in [np.ndarray, list]:
    temperature = np.full(N, temperature)
  T = np.array(temperature)

  density_profile = np.zeros(N)

  for i, layer_dict in enumerate(eos_profile):
      eos=layer_dict['eos']

      if type(eos) in [list, np.ndarray] and len(eos) >= 2:

          if 'h' in eos and 'he' in eos: # ['h', 'he'] and ['he', 'h']
            density_H = calc_density_eos(pressure_profile[i][1], T[i], interp=interpH)
            density_He = calc_density_eos(pressure_profile[i][1], T[i], interp=interpHe)
            keywords_check(layer_dict, i, "X_H", "Y_He")
            density_profile[i] = ((layer_dict['X_H'])/(density_H) + (layer_dict['Y_He']/(density_He)))**(-1) # see formula (1) in Miguel+2016 for mix

          elif 'rocky_1' in eos and 'rocky_2' in eos: # ['rocky_1', 'rocky_2']

            keywords_check(layer_dict, i,  "k_0_1", "k_d_1", "rho_0_1", "M_1", "k_0_2", "k_d_2", "rho_0_2", "M_2")
            density_1 = rocky_eos(pressure_profile[i][1], layer_dict['k_0_1'], layer_dict['k_d_1'], layer_dict['rho_0_1'])
            density_2 = rocky_eos(pressure_profile[i][1], layer_dict['k_0_2'], layer_dict['k_d_2'], layer_dict['rho_0_2'])
            density_profile[i] = ((layer_dict['M_1'])/(density_1) + (layer_dict['M_2'])/(density_2))**(-1)

        # other mixture possibilities?

      elif type(eos)==str or len(eos)==1:
          if type(eos) in [list, np.ndarray] and len(eos)==1:
              eos = eos[0] # just to be sure
          #single eos, so no mixture
          if eos == "he":
              density_profile[i] = calc_density_eos(pressure_profile[i][1], T[i], interp=interpHe)
                
          elif eos == "h":
              density_profile[i] = calc_density_eos(pressure_profile[i][1], T[i], interp=interpH)

          elif eos == "rocky":
              keywords_check(layer_dict, i, "k_0", "k_d", "rho_0")

              K_0 = layer_dict['k_0']
              K_d = layer_dict['k_d']
              rho_0 = layer_dict['rho_0']
              density_profile[i] = rocky_eos(pressure_profile[i][1], K_0, K_d, rho_0)
          else:
              raise ValueError(f"Unknown equation of state: {eos} in shell with index {i}! One string was detected.")
      else:
          raise ValueError(f"Unknown equation of state: {eos} in shell with index {i}! It either needs to be a string, e.g. 'h', 'he' or 'rocky', or a list of strings (['h', 'he'], ['he', 'h'] or ['rocky_1', 'rocky_2'] for a mixture.")
  return density_profile
