import numpy as np

from multiiter import interpolator_dE_dT_H, interpolator_dE_drho_H, interpolator_dE_dT_He, interpolator_dE_drho_He, drho_dT_H3, drho_dp_H3, drho_dT_He3, drho_dp_He3, interpolator, interpolatorHe

from eos_function import calc_density_eos

def find_T_profile(pressure_profile, eos_profile, density_profile, T_0):
  p_profile = pressure_profile[:, 2]

  T_profile = np.zeros_like(p_profile)
  T_profile[-1] = T_0

  for i in range(len(p_profile)-1, 0, -1):
      

      T = T_profile[i]
      p = p_profile[i]

      if eos_profile[i]['eos'] == 'h':
          # hydrogen
          rho = calc_density_eos(p, T, interpolator)
          dEdT = interpolator_dE_dT_H(np.column_stack((T, rho)))[0]
          dEdrho = interpolator_dE_drho_H(np.column_stack((T, rho)))[0]
          drhodT = drho_dT_H3(T, p, rho)
          drhodp = drho_dp_H3(T, p, rho)

      else:
          # Helium
          rho = calc_density_eos(p, T, interpolatorHe)
          dEdT = interpolator_dE_dT_He(np.column_stack((T, rho)))[0]
          dEdrho = interpolator_dE_drho_He(np.column_stack((T, rho)))[0]
          drhodT = drho_dT_He3(T, p, rho)
          drhodp = drho_dp_He3(T, p, rho)

      dTdp = -drhodp / (drhodT + dEdT/(dEdrho - p/rho**2))
      dp = p_profile[i-1] - p
      dT = dTdp * dp

      # standard, linear version
      # T_profile[i-1] = T + max(dT, 0)
      # log-integrated alternative (which gives a factor rather than an addend)
      T_profile[i-1] = T*(p_profile[i-1]/p)**(p/T*max(dTdp,0))

  return T_profile
