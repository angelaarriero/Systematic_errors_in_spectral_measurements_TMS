#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:51:54 2023

@author: aarriero
"""
import numpy as np
import matplotlib.pyplot as plt
import sys

# Main functions used
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
def noise_1f_white_ang(T_obs,f_sampling,signoise,meannoise,alpha,f_knee):
    
    # Derived parameters
    t_sampling        = 1.0 / f_sampling        # time between samples (s)
    nsamp             = int(T_obs * f_sampling) # total number of samples (samples)
    time_sample_array = np.arange(nsamp) * t_sampling
    dt = t_sampling
    dF = 1.0/T_obs 
    #Generate white noise
    White_noise = np.random.normal(meannoise, signoise, nsamp) #  loc, scale, size
    
    # Computing the one-dimensional discrete Fourier Transform. Normalised
    White_noise_fft = direct_fft( White_noise, f_sampling ) 
    # Return the Discrete Fourier Transform sample frequencies.
    F = np.fft.fftfreq(nsamp, d = t_sampling)
    # Power spectrum: |G|^2
    masc = (F > 0) #para solo usar frecuencias positivas
    Power_spec= powerspectrum(White_noise, f_sampling )
    amplitud_noise= F[masc]*0+signoise**2. * T_obs/f_sampling
    amplitud_noise_cons= signoise**2. * T_obs/f_sampling
    #========================
    # 1/f SECTION.
    # First, we define 1/f noise parameters, and build the correction function

    ps_corr = F*0 
    cut     = (F>0)
    ps_corr[cut] = 1. + (f_knee/F[cut])**alpha
    cut     = (F<0)
    ps_corr[cut] = 1. + (f_knee/np.abs(F[cut]))**alpha
    cut     = (F==0)
    ps_corr[cut] = 1. + (f_knee/F[1])**alpha
    
    noise_1f=Power_spec*ps_corr
    b=White_noise_fft *np.sqrt(ps_corr) #b=White_noise_fft *np.sqrt(ps_corr)
    b_conj=np.real(b * np.conjugate(b) ) 
    curve_1fnoise=signoise**2. * T_obs/f_sampling * ps_corr
    #1/f noise aspl a function of time
    time_1fnoise2= inverse_fft(b, f_sampling)
    return time_sample_array,White_noise,F,Power_spec,amplitud_noise,White_noise_fft,masc,noise_1f,curve_1fnoise,time_1fnoise2,b_conj,nsamp
