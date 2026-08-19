# Python model of gas giants

This is the repository of the lab project in the Summer of 2026 by Birger Aufschläger and Leonie Parsiegel. Supervised by Torsten Löhne (Astrophysical Institute, FSU Jena).

# Files

- apjs504506t{2,3}_mrt.txt
  * 2: the H-REOS.3 table
  * 3: the He-REOS.3 table
  * read "Ab initio equations of state for hydrogen (H-REOS.3) and helium (He-REOS.3) and their implications for the interior of Brown Dwarfs" by Becker et. al 2014 for more context 

- make_interpolators.py
  * terminal script to create all the interpolators once from the EOS tables and save the functioninstances in the --dirname folder. 
  * We save the created functions with the [Joblib package](https://github.com/joblib/joblib).

- multiiter.py
  * location of the function "multi_iteration" which is the main access point to the model.
  * read location of interpolators can be changed here
  * location of create_eos_profile function, which creates the dic with the EOS informations per layer from the layers_def dic given in make_planet_model.py. 
  
- make_planet_model.py
  * template script to create a planet model. Should be worked on further
  
- make_*_graph.py
  * scripts used to investigate different parameters of the model

# Folders

## images

this has all the created graphs, made with the make_*_graph.py scripts

## interpolators

this has all the saved interpolators made with the make_interpolator.py script. We save the created functions with the [Joblib package](https://github.com/joblib/joblib).

## misc

tested ideas or random files but all of them are not used in the actual model.

# Usage
1. layers_def dictionary needs to be provided to the create_eos_profile function. This created eos_profile needs to be provided to the multi_iteration function
2. multi_iteration is main model function and needs:
   * initial density
   * total mass
   * total number of layers N
   * surface temerature T
   * the eos_profile dictionary created by the create_eos_profile function
   * optional: mass profile: a list of length N with a mass for each layer. If not provided a constant distribution is assumed
	 * Note: internal create_{mass, temp, density}_profile function, with controlling keywords, could be implemented, but are not in use for now
   * optional: tolerance (of central density for convergence), default: 1e-6
   * optional: max_iter(ations), default: 20
