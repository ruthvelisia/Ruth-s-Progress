import pandas as pd
import itertools as it
from InitialData import *
from Hangar import * 
import gurobipy as gp
from gurobipy import Model
import datetime
from datetime import date
from datetime import timedelta
import calendar
import numpy as np

initial_data = InitialData()
initial_data.LoadAllFile()

I = ['PK-GLA', 'PK-GLE']
D = initial_data.initial_flight_schedule_df['End Date'].unique() #calendar day indicator

status_per_day_df = pd.DataFrame(columns = ['Date', 'Registration', 'FH', 'FC', 'FD', 'Start Location', 'End Location', 'Stay Duration', 'Possible Maintenance Location'])

FH = {}
FC = {}
FD = {}

#Initial FH/FC
for i in I:
    FH[i] = initial_data.aircraft_status_df.loc[i]['Initial FH']
    FC[i] = initial_data.aircraft_status_df.loc[i]['Initial FC']
    FD[i] = initial_data.aircraft_profile_df.loc[i]['Original C of A']

#Scheduling
for d in D:
    one_day_schedule = initial_data.initial_flight_schedule_df[initial_data.initial_flight_schedule_df['End Date'] == d]
    for i in I:
        schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
        sum_schedule = schedule_aircraft_per_day.sum()
        FH[i] += sum_schedule['Util FH']
        FC[i] += sum_schedule['Util FC']
        FD[i] = pd.Timestamp(d) - initial_data.aircraft_profile_df.loc[i]['Original C of A']
        start_loc[i] += sum_schedule['Start Loc']
        end_loc[i] += sum_schedule['End Loc']
        stay_duration[i] = sum_schedule['Duration']
        possible_maint_loc[i] = sum_schedule['Maint Station']
        status_per_day_df = status_per_day_df.append({'Date' : d, 'Registration' : i, 'FH' : FH[i], 'FC' : FC[i], 'FD' : FD[i].days, 'Start Location' : start_loc[i], 'End Location' : end_loc[i], 'Stay Duration' : stay_duration[i], 'Possible Maintenance Location' : possible_maint_loc[i]}, ignore_index=True)
        
   
#print(status_per_day_df[status_per_day_df['Registration'] == 'PK-GLA'])

    
def FormulaRuth(aircraft_profile, all_schedule, effective_slot, hangar_profile, initial_aircraft_status, interval_limitation, last_maintenance_status, maintenance_data, maintenance_interval, maintenance_status_31_Dec, towing_time):
     
    #Define index
    #i = index of aircraft registration
    #d = index of calendar day
    #t = index of aircraft_profile
    #city = index of city
    #h = index of hangar
    #k = index of maintenance type check
    #intv = index of interval type
    #d = index of calendar day
    #tk = index of aircraft type and maintenance type
    
    #Define sets
    I = aircraft_profile['Registration'] #set of aircraft registration
    N = len(aircraft_profile['Registration']) #number of aircraft fleet
    T = aircraft_profile['Type'].unique() #set of aircraft types
    dict_type_checks = {}
    hasil = Aircraft.Checks('type apa')
    for unique_aircraft_type in t:
        aircraft_type_checks_df = maintenance_data[maintenance_data['Type'] == unique_aircraft_type]
        all_aircraft_maintenance_unique_letters = aircraft_type_checks_df['Letter'].unique()
        aircraft_check_codes = []
        for all_aircraft_maintenance_unique_letter in all_aircraft_maintenance_unique_letters:
            aircraft_check_codes.append(unique_aircraft_type + "_" + all_aircraft_maintenance_unique_letter)
            dict_type_checks[unique_aircraft_type] = aircraft_check_codes
    CITY, H = hangar_profile['City','Hangar Code']  #sets of city and hangar code
    K = maintenance_data['Check1'] #set of maintenance type check
    INTV =  ['FH', 'FC', 'DY'] #set of interval types
    D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
    F = all_schedule['Start Loc'] #set of node a
    G = all_schedule['End Loc'] #set of node b
    nc = sum(len(F) + len(G)) #set of nodes a and b
    TK = limitation['Checkpoint'] #sets of aircraft type_maint type


    #Define parameters
    #1, 2, 3. maximum FH/FC/DY tolerance of type k check interval of aircraft type  t(i)
    for i in I:
        i = initial_data.aircraft_profile_df['Registration']
        for t in T:
            t[i] = initial_data.aircraft_profile_df['Type']
            for k in K:
                k[t][i] = initial_data.interval_limitation_df['Check1'] 
                for intv in INTV:
                    for index, row in limitation.iterrows():
                    if initial_data.interval_limitation_df.row
                    limit_FH[k][t][i] = initial_data.interval_limitation_df.row['Limitation FH']
                    limit_FC[k][t][i] = initial_data.interval_limitation_df.row['Limitation FC']
                    limit_DY[k][t][i] = initial_data.interval_limitation_df.row['Limitation DY']
    
    #4, 5. average daily FH and FC usage for aircraft i at day d
    #avg_utilization_FH = {}
    #avg_utilization_FC = {}
    for i in I:
        for d in D:
            for index, row in aircraft_profile.iterrows():
                avg_utilization_FH[i] = initial_data.aircraft_profile_df.row['Avg FH']
                avg_utilization_FC[i] = initial_data.aircraft_profile_df.row['Avg FC']
    
    #6, 7, 8. interval of type k check of aircraft type  t(i) in terms of FH/FC/DY
    for i in I:
        i = initial_data.aircraft_profile_df['Registration']
        for t in T:
            t[i] = initial_data.aircraft_profile_df['Type']
            for k in K:
                k[t][i] = initial_data.maintenance_interval_df['Check1']
                for intv in INTV:
                    interval_check[intv][k][t][i] = initial_data.maintenance_interval_df['FH Value']
    
    
    #9 hangar capacity
    for h in range(H):
        hangar_cap = hangar_profile['Slot']
    #10 hangar capacity based on months
    hangar_cap_jan = {}
    hangar_cap_feb = {}
    hangar_cap_mar = {}
    hangar_cap_apr = {}
    hangar_cap_may = {}
    hangar_cap_jun = {}
    hangar_cap_jul = {}
    hangar_cap_aug = {}
    hangar_cap_sep = {}
    hangar_cap_oct = {}
    hangar_cap_nov = {}
    hangar_cap_dec = {}
    for h in range(H):
        for index, row in hangar_profile.iterrows():
            hangar_cap_jan['Unique Code'] = row['January']
            hangar_cap_feb['Unique Code'] = row['February']
            hangar_cap_mar['Unique Code'] = row['March']
            hangar_cap_apr['Unique Code'] = row['April']
            hangar_cap_may['Unique Code'] = row['May']
            hangar_cap_jun['Unique Code'] = row['June']
            hangar_cap_jul['Unique Code'] = row['July']
            hangar_cap_aug['Unique Code'] = row['August']
            hangar_cap_sep['Unique Code'] = row['September']
            hangar_cap_oct['Unique Code'] = row['October']
            hangar_cap_nov['Unique Code'] = row['November']
            hangar_cap_dec['Unique Code'] = row['December']
    
    
    #Status per day
    status_per_day_df = pd.DataFrame(columns = ['Date', 'Registration', 'FH', 'FC', 'FD', 'Start Location', 'End Location', 'Stay Duration', 'Possible Maintenance Location'])
    
    FH = {}
    FC = {}
    FD = {}
    
    #Initial FH/FC/FD
    for i in I:
        FH[i] = initial_data.aircraft_status_df.loc[i]['Initial FH']
        FC[i] = initial_data.aircraft_status_df.loc[i]['Initial FC']
        FD[i] = initial_data.aircraft_profile_df.loc[i]['Original C of A']
    
    
    #Scheduling
    for d in D:
        one_day_schedule = initial_data.initial_flight_schedule_df[initial_data.initial_flight_schedule_df['End Date'] == d]
        for i in I:
        schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
        sum_schedule = schedule_aircraft_per_day.sum()
        FH[i] += sum_schedule['Util FH']
        FC[i] += sum_schedule['Util FC']
        FD[i] = pd.Timestamp(d) - initial_data.aircraft_profile_df.loc[i]['Original C of A']
        start_loc[i] += sum_schedule['Start Loc']
        end_loc[i] += sum_schedule['End Loc']
        stay_duration[i] = sum_schedule['Duration']
        possible_maint_loc[i] = sum_schedule['Maint Station']
        status_per_day_df = status_per_day_df.append({'Date' : d, 'Registration' : i, 'FH' : FH[i], 'FC' : FC[i], 'FD' : FD[i].days, 'Start Location' : start_loc[i], 'End Location' : end_loc[i], 'Stay Duration' : stay_duration[i], 'Possible Maintenance Location' : possible_maint_loc[i]}, ignore_index=True)
        
   
#print(status_per_day_df[status_per_day_df['Registration'] == 'PK-GLA'])
    
    #Last Maint Status
    #MOP --> CONTOHNYA A-1
    #BUAT TABEL MOP - LAST MAINTENANCE
    
    
    #Define the model
    m = Model("MIP Model")
    
    #Define variables
    # continuous variable to prevent subtours: each city will have a
# different sequential id in the planned route except the first one
#y = [model.add_var() for i in V]
    
    #1. Binary Variables indicating if aircraft i from city a at day d-1 to b at route r 
    #x = [[model.add_var(var_type=BINARY) for j in V] for i in V]
    
    

    #for i in I, 
    
    #Define objective value
    #for i in V:
        #model += xsum(x[i][j] for j in V - {i}) == 1
    #Define constraints
    
    #Optimize
    


