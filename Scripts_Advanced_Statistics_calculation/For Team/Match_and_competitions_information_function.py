# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 22:33:10 2022

@author: USR02709
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
from matplotlib.colors import to_rgba
from statsbombpy import sb
from mplsoccer import Pitch, FontManager,VerticalPitch

import seaborn as sns
from matplotlib.cm import get_cmap



def match_information(competition_id,season_id):
    #C:\Users\hp\Desktop\Script python\Calcio\Da modificare\David\statsbomb_data\data
    with open(rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Dati\open-data-master\data\competitions.json') as data_file:
        #print (mypath+'events/'+file)
        competitions = json.load(data_file)
    
    

    
    #encoding="utf8" solo per euro 2020 e forse messi
    #:\Users\hp\Desktop\Script python\Calcio\Da modificare\David\statsbomb_data\data\
    with open(rf'C:\Users\david\OneDrive\Football Analytics\Calcio\Dati e Progetti\Dati\open-data-master\data\matches\{competition_id}\{season_id}.json',  encoding="utf8") as data_file:
        #print (mypath+'events/'+file)
        data = json.load(data_file)
        
        
    file_name=str(season_id)+'.json'    
        
    from pandas import json_normalize
    dfm = json_normalize(data, sep = "_").assign(match_id = file_name[:-5])
    
    lenght=len(data)
    return data,lenght,dfm

    
    
    
    
    