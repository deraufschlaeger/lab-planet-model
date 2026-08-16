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

def give_radius_from_helium_abundance(he_ab, num_mix_layers = 20, temp = 160, core_mass_ratio=0.2, num_core_layers = 10, mass_total = 1.898e27, rho_0 = 1300, quiet=True):
    
    layers_def = [
        {
            'eos_type': 'rocky',
            'params': {'k_0': 270.6e9, 'k_d': 3.81, 'rho_0': 4105.9},
            'num_layers': num_core_layers
        },
        {
            'eos_type': ['h', 'he'],
            'params': {'X_H': 1-he_ab, 'Y_He': he_ab},
            'num_layers': num_mix_layers
        },
        {
            'eos_type': 'h',
            'params': {},
            'num_layers': 180
        }
    ]
        
    eos_profile = create_eos_profile(layers_def)

    N = len(eos_profile)

    mass_dictionary = {'n_core': num_core_layers,
                       'core_mass_ratio': core_mass_ratio}

    r_profile, p_profile, rho_profile, temp_profile = multi_iteration(rho_0, mass_total, N, temp, eos_profile, quiet=quiet, max_iter = 40, mass_distro_profile=mass_dictionary)
    if quiet==False:
        print(core_mass_ratio)
        print(r_profile[-1][-1])

    return r_profile[-1][-1]

abundance_array = np.linspace(0, 1, num=10)
print('used Helium Abundances:', abundance_array)

'''
#Vary the number of mixture layers

layers_num_array = range(1, 21, 2)
print('Used Number of layers:', list(layers_num_array))

n_num = len(layers_num_array)

cm = plt.get_cmap('gist_rainbow')
fig, ax = plt.subplots(figsize=(20,12))
ax.set_prop_cycle(color=[cm(1.*i/n_num) for i in range(n_num)])
                     

for num_mix_layers in layers_num_array:
    

    radius_array = [give_radius_from_helium_abundance(ab, num_mix_layers=num_mix_layers)/1e3 for ab in abundance_array]

    #print('resulting Radii:', np.array(radius_array))
    ax.plot(abundance_array, radius_array, label=f'num_mix_layers={num_mix_layers}')

ax.set_ylabel('Radius [km]')
ax.set_xlabel('Helium abundance just above the core')
ax.grid(True)
ax.legend()
plt.show()

'''

#Vary the core mass ratio
n_num = 10

cmr_array = np.linspace(0.001 , 0.9, num=n_num)
print('used cmr:', cmr_array)

cm = plt.get_cmap('gist_rainbow')
fig, ax = plt.subplots()
ax.set_prop_cycle(color=[cm(1.*i/n_num) for i in range(n_num)])

slope_list = []
for cmr in cmr_array:

    radius_array = [give_radius_from_helium_abundance(ab, core_mass_ratio=cmr) / 1e3 for ab in abundance_array]
    b, m = np.polynomial.polynomial.polyfit(abundance_array, radius_array, 1)
    #slope_list.append(m)
    ax.scatter(cmr, m, label=f'cmr={cmr:.3f}')
    #ax.plot(abundance_array, radius_array, label=f'cmr={cmr:.3f}')

#ax.scatter(cmr_array, slope_list)
ax.set_ylabel('slope [km]')
ax.set_xlabel('core mass ratio')
#ax.set_ylabel('radius [km]')
#ax.set_xlabel('helium abundance right above the core')
ax.grid(True)
#ax.set_title('slope of outermost Radii, when increasing helium abundance just above the core from 0 (no helium) to 1 (all helium)')
#ax.legend()
plt.show()
