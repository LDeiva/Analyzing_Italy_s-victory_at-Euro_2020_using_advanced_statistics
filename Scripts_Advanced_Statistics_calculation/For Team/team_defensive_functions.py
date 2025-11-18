# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:10:25 2023

@author: hp
"""

"""1)STATISTICHE PER SQUADRA E GIOCATORI"""
import pandas as pd
import numpy as np

"""FUNZIONE PER Le divisioni con 0 a denominatore."""
def division(y, x):
    return 0 if x == 0 else y / x

def percentage(y, x):
    return 0 if x == 0 else (y / x)*100



"""Defensive Stats For Team"""
#Calcolo il PPDA come fa Statsbomb, nel modo che mi hanno speiegato per e-mail.
def PPDA(df,d_team_name,team_name):
    ppda_list=[0 for i in range(len(d_team_name[1:]))]
    d_team_name=d_team_name[-1]
    columns=list(df.columns)
    Offensive_pass_number=0
    Number_of_defensive_actions=0
    fc=0
    df_o=df[(df['team_name']!=team_name)]
    df_d=df[(df['team_name']==d_team_name)]
    for c in range(len(df_o)):
        if df_o['type_name'].iloc[c]=='Pass' and pd.isnull(df_o['pass_outcome_name'].iloc[c])==True and df_o['location'].iloc[c][0]<72:            
            Offensive_pass_number+=1
                
    for i in range(len(df_d)):            
        if df_d['duel_type_name'].iloc[i]=='Tackle' and df_d['location'].iloc[i][0]>=48:  
            Number_of_defensive_actions+=1
            
        if df_d['type_name'].iloc[i]=='Interception' and df_d['location'].iloc[i][0]>=48:
            Number_of_defensive_actions+=1
            
        if 'foul_committed_type_name' in columns:
            if 'foul_committed_offensive' in columns:
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['foul_committed_offensive'].iloc[i]!=True and pd.isnull(df_d['foul_committed_type_name'].iloc[i])==True and df_d['location'].iloc[i][0]>=48:
                    fc+=1
                    Number_of_defensive_actions+=1
            else:
                if df_d['type_name'].iloc[i]=='Foul Committed' and pd.isnull(df_d['foul_committed_type_name'].iloc[i])==True and df_d['location'].iloc[i][0]>=48: 
                    Number_of_defensive_actions+=1
        else:    
            if 'foul_committed_offensive' in columns:
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['location'].iloc[i][0]>=48 and df_d['foul_committed_offensive'].iloc[i]!=True:
                    Number_of_defensive_actions+=1
            else:       
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['location'].iloc[i][0]>=48:
                    Number_of_defensive_actions+=1

        if df_d['type_name'].iloc[i]=='Dribbled Past' and df_d['location'].iloc[i][0]>=48:
            Number_of_defensive_actions+=1

        if df_d['type_name'].iloc[i]=='Block' and df_d['location'].iloc[i][0]>=48 :
            Number_of_defensive_actions+=1
            
    PPDA=Offensive_pass_number/Number_of_defensive_actions
    ppda_list.append(PPDA)
    return ppda_list

"""Defensive Stats For Team"""
#Calcolo il PPDA come fa Statsbomb, nel modo che mi hanno speiegato per e-mail.
def APPDA(df,d_team_list,team_list):
    ppda_list=[0 for i in range(len(team_list[1:]))]
    columns=list(df.columns)
    Offensive_pass_number=0
    Number_of_defensive_actions=0
    fc=0
    df_o=df[(df['team_name']==team_list[-1])]
    df_d=df[(df['team_name'].isin(d_team_list))]
    for c in range(len(df_o)):
        if df_o['type_name'].iloc[c]=='Pass' and pd.isnull(df_o['pass_outcome_name'].iloc[c])==True and df_o['location'].iloc[c][0]<72:            
            Offensive_pass_number+=1
                
    for i in range(len(df_d)):            
        if df_d['duel_type_name'].iloc[i]=='Tackle' and df_d['location'].iloc[i][0]>=48:  
            Number_of_defensive_actions+=1
            
        if df_d['type_name'].iloc[i]=='Interception' and df_d['location'].iloc[i][0]>=48:
            Number_of_defensive_actions+=1
            
        if 'foul_committed_type_name' in columns:
            if 'foul_committed_offensive' in columns:
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['foul_committed_offensive'].iloc[i]!=True and pd.isnull(df_d['foul_committed_type_name'].iloc[i])==True and df_d['location'].iloc[i][0]>=48:
                    fc+=1
                    Number_of_defensive_actions+=1
            else:
                if df_d['type_name'].iloc[i]=='Foul Committed' and pd.isnull(df_d['foul_committed_type_name'].iloc[i])==True and df_d['location'].iloc[i][0]>=48: 
                    Number_of_defensive_actions+=1
        else:    
            if 'foul_committed_offensive' in columns:
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['location'].iloc[i][0]>=48 and df_d['foul_committed_offensive'].iloc[i]!=True:
                    Number_of_defensive_actions+=1
            else:       
                if df_d['type_name'].iloc[i]=='Foul Committed' and df_d['location'].iloc[i][0]>=48:
                    Number_of_defensive_actions+=1

        if df_d['type_name'].iloc[i]=='Dribbled Past' and df_d['location'].iloc[i][0]>=48:
            Number_of_defensive_actions+=1

        if df_d['type_name'].iloc[i]=='Block' and df_d['location'].iloc[i][0]>=48 :
            Number_of_defensive_actions+=1
            
    PPDA=Offensive_pass_number/Number_of_defensive_actions
    ppda_list.append(PPDA)
    return ppda_list


"""Calcolo altezza media interventi difensivi, escludo le pressioni e metto solo tackle e non duelli aerei"""
def Average_Defensive_Distance(df,home_list):
    add_list=[0 for i in range(len(home_list[1:]))]
    team=home_list[-1]
    columns=list(df.columns)
    height=0
    df=df[df['team_name']==team]
    n=0
    
    for i in range(len(df)):
        if df['duel_type_name'].iloc[i]=='Tackle':
            height+=int(df['location'].iloc[i][0])        
            n+=1
        if df['type_name'].iloc[i]=='Dribbled Past':
            height+=int(df['location'].iloc[i][0])        
            n+=1       
        if df['type_name'].iloc[i]=='Interception':
            height+=int(df['location'].iloc[i][0])        
            n+=1    
        if df['type_name'].iloc[i]=='Block':
            height+=int(df['location'].iloc[i][0])        
            n+=1    
        if 'foul_committed_type_name' in columns:
            if 'foul_committed_offensive' in columns:

                if df['type_name'].iloc[i]=='Foul Committed' and df['foul_committed_offensive'].iloc[i]!=True and pd.isnull(df['foul_committed_type_name'].iloc[i])==True:
                        height+=int(df['location'].iloc[i][0])        
                        n+=1         
            else:
                if df['type_name'].iloc[i]=='Foul Committed'  and pd.isnull(df['foul_committed_type_name'].iloc[i])==True:
                        height+=int(df['location'].iloc[i][0])        
                        n+=1         
                
        else:
            if 'foul_committed_offensive' in columns:

                if df['type_name'].iloc[i]=='Foul Committed' and df['foul_committed_offensive'].iloc[i]!=True:
                        height+=int(df['location'].iloc[i][0])        
                        n+=1     
            else:
                if df['type_name'].iloc[i]=='Foul Committed':
                        height+=int(df['location'].iloc[i][0])        
                        n+=1               
        #Faccio il numero totale di interventi meno il numero di falli fatti in possesso della palla
    ADD=height/n
    add_list.append(ADD)
    return add_list



"""Calcolo le azioni difensive fatte in area e fuori area""" 
def Defensive_Actions_in_out_Area(df,lista):
    inside_list=[]
    outside_list=[]
    total_list=[]
    inside_perc_list=[]
    outside_perc_list=[]
    

    
    columns=list(df.columns)
    for p in lista:
        defensive_team=df[df['player_name']==p]
        inside=0
        outside=0
        for i in range(len(defensive_team)):
    
            if defensive_team['duel_type_name'].iloc[i]=='Tackle':
                if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                    inside+=1
                else:
                    outside+=1
            if defensive_team['type_name'].iloc[i]=='Dribbled Past':
                if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                    inside+=1
                else:
                    outside+=1
            if defensive_team['type_name'].iloc[i]=='Interception':
                if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                    inside+=1
                else:
                    outside+=1
            if defensive_team['type_name'].iloc[i]=='Block':
                if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                    inside+=1
                else:
                    outside+=1
                    
            if 'foul_committed_type_name' in columns:
                if 'foul_committed_offensive' in columns:
               
                    if defensive_team['type_name'].iloc[i]=='Foul Committed' and pd.isnull(defensive_team['foul_committed_type_name'].iloc[i])==True and df['foul_committed_offensive'].iloc[i]!=True:
                        if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                            inside+=1
                        else:
                            outside+=1 
                else:
                    if defensive_team['type_name'].iloc[i]=='Foul Committed' and pd.isnull(defensive_team['foul_committed_type_name'].iloc[i])==True:
                        if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                            inside+=1
                        else:
                            outside+=1 
                    
            else:
                if 'foul_committed_offensive' in columns:
    
                    if defensive_team['type_name'].iloc[i]=='Foul Committed' and df['foul_committed_offensive'].iloc[i]!=True:
                        if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                            inside+=1
                        else:
                            outside+=1
                else:
                    if defensive_team['type_name'].iloc[i]=='Foul Committed':
                        if defensive_team['location'].iloc[i][0]<=18 and 18<=defensive_team['location'].iloc[i][1]<=62:
                            inside+=1
                        else:
                            outside+=1 
                            
        total=inside+outside
        
        inside_perc=percentage(inside,total)
        outside_perc=percentage(outside,total)
        
        inside_list.append(inside)
        outside_list.append(outside)
        total_list.append(total)
        inside_perc_list.append(inside_perc)
        outside_perc_list.append(outside_perc)
        
    """Calcolo valori per Team"""
    inside_list.append(sum(inside_list))
    outside_list.append(sum(outside_list))
    total_list.append(sum(total_list))
    inside_perc_list.append(percentage(inside_list[-1],total_list[-1]))
    outside_perc_list.append(percentage(outside_list[-1],total_list[-1]))        
    
    return inside_list,outside_list,total_list,inside_perc_list,outside_perc_list
 



#-----------------------------------------------------------
#la home_list serve per creare la lista lunga come il numero di players dell'italia così aggiungo il parametro alla fine ed ho il valore del parametro concesso dall'italia.
#La o_team è il nome dei giocatori avversari da cui calcolo il parametro globale
#-----------------------------------------------------------


"""Calcolo gli xg against e i tiri against di vario tipo"""
def XG_Shots_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[df['player_name'].isin(lista_against)]
    #I create lists with only Open Play or Set Piece or Penalty Shots
    opShot=df[(df['type_name']=='Shot') & (df['shot_type_name']=='Open Play')  & (df['period']<=4)] 
    spShot=df[(df['type_name']=='Shot') & ((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off'))  & (df['period']<=4)]
    pShot=df[(df['type_name']=='Shot') & (df['shot_type_name']=='Penalty')  & (df['period']<=4)]
    
    #Liste in cui inserire le varie analisi 
    opXG=[0 for i in range(len(lista_home))]
    spXG=[0 for i in range(len(lista_home))]
    pXG=[0 for i in range(len(lista_home))]
    npXG=[0 for i in range(len(lista_home))]
    tXG=[0 for i in range(len(lista_home))]
    opXGs=[0 for i in range(len(lista_home))]
    spXGs=[0 for i in range(len(lista_home))]
    pXGs=[0 for i in range(len(lista_home))]
    npXGs=[0 for i in range(len(lista_home))]
    tXGs=[0 for i in range(len(lista_home))]
    ops=[0 for i in range(len(lista_home))]
    sps=[0 for i in range(len(lista_home))]
    ps=[0 for i in range(len(lista_home))]
    nps=[0 for i in range(len(lista_home))]
    ts=[0 for i in range(len(lista_home))]
    
    #Calcolo gli Shots per squadra avversaria.
    opSA=len(opShot)
    spSA=len(spShot)
    pSA=len(pShot)
    npSA=opSA+spSA
    tSA=opSA+spSA+pSA
    
    #Aggiungo alla lista il numero di tiri subiti
    ops.append(opSA)
    sps.append(spSA)
    ps.append(pSA)
    nps.append(npSA)
    ts.append(tSA)
    
    #Calcolo gli xg
    opxg=opShot['shot_statsbomb_xg'].sum()
    spxg=spShot['shot_statsbomb_xg'].sum()
    pxg=pShot['shot_statsbomb_xg'].sum()
    npxg=opxg+spxg
    txg=opxg+spxg+pxg
    
    #Aggiungo alla lista il numero di XG subiti
    opXG.append(opxg)
    spXG.append(spxg)
    pXG.append(pxg)
    npXG.append(npxg)
    tXG.append(txg)
        
    #Calcolo gli XG su tiro subiti.
    opxgs=division(opxg,opSA)
    spxgs=division(spxg,spSA)
    pxgs=division(pxg,pSA)
    npxgs=division(npxg,npSA)
    txgs=division(txg,tSA)

    #Aggiungo alla lista il numero di XG su tiro subiti
    opXGs.append(opxgs)
    spXGs.append(spxgs)
    pXGs.append(pxgs)
    npXGs.append(npxgs)
    tXGs.append(txgs)
    
    return opXG,spXG,pXG,npXG,tXG,opXGs,spXGs,npXGs,tXGs,ops,sps,ps,nps,ts



#Calcolo i tiri in porta concessi
def Shots_on_targhet_conceeded(df,lista_home,lista_against):
    
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Cerco i tiri inporta in open play, set pieces e penalty
    opsa_on_t=df[(df['shot_type_name']=='Open Play') & ((df['shot_outcome_name']=='Goal') | (df['shot_outcome_name']=='Saved') | (df['shot_outcome_name']=='Saved to Post'))]
    spsa_on_t=df[((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off')) & ((df['shot_outcome_name']=='Goal') | (df['shot_outcome_name']=='Saved') | (df['shot_outcome_name']=='Saved to Post'))]
    psa_on_t=df[(df['shot_type_name']=='Penalty') & ((df['shot_outcome_name']=='Goal') | (df['shot_outcome_name']=='Saved') | (df['shot_outcome_name']=='Saved to Post'))]
    
    #Liste in cui inserire le varie analisi 
    opSA_on_Targhet=[0 for i in range(len(lista_home))]
    spSA_on_Targhet=[0 for i in range(len(lista_home))]
    pSA_on_Targhet=[0 for i in range(len(lista_home))]

        
    #Faccio l'append dei tiri nelle liste
    opSA_on_Targhet.append(len(opsa_on_t))
    spSA_on_Targhet.append(len(spsa_on_t))
    pSA_on_Targhet.append(len(psa_on_t))
    npSA_on_Targhet=[x+y for x,y in zip(opSA_on_Targhet,spSA_on_Targhet)]
    tSA_on_Targhet=[x+y for x,y in zip(npSA_on_Targhet,pSA_on_Targhet)]
    
    return opSA_on_Targhet,spSA_on_Targhet,pSA_on_Targhet,npSA_on_Targhet,tSA_on_Targhet   


"""Calcolo numero di tiri da dentro e fuori area considerando solo quelli su azione, per ogni player"""
def Out_and_In_shots_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Liste in cui inserire le varie analisi 
    inside_conceeded=[0 for i in range(len(lista_home))]
    outside_conceeded=[0 for i in range(len(lista_home))]
    
    #filtro per i tiri in open play
    shots=df[(df['type_name']=='Shot') &  (df['shot_type_name']=='Open Play')]
    
    outside_shots=0
    inside_shots=0
    #I calculate for player shot inside and outside area 
    for i in range(len(shots)):
        if shots['location'].iloc[i][0]>=102 and 18<=shots['location'].iloc[i][1]<=62:
            inside_shots+=1
        else:
            outside_shots+=1
    
    inside_conceeded.append(inside_shots)
    outside_conceeded.append(outside_shots)

    return inside_conceeded,outside_conceeded



"""Calcolo distanza media dei tiri in Open Play, per ogni player"""
def Shots_lenght_conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]
    
    #Liste in cui inserire le varie analisi 
    mean_shot_lenghtA=[0 for i in range(len(lista_home))]

    n_sA=[]
    s_l_lA=[]
    

    shots=df[(df['type_name']=='Shot') & (df['shot_type_name']=='Open Play')  & (df['period']<=4)]
    n_shots=len(shots)
    n_sA.append(n_shots)
    #Calcolo la distanza dei tiri totale
    shots_lenght=0
    for i in range(len(shots)):
        
        s_l=np.sqrt(np.square(shots['shot_end_location'].iloc[i][0]-shots['location'].iloc[i][0]) + np.square(shots['shot_end_location'].iloc[i][1]-shots['location'].iloc[i][1]))
        shots_lenght+=s_l
    s_l_lA.append(shots_lenght)
        
    #Faccio la distanza dei tiri diviso il numero di tiri e trovo la distanza media    
    m_shot_lenght=division(shots_lenght,n_shots)
    
    #Aggiungo alla lista la distanza media
    mean_shot_lenghtA.append(m_shot_lenght)    
        
    return mean_shot_lenghtA

"""Calcolo i tiri effettuati solo con il portiere a frapporsi tra il tiratore e la porta, per ogni giocatore"""
def clear_shots_conceeded(df,lista_home,lista_against):
    clear_shots_list=[0 for i in range(len(lista_home))]

    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    columns=list(df.columns)
    #List where i put clear shots for every player.


    if 'shot_one_on_one' in columns:
        shot=df[(df['shot_one_on_one']==True) & (df['period']<=4)]
        c_s=len(shot)
        clear_shots_list.append(c_s)
    else:
        c_s=0
        clear_shots_list.append(c_s)
            

    return clear_shots_list



"""Calcolo il numero di gol effettuati in totale, su open play e penalty per ogni player"""
def GOL_Conceeded(df,lista_home,lista_against):
    
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]
    
    
    opgA_list=[0 for i in range(len(lista_home))]
    spgA_list=[0 for i in range(len(lista_home))]
    pgA_list=[0 for i in range(len(lista_home))]
    tgA_list=[0 for i in range(len(lista_home))]
    nonpgA_list=[0 for i in range(len(lista_home))]
    
    #I create df with goal for every player 
    goal=df[(df['shot_outcome_name']=='Goal')]
    open_play_goal=goal[goal['shot_type_name']=='Open Play']
    set_piece_goal=goal[(goal['shot_type_name']=='Corner') | (goal['shot_type_name']=='Free Kick') | (goal['shot_type_name']=='Kick Off')]
    penalty_gol=goal[(goal['shot_type_name']=='Penalty')]
    
    #Calcolo il numero di gol per ogni tipologia e quelli totali
    opg=len(open_play_goal)
    spg=len(set_piece_goal)
    pg=len(penalty_gol)
    total_goal=opg+spg+pg
    nonpenalty_goal=opg+spg
    #Li inserisco nelle relative liste
    opgA_list.append(opg)
    spgA_list.append(spg)
    pgA_list.append(pg)
    tgA_list.append(total_goal)
    nonpgA_list.append(nonpenalty_goal)
        

    return opgA_list,spgA_list,pgA_list,nonpgA_list,tgA_list


"""Passaggi fatti, completati concessi e la loro percentuale di completamento"""
def Passes_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Creo le liste che mi servono
    conceeded_passes=[0 for i in range(len(lista_home))]
    conceeded_success_passes=[0 for i in range(len(lista_home))]
    conceeded_success_passes_perc=[0 for i in range(len(lista_home))]
    
    #Calcolo i passaggi effettuati dagli avversari
    passaggi=df[(df['type_name']=='Pass')] 
    n_pass=len(passaggi) #Number of passes done
    conceeded_passes.append(n_pass)

    #I calculate number of passes completed conceeded.
    successful_passes=df[(df['type_name']=='Pass')& (pd.isnull(df['pass_outcome_name'])==True) ]
    n_succesfull_passes=len(successful_passes) #Number of passes completed
    conceeded_success_passes.append(n_succesfull_passes)
        
    #I calculate percentage of completed passes for every players.
    Succesfull_pass_percentage=percentage(n_succesfull_passes,n_pass)
    conceeded_success_passes_perc.append(Succesfull_pass_percentage)
        
    return conceeded_passes,conceeded_success_passes,conceeded_success_passes_perc

"""Calcolo i passaggi che partono da fuori area e finiscono in area totali e succesfully"""
def Passes_and_cross_into_the_Box_conceeded(df,lista_home,lista_against):
    p_b_list=[0 for i in range(len(lista_home))]
    s_p_b_list=[0 for i in range(len(lista_home))]
    p_p_b_list=[0 for i in range(len(lista_home))]
    
    c_b_list=[0 for i in range(len(lista_home))]
    s_c_b_list=[0 for i in range(len(lista_home))]
    p_c_b_list=[0 for i in range(len(lista_home))]
    
    b_c_percentage_list=[0 for i in range(len(lista_home))]
    
    #Creo df che mi servono
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]
    passaggi=df[(df['type_name']=='Pass')] 

    
    p_b=0
    s_p_b=0
    c_b=0
    s_c_b=0
   
    for i in range(len(passaggi)):
        if passaggi['type_name'].iloc[i]=='Pass' and passaggi['pass_cross'].iloc[i]!=True:
            if passaggi['location'].iloc[i][0]<102 or passaggi['location'].iloc[i][1]>62 or passaggi['location'].iloc[i][1]<18:
                if passaggi['pass_end_location'].iloc[i][0]>=102 and 18<=passaggi['pass_end_location'].iloc[i][1]<=62:
                    p_b+=1
                    if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                        s_p_b+=1
                        
        elif passaggi['type_name'].iloc[i]=='Pass' and passaggi['pass_cross'].iloc[i]==True:
            if passaggi['location'].iloc[i][0]<102 or passaggi['location'].iloc[i][1]>62 or passaggi['location'].iloc[i][1]<18:
                if passaggi['pass_end_location'].iloc[i][0]>=102 and 18<=passaggi['pass_end_location'].iloc[i][1]<=62:
                    c_b+=1
                    if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                        s_c_b+=1
                            
    #Append for passes into the box spcific lis            
    p_b_list.append(p_b)
    s_p_b_list.append(s_p_b)
    #In case passes in box are 0 it isn't possible to calculate the percentage and i put it =0 manually.
    p_p_b_list.append(percentage(s_p_b,p_b))

    #Append for passes into the box spcific lis            
    c_b_list.append(c_b)
    s_c_b_list.append(s_c_b)
    #In case passes in box are 0 it isn't possible to calculate the percentage and i put it =0 manually.
    p_c_b_list.append(percentage(s_c_b,c_b))
    
    n_p_b=p_b+c_b
    #Calculation for Box Cross percentage.
    b_c_percentage_list.append((c_b/n_p_b)*100)
        
    """I Calculate Pass in Box for Team""" 
    p_b_list.append(sum(p_b_list))
    s_p_b_list.append(sum(s_p_b_list))
    p_p_b_list.append(percentage(s_p_b_list[-1],p_b_list[-1]))

    """I Calculate Cross in Box for Team""" 
    c_b_list.append(sum(c_b_list))
    s_c_b_list.append(sum(s_c_b_list))
    
    n_p_b_total=c_b_list[-1]+s_c_b_list[-1]
    p_c_b_list.append(percentage(s_c_b_list[-1],n_p_b_total))

    """I Calculate Box Cross Percentage for Team""" 
    b_c_percentage_list.append(percentage(p_c_b_list[-1],p_b_list[-1]))
    
    
    return p_b_list,s_p_b_list,p_p_b_list,c_b_list,s_c_b_list,p_c_b_list,b_c_percentage_list



"""Calcolo passaggi in area"""
def Box_Pass_conceeded(df,lista_home,lista_against):
        pass_area_list=[0 for i in range(len(lista_home))]
        succ_pass_area_list=[0 for i in range(len(lista_home))]
        perc_succ_pass_area_list=[0 for i in range(len(lista_home))]
        
        passaggi_in_area=0
        passaggi_in_area_completati=0

        passaggi=df[(df['type_name']=='Pass') & (df['player_name'].isin(lista_against)) & (df['period']<=4)]
        for i in range(len(passaggi)):
            if passaggi['location'].iloc[i][0]>=102 and 18<=passaggi['location'].iloc[i][1]<=62:
                passaggi_in_area+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    passaggi_in_area_completati+=1
                    
                        
        #Popolo le liste passagi          
        pass_area_list.append(passaggi_in_area)
        succ_pass_area_list.append(passaggi_in_area_completati)
        perc_succ_pass_area_list.append(percentage(passaggi_in_area_completati,passaggi_in_area))
            

            
        """I Calculate Pass in Box for Team""" 
        pass_area_list.append(sum(pass_area_list))
        succ_pass_area_list.append(sum(succ_pass_area_list))
        perc_succ_pass_area_list.append(percentage(succ_pass_area_list[-1],pass_area_list[-1]))
        
        return pass_area_list,succ_pass_area_list,perc_succ_pass_area_list               

"""Conceeded Corners"""
def Corners_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Creo le liste che mi servono
    corner_conceeded=[0 for i in range(len(lista_home))]

    #Trovo il numero di corner concessi
    corner=df[(df['pass_type_name']=='Corner')]
    corners_number=len(corner)
    corner_conceeded.append(corners_number)

    return corner_conceeded


"""Calcolo i tocchi di ogni giocatore."""
def Touches_conceeded(df,lista_home,lista_against):
    player_touch_list=[0 for i in range(len(lista_home))]
    

    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]
    

    # Trova gli indici sequenziali
    sequential_indices = []
    current_sequence = []
    for idx in tocchi.index:
        if len(current_sequence) == 0 or idx == current_sequence[-1] + 1:
            current_sequence.append(idx)
        else:
            if len(current_sequence) > 1:
                sequential_indices.append(current_sequence)
            current_sequence = [idx]
    # Aggiungi l'ultima sequenza se necessario
    if len(current_sequence) > 1:
        sequential_indices.append(current_sequence)
    
    #creo la lista che mi servirà per calcolare gli eventi singoli che saranno conteggi anche loro.
    lista_unificata = []
    for lista in sequential_indices:
        lista_unificata += lista
            
    #trova gli indici non sequienziali
    non_sequential_indices= list(set(tocchi.index) - set(lista_unificata))
    
    touch=len(sequential_indices)+len(non_sequential_indices)
    
    player_touch_list.append(touch)
    
    player_touch_list.append(sum(player_touch_list)) 

    return player_touch_list


"""Calcolo i tocchi in area concessi."""
def Touches_in_final_third_conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Creo le liste che mi servono
    touches_in_final_third_conceeded=[0 for i in range(len(lista_home))]
    
    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]

    #Splitto le coordinate in x e y per filtrare gli eventi correlati ai tocchi solo in area avversaria.
    #Così calcolo i tocchi in area
    x,y=zip(*tocchi['location'])
    tocchi['x'],tocchi['y']=x,y
    touch_in_box=tocchi[(tocchi['x']>=80)]
    #Calcolo i tocchi in area concessi
    # Trova gli indici sequenziali
    sequential_indices = []
    current_sequence = []
    for idx in touch_in_box.index:
        if len(current_sequence) == 0 or idx == current_sequence[-1] + 1:
            current_sequence.append(idx)
        else:
            if len(current_sequence) > 1:
                sequential_indices.append(current_sequence)
            current_sequence = [idx]
    # Aggiungi l'ultima sequenza se necessario
    if len(current_sequence) > 1:
        sequential_indices.append(current_sequence)
    
    #creo la lista che mi servirà per calcolare gli eventi singoli che saranno conteggi anche loro.
    lista_unificata = []
    for lista in sequential_indices:
        lista_unificata += lista
            
    #trova gli indici non sequienziali
    non_sequential_indices= list(set(touch_in_box.index) - set(lista_unificata))
    
    tocchi_inside_area=len(sequential_indices)+len(non_sequential_indices)
    
    touches_in_final_third_conceeded.append(tocchi_inside_area)


    return touches_in_final_third_conceeded


"""Calcolo i tocchi in area concessi."""
def Touches_in_box_conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Creo le liste che mi servono
    touches_box_conceeded=[0 for i in range(len(lista_home))]
    
    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]

    #Splitto le coordinate in x e y per filtrare gli eventi correlati ai tocchi solo in area avversaria.
    #Così calcolo i tocchi in area
    x,y=zip(*tocchi['location'])
    tocchi['x'],tocchi['y']=x,y
    touch_in_box=tocchi[(tocchi['x']>=102)  & (tocchi['y']<=62)  & (tocchi['y']>=18)]
    #Calcolo i tocchi in area concessi
    # Trova gli indici sequenziali
    sequential_indices = []
    current_sequence = []
    for idx in touch_in_box.index:
        if len(current_sequence) == 0 or idx == current_sequence[-1] + 1:
            current_sequence.append(idx)
        else:
            if len(current_sequence) > 1:
                sequential_indices.append(current_sequence)
            current_sequence = [idx]
    # Aggiungi l'ultima sequenza se necessario
    if len(current_sequence) > 1:
        sequential_indices.append(current_sequence)
    
    #creo la lista che mi servirà per calcolare gli eventi singoli che saranno conteggi anche loro.
    lista_unificata = []
    for lista in sequential_indices:
        lista_unificata += lista
            
    #trova gli indici non sequienziali
    non_sequential_indices= list(set(touch_in_box.index) - set(lista_unificata))
    
    tocchi_inside_area=len(sequential_indices)+len(non_sequential_indices)
    
    touches_box_conceeded.append(tocchi_inside_area)


    return touches_box_conceeded


"""Calcolo le Deep Progression Permesse"""
def Deep_Progression_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]

    #Creo le liste che mi servono
    deep_progression_conceeded=[0 for i in range(len(lista_home))]
    
    #Calcolo le deep progression completitions concesse
    dpc=0
    deep_progression=df[ ((df['type_name']=='Carry') | (df['type_name']=='Pass') | (df['type_name']=='Dribble'))]
    for i in range(len(deep_progression)):
        if 80<=deep_progression['location'].iloc[i][0]<102 or ( deep_progression['location'].iloc[i][0]>=102 and  (deep_progression['location'].iloc[i][1]<18 or deep_progression['location'].iloc[i][1]>62)):  
            dpc+=1
        else:
            continue
        
    #Aggiungo alla lista il numero di deep progression 
    deep_progression_conceeded.append(dpc)
    
    return deep_progression_conceeded

"""Calcolo progressioni con cui entro nella 3/4 offensiva,per giocatore"""
def three_quarters_Carries_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]
    
    #Creo la lista che mi serve
    t_q_c_conceeded=[0 for i in range(len(lista_home))]

    #Calcolo i tree quarter carries conceeded.
    carryes=df[(df['type_name']=='Carry')]
    t_q_c=0
    for i in range(len(carryes)):
        if carryes['location'].iloc[i][0]<60 and 60<=carryes['carry_end_location'].iloc[i][0]<90:
            t_q_c+=1
        else:
            continue
        
    t_q_c_conceeded.append(t_q_c)

    return t_q_c_conceeded


"""Calcolo progressioni con cui entro in area concessi"""
def inside_area_Carries_Conceeded(df,lista_home,lista_against):
    #Filtro il df per i giocatori avversari
    df=df[(df['player_name'].isin(lista_against)) & (df['period']<=4)]
    
    #Creo la lista che mi serve
    i_a_c_conceeded=[0 for i in range(len(lista_home))]
    
    #Trovo le portate
    carryes=df[(df['type_name']=='Carry')]
    #Calcolo le portate che entrano in area concesse
    i_a_c=0
    for i in range(len(carryes)):
        if carryes['location'].iloc[i][0]<102 or (carryes['location'].iloc[i][0]>=102 and (carryes['location'].iloc[i][1]<18 or carryes['location'].iloc[i][1]>62)):
            if carryes['carry_end_location'].iloc[i][0]>=102 and 18<=carryes['carry_end_location'].iloc[i][1]<=62:
                i_a_c+=1
        else:
            continue
        
        
    #Aggiungo alla lista
    i_a_c_conceeded.append(i_a_c)
    
    return i_a_c_conceeded

"""calcolo i passaggi, che non sono cross, permessi agli avversari entro 20 metri dalla porta."""
def Deep_Pass_Completions_Conceeded(df,lista_home,lista_against):
    
    dpca_list=[0 for i in range(len(lista_home))]
    dspca_list=[0 for i in range(len(lista_home))]
    dsppca_list=[0 for i in range(len(lista_home))]
    
    Pass=0
    Successfull_Pass=0
    Pass_no_cross=df[(df['type_name']=='Pass')  & (df['pass_cross']!=True) & (df['player_name'].isin(lista_against))] 
    for i in range(len(Pass_no_cross)):
        end_distance=np.sqrt(np.square(120-Pass_no_cross['pass_end_location'].iloc[i][0]) + (np.square(40-Pass_no_cross['pass_end_location'].iloc[i][1])))
        if end_distance<=20:
            Pass+=1
            if pd.isnull(Pass_no_cross['pass_outcome_name'].iloc[i])==True :
                Successfull_Pass+=1
            
    dpca_list.append(Pass)
    dspca_list.append(Successfull_Pass)
    dsppca_list.append(percentage(dspca_list[-1],dpca_list[-1]))
    return dpca_list,dspca_list,dsppca_list




"""calcolo i cross permessi agli avversari entro 20 metri dalla porta."""
def Deep_Cross_Completions_Conceeded(df,lista_home,lista_against):
    
    dcca_list=[0 for i in range(len(lista_home))]
    dscca_list=[0 for i in range(len(lista_home))]
    dscpca_list=[0 for i in range(len(lista_home))]

    Cross=0
    Succesfull_Cross=0

    cross=df[(df['type_name']=='Pass') & (df['pass_cross']==True) & (df['player_name'].isin(lista_against))] 
    for i in range(len(cross)):
        end_distance=np.sqrt(np.square(120-cross['pass_end_location'].iloc[i][0]) + (np.square(40-cross['pass_end_location'].iloc[i][1])))
        if end_distance<=20:
            Cross+=1
            if pd.isnull(cross['pass_outcome_name'].iloc[i])==True :
                Succesfull_Cross+=1
                
                
    dcca_list.append(Cross)
    dscca_list.append(Succesfull_Cross)
    dscpca_list.append(percentage(dscca_list[-1],dcca_list[-1]))
    
    
    return dcca_list,dscca_list,dscpca_list

"""Defensive Macro Stats"""


"""Calcolo il numero di pressioni e contropressioni effettuate per valutare pressing e gegenpressing.
Calcolo la percentuale di pressioni effettuate nella metà campo avversaria,conisderando pressioni e contropress"""

def Pressure_and_Counterpressures_for_player(df,lista):
    p_list=[]#Lista numero pressioni
    cp_list=[]#Lista numero contropressioni
    ph_list=[]#Lista altezza pressioni
    ch_list=[]#Lista altezza contropressioni
    mph_list=[]#Lista altezza media pressioni
    mcph_list=[]#Lista altezza media contropressioni
    op_list=[]#Lista pressioni offensive    
    op_perc_list=[]#Lista percentuale sul totale pressioni offensive  
    
    for p in lista:
        Pressures=0
        Counterpressures=0
        pressure_height=0
        counterpressure_height=0

        press=df[df['player_name']==p]
        for i in range(len(press)):
            if press['type_name'].iloc[i]=='Pressure' and press['counterpress'].iloc[i]!=True:
                
                Pressures+=1
                pressure_height+=press['location'].iloc[i][0]
            elif press['type_name'].iloc[i]=='Pressure' and press['counterpress'].iloc[i]==True:
                
                Counterpressures+=1
                counterpressure_height+=press['location'].iloc[i][0]
                
        p_list.append(Pressures)
        cp_list.append(Counterpressures)
        ph_list.append(pressure_height)
        ch_list.append(counterpressure_height)
                
        #Calculation of mean pressure height
        mean_pressure_height=division(pressure_height,Pressures)

        mph_list.append(mean_pressure_height)
        
        #Calculation of mean counterpressure height
        mean_counterpressure_height=division(counterpressure_height,Counterpressures)

        mcph_list.append(mean_counterpressure_height)
        
        #Calcolo la percentuale di pressioni nella metà campo avversaria
        Pressure=df[(df['type_name']=='Pressure') & (df['player_name']==p) & (df['counterpress']!=True)]
        Total_Pressure=len(Pressure)
        offensive_half_pressure=0
        for b in range(len(Pressure)):
            if Pressure['location'].iloc[b][0]>60:
                offensive_half_pressure+=1
        op_list.append(offensive_half_pressure)
        
        #Calculation of offensive pressure percentage on the total ammount of pressure
        offensive_half_pressure_perc=percentage(offensive_half_pressure,Total_Pressure)
        
        op_perc_list.append(offensive_half_pressure_perc)
    
    """I Calculate Pressure and Conterpressue for Team"""  
    p_list.append(sum(p_list))
    cp_list.append(sum(cp_list))
    ph_list.append(sum(ph_list))
    ch_list.append(sum(ch_list))
    mph_list.append(ph_list[-1]/p_list[-1])
    mcph_list.append(ch_list[-1]/cp_list[-1])
    op_list.append(sum(op_list))
    op_perc_list.append((op_list[-1]/p_list[-1])*100) 

    return p_list,mph_list,cp_list,mcph_list,op_list,op_perc_list



""" Calcolo il numero di palloni recuperati in tutto il campo e l'altezza media dei recuperi, per giocatore"""

def Ball_Recovery_for_player(df,lista):
    columns=list(df.columns)
    b_r_list=[]
    h_list=[]
    m_r_h_list=[]
    for p in lista:
        df_p=df[(df['player_name']==p) & (df['type_name']=='Ball Recovery') ]
        height=0
        B_r=0
        
        if 'ball_recovery_recovery_failure' in columns:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery' and df_p['ball_recovery_recovery_failure'].iloc[i]!=True:
                    B_r+=1
                    height+=df_p['location'].iloc[i][0]

        else:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery':
                    B_r+=len(df_p)
                    height+=df_p['location'].iloc[i][0]

            
        #Calcualation of mean recovery height
        mean_recovery_height=division(height,B_r)
        
        b_r_list.append(B_r)   
        h_list.append(height)   
        m_r_h_list.append(mean_recovery_height)   

    """I Calculate Ball recovery for Team"""  
    b_r_list.append(sum(b_r_list))
    h_list.append(sum(h_list))
    m_r_h_list.append(division(h_list[-1],b_r_list[-1]))        
    
    return b_r_list,m_r_h_list


""" Calcolo il numero di palloni recuperati nella metà campo avversaria."""        
def High_Ball_Recovery_for_player(df,lista):
    columns=list(df.columns)
    h_b_r_lista=[]
    for p in lista:

        df_p=df[(df['player_name']==p) & (df['type_name']=='Ball Recovery') ]
        H_B_r=0
        
        if 'ball_recovery_recovery_failure' in columns:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery' and df_p['ball_recovery_recovery_failure'].iloc[i]!=True and df_p['location'].iloc[i][0]>=60:
                    H_B_r+=1
        else:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery' and df_p['location'].iloc[i][0]>=60:
                    H_B_r+=1
                    
        h_b_r_lista.append(H_B_r)

    """I Calculate High Ball recovery for Team"""  
    
    h_b_r_lista.append(sum(h_b_r_lista))        
    return h_b_r_lista


""" Calcolo il numero di palloni recuperati nell'ultimo terzo di campo."""        
def Ball_Recovery_in_Final_Third_for_player(df,lista):
    columns=list(df.columns)
    b_r_f_t_lista=[]
    for p in lista:

        df_p=df[(df['player_name']==p) & (df['type_name']=='Ball Recovery') ]
        H_B_f_t_r=0
        
        if 'ball_recovery_recovery_failure' in columns:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery' and df_p['ball_recovery_recovery_failure'].iloc[i]!=True and df_p['location'].iloc[i][0]>=80:
                    H_B_f_t_r+=1
        else:
            for i in range(len(df_p)):
                if df_p['type_name'].iloc[i]=='Ball Recovery' and df_p['location'].iloc[i][0]>=80:
                    H_B_f_t_r+=1
                    
        b_r_f_t_lista.append(H_B_f_t_r)

    """I Calculate High Ball recovery for Team"""  
    
    b_r_f_t_lista.append(sum(b_r_f_t_lista))        
    return b_r_f_t_lista



"""Calcolo le palle 
recuperate dalla squadra entro 5 secondi dalla pressione di un giocatore."""
def Pressure_Regains(df,lista,team_name):
    
    from datetime import datetime, timedelta
    
    p_r_lista=[]
    df['timestamp']=pd.to_datetime(df['timestamp'],format='%H:%M:%S.%f')
    #lista=away_list
    #Filtro per player
    for p in lista:
        p_r=0
        #team_name = df.loc[df['player_name'] == p, 'team_name'].iloc[0]
        df_p=df[((df['type_name']=='Pressure') & (df['player_name']==p)) | ((df['type_name']=='Ball Recovery')  & (df['team_name']==team_name) )]
        b_r=df_p[df_p['type_name']=='Ball Recovery']
        #Cerco tutte le pressioni e guardo se entro 5 secondi da quando è avvenuta la sqaudra ha recuperato la palla
        for i in list(b_r.index):
            
            period=df_p['period'].loc[i]
            b_r_time=df_p['timestamp'].loc[i]

            # Trovare la posizione dell'indice cercato nel DataFrame
            posizione = df_p.index.get_loc(i)
            
            # Trovare l'indice precedente utilizzando il metodo iloc
            indice_precedente = df_p.index[posizione - 1]
            
            #Trovo l'evento precedente
            pressure=pd.DataFrame(df_p.loc[indice_precedente]).T
            
            period_pressure=pressure['period'].iloc[0]
            #Controllo sia una pressure
            if pressure['type_name'].iloc[0]=='Pressure' and period_pressure==period:
                
                pressure_time=pressure['timestamp'].iloc[0]
                
                time_diff=(b_r_time-pressure_time).total_seconds()
                
                if time_diff<=5:
                    p_r+=1
                    
        #Aggiungo il conteggio a 
        p_r_lista.append(p_r)         
        
    """Calcolo per tutta la squadra"""
    p_r_lista.append(sum(p_r_lista))      
    
    return p_r_lista




#"""CALCOLO AZIONI DIFENSIVE SQUADRA"""

"""Calcolo numero contrasti fatti e la percentuale dei vinti"""

def Tackles_for_player(df,lista):
    t_n_list=[]
    w_t_list=[]
    t_w_p_list=[]
    for p in lista:
        Duel=df[(df['type_name']=='Duel') & (df['player_name']==p)]
        tackles=Duel[Duel['duel_type_name']=='Tackle']
        tackles_n=0
        won_tackles_n=0
        for i in range(len(tackles)):
            tackles_n+=1
            if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                won_tackles_n+=1
                
        t_n_list.append(tackles_n)
        w_t_list.append(won_tackles_n)
         
        #Calculation of percentage of tackles won on total ammount of tackle
        tackles_won_perc=percentage(won_tackles_n,tackles_n)
            
        t_w_p_list.append(tackles_won_perc)
        
    """I Calculate Tackles for Team"""  
    t_n_list.append(sum(t_n_list))
    w_t_list.append(sum(w_t_list))
    t_w_p_list.append(percentage(w_t_list[-1],t_n_list[-1]))   
       
    return t_n_list,w_t_list,t_w_p_list

"""Calcolo numero contrasti fatti e la percentuale dei vinti in area"""

def Tackles_for_player_inside_area(df,lista):
    t_n_i_a_list=[]
    w_t_i_a_list=[]
    t_w_p_i_a_list=[]
    for p in lista:
        Duel=df[(df['type_name']=='Duel') & (df['player_name']==p)]
        tackles=Duel[Duel['duel_type_name']=='Tackle']
        tackles_n=0
        won_tackles_n=0
        for i in range(len(tackles)):
            tackles_n+=1
            if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                if 0<=tackles['location'].iloc[i][0]<=18 and 18<=tackles['location'].iloc[i][1]<=62:
                    won_tackles_n+=1
                
        t_n_i_a_list.append(tackles_n)
        w_t_i_a_list.append(won_tackles_n)
         
        #Calculation of percentage of tackles won on total ammount of tackle
        tackles_won_perc=percentage(won_tackles_n,tackles_n)
            
        t_w_p_i_a_list.append(tackles_won_perc)
        
    """I Calculate Tackles for Team"""  
    t_n_i_a_list.append(sum(t_n_i_a_list))
    w_t_i_a_list.append(sum(w_t_i_a_list))
    t_w_p_i_a_list.append(percentage(w_t_i_a_list[-1],t_n_i_a_list[-1]))   
       
    return t_n_i_a_list,w_t_i_a_list,t_w_p_i_a_list


"""Calcolo i contrasti fatti nella 3/4 difensiva, centrale e offensiva."""
def Tackles_zones_for_player(df,lista):
    #Creo le liste dove mettere i tackle fatti per le varie zone di campo per ogni player
    d_tq_t_list=[]
    md_tq_t_list=[]
    mo_tq_t_list=[]
    o_tq_t_list=[]
    
    #Creo le liste dove mettere i tackle vinti per le varie zone di campo per ogni player
    s_d_tq_t_list=[]
    s_md_tq_t_list=[]
    s_mo_tq_t_list=[]
    s_o_tq_t_list=[]

    #Creo le liste dove mettere le percentuali dei tackle completati per le varie zone di campo per ogni player
    p_d_tq_t_list=[]
    p_md_tq_t_list=[]
    p_mo_tq_t_list=[]
    p_o_tq_t_list=[]
    
    for p in lista:
        tackles=df[(df['duel_type_name']=='Tackle') & (df['player_name']==p) ] 
        #Calcolo contrasti tentati nelle varie one del campo
        d_tq_t=0#contrasti nei primi 30 metri di campo lontani dalla propria porta.
        md_tq_t=0#contrasti fatti tra i 30 e i 60 metri di campo lontani dalla propria porta.
        mo_tq_t=0#contrasti fatti tra i 60 e i 90 metri di campo lontani dalla propria porta.
        o_tq_t=0#contrasti fatti tra i 90 e i 120 metri di campo lontani dalla propria porta.
        
        #Calcolo contrasti completati nelle varie one del campo
        s_d_tq_t=0#contrasti nei primi 30 metri di campo lontani dalla propria porta.
        s_md_tq_t=0#contrasti fatti tra i 30 e i 60 metri di campo lontani dalla propria porta.
        s_mo_tq_t=0#contrasti fatti tra i 60 e i 90 metri di campo lontani dalla propria porta.
        s_o_tq_t=0#contrasti fatti tra i 90 e i 120 metri di campo lontani dalla propria porta.
        
        for i in range(len(tackles)):
            if tackles['location'].iloc[i][0]<=30:
                d_tq_t+=1
                if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                    s_d_tq_t+=1
            if 30<tackles['location'].iloc[i][0]<=60:
                md_tq_t+=1
                if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                    s_md_tq_t+=1                
            if 60<tackles['location'].iloc[i][0]<=90:
                mo_tq_t+=1
                if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                    s_mo_tq_t+=1     
            if 90<tackles['location'].iloc[i][0]<=120:
                o_tq_t+=1
                if tackles['duel_outcome_name'].iloc[i]=='Success In Play' or tackles['duel_outcome_name'].iloc[i]=='Success Out' or tackles['duel_outcome_name'].iloc[i]=='Won' or tackles['duel_outcome_name'].iloc[i]=='Success':
                    s_o_tq_t+=1  
                    
        #aggiungo alla lista i valori per i vari giocatori dei passaggi fatti.
        d_tq_t_list.append(d_tq_t)
        md_tq_t_list.append(md_tq_t)
        mo_tq_t_list.append(mo_tq_t)
        o_tq_t_list.append(o_tq_t)

        #aggiungo alla lista i valori per i vari giocatori il numero di passaggi riusciti.       
        s_d_tq_t_list.append(s_d_tq_t)
        s_md_tq_t_list.append(s_md_tq_t)
        s_mo_tq_t_list.append(s_mo_tq_t)
        s_o_tq_t_list.append(s_o_tq_t)          
        
        #Calcolo percentuali passaggi completati per ogni zona del campo interessata per ogni giocatore.
        p_d_tq_t=percentage(s_d_tq_t,d_tq_t)

        p_md_tq_t=percentage(s_md_tq_t,md_tq_t)

        p_mo_tq_t=percentage(s_mo_tq_t,mo_tq_t)

        p_o_tq_t=percentage(s_o_tq_t,o_tq_t)

        #aggiungo alla lista i valori per i vari giocatori della percentuale dei passaggi riusciti.      
        p_d_tq_t_list.append(p_d_tq_t)
        p_md_tq_t_list.append(p_md_tq_t)
        p_mo_tq_t_list.append(p_mo_tq_t)
        p_o_tq_t_list.append(p_o_tq_t)  
        
        
    """I Calculate Tackles zone for Team"""  
    #Number of total passes in the different pitch zones
    d_tq_t_list.append(sum(d_tq_t_list))
    md_tq_t_list.append(sum(md_tq_t_list))
    mo_tq_t_list.append(sum(mo_tq_t_list))
    o_tq_t_list.append(sum(o_tq_t_list))

    #Number of total succesfull passes in the different pitch zones
    s_d_tq_t_list.append(sum(s_d_tq_t_list))
    s_md_tq_t_list.append(sum(s_md_tq_t_list))
    s_mo_tq_t_list.append(sum(s_mo_tq_t_list))
    s_o_tq_t_list.append(sum(s_o_tq_t_list))

    #Percentage of succesfull passes on total amount of passes done.    
    p_d_tq_t=percentage(s_d_tq_t_list[-1],d_tq_t_list[-1])

    p_md_tq_t=percentage(s_md_tq_t_list[-1],md_tq_t_list[-1])

    p_mo_tq_t=percentage(s_mo_tq_t_list[-1],mo_tq_t_list[-1])

    p_o_tq_t=percentage(s_o_tq_t_list[-1],o_tq_t_list[-1])        
    
    p_d_tq_t_list.append(p_d_tq_t)
    p_md_tq_t_list.append(p_md_tq_t)
    p_mo_tq_t_list.append(p_mo_tq_t)
    p_o_tq_t_list.append(p_o_tq_t)   
    
    return d_tq_t_list,s_d_tq_t_list,p_d_tq_t_list,md_tq_t_list,s_md_tq_t_list,p_md_tq_t_list,mo_tq_t_list,s_mo_tq_t_list,p_mo_tq_t_list,o_tq_t_list,s_o_tq_t_list,p_o_tq_t_list




"""Calcolo i duelli aerei fatti, vinti e persi e la percentuale di quelli vinti."""
def Aerel_duels_for_player(df,lista):
    columns=list(df.columns)
    a_l_lista=[]
    a_w_lista=[]
    t_a_d_lista=[]
    a_w_p_lista=[]
    
    for p in lista:
        #Calcolo i duelli persi 
        aerial_lost=df[(df['player_name']==p) & (df['duel_type_name']=='Aerial Lost') ]
        a_l=len(aerial_lost)
        a_l_lista.append(a_l)
        #Calcolo i duelli vinti
        if 'shot_aerial_won' in columns:
            shot_aerial_won=df[(df['player_name']==p) &  (df['shot_aerial_won']==True) ]
            s_a_w=len(shot_aerial_won)
        else:
            s_a_w=0
        
        if 'shot_aerial_won' in columns:
            pass_aerial_won=df[(df['player_name']==p) &  (df['pass_aerial_won']==True) ]
            p_a_w=len(pass_aerial_won)

        else:
            p_a_w=0


        if 'clearance_aerial_won' in columns:
            clearance_aerial_won=df[(df['player_name']==p) &  (df['clearance_aerial_won']==True) ]
            c_a_w=len(clearance_aerial_won)
        
        else:
            c_a_w=0

        if 'miscontrol_aerial_won' in columns:
            miscontrol_aerial_won=df[(df['player_name']==p) &  (df['miscontrol_aerial_won']==True) ]
            m_a_w=len(miscontrol_aerial_won)
        
        else:
            m_a_w=0
            
        a_w = s_a_w + p_a_w + c_a_w + m_a_w
        a_w_lista.append(a_w)
        #Calcolo i duelli totali fatti
        t_a_d=a_l+a_w
        t_a_d_lista.append(t_a_d)
        
        #Calcolo la percentuale sul totale dei duelli aerei vinti
        a_w_p=percentage(a_w,t_a_d)
            
        a_w_p_lista.append(a_w_p)

    """I Calculate Aereal Duel for Team"""  
    a_l_lista.append(sum(a_l_lista))
    a_w_lista.append(sum(a_w_lista))
    t_a_d_lista.append(sum(t_a_d_lista))
    
    a_w_p_lista.append(percentage(a_w_lista[-1],t_a_d_lista[-1]))        
    
    return a_l_lista,a_w_lista,t_a_d_lista,a_w_p_lista

"""Calcolo i duelli aerei fatti, vinti e persi e la percentuale di quelli vinti."""
def Aerel_duels_for_player_in_area(df,lista):
    columns=list(df.columns)
    a_l_i_a_lista=[]
    a_w_i_a_lista=[]
    t_a_d_i_a_lista=[]
    a_w_p_i_a_lista=[]
    
    for p in lista:
        a_l=0
        s_a_w=0
        p_a_w=0
        c_a_w=0
        m_a_w=0
        #Calcolo i duelli persi 
        aerial_lost=df[(df['player_name']==p) & (df['duel_type_name']=='Aerial Lost') ]
        for i in range(len(aerial_lost)):
            if 0<=aerial_lost['location'].iloc[i][0]<=18 and 18<=aerial_lost['location'].iloc[i][1]<=62:
                a_l+=1
                
        a_l_i_a_lista.append(a_l)
        #Calcolo i duelli vinti
        if 'shot_aerial_won' in columns:
            shot_aerial_won=df[(df['player_name']==p) &  (df['shot_aerial_won']==True) ]
            for i in range(len(shot_aerial_won)):
                if 0<=shot_aerial_won['location'].iloc[i][0]<=18 and 18<=shot_aerial_won['location'].iloc[i][1]<=62:
                    s_a_w+=1
        else:
            s_a_w=0
        
        if 'shot_aerial_won' in columns:
            pass_aerial_won=df[(df['player_name']==p) &  (df['pass_aerial_won']==True) ]
            for i in range(len(pass_aerial_won)):
                if 0<=pass_aerial_won['location'].iloc[i][0]<=18 and 18<=pass_aerial_won['location'].iloc[i][1]<=62:
                    p_a_w+=1


        else:
            p_a_w=0


        if 'clearance_aerial_won' in columns:
            clearance_aerial_won=df[(df['player_name']==p) &  (df['clearance_aerial_won']==True) ]
            for i in range(len(clearance_aerial_won)):
                if 0<=clearance_aerial_won['location'].iloc[i][0]<=18 and 18<=clearance_aerial_won['location'].iloc[i][1]<=62: 
                    c_a_w+=1
        
        else:
            c_a_w=0

        if 'miscontrol_aerial_won' in columns:
            miscontrol_aerial_won=df[(df['player_name']==p) &  (df['miscontrol_aerial_won']==True) ]
            for i in range(len(miscontrol_aerial_won)):
                if 0<=miscontrol_aerial_won['location'].iloc[i][0]<=18 and 18<=miscontrol_aerial_won['location'].iloc[i][1]<=62:
                    m_a_w+=1
        
        else:
            m_a_w=0
            
        a_w = s_a_w + p_a_w + c_a_w + m_a_w
        a_w_i_a_lista.append(a_w)
        #Calcolo i duelli totali fatti
        t_a_d=a_l+a_w
        t_a_d_i_a_lista.append(t_a_d)
        
        #Calcolo la percentuale sul totale dei duelli aerei vinti
        a_w_p=percentage(a_w,t_a_d)
            
        a_w_p_i_a_lista.append(a_w_p)

    """I Calculate Aereal Duel for Team"""  
    a_l_i_a_lista.append(sum(a_l_i_a_lista))
    a_w_i_a_lista.append(sum(a_w_i_a_lista))
    t_a_d_i_a_lista.append(sum(t_a_d_i_a_lista))
    
    a_w_p_i_a_lista.append(percentage(a_w_i_a_lista[-1],t_a_d_i_a_lista[-1]))        
    
    return a_l_i_a_lista,a_w_i_a_lista,t_a_d_i_a_lista,a_w_p_i_a_lista

"""Calcolo i Dribbling affrontati, dove sei stato superato e quelli fermati"""
def Faced_Dribbling_for_player(df,lista):
    dribbling_subiti=[]
    dribbling_fermati=[]
    dribbling_fermati_perc=[]
    duel_list=[]
    
    #Cerco i dribbling dove un giocatore è stato saltato
    for p in lista:
        player_dribble_past=df[(df['type_name']=='Dribbled Past') & (df['player_name']==p)]
        d_p=len(player_dribble_past)
        dribbling_subiti.append(d_p)
        
        
    #Cerco i dribbling contrastati
    for p in lista:
        d_f=0
        duel_player=df[(df['duel_type_name']=='Tackle') & (df['player_name']==p)]
        #Trovo il numero di tackle fatti entrando in duello:
        attempted_tackle=len(duel_player)
        duel_list.append(attempted_tackle)
        #trovo l'indice
        ind=list(duel_player.index)
        #ora cerco se l'evento prima del duello è un dribbling, se lo è sarà da contare come dribbling fermato.
        for i in ind:
            if df['type_name'].loc[i-1]=='Dribble':
                d_f+=1
            else:
                continue
            
        dribbling_fermati.append(d_f)
    
    #Dribbling affrontati
    dribling_affrontati=[a+b for a,b in zip(dribbling_subiti,dribbling_fermati)]           
    
    #Calcolo la percentuale di dribling fermati
    dribbling_fermati_perc=[percentage(a,b) for a,b in zip(dribbling_fermati,dribling_affrontati)]
    
    #Calcolo i tackle/Dribbled%
    #Penso che a livello concettuale siano i dribbling fermati in % quindi non va calcolato così ma basta la dribbling_fermati_perc
    #Lascio il calcolo nella funzione ma non la metto come return
    tackle_dribble_perc=[percentage(a,b) for a,b in zip(duel_list,dribbling_subiti)]
    
    
    """I Calculate Dribbling for Team"""  
    dribling_affrontati.append(sum(dribling_affrontati))
    dribbling_subiti.append(sum(dribbling_subiti))
    dribbling_fermati.append(sum(dribbling_fermati))
    duel_list.append(sum(duel_list))
    
    #Percentage of dribbling stopped for Team
    tackle_dribble_perc_team=percentage(dribbling_fermati[-1],dribling_affrontati[-1]) #Percentage of Stopped Dribble 
    dribbling_fermati_perc.append(tackle_dribble_perc_team)  
    
    #Tackle/Dribbled% for Team
    tackle_dribble_perc.append(percentage(duel_list[-1],dribbling_subiti[-1])) 

    return dribling_affrontati, dribbling_subiti, dribbling_fermati,dribbling_fermati_perc
            
"""Calcolo i Dribbling affrontati, dove sei stato superato e quelli fermati"""
def Faced_Dribbling_for_player_in_area(df,lista):
    dribbling_subiti_in_area=[]
    dribbling_fermati_in_area=[]
    dribbling_fermati_in_area_perc=[]
    duel_list=[]
    
    #Cerco i dribbling dove un giocatore è stato saltato
    for p in lista:
        d_p=0
        player_dribble_past=df[(df['type_name']=='Dribbled Past') & (df['player_name']==p)]
        for i in range(len(player_dribble_past)):
            if 0<=player_dribble_past['location'].iloc[i][0]<=18 and 18<=player_dribble_past['location'].iloc[i][1]<=62:
                d_p+=1
        dribbling_subiti_in_area.append(d_p)
        
        
    #Cerco i dribbling contrastati
    for p in lista:
        d_f=0
        d_p=0
        duel_player=df[(df['duel_type_name']=='Tackle') & (df['player_name']==p)]
        for i in range(len(duel_player)):
            if 0<=duel_player['location'].iloc[i][0]<=18 and 18<=duel_player['location'].iloc[i][1]<=62:
                d_p+=1

        #Trovo il numero di tackle fatti entrando in duello:
        duel_list.append(d_p)
        #trovo l'indice
        ind=list(duel_player.index)
        #ora cerco se l'evento prima del duello è un dribbling, se lo è sarà da contare come dribbling fermato.
        for i in ind:
            if df['type_name'].loc[i-1]=='Dribble' and 0<=df['location'].iloc[i][0]<=18 and 18<=df['location'].iloc[i][1]<=62:
                d_f+=1
            else:
                continue
            
        dribbling_fermati_in_area.append(d_f)
    
    #Dribbling affrontati
    dribbling_affrontati_in_area=[a+b for a,b in zip(dribbling_subiti_in_area,dribbling_fermati_in_area)]           
    
    #Calcolo la percentuale di dribling fermati
    dribbling_fermati_in_area_perc=[percentage(a,b) for a,b in zip(dribbling_fermati_in_area,dribbling_subiti_in_area)]
    
    #Calcolo i tackle/Dribbled%
    #Penso che a livello concettuale siano i dribbling fermati in % quindi non va calcolato così ma basta la dribbling_fermati_perc
    #Lascio il calcolo nella funzione ma non la metto come return
    tackle_dribble_perc=[percentage(a,b) for a,b in zip(duel_list,dribbling_subiti_in_area)]
    
    
    """I Calculate Dribbling for Team"""  
    dribbling_affrontati_in_area.append(sum(dribbling_affrontati_in_area))
    dribbling_subiti_in_area.append(sum(dribbling_subiti_in_area))
    dribbling_fermati_in_area.append(sum(dribbling_fermati_in_area))
    duel_list.append(sum(duel_list))
    
    #Percentage of dribbling stopped for Team
    tackle_dribble_perc_team=percentage(dribbling_fermati_in_area[-1],dribbling_affrontati_in_area[-1]) #Percentage of Stopped Dribble 
    dribbling_fermati_in_area_perc.append(tackle_dribble_perc_team)  
    
    #Tackle/Dribbled% for Team
    tackle_dribble_perc.append(percentage(duel_list[-1],dribbling_subiti_in_area[-1])) 

    return dribbling_affrontati_in_area, dribbling_subiti_in_area, dribbling_fermati_in_area,dribbling_fermati_in_area_perc

"""Calcolo i dribbling subiti e fermati da un player
def Dribbling_for_player(df,lista):
    d_list=[]
    s_d_list=[]
    st_d_list=[]
    t_d_list=[]
    
    for p in lista:
        dribble=df[(df['type_name']=='Dribble') & (df['player_name']==p)] #DF of the Dribble happened
        Dribble=len(dribble) #Number of Dribble happened
        d_list.append(Dribble)
        
        #Succesfull dribbling
        success_dribble=dribble[dribble['dribble_outcome_name']=='Complete'] #DF of Successfull Dribble
        Success_dribble=len(success_dribble) #Number of Succesfull Dribble
        s_d_list.append(Success_dribble)
        
        #Stopped dribbling
        stopped_dribble=dribble[dribble['dribble_outcome_name']=='Incomplete'] #DF of Stopped Dribble
        Stopped_dribble=len(stopped_dribble) #Number of stopped dribble
        st_d_list.append(Stopped_dribble)
        
        #Percentage of dribbling stopped
        Dribble_tackled=percentage(Stopped_dribble,Dribble) #Percentage of Stopped Dribble 
        t_d_list.append(Dribble_tackled)
        
    #I Calculate Dribbling for Team
    d_list.append(sum(d_list))
    s_d_list.append(sum(s_d_list))
    st_d_list.append(sum(st_d_list))
    
    #Percentage of dribbling stopped
    Dribble_tackled=percentage(st_d_list[-1],d_list[-1]) #Percentage of Stopped Dribble 

    t_d_list.append(Dribble_tackled)     
      
    return d_list,s_d_list,st_d_list,t_d_list
"""


"""Calcolo i tiri e i passaggi bloccati."""
def Blocks_for_player(df,lista,team_name):
    p_b_list=[]
    s_b_list=[]
    for p in lista:
        shot_block=0
        pass_block=0
        for i in range(len(df)):
            if df['type_name'].iloc[i]=='Block' and df['player_name'].iloc[i]==p:
                if df['type_name'].iloc[i-1]=='Shot' and df['team_name'].iloc[i-1]!=team_name:
                    shot_block+=1
                elif df['type_name'].iloc[i-1]=='Pass' and df['team_name'].iloc[i-1]!=team_name:
                    pass_block+=1
                    
        p_b_list.append(pass_block)
        s_b_list.append(shot_block)       
        
    """I Calculate Blocks for Team"""  
    p_b_list.append(sum(p_b_list))
    s_b_list.append(sum(s_b_list))
    return s_b_list,p_b_list

"""Calcolo i tiri e i passaggi bloccati."""
def Blocks_for_player_in_area(df,lista,team_name):
    p_b_i_a_list=[]
    s_b_i_a_list=[]
    for p in lista:
        shot_block=0
        pass_block=0
        for i in range(len(df)):
            if df['type_name'].iloc[i]=='Block' and df['player_name'].iloc[i]==p and 0<=df['location'].iloc[i][0]<=18 and 18<=df['location'].iloc[i][1]<=62:
                if df['type_name'].iloc[i-1]=='Shot' and df['team_name'].iloc[i-1]!=team_name :
                    shot_block+=1
                elif df['type_name'].iloc[i-1]=='Pass' and df['team_name'].iloc[i-1]!=team_name:
                    pass_block+=1
                    
        p_b_i_a_list.append(pass_block)
        s_b_i_a_list.append(shot_block)       
        
    """I Calculate Blocks for Team"""  
    p_b_i_a_list.append(sum(p_b_i_a_list))
    s_b_i_a_list.append(sum(s_b_i_a_list))
    return s_b_i_a_list,p_b_i_a_list

"""Calcolo gli intercetti fatti"""
def Interceptions_for_player(df,lista):
    int_lista=[]
    s_i_lista=[]
    p_s_i_list=[]
    
    for p in lista:
        interceptions=df[(df['type_name']=='Interception') & (df['player_name']==p)] #DF of Interceptions
        intercepts=len(interceptions) #Number of Interceptions Happened
        int_lista.append(intercepts)
        
        
        succesfull_interceptions=interceptions[(interceptions['interception_outcome_name']!='Lost') & (interceptions['interception_outcome_name']!='Lost In Play')] #DF of Interceptions
        Succesfull_interceptions=len(succesfull_interceptions) #Number of Successfull Interceptions
        s_i_lista.append(Succesfull_interceptions)


        p_s_i_list.append(percentage(Succesfull_interceptions, intercepts))
    """I Calculate Interceptions for Team"""  
    int_lista.append(sum(int_lista))   
    s_i_lista.append(sum(s_i_lista))   
    
    p_s_i_list.append(percentage(s_i_lista[-1], int_lista[-1]))
    
    return int_lista,s_i_lista,p_s_i_list

"""Calcolo le spazzate fatte da ogni giocatore"""
def clearance(df,lista):
    clearance_list=[]
    for p in lista:
        clearance=df[(df['type_name']=='Clearance') & (df['player_name']==p)]
        clearance=len(clearance) #Numero di errori che portano ad un tiro o ad una palla recuperata o ecc.
        clearance_list.append(clearance)

    """I Calculate Clearances for Team"""  
    clearance_list.append(sum(clearance_list)) 

    return clearance_list


"""Calcolo le palle contese vinte, cioè le 50/50"""
def fth_fth_for_player(df,lista):
    columns=list(df.columns)
    fth_fth_faced_list=[]
    fth_fth_won_list=[]
    fth_fth_lost_list=[]
    fth_fth_won_perc_list=[]
    for p in lista:
        palyer=df[(df['player_name']==p) & (df['type_name']=='50/50')]
        fth_fth_faced=0
        fth_fth_won=0
        fth_fth_lost=0
        if 'fth_fth_outcome_name' in columns:
            for i in range(len(palyer)):
                fth_fth_faced+=1
                if palyer['50_50_outcome_name'].iloc[i]=='Won' or palyer['50_50_outcome_name'].iloc[i]=='Success To Team':  
                    fth_fth_won+=1
                else:  
                    fth_fth_lost+=1
            fth_fth_won_perc=(fth_fth_won/fth_fth_faced)*100
            
            fth_fth_faced_list.append(fth_fth_faced)
            fth_fth_won_list.append(fth_fth_won)
            fth_fth_lost_list.append(fth_fth_lost)
            fth_fth_won_perc_list.append(fth_fth_won_perc)

        else:
            fth_fth_faced_list=[0 for i in range(len(lista))]
            fth_fth_won_list=[0 for i in range(len(lista))]
            fth_fth_lost_list=[0 for i in range(len(lista))]
            fth_fth_won_perc_list=[0 for i in range(len(lista))]

        
    """I Calculate Clearances for Team"""  
    fth_fth_faced_list.append(sum(fth_fth_faced_list)) 
    fth_fth_won_list.append(sum(fth_fth_won_list)) 
    fth_fth_lost_list.append(sum(fth_fth_lost_list)) 
    fth_fth_won_perc_list.append(sum(fth_fth_won_perc_list)) 

    return fth_fth_faced_list,fth_fth_won_list,fth_fth_lost_list,fth_fth_won_perc_list










"""Calcolo i falli commessi"""

def Fouls_Committed_for_player(df,lista):
    columns=list(df.columns)
    fouls_list=[]
    for p in lista:
        palyer=df[df['player_name']==p]
        fouls=0
        if 'foul_committed_type_name' in columns:
            for i in range(len(palyer)):
                if palyer['type_name'].iloc[i]=='Foul Committed':  
                    if pd.isnull(palyer['foul_committed_type_name'].iloc[i]) == True:
                        fouls += 1
        else:
            for i in range(len(palyer)):
                if palyer['type_name'].iloc[i]=='Foul Committed':
                    fouls+=1
        fouls_list.append(fouls)    
        
    """I Calculate Fouls committed for Team"""  
    fouls_list.append(sum(fouls_list))   
     
    return fouls_list



    

""""Calcolo gli Errori che hanno portato ad un tiro o ad un evento di un portiere o a una palla recuperata.
In generale gli errori sono un controllo sbagliato o una spazzata fatta male."""

def Error_for_player(df,lista):
    error_list=[]
    for p in lista:
        error=df[(df['type_name']=='Error') & (df['player_name']==p)]
        Error=len(error) #Numero di errori che portano ad un tiro o ad una palla recuperata o ecc.
        error_list.append(Error)

    """I Calculate Interceptions for Team"""  
    error_list.append(sum(error_list)) 
    return error_list

