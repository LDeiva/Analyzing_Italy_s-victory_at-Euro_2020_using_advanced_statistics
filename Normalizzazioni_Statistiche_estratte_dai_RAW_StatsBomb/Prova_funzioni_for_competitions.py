# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 16:37:25 2023

@author: hp
"""


import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.colors import to_rgba
from statsbombpy import sb
from mplsoccer import Pitch, FontManager,VerticalPitch, pitch
from mplsoccer.statsbomb import * 
#from mplsoccer.statsbomb import read_event, EVENT_SLUG
import seaborn as sns
from matplotlib.cm import get_cmap
from Plot_Functions import *
import pandas as pd
from Match_and_competitions_information_function import *
import os
"""Funzione per calcolo percentuali"""
def percentage(y, x):
    return 0 if x == 0 else (y / x)*100
"""Creo i vari Excel contenenti i vari parametri"""

"""Apro iterativamente i vari DF per ogni match giocato e Calcolo i parametri per ogni match e li isnerisco nei 5 dataframe"""
#Creo i 6 dataframe


#Creo DF con i match_id e il numeri di match.
data,lenght,dfm=match_information(55,43)
#Trovo il nome delle squadren del torneo
Teams_name=list(dfm['home_team_home_team_name'].unique())
#Indici per mettere nel dataframe in riga 0 la squadra di casa e in indice 1 la squadra ospite
#index=[0,1]
#Inizio il loop dove trovo i df per ogni squadra nella lista la concateno e tiro fuori i dati.
#Per singolo giocatore e team
#for team_name in Teams_name:
#   os.mkdir(rf'C:\Users\hp\OneDrive\Football Analytics\Calcio\Dati e Progetti\Miei Progetti\Dati Progetto Italia Europeo 2020\Parametri_All_Competitions_for_Teams\{team_name}')
team_name='Spain'
teams_matches=[]
opponents_team=[]
#Qui apro i 51 match su cui ogni volta calcolo i parametri e creo i DF con i parametri.
for i in range(lenght):
    
    d=data[i]#Dal dataframe con tutte le chiavi dei match apro il primo.
    if team_name==d['home_team']['home_team_name'] or team_name==d['away_team']['away_team_name']:

        match_id=d['match_id']#Estraggo l'id per aprire il df match. 
        match_week=d['match_week']#Estraggo la week del match. 
    
        """ Apro il Dataframe dal JSON"""
        #Apriamo il File Json con i dati del Match 
        
        with open(rf'C:\Users\hp\OneDrive\Football Analytics\Calcio\Dati e Progetti\Dati\open-data-master\data\events\{match_id}.json', encoding="utf8") as data_file:
            #print (mypath+'events/'+file)
            Data = json.load(data_file)
        
        file_name=str(match_id)+'.json'    
        
        #Trasformiamo i dati da Json a dataframe leggibile da Pandas 
        from pandas.io.json import json_normalize
        df = json_normalize(Data, sep = "_").assign(match_id = file_name[:-5])
        #Li inseriamo nella lista
        teams_matches.append(df)
        if d['home_team']['home_team_name']!=team_name:
           opponents_team.append(d['home_team']['home_team_name'])
        else:
           opponents_team.append(d['away_team']['away_team_name'])
            
#Ora concateno i df e ho il df contenente tutti gli eventi dei giocatori e della squadra.
#Per la competizione.
Teams_competition_events=pd.concat(teams_matches)
Teams_competition_events=Teams_competition_events.reset_index().drop('level_0',axis=1)

shots=Teams_competition_events[((Teams_competition_events['goalkeeper_type_name']=='Shot Saved') | (Teams_competition_events['goalkeeper_type_name']=='Shot Saved to Post') | (Teams_competition_events['goalkeeper_type_name']=='Shot Saved Off T'))]

#g_c_tk=Teams_competition_events[(Teams_competition_events['duel_type_name']=='Tackle') & (Teams_competition_events['player_name']=='Giorgio Chiellini') ]

team_list=list(Teams_competition_events['team_name'].unique())
team_list.remove(team_name)

#GUARDO LE COLONNE NEL DATAFRAME
columns=list(Teams_competition_events.columns)

#Prendo nomi della squadra di casa (home) e in trasferta (away)
h_team=df['team_name'].iloc[0]
a_team=df['team_name'].iloc[1]

#Prendo lista giocatori impiegati nella partita
#Creo lista per giocatori di casa e totale con anche nome squadra
team_df=Teams_competition_events[(Teams_competition_events['team_name']==team_name)]
team_players=list(team_df['player_name'].unique())
team_players = [x for x in team_players if x == x]

#Creo lista per i giocatori in casa e totale con anche nome squadra
team_list=list(team_df['player_name'].unique())
team_list = [x for x in team_list if x == x]
team_list.append(team_name)

#Creo lista con i ruoli per i giocatori di casa.
team_position=team_df[['player_name','position_name']].value_counts().reset_index()
team_position=team_position.groupby('player_name').agg(lambda grp: ', '.join(grp.unique()))
team_position=team_position.loc[team_players,['position_name']]
t_positions=list(team_position['position_name'])
t_positions.append('Team_name')

#Creo lista per i giocatori in trasferta e totale con anche nome squadra
away_df=Teams_competition_events[(Teams_competition_events['team_name']!=team_name)]
away_players=list(away_df['player_name'].unique())
away_players = [x for x in away_players if x == x]

#Creo Lista con nome giocatori trasferta e nome squadra per statistiche totali.
away_list=list(away_df['player_name'].unique())
away_list = [x for x in away_list if x == x]
away_list.append(a_team)

#Creo lista con i ruoli per i giocatori fuori casa.
away_position=away_df[['player_name','position_name']].value_counts().reset_index()
#Nel caso un giocatore abbia due ruoli perchè con le sostituzioni ha cambiato posizione in campo.
#Le unisco in un unica riga separate da una virgola la definizione del ruolo.
#Se no avrei due volte lo stesso giocatore nel df.
away_position=away_position.groupby('player_name').agg(lambda grp: ', '.join(grp.unique()))
away_position=away_position.loc[away_players,['position_name']]
a_positions=list(away_position['position_name'])
a_positions.append('Team_name')

#Creo list per portieri di ogni squadra.
#Home GoalKeeper.
h_g_k_list=Teams_competition_events[(Teams_competition_events['position_name']=='Goalkeeper') & (Teams_competition_events['team_name']==team_name)]
h_g_k_list=list(set(list(h_g_k_list['player_name'])))
#Creo lista con ruolo
h_gk_position=['Goalkeeper' for i in range(len(h_g_k_list))]
h_gk_position.append('Team_name')
#Creo lista con anche il nome della squadra per fare il df con i valori totali del team
t_g_k_list_h=Teams_competition_events[(Teams_competition_events['position_name']=='Goalkeeper') & (Teams_competition_events['team_name']==team_name)]
t_g_k_list_h=list(set(list(t_g_k_list_h['player_name'])))
t_g_k_list_h.append(team_name)

#Away GoalKeeper.
a_g_k_list=Teams_competition_events[(Teams_competition_events['position_name']=='Goalkeeper') & (Teams_competition_events['team_name']!=team_name)]
a_g_k_list=list(set(list(a_g_k_list['player_name'])))
#Creo lista con ruolo
a_gk_position=['Goalkeeper' for i in range(len(a_g_k_list))]
a_gk_position.append('Team_name')
#Creo lista con anche il nome della squadra per fare il df con i valori totali del team
t_g_k_list_a=Teams_competition_events[(Teams_competition_events['position_name']=='Goalkeeper') & (Teams_competition_events['team_name']!=team_name)]
t_g_k_list_a=list(set(list(t_g_k_list_a['player_name'])))
t_g_k_list_a.append(a_team)


#Creo il Dataframe
"""Per mettere i parametri nel dataframe fai così.
Crei la lista con i nomi delle colonne, metti pure nome team e tempo match.
Crei la lista con i valori dei parametri
Poi con Parametri_HomeTeam.loc[valore indice]=lista parametri inserisci la lista
Lo fai per i due team e sei aposto.
Ora l unica cosa da fare è fare l'append deli vari parametri nella lista e aggiongerla con loc nella funzione e sbatterla nel dataframe
per farla per entrambe le squadre usa il for che hai già creato usando t al posto di AwayTeam e HomeTeam.
Dopo dovresti avere i vari excel da salvare
"""
 
from team_offensive_functions import *
from team_defensive_functions import *
from GoalKeeper_functions import *

opgA_list,spgA_list,pgA_list,nonpgA_list,tgA_list=GOL_Conceeded(df,team_players,away_players)

df=Teams_competition_events[(Teams_competition_events['player_name'].isin(away_players)) & (Teams_competition_events['period']<=4)]

#I create df with goal for every player 
goal=df[(df['shot_outcome_name']=='Goal')]
open_play_goal=goal[goal['shot_type_name']=='Open Play']
set_piece_goal=goal[(goal['shot_type_name']=='Corner') | (goal['shot_type_name']=='Free Kick') | (goal['shot_type_name']=='Kick Off')]
penalty_gol=goal[(goal['shot_type_name']=='Penalty')]


opg=len(open_play_goal)

opgA_list=[0 for i in range(len(team_players))]
opgA_list.append(opg)

free_kick_a=Teams_competition_events[(Teams_competition_events['player_name'].isin(away_players)) & (Teams_competition_events['shot_type_name']=='Free Kick')]
spShot=df[(df['type_name']=='Shot') & ((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off'))  & (df['period']<=4)]
spxg=spShot['shot_statsbomb_xg'].sum()

df=Teams_competition_events
#Provo deep pass
Pass=0
indici=[]
Pass_no_cross=df[(df['type_name']=='Pass')  & (df['pass_cross']!=True) & (df['player_name'].isin(team_players))] 
for i in range(len(Pass_no_cross)):
    end_distance=np.sqrt(np.square(120-Pass_no_cross['pass_end_location'].iloc[i][0]) + (np.square(40-Pass_no_cross['pass_end_location'].iloc[i][1])))
    if end_distance<=20:
        Pass+=1
        indici.append(i)


pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(9, 8), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")
plt.gca().invert_yaxis()

# Specifica le coordinate del centro e il raggio del semicerchio
x_center = 120  # Cambia queste coordinate come preferisci
y_center = 40
raggio = 20

# Crea un array di angoli da 0 a π (180 gradi)
angoli = np.linspace(np.pi/2, (3/2)*np.pi, 100)

# Calcola le coordinate x e y del semicerchio
x = x_center + raggio * np.cos(angoli)
y = y_center + raggio * np.sin(angoli)

# Disegna il semicerchio
plt.fill_between(x, y_center, y, color='b') 
for i in indici:
    plt.scatter(Pass_no_cross['pass_end_location'].iloc[i][0],Pass_no_cross['pass_end_location'].iloc[i][1],color='r',s=1)
        
plt.scatter(x=100,y=40,s=20,color='green')
plt.show()

"""Vediamo i clear shot"""
clear_shots_list=[0 for i in range(len(team_players))]

#Filtro il df per i giocatori avversari
df_a=df[(df['player_name'].isin(away_players)) & (df['period']<=4)]

columns=list(df_a.columns)
#List where i put clear shots for every player.

if 'shot_one_on_one' in columns:
    shot=df_a[(df_a['shot_one_on_one']==True) & (df_a['period']<=4)]
    c_s=len(shot)
    clear_shots_list.append(c_s)
else:
    c_s=0
    clear_shots_list.append(c_s)



"""Provo a cercare i gol"""
goal=df_a[(df_a['shot_outcome_name']=='Goal')]
open_play_goal=goal[goal['shot_type_name']=='Open Play']

opg=len(open_play_goal)

"""Provo le deep pass completition"""

    
Pass=0
Successfull_Pass=0
Pass_no_cross=df[(df['type_name']=='Pass')  & (df['pass_cross']!=True) & (df['player_name'].isin(away_players))] 
for i in range(len(Pass_no_cross)):
    end_distance=np.sqrt(np.square(120-Pass_no_cross['pass_end_location'].iloc[i][0]) + (np.square(40-Pass_no_cross['pass_end_location'].iloc[i][1])))
    if end_distance<=20:
        Pass+=1
        if pd.isnull(Pass_no_cross['pass_outcome_name'].iloc[i])==True :
            Successfull_Pass+=1
        
dpca_list.append(Pass)
dspca_list.append(Successfull_Pass)
dsppca_list.append(percentage(dspca_list[-1],dpca_list[-1]))
     