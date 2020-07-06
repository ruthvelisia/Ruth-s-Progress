# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 14:32:30 2020

@author: evera
"""

import pandas as pd
import numpy as np
import datetime

class Hangar:
    def __init__(self, hangar_dataframe):
        slot_dictionary = {}
        
        allWorkshop = []
        
        for index, row in hangar_dataframe.iterrows():
            allWorkshop = []
            for slot_number in range(row['Slot']):
                allWorkshop.append(row['Workshop'] + "_" + str(slot_number))
            slot_dictionary[row['Workshop']] = allWorkshop
            
        self.hangar_df = hangar_dataframe
        self.slot_dictionary = slot_dictionary
        self.maintenance_df = pd.DataFrame(columns = ['Code','Registered Aircraft', 'Check', 'From', 'To'])
        
    def IsCanMaintenance(self, aircraft_registration, city, check_code, start_check_time, next_flight_time, duration, always_take_if_possible):
        hangar_in_city = self.hangar_df[np.logical_and(self.hangar_df['City'] == city, self.hangar_df[check_code])]
        if (len(hangar_in_city.index) == 0):
            return [False, '']
        
        return [False, '']
    
    def ForceMaintenance(self, workshop, aircraft_registration, check_id, time_from, time_to):
        if workshop not in self.slot_dictionary.keys():
            return
        
        allWorkshopSlot = self.slot_dictionary[workshop]
        
        allWorkshopSlot_np = np.array(allWorkshopSlot)
        availableSlot = allWorkshopSlot_np[np.logical_not(np.isin(allWorkshopSlot_np, self.maintenance_df['Code']))]
        if (len(availableSlot) == 0):
            return
        else:
            self.maintenance_df = self.maintenance_df.append({'Code' : availableSlot[0], 'Registered Aircraft': aircraft_registration, 'Check' : check_id, 'From' : time_from, 'To' : time_to}, ignore_index = True)
        print(self.maintenance_df)