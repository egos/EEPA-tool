import streamlit as st
import pandas as pd
import numpy as np

def Init_data():
    data = {}    
    data['idx_menu'] = 0
    Dict_Content = pd.read_excel("EEPA_content.xlsx", sheet_name= None)

    dfp=  Dict_Content['Pillars'].set_index('idx')
    dfa = Dict_Content['Part_A'].set_index('Q') #.assign(Res=np.NaN)
    dfb = Dict_Content['Part_B'][:3].set_index('Q')  #.assign(Res=np.NaN)

    lenA = dfa.index.nunique()
    lenB = dfb.index.nunique()

    data= dict(
        dfa = dfa,
        dfb = dfb,
        dfp = dfp, 
        lenA = lenA,
        lenB = lenB, 
        lenTot = lenA + lenB
    )

    dfaSize = dfa[dfa.Reponse.notnull()].groupby('Q').size()
    
    for i in range(lenA + lenB):
        if i < lenA : 
                data['Q' +str(i+1)] = [None] * dfaSize.loc[i+1]
        else : 
                data['Q' +str(i+1)] = [None] * 2

    
    
    return data

