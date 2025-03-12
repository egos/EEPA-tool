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

ImportNameList = ['Input_Parameters', 'Input_data' , 'Lookup_IDAyear' , 'Lookup_InArrear']

# CSS to inject contained in a string 
# Inject CSS with Markdown for hide_dataframe_row_index
# hide_dataframe_row_index = """<style>.row_heading.level0 {display:none}.blank {display:none}</style>"""
# st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

menutxt = ['Objective']
menutxt+= [f'Q{i+1}' for i in range(10)]
menutxt+= ['Output']

st.sidebar.image("assets/image1.png", use_container_width=True)
st.sidebar.image("assets/image2.png", use_container_width=True)
            
# Liste des options pour le bouton radio
options = [f'Q{i}' for i in range(10)]


# initialize session_state dictionnary data = contains all results
if 'data' not in session_state: 
    print('-*session state*-')
    data = {}    
    data['idx_menu'] = 0
    for i in range(10):
        data['Q' +str(i+1)] = [None] * 4
    session_state['data'] = data
else :    
    data = session_state['data']

idx_menu = data['idx_menu']
idx_menu_save = int(idx_menu)


save_name = 'EEPA_'+DateNow +'.json'
# pour charger qu'une fois la save grace a GPTo
def load_json():
    uploaded_file = st.session_state["uploaded_json"]
    if uploaded_file is not None:
        # bytes_data = uploaded_file.getvalue()
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        data = json.loads(stringio.read())
        session_state['data'] = data

c1, c2 = st.columns(2)
c1.download_button(label ='📥 {}'.format('Save'),
                        data = json.dumps(data),
                        file_name= save_name,
                        use_container_width=True) 
 
uploaded_file = c2.file_uploader('text',
                                  type  = "json",
                                  on_change = load_json,
                                  key="uploaded_json",
                                  label_visibility = 'collapsed' )

# previous & next buttons widget , change value of idx_menu and save in session_state
with st.sidebar: 
    c1, c2 = st.columns(2)
    if c1.button("previous"): 
        idx_menu-=1
        if idx_menu < 0 : i = 0

    if c2.button("next"):
        idx_menu+=1
        if idx_menu >= len(menutxt) -1 : idx_menu = len(menutxt) -1 

    if st.button('Objective'):
        idx_menu = 0
    session_state['data']['idx_menu'] = idx_menu
    # choice = st.selectbox('options', menutxt)
    # idx_menu = menutxt.index(choice)
    # print(choice)

    with st.expander("PartA", expanded= True) :
        # cols = st.columns(2) 
        # for i in range(10):
        #     if cols[i%2+1].button(f"Q{i+1}", use_container_width=True):
        #         idx_menu = i+1
        #         session_state['data']['idx_menu'] = idx_menu
        # c1, c2 = st.columns(2) 
        for i in range(10):
            c1, c2 = st.columns(2) 
            if c1.button(f"Q{i+1}", use_container_width=True):
                idx_menu = i+1
                session_state['data']['idx_menu'] = idx_menu
            if i == 0 :
                perc = 100* sum([1 if r is not None else 0 for r in data['Q1']]) / 4
                perc = int(perc)
                c2.write('{}%'.format(perc))
            else : 
                c2.write('0%')
    if st.button('Output'):
        idx_menu = 11
        session_state['data']['idx_menu'] = idx_menu


session_state['data']['idx_menu'] = idx_menu

# sidebar checkbox widget color
# for i, MenuTitle in enumerate(menu_list): 
#     if i < idx_menu : st.sidebar.write(":green[{}]".format(MenuTitle))
#     elif i == idx_menu : st.sidebar.write(":blue[{}]".format(MenuTitle))
#     else : st.sidebar.write("{}".format( MenuTitle))

# tabs = ['Objective','PartA','PartB','Output']
# tab = st.tabs(tabs)

# uploaded_file = st.file_uploader("Choisissez un fichier Markdown", type=["txt", "md"])
# content = load_markdown_file(uploaded_file)

# print(100*int(idx_menu/len(menutxt)))

st.progress(int(100*idx_menu/len(menutxt)), text='Global progress / Current : '+ menutxt[idx_menu])

# st.write(menutxt[idx_menu])

if idx_menu == 0:
    with open("assets/disclaimer.md", 'r') as file:    
        TEXT = file.read()
        st.markdown(TEXT)
elif idx_menu == 1:
    Qlist = ['a.     Assets are owned centrally',
             'b.     Assets are managed centrally',
             'c.     Assets are owned at relevant line ministry level',
             'd.     Assets are managed at relevant line ministry level'
             ]
    c = st.columns([0.8,0.2])
    c[0].write('Pillar 1: Institutional Readiness')
    txt = 'Are public assets owned and administered centrally (e.g., via MoF) or are assets owned and administered' \
    ' at the relevant line ministry level (e.g., MoE owns and manages schools assets)?	'
    c[0].write(txt)
    c[1].write('Response :')
    
    for i, Q in enumerate(Qlist):
        c = st.columns([0.8,0.2])
        c[0].write(Qlist[i])
        r = c[1].segmented_control(label=Q,default = data['Q1'][i],options = ['yes','no'], label_visibility = 'collapsed', key=i)
        st.write('')
        # print(r)
        # if r is not None : 
        data['Q1'][i] = r
        session_state['data'] = data
    print(sum([1 if r is not None else 0 for r in data['Q1']]))

    txt = st.text_area(
    "Please add any additional information here",
    "",
    # label_visibility= 'hidden'
    )

    