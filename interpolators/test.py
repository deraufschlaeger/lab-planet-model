from joblib import load

interp_dirname = '.'

interpolator = load(f"./{interp_dirname}/rho_Tp_log_log_Hydrogen_interp.joblib")

interpolatorHe = load(f"./{interp_dirname}/rho_Tp_log_log_Helium_interp.joblib")

interpolatorENer = load(f"./{interp_dirname}/E_rhoT_raw_raw_Hydrogen.joblib")

interpolatorENerHe = load(f"./{interp_dirname}/E_rhoT_raw_raw_Helium.joblib")

#derivatives

interpolator_dE_dT_H = load(f"./{interp_dirname}/dE_dT_T_rho_raw_raw_Hydrogen.joblib")

interpolator_dE_dT_He = load(f"./{interp_dirname}/dE_dT_T_rho_raw_raw_Helium.joblib")

interpolator_dE_drho_H = load(f"./{interp_dirname}/dE_drho_T_rho_raw_raw_Hydrogen.joblib")

interpolator_dE_drho_He = load(f"./{interp_dirname}/dE_drho_T_rho_raw_raw_Helium.joblib")
