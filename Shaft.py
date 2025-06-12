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

image_url = "https://homework.study.com/cimages/multimages/16/060519-118885225862519178792.jpg"

# Create 3 columns and put the image in the middle column
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios as needed
with col2:
    st.image(image_url, caption="Fig. 1: Schematic Drawing of Shaft with Dimensions")

image_url = "https://www.researchgate.net/publication/44220429/figure/download/fig1/AS:670016391356455@1536755764941/Notch-sensitivity-versus-notch-radius-for-steels-and-aluminium-alloys.png"

# Create 3 columns and put the image in the middle column
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios as needed
with col2:
    st.image(image_url, caption="Fig. 2: Notch sensitivity versus notch radius for steels and aluminium alloys")
    st.caption("Note: To find the value for notch radius, r(mm), please refer to this figure. "
               "(The value of notch sensitivity, q, is required)")

image_url = "https://www.engineersedge.com/materials/images/stress-concentration-2.png"

# Create 3 columns and put the image in the middle column
col1, col2, col3 = st.columns([1, 2, 1])  # Adjust ratios as needed
with col2:
    st.image(image_url, caption="Fig. 3: Stress-concentration factor,Kt vs r/d")
    st.caption("Note: Please refer this figure to obtained the value of Kt "
               "(Kt is required to find Kf)")

st.sidebar.header('User Input Parameters')

def user_input_features():
    shaft_diameter_A = st.sidebar.number_input('Shaft Diameter(A), D (mm)', value = 30)
    shaft_diameter_B = st.sidebar.number_input('Shaft Diameter(B), D (mm)', value = 0.01)
    shaft_length = st.sidebar.number_input('Shaft Length, L (mm)', value = 0.01)
    Applied_Force_at_Point_A = st.sidebar.number_input('Applied Force(A), Fa (N)', value = 0.01)
    Applied_Force_at_Point_B = st.sidebar.number_input('Applied Force(B), Fb (N)', value = 0.01)
    Sy = st.sidebar.number_input('Yield Stress, Sy (MPa)', value = 0.01)
    UTS = st.sidebar.number_input('Ultimate Tensile Strength, UTS (MPa)', value = 0.01)
    Length_from_Fa_to_shaft_end = st.sidebar.number_input('Length from Fa to shaft end, Lf (mm)', value = 0.01)
    Length_from_Fb_to_shaft_end = st.sidebar.number_input('Length from Fb to shaft end, Lf (mm)', value = 0.01)
    Constant_a_for_ka = st.sidebar.number_input('Constant a for ka, a', value = 0.00)
    Constant_b_for_ka = st.sidebar.number_input('Constant b for ka, b', value = 0.00)
    Notch_radius = st.sidebar.number_input('Notch radius,r(mm)', value = 0.01)
    Kt = st.sidebar.number_input('Stress concentration factor,Kt', value = 0.01)

    data = {'Da (mm)': shaft_diameter_A,
            'Db (mm)': shaft_diameter_B,
            'L (mm)': shaft_length,   
            'Fa (N)': Applied_Force_at_Point_A,
            'Fb (N)': Applied_Force_at_Point_B,
            'Lfa (mm)': Length_from_Fa_to_shaft_end,
            'Lfb (mm)': Length_from_Fb_to_shaft_end,
            'UTS (MPa)': UTS,
            'Sy (MPa)': Sy,
            'a': Constant_a_for_ka,
            'b': Constant_b_for_ka,
            'r(mm)': Notch_radius,
            'Kt': Stress_concentration_factor,}
           
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

Da=df['Da (mm)'].values.item()
Db=df['Db (mm)'].values.item()
L=df['L (mm)'].values.item()
Fa=df['Fa (N)'].values.item()
Fb=df['Fb (N)'].values.item()
UTS=df['UTS (MPa)'].values.item()
Sy=df['Sy (MPa)'].values.item()
Lfa=df['Lfa (mm)'].values.item()
Lfb=df['Lfb (mm)'].values.item()
a=df['a'].values.item()
b=df['b'].values.item()
r=df['r(mm)'].values.item()
Kt=df['Kt'].values.item()


st.subheader('Nomenclature')
st.markdown("""
- **Da**: Shaft diameter A (Big)
- **Db**: Shaft diameter B (Small)
- **L**: Shaft length
- **F**: Applied force on the shaft
- **Sy**: Shaft material yield stress
- **UTS**: Shaft material Ultimate Tensile Strength
- **Lfa**: Length from force application point A to shaft end
- **Lfb**: Length from force application at point B to shaft end
- **a, b**: Constants for ka calculation
- **r**: Notch radius
- **Kt**: Stress concentration factor
""")

# Calculate Se'
Se_prime = 0.5*UTS

# Calculate ka
ka = a*(UTS**b)

# Calculate kb
def calculate_kb(Da):
    if 7.62 <= Da <= 51:
        return 1.24 * (Da ** -0.107)
    elif 51 < Da <= 254:
        return 1.51 * (Da ** -0.157)
    else:
        return None

kb = calculate_kb(Da)

#Calculate Se

Se = (ka*kb)*Se_prime

#Calculate Neuber Constant(Bending/axial)
def calculate_NC(UTS):
    if 340 <= UTS <= 1700:
        return 1.24 - 2.25e-3*UTS + 1.60e-6*(UTS**2) - 4.11e-10*(UTS**3)
    else:
        return None
    
NC = calculate_NC(UTS)

if NC is not None:
    user_input = {
        'Da (mm)': "{:.2f}".format(Da),
        'Db (mm)': "{:.2f}".format(Db),
        'L (mm)': "{:.2f}".format(L),
        'Lfa (mm)': "{:.2f}".format(Lfa),
        'Lfb (mm)': "{:.2f}".format(Lfb),
        'Fa (N)': "{:.2f}".format(Fa),
        'Fb (N)': "{:.2f}".format(Fb),
        'UTS (MPa)': "{:.2f}".format(UTS),
        'Sy (MPa)': "{:.2f}".format(Sy),
        'NC (√(mm))': "{:.2f}".format(NC),  # only when NC is valid
        'a': "{:.2f}".format(a),
        'b': "{:.2f}".format(b),
        'r(mm)': "{:.2f}".format(r)
    }
else:
    st.error("Cannot calculate NC: UTS must be between 340 MPa and 1700 MPa")
    user_input = {
        'Da (mm)': "{:.2f}".format(Da),
        'Db (mm)': "{:.2f}".format(Db),
        'L (mm)': "{:.2f}".format(L),
        'Lfa (mm)': "{:.2f}".format(Lfa),
        'Lfb (mm)': "{:.2f}".format(Lfb),
        'Fa (N)': "{:.2f}".format(Fa),
        'Fb (N)': "{:.2f}".format(Fb),
        'UTS (MPa)': "{:.2f}".format(UTS),
        'Sy (MPa)': "{:.2f}".format(Sy),
        'a': "{:.2f}".format(a),
        'b': "{:.2f}".format(b),
        'r(mm)': "{:.2f}".format(r)
    }

            
user_input_df=pd.DataFrame(user_input, index=[0])
st.subheader('User Input Parameters')
st.write(user_input_df)



# Calculate Se'
calculated_param={'Se_prime (MPa)': "{:.2f}".format(Se_prime)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Se prime')
st.write(calculated_param_df)

#Calculate ka
calculated_param={'ka': "{:.2f}".format(ka)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated ka')
st.write(calculated_param_df)

#Calculate kb
if kb is not None:
    calculated_param = {'kb': "{:.2f}".format(kb)}
    calculated_param_df = pd.DataFrame(calculated_param, index=[0])
    st.subheader('Calculated kb')
    st.write(calculated_param_df)
else:
    st.error("Cannot calculate kb: Shaft diameter Da must be between 7.62 mm and 254 mm")

#Calculate Se
calculated_param={' Se (MPa)': "{:.2f}".format(Se)}
calculated_param_df=pd.DataFrame(calculated_param, index=[0])
st.subheader('Calculated Se ')
st.write(calculated_param_df)

#Calculate Neuber Constant(Bending/axial)
if NC is not None:
    calculated_param = {'NC(√(mm))': "{:.2f}".format(NC),}
    calculated_param_df = pd.DataFrame(calculated_param, index=[0])
    st.subheader('Calculated Neuber Constant')
    st.write(calculated_param_df)
else:
    st.error("Cannot calculate NC: UTS must be between 340 Mpa and 1700 Mpa")

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
