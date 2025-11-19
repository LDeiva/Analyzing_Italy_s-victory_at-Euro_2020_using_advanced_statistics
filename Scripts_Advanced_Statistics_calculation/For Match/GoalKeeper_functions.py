# -*- coding: utf-8 -*-
"""
Created on Sun May  7 21:30:17 2023

@author: USR02709
"""

import pandas as pd
import numpy as np

"""FUNZIONE PER Le divisioni con 0 a denominatore."""
def division(y, x):
    return 0 if x == 0 else y / x

def percentage(y, x):
    return 0 if x == 0 else (y / x)*100

""""Parametri per portiere."""


"""Calcolo lunghezza media passaggi del portiere"""
def gk_Pass_lenght(df,lista):
    gk_list=[]
    pass_lenght_list=[]
    number_of_pass_list=[]
    for p in lista:
        gkpass=df[(df['player_name']==p) & (df['type_name']=='Pass')]
        Pass_lenght=0
        number_of_pass=len(gkpass)
        number_of_pass_list.append(number_of_pass)
        for i in range(len(gkpass)):
            p_l=np.sqrt(np.square(gkpass['pass_end_location'].iloc[i][0]-gkpass['location'].iloc[i][0]) + np.square(gkpass['pass_end_location'].iloc[i][1]-gkpass['location'].iloc[i][1]))
            Pass_lenght+=p_l
        mean_Pass_lenght=division(Pass_lenght,number_of_pass)
        pass_lenght_list.append(Pass_lenght)
        gk_list.append(mean_Pass_lenght)
        
    """Calcolo la lunghezza media dei passaggi per squadra"""
    pass_lenght_list.append(sum(pass_lenght_list))
    number_of_pass_list.append(sum(number_of_pass_list))
    mean_Pass_lenght_team=division(pass_lenght_list[-1],number_of_pass_list[-1])
    gk_list.append(mean_Pass_lenght_team)
    return gk_list

"""Calcolo Rigori Affrontati dal portiere."""
def gk_penalty(df,lista):
    n_p_list=[]#Rigori affrontati
    c_p_list=[]#Rigori segnati\Conceded
    b_p_list=[]#Rigori parati
    f_p_list=[]#Rigori falliti

    #I find for every player df for penalties kick, scored, failed and saved 
    for p in lista:

        failed_penalty=0
        
        for i in range(len(df)):
            if df['goalkeeper_type_name'].iloc[i]=='Shot Faced' and df['player_name'].iloc[i]==p and df['shot_type_name'].iloc[i-1]=='Penalty':
                failed_penalty+=1
            
        bp=df[((df['goalkeeper_type_name']=='Penalty Saved') | (df['goalkeeper_type_name']=='Penalty Saved to Post')) & (df['player_name']==p)]
        blocked_penalty=len(bp)
        
        cp=df[(df['goalkeeper_type_name']=='Penalty Conceded') & (df['player_name']==p)] 
        conceded_penalty=len(cp)
            
        #Rigori affrontati
        faced_penalty=conceded_penalty+blocked_penalty+failed_penalty
        
        
        n_p_list.append(faced_penalty)
        c_p_list.append(conceded_penalty)
        b_p_list.append(blocked_penalty)
        f_p_list.append(failed_penalty)
        
    """I create Penalties list for Team""" 
    n_p_list.append(sum(n_p_list))
    c_p_list.append(sum(c_p_list))
    b_p_list.append(sum(b_p_list))
    f_p_list.append(sum(f_p_list))
        
    return n_p_list,c_p_list,b_p_list,f_p_list



"""Calcolo Tiri Affrontati dal portiere e percentuale parate, non considerando i rigori."""
def gk_saved_percentage(df,lista):
    columns=list(df.columns)
    n_s_list=[]#Tiri affrontati
    n_s_ot_list=[]#Tiri in porta affrontati
    c_g_list=[]#Gol subiti
    b_s_list=[]#Tiri parati
    b_s_ot_list=[]#Tiri in porta parati
    s_p_list=[]#Percentuale parate

    #I find for every player df for penalties kick, scored, failed and saved 
    for p in lista:
        if 'block_save_block' in columns: 
            failed_shot=0
            on_targhet_failed_shot=0
            #Calcolo tiri affrontati che non sono rigori.
            for i in range(len(df)):
                if df['goalkeeper_type_name'].iloc[i]=='Shot Faced' and df['player_name'].iloc[i]==p  and df['shot_type_name'].iloc[i-1]!='Penalty':
                    failed_shot+=1
                    if df['block_save_block'].iloc[i-1]==True:
                        on_targhet_failed_shot+=1
                        
                        
            #Calcolo tiri in porta, considero pure quelli bloccati dal difensore, non vengono considerati i rigori, che non hanno queste definizioni.
            #Ma come definizioni hanno non Shot Saved, ma Penalty saved ecc.
            
            bs=df[((df['goalkeeper_type_name']=='Shot Saved') | (df['goalkeeper_type_name']=='Shot Saved to Post') | (df['goalkeeper_type_name']=='Shot Saved Off T')) & (df['player_name']==p)]
            blocked_shot=len(bs)
            
            cg=df[(df['goalkeeper_type_name']=='Goal Conceded') & (df['player_name']==p)] 
            conceded_goal=len(cg)
                
            #Tiri affrontati
            faced_shot=conceded_goal+blocked_shot+failed_shot

            #Tiri in porta parati
            on_targhet_saved_shot=df[((df['goalkeeper_type_name']=='Shot Saved') | (df['goalkeeper_type_name']=='Shot Saved to Post')) & (df['player_name']==p)]
            blocked_shot_on_targhet=len(on_targhet_saved_shot)


            #Tiri in porta affrontati
            on_targhet_faced_shot=conceded_goal+blocked_shot_on_targhet+on_targhet_failed_shot
            
            
            #Percentuale titi parati.
            #N.B. Si usano solo i tiri in porta per calcolare la %
            perc_saved_shots=percentage((on_targhet_faced_shot-conceded_goal),on_targhet_faced_shot)
            
            n_s_list.append(faced_shot)
            n_s_ot_list.append(on_targhet_faced_shot)
            c_g_list.append(conceded_goal)
            b_s_list.append(blocked_shot)
            b_s_ot_list.append(blocked_shot_on_targhet)
            s_p_list.append(perc_saved_shots)
            
            
        else:
            
            failed_shot=0
            on_targhet_failed_shot=0
            #Calcolo tiri affrontati che non sono rigori.
            for i in range(len(df)):
                if df['goalkeeper_type_name'].iloc[i]=='Shot Faced' and df['player_name'].iloc[i]==p  and df['shot_type_name'].iloc[i-1]!='Penalty':
                    failed_shot+=1
                       
            #Calcolo tiri in porta, considero pure quelli bloccati dal difensore.
           
            bs=df[((df['goalkeeper_type_name']=='Shot Saved') | (df['goalkeeper_type_name']=='Shot Saved to Post') | (df['goalkeeper_type_name']=='Shot Saved Off T')) & (df['player_name']==p)]
            blocked_shot=len(bs)
           
            cg=df[(df['goalkeeper_type_name']=='Goal Conceded') & (df['player_name']==p)] 
            conceded_goal=len(cg)
               
            #Tiri affrontati
            faced_shot=conceded_goal+blocked_shot+failed_shot
           
            #Tiri in porta parati
            on_targhet_saved_shot=df[((df['goalkeeper_type_name']=='Shot Saved') | (df['goalkeeper_type_name']=='Shot Saved to Post')) & (df['player_name']==p)]
            blocked_shot_on_targhet=len(on_targhet_saved_shot) 
           
            #Tiri in porta affrontati
            on_targhet_faced_shot=conceded_goal+blocked_shot_on_targhet
           
            #Percentuale titi parati.
            #N.B. Si usano solo i tiri in porta per calcolare la %
            perc_saved_shots=percentage((on_targhet_faced_shot-conceded_goal),on_targhet_faced_shot)
           
            n_s_list.append(faced_shot)
            n_s_ot_list.append(on_targhet_faced_shot)
            c_g_list.append(conceded_goal)
            b_s_list.append(blocked_shot)
            b_s_ot_list.append(blocked_shot_on_targhet)
            s_p_list.append(perc_saved_shots)
            
     
         
    """I create Penalties list for Team""" 
    n_s_list.append(sum(n_s_list))
    n_s_ot_list.append(sum(n_s_ot_list))
    c_g_list.append(sum(c_g_list))
    b_s_list.append(sum(b_s_list))
    b_s_ot_list.append(sum(b_s_ot_list))
    
    #Percentuale titi parati totale.
    #N.B. Si usano solo i tiri in porta per calcolare la %
    perc_saved_shots=percentage((n_s_ot_list[-1]-c_g_list[-1]),n_s_ot_list[-1])
    s_p_list.append(perc_saved_shots)
        
    return n_s_list,b_s_list,b_s_ot_list,s_p_list,n_s_ot_list,c_g_list

    

    
"""Calcolo il numero di azioni difensive del portiere, per i diversi tipi.
Calcolo pure le azioni fatte in area e fuori area e distanza media interventi."""
def Keeper_Sweeper(df,lista):
    
    claim_list=[]#Prese basse in uscita.
    clear_list=[]#Spazzate di testa o piede.
    punch_list=[]#Spazzate di pugno
    collected_list=[]#Prese alte
    succesfull_collected_list=[]#Prese alte con successo
    collected_percentage_list=[]#Percentuale di prese alte riuscite
    sweep_list=[]#Spazzate totali somma tra clear e punch
    tackle_list=[]#Contrasti fatti dal portiere
    succesfull_tackle_list=[]#Lista tackle con successo
    tackle_percentage_list=[]#Percentuale tackle riusciti
    in_area_action_list=[]#Azioni fatte in area
    out_area_action_list=[]#Azioni fatte fuori area
    defensive_action_lenght_list=[]#Distanza totale azioni fatte nella partita
    mean_defensive_action_lenght_list=[]#Distanza media azioni difensive
    total_actions=[]#Numero totale di interventi difensivi
    failed_col=[]
    
    for p in lista:
        claim=0
        clear=0
        punch=0
        collected=0
        succesfull_collected=0
        failed_collected=0
        tackle=0
        succesfull_tackle=0
        failed_tackle=0
        in_area=0
        out_area=0
        actions_distance=0
        gk=df[df['player_name']==p]
        for i in range(len(gk)):
            #Calcolo le prese
            if gk['goalkeeper_type_name'].iloc[i]=='Collected':
                collected+=1
                actions_distance+=gk['location'].iloc[i][0]
                
                if gk['goalkeeper_outcome_name'].iloc[i]=='Succesfull' or gk['goalkeeper_outcome_name'].iloc[i]=='Collected Twice':
                    succesfull_collected+=1
                else:
                    failed_collected+=1
                    
                    if gk['location'].iloc[i][0]<=18 and 18<=gk['location'].iloc[i][1]<=62:
                        in_area+=1
                    else:
                        out_area+=1
                        
                    
            #Calcolo i Tackle
            if gk['goalkeeper_type_name'].iloc[i]=='Smother':
                tackle+=1
                actions_distance+=gk['location'].iloc[i][0]
                
                if gk['goalkeeper_outcome_name'].iloc[i]=='Success' or gk['goalkeeper_outcome_name'].iloc[i]=='Won':
                    succesfull_tackle+=1
                else:
                    failed_tackle+=1    

                    if gk['location'].iloc[i][0]<=18 and 18<=gk['location'].iloc[i][1]<=62:
                        in_area+=1
                    else:
                        out_area+=1
                
            #Calcolo i clear i punch e le spazzate totali
            if gk['goalkeeper_outcome_name'].iloc[i]=='Clear':
                clear+=1
                actions_distance+=gk['location'].iloc[i][0]
                
                if gk['location'].iloc[i][0]<=18 and 18<=gk['location'].iloc[i][1]<=62:
                    in_area+=1
                else:
                    out_area+=1   
                
            if gk['goalkeeper_type_name'].iloc[i]=='Punch':
                punch+=1
                actions_distance+=gk['location'].iloc[i][0]                
                
                if gk['location'].iloc[i][0]<=18 and 18<=gk['location'].iloc[i][1]<=62:
                    in_area+=1
                else:
                    out_area+=1  

            if gk['goalkeeper_type_name'].iloc[i]=='Claim':
                claim+=1
                actions_distance+=gk['location'].iloc[i][0]                
                
                if gk['location'].iloc[i][0]<=18 and 18<=gk['location'].iloc[i][1]<=62:
                    in_area+=1
                else:
                    out_area+=1  


        """Calcolo somma tra clear e punch i sweep cioè le spazzate totali"""
        sweep=punch+clear
         
        """Calcolo la percentuale di tackle e prese risucite"""
        Succesfull_tackle_perc=percentage(succesfull_tackle,tackle)
        
        Succesfull_collected_perc=percentage(succesfull_collected,collected)
        
        """Calcolo distanza media interventi difensivi"""
        total_action=sweep+collected+tackle+claim
        mean_difensive_distance=division(actions_distance, total_action)
        
         
        """Li aggiungo alle liste"""
        claim_list.append(claim)
        clear_list.append(clear)
        punch_list.append(punch)
        collected_list.append(collected)
        failed_col.append(failed_collected)
        succesfull_collected_list.append(succesfull_collected)
        collected_percentage_list.append(Succesfull_collected_perc)
        sweep_list.append(sweep)
        tackle_list.append(tackle)
        succesfull_tackle_list.append(succesfull_tackle)
        tackle_percentage_list.append(Succesfull_tackle_perc)
        in_area_action_list.append(in_area)
        out_area_action_list.append(out_area)
        defensive_action_lenght_list.append(actions_distance)
        mean_defensive_action_lenght_list.append(mean_difensive_distance)
        total_actions.append(total_action)
        
    """Calcolo valori totali per la squadra dei parametri."""
    claim_list.append(sum(claim_list))
    clear_list.append(sum(clear_list))
    punch_list.append(sum(punch_list))
    collected_list.append(sum(collected_list))
    succesfull_collected_list.append(sum(succesfull_collected_list))
    failed_col.append(sum(failed_col))
    collected_percentage_list.append(percentage(succesfull_collected_list[-1],collected_list[-1]))
    sweep_list.append(sum(sweep_list))
    tackle_list.append(sum(tackle_list))
    succesfull_tackle_list.append(sum(succesfull_tackle_list))
    tackle_percentage_list.append(division(succesfull_tackle_list[-1],tackle_list[-1]))
    in_area_action_list.append(sum(in_area_action_list))
    out_area_action_list.append(sum(out_area_action_list))
    defensive_action_lenght_list.append(sum(defensive_action_lenght_list))
    total_actions.append(sum(total_actions))
    mean_defensive_action_lenght_list.append(division(defensive_action_lenght_list[-1], total_actions[-1]))  
  
    return claim_list,clear_list,punch_list,collected_list,succesfull_collected_list,collected_percentage_list,sweep_list,tackle_list,succesfull_tackle_list,tackle_percentage_list,in_area_action_list,out_area_action_list,total_actions,mean_defensive_action_lenght_list





