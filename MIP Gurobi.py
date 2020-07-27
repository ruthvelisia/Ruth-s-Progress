import pandas as pd
import itertools as it
from InitialData import *
from Workshop import * 
import sys
import gurobipy as gp
from gurobipy import *
import math
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
from ScehduleDatabase import *

initial_data = InitialData()
initial_data.LoadAllFile()


#Load the data --> in MIP Model & MIP Model Sampel
#Loading data: InitialData.py


#Preprocessing 
#Aircraft Data: Aircraft.py, AircraftDatabase.py
#Hangar Data: HangarDatabase.py, Workshop.py
#Scheduling Data: Schedule.py


#Define sets and indexes
#Define index
#i = index of aircraft registration
#d = index of calendar day
#t = index of aircraft_profile
#city = index of city
#h = index of hangar
#k = index of maintenance type check
#intv = index of interval type
#d = index of calendar day

#Define sets
I = initial_data.aircraft_profile_df.index.values #set of aircraft registration
N = len(I) #number of aircraft fleet
T = initial_data.aircraft_profile['Type'].unique() #set of aircraft types
CITY = initial_data.hangar_profile_df['City'].unique() #set of city
H = initial_data.hangar_profile_df.index.values  #set of hangar code
K = initial_data.maintenance_data_df['Letter'].unique() #set of maintenance type check
INTV =  ['FH', 'FC', 'DY'] #set of interval types
D = initial_data.initial_flight_schedule_df['End Date'].unique() #set of calendar day indicator
F = initial_data.initial_flight_schedule_df['Start Loc'].unique() #set of node a
G = initial_data.initial_flight_schedule_df['End Loc'].unique() #set of node b
nc = sum(len(F) + len(G)) #set of nodes a and b


#Define parameters
#Parameters 1, 2, 3. maximum FH/FC/DY tolerance of type k check interval of aircraft type  t(i)
#limit_FH: self.limit_FH
#limit_FC: self.limit_FC
#limit_FD: self.limit_FD

#Parameters 4, 5. average daily FH and FC usage for aircraft i at day d
#avg_utilization_FH: self.avg_utilization_FH
#avg_utilization_FC: self.avg_utilization_FC

#Parameters 6, 7, 8. interval of type k check of aircraft type  t(i) in terms of FH/FC/DY
#interval_check_FH: self.interval_check_FH
#interval_check_FC: self.interval_check_FC
#interval_check_FD: self.interval_check_FD      

#Parameter 9 hangar capacity at city b on day d
#total_slot = self.total_slot
#effective_slot = effective_slot

#Parameter 10 grounded_penalty: daily penalty for having an aircraft on the ground waiting for a maintenance slot
#PR: grounded_penalty = pg = Biaya penalty = biaya operasional 1 hari / biaya per FH untuk pengerjaan maintenance 
#PR2: Atau pg = Big M

#Parameter 11 tolerance_penalty: penalty for an aircraft using the tolerance
#tolerance_penalty = pa = biaya administratif (ex: 3 million IDR/ biaya per FH untuk pengerjaan maintenance)

#Parameter 12 duration of check k for an aircraft type t(i)
#PR: maintenance_check_duration = masukkan di folder MaintenanceDatabase
#maintenance_duration = self.maintenance_duration

#Parameter 13 start time of aircraft i at city a on day d+〖∆t〗_(t(i),k)
#start_time = self.start_time

#Parameter 14 end time of aircraft i at city b on day d
#end_time = self.end_time

#Parameter 15 towing time from/to workshop h
##towing_time = self.towing_time

#Parameter 16 probability of available average monthly slots for workshop utilisation in month m
#probability = self.check_probs



#I. Create empty Model
m = gp.Model("MIP Model")

#II. Define decision variables
#The variable template: addVar (lb=0.0, ub=GRB.INFINITY, obj=0.0, vtype=GRB.CONTINUOUS, name="", column=None )
#x = [[model.add_var(name="x({} ,{})".format(j, t), var_type=BINARY) for t in T] for j in J]

#1. y routing decision variable
routing_var = m.addVars(I, F, G, D, vtype=GRB.BINARY, name='y')

#2. w urgency rate decision variable
urgency_rate_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='w')

#3. x premature and maintenance requirement decision variable
premature_requirement_var = m.addVars(I, K, G, D, vtype=GRB.BINARY, name='x')

#4. v violation decision variable
violation_var = m.addVars(I, K, D, vtype=GRB.BINARY, name='v')

#5. o hangar check status decision variable
hangar_check_status_var = m.addVars(I, K, H, G, D, vtype=GRB.BINARY, name='o')

#6. n grounded check status decision variable
grounded_check_status_var = m.addVars(I, D, vtype=GRB.BINARY, name='n')
 
#7. dy total days decision variable
total_days_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='dy')

#8. fh total fh decision variable
total_fh_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='fh')

#9. fc total fc decision variable
total_fc_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='fc')

#10. e-dy extra days decision variable
extra_days_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-dy' )

#11. e-fh extra fh decision variable
extra_fh_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-fh' )

#12. e-fc extra fc decision variable
extra_fc_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='e-fc' )

#13. teta tolerance rate decision variable
tolerance_rate_var = m.addVars(I, K, D, lb=0.0, ub=GRB.INFINITY, vtype=GRB.CONTINUOUS, name='teta')

#gam maintenance check status decision variable
#maintenance_check_status_var = m.addVars(I, K, G, D, vtype=GRB.BINARY, name='gam')

#III. Set objective function
m.setObjective(sum(violation_var[i][k][d] for i in I for k in K for d in D), GRB.MINIMIZE)
#TO DO LIST: m.setObjective(minimize unused FH)
#Example: m.setObjective(sum(buy[f]*cost[f] for f in foods), GRB.MINIMIZE)

#IV. Define constraints
#1. Constraint 1: One arc will depart from every airport(city) a
routing_var = []
m.addConstr(
    routing_var(I, F, G, D) == 1 for i in F for a in F for b in G for d in D), "node")
    

#for i in I:
#    routing_var.append([])
#    for a in F:
#        for d in D:
#            routing_var[b].append(m.add)
    
#    for a in F:
#        routing_var.append([]) 
#            routing_var
#        routing_var[a].append([])
        

#for a in F:
#    for b in G:
#        for d in D:
#            m.addConstr(sum(routing_var[I, F, G, D] == 1 for i  ))
            
#m.addConstrs(
#    (flow.sum('*',i,j) <= capacity[i,j] for i,j in arcs), "cap")

#m.addConstrs(
#    (flow.sum('*',i,j) <= capacity[i,j] for i,j in arcs), "cap")

# Equivalent version using Python looping
# for i,j in arcs:
#   m.addConstr(sum(flow[h,i,j] for h in commodities) <= capacity[i,j],
#               "cap[%s,%s]" % (i, j))

    
#transport = []
#for w in warehouses:
#  transport.append([])
#  for p in plants:
#    transport[w].append(m.addVar(obj=transCosts[w][p],
#                                 name="trans[%d,%d]" % (w, p)))  
m.addConstr()



#m.addConstrs(
#    (quicksum(nutritionValues[f,c] * buy[f] for f in foods)
#    	== [minNutrition[c], maxNutrition[c]]
#     for c in categories), "_")


#V. Save model
m.write('mipmodel1.lp')

#VI. Optimize
#m.optimize()
#status = m.status
#if status == GRB.Status.UNBOUNDED:
#    print('The model cannot be solved because it is unbounded')
#    exit(0)
#if status == GRB.Status.OPTIMAL:
#    print('The optimal objective is %g' % m.objVal)
#    exit(0)
#if status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
#    print('Optimization was stopped with status %d' % status)
#    exit(0)

#VII. IIS
#print('The model is infeasible; computing IIS')
#m.computeIIS()
#if m.IISMinimal:
#  print('IIS is minimal\n')
#else:
#  print('IIS is not minimal\n')
#print('\nThe following constraint(s) cannot be satisfied:')
#for c in m.getConstrs():
#    if c.IISConstr:
#        print('%s' % c.constrName)