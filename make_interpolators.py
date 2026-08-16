#!/usr/bin/env python3

import numpy as np
import pandas as pd
import scipy.interpolate
import argparse

parser = argparse.ArgumentParser(
                    prog='Make_interpolators',
                    usage='make_interpolators.py [-s [stepsize] -d [dirname]',
                    description="It creates the interpolators needed for the EOS and adiabatic temperature profile from hardcoded tabulated EOS datafiles. For Hydrogen it is 'apjs504506t2_mrt.txt' and for Helium it is 'apjs504506t3_mrt.txt'. The script saves them as .joblib files to the directory classified in the option --dirname.")

parser.add_argument('-s', '--step', type=float, default=1e-4, help='stepsize for the numerical drivates. Default: 1e-4')

parser.add_argument('-d', '--dirname', type=str, default='interpolators', help="name for the directory, where the .joblib files will be saved. Default: 'interpolators'")

args = parser.parse_args()

#----------------READING-DATA-----------------------------------------------------
## Hydrogen data====================================
data_h_raw = pd.read_csv(
    "apjs504506t2_mrt.txt",
    sep=r"\s+",
    skiprows=15,
    usecols=[0, 1, 2, 3],
    names=["rho_H_raw", "T_H_raw", "p_H_raw", "E_H_raw"]
)

# Apply log transformation to all columns
data_h_log = pd.DataFrame({
    "rho_H": np.log(data_h_raw["rho_H_raw"] * 1000), #[kg/m^3]
    "T_H": np.log(data_h_raw["T_H_raw"]),
    "p_H": np.log(data_h_raw["p_H_raw"] * 1e9), #[Pa]
    "E_H": np.log(data_h_raw["E_H_raw"] * 1e6)
}) #this will produce a RuntimeWarning because there are negative values in E_H

E_H_raw = data_h_raw["E_H_raw"] * 1e6
p_H_raw = data_h_raw["p_H_raw"] * 1e9
T_H_raw = data_h_raw["T_H_raw"]
rho_H_raw = data_h_raw["rho_H_raw"] * 1000


rho_H = data_h_log["rho_H"].to_numpy()
T_H = data_h_log["T_H"].to_numpy()
p_H = data_h_log["p_H"].to_numpy()
E_H = data_h_log["E_H"].to_numpy()

Tp_H = np.column_stack((T_H, p_H))
rhoT = np.column_stack((T_H, rho_H))
rhoT_raw = np.column_stack((T_H_raw, rho_H_raw))
Tp_H_raw = np.column_stack((T_H_raw, p_H_raw))
#==============================================

## Helium data=================================
data_he_raw = pd.read_csv(
    "apjs504506t3_mrt.txt",
    sep=r"\s+",
    skiprows=15,
    usecols=[0, 1, 2, 3],
    names=["rho_He_raw", "T_He_raw", "p_He_raw", "E_He_raw"]
)

# Apply log transformation to all columns
data_he_log = pd.DataFrame({
    "rho_He": np.log(data_he_raw["rho_He_raw"] * 1000),
    "T_He": np.log(data_he_raw["T_He_raw"]),
    "p_He": np.log(data_he_raw["p_He_raw"] * 1e9),
    "E_He": np.log(data_he_raw["E_He_raw"] * 1e6)
}) #this will produce a RuntimeWarning because there are negative values in E_H

E_He_raw = data_he_raw["E_He_raw"] * 1e6
p_He_raw = data_he_raw["p_He_raw"] * 1e9
T_He_raw = data_he_raw["T_He_raw"]
rho_He_raw = data_he_raw["rho_He_raw"] * 1000


rho_He = data_he_log["rho_He"].to_numpy()
T_He = data_he_log["T_He"].to_numpy()
p_He = data_he_log["p_He"].to_numpy()
E_He = data_he_log["E_He"].to_numpy()

Tp_He = np.column_stack((T_He, p_He))
rhoT_He = np.column_stack((T_He, rho_He))
Tp_He_raw = np.column_stack((T_He_raw, p_He_raw))
rhoT_He_raw = np.column_stack((T_He_raw, rho_He_raw))
#=============================================
#------------------------------------------------------------------------------------

#----------------------MAKE-INTERPOLATORS--------------------------------------------

interpolator = scipy.interpolate.LinearNDInterpolator(Tp_H, rho_H) # Hydrogen
interpolatorHe = scipy.interpolate.LinearNDInterpolator(Tp_He, rho_He) #He

interpolatorENer = scipy.interpolate.LinearNDInterpolator(rhoT_raw, E_H_raw)
interpolatorENerHe = scipy.interpolate.LinearNDInterpolator(rhoT_He_raw, E_He_raw)

#----------------------MAKE-DERIVATIVES-------------------------------------
h = args.step

dE_dT_H = (
    interpolatorENer(T_H_raw + h, rho_H_raw)
    - interpolatorENer(T_H_raw, rho_H_raw)
) / (h)

dE_drho_H = (
    interpolatorENer(T_H_raw, rho_H_raw + h)
    - interpolatorENer(T_H_raw, rho_H_raw)
) / (h)

interpolator_dE_dT_H = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_H_raw, rho_H_raw)),
    dE_dT_H
)

interpolator_dE_drho_H = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_H_raw, rho_H_raw)),
    dE_drho_H
)


dE_dT_He = (
    interpolatorENerHe(T_He_raw + h, rho_He_raw)
    - interpolatorENerHe(T_He_raw, rho_He_raw)
) / (h)

dE_drho_He = (
    interpolatorENerHe(T_He_raw, rho_He_raw + h)
    - interpolatorENerHe(T_He_raw, rho_He_raw)
) / (h)

interpolator_dE_dT_He = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_He_raw, rho_He_raw)),
    dE_dT_He
)

interpolator_dE_drho_He = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_He_raw, rho_He_raw)),
    dE_drho_He
)

dE_dT_H = (
    interpolatorENer(T_H_raw + h, rho_H_raw)
    - interpolatorENer(T_H_raw, rho_H_raw)
) / (h)

dE_drho_H = (
    interpolatorENer(T_H_raw, rho_H_raw + h)
    - interpolatorENer(T_H_raw, rho_H_raw)
) / (h)

interpolator_dE_dT_H = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_H_raw, rho_H_raw)),
    dE_dT_H
)

interpolator_dE_drho_H = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_H_raw, rho_H_raw)),
    dE_drho_H
)

dE_dT_He = (
    interpolatorENerHe(T_He_raw + h, rho_He_raw)
    - interpolatorENerHe(T_He_raw, rho_He_raw)
) / (h)

dE_drho_He = (
    interpolatorENerHe(T_He_raw, rho_He_raw + h)
    - interpolatorENerHe(T_He_raw, rho_He_raw)
) / (h)

interpolator_dE_dT_He = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_He_raw, rho_He_raw)),
    dE_dT_He
)

interpolator_dE_drho_He = scipy.interpolate.LinearNDInterpolator(
    np.column_stack((T_He_raw, rho_He_raw)),
    dE_drho_He
)

#---------------------SAVE-INTERPOLATORS-------------------------------------------

from joblib import dump

from pathlib import Path

Path(f"./{args.dirname}/").mkdir(parents=True, exist_ok=True)

dump(interpolator, f"./{args.dirname}/rho_Tp_log_log_Hydrogen_interp.joblib")

dump(interpolatorHe, f"./{args.dirname}/rho_Tp_log_log_Helium_interp.joblib")

dump(interpolatorENer, f"./{args.dirname}/E_rhoT_raw_raw_Hydrogen.joblib")

dump(interpolatorENerHe, f"./{args.dirname}/E_rhoT_raw_raw_Helium.joblib")

#derivatives

dump(interpolator_dE_dT_H,  f"./{args.dirname}/dE_dT_T_rho_raw_raw_Hydrogen.joblib")

dump(interpolator_dE_dT_He, f"./{args.dirname}/dE_dT_T_rho_raw_raw_Helium.joblib")

dump(interpolator_dE_drho_H, f"./{args.dirname}/dE_drho_T_rho_raw_raw_Hydrogen.joblib")

dump(interpolator_dE_drho_He, f"./{args.dirname}/dE_drho_T_rho_raw_raw_Helium.joblib")
