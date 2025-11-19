# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 21:42:38 2023

@author: hp
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

path=rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Miei Progetti\Prova dati euro 2020\Full Competition'
#Trovo il numero di settimane della competizione
teams=os.listdir(f'{path}')
#numero_weeks=os.listdir(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches')

#Ora divido per tipo di parametri gli excel dentro le cartelle all'interno delle liste
shots_stats=[]
passes_stats=[]
passession_stats=[]
defensive_actions_stats=[]
defensive_parameters_stats=[]
gk_stats=[]
defensive_teams_stats=[]

for i in teams:
    #os.mkdir(rf'C:\Users\hp\OneDrive\Football Analytics\Calcio\Dati e Progetti\Miei Progetti\Dati Progetto Italia Europeo 2020\Parametri_Normalizzati_Gironi_for_Teams\{i}')

    print(i)
    directory_path=rf'{path}\{i}'
    #directory_path=rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}'
    lista_file = os.listdir(directory_path)
    for file in lista_file:
        #if Teams_names[i] in file:
        if 'Shots' in file:
            df=pd.read_excel(rf'{path}\{i}\{file}')
            #df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            #df=df.set_index('Unnamed: 0')  
            #df=df.reset_index().drop('index',axis=1)
            shots_stats.append(df)
            columns_shot=df.columns
        elif 'Passes' in file:
            df=pd.read_excel(rf'{path}\{i}\{file}')
            #df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            #df=df.set_index('Unnamed: 0')    
            #df=df.reset_index().drop('index',axis=1)
            passes_stats.append(df)               
            columns_passes_stats=df.columns            
        elif 'Possession' in file:             
            df=pd.read_excel(rf'{path}\{i}\{file}')
           # df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            #df=df.set_index('Unnamed: 0')  
            #df=df.reset_index().drop('index',axis=1)
            passession_stats.append(df)   
            columns_passession_stats=df.columns              
        elif 'Defensive_Actions' in file:          
            df=pd.read_excel(rf'{path}\{i}\{file}')
           # df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            # df=df.set_index('Unnamed: 0')     
           # df=df.reset_index().drop('index',axis=1)
            defensive_actions_stats.append(df) 
            columns_defensive_actions=df.columns                   
        elif 'Defensive_Parameters' in file:
            df=pd.read_excel(rf'{path}\{i}\{file}')
            #df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            # df=df.set_index('Unnamed: 0')     
            #df=df.reset_index().drop('index',axis=1)
            defensive_parameters_stats.append(df)   
            columns_defensive_parameters=df.columns              
        elif 'Goalkeeper' in file:
            df=pd.read_excel(rf'{path}\{i}\{file}')
            #df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            # df=df.set_index('Unnamed: 0')  
            #df=df.reset_index().drop('index',axis=1)
            gk_stats.append(df)   
            columns_gk=df.columns
        elif 'Defensive_Team' in file:             
            df=pd.read_excel(rf'{path}\{i}\{file}')
            #df=pd.read_excel(rf'C:\Users\usr02709\Desktop\Materiale\FA\Script\Statistiche_Euro_2020_All_Matches\week_{i}\{file}')
            #df=df.set_index('Unnamed: 0') 
           # df=df.reset_index().drop('index',axis=1)
            defensive_teams_stats.append(df)   
            columns_defensive_teams=df.columns
    else:
        continue

"""CREO I FILE NORMALIZZATI"""
result_path=rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Miei Progetti\Prova dati euro 2020\Full Competition Normalization'

#1) Normalizzo shots_stats
for t,dss in zip(teams,shots_stats):
    os.makedirs(rf'{result_path}\{t}') 
    dss.set_index('Player_Name',inplace=True)
    #dss=shots_stats[0].set_index('Player_Name')
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni
    dss_norm['P90_opXG']=(dss['opXG']/dss['Times'])*90    
    dss_norm['P90_spXG']=(dss['spXG']/dss['Times'])*90    
    dss_norm['P90_pXG']=(dss['pXG']/dss['Times'])*90  
    dss_norm['P90_npXG']=(dss['npXG']/dss['Times'])*90    
    dss_norm['P90_tXG']=(dss['tXG']/dss['Times'])*90    
    dss_norm['P90_opShots']=(dss['opShots']/dss['Times'])*90    
    dss_norm['P90_spShots']=(dss['spShots']/dss['Times'])*90    
    dss_norm['P90_pShots']=(dss['pShots']/dss['Times'])*90    
    dss_norm['P90_npShots']=(dss['npShots']/dss['Times'])*90    
    dss_norm['P90_tShots']=(dss['tShots']/dss['Times'])*90    
    dss_norm['P90_opShots_On_Targhet']=(dss['opShots_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_spShots_On_Targhet']=(dss['spShots_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_pShots_on_Targhet']=(dss['pShots_on_Targhet']/dss['Times'])*90    
    dss_norm['P90_npShots_On_Targhet']=(dss['npShots_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_tShots_On_Targhet']=(dss['tShots_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_Inside_Shots']=(dss['Inside_Shots']/dss['Times'])*90    
    dss_norm['P90_Outside_Shots']=(dss['Outside_Shots']/dss['Times'])*90    
    dss_norm['P90_Foot_Shots']=(dss['Foot_Shots']/dss['Times'])*90    
    dss_norm['P90_Foot_Gol']=(dss['Foot_Gol']/dss['Times'])*90    
    dss_norm['P90_Head_Shots']=(dss['Head_Shots']/dss['Times'])*90    
    dss_norm['P90_Head_Gol']=(dss['Head_Gol']/dss['Times'])*90    
    dss_norm['P90_Dribling_Shots']=(dss['Dribling_Shots']/dss['Times'])*90    
    dss_norm['P90_Dribbling_Goal']=(dss['Dribbling_Goal']/dss['Times'])*90    
    dss_norm['P90_opGol']=(dss['opGol']/dss['Times'])*90    
    dss_norm['P90_spGol']=(dss['spGol']/dss['Times'])*90    
    dss_norm['P90_pGol']=(dss['pGol']/dss['Times'])*90    
    dss_norm['P90_npGol']=(dss['npGol']/dss['Times'])*90    
    dss_norm['P90_tGol']=(dss['tGol']/dss['Times'])*90   
    dss_norm['P90_Penalty_Kick']=(dss['Penalty_Kick']/dss['Times'])*90        
    dss_norm['P90_Scored_Penalty']=(dss['Scored_Penalty']/dss['Times'])*90    
    dss_norm['P90_Blocked_Penalty']=(dss['Blocked_Penalty']/dss['Times'])*90    
    dss_norm['P90_Failed_Penalty']=(dss['Failed_Penalty']/dss['Times'])*90    
    dss_norm['P90_Free_Kicks_Numbers']=(dss['Free_Kicks_Numbers']/dss['Times'])*90    
    dss_norm['P90_Free_Kicks_Goals']=(dss['Free_Kicks_Goals']/dss['Times'])*90    
    dss_norm['P90_Clear_Shots']=(dss['Clear_Shots']/dss['Times'])*90    

    shots_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    shots_stats_norm.to_excel(rf'{result_path}\{t}\Shots_Stats_P90.xlsx')


#2) Normalizzo Pass_Stats
for t,dss in zip(teams,passes_stats):

    dss.set_index('Player_Name',inplace=True)
    #dss=shots_stats[0].set_index('Player_Name')
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni
    dss_norm['P90_Attempted_Passes']=(dss['Attempted_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Passes']=(dss['Succesfull_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Passes_Under_Pressure']=(dss['Attempted_Passes_Under_Pressure']/dss['Times'])*90  
    dss_norm['P90_Succesfull_Passes_Under_Pressure']=(dss['Succesfull_Passes_Under_Pressure']/dss['Times'])*90    
    dss_norm['P90_Passes_in_Final_Third']=(dss['Passes_in_Final_Third']/dss['Times'])*90  
    dss_norm['P90_Succesfull_Passes_in_Final_Third']=(dss['Succesfull_Passes_in_Final_Third']/dss['Times'])*90  
    dss_norm['P90_Passes_Forward_in_Final_Third']=(dss['Passes_Forward_in_Final_Third']/dss['Times'])*90  
    dss_norm['P90_Succesfull_Passes_Forward_in_Final_Third']=(dss['Succesfull_Passes_Forward_in_Final_Third']/dss['Times'])*90      
    dss_norm['P90_LowDefensive_3/4_Attempted_Passes']=(dss['LowDefensive_3/4_Attempted_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_LowDefensive_3/4_Passes']=(dss['Succesfull_LowDefensive_3/4_Passes']/dss['Times'])*90    
    dss_norm['P90_HighDefensive_3/4_Attempted_Passes']=(dss['HighDefensive_3/4_Attempted_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_HighDefensive_3/4_Passes']=(dss['Succesfull_HighDefensive_3/4_Passes']/dss['Times'])*90    
    dss_norm['P90_LowOffensive_3/4_Attempted_Passes']=(dss['LowOffensive_3/4_Attempted_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_LowOffensive_3/4_Passes']=(dss['Succesfull_LowOffensive_3/4_Passes']/dss['Times'])*90    
    dss_norm['P90_HighOffensive_3/4_Attempted_Passes']=(dss['HighOffensive_3/4_Attempted_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_HighOffensive_3/4_Passes']=(dss['Succesfull_HighOffensive_3/4_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Progressive_Passes']=(dss['Attempted_Progressive_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Progressive_Passes']=(dss['Succesfull_Progressive_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Short_Passes']=(dss['Attempted_Short_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Short_Passes']=(dss['Succesfull_Short_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Middle_Passes']=(dss['Attempted_Middle_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Middle_Passes']=(dss['Succesfull_Middle_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Long_Passes']=(dss['Attempted_Long_Passes']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Long_Passes']=(dss['Succesfull_Long_Passes']/dss['Times'])*90    
    dss_norm['P90_Attempted_Long_Passes_Underpressure']=(dss['Attempted_Long_Passes_Underpressure']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Long_Passes_Underpressur']=(dss['Succesfull_Long_Passes_Underpressur']/dss['Times'])*90    
    dss_norm['P90_Attempted_Long_Passes_Unpressed']=(dss['Attempted_Long_Passes_Unpressed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Long_Passes_Unpressed']=(dss['Succesfull_Long_Passes_Unpressed']/dss['Times'])*90        
    dss_norm['P90_Attempted_Throw']=(dss['Attempted_Throw']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Throw']=(dss['Succesfull_Throw']/dss['Times'])*90    
    dss_norm['P90_Key_Passes']=(dss['Key_Passes']/dss['Times'])*90    
    dss_norm['P90_Key_Passes_Under_Pressure']=(dss['Key_Passes_Under_Pressure']/dss['Times'])*90    
    dss_norm['P90_Through_Ball']=(dss['Through_Ball']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Through_Ball']=(dss['Succesfull_Through_Ball']/dss['Times'])*90    
    dss_norm['P90_Through_Ball_Under_Pressure']=(dss['Through_Ball_Under_Pressure']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Through_Ball_Under_Pressure']=(dss['Succesfull_Through_Ball_Under_Pressure']/dss['Times'])*90    
    dss_norm['P90_Attempted_Scambi']=(dss['Attempted_Scambi']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Scambi']=(dss['Succesfull_Scambi']/dss['Times'])*90    
    dss_norm['P90_Corners']=(dss['Corners']/dss['Times'])*90    
    dss_norm['P90_Attempted_Cross']=(dss['Attempted_Cross']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Cross']=(dss['Succesfull_Cross']/dss['Times'])*90    
    dss_norm['P90_Passes_Into_Box']=(dss['Passes_Into_Box']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Passes_Into_Box']=(dss['Succesfull_Passes_Into_Box']/dss['Times'])*90    
    dss_norm['P90_Cross_Into_Box']=(dss['Cross_Into_Box']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Cross_Into_Box']=(dss['Succesfull_Cross_Into_Box']/dss['Times'])*90    
    dss_norm['P90_Passes_Inside_Box']=(dss['Passes_Inside_Box']/dss['Times'])*90  
    dss_norm['P90_Succesfull_Passes_Inside_Box']=(dss['Succesfull_Passes_Inside_Box']/dss['Times'])*90    
    dss_norm['P90_Deep_Pass_Completion']=(dss['Deep_Pass_Completion']/dss['Times'])*90 
    dss_norm['P90_Succesfull_Deep_Pass_Completion']=(dss['Succesfull_Deep_Pass_Completion']/dss['Times'])*90     
    dss_norm['P90_Deep_Cross_Completion']=(dss['Deep_Cross_Completion']/dss['Times'])*90 
    dss_norm['P90_Succesfull_Deep_Cross_Completion']=(dss['Succesfull_Deep_Cross_Completion']/dss['Times'])*90     
    dss_norm['P90_Attempted_Goal_Kick']=(dss['Attempted_Goal_Kick']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Goal_Kick']=(dss['Succesfull_Goal_Kick']/dss['Times'])*90    
    dss_norm['P90_Ball_Receipt_Under_Pressure']=(dss['Ball_Receipt_Under_Pressure']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Ball_Receipt_Under_Pressure']=(dss['Succesfull_Ball_Receipt_Under_Pressure']/dss['Times'])*90    

    passes_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    passes_stats_norm.to_excel(rf'{result_path}\{t}\Passes_Stats_P90.xlsx')


#3) Normalizzo Possession Stats
for t,dss in zip(teams,passession_stats):
    dss.set_index('Player_Name',inplace=True)
    #dss=shots_stats[0].set_index('Player_Name')
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni
    dss_norm['P90_Possession_Number']=(dss['Possession_Number']/dss['Times'])*90    
    dss_norm['P90_Touches']=(dss['Touches']/dss['Times'])*90    
    dss_norm['P90_Touches_in_Final_Third']=(dss['Touches_in_Final_Third']/dss['Times'])*90    
    dss_norm['P90_Touches_in_Box']=(dss['Touches_in_Box']/dss['Times'])*90  
    dss_norm['P90_Attempted_Dribbling']=(dss['Attempted_Dribbling']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Dribbling']=(dss['Succesfull_Dribbling']/dss['Times'])*90    
    dss_norm['P90_Carries_Number']=(dss['Carries_Number']/dss['Times'])*90    
    dss_norm['P90_Progressive_Carries_Number']=(dss['Progressive_Carries_Number']/dss['Times'])*90    
    dss_norm['P90_Progressive_Carries_Distance']=(dss['Progressive_Carries_Distance']/dss['Times'])*90    
    dss_norm['P90_3/4_Carries']=(dss['3/4_Carries']/dss['Times'])*90    
    dss_norm['P90_Inside_area_Carries']=(dss['Inside_area_Carries']/dss['Times'])*90    
    dss_norm['P90_Deep_Progressions']=(dss['Deep_Progressions']/dss['Times'])*90    
    dss_norm['P90_Lost_Balls_After_Dribbling']=(dss['Lost_Balls_After_Dribbling']/dss['Times'])*90    
    dss_norm['P90_Defensive_Lost_Balls_After_Dribbling']=(dss['Defensive_Lost_Balls_After_Dribbling']/dss['Times'])*90    
    dss_norm['P90_Lost_Balls_After_Miscontroll']=(dss['Lost_Balls_After_Miscontroll']/dss['Times'])*90    
    dss_norm['P90_Defensive_Lost_Balls_After_Miscontroll']=(dss['Defensive_Lost_Balls_After_Miscontroll']/dss['Times'])*90    
    dss_norm['P90_Lost_Balls_After_Tackles']=(dss['Lost_Balls_After_Tackles']/dss['Times'])*90    
    dss_norm['P90_Defensive_Lost_Balls_After_Tackles']=(dss['Defensive_Lost_Balls_After_Tackles']/dss['Times'])*90    
    dss_norm['P90_Lost_Balls_After_Error']=(dss['Lost_Balls_After_Error']/dss['Times'])*90    
    dss_norm['P90_Defensive_Lost_Balls_After_Error']=(dss['Defensive_Lost_Balls_After_Error']/dss['Times'])*90    
    dss_norm['P90_Total_Lost_Balls']=(dss['Total_Lost_Balls']/dss['Times'])*90    
    dss_norm['P90_Defensive_Total_Lost_Balls']=(dss['Defensive_Total_Lost_Balls']/dss['Times'])*90    
    dss_norm['P90_Foul Won']=(dss['Foul Won']/dss['Times'])*90    

    possession_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    possession_stats_norm.to_excel(rf'{result_path}\{t}\Possession_Stats_P90.xlsx')


#4) Normalizzo Defensive Actions Stats
for t,dss,poss in zip(teams,defensive_actions_stats,passession_stats):
    print(dss)
    
    dss.set_index('Player_Name',inplace=True)
    #dss=defensive_actions_stats[0].set_index('Player_Name')
    #poss=passession_stats[0]
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    
    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni
    dss_norm['PAdj90_Tackles_Attempted']=((dss['Tackles_Attempted'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Won_Tackles']=((dss['Won_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Tackles_Attempted_in_Area']=((dss['Tackles_Attempted_in_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Won_Tackles_in_Area']=((dss['Won_Tackles_in_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_LowDefensive_3/4_Tackles']=((dss['LowDefensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Succesfull_LowDefensive_3/4_Tackles']=((dss['Succesfull_LowDefensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_HighDefensive_3/4_Tackles']=((dss['HighDefensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Succesfull_HighDefensive_3/4_Tackles']=((dss['Succesfull_HighDefensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90       
    dss_norm['PAdj90_LowOffensive_3/4_Tackles']=((dss['LowOffensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90        
    dss_norm['PAdj90_Succesfull_LowOffensive_3/4_Tackles']=((dss['Succesfull_LowOffensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_HighOffensive_3/4_Tackles']=((dss['HighOffensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Succesfull_HighOffensive_3/4_Tackles']=((dss['Succesfull_HighOffensive_3/4_Tackles'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['P90_Lost_Aereal_Duel']=(dss['Lost_Aereal_Duel']/dss['Times'])*90    
    dss_norm['P90_Won_Aereal_Duel']=(dss['Won_Aereal_Duel']/dss['Times'])*90    
    dss_norm['P90_Total_Aereal_Duel']=(dss['Total_Aereal_Duel']/dss['Times'])*90    
    dss_norm['P90_Lost_Aereal_Duel_in_Area']=(dss['Lost_Aereal_Duel_in_Area']/dss['Times'])*90    
    dss_norm['P90_Won_Aereal_Duel_in_Area']=(dss['Won_Aereal_Duel_in_Area']/dss['Times'])*90    
    dss_norm['P90_Total_Aereal_Duel_in_Area']=(dss['Total_Aereal_Duel_in_Area']/dss['Times'])*90    
    dss_norm['P90_Attempted_Dribbling_Suffered']=(dss['Attempted_Dribbling_Suffered']/dss['Times'])*90    
    dss_norm['P90_Dribbled_Past_Suffered']=(dss['Dribbled_Past_Suffered']/dss['Times'])*90       
    dss_norm['P90_Stopped_Dribbling']=(dss['Stopped_Dribbling']/dss['Times'])*90       
    dss_norm['P90_Attempted_Dribbling_Suffered_in_Area']=(dss['Attempted_Dribbling_Suffered_in_Area']/dss['Times'])*90    
    dss_norm['P90_Dribbled_Past_Suffered_in_Area']=(dss['Dribbled_Past_Suffered_in_Area']/dss['Times'])*90       
    dss_norm['P90_Stopped_Dribbling_in_Area']=(dss['Stopped_Dribbling_in_Area']/dss['Times'])*90        
    dss_norm['PAdj90_Blocked_Shots']=((dss['Blocked_Shots'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Blocked_Pases']=((dss['Blocked_Pases'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Blocked_Shots_in_Area']=((dss['Blocked_Shots_in_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Blocked_Pases_in_Area']=((dss['Blocked_Pases_in_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Interceptions']=((dss['Interceptions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Succesfull_Interceptions']=((dss['Succesfull_Interceptions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Clearance']=((dss['Clearance'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['P90_Numero_Palle_Contese']=(dss['Numero_Palle_Contese']/dss['Times'])*90    
    dss_norm['P90_Palle_Contese_Vinte']=(dss['Palle_Contese_Vinte']/dss['Times'])*90    
    dss_norm['P90_Palle_Contese_Perse']=(dss['Palle_Contese_Perse']/dss['Times'])*90    
    dss_norm['PAdj90_Fouls_committed']=((dss['Fouls_committed'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Inside_Area_Defensive_Actions']=((dss['Inside_Area_Defensive_Actions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Outside_Area_Defensive_Actions']=((dss['Outside_Area_Defensive_Actions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Total_Defensive_Actions']=((dss['Total_Defensive_Actions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['P90_Errors']=(dss['Errors']/dss['Times'])*90    

    defensive_actions_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    defensive_actions_stats_norm.to_excel(rf'{result_path}\{t}\defensive_actions_stats_norm_P90.xlsx')


#5) Normalizzo Defensive Actions Stats
for t,dss,poss in zip(teams,defensive_parameters_stats,passession_stats):
    print(dss)

    dss.set_index('Player_Name',inplace=True)
    #dss=defensive_parameters_stats[0].set_index('Player_Name')
    #poss=passession_stats[0]
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    #Normalizzo per 90 minuti
    dss_norm['P90_Pressures']=(dss['Pressures']/dss['Times'])*90    
    dss_norm['P90_Conterpressures']=(dss['Conterpressures']/dss['Times'])*90    
    dss_norm['P90_Offensive_Pressure']=(dss['Offensive_Pressure']/dss['Times'])*90  
    dss_norm['P90_Balls_Recovered']=(dss['Balls_Recovered']/dss['Times'])*90    
    dss_norm['P90_Offensive_Balls_Recoverd']=(dss['Offensive_Balls_Recoverd']/dss['Times'])*90    
    dss_norm['P90_Pressure_Regains']=(dss['Pressure_Regains']/dss['Times'])*90    

    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni

    defensive_parameters_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    defensive_parameters_stats_norm.to_excel(rf'{result_path}\{t}\defensive_parameters_stats_norm_P90.xlsx')

#6) Normalizzo Defensive Actions Stats
for t,dss,poss in zip(teams,defensive_teams_stats,passession_stats):
    print(dss)

    dss.set_index('Player_Name',inplace=True)
    #dss=defensive_teams_stats[0].set_index('Player_Name')
    #poss=passession_stats[0]
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    #Normalizzo per 90 minuti
    dss_norm['P90_opXGA']=(dss['opXGA']/dss['Times'])*90    
    dss_norm['P90_spXGA']=(dss['spXGA']/dss['Times'])*90    
    dss_norm['P90_pXGA']=(dss['pXGA']/dss['Times'])*90  
    dss_norm['P90_npXGA']=(dss['npXGA']/dss['Times'])*90    
    dss_norm['P90_tXGA']=(dss['tXGA']/dss['Times'])*90    
    dss_norm['P90_opShotsA']=(dss['opShotsA']/dss['Times'])*90    
    dss_norm['P90_spShotsA']=(dss['spShotsA']/dss['Times'])*90    
    dss_norm['P90_pShotsA']=(dss['pShotsA']/dss['Times'])*90    
    dss_norm['P90_npShotsA']=(dss['npShotsA']/dss['Times'])*90    
    dss_norm['P90_tShotsA']=(dss['tShotsA']/dss['Times'])*90    
    dss_norm['P90_opShotsA_On_Targhet']=(dss['opShotsA_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_spShotsA_On_Targhet']=(dss['spShotsA_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_pShotsA_On_Targhet']=(dss['pShotsA_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_npShotsA_On_Targhet']=(dss['npShotsA_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_tShotsA_On_Targhet']=(dss['tShotsA_On_Targhet']/dss['Times'])*90    
    dss_norm['P90_Inside_Area_Shots_Allowed']=(dss['Inside_Area_Shots_Allowed']/dss['Times'])*90    
    dss_norm['P90_Outside_Area_Shots_Aallowed']=(dss['Outside_Area_Shots_Aallowed']/dss['Times'])*90    
    dss_norm['P90_Clear_Shots_Allowed']=(dss['Clear_Shots_Allowed']/dss['Times'])*90    
    dss_norm['P90_Open_Play_Goal_A']=(dss['Open_Play_Goal_A']/dss['Times'])*90    
    dss_norm['P90_Set_Piece_Goal_A']=(dss['Set_Piece_Goal_A']/dss['Times'])*90    
    dss_norm['P90_Penalty_Goal_A']=(dss['Penalty_Goal_A']/dss['Times'])*90    
    dss_norm['P90_NonPenalty_Goal_A']=(dss['NonPenalty_Goal_A']/dss['Times'])*90    
    dss_norm['P90_Total_Goal_A']=(dss['Total_Goal_A']/dss['Times'])*90   
    dss_norm['P90_Passes_Allowed']=(dss['Passes_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Passes_Allowed']=(dss['Succesfull_Passes_Allowed']/dss['Times'])*90    
    dss_norm['P90_Corner_Allowed']=(dss['Corner_Allowed']/dss['Times'])*90    
    dss_norm['P90_Touches_Allowed']=(dss['Touches_Allowed']/dss['Times'])*90    
    dss_norm['P90_Touches_in_Final_Third_Allowed']=(dss['Touches_in_Final_Third_Allowed']/dss['Times'])*90    
    dss_norm['P90_Touches_in_Box_Allowed']=(dss['Touches_in_Box_Allowed']/dss['Times'])*90    
    
    dss_norm['P90_Passes_Into_Box_Allowed']=(dss['Passes_Into_Box_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Passes_Into_Box_Allowed']=(dss['Succesfull_Passes_Into_Box_Allowed']/dss['Times'])*90    
   
    dss_norm['P90_Cross_Into_Box_Allowed']=(dss['Cross_Into_Box_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Cross_Into_Box_Allowed']=(dss['Succesfull_Cross_Into_Box_Allowed']/dss['Times'])*90    
    
    dss_norm['P90_Passes_Inside_Box_Allowed']=(dss['Passes_Inside_Box_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Passes_Inside_Box_Allowed']=(dss['Succesfull_Passes_Inside_Box_Allowed']/dss['Times'])*90    
  
    dss_norm['P90_Deep_Progression_Allowed']=(dss['Deep_Progression_Allowed']/dss['Times'])*90    
    dss_norm['P90_Three_Quarters_Carries_Allowed']=(dss['Three_Quarters_Carries_Allowed']/dss['Times'])*90    
    dss_norm['P90_Inside_Area_Carries_Allowed']=(dss['Inside_Area_Carries_Allowed']/dss['Times'])*90    
    dss_norm['P90_Deep_Pass_Completion_Allowed']=(dss['Deep_Pass_Completion_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Deep_Pass_Completion_Allowed']=(dss['Succesfull_Deep_Pass_Completion_Allowed']/dss['Times'])*90    
    dss_norm['P90_Deep_Cross_Completion_Allowed']=(dss['Deep_Cross_Completion_Allowed']/dss['Times'])*90    
    dss_norm['P90_Succesfull_Deep_Cross_Completion_Percentage_Allowed']=(dss['Succesfull_Deep_Cross_Completion_Percentage_Allowed']/dss['Times'])*90    

    """Calcolo e inserisco le colonne normalizzate."""
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni

    defensive_teams_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    defensive_teams_stats_norm.to_excel(rf'{result_path}\{t}\defensive_teams_stats_norm_P90.xlsx')

#6) Normalizzo goalkeeper Stats
for t,dss,poss in zip(teams,gk_stats,passession_stats):
    print(dss)

    dss.set_index('Player_Name',inplace=True)
    #dss=gk_stats[0].set_index('Player_Name')
    #poss=passession_stats[0]
    #Creo il df in cui inserirò le colonne normalizzate
    dss_norm=pd.DataFrame(index=dss.index)
    
    #Normalizzo per 90 minuti
    dss_norm['P90_Penalties_Faced']=(dss['Penalties_Faced']/dss['Times'])*90    
    dss_norm['P90_Penalties_Conceded']=(dss['Penalties_Conceded']/dss['Times'])*90    
    dss_norm['P90_Penalties_Blocked']=(dss['Penalties_Blocked']/dss['Times'])*90  
    dss_norm['P90_Penalties_Failed']=(dss['Penalties_Failed']/dss['Times'])*90    
    dss_norm['P90_Shots_Faced']=(dss['Shots_Faced']/dss['Times'])*90    
    dss_norm['P90_Shots_on_targhet_Faced']=(dss['Shots_on_targhet_Faced']/dss['Times'])*90
    dss_norm['P90_Shots_Blocked']=(dss['Shots_Blocked']/dss['Times'])*90    
    dss_norm['P90_Shots_Blocked_on_Targhet']=(dss['Shots_Blocked_on_Targhet']/dss['Times'])*90    
    dss_norm['P90_Goal_Conceded']=(dss['Goal_Conceded']/dss['Times'])*90    
    dss_norm['PAdj90_Claims']=((dss['Claims'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Clears']=((dss['Clears'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Punchs']=((dss['Punchs'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Collected']=((dss['Collected'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90        
    dss_norm['PAdj90_Collected_Succesfull']=((dss['Collected_Succesfull'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Sweep']=((dss['Sweep'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Tackles_Gk']=((dss['Tackles_Gk'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Tackles_succesfull_Gk']=((dss['Tackles_succesfull_Gk'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Defensive_Actions_In_Area']=((dss['Defensive_Actions_In_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Defensive_Actions_Out_Area']=((dss['Defensive_Actions_Out_Area'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    
    dss_norm['PAdj90_Total_actions']=((dss['Total_actions'] * 2 / (1 + np.exp(-10 * (poss['Possession_Percentage'].iloc[-1] - 0.5))))/dss['Times'])*90    

        
    """Calcolo e inserisco le colonne normalizzate."""
    
    #Metto nomi e posizione giocatori
    #Inserisco colonne noralizzate sui 90 minuti e alcune non normalizzate perchè generate da operazioni

    gk_stats_norm=pd.merge(dss,dss_norm,on='Player_Name')
    
    gk_stats_norm.to_excel(rf'{result_path}\{t}\gk_stats_norm_P90.xlsx')



