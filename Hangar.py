import pandas as pd
import numpy as np
import datetime
from Formula import *

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
        
    def IsCanMaintenance(self, aircraft_registration, city, check_code, start_check_time, limit_time, duration, always_take_if_possible):
        hangar_in_city = self.hangar_df[np.logical_and(self.hangar_df['City'] == city, self.hangar_df[check_code])]
        if (len(hangar_in_city.index) == 0):
            return [False]
        
        allWorkshopSlot = []
        for workshop in hangar_in_city['Workshop'].values:
            if workshop in self.slot_dictionary.keys():
                for workshopSlot in self.slot_dictionary[workshop]:
                    allWorkshopSlot.append(workshopSlot)
        
        allWorkshopSlot_np = np.array(allWorkshopSlot)
        
        emptySlots = allWorkshopSlot_np[np.logical_not(np.isin(allWorkshopSlot_np, self.maintenance_df['Code']))]
        filledSlots = np.setdiff1d(allWorkshopSlot_np, emptySlots)
        
        if(len(emptySlots) > 0):
            # If there's empty slot
            return [True, emptySlots[0], start_check_time]
        else:
            # if no empty slot then search slot that emptied soon
            valid_df = self.maintenance_df[self.maintenance_df['Code'].isin(filledSlots)]
            # Filter by maintenance finish time that earlier than limit time
            valid_df = valid_df[valid_df['To'] <= limit_time]
            # Filter each slot that has the latest schedule
            valid_df = valid_df[['Code', 'To']].groupby('Code').max()
            # Sort from the earliest to from each unique slot
            valid_df = valid_df.sort_values(by=['To'])
            print(valid_df.iloc[0]['To'])
            if(always_take_if_possible):
                return [True, valid_df.index[0], valid_df.iloc[0]['To']]
            elif(Formula.IsTimeEnough(valid_df.iloc[0]['To'], limit_time, duration)):
                return [True, valid_df.index[0], valid_df.iloc[0]['To']]
        
        return [False]
    
    def ForceMaintenance(self, workshop, aircraft_registration, check_id, time_from, time_to):
        if workshop not in self.slot_dictionary.keys():
            return
        
        allWorkshopSlot = self.slot_dictionary[workshop]
        
        allWorkshopSlot_np = np.array(allWorkshopSlot)
        availableSlot = allWorkshopSlot_np[np.logical_not(np.isin(allWorkshopSlot_np, self.maintenance_df['Code']))]
        if (len(availableSlot) == 0):
            self.maintenance_df = self.maintenance_df.append({'Code' : allWorkshopSlot_np[0], 'Registered Aircraft': aircraft_registration, 'Check' : check_id, 'From' : time_from, 'To' : time_to}, ignore_index = True)
        else:
            self.maintenance_df = self.maintenance_df.append({'Code' : availableSlot[0], 'Registered Aircraft': aircraft_registration, 'Check' : check_id, 'From' : time_from, 'To' : time_to}, ignore_index = True)