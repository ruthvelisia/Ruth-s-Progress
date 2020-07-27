# -*- coding: utf-8 -*-
import pandas as pd
import itertools as it 
import sys
import gurobipy as gp
import math
from gurobipy import *
import datetime
from datetime import date
from datetime import timedelta
import calendar
import numpy as np
from InitialData import *
from Aircraft import *
from AircraftDatabase import *
from Workshop import *
from HangarDatabase import *
from Maintenance import *
from MaintenanceDatabase import *
from Schedule import *
#from Formula import *
#from ScehduleDatabase import *
from MIP Gurobi (sample) import *

initial_data = InitialData()
initial_data.LoadAllFile()

#Sample
I = ['PK-GLA', 'PK-GMN', 'PK-GAK']
K = ['A', 'C']
D = initial_data.initial_flight_schedule_df['End Date'].unique() #calendar day indicator
CITY = initial_data.hangar_profile_df['City'].unique()
H = initial_data.hangar_profile_df.index.values
INTV =  ['FH', 'FC', 'DY'] #set of interval types
NO = list(range(1, 400))
D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
F = ['CGK', 'KNO', 'BDO', 'AMQ'] #set of node a
G = ['DPS', 'SUB', 'PDG', 'SOQ'] #set of node b

aircraft_database = AircraftDatabase(I, initial_data.aircraft_profile_df)
aircraft_database.UpdatePerDayData(D, initial_data.aircraft_profile_df, initial_data.aircraft_status_df, initial_data.initial_flight_schedule_df)
aircraft_database.UpdateLimitMaintenanceData(K, initial_data.aircraft_profile_df, initial_data.interval_limitation_df)
aircraft_database.UpdateAverageUtilizationData(initial_data.aircraft_profile_df)
aircraft_database.UpdateIntervalCheckData(K, initial_data.aircraft_profile_df, initial_data.maintenance_interval_df)    
aircraft_database.UpdateLastMaintenance(K, initial_data.last_maintenance_status_df)

hangar_database = HangarDatabase(H,CITY, initial_data.hangar_profile_df)
hangar_database.UpdateUsedSlot(initial_data.initial_maintenance_status_df)

maintenance_database = MaintenanceDatabase(T, K)
maintenance_database.UpdateMaintenanceDuration(initial_data.maintenance_data_df)


#Initial Urgency Rate
urgency_rate_var = 
urgency_rate_var =

#Update schedule
class FlyingStatus:
    def __init__(self, I, aircraft_profile_df):
        self.Aircrafts = {}
        self.I = I
        for i in I:
            self.Aircrafts[i] = Aircraft(i, aircraft_profile_df.loc[i]['Type'])
    
    def UpdatePerDayData(self, D, aircraft_profile_df, aircraft_status_df, initial_flight_schedule_df):
        #self.status_per_day_df = pd.DataFrame(columns=['Date', 'Registration', 'FH', 'FC', 'FD','Start Location', 'End Location', 'Stay Duration', 'Possible Maintenance Location'])

        #Initial FH/FC
        for i in self.I:
            self.Aircrafts[i].Sum_FH_Util = aircraft_status_df.loc[i]['Initial FH']
            self.Aircrafts[i].Sum_FC_Util = aircraft_status_df.loc[i]['Initial FC']

        #Scheduling
        for d in D:
            one_day_schedule = initial_flight_schedule_df[initial_flight_schedule_df['End Date'] == d]
            for i in self.I:
                schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
                sum_schedule = schedule_aircraft_per_day.sum()
                self.Aircrafts[i].Sum_FH_Util += sum_schedule['Util FH']
                self.Aircrafts[i].Sum_FC_Util += sum_schedule['Util FC']
                self.Aircrafts[i].FH[d] = self.Aircrafts[i].Sum_FH_Util
                self.Aircrafts[i].FC[d] = self.Aircrafts[i].Sum_FC_Util
                self.Aircrafts[i].FD[d] = (pd.Timestamp(d) - aircraft_profile_df.loc[i]['Original C of A']).days
                
                if(len(schedule_aircraft_per_day.index) > 0): # Aircraft i has flight on day d
                    latest_schedule = schedule_aircraft_per_day.sort_values(by='Chox on time', ascending=False).iloc[0]
                    #if(len(schedule_aircraft_per_day.index) > 1):
                    #    print("Aircraft " + self.Aircrafts[i].i + " double flight on " + str(d) + " latest : " + str(latest_schedule['Chox on time']))
                    self.Aircrafts[i].start_time[d] = pd.to_datetime(str(latest_schedule['Start Date']) + " " + str(latest_schedule['Chox off time']))
                    self.Aircrafts[i].end_time[d] = pd.to_datetime(str(latest_schedule['End Date']) + " " + str(latest_schedule['Chox on time']))
                    self.Aircrafts[i].start_loc[d] = latest_schedule['Start Loc']
                    self.Aircrafts[i].end_loc[d] = latest_schedule['End Loc']
                    self.Aircrafts[i].stay_duration[d] = latest_schedule['Duration']
                    self.Aircrafts[i].possible_maint_loc[d] = latest_schedule['Maint Station']
                else: # Aircraft i doesn't have flight on day d
                    #print("Aircraft " + self.Aircrafts[i].i + " Doesn't fly on " + str(d))
                    self.Aircrafts[i].start_time[d] =  np.nan
                    self.Aircrafts[i].end_time[d] =  np.nan
                    self.Aircrafts[i].start_loc[d] = np.nan
                    self.Aircrafts[i].end_loc[d] = np.nan
                    self.Aircrafts[i].stay_duration[d] = np.nan
                    self.Aircrafts[i].possible_maint_loc[d] = np.nan
                    
        def CheckingRemainingDays(self, D, aircraft_profile_df, aircraft_status_df, initial_flight_schedule_df):
            
