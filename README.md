# Systematic_errors_in_spectral_measurements_TMS

This repository contains the source code used to generate the results presented in the paper 'Systematic Errors in Spectral Measurements with the Tenerife Microwave Spectrometer'. It includes the computational models developed for Jones matrices and Friis transmission equations to characterize the instrument's signal chain.

Contents

#Section 3.2 | Jones Matrix Implementation: Jones_and_stokes_TMS_paper_jan2026.ipynb: Notebook for the derivation and output of the Jones matrices. Install SimPy library.

#Section 4 | Model Validation (Jones Calculus vs. Friis Equations): Test_friis_VS_stokes_paper_Jan2026.ipynb: Comparison between the nominal Jones matrix values and their Friis equation equivalents. Data Dependencies: datos_betas_jonesmatrix_BEM_27nov.zip and datos_friis_BEM_betas_26nov.zip

#Section 6 | TMS System Model (Friis Framework): TMS_main_delta_eq.ipynb: Implementation of the full Friis equation model for the TMS instrument. TMS_deltaT_functions_github.py: Principal script for the complete TMS system analysis.

#General Documents folder: It contains the nominal values of the TMS components and also other functions required to operate the code.

The GitHub viewer sometimes has trouble displaying the contents of Jupyter files online. I suggest using the platform https://nbviewer.org/ to view the content

