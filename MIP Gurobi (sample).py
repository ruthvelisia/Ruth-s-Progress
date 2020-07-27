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
I = ['PK-GRF']
K = ['A']

All_D = pd.date_range('2019-01-01', '2019-12-31', freq='D') #calendar day indicator
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

#Load the data --> in MIP Model & MIP Model Sampel

#Define sets and indexes --> in MIP Model & MIP Model Sampel

#Preprocessing --> in MIP Model & MIP Model Sampel

#WORKFLOW

for D in All_D:
    #I. Create empty Model
    m = gp.Model("MIP Model")
    
    #II. Define decision variables
    
    #1. y routing decision variable
    routing_var = m.addVars(I, C, C, D, vtype=GRB.BINARY, name='y')
    for i,arc,d in list(itertools.product(I, arcs, D)):
        from_city = arc[0]
        to_city = arc[1]
        daily_data = aircraft_database.GetAircraftDailyData(i,d)
        isStartLocIn_f = daily_data.start_loc == from_city
        isEndLocIn_g = daily_data.end_loc == to_city
        routing_var[i, from_city, to_city, d] = int(isStartLocIn_f & isEndLocIn_g)
    
    #2. w urgency rate decision variable
    urgency_rate_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='w')
    urgency_rate_max_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='ga tau')
    
    #3. v violation decision variable
    violation_var = m.addVars(I, K, D, vtype=GRB.BINARY, name='v')
    
    #4. n grounded check status decision variable
    grounded_check_status_var = m.addVars(I, D, vtype=GRB.BINARY, name='n')
    
    #7. dy total days decision variable
    total_days_var = m.addVars(I, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='dy')
    #for i,d in list(itertools.product(I,D)):
        #total_days_var = aircraft_database.Aircrafts[i].FD[d]
    
    #8. fh total fh decision variable
    total_fh_var = m.addVars(I, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='fh')
    #for i,d in list(itertools.product(I,D)):
        #total_fh_var = aircraft_database.Aircrafts[i].FH[d] 
    
    #9. fc total fc decision variable
    total_fc_var = m.addVars(I, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='fc')
    #for i,d in list(itertools.product(I,D)):
        #total_fc_var = aircraft_database.Aircrafts[i].FC[d] 
    
    #10. e-dy extra days decision variable
    extra_fd_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-dy' )
    #11. e-fh extra fh decision variable
    extra_fh_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-fh' )
    #12. e-fc extra fc decision variable
    extra_fc_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-fc' )
    
    for i,k,d in list(itertools.product(I,K,D)):
        urgency_data = aircraft_database.CalculateUrgencyRate(i,k,d)
        urgency_value = urgency_data[0]
        urgency_check_number = urgency_data[1]
        urgency_limit = urgency_data[2]
        
        if(pd.isnull(urgency_value)):
            urgency_rate_var[i,k,d] = 0
            urgency_rate_max_var[i,k,d] = 0
        else:
            urgency_rate_var[i,k,d] = urgency_value
            urgency_rate_max_var[i,k,d] = 1 + urgency_limit
            
        if urgency_rate_var[i,k,d] > 1 :
            violation_var[i,d] == 1
        else:
            violation_var[i,d] == 0
        
        if urgency_rate_var[i,k,d] > urgency_rate_max_var[i,k,d]:
            grounded_check_status_var[i,d] == 1
        else:
            grounded_check_status_var[i,d] == 0
            
        if (urgency_rate_var[i,k,d] > 1) :
            daily_data = aircraft_database.GetAircraftDailyData(i, d)
            maintenance_data = aircraft_database.GetAircraftMaintenanceData(i, k)
            
            extra_fd_var[i,k,d] = daily_data.FD - (math.floor(daily_data.FD/maintenance_data.interval_check_FD)* maintenance_data.interval_check_FD)
            extra_fh_var[i,k,d] = daily_data.FH - (math.floor(daily_data.FH/maintenance_data.interval_check_FH)* maintenance_data.interval_check_FH)
            extra_fc_var[i,k,d] = daily_data.FC - (math.floor(daily_data.FC/maintenance_data.interval_check_FC)* maintenance_data.interval_check_FC)
    
    for i,d in list(itertools.product(I, D)):
        daily_data = aircraft_database.GetAircraftDailyData(i, d)
        total_days_var[i,d] = daily_data.FD
        total_fh_var[i,d] = daily_data.FH
        total_fc_var[i,d] = daily_data.FC
        
    # for i,k,intv,d,no in list(itertools.product(I,K,INTV,D)):
    #     if np.logical_and(urgency_rate_var[i,k,intv,d,no] >= 0.9, urgency_rate_var[i,k,intv,d,no] < 1):
    #         aircraft_maint_status = "Premature"
    #     if urgency_rate_var[i,k,intv,d,no] == 1:
    #         aircraft_maint_status = "On Time"
    #     if np.logical_and(urgency_rate_var[i,k,intv,d,no] > 1.0, urgency_rate_var[i,k,intv,d,no] <= 1+ max[limit_intv_FH, limit_intv_FC, limit_intv_FH]):
    #         aircraft_maint_status = "Within tolerance"
    #     if urgency_rate_var[i,k,intv,d,no] > 1+ max[limit_intv_FH, limit_intv_FC, limit_intv_FH]:
    #         aircraft_maint_status = "Exceed tolerance"
        
    
    #5. x premature and maintenance requirement decision variable
    maintenance_requirement_var = m.addVars(I, K, G, D, vtype=GRB.BINARY, name='x')
    #Logic if the routing var = 1 while the urgency rate >0.9
    for i,arc,d in list(itertools.product(I, arcs, D)):
        is_any_urgent = False
        for k in K:
            is_any_urgent = urgency_rate_var[i,k,d] > 0.9
            if(is_any_urgent): 
                break
            
        if np.logical_and(routing_var[i, arc[0], arc[1],d] == 1, is_any_urgent):
            #and isEndLocIn_g == b)
            maintenance_requirement_var[i, k, arc[1], d] = 1
        else:
            maintenance_requirement_var[i, k, arc[1], d] = 0
            #bruteforce maintenance_requirement_var[i,k,b,d] == 1
            #assign pesawat lain untuk menggantikan pesawat i (cek ketersediaan pesawat available yang sedang parking)
            #cari pesawat yang statusnya parking        
    
    
    
    #6. o hangar check status decision variable
    hangar_check_status_var = m.addVars(I, K, H, C, vtype=GRB.BINARY, name='o')
    for i,k,h,c in list(itertools.product(I, K, H, C)):
        if(aircraft_database.Aircrafts[i].last_maintenance_number[k] == -1):
            hangar_check_status_var[i,k,h,c] = 0
        elif(hangar_database.Workshops[h].city != c):
            hangar_check_status_var[i,k,h,c] = 0
        elif(hangar_database.Workshops[h].check_probs[aircraft_database.Aircrafts[i].t + '_' + k] <= 0):
            hangar_check_status_var[i,k,h,c] = 0
        else:
            hangar_check_status_var[i,k,h,c] = 1
    
    #13. teta tolerance rate decision variable
    #tolerance_rate_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='teta')
    
    #gam maintenance check status decision variable
    #maintenance_check_status_var = m.addVars(I, K, G, D, vtype=GRB.BINARY, name='gam')
    
    #III. Set objective function
    m.setObjective(sum(violation_var[i,k,d] for i,k,d in itertools.product(I, K, D)), GRB.MINIMIZE)
    
    #TO DO LIST: m.setObjective(minimize unused FH)
    #Example: m.setObjective(sum(buy[f]*cost[f] for f in foods), GRB.MINIMIZE)
    
    aircraft_day = list(itertools.product(I,D))
    aircraft_check_day = list(itertools.product(I, K, D))
    aircraft_maintenance_no_intv_day = list(itertools.product(I,K,D))
    #IV. Define constraints
    
    #2. Constraint 2:  To ensure that the aircraft will perform the maintenance 
    for i,k,d in aircraft_check_day:
        m.addConstrs(quicksum(routing_var[i,a,b,d] for a,b in arcs) >= maintenance_requirement_var[i,k,b,d] for b in C)
    
    #1. Constraint 1: One arc will depart from every airport(city) a
    #3. Constraint 3: That the variable v_i^k is zero when the aircraft i is in operation
    #4. Constraint 4: the variable χ_(i,b,d)^k are zero when the aircraft  i is flying
    for i,d in aircraft_day:
        #1
        m.addConstr(quicksum(routing_var[i,a,b,d] for a,b in arcs) == 1, "routing_constraint")
        if (routing_var[i,a,b,d] for a,b in arcs) == 1:
            for k in K:
                #3
                m.addConstr(violation_var[i,k,d] == 0) 
                #4
                m.addConstr(maintenance_requirement_var[i,k,b,d] for b in C == 0)                 
    
    #5. Constraints 5 - 7: the recurrence relation between consecutive maintenance requirement variables
    for i,k,d in aircraft_maintenance_intv_day:
        previous_urgency = aircraft_database.CalculateUrgencyRate(i,k,d, aircraft_database.Aircrafts[i].last_maintenance_number[k]-1)
        m.addConstrs(urgency_rate_var[i,k,d] >= (1-previous_urgency) + usage * maintenance_requirement_var[i,k,b,d] for k, b in list(itertools.product(K, C)) + 1 - maintenance_requirement_var[i,k,b,d] for b in C - violation_var[i,k,d])
        
        # if intv == "FH":
        #     fh_divisor[i,k] = math.floor((aircraft_database.Aircrafts[i].FH[d] - aircraft_database.Aircrafts[i].interval_check_FH[k])/(aircraft_database.Aircrafts[i].interval_check_FH[k]))
        #     fh_usage = (((aircraft_database.Aircrafts[i].FH[d])-(fh_divisor[i,k] *(aircraft_database.Aircrafts[i].interval_check_FH[k])))/((fh_divisor[i,k] *(aircraft_database.Aircrafts[i].interval_check_FH[k]))))
            
        # if intv == "FC":
        #     fc_divisor = math.floor((aircraft_database.Aircrafts[i].FC[d] - aircraft_database.Aircrafts[i].interval_check_FC[k])/(aircraft_database.Aircrafts[i].interval_check_FC[k]))
        #     fc_usage = (((aircraft_database.Aircrafts[i].FC[d])-(fc_divisor*(aircraft_database.Aircrafts[i].interval_check_FC[k])))/((fh_divisor*(aircraft_database.Aircrafts[i].interval_check_FC[k]))))
        #     m.addConstrs(urgency_rate_var[i,k,no,intv,d] >= (1-(urgency_rate_var[i,k,no-1,intv,d])) + fc_usage * maintenance_requirement_var[i,k,b,d] for k, b in list(itertools.product(K, G)) + 1 - maintenance_requirement_var[i,k,b,d] for b in G - violation_var[i,k,d])
        # else:
        #     pass
        #     #fd_divisior = math.floor((aircraft_database.Aircrafts[i].FD[d] - aircraft_database.Aircrafts[i].interval_check_FD[k])/(aircraft_database.Aircrafts[i].interval_check_FD[k]))        fd_usage = (((aircraft_database.Aircrafts[i].FD[d])-(fd_divisor*(aircraft_database.Aircrafts[i].interval_check_FD[k])))/((fd_divisor*(aircraft_database.Aircrafts[i].interval_check_FD[k]))))
        #     #m.addConstrs(urgency_rate_var[i,k,no,intv,d] >= (1-(urgency_rate_var[i,k,no-1,intv,d])) + fd_usage *  maintenance_requirement_var[i,k,b,d] for k, b in list(itertools.product(K, G)) + 1 - maintenance_requirement_var[i,k,b,d] for b in G - violation_var[i,k,d])
    
    #6. Constraint 8: the minimum recurrence relation between consecutive maintenance requirement variables
    #for i,k,no,intv,d in aircraft_maintenance_no_intv_day:
    #    urgency_rate_list[i,k,d] = min(urgency_rate_constraint_FH[i,k,intv,d], urgency_rate_constraint_FD[i,k,intv,d], urgency_rate_constraint_FD[i,k,intv,d])
    #    urgency_rate_var[i,k,d] = urgency_rate_list[i,k,d]
        
    #7. Constraint 9: the maintenance is performed between the minimum of premature interval and the tolerance limit
    for i,k,d in aircraft_maintenance_intv_day:
        m.addConstrs(0.9 <= urgency_rate_var[i,k,d] <= urgency_rate_max_var[i,k,d],"urgency_limit_constraint_FD")    
        
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
    

#model.optimize()
#printSolution()

#if model.status == GRB.Status.OPTIMAL:
#    print('Optimal objective: %g' % model.objVal)
#elif model.status == GRB.Status.INF_OR_UNBD:
#    print('Model is infeasible or unbounded')
#    exit(0)
#elif model.status == GRB.Status.INFEASIBLE:
#    print('Model is infeasible')
#    exit(0)
#elif model.status == GRB.Status.UNBOUNDED:
#    print('Model is unbounded')
#    exit(0)
#else:
#    print('Optimization ended with status %d' % model.status)
#    exit(0)

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
        



