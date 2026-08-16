from scipy.optimize import minimize
import traceback
import numpy as np

target_radius = 469700.0
ceres_mass = 9.38392e20

def objective_function(params):
    # params = [rho_0, K_0, K_d]
    rho_0_curr, k_0_curr, k_d_curr = params
    
    # Physikalische Schranken um unsinnige Werte zu vermeiden
    if rho_0_curr < 1000 or k_0_curr < 1e9 or k_d_curr < 1:
        return 1e30

    try:
        results = multi_iteration(
            starting_density=2161.6,
            mass_total=ceres_mass,
            N=20, # Etwas höhere Auflösung für die Optimierung
            T=172.5,
            quiet=True,
            eos='rocky',
            k_0=k_0_curr,
            k_d=k_d_curr,
            rho_0=rho_0_curr
        )

        if isinstance(results, tuple) and len(results) == 3:
            R_p = results[0]
            if isinstance(R_p, np.ndarray) and R_p.ndim == 2:
                calc_radius = R_p[-1][2]
                # Ziel: Differenz zum realen Radius minimieren
                return (calc_radius - target_radius)**2
        return 1e30
    except Exception:
        return 1e30

# Startwerte: rho_0 ~ 2500, K_0 ~ 50 GPa, K_d ~ 4.0
initial_guess = [2500.0, 50e9, 4.0]

# Optimierung über alle 3 Parameter
result = minimize(objective_function, initial_guess, method='Nelder-Mead', tol=1e-1)

if result.success:
    opt_rho_0, opt_k_0, opt_k_d = result.x
    print("\n--- Optimale EOS-Parameter gefunden ---")
    print(f"rho_0: {opt_rho_0:.2f} kg/m^3")
    print(f"K_0:   {opt_k_0/1e9:.2f} GPa")
    print(f"K_d:   {opt_k_d:.3f}")

    # Finale Profile mit optimierten Parametern berechnen
    res_final = multi_iteration(
        2161.6, ceres_mass, 20, 172.5, quiet=True,
        eos='rocky', k_0=opt_k_0, k_d=opt_k_d, rho_0=opt_rho_0
    )

    final_rad = res_final[0][-1][2]
    print(f"\nResultierender Radius: {final_rad:.2f} m")
    print(f"Zielradius:            {target_radius:.2f} m")
    print(f"Abweichung:            {abs(final_rad - target_radius):.4f} m")
else:
    print(f"Optimierung fehlgeschlagen: {result.message}")
