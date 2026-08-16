#!/usr/bin/env python3

from multiiter import multi_iteration

import argparse

parser = argparse.ArgumentParser(
                    prog='make_planet_model.py',
                    usage='make_planet_model.py -m [MASS]',
                    description="This script creates a model of a planet.")

# SHELL ARGUMENTS

parser.add_argument('-m', '--mass', type=float, default=1.898e27, help="Total mass of the model planet in kilograms. Default: 1898e27 (Jupitermass).")

parser.add_argument('-mi', '--max_iter', type=int, default=40, help="Maximum number of iterations. Default: 40.")

parser.add_argument('-d', '--density', type=float, default=1300, help="Starting density for the model in kilograms per cubicmeters. Default: 1300 (Mean Jupiter density).")

parser.add_argument('-t', '--temperature', type=float, default=300, help="Surface temperature of the model planet in Kelvin. Default: 300.")

parser.add_argument('-q', '--quiet', action='store_true', help="if given the function will work quietly and not print stuff out")

#parser.add_argument

#---------------------------

args = parser.parse_args()

layers_def = [
    {
        'eos_type': 'rocky',
        'params': {'k_0': 270.6e9, 'k_d': 3.81, 'rho_0': 4105.9},
        'num_layers': 2
    },
    {
        'eos_type': 'he',
        'params': {},
        'num_layers': 10
    },
    {
        'eos_type': 'h',
        'params': {},
        'num_layers': 90
    }
]

eos_profile = create_eos_profile(layers_def)

N = len(eos_profile)

mass_total = args.mass #kg

rho_0 = args.density #kg/m^3

T_0 = args.temperature #K

r_profile, p_profiile, rho_profile, tmp_profile = multi_iteration(
    rho_0,
    mass_total,
    N,
    T_0,
    eos_profile,
    quiet=args.quiet,
    max_iter=args.max_iter,
    
)
