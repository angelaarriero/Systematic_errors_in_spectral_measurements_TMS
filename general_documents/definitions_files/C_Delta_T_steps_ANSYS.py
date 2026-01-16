import sys
import os
# Ruta absoluta a tu proyecto principal
ruta_base = "/home/aarriero/Documents/Angela_cmb/four_year/"
# Agregar al sys.path (al inicio para prioridad)
sys.path.insert(0, ruta_base)
print(ruta_base)

import csv
import numpy as np

from numpy.fft import fft

sys.path.append(os.path.join(ruta_base, "general_documents/definitions_files"))

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
ruta_toml = os.path.join(ruta_base, "general_documents", "data_files")
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

def C_Delta_T(array1_tiempo,array4_Tsky,t_load_r,n,step):
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##################### TEMPERATURE INPUT FRONT END: ANSYS OUTPUT #################################################
    ##########################################################################################################
    ##########################################################################################################
    #n=data["Sky"]["n"]
    ruta_files_n = os.path.join(ruta_base, "general_documents", "data_files")
    f1_file = os.path.join(ruta_files_n , "V1_Datos_ANSYS_TMS_coldload_STEPS_DEC25_V1.csv")
    x, y_ajustada_append=rectas_ANSYS_outputs(f1_file,51)
    if step==100:
        print('nominal case: paper')
        Tw=np.ones(n)*data["Window"]["Temperature"] # T. window 300K
        Tirf=np.ones(n)*data["IRfilter"]["Temperature"] # T. IR filter 50K
        Txps=np.ones(n)*0
        Tfhs= np.ones(n)*data["FeedHornSky"]["Temperature"] # T. sky feed-horn 5K
        Tomts=np.ones(n)*data["OMTsky"]["Temperature"] # T. OMT sky 5K
        ThX=np.ones(n)*data["HybridX"]["Temperature"]# T. Hybrid X

        Tl=np.ones(n)*data["4KCL"]["Temperature"] # T. Cold-Load
        Tfhl=np.ones(n)*data["FeedHornload"]["Temperature"] # T.load feed-horn
        Tomtl=np.ones(n)*data["OMTload"]["Temperature"] # T. OMT load
        ThY=np.ones(n)*data["HybridY"]["Temperature"] # T.Hybrid Y
        Tenv2_LNA=np.ones(n)*data["Environment"]["Tenv2"] # T. environment 2
    else:
        ##### [0]--> 5K [10]-->6K [20]-->7K [30]-->8K [40]-->9K [50]-->10K
        
        print('Step_ANSYS',y_ajustada_append[0][step])
        Tw=np.ones(n)*y_ajustada_append[1][step] # T. window
        Tirf=np.ones(n)*y_ajustada_append[3][step]# T. IR filter
        Txps=np.ones(n)*y_ajustada_append[4][step]# T. XPS filter
        Tfhs=np.ones(n)* y_ajustada_append[6][step] # T. sky feed-horn
        Tfhl=np.ones(n)*y_ajustada_append[7][step] # T.load feed-horn
        Tomts=np.ones(n)*y_ajustada_append[8][step] # T. OMT sky
        Tomtl=np.ones(n)*y_ajustada_append[9][step] # T. OMT load
        Tl=np.ones(n)*y_ajustada_append[10][step] # T. Cold-Load
        ThX=np.ones(n)*y_ajustada_append[11][step]# T. Hybrid X
        ThY=np.ones(n)*y_ajustada_append[12][step] # T.Hybrid Y
        Tenv2_LNA=np.ones(n)*y_ajustada_append[15][step] # T environment LNA Tenv2
    
    
    """""
    
    ##### [0]--> 5K [10]-->6K [20]-->7K [30]-->8K [40]-->9K [50]-->10K
    x, y_ajustada_append=rectas_ANSYS_outputs(f1_file,51)
    print('Step_ANSYS',y_ajustada_append[0][step])
    Tw=np.ones(n)*y_ajustada_append[1][step] # T. window
    Tirf=np.ones(n)*y_ajustada_append[3][step]# T. IR filter
    Txps=np.ones(n)*y_ajustada_append[4][step]# T. XPS filter
    Tfhs=np.ones(n)* y_ajustada_append[6][step] # T. sky feed-horn
    Tfhl=np.ones(n)*y_ajustada_append[7][step] # T.load feed-horn
    Tomts=np.ones(n)*y_ajustada_append[8][step] # T. OMT sky
    Tomtl=np.ones(n)*y_ajustada_append[9][step] # T. OMT load
    Tl=np.ones(n)*y_ajustada_append[10][step] # T. Cold-Load
    ThX=np.ones(n)*y_ajustada_append[11][step]# T. Hybrid X
    ThY=np.ones(n)*y_ajustada_append[12][step] # T.Hybrid Y
    Tenv2_LNA=np.ones(n)*y_ajustada_append[15][step] # T environment LNA Tenv2
    """""
    
    """""
    Tw=np.ones(n)*data["Window"]["Temperature"] # T. window 300K
    Tirf=np.ones(n)*data["IRfilter"]["Temperature"] # T. IR filter 50K
    Txps=np.ones(n)*0 # T. XPS filter
    Tfhs= np.ones(n)*data["FeedHornSky"]["Temperature"] # T. sky feed-horn 5K
    Tomts=np.ones(n)*data["OMTsky"]["Temperature"] # T. OMT sky 5K
    ThX=np.ones(n)*data["HybridX"]["Temperature"]# T. Hybrid X

    Tl=np.ones(n)*data["4KCL"]["Temperature"] # T. Cold-Load
    Tfhl=np.ones(n)*data["FeedHornload"]["Temperature"] # T.load feed-horn
    Tomtl=np.ones(n)*data["OMTload"]["Temperature"] # T. OMT load
    ThY=np.ones(n)*data["HybridY"]["Temperature"] # T.Hybrid Y
    """""

    Tenv1=np.ones(n)*data["Environment"]["Tenv1"] # T. environment 1 
    Tenv2=np.ones(n)*data["Environment"]["Tenv2"] # T. environment 2
    Troom=np.ones(n)*data["Environment"]["Troom"] # T. cryos 1 (T.room)
    
    T_ext_cry=np.ones(n)*data["Environment"]["T_ext_cry"] # 
    T_BEM_filter=np.ones(n)*data["Environment"]["T_BEM_filter"] # 
    T_after_filt_BEM=np.ones(n)*data["Environment"]["T_after_filt_BEM"] # 
    T_after_ampl_DC=np.ones(n)*data["Environment"]["T_after_ampl_DC"] # 
    T_FPGA=np.ones(n)*data["Environment"]["T_FPGA"] #
    
    Tcryo1=np.ones(n)*data["Environment"]["Tcryo1"] # T. cryos 2 (1st stage)
    Tcryo2=np.ones(n)*data["Environment"]["Tcryo2"] # T. cryos 3  (2nd stage)

    SPOw=np.ones(n)*pow(10,data["SPO"]["Window"]/10) # SPO window
    #SPOw=np.zeros(n)
    SPOirf=np.ones(n)*pow(10,data["SPO"]["IRfilter"]/10)# SPO IR filter
    SPO=pow(10,np.ones(n)*data["SPO"]["4KCL"]) # SPO Cold-load
    
    RLirf=np.ones(n)*pow(10,(data["IRfilter"]["RL"]/10)) # Return Loss IR filter
    RLlna1s=np.ones(n)*pow(10,(data["LNA1"]["RL"]/10)) # Return Loss lna1
    RLlna2s=np.ones(n)*pow(10,(data["LNA2"]["RL"]/10)) # Return Loss lna2
    RLlna3l=np.ones(n)*pow(10,(data["LNA3"]["RL"]/10)) # Return Loss lna3
    RLlna4l=np.ones(n)*pow(10,(data["LNA4"]["RL"]/10)) # Return Loss lna4
    
    
    ##...............--------###################...............###
    ####...............# Losses Return and Insertion loss ...............
    ###...............----------#############...............#
    ruta_files_n = os.path.join(ruta_base, "general_documents", "data_files")
    f1_file = os.path.join(ruta_files_n , "rl_hyb.csv")
    f2_file = os.path.join(ruta_files_n , "IL_hyb.csv")
    f3_file = os.path.join(ruta_files_n , "IL_omt.csv")
    #f4_file = os.path.join(ruta_files_n , "RL_omt.csv")
    f4_file = os.path.join(ruta_files_n , "OMT_measure_R.csv")
    f5_file = os.path.join(ruta_files_n , "RL_feedhorn.csv")
    f6_file = os.path.join(ruta_files_n , "RL_window.csv")
    f7_file = os.path.join(ruta_files_n , "LNA_20C.csv")
    f8_file = os.path.join(ruta_files_n , "CR117_load_RL.csv")
    f9_file = os.path.join(ruta_files_n , "TN_20_C.csv")
    f10_file = os.path.join(ruta_files_n , "noise_lna_amp_roomT.csv")
    f11_file = os.path.join(ruta_files_n , "gain_lna_amp_roomT.csv")
    f12_file = os.path.join(ruta_files_n , "GAIN_DC.csv")
    f13_file = os.path.join(ruta_files_n , "Noise_figu_DC.csv")
    f14_file = os.path.join(ruta_files_n , "TMS_IR_filter_10_layers_IL_10-20GHz.csv")
    

    Q,W,E,R,Z,X,C,V,xx1,data_RL_W,data_RL_FH,data_RL_omt,data_IL_omt,data_IL_hyb,data_RL_hyb,data_gain_lna,N,M,data_RL_load,U,Qs,Ws,Es,Rs,noise_lna_amp_roomT,N1,N2,N3,N4,Un1,Un2,Un3,Un4,sfN1=datos_simulados_RI(n,f1_file,f2_file,f3_file,f4_file,f5_file,f6_file,f7_file,f8_file,f9_file,f10_file)

    ### XPS material 
    x_fit,y_fit_IRfilter_il =datos_componente3(f14_file,n,0)
    IL_irfilter_t=y_fit_IRfilter_il
    x_fit2,y_fit_window_il =datos_componente3(f14_file,n,-0.05)
    x_fit3,y_fit_Q_il =datos_componente3(f14_file,n,-0.1)
    x_fit3,y_fit_OMT_il =datos_componente3(f14_file,n,-0.35)#-0.35
    #min_max3(y_fit_OMT_il)
    
    Q=y_fit_Q_il
    R=y_fit_window_il
    print('max:L W',10*np.log10(1-max(R))) 
    print('min:L W',10*np.log10(1-min(R))) 
    print('mean:L W',10*np.log10(1-np.mean(R)))
    E=IL_irfilter_t ## il IRfilter
    print('max:L IR',10*np.log10(1-max(E)))
    print('min:L IR',10*np.log10(1-min(E)))
    print('mean:L IR',10*np.log10(1-np.mean(E)))
    
    Wl=Q## il FH
    Ws=Q 
    print('max:L fh',10*np.log10(1-max(Wl)))
    print('min:L fh',10*np.log10(1-min(Wl)))
    print('mean:L fh',10*np.log10(1-np.mean(Wl)))
    Vl=V ## rl FH
    Vs=V 
    Xl=X ## RL OMT
    Xs=X 
    Ql=y_fit_OMT_il ## IL OMT
    Qs=y_fit_OMT_il
    print('max:L omt',10*np.log10(1-max(Ql)))
    print('min:L omt',10*np.log10(1-min(Ql)))
    print('mean:L omt',10*np.log10(1-np.mean(Ql)))
    
    C1=C ## RL HYB
    Q1=Q ## IL HYB
    C2=C 
    Q2=Q 
    print('max:L HYB',10*np.log10(1-max(Q1)))
    print('min:L HYB',10*np.log10(1-min(Q1)))
    print('mean:L hyb',10*np.log10(1-np.mean(Q1)))
    
    #### LNAs 
    ## https://lownoisefactory.com/wp-content/uploads/2022/03/lnf-lnc6_20c.pdf
    ### I assume same Tn and G to all the amplifiers
    
    G1=N # GAIN
    G2=N
    G3=N
    G4=N
    
    U1=U ## noise temperature
    U2=U
    U3=U
    U4=U
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ############################### TEMPERATURE INPUT BACKED END #################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ## AMPLIFIERS
    ### https://qpmw.com/product/amplifiers/low-noise/amlna-0120-01/#!prettyPhoto
    RlnaBEM=np.ones(n)*pow(10,(data["BEM_amp"]["RL"]/10)) # Return Loss 
    GainBEM=np.ones(n)*pow(10,(data["BEM_amp"]["Gain"]/10)) # Gain 
    TnBem=np.ones(n)*((pow(10,(data["BEM_amp"]["Fnoise"])/10)-1)*300) ### Noise Temperature (noise figure= 4dB)

    ### FILTER
    RfilBem=np.ones(n)*pow(10,(data["BEM_filter"]["RL"]/10)) # Return Loss
    IfilBem=np.ones(n)*pow(10,(data["BEM_filter"]["IL"]/10)) # Insertion Loss
    
    TnBem_var=(noise_lna_amp_roomT-np.mean(noise_lna_amp_roomT))*(np.mean(TnBem)/np.mean(noise_lna_amp_roomT))+np.mean(TnBem)

    freq11, data_res11,xdup_freq11,ydup_dat11,xx11,gain_lna_amp_roomT =datos_componente(f11_file,n) #gainLNAtroom
    new_gain_lna_troom=sparams_to_power(gain_lna_amp_roomT,n) ### used to simulate the gain in the BEM AMPL
    GainBEM=new_gain_lna_troom
    
    TnBem_var1=TnBem_var
    TnBem_var2=TnBem_var
    TnBem_var3=TnBem_var
    TnBem_var4=TnBem_var
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ################################ TEMPERATURE INPUT DOWN-CONVERTER #################################################
    ##########################################################################################################
    ##########################################################################################################
    
    ## MIXER
    ### https://www.mouser.com/datasheet/2/1030/MDB_24H_2b-1700725.pdfsrsltid=AfmBOoqOyqtMh0OO23Dcg78k4z348bNhYnHH7l0cSBzv10tH27Pgxidj
    T_mixer=np.ones(n)*data["Mixer"]["T_mixer"] # 
    Fmixer=(np.ones(n)*(pow(10,(data["Mixer"]["Fnoise"]/10))-1)) # noise figure
    Lmixer=np.ones(n)*(1-pow(10,(data["Mixer"]["Lmixer"]/10))) # Conversion Loss 
    LO=np.ones(n)*(data["Mixer"]["LO"]/10) #T. added due to the LO
    # ----- MIXER EQUATION ----
    
    #Tmixer_A1=T_mixer*(Fmixer-pow(10,(2/10))+Lmixer)+LO*T_after_ampl_DC ##----> check this
    Tmixer_A1=1000
    Tmixer_A2=Tmixer_A1
    Tmixer_B1=Tmixer_A1
    Tmixer_B2=Tmixer_A1
    
    #### AMPLIFIERS DC
    ###https://www.mouser.com/datasheet/2/1030/PHA_202_2b-1700733.pdf?srsltid=AfmBOoqVZ1XoPo0bhApVXruea505aW-8BDN38TfeyBMXNrZrS3EYFWaa
    RlnaDC=np.ones(n)*pow(10,(data["DC_amp"]["RL"]/10)) # Return Loss 
    TnDC=np.ones(n)*((pow(10,(data["DC_amp"]["Fnoise"])/10)-1)*300) # Noise Temperature
    GainDC=np.ones(n)*pow(10,(data["DC_amp"]["Gain"]/10)) # Gain

    ##### FILTER
    TfilDC=np.ones(n)*300  # T. filter == T.room
    IfilDC=np.ones(n)*pow(10,(data["DC_filter"]["IL"]/10)) # Insertion Loss
    RfilDC=np.ones(n)*pow(10,(data["DC_filter"]["RL"]/10)) # Return Loss
    
    freq12, data_res12,xdup_freq12,ydup_dat12,xx11,gain_amp_DC =datos_componente2(f12_file,n) #gainampl DC
    new_gain_DC_troom=sparams_to_power(gain_amp_DC,n) ###
    
    GainDC=new_gain_DC_troom
    TnDC_conve=conversion_dc(f13_file,n)
    TnDC=TnDC_conve
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ################################ CALCULATION OF LOSSES DUE TO MATERIAL#####################################
    ################################ PROPERTIES AND PHYSICAL TEMPERATURE ####################################
    ##########################################################################################################
    ##########################################################################################################
    
    #...............#######################################################################...................#
    #...............#################        hw=(1-L)(1-R)(1-SPO)        ###################...............#
    #R=0
    hw=(np.ones(n)-Z)*(np.ones(n)-R)*(np.ones(n)-SPOw) # h Window
    #print('esto es L de w:',np.mean(R))
    #hw=(np.ones(n)-0.01384414741820192)*(np.ones(n)-R)*(np.ones(n)-SPOw)
    #print('hw:',np.mean(hw))
    hirf=(np.ones(n)-RLirf)*(np.ones(n)-E)*(np.ones(n)-SPOirf) # h IR filter
    hXPS=(np.ones(n)-RLirf)*(np.ones(n)-E)*(np.ones(n)-SPOirf) # h XPS
    #hXPS=np.ones(n) # h XPS
    #print('hirf:',np.mean(hirf))
    hfhs=(np.ones(n)-Vs)*(np.ones(n)-Ws) # h sky feed-horn
    #print('hfhs:',np.mean(hfhs))
    homts=(np.ones(n)-Xs)*(np.ones(n)-Qs) # h sky OMT
    hfhl=(np.ones(n)-Vl)*(np.ones(n)-Wl) # h Load feed-horn
    #print('hfhl:',np.mean(hfhl))
    homtl=(np.ones(n)-Xl)*(np.ones(n)-Ql) # h load omt
    hhyb1=(np.ones(n)-C1)*(np.ones(n)-Q1) # h hybrid X
    hhyb2=(np.ones(n)-C2)*(np.ones(n)-Q2) # h hybrid Y
    hlna1=(1-RLlna1s) # h LNA1
    hlna2=(1-RLlna2s) # h LNA2
    hlna3=(1-RLlna3l) # h LNA3
    hlna4=(1-RLlna4l) # h LNA4
    hload=(np.ones(n)-M)*(1-SPO) #h Cold-load
    hlnaBEM=(np.ones(n)-RlnaBEM)
    hfilterBEM=np.ones(n)*((np.ones(n)-RfilBem)*(np.ones(n)-IfilBem)) ### 
    hlnaDC=(np.ones(n)-RlnaDC)
    hfilDC=(np.ones(n)-RfilDC)*(np.ones(n)-IfilDC)
    ### effective losses of hybrids and LNAs BEM stage
    Aphi1=((hhyb1*hlna1)/(2*np.ones(n)))
    Aphi2=((hhyb1*hlna2)/(2*np.ones(n)))
    Aphi3=((hhyb2*hlna3)/(2*np.ones(n)))
    Aphi4=((hhyb2*hlna4)/(2*np.ones(n)))
    
    if step==100:
        hXPS=np.ones(n) # h XPS
        print('2. nominal case: paper')
    else:
        hXPS=(np.ones(n)-RLirf)*(np.ones(n)-E)*(np.ones(n)-SPOirf) # h XPS
        print('steps case')
        
    #a2=hw*hirf*hfhs*homts*0.5  #### beta SKY
    a2=hw*hirf*hXPS*hfhs*homts*0.5  #### beta SKY
    a3=hfhl*homtl*0.5*(np.ones(n)-M)*(1-SPO) #### beta LOAD
    ### effective SPO 
    #a8=hirf*hfhs*homts*0.5*(SPOw)####---->>spo SKY
    a8=hirf*hXPS*hfhs*homts*0.5*(SPOw)####---->>spo SKY
    a8_1=hirf*hfhs*homts*0.5*(SPOirf)
    
    a9=hfhs*homts*0.5*(SPOirf) ####---->>spo SKY
    a10=hfhl*homtl*0.5*(SPO) ####---->>spo LOAD
    
    HDC=(hlnaDC*hfilDC)*GainDC ## 
    loss1_Hs=hlnaBEM*hfilterBEM*G1*GainBEM*HDC
    loss2_Hs=hlnaBEM*hfilterBEM*G2*GainBEM*HDC
    loss3_Hs=hlnaBEM*hfilterBEM*G3*GainBEM*HDC
    loss4_Hs=hlnaBEM*hfilterBEM*G4*GainBEM*HDC
    
    

    
    
    #...............#######################################################################...................#
    #...............#################   Beta sky and Beta load TOTAL        ###################...............#
    
    
    beta_sky1=(a2*hlna1*hhyb1*loss1_Hs)/(2*np.ones(n))
    beta_sky2=(a2*hlna2*hhyb1*loss1_Hs)/(2*np.ones(n))
    beta_sky3=(a2*hlna3*hhyb2*loss1_Hs)/(2*np.ones(n))
    beta_sky4=(a2*hlna4*hhyb2*loss1_Hs)/(2*np.ones(n))

    beta_load1=(a3*hlna1*hhyb1*loss1_Hs)/(2*np.ones(n))
    beta_load2=(a3*hlna2*hhyb1*loss1_Hs)/(2*np.ones(n))
    beta_load3=(a3*hlna3*hhyb2*loss1_Hs)/(2*np.ones(n))
    beta_load4=(a3*hlna4*hhyb2*loss1_Hs)/(2*np.ones(n))

    
    
    #...............#######################################################################...................#
    #...............#################       SUMMATORIES        ###################...............#
    
    ### hybrid FIRST STAGE
    
    hyb_effect1=(ThX*Q1)+(Tenv2*C1) # (T.hybX* Il.HybX)+ (T.env2*RL.hybX)
    hyb_effect2=(ThY*Q2)+(Tenv2*C2) # (T.hybY* Il.HybY)+ (T.env2*RL.hybY)
    
    
    ##### Summatory for effective Insertion losses 
    
    if step==100:
        sum_tem_IL_sky=(Tw*R*hirf*hfhs*homts*0.5*(1-SPOw))+ (Tirf*E*hfhs*homts*0.5*(1-SPOirf))+(Tfhs*Ws*homts*0.5)+(Tomts*Qs)
    else:
        sum_tem_IL_sky=(Tw*R*hirf*hXPS*hfhs*homts*0.5*(1-SPOw))+ (Tirf*E*hXPS*hfhs*homts*0.5*(1-SPOirf)) + (Txps*E*hfhs*homts*0.5*(1-SPOirf))+(Tfhs*Ws*homts*0.5)+(Tomts*Qs)
        
    #sum_tem_IL_sky=(Tw*R*hirf*hfhs*homts*0.5*(1-SPOw))+ (Tirf*E*hfhs*homts*0.5*(1-SPOirf))+(Tfhs*Ws*homts*0.5)+(Tomts*Qs)
    #sum_tem_IL_sky=(Tw*R*hirf*hXPS*hfhs*homts*0.5*(1-SPOw))+ (Tirf*E*hXPS*hfhs*homts*0.5*(1-SPOirf)) + (Txps*E*hfhs*homts*0.5*(1-SPOirf))+(Tfhs*Ws*homts*0.5)+(Tomts*Qs)

    sum_tem_IL_load=(Tfhl*Wl*homtl*0.5)+(Tomtl*Ql)

    ##### Summatory for effective Return losses 
    
    if step==100:
        sum_R_sky=(Z*hirf*hfhs*homts*0.5*(Tenv1/Tenv2)*(1-SPOw))+(RLirf*hfhs*homts*0.5*(1-SPOirf))+(Vs*homts*0.5)+(Xs)    
    else:
        sum_R_sky=(Z*hirf*hXPS*hfhs*homts*0.5*(Tenv1/Tenv2)*(1-SPOw))+(RLirf*hXPS*hfhs*homts*0.5*(1-SPOirf))+(RLirf*hfhs*homts*0.5*(1-SPOirf))+(Vs*homts*0.5)+(Xs)
    
    #sum_R_sky=(Z*hirf*hfhs*homts*0.5*(Tenv1/Tenv2)*(1-SPOw))+(RLirf*hfhs*homts*0.5*(1-SPOirf))+(Vs*homts*0.5)+(Xs)
    #sum_R_sky=(Z*hirf*hXPS*hfhs*homts*0.5*(Tenv1/Tenv2)*(1-SPOw))+(RLirf*hXPS*hfhs*homts*0.5*(1-SPOirf))+(RLirf*hfhs*homts*0.5*(1-SPOirf))+(Vs*homts*0.5)+(Xs)
    
    sum_R_load=(M*(1-SPO)*hfhl*homtl*0.5)+(Vl*homtl*0.5)+(Xl)
    
    if step==100:
        offs1=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)+(Tcryo2*a10))
        offl1=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)-(Tcryo2*a10))
        offs2=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)+(Tcryo2*a10))
        offl2=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)-(Tcryo2*a10))
    else:
        offs1=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)+(Tcryo2*a10))
        offl1=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)-(Tcryo2*a10))
        offs2=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)+(Tcryo2*a10))
        offl2=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)-(Tcryo2*a10))
    
    
    #offs1=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)+(Tcryo2*a10))
    #offl1=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)-(Tcryo2*a10))
    #offs2=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)+(Tcryo2*a10))
    #offl2=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9)-(Tcryo2*a10))
    
    #offs1=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)+(Tcryo2*a10))
    #offl1=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)-(Tcryo2*a10))
    #offs2=((sum_tem_IL_sky)+(sum_tem_IL_load))+Tenv2*((sum_R_sky)+sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)+(Tcryo2*a10))
    #offl2=((sum_tem_IL_sky)-(sum_tem_IL_load))+Tenv2*((sum_R_sky)-sum_R_load)+((T_ext_cry*a8+Tcryo1*a9+Tcryo2*a8_1)-(Tcryo2*a10))
    
    
    #...............#######################################################################...................#
    #...............#################    OFFSET: A1,A2,B1,B2 FEM           ###################...............#
    
    if step==100:
        A1_off=((Aphi1*offs1)+(hyb_effect1*hlna1)+(Tenv2*RLlna1s))
        B1_off=((Aphi3*offs2)+(hyb_effect2*hlna3)+(Tenv2*RLlna3l))
        A2_off=((Aphi2*offl1)+(hyb_effect1*hlna2)+(Tenv2*RLlna2s))
        B2_off=((Aphi4*offl2)+(hyb_effect2*hlna4)+(Tenv2*RLlna4l))
        
    else:
        A1_off=((Aphi1*offs1)+(hyb_effect1*hlna1)+(Tenv2_LNA*RLlna1s))
        B1_off=((Aphi3*offs2)+(hyb_effect2*hlna3)+(Tenv2_LNA*RLlna3l))
        A2_off=((Aphi2*offl1)+(hyb_effect1*hlna2)+(Tenv2_LNA*RLlna2s))
        B2_off=((Aphi4*offl2)+(hyb_effect2*hlna4)+(Tenv2_LNA*RLlna4l))
    
    #A1_off=((Aphi1*offs1)+(hyb_effect1*hlna1)+(Tenv2*RLlna1s))
    #B1_off=((Aphi3*offs2)+(hyb_effect2*hlna3)+(Tenv2*RLlna3l))
    #A2_off=((Aphi2*offl1)+(hyb_effect1*hlna2)+(Tenv2*RLlna2s))
    #B2_off=((Aphi4*offl2)+(hyb_effect2*hlna4)+(Tenv2*RLlna4l))
    
    #A1_off=((Aphi1*offs1)+(hyb_effect1*hlna1)+(Tenv2_LNA*RLlna1s))
    #B1_off=((Aphi3*offs2)+(hyb_effect2*hlna3)+(Tenv2_LNA*RLlna3l))
    #A2_off=((Aphi2*offl1)+(hyb_effect1*hlna2)+(Tenv2_LNA*RLlna2s))
    #B2_off=((Aphi4*offl2)+(hyb_effect2*hlna4)+(Tenv2_LNA*RLlna4l))
    
    
    
    #...............#######################################################################...................#
    #...............#################    OFFSET BEM +   DOWN-CONVERTER         ###################...............#
    
    
    ### OFFSET DUE TO BEM COMPONENTS, AMPLIFIERS AND FILTERS
    Tloss2_1=((T_BEM_filter*RlnaBEM*hfilterBEM*GainBEM)+(T_BEM_filter*IfilBem)+(T_after_filt_BEM*RfilBem))*HDC
    ### OFFSET DUE TO DOWN-CONVERTER COMPONENTS, MIXER, AMPLIFIERS AND FILTERS
    Tloss3_1=(((1-RlnaDC)*hfilDC*GainDC)*Tmixer_A1)+(T_after_ampl_DC*RlnaDC*hfilDC*GainDC)+(TfilDC*IfilDC)+T_FPGA*RfilDC
    
    #...............#######################################################################...................#
    #...............#################    Noise Temperatures         ###################...............#
    
    #### FEM (LNAs)
    Tn1=U1*hlnaBEM*hfilterBEM*hfilDC*hlnaDC*GainDC*GainBEM*G1
    Tn2=U2*hlnaBEM*hfilterBEM*hfilDC*hlnaDC*GainDC*GainBEM*G2
    Tn3=U3*hlnaBEM*hfilterBEM*hfilDC*hlnaDC*GainDC*GainBEM*G3
    Tn4=U4*hlnaBEM*hfilterBEM*hfilDC*hlnaDC*GainDC*GainBEM*G4
    #### BEM (amplifiers)
    Tn2bem_1=TnBem_var1*hfilterBEM*hfilDC*hlnaDC*GainDC*GainBEM
    #### DOWN-CONVERTER (amplifiers)
    Tn3DC_1=TnDC*hfilDC*GainDC
    
    #####  NOISE TEMPERATURE IN THE X BRANCH
    Tn1FEM_1=(Tn1+Tn2)
    TnBEM_1= (Tn2bem_1)+(Tn2bem_1)
    TnDC_1=(Tn3DC_1)+(Tn3DC_1)
    #####  NOISE TEMPERATURE IN THE Y BRANCH
    Tn1FEM_3=(Tn3+Tn4)
    TnBEM_3=(Tn2bem_1)+(Tn2bem_1)
    TnDC_3=(Tn3DC_1)+(Tn3DC_1) 
    
    Gtot=hfilterBEM*hfilDC*GainDC*GainBEM*G1 #### TOTAL GAIN SYSTEM
    
    T_sky_bet_total=(2*beta_sky2+2*beta_sky4)/Gtot
    T_load_bet_total=(2*beta_load2+2*beta_load4)/Gtot
    ##### Noise temperature of sky and load isolated
    
    Tn_tot_sky=(Tn1FEM_1+TnBEM_1+TnDC_1)/Gtot
    Tn_tot_load=(Tn1FEM_3+TnBEM_3+TnDC_3)/Gtot
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ################################           MAIN CODE                 #####################################
    ################################ SKY AND LOAD INPUT: RADIOMETER OUTPUT ####################################
    #####################################       Delta T             ########################################
    ##########################################################################################################
    
    total_I1_BEM_atmos_cmb=[]
    total_I2_BEM_atmos_cmb=[]
    total_I1_FEM_atmos_cmb=[]
    total_I2_FEM_atmos_cmb=[]
    total_FEM_atmos_cmb=[]
    total_BEM_atmos_cmb=[]
    Tlss_1=[]
    Tlss_2=[]
    Tlss_3=[]
    Tlss_4=[]
    Tlss_sky=[]
    Tlss_load=[]
    Tlss_resta=[]
    Tloss_sky=[]
    Tloss_load=[]
    total_C1_BEM_atmos_cmb=[]
    total_C2_BEM_atmos_cmb=[]
    total_D1_BEM_atmos_cmb=[]
    total_D2_BEM_atmos_cmb=[]
    freq_spec=[]
    for i in range(np.size(array1_tiempo)):
        
        ##########################################################################################################
        ########################### delta T equation outputs A1,A2,B1,B2 ############################################
        ##########################################################################################################
        ##########################################################################################################
        
        t_sky_r=array4_Tsky[i] # INPUT OF SKY

        #...............########################################################...................#
    #...............#################   FEM CALCULATION (IDEAL BEM AND DOWN-CONVERTER)      #########...............#
    ########################################################################################################
    
        e1_copy=Aphi1*(t_sky_r*a2 +t_load_r*a3)+A1_off## A1
        e2_copy=Aphi2*(t_sky_r*a2 -t_load_r*a3)+A2_off## A2
        e3_copy=Aphi3*(t_sky_r*a2 +t_load_r*a3)+B1_off## B1
        e4_copy=Aphi4*(t_sky_r*a2 -t_load_r*a3)+B2_off## B2
        
        Tn1_copy=U1 
        Tn2_copy=U2
        Tn3_copy=U3
        Tn4_copy=U4
        
        #...............######## HYBRID SECOND STAGE (DIGITAL HYBRIDS X and Y) inside the FPGA. #...........#########
        C1r_copy=(((e1_copy*G1)+(e2_copy*G2))) #C1
        C2r_copy=(((e1_copy*G1)-(e2_copy*G2))) #C2
        D1r_copy=(((e3_copy*G3)+(e4_copy*G4))) #D1
        D2r_copy=(((e3_copy*G3)-(e4_copy*G4))) #D2
        
        ############## SKY AND LOAD RECONSTRUCTED. I add the noise of the LNAs FIGURE 4 GREEN LINE (paper angela)
        sky_gth_copy=(C1r_copy+D1r_copy+(Tn1_copy*G1)+(Tn2_copy*G2))/G1
        load_gth_copy=(C2r_copy+D2r_copy+(Tn3_copy*G3)+(Tn4_copy*G4))/G3
        
        total_I1_FEM_atmos_cmb.append(sky_gth_copy)
        total_I2_FEM_atmos_cmb.append(load_gth_copy)
        Total_noBem_dc=(sky_gth_copy-load_gth_copy)
        
        total_FEM_atmos_cmb.append(Total_noBem_dc)
        
        ##########################################################################################################
        ##########################################################################################################
       #...............########################################################...................#
    #...............#################  Delta T: FEM+BEM+DOWN-CONVERTER       #########...............#
    ##########################################################################################################
    ##########################################################################################################
    
        
        e1=Aphi1*(t_sky_r*a2 +t_load_r*a3)+A1_off## A1
        e2=Aphi2*(t_sky_r*a2 -t_load_r*a3)+A2_off## A2
        e3=Aphi3*(t_sky_r*a2 +t_load_r*a3)+B1_off## B1
        e4=Aphi4*(t_sky_r*a2 -t_load_r*a3)+B2_off## B2
        
        #"""""
        s1=(loss1_Hs*e1)+(Tloss2_1)+(Tloss3_1) ### A1+BEM+DC
        s2=(loss2_Hs*e2)+(Tloss2_1)+(Tloss3_1) ### A2+BEM+DC
        s3=(loss3_Hs*e3)+(Tloss2_1)+(Tloss3_1) ### B1+BEM+DC
        s4=(loss4_Hs*e4)+(Tloss2_1)+(Tloss3_1) ### B2+BEM+DC
        #"""""
        
        #""""" in this part I remove the contribution of the beta sky and load, and also the input sky/load
        s1_noise_contr=(loss1_Hs*A1_off)+(Tloss2_1)+(Tloss3_1) ### A1+BEM+DC
        s2_noise_contr=(loss1_Hs*A2_off)+(Tloss2_1)+(Tloss3_1) ### A2+BEM+DC
        s3_noise_contr=(loss1_Hs*B1_off)+(Tloss2_1)+(Tloss3_1) ### B1+BEM+DC
        s4_noise_contr=(loss1_Hs*B2_off)+(Tloss2_1)+(Tloss3_1) ### B2+BEM+DC
        
        Tlss_1.append(s1_noise_contr)# A1
        Tlss_2.append(s2_noise_contr)# A2
        Tlss_3.append(s3_noise_contr)# B1
        Tlss_4.append(s4_noise_contr)# B2
        
        Tlss_sky_t=s1_noise_contr+s2_noise_contr+s3_noise_contr+s4_noise_contr
        Tlss_load_t=s1_noise_contr-s2_noise_contr+s3_noise_contr-s4_noise_contr
        
        Tlss_sky.append(Tlss_sky_t/Gtot)
        Tlss_load.append(Tlss_load_t/Gtot)
        Tlss_resta.append((Tlss_sky_t/Gtot)-(Tlss_load_t/Gtot))


        ##### second hybrid inside the FPGA
        C1r=(((s1)+(s2)))
        C2r=(((s1)-(s2)))
        D1r=(((s3)+(s4)))
        D2r=(((s3)-(s4)))
        
        total_C1_BEM_atmos_cmb.append(C1r)
        total_C2_BEM_atmos_cmb.append(C2r)
        total_D1_BEM_atmos_cmb.append(D1r)
        total_D2_BEM_atmos_cmb.append(D2r)
        #""""
        ###########################################################################################################
        ############# NOW HERE, WE SUMM THE SIGNALS C1,D1, C2 ,D2 WITH THE THERMAL NOISE ADDED BY THE AMPLIFIERS
        ################################# FEM+BEM+DC

        sky_gth2=(C1r+D1r+Tn1FEM_1+TnBEM_1+TnDC_1) ## Tsky I1
        load_gth2=(C2r+D2r+Tn1FEM_3+TnBEM_3+TnDC_3) ## Tload I2
        
        total_I1_BEM_atmos_cmb.append(sky_gth2)
        total_I2_BEM_atmos_cmb.append(load_gth2)

        Total_bem_dc=(sky_gth2-load_gth2)/Gtot ##### WE OBTAIN THE OUTPUT DIVIDING BY THE TOTAL GAIN CONTRIBUTION
        total_BEM_atmos_cmb.append(Total_bem_dc)
        freq_spec.append(xx1)
    
   
    return total_BEM_atmos_cmb,total_I1_BEM_atmos_cmb,total_I2_BEM_atmos_cmb,freq_spec,Tlss_resta,y_ajustada_append,T_sky_bet_total,T_load_bet_total

def Weights_subBands(array1_tiempo,freq_spec,total_BEM_atmos_cmb):
    
    ########################################################################################################################
    ###################### SUBBANDAS PROMEDIO
    #############################################################################################
    #### aqui voy a calcular el promedio cada 250 Mhz con pesos == 1
    increase=0
    new_freq=freq_spec[0]*1e9
    band_pass_prom=[]
    size_arr_freq=int((new_freq[np.size(new_freq)-1]-new_freq[0])/250e6)
    index_band_pass=[]
    sub_band_def=[]
    for i in range(np.size(array1_tiempo)):### tiempo de observacion en segundos
        for j in range(size_arr_freq): ####### frecuencias de 10 a 20 Ghz
            x = new_freq[0]+(240e6*j)+(j*1e7) #### elijo la frecuencia principal (10Ghz)+ 240Mhz*(0)+(0)*1e7
            x_f = x+240e6
            sub_band_def.append(np.array([x,x_f]))
            #print('inicio',x)
            #print('fin',x_f)
            indices = np.where((new_freq >= x) & (new_freq <= x_f))[0]
            index_band_pass.append(indices)
            band_pass_prom.append(np.mean(total_BEM_atmos_cmb[i][indices]))

    band_pass_prom_t=np.reshape(band_pass_prom, (np.size(array1_tiempo),size_arr_freq))
    sub_band_def=np.reshape(sub_band_def, (np.size(array1_tiempo),size_arr_freq*2))
    print('band_pass_prom_t',np.shape(band_pass_prom_t))
    
    return sub_band_def, band_pass_prom_t,index_band_pass

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

def noise_instrument(array1_tiempo,freq_spec,band_pass_prom_t,f_knee,alpha):
    ###############################################################################################
    ########################## Definitions #################################
    
    nsamp=np.size(array1_tiempo)
    t_sampling=(array1_tiempo[1]-array1_tiempo[0])
    f_sampling = int(1/(array1_tiempo[1]-array1_tiempo[0]))
    T_obs= nsamp  / f_sampling

    F = np.fft.fftfreq(nsamp, d = t_sampling)
    ps_corr = F*0 
    cut     = (F>0)
    ps_corr[cut] = 1. + (f_knee/F[cut])**alpha
    cut     = (F<0)
    ps_corr[cut] = 1. + (f_knee/np.abs(F[cut]))**alpha
    cut     = (F==0)
    ps_corr[cut] = 1. + (f_knee/F[1])**alpha
    
    sigma_new=[]
    BEM_sigma_total=[]
    noise_total_sigma=[]
    Ti_total=[]
    mean_delta_T_sub_band_new=[]
        
    Ti_total_whitenoise=[]
    Ti_total_1fnoise=[]
    White_noise_fft=[]
    noise_1f_mean_curve=[]
    noise_1f_mean=[]
    Power_spec_whitenoise=[]
    f_sampling = int(1/(array1_tiempo[1]-array1_tiempo[0]))
    t_sampling=(array1_tiempo[1]-array1_tiempo[0])
    nsamp=np.size(array1_tiempo)
    print('nsamp',nsamp)
    new_freq=freq_spec[0]*1e9
    size_arr_freq=int((new_freq[np.size(new_freq)-1]-new_freq[0])/250e6)
    White_noise_subbands=[]
    
    print('size_arr_freq',(size_arr_freq))

    ################### sigma(i)=Tsys/sqrt(250MHz*time)
    
    for i in range(size_arr_freq):
        for j in range(np.size(array1_tiempo)):
            signoise    = band_pass_prom_t[j][i]/(np.sqrt(250e6*t_sampling))
            sigma_new.append(signoise)
            
    reshape_White_noise=np.reshape(sigma_new, (np.size(array1_tiempo), size_arr_freq))
    
    for i in range(size_arr_freq):
        ####################### White_noise ##################################
        media = 0      
        sigma = reshape_White_noise[:,i] 
        num_muestras = nsamp
        
        White_noise = np.random.normal(loc=media, scale=sigma, size=num_muestras)
        White_noise_subbands.append(White_noise)
        
        ###############################################################################################
    ############################################### 1/f NOISE ##################################
        Power_spec= powerspectrum(White_noise, f_sampling )
        noise_1f=Power_spec*ps_corr
        noise_1f_mean.append((noise_1f))
        curve_1fnoise=signoise**2. * T_obs/f_sampling * ps_corr
        noise_1f_mean_curve.append((curve_1fnoise))
        
        
    ################################  TOTAL NOISE ####################################################
    suma_total_signal_whitenoise=[]
    for i in range(size_arr_freq):
        a=band_pass_prom_t.T[i]+White_noise_subbands[i]
        suma_total_signal_whitenoise.append(a)
    print('suma_total_signal_whitenoise',np.shape(suma_total_signal_whitenoise))
    
    return sigma_new,White_noise_subbands,noise_1f_mean,noise_1f_mean_curve,suma_total_signal_whitenoise

