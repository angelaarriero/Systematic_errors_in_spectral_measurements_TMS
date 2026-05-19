import sys
import os

import numpy as np

from numpy.fft import fft

sys.path.append("general_documents/definitions_files")


from convert_csv_files_inputsignals_tosimulate import datos_componente
from convert_csv_files_inputsignals_tosimulate import datos_componente2
from convert_csv_files_inputsignals_tosimulate import datos_componente3

from convert_csv_files_inputsignals_tosimulate import sparams_to_power
from convert_csv_files_inputsignals_tosimulate import datos_simulados_RI
from convert_csv_files_inputsignals_tosimulate import conversion_dc
from convert_csv_files_inputsignals_tosimulate import desplazar_en_frecuencia
from convert_csv_files_inputsignals_tosimulate import min_max
from convert_csv_files_inputsignals_tosimulate import min_max2
from convert_csv_files_inputsignals_tosimulate import min_max3


import toml
# Carpeta donde está tu archivo TOML
ruta_toml = os.path.join("general_documents/data_files")
# Nombre del archivo TOML
toml_name = "input_params_simulation_V1_def"
toml_file = os.path.join(ruta_toml, toml_name + ".toml")
print("Ruta completa del archivo:", toml_file)
# Cargar el archivo TOML
data = toml.load(toml_file)
print("Archivo cargado correctamente")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec

from convert_csv_files_inputsignals_tosimulate import rectas_ANSYS_outputs

def direct_fft(f,f_s):
    return  np.fft.fft(f) / f_s

def inverse_fft(f,f_s):
    return np.real(np.fft.ifft(f)) * f_s

def powerspectrum(f, f_s):
    Fourier = direct_fft(f,f_s)
    return np.real(Fourier  * np.conjugate(Fourier) ) 
    
def freq_values(nsamp,t_sampling):
    F = np.fft.fftfreq(nsamp, d = t_sampling)
    return F

def C_Delta_T(array1_tiempo, array4_Tsky, step, ideal, scatter):
    n=1000

    # ── 1. Carga de archivos ──────────────────────────────────────────────────
    ruta_files_n = os.path.join("general_documents/data_files")

    files = {
        "ansys":        "V1_Datos_ANSYS_TMS_coldload_STEPS_DEC25_V1.csv",
        "rl_hyb":       "rl_hyb.csv",
        "IL_hyb":       "IL_hyb.csv",
        "IL_omt":       "IL_omt.csv",
        "OMT_measure":  "OMT_measure_R.csv",
        "RL_feedhorn":  "RL_feedhorn.csv",
        "RL_window":    "RL_window.csv",
        "LNA_20C":      "LNA_20C.csv",
        "CR117":        "CR117_load_RL.csv",
        "TN_20_C":      "TN_20_C.csv",
        "noise_lna":    "noise_lna_amp_roomT.csv",
        "gain_lna":     "gain_lna_amp_roomT.csv",
        "GAIN_DC":      "GAIN_DC.csv",
        "Noise_DC":     "Noise_figu_DC.csv",
        "IR_filter":    "TMS_IR_filter_10_layers_IL_10-20GHz.csv",
    }
    fp = {k: os.path.join(ruta_files_n, v) for k, v in files.items()}

    _, y_ajustada_append = rectas_ANSYS_outputs(fp["ansys"], 51)

    Q, W, E, R, Z, X, C, V, xx1, *_, N, M, _, U, Qs, Ws, Es, Rs, \
        noise_lna_amp_roomT, N1, N2, N3, N4, Un1, Un2, Un3, Un4, sfN1 = \
        datos_simulados_RI(n, fp["rl_hyb"], fp["IL_hyb"], fp["IL_omt"],
                           fp["OMT_measure"], fp["RL_feedhorn"], fp["RL_window"],
                           fp["LNA_20C"], fp["CR117"], fp["TN_20_C"], fp["noise_lna"])

    # ── 2. Parámetros ópticos por caso ───────────────────────────────────────
    ones = np.ones(n)   # alias reutilizable

    def _from_data(key, subkey, scale=1.0):
        return ones * data[key][subkey] * scale

    def _db(key, subkey):
        return ones * pow(10, data[key][subkey] / 10)

    if ideal == 1:
        # Caso ideal: todo cero salvo excepciones
        Tw = Tirf = Txps = Tfhs = Tomts = ThX = np.zeros(n)
        Tl = Tfhl = Tomtl = ThY = Tenv2_LNA = Tenv1 = Troom = np.zeros(n)
        T_ext_cry = T_BEM_filter = T_after_filt_BEM = T_after_ampl_DC = np.zeros(n)
        Tcryo1 = Tcryo2 = np.zeros(n)
        Tenv2  = ones * 1e-20
        T_FPGA = ones
        t_load_r = ones * 8
        SPOw = SPOirf = SPO = np.zeros(n)
        RLirf = RLlna1s = RLlna2s = RLlna3l = RLlna4l = ones
        print('This is the ideal case: if input 8, then output 0')

    elif step == 100 and scatter == 0:
        
        t_load_r = ones * 8
        Tw    = ones * data["Window"]["Temperature"]
        Tirf  = ones * data["IRfilter"]["Temperature"]
        Txps  = np.zeros(n)
        Tfhs  = ones * data["FeedHornSky"]["Temperature"]
        Tomts = ones * data["OMTsky"]["Temperature"]
        ThX   = ones * data["HybridX"]["Temperature"]
        Tl    = ones * data["4KCL"]["Temperature"]
        Tfhl  = ones * data["FeedHornload"]["Temperature"]
        Tomtl = ones * data["OMTload"]["Temperature"]
        ThY   = ones * data["HybridY"]["Temperature"]
        Tenv2_LNA = ones * data["Environment"]["Tenv2"]
        Tenv1 = ones * data["Environment"]["Tenv1"]
        Tenv2 = ones * data["Environment"]["Tenv2"]
        Troom = ones * data["Environment"]["Troom"]
        T_ext_cry       = ones * data["Environment"]["T_ext_cry"]
        T_BEM_filter    = ones * data["Environment"]["T_BEM_filter"]
        T_after_filt_BEM= ones * data["Environment"]["T_after_filt_BEM"]
        T_after_ampl_DC = ones * data["Environment"]["T_after_ampl_DC"]
        T_FPGA          = ones * data["Environment"]["T_FPGA"]
        Tcryo1 = ones * data["Environment"]["Tcryo1"]
        Tcryo2 = ones * data["Environment"]["Tcryo2"]
        SPOw   = _db("SPO", "Window");  SPOirf = _db("SPO", "IRfilter")
        SPO    = pow(10, ones * data["SPO"]["4KCL"])
        RLirf  = _db("IRfilter", "RL"); RLlna1s = _db("LNA1", "RL")
        RLlna2s= _db("LNA2", "RL");    RLlna3l  = _db("LNA3", "RL")
        RLlna4l= _db("LNA4", "RL")
        print('This is the case for the results in the paper: if input 8, Delta T = 6.91 K')

    # ── 3. Componentes ópticas (IR filter, OMT, feedhorn, etc.) ──────────────
    _, y_fit_IRfilter_il = datos_componente3(fp["IR_filter"], n,  0.00)
    _, y_fit_window_il   = datos_componente3(fp["IR_filter"], n, -0.05)
    _, y_fit_Q_il        = datos_componente3(fp["IR_filter"], n, -0.10)
    _, y_fit_OMT_il      = datos_componente3(fp["IR_filter"], n, -0.35)

    Q = y_fit_Q_il;   R = y_fit_window_il
    E = y_fit_IRfilter_il           # IL IR filter
    Wl = Ws = Q                     # IL feedhorn
    Vl = Vs = V                     # RL feedhorn
    Xl = Xs = X                     # RL OMT
    Ql = Qs = y_fit_OMT_il          # IL OMT
    C1 = C2 = C                     # RL hybrid
    Q1 = Q2 = Q                     # IL hybrid
    G1 = G2 = G3 = G4 = N          # LNA gain
    U1 = U2 = U3 = U4 = U          # LNA noise temp

    # ── 4. BEM ────────────────────────────────────────────────────────────────
    RlnaBEM  = _db("BEM_amp",    "RL")
    GainBEM  = _db("BEM_amp",    "Gain")
    TnBem    = ones * ((pow(10, data["BEM_amp"]["Fnoise"] / 10) - 1) * 300)
    RfilBem  = _db("BEM_filter", "RL")
    IfilBem  = _db("BEM_filter", "IL")
    TnBem_var = (noise_lna_amp_roomT - np.mean(noise_lna_amp_roomT)) * \
                (np.mean(TnBem) / np.mean(noise_lna_amp_roomT)) + np.mean(TnBem)

    _, _, _, _, _, gain_lna_amp_roomT = datos_componente(fp["gain_lna"], n)
    GainBEM = sparams_to_power(gain_lna_amp_roomT, n)
    TnBem_var1 = TnBem_var2 = TnBem_var3 = TnBem_var4 = TnBem_var

    # ── 5. Down-Converter ─────────────────────────────────────────────────────
    RlnaDC = _db("DC_amp",    "RL")
    TnDC   = ones * ((pow(10, data["DC_amp"]["Fnoise"] / 10) - 1) * 300)
    GainDC = _db("DC_amp",    "Gain")
    TfilDC = ones * 300
    IfilDC = _db("DC_filter", "IL")
    RfilDC = _db("DC_filter", "RL")
    Tmixer_A1 = Tmixer_A2 = Tmixer_B1 = Tmixer_B2 = 1000

    _, _, _, _, _, gain_amp_DC = datos_componente2(fp["GAIN_DC"], n)
    GainDC = sparams_to_power(gain_amp_DC, n)
    TnDC   = conversion_dc(fp["Noise_DC"], n)

    # ── 6. Eficiencias (h) ────────────────────────────────────────────────────
    if ideal == 1:
        hw = hirf = hXPS = hfhs = homts = hfhl = homtl = ones
        hhyb1 = hhyb2 = hlna1 = hlna2 = hlna3 = hlna4 = ones
        hload = hlnaBEM = hfilterBEM = hlnaDC = hfilDC = ones
    else:
        hw      = (ones - Z) * (ones - R) * (ones - SPOw)
        hirf    = (ones - RLirf) * (ones - E) * (ones - SPOirf)
        hXPS    = ones if step == 100 else hirf.copy()
        hfhs    = (ones - Vs) * (ones - Ws)
        homts   = (ones - Xs) * (ones - Qs)
        hfhl    = (ones - Vl) * (ones - Wl)
        homtl   = (ones - Xl) * (ones - Ql)
        hhyb1   = (ones - C1) * (ones - Q1)
        hhyb2   = (ones - C2) * (ones - Q2)
        hlna1   = 1 - RLlna1s;  hlna2 = 1 - RLlna2s
        hlna3   = 1 - RLlna3l;  hlna4 = 1 - RLlna4l
        hload   = (ones - M) * (1 - SPO)
        hlnaBEM = ones - RlnaBEM
        hfilterBEM = (ones - RfilBem) * (ones - IfilBem)
        hlnaDC  = ones - RlnaDC
        hfilDC  = (ones - RfilDC) * (ones - IfilDC)

    Aphi1 = hhyb1 * hlna1 / 2
    Aphi2 = hhyb1 * hlna2 / 2
    Aphi3 = hhyb2 * hlna3 / 2
    Aphi4 = hhyb2 * hlna4 / 2


    # ── 7. Betas y ganancias ──────────────────────────────────────────────────
    a2   = hw * hirf * hXPS * hfhs * homts * 0.5          # beta SKY
    a3   = hfhl * homtl * 0.5 * (ones if ideal == 1 else (ones - M) * (1 - SPO))  # beta LOAD
    a8   = hirf * hXPS * hfhs * homts * 0.5 * SPOw
    a8_1 = hirf * hfhs * homts * 0.5 * SPOirf
    a9   = hfhs * homts * 0.5 * SPOirf
    a10  = hfhl * homtl * 0.5 * SPO


    theta_bem_dc= hlnaDC * hfilDC*hlnaBEM * hfilterBEM
    

    HDC      = hlnaDC * hfilDC * GainDC
    loss_Hs  = hlnaBEM * hfilterBEM * GainBEM * HDC   # igual para G1=G2=G3=G4=N
    loss1_Hs = loss2_Hs = loss3_Hs = loss4_Hs = loss_Hs * G1
    

    # ── 8. Sumatorias de pérdidas ──────────────────────────────────────────────
    hyb_effect1 = ThX * (1 if ideal == 1 else Q1) + Tenv2 * (1 if ideal == 1 else C1)
    hyb_effect2 = ThY * (1 if ideal == 1 else Q2) + Tenv2 * (1 if ideal == 1 else C2)
    
   

    if step == 100 or ideal == 1:
        sum_tem_IL_sky = (Tw*R*hirf*hfhs*homts*0.5*(1 if ideal==1 else (1-SPOw)) +
                          Tirf*E*hfhs*homts*0.5*(1 if ideal==1 else (1-SPOirf)) +
                          Tfhs*Ws*homts*0.5 + Tomts*Qs)
        A_Tw_IL=R*hirf*hfhs*homts*0.5*(1-SPOw)
        
        
        A_Tirf_IL=E*hfhs*homts*0.5*(1-SPOirf)
        A_Tfhs_IL=Ws*homts*0.5
        A_Tomts_IL=Qs
        
        sum_R_sky = (Z*hirf*hfhs*homts*0.5*(Tenv1/Tenv2)*(1 if ideal==1 else (1-SPOw)) +
                     RLirf*hfhs*homts*0.5*(1 if ideal==1 else (1-SPOirf)) +
                     Vs*homts*0.5 + Xs)
        A_Tw_RL=Z*hirf*hfhs*homts*0.5*(1-SPOw)*Tenv1
        

        A_Tirf_RL=RLirf*hfhs*homts*0.5*(1-SPOirf)
        A_Tfhs_RL=Vs*homts*0.5
        A_Tomts_RL=Xs


        cryo_s = T_ext_cry*a8 + Tcryo1*a9
        cryo_l = Tcryo2*a10
    else:
        sum_tem_IL_sky = (Tw*R*hirf*hXPS*hfhs*homts*0.5*(1-SPOw) +
                          Tirf*E*hXPS*hfhs*homts*0.5*(1-SPOirf) +
                          Txps*E*hfhs*homts*0.5*(1-SPOirf) +
                          Tfhs*Ws*homts*0.5 + Tomts*Qs)
        sum_R_sky = (Z*hirf*hXPS*hfhs*homts*0.5*(Tenv1/Tenv2)*(1-SPOw) +
                     RLirf*hXPS*hfhs*homts*0.5*(1-SPOirf) +
                     RLirf*hfhs*homts*0.5*(1-SPOirf) +
                     Vs*homts*0.5 + Xs)
        cryo_s = T_ext_cry*a8 + Tcryo1*a9 + Tcryo2*a8_1
        cryo_l = Tcryo2*a10

    
    sum_tem_IL_load = Tfhl*Wl*homtl*0.5 + Tomtl*Ql
    A_Tfhl_IL=Wl*homtl*0.5
    A_Tomtl_IL=Ql

    sum_R_load      = M*(1-SPO)*hfhl*homtl*0.5 + Vl*homtl*0.5 + Xl
    A_Tloadl_RL=M*(1-SPO)*hfhl*homtl*0.5
    A_Tfhl_RL= Vl*homtl*0.5
    A_Tomtl_RL= Xl

    offs = (sum_tem_IL_sky + sum_tem_IL_load) + Tenv2*(sum_R_sky + sum_R_load) + cryo_s + cryo_l
    offl = (sum_tem_IL_sky - sum_tem_IL_load) + Tenv2*(sum_R_sky - sum_R_load) + cryo_s - cryo_l

    

    Tenv_lna = Tenv2 if (step == 100 or ideal == 1) else Tenv2_LNA
    A1_off = Aphi1*offs + hyb_effect1*hlna1 + Tenv_lna*RLlna1s
    A2_off = Aphi2*offl + hyb_effect1*hlna2 + Tenv_lna*RLlna2s
    

    B1_off = Aphi3*offs + hyb_effect2*hlna3 + Tenv_lna*RLlna3l
    B2_off = Aphi4*offl + hyb_effect2*hlna4 + Tenv_lna*RLlna4l
  
   

    ##############################################################################################
    # ── 9. BEM + DC offsets y ruidos ─────────────────────────────────────────
    Tloss2_1 = ((T_BEM_filter*RlnaBEM*hfilterBEM*GainBEM) +
                T_BEM_filter*IfilBem + T_after_filt_BEM*RfilBem) * HDC
    
    A_T_tloss2= ((RlnaBEM*hfilterBEM) + IfilBem + RfilBem) * hlnaDC * hfilDC 
    
    Tloss3_1 = ((1-RlnaDC)*hfilDC*GainDC*Tmixer_A1 +T_after_ampl_DC*RlnaDC*hfilDC*GainDC +
                TfilDC*IfilDC + T_FPGA*RfilDC)
    
    A_T_tloss3= ((1-RlnaDC)*hfilDC +RlnaDC*hfilDC +IfilDC + RfilDC)

    
    
    common = hlnaBEM * hfilterBEM * hfilDC * hlnaDC * GainDC * GainBEM
    Tn1 = U1 * common * G1;  Tn2 = U2 * common * G2
    Tn3 = U3 * common * G3;  Tn4 = U4 * common * G4
    Tn2bem_1 = TnBem_var * hfilterBEM * hfilDC * hlnaDC * GainDC * GainBEM  # ×2 abajo
    Tn3DC_1  = TnDC * hfilDC * GainDC                                         # ×2 abajo

    if ideal == 1:
        Tloss2_1 = Tloss3_1 = 0
        Tn1 = Tn2 = Tn3 = Tn4 = Tn2bem_1 = Tn3DC_1 = 0

    Tn1FEM_1 = Tn1 + Tn2;   TnBEM_1 = 2 * Tn2bem_1;   TnDC_1 = 2 * Tn3DC_1
    Tn1FEM_3 = Tn3 + Tn4;   TnBEM_3 = TnBEM_1;          TnDC_3 = TnDC_1

    Gtot = hfilterBEM * hfilDC * GainDC * GainBEM * G1
    T_sky_bet_total  = (2*loss_Hs*G1*a2*hlna2*hhyb1*2) / (2*Gtot)  # ≡ original beta_sky2+beta_sky4
    T_load_bet_total = (2*loss_Hs*G1*a3*hlna2*hhyb1*2) / (2*Gtot)

    # ── 10. Bucle temporal (vectorizado por subbanda) ─────────────────────────
    t_sky_arr = np.asarray(array4_Tsky)         # (n_times, n_freq)
    t_load_r  = np.asarray(t_load_r)            # (n,)

    # Precomputar términos independientes del tiempo
    _A2a2 = Aphi1 * a2;  _A2a3 = Aphi1 * a3
    _A3a2 = Aphi2 * a2;  _A3a3 = Aphi2 * a3
    _A4a2 = Aphi3 * a2;  _A4a3 = Aphi3 * a3
    _A5a2 = Aphi4 * a2;  _A5a3 = Aphi4 * a3

    ##############################################################

    print('###########################################################################')
    

    A_THx_cons=(Q1*hlna1 +  C1*hlna1 + RLlna1s)*theta_bem_dc
    A_THy_cons=(Q2*hlna3 +  C2*hlna3 + RLlna3l)*theta_bem_dc

    A_T_HX_IL=Q1
    A_T_HX_RL=C1
    A_T_HY_IL=Q2
    A_T_HY_RL=C2
    A_T_LNA_RL=RLlna1s


    A_T_W=((A_Tw_IL*Aphi1+A_Tw_RL*Aphi1+a8*Aphi1))
    A_T_IRF=((A_Tirf_IL*Aphi1+A_Tirf_RL*Aphi1+a9*Aphi1))
    A_T_FHS=((A_Tfhs_IL*Aphi1+A_Tfhs_RL*Aphi1))
    A_T_OMTS=((A_Tomts_IL*Aphi1+A_Tomts_RL*Aphi1))
    
    A_T_hX=(Aphi1)
    
    A_T_Load=((A_Tloadl_RL*Aphi1+a10*Aphi1))
    A_T_FHL=((A_Tfhl_IL*Aphi1+A_Tfhl_RL*Aphi1))
    A_T_OMTL=((A_Tomtl_IL*Aphi1+A_Tomtl_RL*Aphi1))
    
    A_T_hY=(Aphi2)
    
    A_T_BEM=A_T_tloss2
    A_T_DC=A_T_tloss3
    
    
    results = []
    for t_sky_r in t_sky_arr:
        e1 = _A2a2*t_sky_r + _A2a3*t_load_r + A1_off
        e2 = _A3a2*t_sky_r - _A3a3*t_load_r + A2_off
        e3 = _A4a2*t_sky_r + _A4a3*t_load_r + B1_off
        e4 = _A5a2*t_sky_r - _A5a3*t_load_r + B2_off

        # FEM only (sin BEM/DC)
        C1r_c = G1*e1 + G2*e2;  C2r_c = G1*e1 - G2*e2
        D1r_c = G3*e3 + G4*e4;  D2r_c = G3*e3 - G4*e4
        sky_fem  = (C1r_c + D1r_c + U1*G1 + U2*G2) / G1
        load_fem = (C2r_c + D2r_c + U3*G3 + U4*G4) / G3

        # FEM + BEM + DC
        s1 = loss1_Hs*e1 + Tloss2_1 + Tloss3_1
        s2 = loss2_Hs*e2 + Tloss2_1 + Tloss3_1
        s3 = loss3_Hs*e3 + Tloss2_1 + Tloss3_1
        s4 = loss4_Hs*e4 + Tloss2_1 + Tloss3_1

        s1n = loss1_Hs*A1_off + Tloss2_1 + Tloss3_1
        s2n = loss1_Hs*A2_off + Tloss2_1 + Tloss3_1
        s3n = loss1_Hs*B1_off + Tloss2_1 + Tloss3_1
        s4n = loss1_Hs*B2_off + Tloss2_1 + Tloss3_1

        sky_n  = (s1n+s2n+s3n+s4n) / Gtot
        load_n = (s1n-s2n+s3n-s4n) / Gtot
        

        C1r = s1+s2;  C2r = s1-s2
        D1r = s3+s4;  D2r = s3-s4

        sky_full  = (C1r+D1r+Tn1FEM_1+TnBEM_1+TnDC_1) / Gtot
        load_full = (C2r+D2r+Tn1FEM_3+TnBEM_3+TnDC_3) / Gtot

        results.append((
            sky_full - load_full,   # total_BEM
            sky_full,               # I1
            load_full,              # I2
            sky_fem,                # I1_FEM
            load_fem,               # I2_FEM
            sky_fem - load_fem,     # FEM delta
            sky_n - load_n,         # Tlss_resta
        ))

    (total_BEM_atmos_cmb, total_I1_BEM_atmos_cmb, total_I2_BEM_atmos_cmb,
     _, _, total_FEM_atmos_cmb, Tlss_resta) = map(list, zip(*results))

    freq_spec = [xx1] * len(array1_tiempo)

    ############################## prueba borrar
    
    Lna_tn_test=Tn1FEM_1 / Gtot
    Lna_tn_test_load=Tn1FEM_3 / Gtot
    C1_TEST=(C1r/Gtot)
    D1_TEST=(D1r/Gtot)
    TN1FEM_TEST=(Tn1FEM_1/Gtot)
    TNBEM_TEST=(TnBEM_1/Gtot)
    TNDC_TEST=(TnDC_1/Gtot)
    C2_TEST=(C2r/Gtot)
    D2_TEST=(D2r/Gtot)
    TLOSS_SKY=sky_n
    TLOSS_LOAD=load_n
    LNA_SKY=Lna_tn_test
    LNA_LOAD=Lna_tn_test_load
    TLOSS_FEMA1= (loss1_Hs*e1)/ Gtot
    TLOSS_FEMA2= (loss2_Hs*e2)/ Gtot
    TLOSS_FEMB1= (loss3_Hs*e3)/ Gtot
    TLOSS_FEMB2= (loss4_Hs*e4)/ Gtot
    TLOSS_BEM= Tloss2_1/ Gtot
    TLOSS_DC= Tloss3_1/ Gtot

    

    #"""""
    print('######################################################################################')
    print('Table_C1:WINDOW',np.mean((Tw*R)*(ones - SPOw)+(T_ext_cry*SPOw))) ### R is the Insertion loss of the window
    print('Table_C1:IRF',np.mean((((Tirf*E)*(ones - SPOirf))+(Tcryo1*SPOirf))/hw)) ### E is the Insertion loss of the FILTER
    print('Table_C1:FHsky',np.mean((Tfhs*Ws)/(hw*hirf))) ### Ws is the Insertion loss of the FEEDHORN
    print('Table_C1:OMTsky',np.mean((Tomts*Qs/(hw*hirf*hfhs)))) ### Qs is the Insertion loss of the OMT SKY
    print('Table_C1:HYbsky',np.mean((ThX*Q1)/(hw*hirf*hfhs*homts))) ### Q1 is the Insertion loss of the HYB X SKY
    print('######################################################################################')
    print('Table_C1:FHload',np.mean((Tfhl*Wl)/(hload))) ### Wl is the Insertion loss of the FEEDHORN LOAF
    print('Table_C1:OMTload',np.mean((Tomtl*Ql/(hload*hfhl)))) ### Ql is the Insertion loss of the OMT LOAF
    print('Table_C1:HYbload',np.mean((ThY*Q2)/(hload*hfhl*homtl))) ### Q2 is the Insertion loss of the HYB Y LOAD
    #"""""


    return (total_BEM_atmos_cmb, total_I1_BEM_atmos_cmb, total_I2_BEM_atmos_cmb,
            freq_spec, Tlss_resta,T_sky_bet_total, T_load_bet_total
)

def Weights_subBands(array1_tiempo, freq_spec, total_BEM_atmos_cmb,
                     total_I1_BEM_atmos_cmb, total_I2_BEM_atmos_cmb,
                     T_sky_bet_total, T_load_bet_total,
                     Tlss_resta):
    """
    Calcula el promedio por subbandas de 240 MHz sobre arrays espectrales 2D.
    """
    new_freq      = freq_spec[0] * 1e9                                  # (n_freq,)
    n_times       = len(array1_tiempo)
    size_arr_freq = int((new_freq[-1] - new_freq[0]) / 250e6)

    # --- Límites de subbanda vectorizados (calculados una sola vez) ---
    j             = np.arange(size_arr_freq)
    band_starts   = new_freq[0] + (240e6 + 1e7) * j                    # (size_arr_freq,)
    band_ends     = band_starts + 240e6                                 # (size_arr_freq,)

    # --- Índices de cada subbanda (una sola vez) ---
    index_band_pass = [
        np.where((new_freq >= band_starts[k]) & (new_freq <= band_ends[k]))[0]
        for k in range(size_arr_freq)
    ]

    # --- Convertir inputs 2D a arrays NumPy una sola vez ---
    BEM   = np.asarray(total_BEM_atmos_cmb)          # (n_times, n_freq)
    I1    = np.asarray(total_I1_BEM_atmos_cmb)       # (n_times, n_freq)
    I2    = np.asarray(total_I2_BEM_atmos_cmb)       # (n_times, n_freq)
    TLSS  = np.asarray(Tlss_resta)                   # (n_times, n_freq)

    

    # --- Promedios 2D (n_times × size_arr_freq) con comprensión vectorizada ---
    def _band_means_2d(arr):
        return np.stack(
            [arr[:, idx].mean(axis=1) for idx in index_band_pass],
            axis=1
        )                                                               # (n_times, size_arr_freq)

    band_pass_prom_t              = _band_means_2d(BEM)
    band_pass_prom_t_I1           = _band_means_2d(I1)
    band_pass_prom_t_I2           = _band_means_2d(I2)
    band_pass_prom_t_Tlss_resta   = _band_means_2d(TLSS)




    # --- Promedios 1D (solo frecuencia) ---
    def _band_means_1d(arr):
        return np.array([arr[idx].mean() for idx in index_band_pass])  # (size_arr_freq,)

    band_pass_prom_t_betasky       = _band_means_1d(np.asarray(T_sky_bet_total))
    band_pass_prom_t_betaload      = _band_means_1d(np.asarray(T_load_bet_total))
 

    # --- sub_band_def: (n_times, size_arr_freq*2) ---
    sub_band_row = np.empty(size_arr_freq * 2)
    sub_band_row[0::2] = band_starts
    sub_band_row[1::2] = band_ends
    sub_band_def = np.tile(sub_band_row, (n_times, 1))                 # (n_times, size_arr_freq*2)

    return (
        
        band_pass_prom_t,
        band_pass_prom_t_I1,
        band_pass_prom_t_I2,
        band_pass_prom_t_betasky,
        band_pass_prom_t_betaload,
        band_pass_prom_t_Tlss_resta,
    )
