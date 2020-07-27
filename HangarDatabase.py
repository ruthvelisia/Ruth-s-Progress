import pandas as pd
import numpy as np
import datetime
from Workshop import *

class HangarDatabase:
    def __init__(self, H, G, hangar_profile_df):
        self.Cities = {} # workshops in cities
        self.Workshops = {} # all workshops
        self.H = H
        self.G = G
        for b in G:
            self.Cities[b] = np.array([])
            workshop_incity_df = hangar_profile_df[hangar_profile_df['City'] == b]
            for index in workshop_incity_df.index:
                row = workshop_incity_df.loc[index]
                workshop = Workshop(index, row['Workshop Type'], b, row['Slot'], row['Towing time (hour)'], row['Slot Utilization'],row['Slot Effective'])
                self.Workshops[index] = workshop
                self.Cities[b] = np.append(self.Cities[b], workshop)
                
    def UpdateUsedSlot(self, initial_maintenance_status_df):
        for index,row in initial_maintenance_status_df.iterrows():
            self.Workshops[row['Hangar Code']].used_slot += 1
    