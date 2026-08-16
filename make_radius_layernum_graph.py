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

def give_radius_itercount_from_layernum(layer_multiplier, num_hydrogen_layers=180, he_ab=0.25, num_mix_layers = 10, temp = 160, core_mass_ratio=0.2, num_core_layers = 10, mass_total = 1.898e27, rho_0 = 1300, quiet=True):
    
    layers_def = [
        {
            'eos_type': 'rocky',
            'params': {'k_0': 270.6e9, 'k_d': 3.81, 'rho_0': 4105.9},
            'num_layers': int(num_core_layers * layer_multiplier)
        },
        {
            'eos_type': ['h', 'he'],
            'params': {'X_H': 1-he_ab, 'Y_He': he_ab},
            'num_layers': int(num_mix_layers * layer_multiplier)
        },
        {
            'eos_type': 'h',
            'params': {},
            'num_layers': int(num_hydrogen_layers * layer_multiplier)
        }
    ]
        
    eos_profile = create_eos_profile(layers_def)

    N = len(eos_profile)

    mass_dictionary = {'n_core': num_core_layers,
                       'core_mass_ratio': core_mass_ratio}

    r_profile, p_profile, rho_profile, temp_profile, iter_counter = multi_iteration(rho_0, mass_total, N, temp, eos_profile, quiet=quiet, max_iter = 40, mass_distro_profile=mass_dictionary)
    if quiet==False:
        print(core_mass_ratio)
        print(r_profile[-1][-1])

    return r_profile[-1][-1], iter_counter

multiplier_array = np.linspace(0.1, 10, num=30)
print('used Multipliers:', multiplier_array)

#Vary the number of layers with a multiplier_array
num_core_layers = 10
num_mix_layers = 10
num_hydrogen_layers = 180

iter_counter_array = []
radius_array = []

for multiplier in multiplier_array:
    
    radius, itercounter = give_radius_itercount_from_layernum(multiplier, num_core_layers=num_core_layers, num_mix_layers=num_mix_layers, num_hydrogen_layers=num_hydrogen_layers)
    iter_counter_array.append(itercounter)
    radius_array.append(radius/1e3)

num_layer_array = [int(num_core_layers*multiplier) + int(num_mix_layers*multiplier) + int(num_hydrogen_layers*multiplier) for multiplier in multiplier_array]

print('resulting Radii:', np.array(radius_array))
print('iter_counters:', iter_counter_array)

fig, ax = plt.subplots(figsize=(20,12))

lasize = 25
linewidth= 3

color1 = 'tab:blue'
ax.plot(num_layer_array, radius_array, c=color1, lw=linewidth)
ax.set_ylabel('radius [km]', color=color1, fontsize=lasize)
ax.set_xlabel('Number of Layers', fontsize=lasize)
ax.tick_params(axis='y', labelcolor=color1, labelsize=lasize)

ax.tick_params(axis='x', labelsize=lasize)

ax2 = ax.twinx()

color2 = 'tab:red'
ax2.set_ylabel('Number of Iteration needed to converge', color=color2, fontsize=lasize)
ax2.plot(num_layer_array, iter_counter_array, color=color2, lw=linewidth)
ax2.tick_params(axis='y', labelcolor=color2, labelsize=lasize)

ax.grid(True)
fig.tight_layout()
#ax.legend()
plt.show()
