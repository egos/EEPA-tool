import streamlit as st
from streamlit import session_state
import pandas as pd
import numpy as np
import io
from utils import *
from datetime import datetime
import copy
import json
from io import StringIO

# print('-*BEGIN*-')
DateNow= datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
# print(DateNow)

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

lenA = 4
lenB = 4

menutxt = ['Objective']
menutxt+= [f'Q{i+1}' for i in range(lenA + lenB)]
# menutxt+= [f'Q{i+1}' for i in range(10)]
menutxt+= ['Output']

st.sidebar.image("assets/image1.png", use_container_width=True)
st.sidebar.image("assets/image2.png", use_container_width=True)
         
# # Liste des options pour le bouton radio
# options = [f'Q{i}' for i in range(10)]

# initialize session_state dictionnary data = contains all results
if 'data' not in session_state: 
    print('-*session state*-')

    data = Init_data()
    data['idx_menu'] = 0
    data['idx_menu_2'] = "H"
    session_state['data'] = data
else :    
    data = session_state['data']

idx_menu = data['idx_menu']
lenA = data['lenA']
lenB = data['lenB']
dfa = data['dfa'].copy()
dfb = data['dfb'].copy()
dfp = data['dfp'].copy()

# previous & next buttons widget , change value of idx_menu and save in session_state
c1, c2,c3 = st.columns([1,8,1])
if c1.button("⬅️ Previous"): 
    idx_menu-=1
    if idx_menu < 0 : i = 0
    session_state['data']['idx_menu'] = idx_menu
if c3.button("Next ➡️"):
    idx_menu+=1
    if idx_menu >= len(menutxt) -1 : idx_menu = len(menutxt) -1 
    session_state['data']['idx_menu'] = idx_menu

# progress_bar = c2.empty()
perc = sum(1 for i in range(1,lenA + lenB+1) if None not in data['Q' + str(i)])
perc =  int(100* perc / (lenA + lenB))
if perc >= 100 : 
    progress_text = "Completed"
    st.toast('Completed', icon='🎉')
else :
    progress_text = f"{perc/100:.0%}"
c2.progress(perc, text=progress_text)

with st.sidebar: 
    if st.button('Home'):            
        idx_menu = 0
    # with st.expander("question part A", expanded= False) :
    expanded = True if (idx_menu > 0) & (idx_menu < lenA + 1) else False
    ex = st.expander("Question part A", expanded= expanded)    
    for i in range(lenA):
        idx = i        
        c1, c2 = ex.columns(2) 
        # c1.markdown('')
        if c1.button(f"Question {idx+1}", use_container_width=True):
                idx_menu = i+1
        if None not in data['Q' +str(idx+1)] :
                c2.success('Finish')
        else : c2.warning('Pending')
        session_state['data']['idx_menu'] = idx_menu
    expanded = True if (idx_menu > lenA) & (idx_menu < lenB+lenA+1) else False
    ex = st.expander("Question part B", expanded= expanded)    
    for i in range(lenB):
        idx = i+lenA        
        c1, c2 = ex.columns(2) 
        # c1.markdown('')
        if c1.button(f"Question {i+1}",key = {f"Q{i+ lenA +1}"} , use_container_width=True):
                idx_menu = i+lenA+1
        if None not in data['Q' +str(i+lenA +1)] :
                c2.success('Finish')
        else : c2.warning('Pending')
        session_state['data']['idx_menu'] = idx_menu

    if st.button('Output'):
        idx_menu = lenA +lenB + 1
        session_state['data']['idx_menu'] = idx_menu


    session_state['data']['idx_menu'] = idx_menu

if idx_menu == 0:
    st.subheader("Home")
    with open("assets/disclaimer.md", 'r') as file:    
        TEXT = file.read()
        st.markdown(TEXT)
          
if (idx_menu > 0) & (idx_menu < lenA + 1):
    dfa = data['dfa'].copy()
    Qn = idx_menu
    Qdata = data['Q' +str(idx_menu)]
    st.subheader('Part A , Question ' +str(Qn))
    dfa2 = dfa.loc[Qn]
    Title = dfa2[dfa2.Level == 1].Content.iloc[0]
    Qlist = dfa2[dfa2.Level == 2].Content.tolist()

    pn = dfa2["Pillar"].iloc[0]
    Pillar_List = dfp.loc[pn].tolist()

    c = st.columns([0.3,0.7])
    c[0].write(f"**{Pillar_List[0]}**")
    c[1].write(Pillar_List[1])
    c = st.columns([0.8,0.2])
    c[0].write(f"**Question**") 
    c[1].write('Response :')  
    # st.write(f"**{Title}**")   
    Letters = list('abcde')  

    i = 0 
    print(Qdata)

    for idx, row in dfa2.iterrows():
        c = st.columns([0.01,0.8,0.2])
        Pillar , Level , Content , Reponse = row.tolist()
        # c[0].write("{}. {}".format(Letters[i], Qlist[i]))
        c[1].write(Content)

        if (Reponse == "yes/no") or (Reponse == "other"): 
            r = c[2].segmented_control(
                            label=Content,
                            default = Qdata[i],
                            options = ['yes','no'],
                            label_visibility = 'collapsed',
                            key="segmented_control " + Content 
                            )
            st.write('')
            Qdata[i] = r
            session_state['data'] = data
            i+=1      
        if Reponse == "text":
            r = st.text_area(label=Content,
                               value = Qdata[i],
                               label_visibility = 'collapsed',
                               key = "text_area " + Content)  
            st.write('')
            Qdata[i] = r
            session_state['data'] = data
            i+=1   
        # if Reponse == "other": 
        #      pass                   
    st.divider()            
    # print(sum([1 if r is not None else 0 for r in data['Q1']]))
    txt = st.text_area("Please add any additional information here","",key = "text_area" + str(idx_menu + i) )

elif (idx_menu > lenA) & (idx_menu < lenA+lenB + 1):
    Qn = idx_menu-lenA
    Qdata = data['Q' +str(idx_menu)]
    st.subheader('Part B , Question ' +str(Qn))

    Qlist = dfb.loc[Qn,[1,2,3,4,5]].tolist()
    pn = dfb.loc[Qn,"Pillar"]
    Pillar_List = dfp.loc[pn].tolist()
    Definition = dfb.loc[Qn,"Definition"]
    Title = dfb.loc[Qn,"Title"]

    Qlist2= [
         "Please select the sentence that best describes your current level.",
         "Please select the sentence that best describes your aspirational level (in 3-5 years)."
            ]

    c = st.columns([0.3,0.7])
    c[0].write(f"**{Pillar_List[0]}**")
    c[1].write(Pillar_List[1])

    st.write(f"**{Definition}**")
    st.write(f"**{Title}**")

    md_list = "\n".join(f"{i}. {txt}" for i, txt in enumerate(Qlist, start=1))
    st.markdown(md_list)

    c = st.columns([0.7,0.3])
    c[1].write('Response :') 
    
    for i, Q in enumerate(Qlist2):
        c = st.columns([0.7,0.3])
        c[0].write(Q)
        r = c[1].segmented_control(label=Q,
                                   default = Qdata[i],
                                   options = list(range(1,6)),
                                   label_visibility = 'collapsed',
                                   key="segmented_control" + str(2**idx_menu) + " " +str(2**i))
        st.write('')
        Qdata[i] = r
        session_state['data'] = data

if idx_menu  == lenA +lenB + 1:
     st.subheader('Output')
     tabs = st.tabs(["OUTPUT-Part B Scorecard", "Output P1", "Output P2"])     
     tabs[0].image("assets/SC1.png", use_container_width=True, )
     tabs[1].image("assets/SC2.png", use_container_width=True, )
     tabs[2].image("assets/SC3.png", use_container_width=True, )

print('idx_menu' , idx_menu)
# print(dfb)
# print(session_state['data'])
# for k,v in session_state['data'].items():
#      if 'Q' in k:
#           print(k,v)