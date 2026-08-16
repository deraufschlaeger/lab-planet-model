from multiiter import multi_iteration, create_eos_profile
import numpy as np
from matplotlib import pyplot as plt

#jupyter:

'''rho_0 = 1249.5 kg/m^3
K_0 = 4.26 GPa
K_0' = 7.75

Perovskite
rho_0 4105.9
K_0 = 270.6
K_0' = 3.81
'''

def give_radius_from_cmr(core_mass_ratio, num_core_layers = 25, mass_total = 1.898e27, rho_0 = 1300, T_0 = 160, layers_def=None, quiet=True):
    if layers_def==None:
        layers_def = [
            {
                'eos_type': 'rocky',
                'params': {'k_0': 270.6e9, 'k_d': 3.81, 'rho_0': 4105.9},
                'num_layers': num_core_layers
            },
            {
                'eos_type': ['h', 'he'],
                'params': {'X_H': 0.75, 'Y_He': 0.25},
                'num_layers': 10*2.5
            },
            {
                'eos_type': 'h',
                'params': {},
                'num_layers': 180*2.5 
            }
        ]

    eos_profile = create_eos_profile(layers_def)

    N = len(eos_profile)

    mass_dictionary = {'n_core': num_core_layers,
                       'core_mass_ratio': core_mass_ratio}

    r_profile, p_profile, rho_profile, temp_profile = multi_iteration(rho_0, mass_total, N, T_0, eos_profile, quiet=quiet, max_iter = 40, mass_distro_profile=mass_dictionary)
    if quiet==False:
        print(core_mass_ratio)
        print(r_profile[-1][-1])

    return r_profile[-1][-1]

cmr_array = np.linspace(0.00001 , 1, num=40)
#[0.01, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]

print('Used Core Mass Ratios:', cmr_array)

radius_array = []

for cmr in cmr_array:
    radius_array.append(give_radius_from_cmr(cmr, mass_total=5.683e26, rho_0=687, T_0=134)/1e3)

print('Resulting Radii:', np.array(radius_array))

print('radii between 0.02 and 0.05 cmr:', np.array(radius_array)[np.argwhere((0.15765<cmr_array) & (cmr_array<0.189180))])

plt.scatter(cmr_array, radius_array)
plt.ylabel('radius [km]')
plt.xlabel('core mass ratio')
plt.grid()
plt.tight_layout()
plt.show()
