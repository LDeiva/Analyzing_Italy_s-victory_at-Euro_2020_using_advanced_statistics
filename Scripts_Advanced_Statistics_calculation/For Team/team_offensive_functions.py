# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:10:26 2023

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

"""A) Statistiche Tiri e GOL Squadra"""

"""Calcolo gli XG fatti su azione manovrata (Open Play) e su calcio piazzato (Set Piece) per giocatore."""
"""Calcolo pure gli XG per tiro per giocatore"""
def XG_for_player(df,lista):
    #I create lists with only Open Play or Set Piece or Penalty Shots
    opShot=df[(df['type_name']=='Shot') & (df['shot_type_name']=='Open Play')  & (df['period']<=4)] 
    spShot=df[(df['type_name']=='Shot') & ((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off'))  & (df['period']<=4)]
    pShot=df[(df['type_name']=='Shot') & (df['shot_type_name']=='Penalty')  & (df['period']<=4)]
    
    opXG=[]
    spXG=[]
    pXG=[]
    opXGs=[]
    spXGs=[]
    pXGs=[]
    ops=[]
    sps=[]
    ps=[]
    
    for p in lista:
        #Calcolo XG e gli XGs in open play per ogni giocatore
        opshot=opShot[opShot['player_name']==p]#DF con solo i tiri in open play per quel player
        opxg=opshot['shot_statsbomb_xg'].sum()#Somma XG in open playper quel player
        opXG.append(opxg)#Inserisco gli XG in open play per player nella lista
        opS=len(opshot)
        ops.append(opS)
        opXGs.append(opxg/opS)#Calcolo gli XG per tiro  in open play
        
        #Calcolo XG in set piece per ogni giocatore
        spshot=spShot[spShot['player_name']==p]#DF con solo i tiri in set piece per quel player
        spxg=spshot['shot_statsbomb_xg'].sum()#Somma XG in set piece per quel player
        spXG.append(spxg)#Inserisco gli XG in Set Piece nella lista per quel player
        spS=len(spshot)
        sps.append(spS)
        spXGs.append(spxg/spS)#Calcolo gli XG per tiro in set piece
        
        #Calcolo XG Penalty per ogni giocatore
        pshot=pShot[pShot['player_name']==p]#DF con solo i tiri in penalty per quel player
        pxg=pshot['shot_statsbomb_xg'].sum()#Somma XG in in penalty per quel player
        pXG.append(pxg)#Inserisco gli XG in penalty nella lista in penalty per quel player
        pS=len(pShot)
        ps.append(pS)
        pXGs.append(pxg/pS)#Calcolo gli XG per tiro in penalty
    
    #If a Player have nan xg because didn't do a shot, i replace nan with 0.
    for i in range(len(opXGs)):
  
        # replace nan with 0
        if opXGs[i] !=opXGs[i]:
            opXGs[i] = 0
    #If a Player have nan xg because didn't do a shot, i replace nan with 0.
            
    for c in range(len(spXGs)):
 
        # replace nan with 0
        if spXGs[c] !=spXGs[c]:
            spXGs[c] = 0        
    #If a Player have nan xg because didn't do a shot, i replace nan with 0.
            
    for u in range(len(spXGs)):
 
        # replace nan with 0
        if pXGs[u] !=pXGs[u]:
            pXGs[u] = 0  
            
    #Total XG for player without penalty
    nptXG=[x + y for x, y in zip(opXG, spXG)]  #No penalty total xg for player
    nptshots=[z + r for z, r in zip(ops, sps)]  #Total Shots for player without penalty
    nptXGs=[a/b for a, b in zip(nptXG, nptshots)]  #No penalty  total xg for shot for player
    
    #Total XG for player with penalty
    tXG=[x + y for x, y in zip(nptXG, pXG)]  #Total xg
    tshots=[z + r for z, r in zip(nptshots, ps)]  
    tXGs=[a/b for a, b in zip(tXG, tshots)]  #Total xg for shot
    
    """I calculate the Team value for Xg, Shots and XGs"""
    #Team XG
    #XG for Open Play
    TopXG=sum(opXG)
    opXG.append(TopXG)
    #XG for Set Piece  
    TspXG=sum(spXG)
    spXG.append(TspXG)

    #XG for Penalty   
    TpXG=sum(pXG)
    pXG.append(TpXG)

    #No penalty Total XG
    TnpXG=sum(nptXG)
    nptXG.append(TnpXG)
    
    #Total XG
    TXG=sum(tXG)
    tXG.append(TXG)
    
    #Team Shots
    #Shots for Open Play
    TopS=sum(ops)
    ops.append(TopS)
    #Shots for Set Piece
    TspS=sum(sps)
    sps.append(TspS)
    #Shots for Penalty   
    TpS=sum(ps)
    ps.append(TpS)
    #No penalty Total Shots
    TnpS=sum(nptshots)
    nptshots.append(TnpS)
    #Total Shots
    TS=sum(tshots)
    tshots.append(TS)
    
    #Team XG for Shot
    #XGs for Open Play
    TopXGs=TopXG/TopS
    opXGs.append(TopXGs)
    #XGs for Set Piece  
    TspXGs=TspXG/TspS
    spXGs.append(TspXGs)
    #XGs for Penalty   
    TpXGs=TpXG/TpS
    pXGs.append(TpXGs)
    #No penalty Total XGs
    TnpXGs=TnpXG/TnpS
    nptXGs.append(TnpXGs)
    #Total XGs
    TXGs=TXG/TS
    tXGs.append(TXGs) 
    
    return opXG,opXGs,spXG,spXGs,pXG,nptXG,nptXGs,tXG,tXGs




"""Calcolo i tiri fatti su azione (Open Paly) e in calcio piazzato (Set Piece) per ogni giocatore."""
def Shots_for_player(df,lista):
    opShot=df[(df['type_name']=='Shot') & (df['period']<=4) & (df['shot_type_name']=='Open Play')] #DF for shots in Open Play
    spShot=df[(df['type_name']=='Shot') & (df['period']<=4) & ((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off'))]#DF for shots in Set Piece
    pShot=df[(df['shot_type_name']=='Penalty')]
    ops=[]
    sps=[]
    ps=[]
    nps=[]
    ts=[]
    #I calculate shot in OP and in SP for every player
    for p in lista:
        opS=opShot[opShot['player_name']==p]
        opS=len(opS)
        ops.append(opS)

        spS=spShot[spShot['player_name']==p]
        spS=len(spS)
        sps.append(spS)
        
        pS=pShot[pShot['player_name']==p]
        pS=len(pS)
        ps.append(pS)
        
        Nps=opS+spS
        nps.append(Nps)
        
        Ts=opS+spS+pS
        ts.append(Ts)
        
    #I create Team valuem or shots
    ops.append(sum(ops))
    sps.append(sum(sps))
    ps.append(sum(ps))
    nps.append(sum(nps))
    ts.append(sum(ts))

    return ops,sps,ps,nps,ts


"""Calcolo tiri in porta totali e in open play e penalty, per ogni player"""
def shot_on_targhet_for_player(df,lista,defensiveteam):
    columns=list(df.columns)
    npShot=df[(df['type_name']=='Shot') & (df['period']<=4) & (df['shot_type_name']=='Open Play')]
    spShot=df[(df['type_name']=='Shot') & (df['period']<=4) & ((df['shot_type_name']=='Corner') | (df['shot_type_name']=='Free Kick') | (df['shot_type_name']=='Kick Off'))]
    #Contatori per i tiri in open play in set piece e per i penalty.
    shot_ot_op=0
    shot_ot_sp=0
    shot_ot_p=0
    #Liste in cui inserire i tiri in open play in set piece e per i penalty.
    s_ot_op=[]
    s_ot_sp=[]
    s_ot_p=[]
    for p in lista:
        shot_ot_op=0
        shot_ot_sp=0
        shot_ot_p=0

        if 'block_save_block' in columns:
            
            for i in range(len(df)):  
                
                if df['shot_type_name'].iloc[i]=='Open Play' and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):                  
                        shot_ot_op+=1 
    
                    elif df['block_save_block'].iloc[i+1]==True:                   
                        shot_ot_op+=1   
    
                if (df['shot_type_name'].iloc[i]=='Corner' or df['shot_type_name'].iloc[i]=='Free Kick' or df['shot_type_name'].iloc[i]=='Kick Off') and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):

                        shot_ot_sp+=1

                    elif df['block_save_block'].iloc[i+1]==True:
                        shot_ot_sp+=1
      
    
                if df['shot_type_name'].iloc[i]=='Penalty' and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):
                        shot_ot_p+=1                
    
            s_ot_op.append(shot_ot_op)
            s_ot_sp.append(shot_ot_sp)
            s_ot_p.append(shot_ot_p)
            
        else:          
            for i in range(len(df)):  
                
                if df['shot_type_name'].iloc[i]=='Open Play' and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):
                
                        shot_ot_op+=1 
                    else:
                        continue
    
                if (df['shot_type_name'].iloc[i]=='Corner' or df['shot_type_name'].iloc[i]=='Free Kick' or df['shot_type_name'].iloc[i]=='Kick Off') and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):

                        shot_ot_sp+=1
                    else:
                        continue
   
                if df['shot_type_name'].iloc[i]=='Penalty' and df['player_name'].iloc[i]==p and df['period'].iloc[i]<=4:
                    if (df['shot_outcome_name'].iloc[i]=='Goal' or df['shot_outcome_name'].iloc[i]=='Saved' or df['shot_outcome_name'].iloc[i]=='Saved to Post'):
                        shot_ot_p+=1  

            s_ot_op.append(shot_ot_op)
            s_ot_sp.append(shot_ot_sp)
            s_ot_p.append(shot_ot_p)

    tot_s_ot=[a+b+c for a,b,c in zip(s_ot_op,s_ot_sp,s_ot_p)]     
    s_ot_nop=[d+e for d,e in zip(s_ot_op,s_ot_sp)]      
    
    """I create Shot on Targhet for Team"""
    s_ot_op.append(sum(s_ot_op))
    s_ot_sp.append(sum(s_ot_sp))
    s_ot_p.append(sum(s_ot_p))
    tot_s_ot.append(sum(tot_s_ot))
    s_ot_nop.append(sum(s_ot_nop))
    return s_ot_op,s_ot_sp,s_ot_p,s_ot_nop,tot_s_ot


 


"""Calcolo distanza media dei tiri in Open Play, per ogni player"""
def Shots_lenght_for_player(df,lista):
    mean_shot_lenght=[]
    n_s=[]
    s_l_l=[]
    for p in lista:
        shots=df[(df['type_name']=='Shot') & (df['player_name']==p)  & (df['shot_type_name']=='Open Play')  & (df['period']<=4)]
        n_shots=len(shots)
        n_s.append(n_shots)
        shots_lenght=0
        for i in range(len(shots)):
            
            s_l=np.sqrt(np.square(shots['shot_end_location'].iloc[i][0]-shots['location'].iloc[i][0]) + np.square(shots['shot_end_location'].iloc[i][1]-shots['location'].iloc[i][1]))
            shots_lenght+=s_l
        s_l_l.append(shots_lenght)
        
        #If number of shots is 0 the division is impossible for mean shot lenght and i have to impose mean shot lenght=0 manually.

        m_shot_lenght=division(shots_lenght,n_shots)
            
        mean_shot_lenght.append(m_shot_lenght)    
        
    """I create mean Shot Lenght for Team"""  
    t_n_s=sum(n_s)
    t_s_l=sum(s_l_l)
    mean_shot_lenght.append(division(t_s_l,t_n_s))
    return mean_shot_lenght




"""Calcolo numero di tiri da dentro e fuori area considerando solo quelli su azione, per ogni player"""
def Out_and_In_shots_for_player(df,lista):
    inside_list=[]
    outside_list=[]
    #I create dataframe for every Player's Shot
    for p in lista:
        shots=df[(df['type_name']=='Shot') & (df['player_name']==p) & (df['shot_type_name']=='Open Play')  & (df['period']<=4)]
        outside_shots=0
        inside_shots=0
        #I calculate for player shot inside and outside area 
        for i in range(len(shots)):
            if shots['location'].iloc[i][0]>=102 and 18<=shots['location'].iloc[i][1]<=62:
                inside_shots+=1
            else:
                outside_shots+=1
                
        inside_list.append(inside_shots)
        outside_list.append(outside_shots) 
        
    """I create meanInside e Outside Area Shot  for Team""" 
    inside_list.append(sum(inside_list))
    outside_list.append(sum(outside_list))

    return inside_list,outside_list



""" Calcolo il numero di tiri e di gol fatti di piede e di testa e post dribbling per giocatore"""
def Shot_type_for_player(df,lista):
    columns=list(df.columns)
    #List where i am going to put head, foot and after dribbling shots and Gol for every player 
    hs_list=[]
    fs_list=[]
    ds_list=[]
    hg_list=[]
    fg_list=[]
    dg_list=[]
    #I create df for every player for Shots.
    for p in lista:
        shot=df[(df['type_name']=='Shot') & (df['player_name']==p)  & (df['period']<=4)]
        #if in df i have shots after dribbling
        if 'shot_follows_dribble' in columns:
            hs=0
            fs=0
            ds=0
            hg=0
            fg=0
            dg=0    
            #I find different type of shots and goals Right Foot

            for i in range(len(shot)):
                if shot['shot_body_part_name'].iloc[i]=='Head':
                    hs+=1
                    if shot['shot_outcome_name'].iloc[i]=='Goal':
                        hg+=1
                if shot['shot_body_part_name'].iloc[i]=='Right Foot' or shot['shot_body_part_name'].iloc[i]=='Left Foot':
                    fs+=1
                    if shot['shot_outcome_name'].iloc[i]=='Goal':
                        fg+=1
                if shot['shot_follows_dribble'].iloc[i]==True:
                    ds+=1
                    if shot['shot_outcome_name'].iloc[i]=='Goal':
                        dg+=1
            hs_list.append(hs)
            fs_list.append(fs)
            ds_list.append(ds)
            hg_list.append(hg)
            fg_list.append(fg)
            dg_list.append(dg)    
        #If in df these aren't shots after dribbling
        else:
            hs=0
            fs=0
            ds=0
            hg=0
            fg=0
            dg=0
            #I find different type of shots and goals 
            for i in range(len(shot)):
    
                if shot['shot_body_part_name'].iloc[i]=='Head':
                    hs+=1
                    if shot['shot_outcome_name'].iloc[i]=='Goal':
                        hg+=1
                if shot['shot_body_part_name'].iloc[i]=='Right Foot' or shot['shot_body_part_name'].iloc[i]=='Left Foot':
                    fs+=1
                    if shot['shot_outcome_name'].iloc[i]=='Goal':
                        fg+=1
            hs_list.append(hs)
            fs_list.append(fs)
            ds_list.append(ds)
            hg_list.append(hg)
            fg_list.append(fg)
            dg_list.append(dg)       
            
    """I create Shot Type for Team""" 
    hs_list.append(sum(hs_list))
    fs_list.append(sum(fs_list))
    ds_list.append(sum(ds_list))
    hg_list.append(sum(hg_list))
    fg_list.append(sum(fg_list))
    dg_list.append(sum(dg_list))           
    
    return fs_list,fg_list,hs_list,hg_list,ds_list,dg_list



"""Calcolo il numero di gol effettuati in totale, su open play e penalty per ogni player"""
def GOL_for_player(df,lista):
    opg_list=[]
    spg_list=[]
    pg_list=[]
    tg_list=[]
    nonpg_list=[]
    for p in lista:
        #I create df with goal for every player 
        goal=df[(df['shot_outcome_name']=='Goal')  & (df['period']<=4) & (df['player_name']==p)]
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
        opg_list.append(opg)
        spg_list.append(spg)
        pg_list.append(pg)
        tg_list.append(total_goal)
        nonpg_list.append(nonpenalty_goal)
        
    """I create Goal in Open Play, set Peace, non penalty e total for Team""" 
    opg_list.append(sum(opg_list))
    spg_list.append(sum(spg_list))
    pg_list.append(sum(pg_list))
    tg_list.append(sum(tg_list))
    nonpg_list.append(sum(nonpg_list))

    return opg_list,spg_list,pg_list,nonpg_list,tg_list




"""Calcolo i Penalty avuti, segnati, sbagliati e percentuale parati"""         
          
def Penalty_for_player(df,lista):
    #Lists where i put penalties kick, scored, failed and saved for every player.
    n_p_list=[]
    s_p_list=[]
    b_p_list=[]
    f_p_list=[]
    
    #I find for every player df for penalties kick, scored, failed and saved 
    for p in lista:
        
        penalty=df[(df['player_name']==p) & (df['shot_type_name']=='Penalty')]
        number_of_penalty=len(penalty)
        
        scored_penalty=penalty[(penalty['shot_outcome_name']=='Goal')]
        number_of_scored=len(scored_penalty)
        
        blocked_penalty=penalty[(penalty['shot_outcome_name']=='Saved') | (penalty['shot_outcome_name']=='Saved To Post')]
        number_of_blocked=len(blocked_penalty)
        
        failed_penalty=penalty[(penalty['shot_outcome_name']=='Saved Off T') | (penalty['shot_outcome_name']=='Off T') | (penalty['shot_outcome_name']=='Post')]
        number_of_failed=len(failed_penalty)
        
        n_p_list.append(number_of_penalty)
        s_p_list.append(number_of_scored)
        b_p_list.append(number_of_blocked)
        f_p_list.append(number_of_failed)
        
    """I create Penalties list for Team""" 
    n_p_list.append(sum(n_p_list))
    s_p_list.append(sum(s_p_list))
    b_p_list.append(sum(b_p_list))
    f_p_list.append(sum(f_p_list))
    return n_p_list,s_p_list,b_p_list,f_p_list




"""Calcolo il numero di punizioni e i gol fatti da essi, per ogni giocatore"""
def Free_kick_for_player(df,lista):
    #Lists where i put free kick kicked and scored for every player.
    f_k_list=[]
    f_k_g_list=[]
    for p in lista:
        #Calcolo numero punizioni
        punizioni=df[(df['shot_type_name']=='Free Kick') & (df['player_name']==p)  & (df['period']<=4)]
        F_K=len(punizioni)
        f_k_list.append(F_K)
        #Calcolo gol fatti su punizione
        Free_Kick_Goal=punizioni[punizioni['shot_outcome_name']=='Goal']
        F_K_G=len(Free_Kick_Goal)
        f_k_g_list.append(F_K_G)
    """I Calculate Free Kicks and Free Kicks Goals for Team"""   
    f_k_list.append(sum(f_k_list))   
    f_k_g_list.append(sum(f_k_g_list))   

    return f_k_list,f_k_g_list



"""Calcolo i tiri effettuati solo con il portiere a frapporsi tra il tiratore e la porta, per ogni giocatore"""
def clear_shots_for_player(df,lista):
    columns=list(df.columns)
    #List where i put clear shots for every player.
    c_s_list=[]
    for p in lista:
        if 'shot_one_on_one' in columns:
            shot=df[(df['shot_one_on_one']==True) & (df['player_name']==p) & (df['period']<=4)]
            c_s=len(shot)
            c_s_list.append(c_s)
        else:
            c_s=0
            c_s_list.append(c_s)
            
    """I Calculate Clear shots for Team"""       
    c_s_list.append(sum(c_s_list))
    return c_s_list


"""D) Calcolo le statistiche sui Passaggi per ogni giocatore"""

"""Calcolo i Passaggi fatti riuciti, la loro percentuale di riuscita e la distanza media per giocatore."""
def Passes_for_player(df,lista):
    #List where i put pass done, completed, % of completition and average pass distance
    pass_list=[]
    succ_pass_list=[]
    perc_pass_list=[]
    pass_dist=[]
    mean_pass_dist_list=[]
    for p in lista:
        #I calculate number of passes done for every players.
        passaggi=df[(df['type_name']=='Pass') & (df['player_name']==p) ] 
        n_pass=len(passaggi) #Number of passes done
        pass_list.append(n_pass)
        
        #I calculate number of passes completed for every players.
        successful_passes=df[(df['type_name']=='Pass') & (df['player_name']==p) & (pd.isnull(df['pass_outcome_name'])==True) ]
        n_succesfull_passes=len(successful_passes) #Number of passes completed
        succ_pass_list.append(n_succesfull_passes)
        
        #I calculate percentage of completed passes for every players.
        Succesfull_pass_percentage=percentage(n_succesfull_passes,n_pass)
        perc_pass_list.append(Succesfull_pass_percentage)
        
        #I calculate mean average distance for passes for every players.
        distanza_passaggi=sum([x for x in passaggi['pass_length']])
        pass_dist.append(distanza_passaggi)
        
        #If a Player have 0 pass i can't do division for mean pass dist, i replace error with 0.
        average_passes_distance=division(distanza_passaggi,n_pass) #Average distance for passes    
        
        mean_pass_dist_list.append(average_passes_distance)
        
    """I Calculate Pass Stats for Team"""       
    pass_list.append(sum(pass_list))
    succ_pass_list.append(sum(succ_pass_list))
    pass_dist.append(sum(pass_dist))
    
    #If a Player have 0 pass i can't do division for mean pass dist, i replace error with 0.
    average_passes_distance=division(pass_dist[-1],pass_list[-1]) #Average distance for passes    
    
    mean_pass_dist_list.append(average_passes_distance)    
    
    #If a Player have 0 pass i can't do division for succesfull pass percentage, i replace error with 0.
    perc_pass_list.append(percentage(succ_pass_list[-1],pass_list[-1]))
    
    
    return pass_list,succ_pass_list,perc_pass_list,mean_pass_dist_list


"""Calcolo i passaggi sotto pressione"""
def passes_under_pressure(df,lista):
    passes=df[df['type_name']=='Pass']
    passes_under_pressure_list=[]
    succesfull_passes_under_pressure_list=[]
    perc_succesful_passes_under_pressure_list=[]
    for p in lista:
        u_p_pass=passes[(passes['player_name']==p) & (passes['under_pressure']==True)]
        #I calculate number of passes done for every players under pressure.
        n_pass=len(u_p_pass) #Number of passes done under pressure
        passes_under_pressure_list.append(n_pass)
        
        #I calculate number of passes completed for every players under pressure.
        successful_passes_under_pressure=passes[(passes['player_name']==p) & (passes['under_pressure']==True) & (pd.isnull(passes['pass_outcome_name'])==True) ]
        n_succesfull_passes_under_pressure=len(successful_passes_under_pressure) #Number of passes completed under pressure
        succesfull_passes_under_pressure_list.append(n_succesfull_passes_under_pressure)
        
        #I calculate percentage of completed passes for every players.
        Succesfull_pass_percentage_under_pressure=percentage(n_succesfull_passes_under_pressure,n_pass)
        perc_succesful_passes_under_pressure_list.append(Succesfull_pass_percentage_under_pressure)

    """I Calculate Pass Stats for Team"""       
    passes_under_pressure_list.append(sum(passes_under_pressure_list))
    succesfull_passes_under_pressure_list.append(sum(succesfull_passes_under_pressure_list))

    #If a Player have 0 pass i can't do division for succesfull pass percentage, i replace error with 0.
    perc_succesful_passes_under_pressure_list.append(percentage(succesfull_passes_under_pressure_list[-1],passes_under_pressure_list[-1]))

    return passes_under_pressure_list,succesfull_passes_under_pressure_list,perc_succesful_passes_under_pressure_list


"""Calcolo i passaggi nel terzo finale di campo e i passaggi in avanti nella stessa zona di campo"""
def Passes_in_Final_Third(df,lista):
    pass_in_f_t=[]#Passaggi nel terzo di campo offensivo
    succesfull_pass_in_f_t=[]#Passaggi completati nel terzo di campo offensivo
    succesfull_pass_in_f_t_percentage=[]#Percentuale Passaggi completati nel terzo di campo offensivo
    pass_in_f_t_forward=[]#Passaggi in avanti nel terzo di campo offensivo
    succesfull_pass_in_f_t_forward=[]#Passaggi completati in avanti nel terzo di campo offensivo
    succesfull_pass_in_f_t_percentage_forward=[]#Percentuale Passaggi completati in avanti nel terzo di campo offensivo
    pass_in_f_t_forward_percentage=[]#Percentuale Passaggi in avanti rispetto al totale nel terzo di campo offensivo
    
    #Inizio il calcolo per giocatore
    for p in lista:
        player=df[(df['type_name']=='Pass') & (df['player_name']==p)]
        passes=0
        succ_passes=0
        passes_forward=0
        succ_pass_forward=0
        
        for i in range(len(player)):
            if player['location'].iloc[i][0]>80:
                passes+=1
                start_distance=np.sqrt(np.square(120-player['location'].iloc[i][0]) + (np.square(40-player['location'].iloc[i][1])))
                end_distance=np.sqrt(np.square(120-player['pass_end_location'].iloc[i][0]) + (np.square(40-player['pass_end_location'].iloc[i][1])))


                if end_distance<start_distance:
                    passes_forward+=1     
                    
                if pd.isnull(player['pass_outcome_name'].iloc[i])==True:
                    succ_passes+=1
                    if end_distance<start_distance:
                        succ_pass_forward+=1   
        
        #Faccio le percentuali
        s_p_f_t_p=percentage(succ_passes,passes) #Percentuale Passaggi nell'ultimo terzo completati
        s_p_f_t_f_p=percentage(succ_pass_forward,passes_forward) #Percentuale Passaggi in avanti nell'ultimo terzo completati
        p_f_f_t_p=percentage(passes_forward,passes) #Percentuale Passaggi in avanti rispetto al totale
        
        pass_in_f_t.append(passes)
        succesfull_pass_in_f_t.append(succ_passes)
        succesfull_pass_in_f_t_percentage.append(s_p_f_t_p)
        pass_in_f_t_forward.append(passes_forward)
        succesfull_pass_in_f_t_forward.append(succ_pass_forward)
        succesfull_pass_in_f_t_percentage_forward.append(s_p_f_t_f_p)
        pass_in_f_t_forward_percentage.append(p_f_f_t_p)       
    
    #Faccio il calcolo per Team
    pass_in_f_t.append(sum(pass_in_f_t))
    succesfull_pass_in_f_t.append(sum(succesfull_pass_in_f_t))
    succesfull_pass_in_f_t_percentage.append(percentage(succesfull_pass_in_f_t[-1],pass_in_f_t[-1]))
    pass_in_f_t_forward.append(sum(pass_in_f_t_forward))
    succesfull_pass_in_f_t_forward.append(sum(succesfull_pass_in_f_t_forward))
    succesfull_pass_in_f_t_percentage_forward.append(percentage(succesfull_pass_in_f_t_forward[-1],pass_in_f_t_forward[-1]))
    pass_in_f_t_forward_percentage.append(percentage(pass_in_f_t_forward[-1],pass_in_f_t[-1]))       

    return pass_in_f_t,succesfull_pass_in_f_t,succesfull_pass_in_f_t_percentage,pass_in_f_t_forward,succesfull_pass_in_f_t_forward,succesfull_pass_in_f_t_percentage_forward,pass_in_f_t_forward_percentage



"""Calcolo i Passaggi fatti nella 3/4 difensiva, centrale e offensiva, per ogni giocatore."""
def Passes_zones_for_player(df,lista):
    #Creo le liste dove mettere i passaggi fatti per èle varie zone di campo per ogni player
    d_tq_p_list=[]
    md_tq_p_list=[]
    mo_tq_p_list=[]
    o_tq_p_list=[]
    
    #Creo le liste dove mettere i passaggi completatati per le varie zone di campo per ogni player
    s_d_tq_p_list=[]
    s_md_tq_p_list=[]
    s_mo_tq_p_list=[]
    s_o_tq_p_list=[]

    #Creo le liste dove mettere le percentuali dei passaggi completati per le varie zone di campo per ogni player
    p_d_tq_p_list=[]
    p_md_tq_p_list=[]
    p_mo_tq_p_list=[]
    p_o_tq_p_list=[]
    
    for p in lista:
        passaggi=df[(df['type_name']=='Pass') & (df['player_name']==p) ] 
        #Calcolo passaggi tentati nelle varie zone del campo
        d_tq_p=0#Passaggi nei primi 30 metri di campo lontani dalla propria porta.
        md_tq_p=0#Passaggi fatti tra i 30 e i 60 metri di campo lontani dalla propria porta.
        mo_tq_p=0#Passaggi fatti tra i 60 e i 90 metri di campo lontani dalla propria porta.
        o_tq_p=0#Passaggi fatti tra i 90 e i 120 metri di campo lontani dalla propria porta.
        
        #Calcolo passaggi completati nelle varie one del campo
        s_d_tq_p=0#Passaggi nei primi 30 metri di campo lontani dalla propria porta.
        s_md_tq_p=0#Passaggi fatti tra i 30 e i 60 metri di campo lontani dalla propria porta.
        s_mo_tq_p=0#Passaggi fatti tra i 60 e i 90 metri di campo lontani dalla propria porta.
        s_o_tq_p=0#Passaggi fatti tra i 90 e i 120 metri di campo lontani dalla propria porta.
        
        for i in range(len(passaggi)):
            if passaggi['location'].iloc[i][0]<=30 and passaggi['pass_type_name'].iloc[i]!='Goal Kick':
                d_tq_p+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    s_d_tq_p+=1
            if 30<passaggi['location'].iloc[i][0]<=60:
                md_tq_p+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    s_md_tq_p+=1                
            if 60<passaggi['location'].iloc[i][0]<=90:
                mo_tq_p+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    s_mo_tq_p+=1     
            if 90<passaggi['location'].iloc[i][0]<=120:
                o_tq_p+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    s_o_tq_p+=1  
        
        #aggiungo alla lista i valori per i vari giocatori dei passaggi fatti.
        d_tq_p_list.append(d_tq_p)
        md_tq_p_list.append(md_tq_p)
        mo_tq_p_list.append(mo_tq_p)
        o_tq_p_list.append(o_tq_p)

        #aggiungo alla lista i valori per i vari giocatori il numero di passaggi riusciti.       
        s_d_tq_p_list.append(s_d_tq_p)
        s_md_tq_p_list.append(s_md_tq_p)
        s_mo_tq_p_list.append(s_mo_tq_p)
        s_o_tq_p_list.append(s_o_tq_p)                    
        
        #Calcolo percentuali passaggi completati per ogni zona del campo interessata per ogni giocatore.
        #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

        p_d_tq_p=percentage(s_d_tq_p,d_tq_p)
            
        #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

        p_md_tq_p=percentage(s_md_tq_p,md_tq_p)

        #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

        p_mo_tq_p=percentage(s_mo_tq_p,mo_tq_p)

        #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

        p_o_tq_p=percentage(s_o_tq_p,o_tq_p)
            

        #aggiungo alla lista i valori per i vari giocatori della percentuale dei passaggi riusciti.      
        p_d_tq_p_list.append(p_d_tq_p)
        p_md_tq_p_list.append(p_md_tq_p)
        p_mo_tq_p_list.append(p_mo_tq_p)
        p_o_tq_p_list.append(p_o_tq_p)  
        
    """I Calculate Pass Stats for Team"""  
    #Number of total passes in the different pitch zones
    d_tq_p_list.append(sum(d_tq_p_list))
    md_tq_p_list.append(sum(md_tq_p_list))
    mo_tq_p_list.append(sum(mo_tq_p_list))
    o_tq_p_list.append(sum(o_tq_p_list))

    #Number of total succesfull passes in the different pitch zones
    s_d_tq_p_list.append(sum(s_d_tq_p_list))
    s_md_tq_p_list.append(sum(s_md_tq_p_list))
    s_mo_tq_p_list.append(sum(s_mo_tq_p_list))
    s_o_tq_p_list.append(sum(s_o_tq_p_list))

    #Percentage of succesfull passes on total amount of passes done.
    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

    p_d_tq_p=percentage(s_d_tq_p_list[-1],d_tq_p_list[-1])

    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

    p_md_tq_p=percentage(s_md_tq_p_list[-1],md_tq_p_list[-1])

    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

    p_mo_tq_p=percentage(s_mo_tq_p_list[-1],mo_tq_p_list[-1])

    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

    p_o_tq_p=percentage(s_o_tq_p_list[-1],o_tq_p_list[-1])   
        
    p_d_tq_p_list.append(p_d_tq_p)
    p_md_tq_p_list.append(p_md_tq_p)
    p_mo_tq_p_list.append(p_mo_tq_p)
    p_o_tq_p_list.append(p_o_tq_p)   

          
    return d_tq_p_list,s_d_tq_p_list,p_d_tq_p_list,md_tq_p_list,s_md_tq_p_list,p_md_tq_p_list,mo_tq_p_list,s_mo_tq_p_list,p_mo_tq_p_list,o_tq_p_list,s_o_tq_p_list,p_o_tq_p_list






"""Calcolo il numero di passaggi progressivi, la distanza media per passaggio e la distanza totale dei passaggi progressivi.
Li calcolo per singolo giocatore."""
def Progressive_Passes(df,lista):
    
    #List where i put progressive pass done, completed, % of completition and average pass distance.
    p_p_list=[]
    s_p_p_list=[]
    p_p_p_list=[]
    p_d_list=[]
    m_p_d_list=[]
    for p in lista:
        #calculate distance and which passes are progressive_passes for every player.
        Pass=df[(df['type_name']=='Pass') & (df['player_name']==p)]
        progressive_passes=0
        progressive_distance=0
        succesfull_progressive_passes=0
        #Start calculation
        for i in range(len(Pass)):
            
            start_distance=np.sqrt(np.square(120-Pass['location'].iloc[i][0]) + (np.square(40-Pass['location'].iloc[i][1])))
            end_distance=np.sqrt(np.square(120-Pass['pass_end_location'].iloc[i][0]) + (np.square(40-Pass['pass_end_location'].iloc[i][1])))
            Progressive=end_distance/start_distance
            if Progressive<0.75:
                progressive_passes+=1
                #essendo progressive passes ne calcolo il progressive lenght/distanza
                p_l=np.sqrt(np.square(Pass['pass_end_location'].iloc[i][0]-Pass['location'].iloc[i][0]) + np.square(Pass['pass_end_location'].iloc[i][1]-Pass['location'].iloc[i][1]))
                progressive_distance+=p_l
                if  pd.isnull(Pass['pass_outcome_name'].iloc[i])==True:
                    succesfull_progressive_passes+=1
                    
        #Append progressive passes            
        p_p_list.append(progressive_passes)
        #Append succesfull progressive passes
        s_p_p_list.append(succesfull_progressive_passes)
        #Append progressive distance
        p_d_list.append(progressive_distance)
        
        #Append percentage of succesfull progressive passes on the total amount 
        #If a Player have 0 pass i can't do division for percentage of succesfull progressive passes , i replace error with 0.
        succesfull_progressive_passes_perc=percentage(succesfull_progressive_passes,progressive_passes) #Percentage of succesfull progressive passes 
        
        p_p_p_list.append(succesfull_progressive_passes_perc)        
        
        
        #Append mean distance for progressive passes
        #If a Player have 0 progressive passes i can't do division, i replace error with 0.

        mean_progressive_lenght=division(progressive_distance,progressive_passes) #Mean distances for every progressive passes

        m_p_d_list.append(mean_progressive_lenght)
        
    """I Calculate Pass Stats for Team"""     
    #Append progressive passes            
    p_p_list.append(sum(p_p_list))
    #Append succesfull progressive passes
    s_p_p_list.append(sum(s_p_p_list))
    #Append progressive distance
    p_d_list.append(sum(p_d_list))
    
    #Append percentage of succesfull progressive passes on the total amount 
    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
    total_succesfull_progressive_passes_perc=percentage(s_p_p_list[-1],p_p_list[-1]) #Percentage of total succesfull progressive passes 
        
    p_p_p_list.append(total_succesfull_progressive_passes_perc)
    
    #Append mean distance for progressive passes
    #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

    total_mean_progressive_lenght=division(p_d_list[-1],p_p_list[-1]) #Percentage of total mean progressive distance 

    m_p_d_list.append(total_mean_progressive_lenght)          
    
    return p_p_list,s_p_p_list,p_p_p_list,p_d_list,m_p_d_list





"""Calcolo il numero di passaggi brevi, medi e lunghi e i lanci fatti e completati, e la % di riusciti.
Brevi=tra le 4 e 13 yards.
Medi=tra le 13 e 27 yards.
Lunghi=maggiori di 27 yards.
Lanci=maggiori di 35 yards."""

def Passes_type_for_player(df,lista):
    #Creo lista in cui inserire i tipi di passaggi per ogni giocatore.
     s_p_list=[]
     m_p_list=[]
     l_p_list=[]
     l_p_up_list=[]
     l_p_unp_list=[]
     t_p_list=[]
    
    #Creo lista in cui inserire i tipi di passaggi riusciti per ogni giocatore.
     s_s_p_list=[]
     s_m_p_list=[]
     s_l_p_list=[]
     s_l_p_up_list=[]
     s_l_p_unp_list=[]
     s_t_p_list=[]

    #Creo lista in cui inserire la percentuale di risucita per tipo di passaggi per ogni giocatore.
     p_s_p_list=[]
     p_m_p_list=[]
     p_l_p_list=[]  
     p_l_p_up_list=[]
     p_l_p_unp_list=[]
     p_t_p_list=[]
     

     for p in lista:
     
         passes=df[(df['type_name']=='Pass') & (df['player_name']==p)]
         
         short_passes=0
         short_successfull_passes=0
         
         middle_passes=0
         middle_successfull_passes=0
        
         long_passes=0
         long_successfull_passes=0  
         
         long_passes_underpress=0
         long_successfull_passes_underpress=0
         
         long_passes_unpress=0
         long_successfull_passes_unpress=0
         
         throw=0
         succesfull_throw=0
         for i in range(len(passes)):
             
             #Calcolo i passaggi corti
             if 4<passes['pass_length'].iloc[i]<=13:
                 short_passes+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     short_successfull_passes+=1
             #Calcolo i passaggi medi
             if 13<passes['pass_length'].iloc[i]<=27:
                 middle_passes+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     middle_successfull_passes+=1     
                     
             #Calcolo i passaggi lunghi
             if passes['pass_length'].iloc[i]>=27:
                 long_passes+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     long_successfull_passes+=1
                     
             #Calcolo i passaggi lunghi sottopressione
             if passes['pass_length'].iloc[i]>=27 and passes['under_pressure'].iloc[i]==True:
                 long_passes_underpress+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     long_successfull_passes_underpress+=1                     

             #Calcolo i passaggi lunghi non sottopressione
             if passes['pass_length'].iloc[i]>=27 and passes['under_pressure'].iloc[i]!=True:
                 long_passes_unpress+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     long_successfull_passes_unpress+=1   
                     
             #Calcolo i lanci   
             if passes['pass_length'].iloc[i]>=35 and passes['pass_type_name'].iloc[i]!='Goal Kick':
                 throw+=1
                 if pd.isnull(passes['pass_outcome_name'].iloc[i])==True:
                     succesfull_throw+=1
         
                     
         #aggiungo alla lista i valori per i tipi di passaggi per ogni giocatore.
         s_p_list.append(short_passes)
         m_p_list.append(middle_passes)
         l_p_list.append(long_passes)
         l_p_up_list.append(long_passes_underpress)
         l_p_unp_list.append(long_passes_unpress)
         t_p_list.append(throw)
         
         #aggiungo alla lista i valori per i tipi di passaggi completati per ogni giocatore.      
         s_s_p_list.append(short_successfull_passes)
         s_m_p_list.append(middle_successfull_passes)
         s_l_p_list.append(long_successfull_passes)
         s_l_p_up_list.append(long_successfull_passes_underpress)
         s_l_p_unp_list.append(long_successfull_passes_unpress)
         s_t_p_list.append(succesfull_throw)               
                
         #Calcolo percentuali passaggi completati per ogni tipo di passaggio per ogni giocatore.
         #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         short_successfull_passes_perc=percentage(short_successfull_passes,short_passes)
         
         #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         middle_successfull_passes_perc=percentage(middle_successfull_passes,middle_passes)
             
         #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         long_successfull_passes_perc=percentage(long_successfull_passes,long_passes)
         
         #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         long_successfull_passes_underpress_perc=percentage(long_successfull_passes_underpress,long_passes_underpress)

         #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         long_successfull_passes_unpress_perc=percentage(long_successfull_passes_unpress,long_passes_unpress)

         #If a Player have 0 throw i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
         succesfull_throw_perc=percentage(succesfull_throw,throw)

         
         p_s_p_list.append(short_successfull_passes_perc)
         p_m_p_list.append(middle_successfull_passes_perc)
         p_l_p_list.append(long_successfull_passes_perc) 
         p_l_p_up_list.append(long_successfull_passes_underpress_perc)
         p_l_p_unp_list.append(long_successfull_passes_unpress_perc)
         p_t_p_list.append(succesfull_throw_perc)
     
     """I Calculate Pass Stats for Team"""  
    
     #Add to list total number of different type of shots .
     s_p_list.append(sum(s_p_list))
     m_p_list.append(sum(m_p_list))
     l_p_list.append(sum(l_p_list))
     l_p_up_list.append(sum(l_p_up_list))
     l_p_unp_list.append(sum(l_p_unp_list))
     t_p_list.append(sum(t_p_list))
    
     #Add to list total number of different succesfull type of shots .
     s_s_p_list.append(sum(s_s_p_list))
     s_m_p_list.append(sum(s_m_p_list))
     s_l_p_list.append(sum(s_l_p_list))
     s_l_p_up_list.append(sum(s_l_p_up_list))
     s_l_p_unp_list.append(sum(s_l_p_unp_list))
     s_t_p_list.append(sum(s_t_p_list))  

     #Add to list percentage of total succesfull pass type on total amount of different pass type.
     #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     short_successfull_passes_perc=percentage(s_s_p_list[-1],s_p_list[-1])
         
     #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     middle_successfull_passes_perc=percentage(s_m_p_list[-1],m_p_list[-1])
         
     #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     long_successfull_passes_perc=percentage(s_l_p_list[-1],l_p_list[-1])
     
     #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     long_successfull_passes_underpress_perc=percentage(s_l_p_up_list[-1],l_p_up_list[-1])
     
     #If a Player have 0 pass i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     long_successfull_passes_unpress_perc=percentage(s_l_p_unp_list[-1],l_p_unp_list[-1])

     #If a Player have 0 throw i can't do division for percentage of total succesfull progressive passes , i replace error with 0.

     succesfull_throw_perc=percentage(s_t_p_list[-1],t_p_list[-1])
         
     p_s_p_list.append(short_successfull_passes_perc)
     p_m_p_list.append(middle_successfull_passes_perc)
     p_l_p_list.append(long_successfull_passes_perc) 
     p_l_p_up_list.append(long_successfull_passes_underpress_perc)
     p_l_p_unp_list.append(long_successfull_passes_unpress_perc)
     p_t_p_list.append(succesfull_throw_perc)
     
     return s_p_list,s_s_p_list,p_s_p_list,m_p_list,s_m_p_list,p_m_p_list,l_p_list,s_l_p_list,p_l_p_list,l_p_up_list,s_l_p_up_list,p_l_p_up_list,l_p_unp_list,s_l_p_unp_list,p_l_p_unp_list,t_p_list,s_t_p_list,p_t_p_list




"""Calcolo i passaggi chiave cioè quelli che portano ad un tiro"""
def key_passes_for_player(df,lista):
    k_p_list=[]
    for p in lista:
        key_passes=df[(df['pass_shot_assist']==True) & (df['player_name']==p)] #DF contenente i passaggi chiave
        K_P=len(key_passes) #Numero passaggi chiave
        k_p_list.append(K_P)
    
    """I Calculate Key Passes for Team"""  
    k_p_list.append(sum(k_p_list))
    return k_p_list



"""Calcolo i passaggi chiave cioè quelli che portano ad un tiro"""
def key_passes_under_pressure(df,lista):
    u_p_k_p_list=[]
    for p in lista:
        u_p_key_passes=df[(df['pass_shot_assist']==True) & (df['player_name']==p) & (df['under_pressure']==True)] #DF contenente i passaggi chiave
        u_p_K_P=len(u_p_key_passes) #Numero passaggi chiave
        u_p_k_p_list.append(u_p_K_P)
    
    """I Calculate Key Passes for Team"""  
    u_p_k_p_list.append(sum(u_p_k_p_list))
    return u_p_k_p_list



"""Calcolo passaggi filtranti"""
def Through_Ball_for_player(df,lista):
    t_b_list=[]
    s_t_b_list=[]
    p_t_b_list=[]
    
    for p in lista:
        #Calculation of Throught Ball
        Through_Ball=df[(df['pass_technique_name']=='Through Ball') & (df['player_name']==p)] #DF contenente i passaggi chiave
        T_B=len(Through_Ball) #Numero passaggi filtranti
        t_b_list.append(T_B)
        
        #Calculation of Succesfull Throught Ball
        Succesfull_Through_Ball=df[(df['pass_technique_name']=='Through Ball') & (df['player_name']==p) & (pd.isnull(df['pass_outcome_name'])==True)] #DF contenente i passaggi chiave
        s_t_b=len(Succesfull_Through_Ball)
        s_t_b_list.append(s_t_b)
        
        #Calculation of Percentage of Succesfull Throught Ball
        #If a Player have 0 throught ball i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
        succesfull_Through_Ball_perc=percentage(s_t_b,T_B)
            
        p_t_b_list.append(succesfull_Through_Ball_perc)
        
    """I Calculate Throught ball for Team"""  
    t_b_list.append(sum(t_b_list))
    s_t_b_list.append(sum(s_t_b_list))

    #Calculation of Percentage of Succesfull Throught Ball
    #If a Player have 0 throught ball i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
    succesfull_Through_Ball_perc=percentage(s_t_b_list[-1],t_b_list[-1])
    
    p_t_b_list.append(succesfull_Through_Ball_perc)
    
    return t_b_list,s_t_b_list,p_t_b_list

"""Calcolo passaggi filtranti sottopressione"""
def Through_Ball_under_pressure(df,lista):
    u_p_t_b_list=[]
    u_p_s_t_b_list=[]
    u_p_p_t_b_list=[]
    for p in lista:
        #Calculation of Throught Ball
        u_p_Through_Ball=df[(df['pass_technique_name']=='Through Ball') & (df['under_pressure']==True) & (df['player_name']==p)] #DF contenente i passaggi chiave sottopressione
        u_p_T_B=len(u_p_Through_Ball) #Numero passaggi filtranti
        u_p_t_b_list.append(u_p_T_B)
        
        #Calculation of Succesfull Throught Ball
        u_p_Succesfull_Through_Ball=df[(df['pass_technique_name']=='Through Ball') & (df['under_pressure']==True) & (df['player_name']==p) & (pd.isnull(df['pass_outcome_name'])==True)] #DF contenente i passaggi chiave sottopressione
        u_p_s_t_b=len(u_p_Succesfull_Through_Ball)
        u_p_s_t_b_list.append(u_p_s_t_b)
        
        #Calculation of Percentage of Succesfull Throught Ball
        #If a Player have 0 throught ball i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
        u_p_succesfull_Through_Ball_perc=percentage(u_p_s_t_b,u_p_T_B)
            
        u_p_p_t_b_list.append(u_p_succesfull_Through_Ball_perc)
        
    """I Calculate Throught ball for Team"""  
    u_p_t_b_list.append(sum(u_p_t_b_list))
    u_p_s_t_b_list.append(sum(u_p_s_t_b_list))

    #Calculation of Percentage of Succesfull Throught Ball
    #If a Player have 0 throught ball i can't do division for percentage of total succesfull progressive passes , i replace error with 0.
    u_p_succesfull_Through_Ball_perc=percentage(u_p_s_t_b_list[-1],u_p_t_b_list[-1])
    
    u_p_p_t_b_list.append(u_p_succesfull_Through_Ball_perc)
    
    return u_p_t_b_list,u_p_s_t_b_list,u_p_p_t_b_list


"""Calcolo i passaggi che percorrono più di 35 yard in ampiezza del campo."""
def Scambi_for_player(df,lista):
    scambi_list=[]
    succesfull_scambi_list=[]
    percentage_succesfull_scambi_list=[]
    
    for p in lista:
        passaggi=df[(df['type_name']=='Pass') & (df['player_name']==p) & (df['pass_type_name']!='Corner') & (df['position_name']!='Goalkeeper')]
        scambi=0
        successful_scambi=0
        
        #Calcolo i cambi gioco
        for i in range(len(passaggi)):
            distanza=np.abs(passaggi['location'].iloc[i][1]-passaggi['pass_end_location'].iloc[i][1])
            if distanza>35:
                scambi+=1
                if pd.isnull(passaggi['pass_outcome_name'].iloc[i])==True:
                    successful_scambi+=1
            
        scambi_list.append(scambi) 
        succesfull_scambi_list.append(successful_scambi)

        percentage_succesfull_scambi_list.append(percentage(successful_scambi,scambi))
        
    """I Calculate Throught ball for Team"""  
    scambi_list.append(sum(scambi_list))
    succesfull_scambi_list.append(sum(succesfull_scambi_list))

    percentage_succesfull_scambi_list.append(percentage(succesfull_scambi_list[-1],scambi_list[-1]))
    
    return scambi_list,succesfull_scambi_list,percentage_succesfull_scambi_list




"""Calcolo il numero di Corner effettuati"""
def Corners_for_player(df,lista):
    corner_list=[]
    for p in lista:
        corner=df[(df['pass_type_name']=='Corner') & (df['player_name']==p)]
        corners_number=len(corner)
        corner_list.append(corners_number)
        
    """I Calculate corner for Team"""  
    corner_list.append(sum(corner_list))
    
    return corner_list



"""Calcolo i Cross effettuati, quelli compleatati e la loro %"""
def Cross_for_player(df,lista):
    cross_list=[]
    succesfull_cross_list=[]
    percentage_succ_cross_list=[]
    for p in lista:

        cross=df[(df['type_name']=='Pass') & (df['pass_cross']==True) & (df['player_name']==p)]
        Cross=len(cross)
        cross_list.append(Cross)
        
        Successfull_Cross=0
        
        for i in range(len(cross)):
            if pd.isnull(cross['pass_outcome_name'].iloc[i])==True:
                Successfull_Cross+=1
                
        succesfull_cross_list.append(Successfull_Cross)

        percentage_succ_cross_list.append(percentage(Successfull_Cross,Cross))

    """I Calculate Cross Stats for Team"""  
    cross_list.append(sum(cross_list))
    
    succesfull_cross_list.append(sum(succesfull_cross_list))
    
    percentage_succ_cross_list.append(percentage(succesfull_cross_list[-1],cross_list[-1]))
    
    return cross_list,succesfull_cross_list,percentage_succ_cross_list



"""Calcolo i passaggi che partono da fuori area e finiscono in area totali e succesfully"""
def Passes_and_cross_into_the_Box_for_player(df,lista):
    p_b_list=[]
    s_p_b_list=[]
    p_p_b_list=[]
    
    c_b_list=[]
    s_c_b_list=[]
    p_c_b_list=[]
    
    b_c_percentage_list=[]
    
    for p in lista:
        passaggi=df[df['player_name']==p]
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
        
        #Calculation for Box Cross percentage.
        n_p_b=p_b+c_b

        b_c_percentage_list.append(percentage(c_b, n_p_b))
        
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
def Box_Pass_for_player(df,lista):
        pass_area_list=[]
        succ_pass_area_list=[]
        perc_succ_pass_area_list=[]
        
        for p in lista:
            passaggi_in_area=0
            passaggi_in_area_completati=0
            cross_in_area=0
            cross_in_area_completati=0
            passaggi=df[(df['type_name']=='Pass') & (df['player_name']==p)]
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

"""calcolo i passaggi, che non sono cross, permessi agli avversari entro 20 metri dalla porta."""
def Deep_Pass_Completions(df,lista):
    
    dpc_list=[]
    dspc_list=[]
    dsppc_list=[]
    
    for p in lista:
        Pass=0
        Successfull_Pass=0
        Player_Pass_no_cross=df[(df['type_name']=='Pass')  & (df['pass_cross']!=True) & (df['player_name']==p)] 
        for i in range(len(Player_Pass_no_cross)):
            end_distance=np.sqrt(np.square(120-Player_Pass_no_cross['pass_end_location'].iloc[i][0]) + (np.square(40-Player_Pass_no_cross['pass_end_location'].iloc[i][1])))
            if end_distance<=20:
                Pass+=1
                if pd.isnull(Player_Pass_no_cross['pass_outcome_name'].iloc[i])==True :
                    Successfull_Pass+=1
                
        dpc_list.append(Pass)
        dspc_list.append(Successfull_Pass)
        dsppc_list.append(percentage(Successfull_Pass,Pass))
    
    """Faccio i calcoli per la Squadra"""
    dpc_list.append(sum(dpc_list))
    dspc_list.append(sum(dspc_list))
    dsppc_list.append(percentage(dspc_list[-1],dpc_list[-1]))
    
    
    return dpc_list,dspc_list,dsppc_list




"""calcolo i cross permessi agli avversari entro 20 metri dalla porta."""
def Deep_Cross_Completions(df,lista):
    
    dcc_list=[]
    dscc_list=[]
    dscpc_list=[]

    for p in lista:
        player_cross=df[(df['type_name']=='Pass') & (df['pass_cross']==True) & (df['player_name']==p)] 
        Cross=0
        Succesfull_Cross=0
        for i in range(len(player_cross)):
            end_distance=np.sqrt(np.square(120-player_cross['pass_end_location'].iloc[i][0]) + (np.square(40-player_cross['pass_end_location'].iloc[i][1])))
            if end_distance<=20:
                Cross+=1
                if pd.isnull(player_cross['pass_outcome_name'].iloc[i])==True :
                    Succesfull_Cross+=1
                
                
        dcc_list.append(Cross)
        dscc_list.append(Succesfull_Cross)
        dscpc_list.append(percentage(Succesfull_Cross,Cross))
        
    """Faccio i calcoli per la Squadra"""
    dcc_list.append(sum(dcc_list))
    dscc_list.append(sum(dscc_list))
    dscpc_list.append(percentage(dscc_list[-1],dcc_list[-1]))
        
    return dcc_list,dscc_list,dscpc_list







"""Calcolo il numero di rimesse dal fondo quelle completate e la loro percentuale di riuscita"""
def goal_kick_for_player(df,lista):
    g_k_list=[]
    s_g_k_list=[]
    g_k_p_list=[]
    for p in lista:
        Goal_kick=df[(df['pass_type_name']=='Goal Kick') & (df['player_name']==p)] #DF contenente i rinvii dal fondo
        goal_kick=len(Goal_kick)
        g_k_list.append(goal_kick)
        succesfull_goal_kick=0
        for i in range(len(Goal_kick)):   
            if pd.isnull(Goal_kick['pass_outcome_name'].iloc[i])==True:
                succesfull_goal_kick+=1
                
        s_g_k_list.append(succesfull_goal_kick)   


        succesfull_goal_kick_perc=percentage(succesfull_goal_kick,goal_kick)
        
        g_k_p_list.append(succesfull_goal_kick_perc)

    """I Calculate Pass in Box for Team""" 
    g_k_list.append(sum(g_k_list))
    s_g_k_list.append(sum(s_g_k_list))
    g_k_p_list.append(percentage(s_g_k_list[-1],g_k_list[-1]))
        
    return g_k_list,s_g_k_list,g_k_p_list



def ball_receipt_under_pressure(df,lista):
    b_r=df[df['type_name']=='Ball Receipt*']
    b_r_under_pressure_list=[]
    succesfull_b_r_under_pressure=[]
    perc_succesfull_b_r_under_pressure=[]
    for p in lista:
        #Calcolo il numero di palle ricevute sotto pressione
        u_p_b_r=b_r[(b_r['player_name']==p) & (b_r['under_pressure']==True)]
        n_u_p_b_r=len(u_p_b_r)
        b_r_under_pressure_list.append(n_u_p_b_r)
        
        #Calcolo il numero di palle ricevute sotto pressione con successo
        s_u_p_b_r=b_r[(b_r['player_name']==p) & (b_r['under_pressure']==True) & (pd.isnull(b_r['pass_outcome_name'])==True)]
        n_s_u_p_b_r=len(s_u_p_b_r)
        succesfull_b_r_under_pressure.append(n_s_u_p_b_r)       

        #I calculate percentage of completed passes for every players.
        Succesfull_b_r_percentage_under_pressure=percentage(n_s_u_p_b_r,n_u_p_b_r)
        perc_succesfull_b_r_under_pressure.append(Succesfull_b_r_percentage_under_pressure)

    """I Calculate Ball receipt Stats for Team"""       
    b_r_under_pressure_list.append(sum(b_r_under_pressure_list))
    succesfull_b_r_under_pressure.append(sum(succesfull_b_r_under_pressure))

    #If a Player have 0 pass i can't do division for succesfull pass percentage, i replace error with 0.
    perc_succesfull_b_r_under_pressure.append(percentage(succesfull_b_r_under_pressure[-1],b_r_under_pressure_list[-1]))
    
    return b_r_under_pressure_list,succesfull_b_r_under_pressure,perc_succesfull_b_r_under_pressure


"""Indica il numero di passaggi effettuti nel terzo di campo offensivi"""
def Field_Tilt(df,lista):
    fild_tilt_list=[0 for i in range(len(lista[1:]))]
    team=lista[-1]
    Offensive_Pass=0
    Team_Offensive_Pass=0
    for i in range(len(df)):
        if df['type_name'].iloc[i]=='Pass' and df['location'].iloc[i][0]>=80:
            Offensive_Pass+=1
            if df['type_name'].iloc[i]=='Pass' and df['team_name'].iloc[i]==team and df['location'].iloc[i][0]>=80: 
                Team_Offensive_Pass+=1
    Field_Tilt=(Team_Offensive_Pass/Offensive_Pass)*100
    fild_tilt_list.append(Field_Tilt)
    return fild_tilt_list




"""D) Calcolo Statistiche sul possesso palla e dominio territoriale"""

"""Calcolo possesso palla
per definizione tiene conto di TUTTI  i passaggi fatti completati e non"""
def Possession(df,lista):
    possession_percentage=[0 for i in range(len(lista[1:]))]
    Pass=0
    Team_Pass=0
    team=lista[-1]
    for i in range(len(df)):
        if df['type_name'].iloc[i]=='Pass':
            Pass+=1
            if df['type_name'].iloc[i]=='Pass' and df['team_name'].iloc[i]==team: 
                Team_Pass+=1
    Possession_Percentage=(Team_Pass/Pass)*100
    possession_percentage.append(Possession_Percentage)
    return possession_percentage



"""Calcolo i possessi della squadra"""

def possession_number(df,lista):
    possession_number_list=[0 for i in range(len(lista[1:]))]
    team=lista[-1]

    possession=df[df['possession_team_name']==team]
    
    possession_number=possession['possession'].nunique()
    possession_number_list.append(possession_number)
    
    return possession_number_list




"""Calcolo i tocchi di ogni giocatore."""
def Touches_for_players(df,lista):
    player_touch_list=[]
    

    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]
    
    #Calcolo i tocchi per ogni giocatore
    for p in lista:
        player_touch=tocchi[tocchi['player_name']==p]

        # Trova gli indici sequenziali
        sequential_indices = []
        current_sequence = []
        for idx in player_touch.index:
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
        non_sequential_indices= list(set(player_touch.index) - set(lista_unificata))
        
        touch=len(sequential_indices)+len(non_sequential_indices)
        
        player_touch_list.append(touch)
        
    player_touch_list.append(sum(player_touch_list)) 

    return player_touch_list

    

"""Calcolo i tocchi di ogni giocatore nell'ultimo terzo di campo."""
def Touches_for_players_in_final_third(df,lista):
    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]

    #Splitto le coordinate in x e y per filtrare gli eventi correlati ai tocchi solo in area avversaria.
    #Così calcolo i tocchi in area
    player_touch_in_final_third_list=[]
    x,y=zip(*tocchi['location'])
    tocchi['x'],tocchi['y']=x,y
    touch_in_box=tocchi[tocchi['x']>=80]
    #Calcolo i tocchi per ogni giocatore
    for p in lista:
        player_touch_in_box=touch_in_box[touch_in_box['player_name']==p]

        # Trova gli indici sequenziali
        sequential_indices = []
        current_sequence = []
        for idx in player_touch_in_box.index:
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
        non_sequential_indices= list(set(player_touch_in_box.index) - set(lista_unificata))
        
        tocchi_inside_area=len(sequential_indices)+len(non_sequential_indices)
        
        player_touch_in_final_third_list.append(tocchi_inside_area)
    
    player_touch_in_final_third_list.append(sum(player_touch_in_final_third_list))
    
    return player_touch_in_final_third_list



"""Calcolo i tocchi di ogni giocatore."""
def Touches_in_box(df,lista):
    
    #Filtro i df per ottenere gli eventi su cui calcolare i tocchi.
    tocchi=df[(df['type_name']=='Ball Receipt*') | (df['type_name']=='Pass') | (df['type_name']=='Carry') | (df['type_name']=='Shot')  | (df['type_name']=='Dribble')  | (df['type_name']=='Miscontrol')  | (df['type_name']=='Ball Recovery')]

    #Splitto le coordinate in x e y per filtrare gli eventi correlati ai tocchi solo in area avversaria.
    #Così calcolo i tocchi in area
    player_touch_in_box_list=[]
    x,y=zip(*tocchi['location'])
    tocchi['x'],tocchi['y']=x,y
    touch_in_box=tocchi[(tocchi['x']>=102)  & (tocchi['y']<=62)  & (tocchi['y']>=18)]
    #Calcolo i tocchi per ogni giocatore
    for p in lista:
        player_touch_in_box=touch_in_box[touch_in_box['player_name']==p]

        # Trova gli indici sequenziali
        sequential_indices = []
        current_sequence = []
        for idx in player_touch_in_box.index:
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
        non_sequential_indices= list(set(player_touch_in_box.index) - set(lista_unificata))
        
        tocchi_inside_area=len(sequential_indices)+len(non_sequential_indices)
        
        player_touch_in_box_list.append(tocchi_inside_area)
    
    player_touch_in_box_list.append(sum(player_touch_in_box_list))
    
    return player_touch_in_box_list



"""Calcolo quanti dribling ho fatto e quanti in percentuale sono riusciti, per giocatore."""
def Dribbling_for_players(df,lista):
    d_list=[]
    s_d_list=[]
    s_d_p_list=[]
    for p in lista:
        dribbling=df[(df['type_name']=='Dribble') & (df['player_name']==p)]
        suc_dribbling=dribbling[dribbling['dribble_outcome_name']=='Complete']
        d=len(dribbling)
        d_list.append(d)
        s_d=len(suc_dribbling)
        s_d_list.append(s_d)
        
        #Calculation of percentage of succesfull dribbling.
        s_d_p=percentage(s_d,d)
            
        s_d_p_list.append(s_d_p)

    """I Calculate Pass in Box for Team""" 
    d_list.append(sum(d_list))
    s_d_list.append(sum(s_d_list))
    s_d_p_list.append(percentage(s_d_list[-1],d_list[-1]))
    
    return d_list,s_d_list,s_d_p_list
    
  

"""Calcolo il numero di portate, la distanza totale percorsa palla al piede dalla squadra e quella media per portata, per giocatore."""  
def Carry_mean_lenght_for_players(df,lista):
    carry_list=[]
    lenght_list=[]
    mean_lenght_list=[]
    for p in lista:
        carry=df[(df['type_name']=='Carry') & (df['player_name']==p)]
        Carry_Numbers=len(carry['type_name'])
        carry_list.append(Carry_Numbers)
        Lenght=0
        for i in range(len(carry)):
            lenght=np.sqrt(np.square(carry['carry_end_location'].iloc[i][0]-carry['location'].iloc[i][0]) + np.square(carry['carry_end_location'].iloc[i][1]-carry['location'].iloc[i][1]))
            Lenght+=lenght
        lenght_list.append(Lenght)
        
        #Calculation of mean lenght for carries
        mean_lenght=division(Lenght,Carry_Numbers)

        mean_lenght_list.append(mean_lenght)

    """I Calculate Pass in Box for Team""" 
    carry_list.append(sum(carry_list))
    lenght_list.append(sum(lenght_list))
    mean_lenght_list.append(division(lenght_list[-1],carry_list[-1]))
        
    return carry_list,lenght_list,mean_lenght_list
     
    
"""calcolo il numero di progressioni progressivi, la distanza media per passaggio e la distanza totale dei passaggi progressivi, per giocatore."""
def Progressive_Carries_for_players(df,lista):
    p_c_list=[]
    p_c_d_list=[]
    m_p_c_d_list=[]
    for p in lista:
        #calculate distance and which passes are progressive_passes
        Carries=df[(df['type_name']=='Carry') & (df['player_name']==p)]
        progressive_carries=0
        progressive_distance=0
    
        for i in range(len(Carries)):
            
            start_distance=np.sqrt(np.square(120-Carries['location'].iloc[i][0]) + (np.square(40-Carries['location'].iloc[i][1])))
            end_distance=np.sqrt(np.square(120-Carries['carry_end_location'].iloc[i][0]) + (np.square(40-Carries['carry_end_location'].iloc[i][1])))
            Progressive=end_distance/start_distance
            if Progressive<0.75:
                progressive_carries+=1
                #essendo progressive passes ne calcolo il progressive lenght/distanza
                p_l=np.sqrt(np.square(Carries['carry_end_location'].iloc[i][0]-Carries['location'].iloc[i][0]) + np.square(Carries['carry_end_location'].iloc[i][1]-Carries['location'].iloc[i][1]))
                progressive_distance+=p_l
                
        p_c_list.append(progressive_carries)  
        p_c_d_list.append(progressive_distance)
        
        #Calculation of mean progressive distance
        mean_progressive_lenght=division(progressive_distance,progressive_carries)

        m_p_c_d_list.append(mean_progressive_lenght)

    """I Calculate Progressive Carries for Team""" 
    p_c_list.append(sum(p_c_list))
    p_c_d_list.append(sum(p_c_d_list))
    m_p_c_d_list.append(division(p_c_d_list[-1],p_c_list[-1]))
        
    return p_c_list,p_c_d_list,m_p_c_d_list



"""Calcolo progressioni con cui entro nella 3/4 offensiva,per giocatore"""
def three_quarters_Carries_for_players(df,lista):
    t_q_c_list=[]
    for p in lista:
        carryes=df[(df['type_name']=='Carry') & (df['player_name']==p)]
        t_q_c=0
        for i in range(len(carryes)):
            if carryes['location'].iloc[i][0]<60 and 60<=carryes['carry_end_location'].iloc[i][0]<90:
                t_q_c+=1
            else:
                continue
            
        t_q_c_list.append(t_q_c)

    """I Calculate three_quarters_Carries for Team""" 
    t_q_c_list.append(sum(t_q_c_list))

    return t_q_c_list
   


"""Calcolo progressioni con cui entro in area, per giocatore"""
def inside_area_Carries_for_players(df,lista):
    i_a_c_list=[]
    for p in lista:
        carryes=df[(df['type_name']=='Carry') & (df['player_name']==p)]
        i_a_c=0
        for i in range(len(carryes)):
            if carryes['location'].iloc[i][0]<102 or (carryes['location'].iloc[i][0]>=102 and (carryes['location'].iloc[i][1]<18 or carryes['location'].iloc[i][1]>62)):
                if carryes['carry_end_location'].iloc[i][0]>=102 and 18<=carryes['carry_end_location'].iloc[i][1]<=62:
                    i_a_c+=1
            else:
                continue
            
        i_a_c_list.append(i_a_c)

    """I Calculate inside area Carries for Team""" 
    i_a_c_list.append(sum(i_a_c_list))
    
    return i_a_c_list

"""Numero di passaggi, dribbling e carries nell'ultimo terzo di campo."""
def  Deep_Progressions(df,lista):
    d_p_c=[]
    for p in lista:
        dpc=0
        player=df[(df['player_name']==p) & ((df['type_name']=='Carry') | (df['type_name']=='Pass') | (df['type_name']=='Dribble'))]
        for i in range(len(player)):
            if player['location'].iloc[i][0]>80:  
                dpc+=1
            else:
                continue
        d_p_c.append(dpc)
     
    """Le calcolo per il team"""
    d_p_c.append(sum(d_p_c))
    
    return d_p_c
    
                
            
            
            
            
"""Calcolo la posizione media della squadra durante la partita quando è in possesso della palla"""
def Average_center_of_gravity(df,teamname):
#Creo il df con i passaggi completati dalla squadra che mi interessa prima della prima sostituzione
    First_substitution=df[(df['type_name']=='Substitution')]
    time=First_substitution['minute'].min()
    df=df[(df['type_name']=='Pass') & (df['team_name']==teamname)]
    #df=df[df['minute']<time]
    df=df[pd.isnull(df['pass_outcome_name'])==True]

#Spacchetto le coordinate dei passaggi in lista x e lista y  
    x=[]
    y=[]
    for i in range(len(df['location'])):
    
        x.append(df['location'].iloc[i][0])
        y.append(df['location'].iloc[i][1])
    df['x']=x
    df['y']=y        
    # average locations of players

    average_locs_and_count = (df.groupby('player_name').agg({'x': ['mean'], 'y': ['mean', 'count']}))
    average_locs_and_count.columns = ['x', 'y', 'count']    
    
    #Calcolo baricentro medio
    a_c_o_m=average_locs_and_count.agg({'x': ['mean'], 'y': ['mean']})
    
    av=average_locs_and_count.iloc[:,0:2]
    frames=[av,a_c_o_m]
    final=pd.concat(frames)
    ultimo_elemento_originale=final.index[-1]
    nuovo_ultimo_elemento=f'{teamname}'
    final = final.rename(index={ultimo_elemento_originale: nuovo_ultimo_elemento})
    return final


"""Calcolo le palle perse"""
def Lost_Balls_for_players(df,lista):

    l_b_d_list=[]#Perse per dribbling sbagliato.
    l_b_m_list=[]#Perse perchè sbagliato un controllo.
    l_b_di_list=[]#Perse perchè tolta da un tackle avversario.
    l_b_e_list=[]#Persa perchè commetto un errore di qualche genere.
    #Palle perse nella propria metà campo difensiva, le più pericolose quindi, la di davanti sta per defensivezone.
    d_l_b_d_list=[]#Perse per dribbling sbagliato.
    d_l_b_m_list=[]#Perse perchè sbagliato un controllo.
    d_l_b_di_list=[]#Perse perchè tolta da un tackle avversario.
    d_l_b_e_list=[]#Persa perchè commetto un errore di qualche genere.
    #Lista per palle perse totali.
    l_b_list=[]
    d_l_b_list=[]
    for p in lista:
        df_player=df[df['player_name']==p]
        #Palle perse in ogni zona del campo
        l_b_d=0#Perse per dribbling sbagliato.
        l_b_m=0#Perse perchè sbagliato un controllo.
        l_b_di=0#Perse perchè tolta da un tackle avversario.
        l_b_e=0#Persa perchè commetto un errore di qualche genere.
        #Palle perse nella propria metà campo difensiva, le più pericolose quindi, la di davanti sta per defensivezone.
        d_l_b_d=0#Perse per dribbling sbagliato.
        d_l_b_m=0#Perse perchè sbagliato un controllo.
        d_l_b_di=0#Perse perchè tolta da un tackle avversario.
        d_l_b_e=0#Persa perchè commetto un errore di qualche genere.
        for i in range(len(df_player)):
            if df_player['type_name'].iloc[i]=='Dribble' and df_player['dribble_outcome_name'].iloc[i]=='Incomplete':
                l_b_d+=1
                if df_player['location'].iloc[i][0]<60:
                    d_l_b_d+=1
            if df_player['type_name'].iloc[i]=='Miscontrol':
                l_b_m+=1
                if df_player['location'].iloc[i][0]<60:
                    d_l_b_m+=1            
            if df_player['type_name'].iloc[i]=='Dispossessed':
                l_b_di+=1
                if df_player['location'].iloc[i][0]<60:
                    d_l_b_di+=1
            if df_player['type_name'].iloc[i]=='Error':
                l_b_e+=1
                if df_player['location'].iloc[i][0]<60:
                    d_l_b_e+=1 
        #Inserisco nelle liste i parametri
        l_b_d_list.append(l_b_d)
        d_l_b_d_list.append(d_l_b_d)
        l_b_m_list.append(l_b_m)
        d_l_b_m_list.append(d_l_b_m)
        l_b_di_list.append(l_b_di)
        d_l_b_di_list.append(d_l_b_di)
        l_b_e_list.append(l_b_e)
        d_l_b_e_list.append(d_l_b_e)
        #Calcolo somma palle perse
        l_b=l_b_d+l_b_m+l_b_di+l_b_e#palle perse in ogni zona del campo
        d_l_b=d_l_b_d+d_l_b_m+d_l_b_di+d_l_b_e#Palle perse nella propria metà campo difensiva, le più pericolose quindi, la di davanti sta per defensivezone.
        l_b_list.append(l_b)
        d_l_b_list.append(d_l_b)

    """I Calculate Lost Balls for Team"""  
    
    #Add to list total number of lose ball for every type.
    l_b_d_list.append(sum(l_b_d_list))
    d_l_b_d_list.append(sum(d_l_b_d_list))
    l_b_m_list.append(sum(l_b_m_list))
    d_l_b_m_list.append(sum(d_l_b_m_list))
    l_b_di_list.append(sum(l_b_di_list))
    d_l_b_di_list.append(sum(d_l_b_di_list))
    l_b_e_list.append(sum(l_b_e_list))
    d_l_b_e_list.append(sum(d_l_b_e_list)) 
    #For Team Total lost ball offens and in all pitch.
    l_b_list.append(sum(l_b_list))
    d_l_b_list.append(sum(d_l_b_list))
    
    return l_b_d_list,d_l_b_d_list,l_b_m_list,d_l_b_m_list,l_b_di_list,d_l_b_di_list,l_b_e_list,d_l_b_e_list,l_b_list,d_l_b_list



"""calcolo i falli subiti, per giocatore."""

def Fouls_Won_for_players(df,lista):
    columns=list(df.columns)
    fouls_won_list=[]
    for p in lista:
    
        foul=df[df['player_name']==p]
        fouls=0
        if 'foul_won_defensive' in columns:
            for i in range(len(foul)):
                if foul['type_name'].iloc[i]=='Foul Won':  
                    if pd.isnull(df['foul_won_defensive'].iloc[i])==True:
                        fouls+=1
        else:
            for i in range(len(foul)):
                if foul['type_name'].iloc[i]=='Foul Won':
                    fouls+=1
                    
        fouls_won_list.append(fouls)  
        
        
    """I Calculate Fouls Won for Team"""    
    fouls_won_list.append(sum(fouls_won_list))
    return fouls_won_list  



"""Valuta se un giocatore è stato SOSTITUITO o è entrato"""
def Substitution(df,lista):
    df_sub=df[df['type_name']=='Substitution']
    for i in range(len(df_sub)):
        if df_sub['player_name'].iloc[i] in list(lista.index) and df_sub['substitution_replacement_name'].iloc[i] in list(lista.index):
            lista.loc[df_sub['player_name'].iloc[i]]['Substituted']='Out'
            lista.loc[df_sub['substitution_replacement_name'].iloc[i]]['Replaced']='In'
    
    #lista=list(lista['Substituted'])
    return lista
            
            
            
"""Calcolo il tempo di gioco di ogni giocatore e della squadra"""
def Time(df,lista,team_name):

    #Trovo la lista dei giocatori titolari
    start_player=[]
    team=df[df['team_name']==team_name]
    starter=team['tactics_lineup'].iloc[0]
    for i in range(len(starter)):
        p=starter[i]['player']['name']
        start_player.append(p)
        
    #Tempo della partita
    minute_for_team=df[(df['period']<=4)]   
    minute_f_team=minute_for_team['minute'].iloc[-1]

    #Calcolo tempo di gioco dei titolari        
    giocatori_titolari = [elemento for elemento in lista if elemento in start_player]
    times=[]
    for p in giocatori_titolari:
        player=df[(df['player_name']==p) & (df['period']<=4)]
        if player['type_name'].iloc[-1]=='Substitution':
            sub_time=player['minute'].iloc[-1]
            times.append(sub_time)

        else:
            times.append(minute_f_team)

    #Creo df per i tempi dei titolari
    play_time_starter=pd.DataFrame(times,columns=['Match_Time'],index=giocatori_titolari)
    
    
    #Calcolo tempo di gioco dei sostituti
    giocatori_non_titolari = [elemento for elemento in lista if elemento not in start_player]
    times_non_titolari=[]
    for p in giocatori_non_titolari:
        replaced=df[df['substitution_replacement_name']==p]
        replacement_time=replaced['minute'].iloc[0]
        
        player=df[(df['player_name']==p) & (df['period']<=4)]
        if player['type_name'].iloc[-1]=='Substitution':
            sub_time=player['minute'].iloc[-1]
            played_time=sub_time-replacement_time
            
        else:
            played_time=minute_f_team-replacement_time
            

        times_non_titolari.append(played_time)
    
    #Creo df con tempi di gioco dei non titolari
    play_time_non_starter=pd.DataFrame(times_non_titolari,columns=['Match_Time'],index=giocatori_non_titolari)
    
    #Unisco titolari e non titolari
    player_times = pd.concat([play_time_starter, play_time_non_starter], ignore_index=False)
    
    #Li ordino secondo l'indice originale così da poterli inserire nel df con le statistiche
    player_times_ordinato = player_times.reindex(lista)
    
    #Aggiungo tempo di gioco del match
    player_times_ordinato.loc[team_name,'Match_Time']=minute_f_team

    return player_times_ordinato






"""Calcolo il tempo dei giocatori e del Team per tutta la competizione."""
def Time(df_list,team_list,team_name):
    Times=pd.DataFrame(index=team_list)

    for i in range(len(df_list)):

        df=df_list[i]
        
        #Trovo la lista dei giocatori titolari
        start_player=[]
        team=df[df['team_name']==team_name]
        starter=team['tactics_lineup'].iloc[0]
        for a in range(len(starter)):
            p=starter[a]['player']['name']
            start_player.append(p)
            
        #Tempo della partita
        minute_for_team=df[(df['period']<=4)]   
        minute_f_team=minute_for_team['minute'].iloc[-1]
        
        #Trovo la lista dei giocatori presenti nel match per la squadre che mi interessa 
        team=df[df['team_name']==team_name]
        lista=list(team['player_name'].unique())
        lista = [x for x in lista if x == x]
        #Calcolo tempo di gioco dei titolari        
        giocatori_titolari = [elemento for elemento in lista if elemento in start_player]
        times=[]
        for p in giocatori_titolari:
            player=df[(df['player_name']==p) & (df['period']<=4)]
            if player['type_name'].iloc[-1]=='Substitution':
                sub_time=player['minute'].iloc[-1]
                times.append(sub_time)

            else:
                times.append(minute_f_team)

        #Creo df per i tempi dei titolari
        play_time_starter=pd.DataFrame(times,columns=[f'Time_Match_{i}'],index=giocatori_titolari)
        
        
        #Calcolo tempo di gioco dei sostituti
        giocatori_non_titolari = [elemento for elemento in lista if elemento not in start_player]
        times_non_titolari=[]
        for p in giocatori_non_titolari:
            replaced=df[df['substitution_replacement_name']==p]
            replacement_time=replaced['minute'].iloc[0]
            
            player=df[(df['player_name']==p) & (df['period']<=4)]
            if player['type_name'].iloc[-1]=='Substitution':
                sub_time=player['minute'].iloc[-1]
                played_time=sub_time-replacement_time
                
            else:
                played_time=minute_f_team-replacement_time
                

            times_non_titolari.append(played_time)
        
        #Creo df con tempi di gioco dei non titolari
        play_time_non_starter=pd.DataFrame(times_non_titolari,columns=[f'Time_Match_{i}'],index=giocatori_non_titolari)
        
        #Unisco titolari e non titolari
        player_times = pd.concat([play_time_starter, play_time_non_starter], ignore_index=False)
        
        #Li ordino secondo l'indice originale così da poterli inserire nel df con le statistiche
        player_times_ordinato = player_times.reindex(lista)
        Times= Times.join(player_times_ordinato[f'Time_Match_{i}'])
        #Times = Times.merge(player_times_ordinato[[f'Time_Match_{i}']], left_index=True, right_index=True, how='left')
        #Aggiungo tempo di gioco del match
        Times.loc[team_name,f'Time_Match_{i}']=minute_f_team
    Times['Time']=Times.sum(axis=1)

    return Times