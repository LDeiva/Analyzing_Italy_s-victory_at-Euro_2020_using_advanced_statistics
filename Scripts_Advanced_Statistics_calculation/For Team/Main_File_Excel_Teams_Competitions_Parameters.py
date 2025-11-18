# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 21:50:52 2023

@author: hp
"""

# -*- coding: utf-8 -*-

"""
IN QUESTO SCRIPT APRIAMO I JASON E CHIAMIAMO LE FUNZIONI 
PER CALCOLARE I PARAMETRI DELLE SQUADRE E CREARE GLI EXCEL PER OGNI MATCH.
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
path=rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Miei Progetti\Prova dati euro 2020\Group Stage'
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
for team_name in Teams_name:
    os.mkdir(rf'{path}\{team_name}')
    team_name='Italy'
    teams_matches=[]
    opponents_team=[]
    #Qui apro i 51 match su cui ogni volta calcolo i parametri e creo i DF con i parametri.
    for i in range(lenght):
        
        d=data[i]#Dal dataframe con tutte le chiavi dei match apro il primo.
        match_week=d['match_week']
        if team_name==d['home_team']['home_team_name'] or team_name==d['away_team']['away_team_name']:

            match_id=d['match_id']#Estraggo l'id per aprire il df match. 
            match_week=d['match_week']#Estraggo la week del match. 
            if match_week<=3:

                """ Apro il Dataframe dal JSON"""
                #Apriamo il File Json con i dati del Match 
                
                with open(rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Dati\open-data-master\data\events\{match_id}.json', encoding="utf8") as data_file:
                    #print (mypath+'events/'+file)
                    Data = json.load(data_file)
                
                file_name=str(match_id)+'.json'    
                
                #Trasformiamo i dati da Json a dataframe leggibile da Pandas 
                from pandas import json_normalize
                df = json_normalize(Data, sep = "_").assign(match_id = file_name[:-5])
                #Li inseriamo nella lista
                teams_matches.append(df)

            
                if d['home_team']['home_team_name']!=team_name:
                   opponents_team.append(d['home_team']['home_team_name'])
                else:
                   opponents_team.append(d['away_team']['away_team_name'])
            else:
                continue
   
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
    #team_position=team_position.groupby('player_name').agg(lambda grp: ', '.join(grp.unique()))
    team_position = team_position.groupby('player_name').agg(lambda grp: ', '.join(grp.astype(str).unique()))

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
    #away_position=away_position.groupby('player_name').agg(lambda grp: ', '.join(grp.unique()))
    away_position = away_position.groupby('player_name').agg(lambda grp: ', '.join(grp.astype(str).unique()))

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
    
    #Trovo il Time
    Times=Time(teams_matches,team_list,team_name)
    
        
    """"1)Calcoliamo le funzioni Dei Tiri e Goal fatti dalla squadra offendente"""
    
    #Statistiche per Home team
    
    #1)Calcola vari tipi di Xg e Shots prodotti dalla squadra che attacca.
    opXG,opXGs,spXG,spXGs,pXG,nptXG,nptXGs,tXG,tXGs=XG_for_player(Teams_competition_events,team_players)
    
    #2)calcolo i tiri effettuati.
    ops,sps,ps,nps,ts=Shots_for_player(Teams_competition_events,team_players)
    
    #3)calolo i tiri in porta effettuati.
    s_ot_op,s_ot_sp,s_ot_p,s_ot_nop,tot_s_ot=shot_on_targhet_for_player(Teams_competition_events,team_players,a_team)
    
    #4)Calcolo la shot lenght
    m_s_l=Shots_lenght_for_player(Teams_competition_events,team_players)
    
    #5)Calcolo i tiri fatti in area e fuori
    inside_list,outside_list=Out_and_In_shots_for_player(Teams_competition_events,team_players)
    
    #6)Calcolo con che parte del corpo è stata fatto il tiro e l'eventuale gol
    fs_list,fg_list,hs_list,hg_list,ds_list,dg_list=Shot_type_for_player(Teams_competition_events,team_players)
    
    #7)Calcolo Goal in OP,SP,Penalty ecc.
    opg_list,spg_list,pg_list,nonpg_list,tg_list=GOL_for_player(Teams_competition_events,team_players)
    
    #8)alcolo i rigori effettuati
    n_p_list,s_p_list,b_p_list,f_p_list=Penalty_for_player(Teams_competition_events,team_players)
    
    #9)Calcolo le punizioni per i giocatori
    f_k_list,f_k_g_list=Free_kick_for_player(Teams_competition_events,team_players)
    
    #10)calcolo i clear shots, cioè tiri con solo il portiere tra la porta e il tiratore
    c_s_list=clear_shots_for_player(Teams_competition_events,team_players)
    
    #11)Calcolo i Shot Touch %, non considero i rigori quindi solo i non penalty shots uso.
    #Calcolo i tocchi totali, non li metto in sto df, ma in quello dopo, li calcolo anche qui per calcolare sto paramentro.
    player_touch_list=Touches_for_players(Teams_competition_events,team_players)
    s_t_perc=[percentage(a,b) for a,b in zip(nps,player_touch_list)]

    
    parameters_list_Shots_and_Goal_home=[t_positions,opXG,opXGs,spXG,spXGs,pXG,nptXG,nptXGs,tXG,tXGs
                                        ,ops,sps,ps,nps,ts,
                                        s_ot_op,s_ot_sp,s_ot_p,s_ot_nop,tot_s_ot,
                                        m_s_l,inside_list,outside_list,
                                        fs_list,fg_list,hs_list,hg_list,ds_list,dg_list,
                                        opg_list,spg_list,pg_list,nonpg_list,tg_list,
                                        n_p_list,s_p_list,b_p_list,f_p_list,
                                        f_k_list,f_k_g_list,c_s_list,s_t_perc,Times['Time']]
    
    parameters_name_Shots_and_Goals=['Positions','opXG','opXGs','spXG','spXGs','pXG','npXG','npXGs','tXG','tXGs',
                                     'opShots','spShots','pShots','npShots','tShots',
                                     'opShots_On_Targhet','spShots_On_Targhet','pShots_on_Targhet','npShots_On_Targhet','tShots_On_Targhet',
                                     'Mean_Shots_Lenght','Inside_Shots','Outside_Shots',
                                     'Foot_Shots','Foot_Gol','Head_Shots','Head_Gol','Dribling_Shots','Dribbling_Goal',
                                     'opGol','spGol','pGol','npGol','tGol',
                                     'Penalty_Kick','Scored_Penalty','Blocked_Penalty','Failed_Penalty',
                                     'Free_Kicks_Numbers','Free_Kicks_Goals','Clear_Shots','Shot_Touch_%','Times']
    
    #Faccio il df
    Parameters_Shots_and_Goals_home=pd.DataFrame( list(zip(*parameters_list_Shots_and_Goal_home)),columns=parameters_name_Shots_and_Goals,index=team_list)  
    Parameters_Shots_and_Goals_home.insert(0, 'Player_Name', Parameters_Shots_and_Goals_home.index)

   
    Parameters_Shots_and_Goals_home.to_excel(rf'{path}\{team_name}\Shots_Stats.xlsx',index=False)
   
    """2)Calcolo le Statistiche dei Passaggi"""
    #Calcolo parametri per Home Team
    
    #1)Calcolo i passaggi.
    pass_list,succ_pass_list,perc_pass_list,mean_pass_dist_list=Passes_for_player(Teams_competition_events,team_players)
    
    #2)calcolo passaggi sotto pressione
    passes_under_pressure_list,succesfull_passes_under_pressure_list,perc_succesful_passes_under_pressure_list=passes_under_pressure(Teams_competition_events,team_players)
    
    #3)Calcolo i passaggi nell'ultimo terzo di campo, quelli in avanti sempre nell'ultimo terzo di campo.
    pass_in_f_t,succesfull_pass_in_f_t,succesfull_pass_in_f_t_percentage,pass_in_f_t_forward,succesfull_pass_in_f_t_forward,succesfull_pass_in_f_t_percentage_forward,pass_in_f_t_forward_percentage=Passes_in_Final_Third(Teams_competition_events,team_players)
   
    
    #3)Calcolo i passaggi nelle varie zone del campo
    d_tq_p_list,s_d_tq_p_list,p_d_tq_p_list,md_tq_p_list,s_md_tq_p_list,p_md_tq_p_list,mo_tq_p_list,s_mo_tq_p_list,p_mo_tq_p_list,o_tq_p_list,s_o_tq_p_list,p_o_tq_p_list=Passes_zones_for_player(Teams_competition_events,team_players)
    
    #4)Calcolo i progressive passes
    p_p_list,s_p_p_list,p_p_p_list,p_d_list,m_p_d_list=Progressive_Passes(Teams_competition_events,team_players)
    
    #5)Calcolo i tipi di passaggi effettuati
    s_p_list,s_s_p_list,p_s_p_list,m_p_list,s_m_p_list,p_m_p_list,l_p_list,s_l_p_list,p_l_p_list,l_p_up_list,s_l_p_up_list,p_l_p_up_list,l_p_unp_list,s_l_p_unp_list,p_l_p_unp_list,t_p_list,s_t_p_list,p_t_p_list=Passes_type_for_player(Teams_competition_events,team_players)
    
    #6)Calcolo i passaggi chiave
    k_p_list=key_passes_for_player(Teams_competition_events,team_players)
    
    #7)Passaggi chiave sotto pressione
    u_p_k_p_list=key_passes_under_pressure(Teams_competition_events,team_players)
    
    #8)Calcolo i passaggi filtranti
    t_b_list,s_t_b_list,p_t_b_list=Through_Ball_for_player(Teams_competition_events,team_players)
    
    #9)Calcolo i passaggi filtrant sotto pressione
    u_p_t_b_list,u_p_s_t_b_list,u_p_p_t_b_list=Through_Ball_under_pressure(Teams_competition_events,team_players)
    
    #10)Calcolo i cambi di gioco
    scambi_list,succesfull_scambi_list,percentage_succesfull_scambi_list=Scambi_for_player(Teams_competition_events,team_players)
    
    #11)calcolo i corner
    corner_list=Corners_for_player(Teams_competition_events,team_players)
    
    #12)Calcolo i cross
    cross_list,succesfull_cross_list,percentage_succ_cross_list=Cross_for_player(Teams_competition_events,team_players)
    
    #13)calcolo i passaggi e i cross che entrano in area
    p_b_list,s_p_b_list,p_p_b_list,c_b_list,s_c_b_list,p_c_b_list,b_c_percentage_list=Passes_and_cross_into_the_Box_for_player(Teams_competition_events,team_players)
    
    #14)Calcolo i passaggi e i cross in area
    pass_area_list,succ_pass_area_list,perc_succ_pass_area_list=Box_Pass_for_player(Teams_competition_events,team_players)
    
    #15)Calcolo i Deep Pass Completion
    dpc_list,dspc_list,dsppc_list=Deep_Pass_Completions(Teams_competition_events,team_players)
     
    #16)Calcolo i Deep Cross Completion
    dcc_list,dscc_list,dscpc_list=Deep_Cross_Completions(Teams_competition_events,team_players)
       
    #17)Calcolo il numero di rimesse dal fondo
    g_k_list,s_g_k_list,g_k_p_list=goal_kick_for_player(Teams_competition_events,team_players)
    
    #18)Calcolo palle ricevute sotto pressione
    b_r_under_pressure_list,succesfull_b_r_under_pressure,perc_succesfull_b_r_under_pressure=ball_receipt_under_pressure(Teams_competition_events,team_players)
    

    
    

    
    parameters_Passes_home=[t_positions,pass_list,succ_pass_list,perc_pass_list,mean_pass_dist_list,
                                 passes_under_pressure_list,succesfull_passes_under_pressure_list,perc_succesful_passes_under_pressure_list,
                                 pass_in_f_t,succesfull_pass_in_f_t,succesfull_pass_in_f_t_percentage,pass_in_f_t_forward,succesfull_pass_in_f_t_forward,succesfull_pass_in_f_t_percentage_forward,pass_in_f_t_forward_percentage,
                                 d_tq_p_list,s_d_tq_p_list,p_d_tq_p_list,md_tq_p_list,s_md_tq_p_list,p_md_tq_p_list,mo_tq_p_list,s_mo_tq_p_list,p_mo_tq_p_list,o_tq_p_list,s_o_tq_p_list,p_o_tq_p_list,
                                 p_p_list,s_p_p_list,p_p_p_list,p_d_list,m_p_d_list,
                                 s_p_list,s_s_p_list,p_s_p_list,m_p_list,s_m_p_list,p_m_p_list,l_p_list,s_l_p_list,p_l_p_list,l_p_up_list,s_l_p_up_list,p_l_p_up_list,
                                 l_p_unp_list,s_l_p_unp_list,p_l_p_unp_list,t_p_list,s_t_p_list,p_t_p_list,
                                 k_p_list,u_p_k_p_list,t_b_list,s_t_b_list,p_t_b_list,u_p_t_b_list,u_p_s_t_b_list,u_p_p_t_b_list,
                                 scambi_list,succesfull_scambi_list,percentage_succesfull_scambi_list,corner_list,cross_list,succesfull_cross_list,percentage_succ_cross_list,
                                 p_b_list,s_p_b_list,p_p_b_list,c_b_list,s_c_b_list,p_c_b_list,b_c_percentage_list,pass_area_list,succ_pass_area_list,perc_succ_pass_area_list,
                                 dpc_list,dspc_list,dsppc_list,dcc_list,dscc_list,dscpc_list,
                                 g_k_list,s_g_k_list,g_k_p_list,
                                 b_r_under_pressure_list,succesfull_b_r_under_pressure,perc_succesfull_b_r_under_pressure,Times['Time']]
    
    
    parameters_name_Passes=['Positions','Attempted_Passes','Succesfull_Passes','Succesfull_Passes_%','Average_Passes_Distance',
                                 'Attempted_Passes_Under_Pressure','Succesfull_Passes_Under_Pressure','Succesfull_Passes_%_Under_Pressure',
             'Passes_in_Final_Third','Succesfull_Passes_in_Final_Third','Succesfull_Passes_%_in_Final_Third','Passes_Forward_in_Final_Third','Succesfull_Passes_Forward_in_Final_Third','Succesfull_Passes_Forward_%_in_Final_Third','%_of_Forward_Passes_in_Final_Third',
             'LowDefensive_3/4_Attempted_Passes','Succesfull_LowDefensive_3/4_Passes','Succesfull_LowDefensive_3/4_Passes_%',
             'HighDefensive_3/4_Attempted_Passes','Succesfull_HighDefensive_3/4_Passes','Succesfull_HighDefensive_3/4_Passes_%',
             'LowOffensive_3/4_Attempted_Passes','Succesfull_LowOffensive_3/4_Passes','Succesfull_LowOffensive_3/4_Passes_%',
             'HighOffensive_3/4_Attempted_Passes','Succesfull_HighOffensive_3/4_Passes','Succesfull_HighOffensive_3/4_Passes_%',
             'Attempted_Progressive_Passes','Succesfull_Progressive_Passes','Succesfull_Progressive_Passes_%','Progressive_Distance',
             'Mean_Progressive_Distance',
             'Attempted_Short_Passes','Succesfull_Short_Passes','Succesfull_Short_Passes_%',
             'Attempted_Middle_Passes','Succesfull_Middle_Passes','Succesfull_Middle_Passes_%',
             'Attempted_Long_Passes','Succesfull_Long_Passes','Succesfull_Long_Passes_%',
             'Attempted_Long_Passes_Underpressure','Succesfull_Long_Passes_Underpressur','Succesfull_Long_Passes_Underpressur_%',
             'Attempted_Long_Passes_Unpressed','Succesfull_Long_Passes_Unpressed','Succesfull_Long_Passes_Unpressed_%',
             'Attempted_Throw','Succesfull_Throw','Succesfull_Throw_%','Key_Passes','Key_Passes_Under_Pressure',
             'Through_Ball','Succesfull_Through_Ball','Succesfull_Through_Ball_%',
             'Through_Ball_Under_Pressure','Succesfull_Through_Ball_Under_Pressure','Succesfull_Through_Ball_%_Under_Pressure',
             'Attempted_Scambi','Succesfull_Scambi','Succesfull_Scambi_%','Corners',
             'Attempted_Cross','Succesfull_Cross','Succesfull_Cross_%',
             'Passes_Into_Box','Succesfull_Passes_Into_Box','Succesfull_Passes_Into_Box_%','Cross_Into_Box','Succesfull_Cross_Into_Box','Succesfull_Cross_Into_Box_%','Box_Cross_%',
             'Passes_Inside_Box','Succesfull_Passes_Inside_Box','Succesfull_Passes_Inside_Box_%',
             'Deep_Pass_Completion','Succesfull_Deep_Pass_Completion','Succesfull_Deep_Pass_Completion_Percentage','Deep_Cross_Completion','Succesfull_Deep_Cross_Completion','Succesfull_Deep_Cross_Completion_Percentage',
             'Attempted_Goal_Kick','Succesfull_Goal_Kick','Succesfull_Goal_Kick_%',
             'Ball_Receipt_Under_Pressure','Succesfull_Ball_Receipt_Under_Pressure','Succesfull_Ball_Receipt_%_Under_Pressure','Times']
    
    #Faccio il df
    Parameters_Passes_home=pd.DataFrame(list(zip(*parameters_Passes_home)),columns=parameters_name_Passes,index=team_list)  
    Parameters_Passes_home.insert(0, 'Player_Name', Parameters_Passes_home.index)

    
    Parameters_Passes_home.to_excel(rf'{path}\{team_name}\Passes_Stats.xlsx',index=False)


    """"3)Calcolo Statistiche su possesso palla e dominio territoriale"""
    #Calcolo le statistiche per home team 
    #1)calcolo il possesso palla della squadra di casa
    possession_percentage=Possession(Teams_competition_events,team_list)
    #17)Calcolo il Field Tilt
    fild_tilt=Field_Tilt(Teams_competition_events,team_list)
    #2)Calcolo i possessi
    possession_number_list=possession_number(Teams_competition_events,team_list)
    #3)Calcolo i tocchi
    player_touch_list=Touches_for_players(Teams_competition_events,team_players)
    #3)Calcolo i tocchi nell'ultimo terzo
    player_touch_in_final_third_list=Touches_for_players_in_final_third(Teams_competition_events,team_players)    
    #4)calcolo i tocchi in area
    player_touch_in_box_list=Touches_in_box(Teams_competition_events,team_players)
    #5)Calcolo i dribbling
    d_list,s_d_list,s_d_p_list=Dribbling_for_players(Teams_competition_events,team_players)
    #6)Calcolo le portate palla al piede.
    carry_list,lenght_list,mean_lenght_list=Carry_mean_lenght_for_players(Teams_competition_events,team_players)
    #7)calcolo le portate palla al piede progressive
    p_c_list,p_c_d_list,m_p_c_d_list=Progressive_Carries_for_players(Teams_competition_events,team_players)
    #8)Calcolo le portate che fanno portare la palla nella 3/4 offensiva. 
    t_q_c_list=three_quarters_Carries_for_players(Teams_competition_events,team_players)
    #9)calcolo le portate che portano palla dentro l'area
    i_a_c_list=inside_area_Carries_for_players(Teams_competition_events,team_players)
    #10)Calcolo i deep pass completition
    d_p_c=Deep_Progressions(Teams_competition_events,team_players)
    #11)calcolo le posizioni dei giocatori e medie della squadra
    a_c_o_g=Average_center_of_gravity(Teams_competition_events,team_name)
    a_c_o_g = a_c_o_g.reindex(team_list)
    x=list(a_c_o_g['x'])
    y=list(a_c_o_g['y'])
    #12)Calcolo le palle perse
    l_b_d_list,d_l_b_d_list,l_b_m_list,d_l_b_m_list,l_b_di_list,d_l_b_di_list,l_b_e_list,d_l_b_e_list,l_b_list,d_l_b_list=Lost_Balls_for_players(Teams_competition_events,team_players)
    #13)Calcolo i falli subiti
    fouls_won_list=Fouls_Won_for_players(Teams_competition_events,team_players)

    
    Parameters_Team_Ball_Possession_home=[t_positions,possession_percentage,fild_tilt,possession_number_list,player_touch_list,player_touch_in_final_third_list,
                                          player_touch_in_box_list,d_list,s_d_list,s_d_p_list,carry_list,lenght_list,mean_lenght_list,
                                          p_c_list,p_c_d_list,m_p_c_d_list,t_q_c_list,i_a_c_list,d_p_c,x,y,l_b_d_list,d_l_b_d_list,l_b_m_list,d_l_b_m_list,l_b_di_list,d_l_b_di_list,l_b_e_list,d_l_b_e_list,l_b_list,d_l_b_list,
                                          fouls_won_list,Times['Time']]
    
    parameters_name_Ball_Possession=['Positions','Possession_Percentage','Field_Tilt','Possession_Number','Touches','Touches_in_Final_Third','Touches_in_Box',
                                     'Attempted_Dribbling','Succesfull_Dribbling','Succesfull_Dribbling_%',
                                     'Carries_Number','Carries_Distance','Mean_Carries_Distance','Progressive_Carries_Number','Progressive_Carries_Distance',
                                     'Mean_Progressive_Carries_Distance','3/4_Carries','Inside_area_Carries','Deep_Progressions','Average_Position_x','Average_Position_y',
                                     'Lost_Balls_After_Dribbling','Defensive_Lost_Balls_After_Dribbling',
                                     'Lost_Balls_After_Miscontroll','Defensive_Lost_Balls_After_Miscontroll',
                                     'Lost_Balls_After_Tackles','Defensive_Lost_Balls_After_Tackles',
                                     'Lost_Balls_After_Error','Defensive_Lost_Balls_After_Error',
                                     'Total_Lost_Balls','Defensive_Total_Lost_Balls','Foul Won','Times']
    
    #Faccio il df
    Parameters_Possession_home=pd.DataFrame(list(zip(*Parameters_Team_Ball_Possession_home)),columns=parameters_name_Ball_Possession,index=team_list)  
    Parameters_Possession_home.insert(0, 'Player_Name', Parameters_Shots_and_Goals_home.index)

    
    Parameters_Possession_home.to_excel(rf'{path}\{team_name}\Possession_Stats.xlsx',index=False)

    """4)Statistiche Difensive solo per squadra e non per singolo player"""
    from team_defensive_functions import *

    #Faccio per home team
    #Calcolo gli XG,XGs e i tiri concessi
    opXGA,spXGA,pXGA,npXGA,tXGA,opXGsA,spXGsA,npXGsA,tXGsA,opsA,spsA,psA,npsA,tsA=XG_Shots_Conceeded(Teams_competition_events,team_players,away_players)
    
    #Calcolo Tiri in porta concessi
    opSA_on_Targhet,spSA_on_Targhet,pSA_on_Targhet,npSA_on_Targhet,tSA_on_Targhet=Shots_on_targhet_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i tiri in area e fuori area concessi
    inside_conceeded,outside_conceeded=Out_and_In_shots_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo la distanza media dei tiri concessi
    mean_shot_lenghtA=Shots_lenght_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i clear shots concessi
    c_s_A_list=clear_shots_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i gol concessi
    opgA_list,spgA_list,pgA_list,nonpgA_list,tgA_list=GOL_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i Passaggi Concessi
    conceeded_passes,conceeded_success_passes,conceeded_success_passes_perc=Passes_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i corner concessi
    corner_conceeded=Corners_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i tocchi concessi
    Touch_conceeded=Touches_conceeded(Teams_competition_events,team_players,away_players)
    #Tocchi nell'ultimo terz concessi
    Touches_in_final_third_conceeded=Touches_in_final_third_conceeded(Teams_competition_events,team_players,away_players)    
    #Tocchi in area concessi
    touches_box_conceeded=Touches_in_box_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo passaggi e cross che entrano in area e i box cross concessi
    p_b_list,s_p_b_list,p_p_b_list,c_b_list,s_c_b_list,p_c_b_list,b_c_percentage_list=Passes_and_cross_into_the_Box_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i passaggi in area concessi
    pass_area_list,succ_pass_area_list,perc_succ_pass_area_list=Box_Pass_conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo le deep progression concesse
    deep_progression_conceeded=Deep_Progression_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo le progressioni che portano alla propria 3/4 concesse
    t_q_c_conceeded=three_quarters_Carries_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo le progressioni che portano in area concesse
    i_a_c_conceeded=inside_area_Carries_Conceeded(Teams_competition_events,team_players,away_players)
    #Calcolo i Deep Pass e Cross conceeded
    dpca_list,dspca_list,dsppca_list=Deep_Pass_Completions_Conceeded(Teams_competition_events,team_players,away_players)
    dcca_list,dscca_list,dscpca_list=Deep_Cross_Completions_Conceeded(Teams_competition_events,team_players,away_players)
    #1)Calcolo PPDA
    ppda=PPDA(Teams_competition_events,team_list,team_name)
    #2)Calcolo APPDA
    appda=APPDA(Teams_competition_events,opponents_team,team_list)
    aPPDA=[0 for i in range(len(team_list[1:]))]
    aPPDA.append(appda[-1])
    #2)Calcolo Distanza media inteventi difensivi
    add=Average_Defensive_Distance(Teams_competition_events,team_list)
    #Inserisco i parametri
    parameters_list_Defensive_Team_home=[t_positions,opXGA,opXGsA,spXGA,spXGsA,pXGA,npXGA,npXGsA,tXGA,tXGsA,
                                         opsA,spsA,psA,npsA,tsA,
                                         opSA_on_Targhet,spSA_on_Targhet,pSA_on_Targhet,npSA_on_Targhet,tSA_on_Targhet,
                                         inside_conceeded,outside_conceeded,mean_shot_lenghtA,c_s_A_list,
                                         opgA_list,spgA_list,pgA_list,nonpgA_list,tgA_list,
                                         conceeded_passes,conceeded_success_passes,conceeded_success_passes_perc,
                                         corner_conceeded,Touch_conceeded,Touches_in_final_third_conceeded,touches_box_conceeded,
                                         p_b_list,s_p_b_list,p_p_b_list,c_b_list,s_c_b_list,p_c_b_list,b_c_percentage_list,
                                         pass_area_list,succ_pass_area_list,perc_succ_pass_area_list,
                                         deep_progression_conceeded,t_q_c_conceeded,i_a_c_conceeded,
                                         dpca_list,dspca_list,dsppca_list,
                                         dcca_list,dscca_list,dscpca_list,
                                         ppda,aPPDA,add,
                                         Times['Time']]
    
    parameters_name_Defensive_Team=['Positions','opXGA','opXGsA','spXGA','spXGsA','pXGA','npXGA','npXGsA','tXGA','tXGsA',
                                    'opShotsA','spShotsA','pShotsA','npShotsA','tShotsA',
                                    'opShotsA_On_Targhet','spShotsA_On_Targhet','pShotsA_On_Targhet','npShotsA_On_Targhet','tShotsA_On_Targhet',
                                    'Inside_Area_Shots_Allowed','Outside_Area_Shots_Aallowed','Mean_Shots_Lenght_Distance_Allowed','Clear_Shots_Allowed',
                                    'Open_Play_Goal_A','Set_Piece_Goal_A','Penalty_Goal_A','NonPenalty_Goal_A','Total_Goal_A',
                                    'Passes_Allowed','Succesfull_Passes_Allowed','Succesfull_Passes_%_Allowed',
                                    'Corner_Allowed','Touches_Allowed','Touches_in_Final_Third_Allowed','Touches_in_Box_Allowed',
                                    'Passes_Into_Box_Allowed','Succesfull_Passes_Into_Box_Allowed','Succesfull_Passes_Into_Box_Allowed_%','Cross_Into_Box_Allowed','Succesfull_Cross_Into_Box_Allowed','Succesfull_Cross_Into_Box_Allowed_%','Box_Cross_Allowed_%',
                                    'Passes_Inside_Box_Allowed','Succesfull_Passes_Inside_Box_Allowed','Succesfull_Passes_Inside_Box_Allowed_%',
                                    'Deep_Progression_Allowed','Three_Quarters_Carries_Allowed','Inside_Area_Carries_Allowed',
                                    'Deep_Pass_Completion_Allowed','Succesfull_Deep_Pass_Completion_Allowed','Succesfull_Deep_Pass_Completion_Percentage_Allowed',
                                    'Deep_Cross_Completion_Allowed','Succesfull_Deep_Cross_Completion_Allowed','Succesfull_Deep_Cross_Completion_Percentage_Allowed',
                                    'PPDA','APPDA','ADD',
                                    'Times']
    
    
    #Faccio il df
    Parameters_name_Defensive_Team_home=pd.DataFrame( list(zip(*parameters_list_Defensive_Team_home)),columns=parameters_name_Defensive_Team,index=team_list)  
    #Aggiungo colonna coi nomi dei giocatori
    Parameters_name_Defensive_Team_home.insert(0, 'Player_Name', Parameters_name_Defensive_Team_home.index)

    
    Parameters_name_Defensive_Team_home.to_excel(rf'{path}\{team_name}\Defensive_Team_Stats.xlsx',index=False)


    """5) Difesa della porta e tattica difensiva"""
    #Calcolo le stats per home team
    #1)Calcolo pressioni e contropressioni
    p_list,mph_list,cp_list,mcph_list,op_list,op_perc_list=Pressure_and_Counterpressures_for_player(Teams_competition_events,team_players)
    #2)calcolo il numero di palle recuperate
    b_r_list,m_r_h_list=Ball_Recovery_for_player(Teams_competition_events,team_players)
    #3)Calcolo il numero di palle recuperate nella metà campo avversaria
    h_b_r_lista=High_Ball_Recovery_for_player(Teams_competition_events,team_players)
    #4)Calcolo il numero di palle recuperate nella metà campo avversaria
    b_r_f_t_lista=Ball_Recovery_in_Final_Third_for_player(Teams_competition_events,team_players)
    #5)Calcolo il numero di palle recuperate dopo la pressione di un Player.
    p_r_lista=Pressure_Regains(Teams_competition_events,team_players,team_name)
    
    Parametri_Defensive_Stats_home=[t_positions,p_list,mph_list,cp_list,mcph_list,op_list,op_perc_list,
                                    b_r_list,m_r_h_list,h_b_r_lista,b_r_f_t_lista,p_r_lista,Times['Time']]
    
    parameters_name_Defensive_Stats=['Positions','Pressures','Mean_Pressures_Height','Conterpressures',
                                     'Mean_Counterpressures_Height','Offensive_Pressure','Offensive_Pressures_%',
                                     'Balls_Recovered','Mean_Recovery_Height','Offensive_Balls_Recoverd','Final_third_Balls_Recovery','Pressure_Regains','Times']
    
    
    #Faccio il df
    Parameters_Defensive_Stats_home=pd.DataFrame(list(zip(*Parametri_Defensive_Stats_home)),columns=parameters_name_Defensive_Stats,index=team_list)  
    #Aggiungo colonna coi nomi dei giocatori
    Parameters_Defensive_Stats_home.insert(0, 'Player_Name', Parameters_Shots_and_Goals_home.index)

    
    Parameters_Defensive_Stats_home.to_excel(rf'{path}\{team_name}\Defensive_Parameters_Stats.xlsx',index=False)    
    
    
    """6) Calcolo azioni difensive per la squadra"""
    #Faccio per home team
    
    #1)Calcolo i contrasti fatti,vinti e la loro percentuale
    t_n_list,w_t_list,t_w_p_list=Tackles_for_player(Teams_competition_events,team_players)

    #1)Calcolo i contrasti fatti,vinti e la loro percentuale in area
    t_n_i_a_list,w_t_i_a_list,t_w_p_i_a_list=Tackles_for_player_inside_area(Teams_competition_events,team_players)
    
    #2)Calcolo i contrasti fatti,vinti e la loro percentuale per ogni zona del campo.
    d_tq_t_list,s_d_tq_t_list,p_d_tq_t_list,md_tq_t_list,s_md_tq_t_list,p_md_tq_t_list,mo_tq_t_list,s_mo_tq_t_list,p_mo_tq_t_list,o_tq_t_list,s_o_tq_t_list,p_o_tq_t_list=Tackles_zones_for_player(Teams_competition_events,team_players)
        
    #3)Calcolo i contrasti aerei fatti, vinti e la loro percentuale.
    a_l_lista,a_w_lista,t_a_d_lista,a_w_p_lista=Aerel_duels_for_player(Teams_competition_events,team_players)
 
    #3)Calcolo i contrasti aerei fatti, vinti e la loro percentuale in area.
    a_l_i_a_lista,a_w_i_a_lista,t_a_d_i_a_lista,a_w_p_i_a_lista=Aerel_duels_for_player_in_area(Teams_competition_events,team_players)
    
    #4)Calcolo i dribbbling subiti e contrastati.
    dribling_affrontati, dribbling_subiti, dribbling_fermati,dribbling_fermati_perc=Faced_Dribbling_for_player(Teams_competition_events,team_players)
    
    #4)Calcolo i dribbbling subiti e contrastati in area.
    dribbling_affrontati_in_area, dribbling_subiti_in_area, dribbling_fermati_in_area,dribbling_fermati_in_area_perc=Faced_Dribbling_for_player_in_area(Teams_competition_events,team_players)
        
    #5)Calcolo i tiri e passaggi bloccati
    s_b_list,p_b_list=Blocks_for_player(Teams_competition_events,team_players,team_name)

    #5)Calcolo i tiri e passaggi bloccati in area
    s_b_i_a_list,p_b_i_a_list=Blocks_for_player_in_area(Teams_competition_events,team_players,team_name)
    
    #6)Calcolo gli Intercetti
    int_lista,s_i_lista,p_s_i_list=Interceptions_for_player(Teams_competition_events,team_players)
    
    #7)calcolo le spazzate
    clearance_list=clearance(Teams_competition_events,team_players)
    
    #8)Calcolo le palle contese fatte, vinte, perse e la percentuale delle vinte.
    fth_fth_faced_list,fth_fth_won_list,fth_fth_lost_list,fth_fth_won_perc_list=fth_fth_for_player(Teams_competition_events,team_players)
    
    #9)Calcolo i falli commessi
    fouls_list=Fouls_Committed_for_player(Teams_competition_events,team_players)
    
    #10)Calcolo le azioni difensive fatte dentro e fuori dall'area e la loro percentuale.
    inside,outside,total,inside_perc,outside_perc=Defensive_Actions_in_out_Area(Teams_competition_events,team_list)

    #11)calcolo gli errori che portano ad un tirio avversario o ad un evento di un portiere o a una palla recuperata
    errors=Error_for_player(Teams_competition_events,team_players)
    
    
    Parametri_Defensive_Actions_home=[t_positions,
                                    t_n_list,w_t_list,t_w_p_list,
                                    t_n_i_a_list,w_t_i_a_list,t_w_p_i_a_list,
                                    d_tq_t_list,s_d_tq_t_list,p_d_tq_t_list,
                                    md_tq_t_list,s_md_tq_t_list,p_md_tq_t_list,
                                    mo_tq_t_list,s_mo_tq_t_list,p_mo_tq_t_list,
                                    o_tq_t_list,s_o_tq_t_list,p_o_tq_t_list,
                                    a_l_lista,a_w_lista,t_a_d_lista,a_w_p_lista,
                                    a_l_i_a_lista,a_w_i_a_lista,t_a_d_i_a_lista,a_w_p_i_a_lista,
                                    dribling_affrontati, dribbling_subiti, dribbling_fermati,dribbling_fermati_perc,
                                    dribbling_affrontati_in_area, dribbling_subiti_in_area, dribbling_fermati_in_area,dribbling_fermati_in_area_perc,
                                    s_b_list,p_b_list,s_b_i_a_list,p_b_i_a_list,
                                    int_lista,s_i_lista,p_s_i_list,clearance_list,
                                    fth_fth_faced_list,fth_fth_won_list,fth_fth_lost_list,fth_fth_won_perc_list,fouls_list,
                                    inside,outside,total,inside_perc,outside_perc,errors,Times['Time']]
    
    parameters_name_Defensive_Actions=['Positions',
                                            'Tackles_Attempted','Won_Tackles','Won_Tackles_%',
                                            'Tackles_Attempted_in_Area','Won_Tackles_in_Area','Won_Tackles_%_in_Area',
                                            'LowDefensive_3/4_Tackles', 'Succesfull_LowDefensive_3/4_Tackles','Succesfull_LowDefensive_3/4_Tackles_%',
                                            'HighDefensive_3/4_Tackles','Succesfull_HighDefensive_3/4_Tackles','Succesfull_HighDefensive_3/4_Tackles_%',
                                            'LowOffensive_3/4_Tackles', 'Succesfull_LowOffensive_3/4_Tackles','Succesfull_LowOffensive_3/4_Tackles_%',
                                            'HighOffensive_3/4_Tackles','Succesfull_HighOffensive_3/4_Tackles','Succesfull_HighOffensive_3/4_Tackles_%',
                                            'Lost_Aereal_Duel','Won_Aereal_Duel','Total_Aereal_Duel','Won_Aereal_Duel_%',
                                            'Lost_Aereal_Duel_in_Area','Won_Aereal_Duel_in_Area','Total_Aereal_Duel_in_Area','Won_Aereal_Duel_%_in_Area',
                                            'Attempted_Dribbling_Suffered','Dribbled_Past_Suffered','Stopped_Dribbling','Dribble_Stopped_perc',
                                            'Attempted_Dribbling_Suffered_in_Area','Dribbled_Past_Suffered_in_Area','Stopped_Dribbling_in_Area','Dribble_Stopped_perc_in_Area',
                                            'Blocked_Shots','Blocked_Pases','Blocked_Shots_in_Area','Blocked_Pases_in_Area',
                                            'Interceptions','Succesfull_Interceptions','Succesfull_Interceptions_Percentage','Clearance',
                                            'Numero_Palle_Contese','Palle_Contese_Vinte','Palle_Contese_Perse','%_Palle_Contese_Vinte','Fouls_committed',
                                            'Inside_Area_Defensive_Actions','Outside_Area_Defensive_Actions','Total_Defensive_Actions','Inside_Area_Defensive_Actions_%','Outside_Area_Defensive_Actions_%','Errors','Times']
    
    print(len(Parametri_Defensive_Actions_home),len(parameters_name_Defensive_Actions))
    
    #Faccio il df
    Parameters_Defensive_Actions_home=pd.DataFrame(list(zip(*Parametri_Defensive_Actions_home)),columns=parameters_name_Defensive_Actions,index=team_list)  
    
    #Aggiungo colonna coi nomi dei giocatori
    Parameters_Defensive_Actions_home.insert(0, 'Player_Name', Parameters_Defensive_Actions_home.index)

    
    Parameters_Defensive_Actions_home.to_excel(rf'{path}\{team_name}\Defensive_Actions_Stats.xlsx',index=False)    
    
    
    
    """7) CALCOLO PARAMETRI PORTIERI"""
    #Faccio per la home team.
    
    #1)Calcolo lunghezza media passaggi portiere
    gk_list=gk_Pass_lenght(Teams_competition_events,h_g_k_list)
    
    #2)Calcolo rigori affrontati portiere
    n_p_list,c_p_list,b_p_list,f_p_list=gk_penalty(Teams_competition_events,h_g_k_list)
       
    #3)Calcolo tiri affrontati dal portiere
    n_s_list,b_s_list,b_s_ot_list,s_p_list,n_s_ot_list,c_g_list=gk_saved_percentage(Teams_competition_events,h_g_k_list)

    
    #4)Calcolo azioni da keeper sweeper
    claim_list,clear_list,punch_list,collected_list,succesfull_collected_list,collected_percentage_list,sweep_list,tackle_list,succesfull_tackle_list,tackle_percentage_list,in_area_action_list,out_area_action_list,total_actions,mean_defensive_action_lenght_list=Keeper_Sweeper(Teams_competition_events,h_g_k_list)
    
    #5)Estraggo Tempi di gioco dei Portieri
    GK_Times=Times.loc[t_g_k_list_h]
    
    parameters_name_goalkeeper_home=[h_gk_position,gk_list,n_p_list,c_p_list,b_p_list,f_p_list,
                                 n_s_list,n_s_ot_list,b_s_list,b_s_ot_list,s_p_list,c_g_list,
                                 claim_list,clear_list,punch_list,collected_list,succesfull_collected_list,collected_percentage_list,
                                 sweep_list,tackle_list,succesfull_tackle_list,tackle_percentage_list,in_area_action_list,out_area_action_list,
                                 total_actions,mean_defensive_action_lenght_list,GK_Times['Time']]
    
    
    parameters_name_goalkeeper=['Positions','Pass_Lenght','Penalties_Faced','Penalties_Conceded','Penalties_Blocked','Penalties_Failed',
                                'Shots_Faced','Shots_on_targhet_Faced','Shots_Blocked','Shots_Blocked_on_Targhet','Save_Percentage','Goal_Conceded',
                            'Claims','Clears','Punchs','Collected','Collected_Succesfull','Collected_Succesfull_%',
                            'Sweep','Tackles_Gk','Tackles_succesfull_Gk','Tackles_succesfull_%_Gk',
                            'Defensive_Actions_In_Area','Defensive_Actions_Out_Area','Total_actions',
                            'Mean_Defensive_Actions_lenght','Times']
    
    #Faccio il df
    Parameters_Goalkeeper_home=pd.DataFrame( list(zip(*parameters_name_goalkeeper_home)),columns=parameters_name_goalkeeper,index=t_g_k_list_h)  
    
    #Aggiungo colonna coi nomi dei giocatori
    Parameters_Goalkeeper_home.insert(0, 'Player_Name', Parameters_Goalkeeper_home.index)

    Parameters_Goalkeeper_home.to_excel(rf'{path}\{team_name}\Goalkeeper_Stats.xlsx',index=False)    

