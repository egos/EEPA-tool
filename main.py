import streamlit as st
from streamlit import session_state
import pandas as pd
import numpy as np
import io
# from utils import *
from datetime import datetime
import copy
import json
from io import StringIO





# print('-*BEGIN*-')
DateNow= datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
print(DateNow)

version = "2025-03-12"
st.set_page_config(page_title = "EEPA tool" +version, layout="wide", page_icon="🌐")

st.markdown(
    """    <style>
    div.stButton > button {
        border-radius: 4px;
        padding: 14px 5px;
    }
    </style>    """,
    unsafe_allow_html=True
)

LenA = 3
LenB = 3

menutxt = ['Objective']
menutxt+= [f'Q{i+1}' for i in range(LenA + LenB)]
# menutxt+= [f'Q{i+1}' for i in range(10)]
menutxt+= ['Output']

st.sidebar.image("assets/image1.png", use_container_width=True)
st.sidebar.image("assets/image2.png", use_container_width=True)
            
# # Liste des options pour le bouton radio
# options = [f'Q{i}' for i in range(10)]

# initialize session_state dictionnary data = contains all results
if 'data' not in session_state: 
    print('-*session state*-')
    data = {}    
    data['idx_menu'] = 0
    for i in range(LenA + LenB):
        if i < LenA : 
             data['Q' +str(i+1)] = [None] * 4
        else : 
             data['Q' +str(i+1)] = [None] * 2
    session_state['data'] = data
else :    
    data = session_state['data']
# print(len(data))
idx_menu = data['idx_menu']
idx_menu_save = int(idx_menu)

# previous & next buttons widget , change value of idx_menu and save in session_state
c1, c2,c3 = st.columns([1,8,1])
if c1.button("⬅️ previous"): 
    idx_menu-=1
    if idx_menu < 0 : i = 0
    session_state['data']['idx_menu'] = idx_menu
if c3.button("next ➡️"):
    idx_menu+=1
    if idx_menu >= len(menutxt) -1 : idx_menu = len(menutxt) -1 
    session_state['data']['idx_menu'] = idx_menu
# progress_bar = c2.empty()
perc = sum(1 for i in range(1,LenA + LenB+1) if None not in data['Q' + str(i)])
perc =  int(100* perc / (LenA + LenB))
if perc >= 100 : 
    progress_text = "Completed"
    #  st.toast('Completed', icon='🎉')
else :
    progress_text = f"{perc/100:.0%}"
c2.progress(perc, text=progress_text)


ListA = data['Q1'][:LenA]
ListB = data['Q1'][LenA : LenA+LenB]

with st.sidebar: 
    if st.button('Home'):            
        idx_menu = 0
    # with st.expander("question part A", expanded= False) :
    expanded = True if (idx_menu > 0) & (idx_menu < LenA + 1) else False
    ex = st.expander("question part A", expanded= expanded)    
    for i in range(LenA):
        idx = i        
        c1, c2 = ex.columns(2) 
        # c1.markdown('')
        if c1.button(f"Question {idx+1}", use_container_width=True):
                idx_menu = i+1
        if None not in data['Q' +str(idx+1)] :
                c2.success('finish')
        else : c2.warning('pending')
        session_state['data']['idx_menu'] = idx_menu
    expanded = True if (idx_menu > LenA) & (idx_menu < LenB+LenA+1) else False
    ex = st.expander("question part B", expanded= expanded)    
    for i in range(LenB):
        idx = i+LenA        
        c1, c2 = ex.columns(2) 
        # c1.markdown('')
        if c1.button(f"Question {i+1}",key = {f"Q{i+ LenA +1}"} , use_container_width=True):
                idx_menu = i+LenA+1
        if None not in data['Q' +str(i+LenA +1)] :
                c2.success('finish')
        else : c2.warning('pending')
        session_state['data']['idx_menu'] = idx_menu

    if st.button('Output'):
        idx_menu = LenA +LenB + 1
        session_state['data']['idx_menu'] = idx_menu


    session_state['data']['idx_menu'] = idx_menu

if idx_menu == 0:
    st.subheader("Home")
    with open("assets/disclaimer.md", 'r') as file:    
        TEXT = file.read()
        st.markdown(TEXT)
          

if (idx_menu > 0) & (idx_menu < LenA + 1):
    Qn = idx_menu
    Qdata = data['Q' +str(idx_menu)]

    st.subheader('Part A , Question ' +str(Qn))

    Qlist = ['a.     Assets are owned centrally',
             'b.     Assets are managed centrally',
             'c.     Assets are owned at relevant line ministry level',
             'd.     Assets are managed at relevant line ministry level'
             ]
    txt = 'Are public assets owned and administered centrally (e.g., via MoF) or are assets owned and administered' \
    ' at the relevant line ministry level (e.g., MoE owns and manages schools assets)?	'

    c = st.columns([0.8,0.2])
    c[0].write('Pillar 1: Institutional Readiness')
    c[0].write(txt)
    c[1].write('Response :')        
    for i, Q in enumerate(Qlist):
        c = st.columns([0.8,0.2])
        c[0].write(Qlist[i])
        r = c[1].segmented_control(label=Q,default = Qdata[i],options = ['yes','no'], label_visibility = 'collapsed', key="segmented_control" + str(2**idx_menu)  + " " + str(2**i) )
        st.write('')
        Qdata[i] = r
        session_state['data'] = data
    # print(sum([1 if r is not None else 0 for r in data['Q1']]))
    txt = st.text_area("Please add any additional information here","",key = "text_area" + str(idx_menu + i) )

elif (idx_menu > LenA) & (idx_menu < LenA+LenB + 1):
    Qn = idx_menu-LenA
    Qdata = data['Q' +str(idx_menu)]
    st.subheader('Part B , Question ' +str(Qn))
    Qlist = [
    "1. There is no clear understanding about the pros and cons of an insurance program.",
    "2. The pros and cons of an insurance program have been documented but there is minimal financial or benefits analysis.",
    "3. The pros and cons of an insurance program have been documented together with some financial or benefits analysis.",
    "4. The pros and cons of an insurance program have been documented together with some financial or benefits analysis." \
        " These benefits are described in SMART format and are a key part of policy and benefits design.",
    "5. The pros and cons of an insurance program have been documented together with some financial or benefits analysis." \
         " These benefits are described in SMART format and are a key part of policy and benefits design. Benefits are regularly and independently benchmarked against expectations."
    ]

    Qlist2= [
         "Please select the sentence that best describes your current level.",
         "Please select the sentence that best describes your aspirational level (in 3-5 years)."
            ]

    c = st.columns([0.8,0.2])
    c[0].write('Pillar 1: Institutional Readiness')
    st.write("Has the government assessed the benefits of an insurance program?")

    for i, Q in enumerate(Qlist):
         st.write(Qlist[i])

    c = st.columns([0.7,0.3])
    # c[0].write('Pillar 1: Institutional Readiness')
    # c[0].write(txt)
    c[1].write('Response :') 
    
    for i, Q in enumerate(Qlist2):
        c = st.columns([0.7,0.3])
        c[0].write(Q)
        r = c[1].segmented_control(label=Q,default = Qdata[i],options = list(range(1,6)), label_visibility = 'collapsed', key="segmented_control" + str(2**idx_menu) + " " +str(2**i) )
        st.write('')
        Qdata[i] = r
        session_state['data'] = data
if idx_menu  == LenA +LenB + 1:
     st.subheader('Output')
     tabs = st.tabs(["OUTPUT-Part B Scorecard", "Output P1", "Output P2"])     
     tabs[0].image("assets/SC1.png", use_container_width=True, )
     tabs[1].image("assets/SC2.png", use_container_width=True, )
     tabs[2].image("assets/SC3.png", use_container_width=True, )

print(idx_menu,data)