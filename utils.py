import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

def Init_data():
    data = {}    
    data['idx_menu'] = 0
    Dict_Content = pd.read_excel("EEPA_content.xlsx", sheet_name= None)

    dfp=  Dict_Content['Pillars'].set_index('idx')
    dfa = Dict_Content['Part_A'].set_index('Q') #.assign(Res=np.NaN)
    dfb = Dict_Content['Part_B'].set_index('Q') #.assign(Res=np.NaN)

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
                data['Q' +str(i+1)] = np.random.randint(1, 6, size=2) #[None] * 2

    
    
    return data


def plot_output2(df, Pillar):
    cats = df.category.unique()
    colors = {"Current":"steelblue", "Aspirational":"darkorange"}


    # 2) Créez vos subplots
    fig = make_subplots(
        rows=len(cats), cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        subplot_titles=[""]*len(cats)
    )

    # 3) Tracez les barres et mettez le titre Y=cat à chaque rangée
    for i, cat in enumerate(cats, start=1):
        dfi = df[df.category==cat]
        # Barres empilées
        fig.add_trace(go.Bar(
            x=dfi["Current"], y=dfi["question"],
            orientation="h", marker_color=colors["Current"],
            name="Current" if i==1 else None,
            showlegend=(i==1)
        ), row=i, col=1)
        fig.add_trace(go.Bar(
            x=dfi["Aspirational"], y=dfi["question"],
            orientation="h", marker_color=colors["Aspirational"],
            name="Aspirational" if i==1 else None,
            showlegend=(i==1)
        ), row=i, col=1)

        # Inversion pour que la 1ʳᵉ question soit en haut
        fig.update_yaxes(
            categoryorder="array",
            categoryarray=dfi["question"][::-1],
            automargin=True,
            row=i, col=1
        )

        # Le seul “titre Y” qu’on utilise : le nom de la section
        fig.update_yaxes(
            title_text=cat,
            title_standoff=40,             # espace entre le texte et les labels
            title_font=dict(size=14),
            row=i, col=1
        )

    # 4) Layout général
    fig.update_layout(
        height=900,
        barmode="stack",
        title=Pillar,
        margin=dict(l=220, r=40, t=100, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    # On ne veut “Level” que sous le dernier subplot
    for i in range(1,5):
        fig.update_xaxes(title_text="", row=i, col=1)
    fig.update_xaxes(
        title_text="Level", tick0=0, dtick=1, range=[0,5],
        row=4, col=1
    )

    return fig