# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 20:16:32 2023

@author: USR02709
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import requests

def P90_norm(indice,type_stats,Teams_names,columns_stats):
    #1) Normalizzo le Shot Stats
    team=[]
    for df in type_stats:
        indice_divisore= df.loc[df['Unnamed: 0'] == 0].index[0]
        parte1 = df.loc[:indice_divisore-1, :]
        parte2 = df.loc[indice_divisore+1:, :]
        if Teams_names[indice] in list(parte1['Unnamed: 0']):
            team.append(parte1)
        else:
            team.append(parte2)
    
    # Concateniamo i DataFrame nella lista in un unico DataFrame
    team_concatenato = pd.concat(team)
    team_concatenato.index=team_concatenato['Unnamed: 0']
    
    #Trovo la lista di nomi di nomi unici  
    giocatori_team=list(team_concatenato['Unnamed: 0'].unique())
    
    #Modifico la posizione dell'italia nella lista, mettendola alla fine
    giocatori_team.remove(f'{Teams_names[indice]}')
    giocatori_team.insert(len(giocatori_team), f'{Teams_names[indice]}')
    
    #ora creo il ciclo dove per ogni giocatore e per l'Italia creo le stats di tutto il torneo.
    columns_stats_filt=columns_stats.drop(['Unnamed: 0','Substituted','Replaced'])
    Stats_competition_parameters=pd.DataFrame(columns=columns_stats_filt,index=giocatori_team)
    columns_stats_da_normalizzare_p90 = columns_stats[2:-3]
    
    #Calcolo i parametri sommati e normalizzati per ogni squadra e quindi ogni giocatore per tutta la competizione.
    for p in giocatori_team:
        dfp=team_concatenato.loc[p,:]
        if isinstance(dfp, pd.DataFrame):
            dfp=dfp
        elif isinstance(dfp, pd.Series):
            dfp=dfp.to_frame().T
    
        P90_parameters=((dfp[columns_stats_da_normalizzare_p90].sum(axis=0))/sum(dfp['Match_Time']))*90
        Stats_competition_parameters.loc[p,'Match_Time']=sum(dfp['Match_Time'])
        Stats_competition_parameters.loc[p,columns_stats_da_normalizzare_p90]=P90_parameters
        
        #trovo la posizione con più 
        tipe_of_positions=list(dfp['Positions'].unique())
        tipe_of_positions=sorted(tipe_of_positions,reverse=True,key=len)
    
        Stats_competition_parameters.loc[p,'Positions']=tipe_of_positions[0]

    return Stats_competition_parameters