from multiiter import multi_iteration, create_eos_profile

#jupyter:

'''rho_0 = 1249.5 kg/m^3
K_0 = 4.26 GPa
K_0' = 7.75

Perovskite
rho_0 4105.9
K_0 = 270.6
K_0' = 3.81
'''

layers_def = [
    {
        'eos_type': 'rocky',
        'params': {'k_0': 270.6e9, 'k_d': 3.81, 'rho_0': 4105.9},
        'num_layers': 2 # 50 layers for the rocky core
    },
    {
        'eos_type': 'he',
        'params': {},
        'num_layers': 10 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': ['h', 'he'],
        'params': {'X_H': 0.1, 'Y_He': 0.9},
        'num_layers': 5 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': ['h', 'he'],
        'params': {'X_H': 0.25, 'Y_He': 0.75},
        'num_layers': 5 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': ['h', 'he'],
        'params': {'X_H': 0.5, 'Y_He': 0.5},
        'num_layers': 5 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': ['h', 'he'],
        'params': {'X_H': 0.75, 'Y_He': 0.25},
        'num_layers': 5 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': ['h', 'he'],
        'params': {'X_H': 0.9, 'Y_He': 0.1},
        'num_layers': 5 # 50 layers for the hydrogen shell
    },
    {
        'eos_type': 'h',
        'params': {},
        'num_layers': 80 # 50 layers for the hydrogen shell
    }
]

eos_profile = create_eos_profile(layers_def)

N = len(eos_profile)

mass_total = 1.898e27 #kg

rho_0 = 1300 #kg/m^3

T_0 = 165

r_profile, p_profile, rho_profile, temp_profile = multi_iteration(rho_0, mass_total, N, T_0, eos_profile, quiet=False, max_iter = 40)
