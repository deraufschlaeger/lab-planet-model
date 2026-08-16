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

def give_radius_from_temp(temp, core_mass_ratio=0.2, num_core_layers = 25, mass_total = 1.898e27, rho_0 = 1300, layers_def=None, quiet=True):
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

    r_profile, p_profile, rho_profile, temp_profile = multi_iteration(rho_0, mass_total, N, temp, eos_profile, quiet=quiet, max_iter = 40, mass_distro_profile=mass_dictionary)

    return r_profile, temp_profile

n_num = 30

cm = plt.get_cmap('gist_rainbow')
fig, ax = plt.subplots(figsize=(20,12))

lasize = 25
linewidth= 3

ax.set_prop_cycle(color=[cm(1.*i/n_num) for i in range(n_num)])


temp_array = np.linspace(100, 500, num=n_num)
print('used Temperatures:', temp_array)

for temp in temp_array:
    radius_profile, temp_profile = give_radius_from_temp(temp)
    if temp in [100, 500]:
        ax.plot(radius_profile[:,1]/1e3, temp_profile, label=rf'$T_N={temp:.0f}$K, r_mix={radius_profile[49,2]}')
    else:
        ax.plot(radius_profile[:,1]/1e3, temp_profile)
#print('resulting Radii:', np.array(radius_array))

jupiter = give_radius_from_temp(160)

ax.scatter(jupiter[0][:,1]/1e3, jupiter[1], c='black', label=r'$T_N=160$K (Jupiter)')

ax.axvline(jupiter[0][49,2]/1e3, label=r'composition change in $T_N=160$K: pure H - mix 75% H and 25% He', zorder=-1, color='grey', linestyle='--', lw=linewidth)
ax.axvline(jupiter[0][24,2]/1e3, label=r'composition change in $T_N=160$K: H/HE mix - rocky core', zorder=-1, color='grey', lw=linewidth)

ax.set_xlabel('radius [km]', fontsize=lasize)
ax.set_ylabel('Temperature [K]', fontsize=lasize)
ax.tick_params(axis='both', labelsize=lasize)
ax.grid(True)
ax.legend(fontsize=lasize)
fig.tight_layout()
plt.show()
