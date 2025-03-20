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


# CSS to inject contained in a string 
# Inject CSS with Markdown for hide_dataframe_row_index
# hide_dataframe_row_index = """<style>.row_heading.level0 {display:none}.blank {display:none}</style>"""
# st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


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
# st.write(menutxt[idx_menu])