import streamlit as st
import pandas as pd
from pickle import load
import pickle
import numpy as np
import math as m
from PIL import Image
import os
from glob import glob


st.header("Advanced Shaft Fatigue Evaluation Shafi")

st.subheader('Dimensional Parameters')
htp="https://www.researchgate.net/profile/Changqing-Gong/publication/313456917/figure/fig1/AS:573308992266241@1513698923813/Schematic-illustration-of-the-geometry-of-a-typical-corrosion-defect.png"
st.image(htp, caption= "Fig. 1: Schematic illustration of the geometry of a typical corrosion defect.")

st.sidebar.header('User Input Parameters')

def user_input_features():
    shaft_diameter_A = st.sidebar.number_input('Shaft Diameter(A), D (mm)', value = 0.01)
    shaft_diameter_B = st.sidebar.number_input('Shaft Diameter(B), D (mm)', value = 0.01)
    shaft_length = st.sidebar.number_input('Shaft Length, L (mm)', value = 0.01)
    Applied_Force = st.sidebar.number_input('Applied Force, F (N)', value = 0.01)
    Sy = st.sidebar.number_input('Yield Stress, Sy (MPa)', value = 0.01)
    UTS = st.sidebar.number_input('Ultimate Tensile Strength, UTS (MPa)', value = 0.01)
    Length_of_F_to_shaft_end = st.sidebar.number_input('Length of F to shaft end, Lf (mm)', value = 0.01)
    Constant_a_for_ka = st.sidebar.number_input('Constant a for ka, a', value = 0.00)
    Constant_b_for_ka = st.sidebar.number_input('Constant b for ka, b', value = 0.00)
    Notch_radius = st.sidebar.number_input('Notch radius,r(mm)', value = 0.01)

    data = {'Da (mm)': shaft_diameter_A,
            'Db (mm)': shaft_diameter_B,
            'L (mm)': shaft_length,   
            'F (N)': Applied_Force,
            'Lf (mm)': Length_of_F_to_shaft_end,
            'UTS (MPa)': UTS,
            'Sy (MPa)': Sy,
            'a': Constant_a_for_ka,
            'b': Constant_b_for_ka,
            'r(mm)': Notch_radius,}      
           
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

Da=df['Da (mm)'].values.item()
Db=df['Db (mm)'].values.item()
L=df['L (mm)'].values.item()
F=df['F (N)'].values.item()
UTS=df['UTS (MPa)'].values.item()
Sy=df['Sy (MPa)'].values.item()
Lf=df['Lf (mm)'].values.item()
a=df['a'].values.item()
b=df['b'].values.item()
r=df['r(mm)'].values.item()


st.subheader('Nomenclature')
st.write(' Da is the shaft diameter A; Db is the shaft diameter B; L is the shaft length (i.e., by default = 1000 mm); F is the applied force on the shaft; Sy is the shaft material yield stress; UTS is the shaft material Ultimate Tensile Strength.')

# Calculate Se'
Se_prime = 0.5*UTS

user_input={'Da (mm)': "{:.2f}".format(Da),
            'Db (mm)': "{:.2f}".format(Db),
            'L (mm)': "{:.2f}".format(L),
            'Lf (mm)': "{:.2f}".format(Lf),
            'F (N)': "{:.2f}".format(F),
            'UTS (MPa)': "{:.2f}".format(UTS),
            'Sy (MPa)': "{:.2f}".format(Sy),
            'a': "{:.2f}".format(a),
            'b': "{:.2f}".format(b),
            'r(mm)': "{:.2f}".format(r)}
            
user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)



# Calculate Se'
calculated_param={'Se_prime (MPa)': "{:.2f}".format(Se_prime)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Se prime')
st.write(calculated_param_df)

calculated_param={'PTresca (MPa)': "{:.2f}".format(PTresca)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Intact Pipe Burst Pressure via Tresca')
st.write(calculated_param_df)

# Corroded Pipe
calculated_param={'P_ASME_B31G (MPa)': "{:.2f}".format(P_ASME_B31G)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corroded Pipe Burst Pressure via ASME_B31G')
st.write(calculated_param_df)

calculated_param={'P_DnV (MPa)': "{:.2f}".format(P_DnV)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via DnV')
st.write(calculated_param_df)

calculated_param={'P_PCORRC (MPa)': "{:.2f}".format(P_PCORRC)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Corrorded Pipe Burst Pressure via PCORRC')
st.write(calculated_param_df)

Pressure = [Pvm, PTresca, P_ASME_B31G, P_DnV, P_PCORRC]
index = ["Pvm (MPa)", "PTresca (MPa)", "P_ASME_B31G (MPa)", "P_DnV (MPa)", "P_PCORRC (MPa)"]
df = pd.DataFrame({"Burst Pressure (MPa)": Pressure}, index=index)



# Principle stresses for Maximum Operating Pressure
P1max = Pop_Max*D/(2*t)
P2max = Pop_Max*D/(4*t)
P3max = 0

# Principle stresses for Minimum Operating Pressure
P1min = Pop_Min*D/(2*t)
P2min = Pop_Min*D/(4*t)
P3min = 0




st.subheader('Reference')
st.write('Xian-Kui Zhu, A comparative study of burst failure models for assessing remaining strength of corroded pipelines, Journal of Pipeline Science and Engineering 1 (2021) 36 - 50, https://doi.org/10.1016/j.jpse.2021.01.008')

st.subheader('Assesment')
st.markdown('[Case Study](https://drive.google.com/file/d/1Ako5uVRPYL5k5JeEQ_Xhl9f3pMRBjCJv/view?usp=sharing)', unsafe_allow_html=True)
st.markdown('[Corroded Pipe Burst Data](https://docs.google.com/spreadsheets/d/1YJ7ziuc_IhU7-MMZOnRmh4h21_gf6h5Z/edit?gid=56754844#gid=56754844)', unsafe_allow_html=True)
st.markdown('[Pre-Test](https://forms.gle/wPvcgnZAC57MkCxN8)', unsafe_allow_html=True)
st.markdown('[Post-Test](https://forms.gle/FdiKqpMLzw9ENscA9)', unsafe_allow_html=True)
