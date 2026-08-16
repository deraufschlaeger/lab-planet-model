from multiiter import multi_iteration, create_eos_profile

#earth:

'''Mechanical STRUCTURE
- rigid lithosphere
- semi-fluid astenosphere
- a rigid mesosphere
- liquid outer core
- solid inner core

Chemical STRUCTURE
- silicate crust
- ferromagnesian mantle
- iron-nickle core

MATERIALS:
Silicate:

Iron: (Wagner+2011)
rho_0 = 8269.4 kg/m^3
K_0 = 164.7 GPa
K_0' = 5.650

Nickle:

ice:
rho_0 = 1249.5 kg/m^3
K_0 = 4.26 GPa
K_0' = 7.75

Perovskite: Wagner+2011 (earth's lower mantle?)
rho_0 4145
K_0 = 234 GPa
K_0' = 4.00

Iron alloy (wagner+2011; earths outer core?)
rho_0 = 7488.3 kg/m^3
K_0 = 169.82 GPa
K_0' = 4.9835

Olivine (Wagner+2011)
rho_0 = 3213.7 kg/m^3
K_0 = 127.4 GPa
K_0' = 4.2
'''

n_layer = 30

layers_def = [
    { #core: iron
        'eos_type': 'rocky',
        'params': {'k_0': 164.7e9, 'k_d': 5.650, 'rho_0': 8269.4},
        'num_layers': n_layer
    },
    { # outer core: iron alloy
        'eos_type': 'rocky',
        'params': {'k_0': 169.82e9, 'k_d': 4.9835, 'rho_0': 7488.3},
        'num_layers': n_layer
    },
    { #lower mantle: perovskite
        'eos_type': 'rocky',
        'params': {'k_0': 234e9, 'k_d': 4.00, 'rho_0': 4145},
        'num_layers': n_layer
    },
    { #upper mantle: olivine
        'eos_type': 'rocky',
        'params': {'k_0': 127.7e9, 'k_d': 4.2, 'rho_0': 3213.7},
        'num_layers': n_layer
    }
]

eos_profile = create_eos_profile(layers_def)

N = len(eos_profile)

mass_total = 5.9722e24 #kg

rho_0 = 5515 #kg/m^3

T_0 = 300

r_profile, p_profiile, rho_profile, tmp_profile = multi_iteration(rho_0, mass_total, N, T_0, eos_profile, quiet=False, max_iter = 40)
