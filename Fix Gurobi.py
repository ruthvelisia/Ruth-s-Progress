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
import itertools

initial_data = InitialData()
initial_data.LoadAllFile()

#I = initial_data.aircraft_profile_df.index.values

All_D = pd.date_range('2019-01-01', '2019-01-01', freq='D') #calendar day indicator
T = initial_data.aircraft_profile_df['Type'].unique()
H = initial_data.hangar_profile_df.index.values
INTV =  ['FH', 'FC', 'DY'] #set of interval types
NO = list(range(1, 400))
#D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
F = ['CGK', 'KNO', 'BDO', 'AMQ'] #set of node a
G = ['DPS', 'SUB', 'PDG', 'SOQ'] #set of node b
C = F + G
nc = len(F) + len(G) #set of nodes a and b
arcs = list(itertools.product(C, C))

aircraft_database = AircraftDatabase(I, initial_data.aircraft_profile_df)
aircraft_database.UpdatePerDayData(All_D, initial_data.aircraft_profile_df, initial_data.aircraft_status_df, initial_data.initial_flight_schedule_df)
aircraft_database.UpdateLimitMaintenanceData(K, initial_data.aircraft_profile_df, initial_data.interval_limitation_df)
aircraft_database.UpdateAverageUtilizationData(initial_data.aircraft_profile_df)
aircraft_database.UpdateIntervalCheckData(K, initial_data.aircraft_profile_df, initial_data.maintenance_interval_df)    
aircraft_database.UpdateLastMaintenance(K, initial_data.last_maintenance_status_df)

#for d in D:
#    print(aircraft_database.Aircrafts['PK-GMN'].urgency_rate['A'][d])

hangar_database = HangarDatabase(H, initial_data.hangar_profile_df['City'].unique(), initial_data.hangar_profile_df)
hangar_database.UpdateUsedSlot(initial_data.initial_maintenance_status_df)

maintenance_database = MaintenanceDatabase(T, K)
maintenance_database.UpdateMaintenanceDuration(initial_data.maintenance_data_df)


for D in All_D:
    #I. Create empty Model
    m = gp.Model("MIP Model")
    
    
    #I. Additional parameters
    #1. Routing
    for i,arc,d in list(itertools.product(I, arcs, D)):
        from_city = arc[0]
        to_city = arc[1]
        daily_data = aircraft_database.GetAircraftDailyData(i,d)
        isStartLocIn_f = daily_data.start_loc == from_city
        isEndLocIn_g = daily_data.end_loc == to_city
        routing[i, from_city, to_city, d] = int(isStartLocIn_f & isEndLocIn_g)
    
    #2. Urgency rate
    for i,k,d in list(itertools.product(I,K,D)):
        urgency_data = aircraft_database.CalculateUrgencyRate(i,k,d)
        urgency_value = urgency_data[0]
        urgency_check_number = urgency_data[1]
        urgency_limit = urgency_data[2]
        
        if(pd.isnull(urgency_value)):
            urgency_rate[i,k,d] = 0
            urgency_rate_max[i,k,d] = 0
        else:
            urgency_rate[i,k,d] = urgency_value
            urgency_rate_max[i,k,d] = 1 + urgency_limit

    #3. FH, FC, FD
    #minta data FH, FC, FD
    
    #4. Premature rate (Rw)
    R = 0.9
    
    #5. Tolerance penalty (Pa)
    for i,k,d in list(itertools.product(I,K,D)):
        #untuk tolerance penatly, maka tolerance_penalty = (ada di file tolerance penalty)
    
    #6. Grounded penalty (Pg)
    for i,k,d in list(itertools.product(I,K,D)):
        #untuk grounded penalty, untuk setiap day, maka penalti grounded = (ada di file grounded penalty)
        
    
    #II. Define decision variables
    
    #1. v violation decision variable
    violation_var = m.addVars(I, K, D, vtype=GRB.BINARY, name='v')
    
    #2. n grounded check status decision variable
    grounded_check_status_var = m.addVars(I, D, vtype=GRB.BINARY, name='n')
    
    #3. x premature and maintenance requirement decision variable
    maintenance_requirement_var = m.addVars(I, K, G, D, vtype=GRB.BINARY, name='x')

    #4. o hangar check status decision variable
    hangar_check_status_var = m.addVars(I, K, H, C, vtype=GRB.BINARY, name='o')

    
    #III. Set objective function
    for i,k,d in list(itertools.product[I,K,D]):
        remaining_rate_no_violation[i,k,d] = 1 - urgency_rate[i,k,d]
        remaining_rate_with_violation[i,k,d] = urgency_rate[i,k,d] - 1
    for i,k in list(itertools.product[I,K]):
        limit_decimal[i,k] = limit / interval 
        limit_urgency[i,k] = 1 + limit_decimal[i,k]  
    
    premature_MR_unused_FH = ((maintenance_requirement_var[i,k,b,d] for i,k,b,d in list(itertools.product[I, K, B, D]) -  violation_var[i,k,d] for i,k,b,d in list(itertools.product[I, K, B, D]) * ((remaining_rate_no_violation[i,k,d] for i,k,d in list(itertools.product[I,K,D])) * #intvervalFH) )
    violation_unused_FH = (remaining_rate_with_violation[i,k,d] * violation_var[i,k,d] for i,k,d in list(itertools.product[I, K, D])* #interval_FH)
    penalty_tolerance = (#tolerance penalty * violation_var[i,k,d] for i,k,d in list(itertools.product[I, K, D])
    penalty_grounded = (#grounded penalty * violation_var[i,k,d] for i,k,d in list(itertools.product[I, K, D]) * (urgency_rate[i,k,d] for i,k,d in list(itertools.product[I,K,D]) - limit_urgency[i,k] for i,k in list(itertools.product[I,K]) /average fh) )                     
                         
    m.setObjective(sum(premature_MR_unused_FH + violation_unused_FH + penalty_tolerance + penalty_grounded), GRB.MINIMIZE)
    
    
    #TO DO LIST: m.setObjective(minimize unused FH)
    #Example: m.setObjective(sum(buy[f]*cost[f] for f in foods), GRB.MINIMIZE)
    
    aircraft_day = list(itertools.product(I,D))
    aircraft_check_day = list(itertools.product(I, K, D))
    aircraft_maintenance_no_intv_day = list(itertools.product(I,K,D))

    #IV. Define constraints
    #1. Constraint 1:  To ensure that the aircraft will perform the maintenance 
    for i,k,d in aircraft_check_day:
        m.addConstrs(maintenance_requirement_var[i,k,b,d] for b in C = routing[i, from_city, to_city, d])

    # #3. Constraint 3: That the variable v_i^k is zero when the aircraft i is in operation
    # #4. Constraint 4: the variable χ_(i,b,d)^k are zero when the aircraft  i is flying
    # for i,d in aircraft_day:
    #     #1
    #     m.addConstr(quicksum(routing_var[i,a,b,d] for a,b in arcs) == 1, "routing_constraint")
    #     if (routing_var[i,a,b,d] for a,b in arcs) == 1:
    #         for k in K:
    #             #3
    #             m.addConstr(violation_var[i,k,d] == 0) 
    #             #4
    #             m.addConstr(maintenance_requirement_var[i,k,b,d] for b in C == 0)                 
    
    # #5. Constraints 5 - 7: the recurrence relation between consecutive maintenance requirement variables
    # for i,k,d in aircraft_maintenance_intv_day:
    #     previous_urgency = aircraft_database.CalculateUrgencyRate(i,k,d, aircraft_database.Aircrafts[i].last_maintenance_number[k]-1)
    #     m.addConstrs(urgency_rate_var[i,k,d] >= (1-previous_urgency) + usage * maintenance_requirement_var[i,k,b,d] for k, b in list(itertools.product(K, C)) + 1 - maintenance_requirement_var[i,k,b,d] for b in C - violation_var[i,k,d])
     
    
    # #6. Constraint 8: the minimum recurrence relation between consecutive maintenance requirement variables
    # for i,k,no,intv,d in aircraft_maintenance_no_intv_day:
    #     urgency_rate_list[i,k,d] = min(urgency_rate_constraint_FH[i,k,intv,d], urgency_rate_constraint_FD[i,k,intv,d], urgency_rate_constraint_FD[i,k,intv,d])
    #     urgency_rate_var[i,k,d] = urgency_rate_list[i,k,d]
        
    #4. Constraint 4: the maintenance is performed between the minimum of premature interval and the tolerance limit
    for i,k,d in list(itertools.product[I,K,D]):
        m.addConstrs(0 <= maintenance_requirement_var[i,k,b,d] for b in C + violation_var[i,k,d] - urgency_rate_max[i,k,d] <= 1 - limit_decimal[i,k],"urgency_limit_constraint_FD")    
        
    #8. Constraint 10: only one type k check can be scheduled for the same interval
    for i,d in aircraft_day:
        m.addConstr(quicksum(maintenance_requirement_var[i,k,b,d] for k, b in list(itertools.product(K, C))) == 1)
    
    #9. Constraint 11: the aircraft is available for the minimum time required for each type k check and towing duration
    for i in I:
        m.addConstrs(aircraft_database.Aircrafts[i].stay_duration[d] for d in D * maintenance_requirement_var[i,k,b,d] for k,b,d in list(itertools.product(K, C, D)) >= maintenance_database.maintenance[t][k].durations[aircraft_database.Aircrafts[i].last_maintenance_number[k]] for t,k in list(itertools.product(T, K)) * maintenance_requirement_var[i,k,b,d] for k,b,d in list(itertools.product(K, C, D)) + hangar_database.Workshops[h].towing_time for h,b in list(itertools.product(H, C)))
    
    #10.Constraint 12: there are sufficient slots for a type k check during the entire maintenance time 〖∆t〗_(t(i),k)  for all available aircraft and hangars
    #PR: Codingan day d + durasi seperti apa?
    for i,k in list(itertools.product(I, K)):
        #aircraft_database.Aircrafts[i].end_time[d] + maintenance_database.maintenance[k].duration[aircraft_database.Aircrafts[i].last_maintenance_number[k]] <= aircraft_database.Aircrafts[i].start_time[d+1]
        for duration in maintenance_database.maintenance[k].durations:
            is_hangar_can_check = quicksum(hangar_check_status_var[i,k,h,b,d] for b,h in list(itertools.product(C, H)))
            m.addConstrs(quicksum(maintenance_requirement_var[i,k,b,] for b, d in list(itertools.product(C, D)) <= is_hangar_can_check))
    
    #11. Constraint 13: The operational constraints are required to guarantee that the number of type k checks performed in parallel per day do not exceed the hangar-capacity
    #Codingan check_probs disesuaikan lagi sehingga sesuai per hari
    #PR: Cek durasi, pakai effective slot kah? atau total slot?
    for b,d in list(itertools.product(C, D)):
        month = calendar.month_name[d.month] # January/February/March etc
        m.addConstrs(quicksum(maintenance_requirement_var[i,k,b,d] for i,k in list(itertools.product(I, K))) <= workshop.effective_slot[month] for workshop in hangar_database.City[b])
    
    m.optimize()
    m.printSolution()
    

    if model.status == GRB.Status.OPTIMAL:
        print('Optimal objective: %g' % model.objVal)
    elif model.status == GRB.Status.INF_OR_UNBD:
        print('Model is infeasible or unbounded')
        exit(0)
    elif model.status == GRB.Status.INFEASIBLE:
        print('Model is infeasible')
        exit(0)
    elif model.status == GRB.Status.UNBOUNDED:
        print('Model is unbounded')
        exit(0)
    else:
        print('Optimization ended with status %d' % model.status)
        exit(0)

#def printSolution():
#    if m.status == GRB.Status.OPTIMAL:
#        print('\nCost: %g' % m.objVal)
#        print('\nmaintenance_requirement_var:')

#    else:
#        print('No solution')



#SORTING
#1. SORTING PRIORITAS MASUK HANGAR
#Buat range prioritas dari urgency rate
#awalnya dapat semua prioritas dari pesawat di tanggal tersebut:
#DIAMBIL DARI VARIABEL MAINTENANCE REQUIREMENT (maintenance_requirement_var) dan HANGAR CHECK STATUS VAR (hangar_check_status_var)
    #(setelah sudah ditentukan dari lokasi hangar cocok, kapasitas hangar mencukupi dan durasi hangar mencukupi)
    #prioritas 1: 
        #tentukan dari k yang paling rendah intervalnya --> dari A check, 2Y, 4000 FC, C Check, 36+42M dan D Check
        #Jika ada pesawat yang ada lebih dari 1 k check yang dikerjakan (contoh A dan C), maka ambil C check dan ambil durasi yang paling tinggi (karena akan dikerjakan juga yang A check)
        #Jika ada pesawat yang hari ini ngerjain C check, terus selama dia ngerjain c check besok2nya ada D check, maka ganti dengan durasi D check (yang lebih tinggi) karena semestinya D check akan mengerjakan jg C Check
        #Untuk pengerjaan double job, maka tanggal pengerjaan maintenance diambil paling cepat, dan durasi diambil yang paling tinggi
    #prioritas 2: 
        #Jika ada k yang sama, tentukan urgency rate yang paling tinggi
    #prioritas 3:
        #jika dicek kapasitas yang ada tidak mencukupi/hangar tidak sesuai/durasi tidak sesuai, ganti dengan pesawat yang kurang prioritas namun sesuai dgn hangar dan durasi sesuai
    #prioritas 4:
        #jika pesawat tidak ada lagi yang masuk, hangar dibiarkan kosong


#Jika sudah terisi semua, masukin ke dalam list dan update list hangar 
#Jadi di hangar akan ada HANGAR STATUS: HANGAR CODE (h), Nomor slot terisi/ effective slot, CITY (b), PESAWAT MAINTENANCE (i), MAINTENANCE (k), TERISI DARI TANGGAL (d), DURASI (maintenance_duration), SAMPAI TANGGAL (d+duration)
# Untuk pengisian setelah durasi, maka tinggal tambahkan aja (d+duration)+1 untuk next pesawat yang masuk (asumsi pekerjaan dimulai dari pagi kembali)


#2. SORTING STATUS (FLYING/PARKING/MAINTENANCE)
#DIAMBIL DARI HASIL:
    #VARIABEL MAINTENANCE REQUIREMENT (maintenance_requirement_var)
    #VARIABEL ROUTING (routing_var)
    #VARIABEL HANGAR CHECK STATUS (hangar_check_status_var)

#Jika routing_var == 1; maintenance_requirement_var == 0, : STATUS "FLYING"
#Jika routing_VAR == 1; maintenance_requirement_var == 1, : 
    #cek lagi apakah bisa masuk hangar? cek hangar_check_status dan hangar_capacity
    #Jika iya, maintenance_requiremenet_var == 1, routing_var == 0: STATUS "MAINTENANCE"
    #Jika tidak, maintenance_requirement_var ==0, routing_var == 1: STATUS "FLYING"
#Jika routing_var ==0; maintenance_requirement_var == 1: 
    #cek lagi apakah bisa masuk hangar? cek hangar_check_status dan hangar_capacity
    #Jika iya, maintenance_requiremenet_var == 1, routing_var == 0: STATUS "MAINTENANCE"
    #Jika tidak, maintenance_requirement_var ==0, routing_var == 0: STATUS "PARKING"

#Saran reassignment parking to flying, flying to maintenance
    #1. jadwal yang flying difreeze selama dia maintenance, jadi d nya ga sesuai lagi (???)
    #2. pesawat yang parking masuk ke jadwal pesawat yang akan dimaintenance, tp namanya di schedule ga sesuai lagi (???)
        



