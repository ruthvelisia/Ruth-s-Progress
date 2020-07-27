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
import itertools

initial_data = InitialData()
initial_data.LoadAllFile()

#I = initial_data.aircraft_profile_df.index.values
I = ['PK-GLA', 'PK-GMN', 'PK-GAK']
K = ['A', 'C', 'D']

D = pd.date_range('2019-01-01', '2019-01-31', freq='D') #calendar day indicator
T = initial_data.aircraft_profile_df['Type'].unique()
CITY = initial_data.hangar_profile_df['City'].unique()
H = initial_data.hangar_profile_df.index.values
INTV =  ['FH', 'FC', 'DY'] #set of interval types
NO = list(range(1, 400))
#D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
F = ['CGK', 'KNO', 'BDO', 'AMQ'] #set of node a
G = ['DPS', 'SUB', 'PDG', 'SOQ'] #set of node b
nc = len(F) + len(G) #set of nodes a and b
aircraft_check_day = list(itertools.product(I, K, D))
arcs = list(itertools.product(F, G))
route_per_day = list(itertools.product(arcs,D))
aircraft_day = list(itertools.product(I,D))
aircraft_route_day = list(itertools.product(I,arcs,D))
aircraft_maintenance_no_intv_day = list(itertools.product(I,K,NO,INTV,D))
aircraft_maint_no_day = list(itertools.product(I,K,NO,D))
#print(list(aircraft_maintenance_no_intv_day))
#print(list(route_per_day))    
#print(list(ac_interval)

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

#Flying Status

#WORKFLOW
#Initial Last Maintenance
for i in I:
    for k in K:
        last_maintenance = aircraft_database.Aircrafts[i].last_maintenance[k]
        last_maintenance_no = aircraft_database.Aircrafts[i].last_maintenance_number[k]
        last_maintenance_A = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'A']
        last_maintenance_A_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'A']
        last_maintenance_C = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'C']
        last_maintenance_C_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'C']
        last_maintenance_D = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'D']
        last_maintenance_D_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == 'D']
        last_maintenance_2Y = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '2Y']
        last_maintenance_2Y_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '2Y']            
        last_maintenance_36+42M = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '36+42M']
        last_maintenance_36+42M_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '36+42M']
        last_maintenance_4000FC = aircraft_database.Aircrafts[i].last_maintenance[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '4000FC']
        last_maintenance_4000FC_no = aircraft_database.Aircrafts[i].last_maintenance_number[k][aircraft_database.Aircrafts[i].last_maintenance[k] == '4000FC']

#Initial Urgency Rate
urgency_rate_var = {}
for i in I:
    for k in K:
        if k == "A":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_A[k]
            divisor = aircraft_database.Aircrafts[i].divisor_A[k]
        if k == "C":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_C[k]
            divisor = aircraft_database.Aircrafts[i].divisor_C[k]
        if k == "D":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_D[k]
            divisor = aircraft_database.Aircrafts[i].divisor_D[k]
        if k == "2Y":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_2Y[k]
            divisor = aircraft_database.Aircrafts[i].divisor_2Y[k]
        if k == "36+42M":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_36+42M[k]
            divisor = aircraft_database.Aircrafts[i].divisor_36+42M[k]
        if k == "4000FC":
            urgency_rate_var = aircraft_database.Aircrafts[i].urgency_rate_4000FC[k]
            divisor = aircraft_database.Aircrafts[i].divisor_4000FC[k]


#1. Point of View: Aircraft
#a. Initial FH, FC, FD
for i in I:
    initial_FH = aircraft_database.Aircrafts[i].Sum_FH_Util
    initial_FC = aircraft_database.Aircrafts[i].Sum_FC_Util
    for d in date(2019,1,1):
        initial_FD = aircraft_database.Aircrafts[i].FD[d]
        
#b. Initial Status (Flying/Parking/Maintenance)
for i in I:
    initial_status = aircraft_database.Aircrafts[i].Status


#a. Update flight schedule as of 31-Dec-2018
        
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



#1. Point of View: Aircraft


#a. Update flight schedule as of 31-Dec-2018



#

#Rules:
#1. Urgency rate

#from last maintenance --> urgency rate var = 0 (asumsi)
#Hitung urgency rate awal
#Jika:
    #urgency rate < 1 --> premature
    #urgency rate =1 --> maintenance requirement
    #urgency rate >=1 sampai limit --> within tolerance
    #urgency rate limit sampai seterusnya --> beyond tolerance

#Pengaturan MOP
#last mop
#masuk mop gimana caranya
#next mop

#Jika urgency rate within tolerance
#Hitung extra days FH, FC, FD

#Jika urgency rate di atas tolerance
#grounded no schedule

#1. Term of violation
#if urgency rate > 1 --> violation
#if urgency rate di antara 1 dan limit, maka hitung extra days_FH, FC dan FD

#2. Term of hangar
#jika durasi stay tidak pernah cukup
#dan jika urgency rate >1
#brute force to do maintenance
#assign ke parkir

#ASSIGNMENT KE HANGAR
#PROBABILITAS HANGAR
#MASUK HANGAR PRIORITAS

#3. Term aircraft status
#Jika aircraft parkir
#Jika aircraft maintenance
#Jika aircraft flying