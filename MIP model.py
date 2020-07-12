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

status_per_day_df = pd.DataFrame(columns = ['Date', 'Registration', 'FH', 'FC', 'FD'])

FH = {}
FC = {}

#Initial FH/FC
for i in I:
    FH[i] = initial_data.aircraft_status_df.loc[i]['Initial FH']
    FC[i] = initial_data.aircraft_status_df.loc[i]['Initial FC']
    

#Scheduling
for d in D:
    one_day_schedule = initial_data.initial_flight_schedule_df[initial_data.initial_flight_schedule_df['End Date'] == d]
    for i in I:
        schedule_aircraft_per_day = one_day_schedule[one_day_schedule['Registration'] == i]
        sum_schedule = schedule_aircraft_per_day.sum()
        FH[i] += sum_schedule['Util FH']
        FC[i] += sum_schedule['Util FC']
        date_difference = pd.Timestamp(d) - initial_data.aircraft_profile_df.loc[i]['Original C of A']
        status_per_day_df = status_per_day_df.append({'Date' : d, 'Registration' : i, 'FH' : FH[i], 'FC' : FC[i], 'FD' : date_difference.days  }, ignore_index=True) #PR untuk d: buat index di aircraft profile utk registrasi, dan update data FD untuk d - aircraft C of A
        
        #start location
        #end location
        #duration
        #maint_location
        
   
#print(status_per_day_df[status_per_day_df['Registration'] == 'PK-GLA'])

#ASK: 
    #DEFICIENCIES: 
        #data loading for limitation, 
        #maintenance interval
        #maintenance status 31 Dec
        #last maintenance status
        #towing time
        #effective slot
    
def FormulaRuth(aircraft_profile, all_schedule, effective_slot, hangar_profile, initial_aircraft_status, interval_limitation, last_maintenance_status, maintenance_data, maintenance_interval, maintenance_status_31_Dec, towing_time):
     
    #Define index
    i = aircraft_profile['Registration'] #i = index of aircraft registration
    d = initial_data.initial_flight_schedule_df['End Date'].unique()
    #t = index of aircraft_profile
    #city = index of city
    #h = index of hangar
    #k = index of maintenance type check
    #interval = index of interval type
    #d = index of calendar day
    #tk = index of aircraft type and maintenance type
    
    #Define sets
    I = len(aircraft_profile['Registration']) #set of aircraft registration
    N = len(aircraft_profile['Registration']) #set of aircraft registration
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
    INTERVAL =  ['FH', 'FC', 'DY'] #set of interval types
    D = len(initial_data.initial_flight_schedule_df['End Date'].unique()) #set of calendar day indicator
    F = all_schedule['Start Loc'] #set of node a
    G = all_schedule['End Loc'] #set of node b
    nc = sum(len(F) + len(G)) #set of nodes a and b
    TK = limitation['Checkpoint'] #sets of aircraft type_maint type
    
    #Initial FH/FC/DY (age) and location
    age = {}
    initial_FH = {}
    initial_FC = {}
    initial_location = {}
    for registrasi_pesawat in I:
        fh = initial_aircraft_status.loc[registrasi_pesawat]['Initial FH']
    
    for i in range(I):
        initial_FH = initial_aircraft_status['Initial FH']
        initial_FC = initial_aircraft_status['Initial FC']
        age = datetime.datetime(2019, 1, 1) - aircraft_profile['Original C of A']
        initial_location = initial_aircraft_status['Location']
    
    
    #Scheduling, duration and duration of stay
    #start loc and end loc
    st = {}
    et = {}
    a = {}
    b = {}
    
    D = 5
    
    util_FH = {}
    for i in I:
        for day in d:
            on_day_schedule = all_schedule[all_schedule['Start Date'] == day]
            
            all_schedule['st'] = pd.to_datetime(all_schedule['Start Date'].apply(str)+' '+all_schedule['Chox off time'])
            all_schedule['et'] = pd.to_datetime(all_schedule['End Date'].apply(str)+' '+all_schedule['Chox on time'])
            a, b = all_schedule['Start Loc', 'End Loc']
            idle_duration =  st - et
            possible_maint_location = all_schedule['et']
            
            #util_FH[] = {}
            #util_FH = INITIAL FH
            util_FH = (int(idle_duration.days)*24*60) + int()
    
    util_FH = pd
    util_FH = util_FH + initial_FH
            
            
            


    #Define parameters
    #1, 2, 3. maximum FH/FC/DY tolerance of type k check interval of aircraft type  t(i)
    limit_FH = {}
    limit_FC = {}
    limit_DY = {}
    for tk in range (TK):
        for index, row in limitation.iterrows():
            limit_FH[row['Checkpoint']] = row['Limitation FH']
            limit_FC[row['Checkpoint']] = row['Limitation FC']
            limit_DY[row['Checkpoint']] = row['Limitation DY']
    
    #4, 5. average daily FH usage for aircraft i at day d
    avg_utilization_FH = {}
    avg_utilization_FC = {}
    for i in range (N):
        for index, row in aircraft_profile.iterrows():
            avg_utilization_FH['Registration'] = row['Avg FH']
            avg_utilization_FC['Registration'] = row['Avg FC']
    
    #6, 7, 8. interval of type k check of aircraft type  t(i) in terms of FH/FC/DY
    for unique_aircraft_types in range(T):
        for k in range(K):
            for interval in range(INTERVAL) :
                tkint = maintenance_interval['Interval Checkpoint', 'Value']
    
    
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
    
       

    #XX. Initial FH and FC for aircraft i
    
     
        
    
  
    #  for i in I:
   #     for t in T:
      #  max_dy_tolerance
    
    
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
    


